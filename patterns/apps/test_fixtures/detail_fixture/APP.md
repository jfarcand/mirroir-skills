---
version: 1
app: Detail
spotlight_name: Detail
icon: ⌂
---

# Detail

Test fixture: a "drilled down" screen with a few rows but no back chevron.
Used to mirror the legacy `detail` FakeScenario that simulated being mid-way
through a Settings drill-down.

## Simulator
- root: detail

## Simulator Screen detail
- title: General
- back: null
- tab_bar: false
- element row: "About"
- element row: "Software Update"
- element row: "Storage"
- element row: "Background App Refresh"
- element row: "Date & Time"
- element row: "Keyboard"
