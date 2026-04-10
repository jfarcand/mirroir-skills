---
version: 1
name: content-grid
platform: ios
---

# Content Grid

## Description

Grid or collection layout displaying browsable items. Found in Photos, App Store
(Today/Games/Apps tabs), Music (albums), Podcasts, and any app showing content
in a grid pattern.

## Required Components

- collection-cell

## Supporting Components

- tab-bar-item
- segmented-control
- search-bar
- navigation-bar
- page-title

## Forbidden Components

- feed-post
- toggle-row
- compose-bar

## Navigation Model

- type: grid-browse
- backtrack: tap-back-chevron
- scroll_behavior: finite
- depth_pattern: grid-to-detail

## Exploration Hints

- Tap a few grid items to explore detail views, not all
- Segmented controls switch between content categories
- Search enables targeted browsing
- Grid items typically all lead to the same type of detail screen
- Explore 2-3 representative items per category, then move on
