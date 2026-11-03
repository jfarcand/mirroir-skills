# ABOUTME: Tests for the Stockfish move picker: board parsing and flipping, and frame-by-frame decisions against real Stockfish.
# ABOUTME: Run with `python3 -m unittest discover -s skills/apps/chess-com/decider`; needs stockfish on PATH or in STOCKFISH.
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sf_decider as sf  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
START_ROWS = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
MOVETIME = 100


def flip_rows(placement):
    """The drawn rows of a board whose bottom is black, from a FEN placement."""
    rows = [sf.expand_row(row) for row in placement.split("/")]
    return "/".join(sf.compress_row(row[::-1]) for row in reversed(rows))


def frame(reading, number=1, run_id="t"):
    return {"run_id": run_id, "frame": number, "reading": reading, "ocr": [],
            "controls": [{"name": "board", "kind": "grid", "cols": 8, "rows": 8}]}


class BoardTextTests(unittest.TestCase):
    def test_parse_finds_rows_inside_prose(self):
        rows = sf.parse_reading('The board: "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR".')
        self.assertEqual(rows[4], "....P...")

    def test_parse_rejects_a_row_that_does_not_add_up(self):
        self.assertIsNone(sf.parse_reading("rnbqkbnr/ppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"))

    def test_black_at_bottom_flips_to_fen_placement(self):
        rows = sf.parse_reading(flip_rows(START_ROWS))
        self.assertEqual(sf.bottom_color(rows), "black")
        self.assertEqual(sf.placement_from_screen(rows, "black"), START_ROWS)

    def test_screen_cells_flip_for_black(self):
        self.assertEqual(sf.screen_cell("e2", "white"), "e2")
        self.assertEqual(sf.screen_cell("e7", "black"), "d2")
        self.assertEqual(sf.screen_cell("a1", "black"), "h8")

    def test_implausible_board_is_refused(self):
        self.assertFalse(sf.plausible("8/8/8/8/8/8/8/8"))
        self.assertFalse(sf.plausible("P3k3/8/8/8/8/8/8/4K3"))
        self.assertTrue(sf.plausible("4k3/8/8/8/8/8/8/4K3"))

    def test_castling_never_grows(self):
        self.assertEqual(sf.castling_from(START_ROWS, "Kq"), "Kq")
        self.assertEqual(sf.castling_from("4k3/8/8/8/8/8/8/4K3"), "-")


class DecideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = sf.Engine(sf.find_engine(None))

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def decide(self, reading, state, color="auto"):
        return sf.decide(frame(reading), self.engine, state, MOVETIME, color)

    def test_white_opens_with_a_legal_move(self):
        action, state = self.decide(START_ROWS, None)
        self.assertEqual(state["color"], "white")
        self.assertEqual(action["control"], "board")
        self.assertIn(state["move"], self.engine.legal_moves(sf.START_FEN))
        self.assertEqual(action["cells"], [state["move"][:2], state["move"][2:4]])

    def test_black_waits_for_white_then_answers_in_screen_cells(self):
        action, state = self.decide(flip_rows(START_ROWS), None)
        self.assertEqual(action["control"], "none")
        self.assertEqual(state["color"], "black")
        after_e4 = self.engine.fen_after(sf.START_FEN, "e2e4")
        action, state = self.decide(flip_rows(sf.placement_of(after_e4)), state)
        self.assertEqual(action["control"], "board")
        move = state["move"]
        self.assertEqual(action["cells"][0], sf.screen_cell(move[:2], "black"))

    def test_unchanged_board_after_our_move_waits(self):
        _, state = self.decide(START_ROWS, None)
        action, state = self.decide(sf.placement_of(state["after"]), state)
        self.assertEqual(action["control"], "none")

    def test_move_that_did_not_land_is_resent_then_given_up(self):
        _, state = self.decide(START_ROWS, None)
        move = state["move"]
        for _ in range(sf.MAX_RESENDS):
            action, state = self.decide(START_ROWS, state)
            self.assertEqual(action["cells"][:2], [move[:2], move[2:4]])
        action, state = self.decide(START_ROWS, state)
        self.assertEqual(action["control"], "none")

    def test_bot_reply_is_found_and_answered(self):
        _, state = self.decide(START_ROWS, None)
        reply = self.engine.legal_moves(state["after"])[0]
        reached = self.engine.fen_after(state["after"], reply)
        action, state = self.decide(sf.placement_of(reached), state)
        self.assertEqual(action["control"], "board")
        self.assertIn(state["move"], self.engine.legal_moves(reached))

    def test_misread_waits_then_trusts_the_reading(self):
        _, state = self.decide(START_ROWS, None)
        odd = "rnbqkbnr/pppp1ppp/8/4p3/3PP3/8/PPP2PPP/RNBQKBNR"
        for _ in range(sf.MAX_MISREADS - 1):
            action, state = self.decide(odd, state)
            self.assertEqual(action["control"], "none")
        action, state = self.decide(odd, state)
        self.assertEqual(action["control"], "board")
        self.assertTrue(state["before"].startswith(odd + " w "))

    def test_promotion_taps_the_target_twice_and_is_always_a_queen(self):
        self.assertEqual(sf.queen_promotion("e7e8n"), "e7e8q")
        self.assertEqual(sf.move_action("e7e8q", "white", "t")["cells"], ["e7", "e8", "e8"])
        self.assertEqual(sf.move_action("d2d1q", "black", "t")["cells"], ["e7", "e8", "e8"])
        fen = "8/4P3/8/8/8/8/k7/4K3 w - - 0 1"
        self.assertTrue(self.engine.fen_after(fen, "e7e8q").startswith("4Q3/"))


class ProcessTests(unittest.TestCase):
    """The script as mirroir-mcp runs it: JSON in on stdin, one action out."""

    def run_frame(self, payload, state_dir):
        env = dict(os.environ, MIRROIR_DECIDER_STATE_DIR=state_dir)
        result = subprocess.run([sys.executable, os.path.join(HERE, "sf_decider.py"),
                                 "--movetime", str(MOVETIME)],
                                input=payload, capture_output=True, text=True, env=env,
                                timeout=30)
        return result

    def test_two_frames_share_state_through_run_id(self):
        with tempfile.TemporaryDirectory() as state_dir:
            first = self.run_frame(json.dumps(frame(START_ROWS, 1, "run-1")), state_dir)
            self.assertEqual(first.returncode, 0, first.stderr)
            action = json.loads(first.stdout)
            self.assertEqual(action["control"], "board")
            with open(os.path.join(state_dir, "chess-decider-run-1.json")) as handle:
                state = json.load(handle)
            second = self.run_frame(
                json.dumps(frame(sf.placement_of(state["after"]), 2, "run-1")), state_dir)
            self.assertEqual(json.loads(second.stdout)["control"], "none")
            self.assertTrue(os.path.exists(os.path.join(state_dir, "chess-decider-run-1.log")))

    def test_bad_stdin_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as state_dir:
            result = self.run_frame("not json", state_dir)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
