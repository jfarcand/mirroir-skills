---
version: 1
name: profile-header
platform: ios
---

# Profile Header

## Description

User profile or contact card at the top of a screen. Shows name, avatar placeholder,
and optional subtitle (phone number, email, bio). Found in Contacts, Settings (Apple
ID card), social app profiles, and account screens. Serves as a landmark but is
typically not navigable itself.

## Visual Pattern

- Name or display name prominently placed
- Avatar or initials circle (detected as icon)
- Optional subtitle: phone, email, bio, follower count
- Located near the top of the content zone
- Wider vertical span than standard rows (80-150pt)

## Match Rules

- min_elements: 1
- max_elements: 5
- max_row_height_pt: 160
- zone: content

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
- absorbs_below_within_pt: 60
- absorb_condition: any
