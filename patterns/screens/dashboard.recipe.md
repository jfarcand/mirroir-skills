---
version: 1
name: dashboard
platform: ios
---

# Dashboard

## Description

Card-based overview screen showing summary metrics that drill down to detail
views. Found in Health, Fitness, Stocks, and analytics-style apps. Cards are
the primary navigation elements.

## Required Components

- summary-card

## Supporting Components

- metric-display
- tab-bar-item
- page-title
- chart-axis-label
- section-header
- action-button

## Forbidden Components

- feed-post
- compose-bar
- table-row-disclosure

## Navigation Model

- type: card-drill-down
- backtrack: tap-back-chevron
- scroll_behavior: finite
- depth_pattern: card-to-detail

## Exploration Hints

- Summary cards are the primary drill-down targets
- Metric displays are informational landmarks, not tappable
- Charts indicate a data-heavy detail screen
- Tab bar switches between metric categories
- Expect 2-3 drill-down levels (dashboard → detail → chart)
