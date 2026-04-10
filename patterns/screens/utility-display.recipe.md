---
version: 1
name: utility-display
platform: ios
---

# Utility Display

## Description

Single-screen or minimal-depth app focused on displaying data with light
interaction. Found in Weather, Clock, Calculator, Compass, and other utility
apps. Primary content is large metric displays with minimal navigation.

## Required Components

- metric-display

## Supporting Components

- segmented-control
- action-button
- tab-bar-item
- page-title
- search-bar

## Forbidden Components

- table-row-disclosure
- feed-post
- compose-bar
- table-row-subtitle

## Navigation Model

- type: minimal
- backtrack: tap-tab
- scroll_behavior: finite
- depth_pattern: flat

## Exploration Hints

- Metric displays are the primary content, not tappable
- Segmented controls switch between data views (hourly/daily/weekly)
- Scrolling reveals additional data sections
- Navigation depth is shallow — 1-2 levels maximum
- Tab bar switches between data categories or locations
