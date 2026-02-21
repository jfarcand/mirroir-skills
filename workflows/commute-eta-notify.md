---
version: 1
name: Commute ETA Notification
app: Waze, Messages
ios_min: "17.0"
locale: "fr_CA"
tags: ["workflow", "cross-app", "waze", "messages", "commute"]
---

Get commute ETA from Waze, then send it via iMessage. Demonstrates cross-app data extraction — the AI reads dynamic content from one app and composes it into a message in another.

> Note: --- Waze: get the ETA ---
> Note: --- Messages: compose and send ---

## Steps

1. Launch **Waze**
2. Wait for "Où va-t-on ?" to appear
3. Tap "Où va-t-on ?"
4. Wait for "${DESTINATION:-Travail}" to appear
5. Tap "${DESTINATION:-Travail}"
6. Wait for "Y aller" to appear
7. Tap "Y aller"
8. Wait for "min" to appear
9. Remember: Read the commute time (e.g. '57 min') and ETA (e.g. '17:08') from the navigation screen. You will insert both into a message.
10. Screenshot: "eta_screen"
11. Press Home
12. Launch **Messages**
13. Wait for "Messages" to appear
14. Tap "New Message"
15. Wait for "À :" to appear
16. Tap "À :"
17. Type "${RECIPIENT}"
18. Wait for "${RECIPIENT}" to appear
19. Tap "${RECIPIENT}"
20. Wait for "iMessage" to appear
21. Tap "iMessage"
22. Type "${MESSAGE_PREFIX:-On my way!} {commute_time} to the office (ETA {eta})"
23. Press **Return**
24. Wait for "Distribué" to appear
25. Verify "Distribué" is visible
26. Screenshot: "message_sent"
