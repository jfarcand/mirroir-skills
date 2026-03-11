---
version: 1
name: chart-axis-label
platform: ios
---

# Chart Axis Label

## Description

Row of axis tick labels along a chart's X or Y axis.
Common in Health, Fitness, and any app with data charts.
These are decorative labels — not interactive.

## Visual Pattern

- 3+ short elements in a row
- Numeric values with unit suffixes (cal, h, min, km, pas, bpm)
- Or single-char day/month abbreviations (L, M, J, V, S, D)
- Evenly spaced in a horizontal line

## Match Rules

- min_elements: 3
- max_elements: 10
- max_row_height_pt: 30
- zone: content
- text_pattern: \d+\s*(cal|h|min|km|pas|bpm|%)?$|^:\d

## Interaction

- clickable: false
- click_target: none
- click_result: none
- back_after_click: false

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 0
- absorb_condition: any
