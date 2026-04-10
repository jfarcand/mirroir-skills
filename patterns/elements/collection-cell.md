---
version: 1
name: collection-cell
platform: ios
---

# Collection View Cell

## Description

Grid item in a collection view layout. Common in Photos (thumbnails), App Store
(app cards), Music (album art), and any app displaying a grid of items. Each cell
is independently tappable and leads to a detail view.

## Visual Pattern

- Short label (1-3 words) or image placeholder
- Arranged in a horizontal grid pattern (multiple items per row)
- Uniform sizing across cells
- Often accompanied by a small subtitle or price

## Match Rules

- min_elements: 2
- max_elements: 8
- max_row_height_pt: 60
- zone: content
- exclude_numeric_only: true

## Interaction

- clickable: true
- click_target: first_text
- click_result: pushes_screen
- back_after_click: true
- label_rule: first_text

## Exploration

- explorable: true
- role: depth_navigation
- priority: low

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 30
- absorb_condition: any
- split_mode: per_item
