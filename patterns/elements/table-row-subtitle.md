---
version: 1
name: table-row-subtitle
platform: ios
---

# Table Row with Subtitle

## Description

Two-line table row with a title and a secondary subtitle line below it. The most
common list row pattern in iOS: Mail inbox (sender + subject), Contacts (name +
phone), notifications (app + message), and Settings sub-rows (title + description).

## Visual Pattern

- Primary text label on the first line
- Smaller or gray subtitle text directly below
- Optional chevron at the right edge for navigable rows
- Full-width row, 60-100pt typical height (taller than single-line rows)

## Match Rules

- min_elements: 2
- max_elements: 5
- max_row_height_pt: 110
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
- absorbs_below_within_pt: 40
- absorb_condition: no_chevron_rows_only
