---
version: 1
app: Grid Frames
spotlight_name: Grid Frames
icon: ▦
archetype: game
playable: single-control
---

# Grid Frames

## Structure

FakeMirroring fixture for a board game in the `scene:` step: one 3x3 board of
equal cells, named by screen position (column letter from the left, row number
from the bottom, so `a1` is bottom-left and `c3` top-right). Each frame takes
one move of cell taps. On the first frame only `a1` goes anywhere: it leads to
the second frame, every other cell stays put. On the second frame `c3` shows
GOAL (the success predicate) and every other cell shows DEFAITE (the fail
predicate). So the move `a1`, `c3` passes in one frame and `a1`, `b2` fails.
Only the goal and lose frames show a word of a predicate (a `visible` predicate
matches inside longer text); the cell labels never do. Their boards go nowhere,
so a scene that keeps playing stays put. The board fills the 300pt square at view points (55,200)-(355,500), which
a scene skill's grid control calibrates as window fractions. Its scene skills
live with the mcp sample that runs them: `runner/samples/board-scene/skills/`.

## Simulator
- root: g1

## Simulator Screen g1
- title: Pick a square
- back: null
- tab_bar: false
- element grid: 3x3
- element cell: a1 → g2

## Simulator Screen g2
- title: Pick again
- back: null
- tab_bar: false
- element grid: 3x3
- element cell: a1 → lose
- element cell: a2 → lose
- element cell: a3 → lose
- element cell: b1 → lose
- element cell: b2 → lose
- element cell: b3 → lose
- element cell: c1 → lose
- element cell: c2 → lose
- element cell: c3 → goal

## Simulator Screen goal
- title: GOAL
- back: null
- tab_bar: false
- element grid: 3x3

## Simulator Screen lose
- title: DEFAITE
- back: null
- tab_bar: false
- element grid: 3x3
