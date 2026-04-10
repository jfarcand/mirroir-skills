---
version: 1
name: Standup Autoposter
app: Calendar, Slack
ios_min: "17.0"
locale: "en_US"
tags: ["workflow", "cross-app", "calendar", "slack", "standup", "productivity"]
---

Read today's meetings from Calendar, compose a standup update, and post it to a Slack channel. Demonstrates cross-app data extraction where the AI reads dynamic calendar content and formats it into a Slack message.

## Steps

1. Launch **Calendar**
2. Wait for "Calendar" to appear
3. Tap "Today"
4. Wait for "Today" to appear
5. Remember: Read all event titles and times from today's calendar view. Format as bullet list.
6. Screenshot: "todays_meetings"
7. Press Home
8. Launch **Slack**
9. Wait for "Home" to appear
10. Tap "Search"
11. Wait for "Search" to appear
12. Type "${STANDUP_CHANNEL:-#standup}"
13. Wait for "${STANDUP_CHANNEL:-#standup}" to appear
14. Tap "${STANDUP_CHANNEL:-#standup}"
15. Wait for "Message" to appear
16. Tap "Message"
17. Type "${MESSAGE_PREFIX:-Standup update:} {meetings}"
18. Press **Return**
19. Verify "${MESSAGE_PREFIX:-Standup update:}" is visible
20. Screenshot: "standup_posted"
