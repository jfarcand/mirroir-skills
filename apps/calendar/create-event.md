---
version: 1
name: Create Calendar Event
app: Calendar
ios_min: "17.0"
locale: "en_US"
tags: ["calendar", "create", "productivity"]
---

Create a new event in the iOS Calendar app

## Steps

1. Launch **Calendar**
2. Wait for "Calendar" to appear
3. Tap "+"
4. Wait for "Title" to appear
5. Tap "Title"
6. Type "${EVENT_TITLE:-Team Standup}"
7. Tap "Location or Video Call"
8. Type "${EVENT_LOCATION:-Conference Room}"
9. Tap "Add"
10. Verify "${EVENT_TITLE:-Team Standup}" is visible
11. Screenshot: "event_created"
