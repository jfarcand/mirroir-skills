#!/usr/bin/env python3
# ABOUTME: Stockfish move picker for the Chess.com scene skill: reads one frame's board on stdin, prints the cells to tap.
# ABOUTME: Keeps the game's last known position per run_id, so castling, en passant and misreads are handled by the picker.
"""Pick a chess move for a `scene:` step that declares `decider: required`.

mirroir-mcp runs this once per frame, with no shell, and writes one JSON
object to stdin:

    {"run_id": "...", "frame": 3, "reading": "<8 board rows as drawn>",
     "ocr": [...], "controls": [{"name": "board", "kind": "grid", ...}]}

It prints one action on stdout:

    {"control": "board", "cells": ["e2", "e4"]}        a move, two taps
    {"control": "board", "cells": ["e7", "e8", "e8"]}  a promotion (queen)
    {"control": "none"}                                no touch this frame

`reading` is the board as drawn on screen: 8 rows top to bottom, each left to
right, in FEN piece letters. Cells are screen cells too (a = left column,
1 = bottom row), so when black is at the bottom both are flipped here.

Each frame the reading is checked against the last known position:

- the same board as after our last move: the bot is thinking, wait;
- the board before our last move: our taps did not land, send the move again
  (at most MAX_RESENDS times, then wait);
- one legal bot move away: that move is applied with Stockfish, which keeps
  castling rights, en passant and the move clocks right, and our reply is
  chosen;
- anything else is a misread: wait for a fresh frame. After MAX_MISREADS
  misreads in a row the reading itself is trusted, so the game recovers from
  a position the picker lost track of.

State lives in $MIRROIR_DECIDER_STATE_DIR (default: the system temp directory)
as chess-decider-<run_id>.json, with a .log of every frame next to it.

Usage: sf_decider.py [--color white|black|auto] [--movetime MS] [--engine PATH]

--color auto (the default) takes the colour of the pieces at the bottom on the
first frame. --movetime is Stockfish's thinking time per move (default 3000):
keep it well inside the step's per-frame picker timeout (30 s at most).
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

START_PLACEMENT = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
START_FEN = START_PLACEMENT + " w KQkq - 0 1"
MAX_RESENDS = 2
MAX_MISREADS = 3
DEFAULT_MOVETIME_MS = 3000
ENGINE_FALLBACKS = ("/opt/homebrew/bin/stockfish", "/usr/local/bin/stockfish",
                    "/usr/games/stockfish")
ROW_PATTERN = re.compile(r"[pnbrqkPNBRQK1-8]{1,8}(?:/[pnbrqkPNBRQK1-8]{1,8}){7}")
WAIT = {"control": "none"}


class DeciderError(Exception):
    """A frame the picker cannot answer at all (no engine, bad input)."""


# --------------------------------------------------------------------------
# Board text: parsing the reading, flipping between screen and board.
# --------------------------------------------------------------------------

def expand_row(row):
    """'4P3' -> '....P...'; None when the row does not add up to 8 squares."""
    out = []
    for ch in row:
        out.append("." * int(ch) if ch.isdigit() else ch)
    squares = "".join(out)
    return squares if len(squares) == 8 else None


def compress_row(squares):
    """'....P...' -> '4P3'."""
    out, empty = [], 0
    for ch in squares:
        if ch == ".":
            empty += 1
            continue
        if empty:
            out.append(str(empty))
            empty = 0
        out.append(ch)
    if empty:
        out.append(str(empty))
    return "".join(out)


def parse_reading(reading):
    """The 8 drawn rows (expanded, top to bottom) found in the model's text, or None."""
    if not isinstance(reading, str):
        return None
    match = ROW_PATTERN.search(reading.replace(" ", ""))
    if not match:
        return None
    rows = [expand_row(row) for row in match.group(0).split("/")]
    if any(row is None for row in rows):
        return None
    return rows


def bottom_color(rows):
    """'white' when white's pieces sit mostly in the bottom half as drawn."""
    def count(half, upper):
        return sum(1 for row in half for ch in row if ch != "." and ch.isupper() == upper)
    white_low = count(rows[4:], True)
    black_low = count(rows[4:], False)
    return "white" if white_low >= black_low else "black"


def placement_from_screen(rows, color):
    """FEN piece placement (rank 8 first) from the drawn rows of a board whose
    bottom is `color`'s side."""
    if color == "black":
        rows = [row[::-1] for row in reversed(rows)]
    return "/".join(compress_row(row) for row in rows)


