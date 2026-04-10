---
version: 1
name: settings-list
platform: ios
---

# Settings List

## Description

Drill-down list with grouped sections, chevron rows, toggles, and detail rows.
The primary navigation pattern in Settings, System Preferences, and configuration
screens across iOS apps.

## Required Components

- table-row-disclosure

## Supporting Components

- section-header
- section-footer
- table-row-detail
- table-row-value
- toggle-row
- search-bar

## Forbidden Components

- feed-post
- collection-cell
- compose-bar

## Navigation Model

- type: drill-down
- backtrack: tap-back-chevron
- scroll_behavior: finite
- depth_pattern: linear

## Exploration Hints

- Every chevron row leads to a sub-screen worth exploring
- Toggle rows are state-changing — skip during exploration
- Section headers are stable landmarks for skill steps
- Expect 3-8 drill-down levels in typical apps
- Search bar enables shortcut navigation to deep settings
