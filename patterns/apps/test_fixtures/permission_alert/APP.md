---
version: 1
app: Permission Alert
spotlight_name: Permission Alert
icon: ⚠
---

# Permission Alert

Test fixture: a screen that immediately shows a permission-style modal so
tests for obstacle detection and dismissal can run in isolation.

## Simulator
- root: host

## Simulator Screen host
- title: App
- back: null
- tab_bar: false
- element text: "Background content"

## Simulator Obstacle camera_perm
- title: "Allow access to camera?"
- body: "App needs camera access to take photos."
- buttons: Allow, Don't Allow
- trigger: on_first_describe
