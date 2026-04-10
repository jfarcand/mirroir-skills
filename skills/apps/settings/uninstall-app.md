---
version: 1
name: Uninstall App
app: Settings
ios_min: "17.0"
locale: "en_US"
tags: ["settings", "apps", "uninstall", "destructive"]
---

Remove an app via Settings > General > iPhone Storage. More reliable than the home screen long-press method because the app list is text-based and OCR-friendly. Handles the confirmation dialog automatically.

## Steps

1. Launch **Settings**
2. Wait for "General" to appear
3. Tap "General"
4. Wait for "iPhone Storage" to appear
5. Tap "iPhone Storage"
6. Wait for "iPhone Storage" to appear
7. Scroll until "${APP_NAME}" is visible
8. Tap "${APP_NAME}"
9. Wait for "Delete App" to appear
10. Tap "Delete App"
11. Wait for "Delete App" to appear
12. Tap "Delete App"
13. Screenshot: "app_deleted"
