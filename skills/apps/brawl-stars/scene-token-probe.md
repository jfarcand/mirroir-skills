---
version: 1
name: Scene Token Probe
app: Brawl Stars
kind: game
surface: scene
playable: single-control
controls: [move, fire]
budget: { max_frames: 12, est_tokens: 2700, max_minutes: 4 }
ios_min: "17.0"
locale: "fr_CA"
tags: ["brawl-stars", "game", "scene", "experiment", "token-cost"]
---

A bounded cost probe for the gaming-scene model loop — NOT a game to win. It
drives at most 12 frames of single-control movement at the start of one Brawl
Stars match, then stops, so the real per-frame vision-token cost can be measured
against the ~2700-token/frame model (Surface E / carnet #22). It never tries to
win, and it uses one control at a time: stock single-touch cannot do a
simultaneous move+aim, which is why `playable: single-control`.

Precondition: a match has just started and the playfield (scene) is on-screen,
in landscape. Enter the match by hand (tap JOUER on the main-menu shell) — a
shell skill never does this, and this probe starts from an already-live scene.

## Control map (absolute window px, landscape)

Approximate anchors — **calibrate on-device before the first run**. Positions
scale with the mirror window size, so confirm them with `calibrate_component`
or a `describe_screen` on the live scene first:

- move: the left virtual joystick, rest center ≈ (18% width, 80% height). Drag
  from the center toward a heading to move; release to stop.
- fire: the right attack control, ≈ (85% width, 72% height). Tap to fire
  straight, drag-and-release to aim. Used only between moves, never during one.

## Objective

Capture up to `max_frames` (12) frames while nudging `move` with one short drag
per frame in a safe direction (away from the nearest wall). Stop at 12 frames,
or earlier if the result screen ("QUITTER") appears. The goal is a clean
per-frame cost measurement, not progress in the match.

## Success

The run succeeds when it completes within budget: at most 12 frames, at most
`max_minutes`, and total vision tokens within ~20% of `max_frames * est_tokens`.
Winning or surviving is explicitly out of scope.

## Steps

1. Verify the scene is on-screen (landscape playfield, not the shell).
2. Capture a frame (`screenshot`, using the region/scale lever to cut cost).
3. Perform one short `move` drag in a safe direction.
4. Repeat steps 2-3 until 12 frames are captured or "QUITTER" appears.
5. Stop. Report frames captured, elapsed time, and total vision tokens.
