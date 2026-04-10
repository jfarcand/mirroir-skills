---
version: 1
name: article-modal
platform: ios
---

# Article Modal

## Description

Full-screen modal presenting an informational article with a dismiss button
(✕, ×, X) in the nav bar zone and article content below. Common in Health/Santé
(medication articles, health tips), App Store (app descriptions), and other apps
that present read-only content as a modal overlay.

## Visual Pattern

- Dismiss button (✕, ×, X) in the nav bar zone, typically top-right
- Article title or heading in the content zone below (not on the same row)
- No back chevron (modal, not push navigation)
- Content scrollable below the title

## Match Rules

- has_dismiss_button: true
- row_has_chevron: false
- min_elements: 1
- max_elements: 3
- max_row_height_pt: 40
- zone: nav_bar

## Interaction

- clickable: true
- click_target: first_dismiss_button
- click_result: dismisses
- back_after_click: false

## Exploration

- explorable: false
- role: info
- priority: high

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 200
- absorb_condition: any
