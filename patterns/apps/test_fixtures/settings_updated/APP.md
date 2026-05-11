---
version: 1
app: Settings (Updated)
spotlight_name: Settings (Updated)
icon: ⚙
---

# Settings (Updated)

Test fixture: an "altered" Settings screen with different rows. Used by
assertion-drift tests that compile assertions against the canonical Settings
screen, then verify the assertions detect the change here.

## Simulator
- root: main

## Simulator Screen main
- title: Settings
- back: null
- tab_bar: true
- element row: "Accessibility"
- element row: "Sounds"
- element row: "Wallpaper"
- element row: "Battery"
- element row: "Storage"
- element row: "Notifications"
