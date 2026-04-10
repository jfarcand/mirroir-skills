---
version: 1
name: detail-form
platform: ios
---

# Detail Form

## Description

Form or detail editing screen with mixed controls: text fields, pickers, toggles,
and action buttons. Found in Calendar (new event), Contacts (edit), Reminders
(new task), and any screen where the user fills in structured data.

## Required Components

- table-row-value

## Supporting Components

- toggle-row
- table-row-detail
- inline-picker
- action-button
- destructive-button
- section-header
- navigation-bar

## Forbidden Components

- feed-post
- collection-cell
- summary-card

## Navigation Model

- type: form
- backtrack: tap-back-chevron
- scroll_behavior: finite
- depth_pattern: linear

## Exploration Hints

- Toggle rows change state — skip during exploration
- Inline pickers are interactive but should not be scrolled during exploration
- Destructive buttons must never be tapped
- Value rows may lead to picker sub-screens
- Forms are typically leaf screens — limited further depth
