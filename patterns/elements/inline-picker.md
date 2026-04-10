---
version: 1
name: inline-picker
platform: ios
---

# Inline Picker

## Description

Scroll wheel or inline date/time picker embedded within a screen. Found in Clock
(alarm time), Calendar (event time), Timer, and Settings (Auto-Lock duration).
The picker contains multiple numeric or short-text values stacked vertically.
Must not be confused with a scrollable list — interaction is via swipe within
the picker area, not by tapping individual values.

## Visual Pattern

- Multiple short numeric or time values stacked vertically
- Currently selected value highlighted or centered
- Fixed height container (150-250pt)
- Values are short (1-5 characters): hours, minutes, AM/PM

## Match Rules

- has_numeric_value: true
- min_elements: 3
- max_elements: 10
- max_row_height_pt: 40
- zone: content
- text_pattern: \d{1,2}(:\d{2})?|AM|PM|min|hr

## Interaction

- clickable: false
- click_target: none
- click_result: none
- back_after_click: false

## Exploration

- explorable: false
- role: action
- priority: normal

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 200
- absorb_condition: any
