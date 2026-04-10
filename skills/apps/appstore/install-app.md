---
version: 1
name: Install App from App Store
app: App Store
ios_min: "17.0"
locale: "en_US"
tags: ["appstore", "install", "conditional"]
---

Search for an app in the App Store and install it. The AI handles dynamic UI — search results, GET vs price button, download progress, and authentication prompts. Uses condition to adapt to whether the app is free, paid, or already installed.

## Steps

1. Launch **App Store**
2. Wait for "Search" to appear
3. Tap "Search"
4. Wait for "Search" to appear
5. Tap "Search"
6. Type "${APP_NAME}"
7. Press **Return**
8. Wait for "${APP_NAME}" to appear
9. Tap "${APP_NAME}"
10. Wait for "GET" to appear
11. If "OPEN" is visible:
   1. Remember: App is already installed. Note the current version.
   2. Screenshot: "already_installed"
   Otherwise:
   1. Tap "GET"
   2. Wait for "OPEN" to appear
   3. Verify "OPEN" is visible
   4. Screenshot: "install_complete"
