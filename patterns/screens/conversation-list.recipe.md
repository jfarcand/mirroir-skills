---
version: 1
name: conversation-list
platform: ios
---

# Conversation List

## Description

List of conversations or threads that drill down to individual message views.
Found in Messages, Mail, Slack, WhatsApp, and any messaging app. Each row
shows a contact/sender and preview text.

## Required Components

- table-row-subtitle

## Supporting Components

- tab-bar-item
- search-bar
- compose-bar
- navigation-bar
- profile-header

## Forbidden Components

- summary-card
- collection-cell
- feed-post

## Navigation Model

- type: list-to-thread
- backtrack: tap-back-chevron
- scroll_behavior: finite
- depth_pattern: list-to-detail

## Exploration Hints

- Each conversation row leads to a thread view
- Compose bar indicates a messaging interface
- Explore 2-3 representative conversations, not all
- Thread views have limited depth — no further drill-down
- Search enables finding specific conversations
