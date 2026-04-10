---
version: 1
name: table-row-value
platform: ios
---

# Table Row with Value

## Description

Table row with a label on the left and a right-aligned value that represents the
current setting or state. Common in Settings (Language → English, Auto-Lock → 5
Minutes) and detail views showing key-value pairs. Distinguished from
table-row-detail by having a chevron indicating the value is tappable/changeable.

## Visual Pattern

- Label text aligned left
- Value text aligned right (often gray or blue)
- Chevron at the far right edge
- Full-width row, 44-60pt typical height

## Match Rules

- row_has_chevron: true
- has_numeric_value: false
- min_elements: 2
- max_elements: 4
- max_row_height_pt: 90
- zone: content

## Interaction

- clickable: true
- click_target: first_navigation_element
- click_result: pushes_screen
- back_after_click: true
- label_rule: first_text

## Exploration

- explorable: true
- role: depth_navigation
- priority: normal

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 0
- absorb_condition: any
