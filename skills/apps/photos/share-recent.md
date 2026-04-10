---
version: 1
name: Share Recent Photo
app: Photos, Messages
ios_min: "17.0"
locale: "en_US"
tags: ["photos", "sharing", "long-press", "cross-app"]
---

Open the most recent photo, long-press to access the share menu, and send it via Messages. Demonstrates the long_press gesture and cross-app sharing flow.

## Steps

1. Launch **Photos**
2. Wait for "Library" to appear
3. Tap "Recents"
4. Wait for "Recents" to appear
5. long_press: "recent_photo"
6. Wait for "Share" to appear
7. Tap "Share"
8. Wait for "Messages" to appear
9. Tap "Messages"
10. Wait for "To:" to appear
11. Tap "To:"
12. Type "${RECIPIENT}"
13. Wait for "${RECIPIENT}" to appear
14. Tap "${RECIPIENT}"
15. Tap "Send"
16. Screenshot: "photo_shared"
