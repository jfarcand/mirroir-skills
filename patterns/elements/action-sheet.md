---
version: 1
name: action-sheet
platform: ios
---

# Action Sheet

## Description

Bottom-of-screen popup presenting multiple action options. Common for share menus,
delete confirmations, and multi-choice dialogs. Always includes a Cancel button
that dismisses the sheet without side effects. The explorer should dismiss
action sheets immediately to avoid triggering destructive actions.

## Visual Pattern

- Multiple stacked action labels (each on its own row)
- Cancel button at the bottom (separated by a gap)
- Appears over dimmed background
- Located in the lower half of the content zone
- Each action is a short, tappable label

## Match Rules

- min_elements: 2
- max_elements: 6
- max_row_height_pt: 60
- zone: content

## Interaction

- clickable: true
- click_target: first_dismiss_button
- click_result: dismisses
- back_after_click: false

## Exploration

- explorable: false
- role: info
- priority: normal

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 200
- absorb_condition: any
