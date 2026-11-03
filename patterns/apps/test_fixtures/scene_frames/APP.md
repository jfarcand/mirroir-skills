---
version: 1
app: Scene Frames
spotlight_name: Scene Frames
icon: ▶
archetype: game
playable: single-control
---

# Scene Frames

## Structure

FakeMirroring fixture for the `scene:` step's loop mechanics: a playfield
reduced to a deterministic frame sequence. Every touch on MOVE or FIRE
advances exactly one frame, so a scene's frames, touches and verdict can be
asserted in CI without a game or a real model. FIRE on the first frame loses
(the fail predicate's DEFAITE), MOVE walks the frames to GOAL (the success
predicate) on the fourth. The last frames' buttons go nowhere, so a scene
that keeps playing stays put and spends its budget. No frame but the last
shows a word of a predicate: a `visible` predicate matches inside longer text. Its scene skills live
with the mcp sample that runs them: `runner/samples/game-scene/skills/`.

## Simulator
- root: f1

## Simulator Screen f1
- title: FRAME 1
- back: null
- tab_bar: false
- element text: "Keep moving"
- element button: "MOVE" → f2
- element button: "FIRE" → lose

## Simulator Screen f2
- title: FRAME 2
- back: null
- tab_bar: false
- element text: "Keep moving"
- element button: "MOVE" → f3
- element button: "FIRE" → f3

## Simulator Screen f3
- title: FRAME 3
- back: null
- tab_bar: false
- element text: "Keep moving"
- element button: "MOVE" → f4
- element button: "FIRE" → f4

## Simulator Screen f4
- title: FRAME 4
- back: null
- tab_bar: false
- element text: "GOAL"
- element button: "MOVE"
- element button: "FIRE"

## Simulator Screen lose
- title: FRAME 2
- back: null
- tab_bar: false
- element text: "DEFAITE"
- element button: "MOVE"
- element button: "FIRE"
