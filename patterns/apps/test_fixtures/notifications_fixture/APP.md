---
version: 1
app: Notifications
spotlight_name: Notifications
icon: ◉
---

# Notifications

Test fixture: a Notifications-style settings screen (different from the
real Settings notification sub-screen) used by integration tests that
specifically reference the legacy `Notifications` FakeScenario name.

## Simulator
- root: notif

## Simulator Screen notif
- title: Notifications
- back: null
- tab_bar: false
- element row: "Allow Notifications"
- element row: "Show on Lock Screen"
- element row: "Banners"
- element row: "Sounds"
- element row: "Badges"
