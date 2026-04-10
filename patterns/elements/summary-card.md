---
version: 1
name: summary-card
platform: ios
---

# Summary Card

## Description

Card showing a metric with title, large numeric value, and optional chevron.
Common in Health, Fitness, and dashboard-style apps. Vision describers may
combine the title, value, and timestamp into a single element (e.g.
"Activité, 15:10"), so min_elements is 1 to handle both OCR and vision output.

## Visual Pattern

- Title text on first line
- Large numeric value on second line
- Unit or description near the value
- Optional chevron for navigation

## Match Rules

- chevron_mode: preferred
- min_elements: 2
- max_elements: 3
- max_row_height_pt: 120
- zone: content

## Interaction

- clickable: true
- click_target: first_navigation_element
- click_result: pushes_screen
- back_after_click: true
- label_rule: longest_text

## Exploration

- explorable: true
- role: depth_navigation
- priority: high

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 80
- absorb_condition: any
