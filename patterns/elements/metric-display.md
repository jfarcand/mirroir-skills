---
version: 1
name: metric-display
platform: ios
---

# Metric Display

## Description

Large numeric value with a unit label, used in dashboard and utility apps to show
key metrics prominently. Examples: "72 bpm" in Health, "23°" in Weather, "8,432
steps" in Fitness, "$142.50" in Stocks. Usually not directly tappable for
navigation but serves as a key landmark on the screen.

## Visual Pattern

- Large numeric value (often 2-6 characters)
- Unit or descriptor near the value (bpm, °, steps, km, %)
- Positioned prominently, often centered or left-aligned
- May have a secondary label above or below

## Match Rules

- has_numeric_value: true
- row_has_chevron: false
- min_elements: 1
- max_elements: 1
- max_row_height_pt: 80
- zone: content
- text_pattern: \d+[\.,]?\d*\s*(°|bpm|pas|km|mi|cal|kcal|min|h|%|mg|mmHg|steps)?$

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
- absorbs_below_within_pt: 30
- absorb_condition: any
