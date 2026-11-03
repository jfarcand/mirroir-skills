---
version: 1
name: Scene Token Probe
app: Brawl Stars
kind: game
surface: scene
playable: single-control
controls: [move, fire]
budget: { max_frames: 12, max_tokens: 288000, max_seconds: 240 }
success: { visible: "QUITTER" }
fail: { visible: "Vaincu" }
ios_min: "17.0"
locale: "fr_CA"
tags: ["brawl-stars", "game", "scene", "experiment", "token-cost"]
---

A bounded cost probe for the gaming-scene model loop — NOT a game to win. It
plays at most 12 frames, one touch per frame, at the start of one Brawl Stars
match, so the real per-frame vision-token cost can be measured against its
`max_tokens` budget. It uses one control at a time: stock single-touch cannot
do a simultaneous move+aim, which is why `playable: single-control`.

Precondition: a match has just started and the playfield is on-screen, in
landscape. Enter the match by hand (tap JOUER on the main-menu shell) — a shell
skill never does this, and this probe starts from an already-live scene.

"QUITTER" is on every result screen, so success means the match reached its
result inside the budget. An eliminated brawler shows "Vaincu" before the
result screen, and the fail predicate is read first, so a loss never passes.
Twelve frames from a match's start rarely get there: the expected verdict is
inconclusive on `max_frames`, which is the cost measurement this probe exists
for. Measured on device: about 400 prompt and 250 completion tokens per frame.

## Objective

Keep your brawler alive and moving through the arena: move away from walls and
toward open ground, and fire only when an enemy brawler is close in front of
you. Winning is not required.

## Controls

Calibrated on a live Showdown playfield, landscape mirror window 912x460.

- move: drag from 0.420,0.552 radius 0.12
- fire: tap at 0.840,0.661
