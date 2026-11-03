---
version: 1
name: Play the Chess.com Computer
app: Chess
kind: game
surface: scene
playable: single-control
controls: [board]
decider: required
image_width: 800
budget: { max_frames: 240, max_tokens: 1500000, max_seconds: 2400 }
success: { visible: "Vous avez battu" }
fail: { visible: ["a gagné", "Jouer contre des bots"] }
ios_min: "17.0"
locale: "fr_CA"
tags: ["chess", "chess-com", "game", "scene", "board", "decider", "stockfish"]
---

Play one game against a Chess.com computer bot on a stock iPhone, every
move chosen by an external move picker. The vision model only reads the board;
the picker the scenario step names (`decider:`) chooses each move and answers
the two board cells to tap. `decider/sf_decider.py` next to this skill is a
Stockfish picker for it.

Precondition: a game against the computer is open with the board on screen and
no move played yet. Reach it by hand: Jouer → Jouer contre des bots → set the
strength slider → pick a side → Jouer → "Continuer vers la partie" when the
upgrade offer shows (never "Essayez pour 0,00 $" or "Jouez sans publicités").
The playing side is at the bottom of the board, whichever colour it is.

The scenario that plays it names the picker, never this skill: after targeting
the "Chess" app it holds one step,
`scene: { skill: play-computer, decider: "<path>/decider/sf_decider.py --color auto --movetime 3000" }`,
where a relative path resolves against the scenario's own folder. Keep the
scenario outside this skills tree: every YAML here is read as a skill.

A checkmate win opens a popup over the board reading "Vous avez battu", then
the bot's name, then "par échec et mat" (seen on device): that text is the
success predicate. "Échec et mat" alone is not, since it shows when the bot
mates too. A loss by checkmate opens a popup reading "<bot> a gagné", then
"par échec et mat" (seen on device against Maximum), which the win text does
not contain; a resignation shows no popup at all, only a flag on
the losing king. The app dropping back to the bot list ("Jouer contre des
bots", seen once mid-game on device) also fails the run; the fail predicates
are read first. A draw matches neither and ends on the
budget as inconclusive. A frame the picker cannot place (a misread board, the
bot still thinking) is a wait: no touch, and the next frame reads the board
again.

## Objective

Read the chess board exactly as it appears on screen. Answer the 8 rows from
the top of the board to the bottom, separated by "/", each row read left to
right, in FEN piece letters: K Q R B N P for white pieces, k q r b n p for
black pieces, and a digit for a run of empty squares (each row adds up to 8).
Report the board as drawn, not from either player's point of view: if black's
pieces are at the bottom, the bottom row comes last as drawn. Ignore the yellow
last-move highlight, arrows, coordinates and captured-piece trays. Answer only
the 8 rows, for example
"rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR". Do not choose a move.

## Controls

Calibrated on the live Chess.com board, portrait mirror window 430x930: the
board runs from (8, 325) to (422, 739) in window points.

- board: grid 8x8 from 0.019,0.349 to 0.981,0.795
