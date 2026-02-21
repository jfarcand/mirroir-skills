---
version: 1
name: Expo Go Debug Menu
app: Expo Go
ios_min: "17.0"
locale: "en_US"
tags: ["testing", "expo", "debug"]
---

Open the React Native debug menu via shake gesture in Expo Go

## Steps

1. Launch **Expo Go**
2. Wait for "${APP_SCREEN:-Home}" to appear
3. Tap "${APP_SCREEN:-Home}"
4. Shake the device
5. Wait for "Reload" to appear
6. Verify "Toggle Inspector" is visible
7. Screenshot: "debug_menu"
