---
version: 1
name: feed-post
platform: ios
---

# Feed Post

## Description

Social feed item displaying user-generated content. Found in TikTok, Instagram,
Reddit, Twitter/X, and any infinite-scroll feed. Typically contains a username,
timestamp, content text, and engagement indicators (likes, comments, shares).
Exploration should skip individual posts to avoid infinite scroll traps.

## Visual Pattern

- Username or display name near the top
- Timestamp or relative time ("2h", "3d ago")
- Content text or caption (variable length)
- Engagement row below content (like count, comment count, share)
- Full-width, 100-300pt typical height

## Match Rules

- min_elements: 4
- max_elements: 10
- max_row_height_pt: 60
- zone: content
- has_long_text: false
- row_has_chevron: false
- text_pattern: (?i)(ago|h$|m$|d$|min|like|comment|share|reply|retweet|heart|view)

## Interaction

- clickable: true
- click_target: first_text
- click_result: pushes_screen
- back_after_click: true
- label_rule: first_text

## Exploration

- explorable: false
- role: info
- priority: low

## Grouping

- absorbs_same_row: true
- absorbs_below_within_pt: 120
- absorb_condition: any
