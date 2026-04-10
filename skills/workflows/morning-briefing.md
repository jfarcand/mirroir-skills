---
version: 1
name: Morning Briefing
app: Weather, Calendar, Messages
ios_min: "17.0"
locale: "en_US"
tags: ["workflow", "cross-app", "weather", "calendar", "messages", "productivity"]
---

Check the weather, read today's schedule, and send a morning summary via iMessage. The AI reads live data from two apps and composes a natural-language briefing — something only an AI executor can do. No APIs, no integrations, just screen reading.

## Steps

1. Launch **Weather**
2. Wait for "Weather" to appear
3. Remember: Read the current temperature, conditions, and high/low for today.
4. Screenshot: "weather_check"
5. Press Home
6. Launch **Calendar**
7. Wait for "Calendar" to appear
8. Tap "Today"
9. Wait for "Today" to appear
10. Remember: Read all event titles and times from today's calendar.
11. Screenshot: "calendar_check"
12. Press Home
13. Launch **Messages**
14. Wait for "Messages" to appear
15. Tap "New Message"
16. Wait for "To:" to appear
17. Tap "To:"
18. Type "${RECIPIENT}"
19. Wait for "${RECIPIENT}" to appear
20. Tap "${RECIPIENT}"
21. Wait for "iMessage" to appear
22. Tap "iMessage"
23. Type "Morning briefing: {weather}. Today's schedule: {meetings}"
24. Press **Return**
25. Screenshot: "briefing_sent"
