---
version: 1
name: Send Slack Message
app: Slack
ios_min: "17.0"
locale: "en_US"
tags: ["slack", "messaging", "create"]
---

Send a direct message to a contact in Slack

## Steps

1. Launch **Slack**
2. Wait for "Home" to appear
3. Tap "Direct Messages"
4. Wait for "${RECIPIENT}" to appear
5. Tap "${RECIPIENT}"
6. Wait for "Message" to appear
7. Tap "Message"
8. Type "${MESSAGE:-Hey, just checking in!}"
9. Press **Return**
10. Verify "${MESSAGE:-Hey, just checking in!}" is visible
11. Screenshot: "message_sent"
