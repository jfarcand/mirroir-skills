---
version: 1
name: Batch Archive Inbox
app: Mail
ios_min: "17.0"
locale: "en_US"
tags: ["mail", "workflow", "repeat", "batch"]
---

Archive all unread emails in a loop. Opens each unread email, archives it, returns to the inbox, and repeats until no unread emails remain. Demonstrates the repeat step with while_visible and nested condition for handling edge cases.

## Steps

1. Launch **Mail**
2. Wait for "Inbox" to appear
3. Repeat while "Unread" is visible (max 20):
   1. Tap "Unread"
   2. Wait for "From" to appear
   3. If "Flagged" is visible:
      1. Screenshot: "skipped_flagged"
      2. Tap "< Back"
      Otherwise:
      1. Tap "Archive"
   4. Wait for "Inbox" to appear
4. Screenshot: "inbox_clean"
5. Verify "Unread" is NOT visible
