---
version: 1
name: toolbar
platform: ios
---

# Toolbar

## Description

Bottom toolbar with icon-only action buttons. Different from tab bars: toolbars
contain actions relevant to the current screen content (compose, reply, delete,
organize), not global navigation. Found in Mail (compose, flag, delete), Notes
(checklist, camera, markup), Safari (share, bookmarks, tabs).

## Visual Pattern

- Row of 3-6 small icons or short action labels
- Positioned at the very bottom of the screen
- No persistent labels below icons (unlike tab bar)
- Actions change depending on context/screen

## Match Rules

- min_elements: 2
- max_elements: 6
- max_row_height_pt: 50
- zone: tab_bar
- exclude_numeric_only: true

## Interaction

- clickable: true
- click_target: first_text
- click_result: mutates_in_place
- back_after_click: false

## Exploration

- explorable: false
- role: action
- priority: low

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 0
- absorb_condition: any
