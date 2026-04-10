---
version: 1
name: Visual Regression Test
app: Expo Go
ios_min: "17.0"
locale: "en_US"
tags: ["testing", "qa", "screenshots", "remember", "regression"]
---

Capture screenshots of key app screens for visual regression testing. Navigates a configurable path through the app, capturing and describing each screen. Uses remember to detect unexpected UI changes — something traditional screenshot diffing can't do.

## Steps

1. Launch **Expo Go**
2. Wait for "${APP_SCREEN:-Home}" to appear
3. Tap "${APP_SCREEN:-Home}"
4. Wait for "${LANDING_LABEL:-Welcome}" to appear
5. Verify "${LANDING_LABEL:-Welcome}" is visible
6. Remember: Describe the landing screen layout — note all visible elements, their positions, and any error indicators.
7. Screenshot: "regression_01_landing"
8. Tap "${SCREEN_1_TAP:-Profile}"
9. Wait for "${SCREEN_1_LABEL:-Profile}" to appear
10. Remember: Describe the screen layout and compare with expected elements: navigation bar, content area, any error states.
11. Screenshot: "regression_02_profile"
12. Tap "${SCREEN_2_TAP:-Settings}"
13. Wait for "${SCREEN_2_LABEL:-Settings}" to appear
14. Remember: Check for any visual anomalies — missing icons, truncated text, layout overflow, or unexpected empty states.
15. Screenshot: "regression_03_settings"
