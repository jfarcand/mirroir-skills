---
version: 1
name: destructive-button
platform: ios
---

# Destructive Button

## Description

Red-styled button for irreversible or dangerous actions: Sign Out, Delete Account,
Delete All, Remove, Reset. Must never be tapped during exploration to avoid data
loss or state changes that cannot be undone.

## Visual Pattern

- Single centered text label
- Red or destructive styling
- Common labels: Sign Out, Delete, Remove, Reset, Erase, Supprimer, Déconnexion
- Usually at the bottom of a settings or detail screen

## Match Rules

- min_elements: 1
- max_elements: 1
- max_row_height_pt: 60
- zone: content
- text_pattern: (?i)(sign.?out|log.?out|delete|remove|erase|reset|supprimer|déconnexion|effacer|réinitialiser)

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

- absorbs_same_row: false
- absorbs_below_within_pt: 0
- absorb_condition: any
