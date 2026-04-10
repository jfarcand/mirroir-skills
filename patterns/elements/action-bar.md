---
version: 1
name: action-bar
platform: ios
---

# Action Bar

## Description

Horizontal row of icon-only action buttons for engagement or sharing. Found below
social feed posts (Like, Comment, Share, Bookmark) and in photo viewers (Edit,
Rotate, Delete). Distinguished from tab bars by position (mid-content vs bottom)
and function (actions on content vs navigation).

## Visual Pattern

- Row of 3-6 small icons or short labels
- Evenly spaced horizontally
- Located in the content zone (not tab bar zone)
- Each icon represents an action on the current content
- Typically 30-50pt height

## Match Rules

- min_elements: 3
- max_elements: 6
- max_row_height_pt: 55
- zone: content
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