def screen_cell(square, color):
    """Board square 'e2' -> the screen cell to tap ('e2' for white, 'd7' for black)."""
    if color == "white":
        return square
    file_index = ord(square[0]) - ord("a")
    rank = int(square[1])
    return chr(ord("h") - file_index) + str(9 - rank)


def plausible(placement):
    """One king each and no pawn on the first or last rank: anything else would
    be a misread that could crash the engine."""
    if placement.count("K") != 1 or placement.count("k") != 1:
        return False
    ranks = placement.split("/")
    return not any(ch in "Pp" for ch in ranks[0] + ranks[7])


def castling_from(placement, previous="KQkq"):
    """Castling rights still possible on this board, never more than `previous` had."""
    rows = [expand_row(row) for row in placement.split("/")]
    rank1, rank8 = rows[7], rows[0]
    rights = ""
    if "K" in previous and rank1[4] == "K" and rank1[7] == "R":
        rights += "K"
    if "Q" in previous and rank1[4] == "K" and rank1[0] == "R":
        rights += "Q"
    if "k" in previous and rank8[4] == "k" and rank8[7] == "r":
        rights += "k"
    if "q" in previous and rank8[4] == "k" and rank8[0] == "r":
        rights += "q"
    return rights or "-"


# --------------------------------------------------------------------------
# Stockfish over UCI.
# --------------------------------------------------------------------------

def find_engine(explicit):
    for candidate in (explicit, os.environ.get("STOCKFISH"), shutil.which("stockfish"),
                      *ENGINE_FALLBACKS):
        if candidate and os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    raise DeciderError("stockfish not found: pass --engine or set STOCKFISH")


class Engine:
    """One Stockfish process for the frame."""

    def __init__(self, path):
        self.proc = subprocess.Popen([path], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL, text=True, bufsize=1)
        self._send("uci")
        self._until(lambda line: line == "uciok")
        self._send("isready")
        self._until(lambda line: line == "readyok")

    def _send(self, command):
        self.proc.stdin.write(command + "\n")
        self.proc.stdin.flush()

    def _until(self, done):
        lines = []
        for raw in self.proc.stdout:
            line = raw.strip()
            lines.append(line)
            if done(line):
                return lines
        raise DeciderError("stockfish exited mid-answer")

    def legal_moves(self, fen):
        self._send(f"position fen {fen}")
        self._send("go perft 1")
        lines = self._until(lambda line: line.startswith("Nodes searched"))
        return [line.split(":")[0] for line in lines if re.match(r"^[a-h][1-8][a-h][1-8][qrbn]?:", line)]

    def fen_after(self, fen, move):
        self._send(f"position fen {fen} moves {move}")
        self._send("d")
        lines = self._until(lambda line: line.startswith("Checkers:"))
        for line in lines:
            if line.startswith("Fen: "):
                return line[len("Fen: "):]
        raise DeciderError("stockfish printed no Fen")

    def best_move(self, fen, movetime_ms):
        self._send(f"position fen {fen}")
        self._send(f"go movetime {movetime_ms}")
        lines = self._until(lambda line: line.startswith("bestmove"))
        move = lines[-1].split()[1]
        return None if move == "(none)" else move

    def close(self):
        try:
            self._send("quit")
            self.proc.wait(timeout=2)
        except (BrokenPipeError, subprocess.TimeoutExpired):
            self.proc.kill()


def placement_of(fen):
    return fen.split()[0]


def side_of(fen):
    return "white" if fen.split()[1] == "w" else "black"


# --------------------------------------------------------------------------
# State per scene run.
# --------------------------------------------------------------------------

def state_paths(run_id):
    base = os.environ.get("MIRROIR_DECIDER_STATE_DIR") or tempfile.gettempdir()
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", str(run_id))[:120] or "run"
    stem = os.path.join(base, f"chess-decider-{safe}")
    return stem + ".json", stem + ".log"


