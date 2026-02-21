---
version: 1
name: Email Triage
app: Mail
ios_min: "17.0"
locale: "en_US"
tags: ["mail", "workflow", "conditional", "triage"]
---

Check inbox for unread email and triage it. If an unread email exists, open it and decide whether to flag or archive based on content. If the inbox is empty, take a screenshot and exit. Demonstrates conditional branching with nested conditions.

## Steps

1. Launch **Mail**
2. Wait for "Inbox" to appear
3. If "Unread" is visible:
   1. Tap "Unread"
   2. Wait for "From" to appear
   3. Remember: Read the sender name and subject line of this email.
   4. If "Urgent" is visible:
      1. Tap "Flag"
      2. Verify "Flagged" is visible
      3. Screenshot: "flagged_urgent"
      Otherwise:
      1. Tap "Archive"
      2. Screenshot: "archived"
   Otherwise:
   1. Screenshot: "empty_inbox"
