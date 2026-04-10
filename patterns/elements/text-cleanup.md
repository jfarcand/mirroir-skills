---
version: 1
name: text-cleanup
platform: ios
---

# Text Cleanup Rules

## Description

Defines OCR noise patterns that should be stripped from display labels and
landmark text before they appear in generated skills. These are visual markers
that OCR reads as characters but carry no semantic meaning.

## Strip Prefixes

Characters removed from the beginning of labels:

- •
- ·
- ‣
- ⁃
- ◦
- ○
- ●

## Exclude Labels

Exact text values that should never be used as landmarks or step labels:

- icon
- Icon
- ICON
