---
version: 1
name: Driving ETA Message
app: Waze, Messages
ios_min: "17.0"
locale: "fr_CA"
tags: ["workflow", "cross-app", "waze", "messages", "carplay", "driving"]
---

Tell someone when you will arrive, while the phone is on CarPlay with a Waze
route running. The ETA is read off the route that is already guiding the drive,
and a message is written in an existing Messages conversation. The message is
never sent by the skill: a passenger reads it and says yes first.

Run it with driving mode on in `~/.mirroir-mcp/permissions.json`:

```json
"driving": { "on": true, "allowedApps": ["Waze", "Messages"] }
```

Driving mode refuses any tap on the navigation screen, so nothing here touches
Waze: the skill only reads it, then leaves it with Home. CarPlay keeps its own
screen and goes on guiding while the phone shows Messages. Run it parked or
with a passenger at the Mac, never by the driver.

> Note: --- Waze: read the route already running ---
> Note: --- Messages: write the message, stop before sending ---

## Steps

1. Launch **Waze**
2. Wait for "min" to appear
3. Remember: Read the time left and the distance from the route (e.g. '14 min • 8.4 km'). You will put the time left into the message.
4. Screenshot: "eta_screen"
5. Press Home
6. Launch **Messages**
7. Wait for "${RECIPIENT}" to appear
8. Tap "${RECIPIENT}"
9. Wait for "iMessage" to appear
10. Tap "iMessage"
11. Type "${MESSAGE_PREFIX:-J'arrive dans} {time_left}"
12. Screenshot: "message_ready"
13. Remember: The message is written, not sent. Show it to the user and send it only after they say yes; never press Return without that yes.
