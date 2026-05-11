---
version: 1
app: Detail (Back)
spotlight_name: Detail (Back)
icon: ⌂
---

# Detail (Back)

Test fixture: a "drilled down" screen with a back chevron (`back: home`)
so backtracker / OCR-chevron tests have a known target.

## Simulator
- root: detail

## Simulator Screen home
- title: Home
- back: null
- tab_bar: false
- element row: "Item One" → detail
- element row: "Item Two" → detail

## Simulator Screen detail
- title: General
- back: home
- element row: "About"
- element row: "Software Update"
- element row: "Storage"
- element row: "Background App Refresh"
