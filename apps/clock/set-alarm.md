---
version: 1
name: Set Alarm
app: Clock
ios_min: "17.0"
locale: "en_US"
tags: ["clock", "alarm", "create"]
---

Create a new alarm in the Clock app

## Steps

1. Launch **Clock**
2. Wait for "Alarm" to appear
3. Tap "Alarm"
4. Tap "+"
5. Wait for "Save" to appear
6. Tap "Label"
7. Type "${ALARM_LABEL:-Wake Up}"
8. Tap "Save"
9. Verify "${ALARM_LABEL:-Wake Up}" is visible
10. Screenshot: "alarm_created"
