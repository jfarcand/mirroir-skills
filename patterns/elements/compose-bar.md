---
version: 1
name: compose-bar
platform: ios
---

# Compose Bar

## Description

Bottom-anchored text input area with a send button. Found in Messages, Slack,
WhatsApp, and any messaging or comment interface. Contains a text field placeholder
(iMessage, Message, Type a message) and a send/submit icon.

## Visual Pattern

- Text input placeholder ("iMessage", "Message", "Aa")
- Send or submit button to the right
- Fixed at the bottom of the content area, above tab bar
- Single row, 40-50pt typical height

## Match Rules

- min_elements: 1
- max_elements: 3
- max_row_height_pt: 60
- zone: content
- text_pattern: (?i)(message|imessage|type|write|aa$|envoyer|écrire)

## Interaction

- clickable: true
- click_target: first_text
- click_result: mutates_in_place
- back_after_click: false

## Exploration

- explorable: false
- role: action
- priority: normal

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 0
- absorb_condition: any