def load_state(path):
    try:
        with open(path) as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def save_state(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w") as handle:
        json.dump(state, handle)
    os.replace(tmp, path)


def log(path, message):
    try:
        with open(path, "a") as handle:
            handle.write(message + "\n")
    except OSError:
        pass


# --------------------------------------------------------------------------
# The decision.
# --------------------------------------------------------------------------

def move_action(move, color, why):
    """The board cells to tap for UCI `move`; a promotion taps the target twice
    (Chess.com's picker opens on the target square with the queen there)."""
    cells = [screen_cell(move[0:2], color), screen_cell(move[2:4], color)]
    if len(move) == 5:
        cells.append(cells[1])
    return {"control": "board", "cells": cells, "rationale": why}


def queen_promotion(move):
    """v1 always promotes to a queen, the piece the double tap picks."""
    return move[:4] + "q" if len(move) == 5 else move


def play(engine, fen, state, movetime_ms, why):
    """Choose our move from `fen` (our turn), record it, and return the action."""
    move = engine.best_move(fen, movetime_ms)
    if move is None:
        state.update(before=fen, after=None, move=None, resends=0)
        return dict(WAIT, rationale=f"{why}; no legal move, the game is over")
    move = queen_promotion(move)
    after = engine.fen_after(fen, move)
    state.update(before=fen, after=after, move=move, resends=0, misreads=0)
    return move_action(move, state["color"], f"{why}; playing {move}")


def decide(frame, engine, state, movetime_ms, requested_color):
    """One frame: returns (action, state). `state` is None on a run's first frame."""
    rows = parse_reading(frame.get("reading"))
    if rows is None:
        if state is not None:
            state["misreads"] = state.get("misreads", 0) + 1
        return dict(WAIT, rationale="no 8x8 board in the reading"), state

    if state is None:
        color = bottom_color(rows) if requested_color == "auto" else requested_color
        state = {"color": color, "before": None, "after": None, "move": None,
                 "resends": 0, "misreads": 0}
        placement = placement_from_screen(rows, color)
        if placement == START_PLACEMENT:
            if color == "white":
                return play(engine, START_FEN, state, movetime_ms, "first move as white"), state
            state["after"] = START_FEN
            return dict(WAIT, rationale="playing black, white moves first"), state
        if not plausible(placement):
            return dict(WAIT, rationale="first board is not a legal position"), state
        side = "w" if color == "white" else "b"
        fen = f"{placement} {side} {castling_from(placement)} - 0 1"
        return play(engine, fen, state, movetime_ms, "joined a game in progress"), state

    placement = placement_from_screen(rows, state["color"])
    after = state.get("after")
    before = state.get("before")

    if after and placement == placement_of(after):
        state["misreads"] = 0
        return dict(WAIT, rationale="board unchanged since our move, the bot is thinking"), state

    if before and state.get("move") and placement == placement_of(before):
        if state.get("resends", 0) < MAX_RESENDS:
            state["resends"] = state.get("resends", 0) + 1
            return move_action(state["move"], state["color"],
                               f"our {state['move']} did not land, sending it again"), state
        return dict(WAIT, rationale=f"{state['move']} still not on the board after resends"), state

    if after and side_of(after) != state["color"]:
        for reply in engine.legal_moves(after):
            reached = engine.fen_after(after, reply)
            if placement_of(reached) == placement:
                return play(engine, reached, state, movetime_ms, f"the bot played {reply}"), state

    state["misreads"] = state.get("misreads", 0) + 1
    if state["misreads"] < MAX_MISREADS or not plausible(placement):
        return dict(WAIT, rationale=f"board is not one bot move from the last position "
                                    f"(misread {state['misreads']}), reading again"), state
    previous = after.split()[2] if after else "KQkq"
    side = "w" if state["color"] == "white" else "b"
    fen = f"{placement} {side} {castling_from(placement, previous)} - 0 1"
    return play(engine, fen, state, movetime_ms,
                f"trusting the reading after {state['misreads']} misreads"), state


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--color", choices=("white", "black", "auto"), default="auto")
    parser.add_argument("--movetime", type=int, default=DEFAULT_MOVETIME_MS)
    parser.add_argument("--engine")
    args = parser.parse_args(argv)

    try:
        frame = json.loads(sys.stdin.read())
    except ValueError as error:
        sys.stderr.write(f"sf_decider: stdin is not JSON: {error}\n")
        return 2
    state_path, log_path = state_paths(frame.get("run_id", "run"))
    engine = Engine(find_engine(args.engine))
    try:
        action, state = decide(frame, engine, load_state(state_path), args.movetime, args.color)
    finally:
        engine.close()
    if state is not None:
        save_state(state_path, state)
    log(log_path, json.dumps({"frame": frame.get("frame"), "reading": frame.get("reading"),
                              "action": action}))
    print(json.dumps(action))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except DeciderError as error:
        sys.stderr.write(f"sf_decider: {error}\n")
        sys.exit(1)
