---
version: 1
name: banner-notification
platform: ios
---

# Banner Notification

## Description

Transient notification banner that appears at the top of the screen over any app.
Shows app name, short message preview, and auto-dismisses after a few seconds.
Must be recognized and ignored during exploration — tapping it navigates away
from the current app.

## Visual Pattern

- App name or icon in the top-left
- Short preview text (1-2 lines)
- Appears at the very top of the screen, overlapping the status bar
- Rounded rectangle shape
- Temporary: disappears after 3-5 seconds

## Match Rules

- min_elements: 1
- max_elements: 3
- max_row_height_pt: 80
- zone: nav_bar

## Interaction

- clickable: false
- click_target: none
- click_result: none
- back_after_click: false

## Exploration

- explorable: false
- role: info
- priority: normal

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 40
- absorb_condition: any
