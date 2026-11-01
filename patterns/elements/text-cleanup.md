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
- *

## Segment Separators

Characters OCR reads between two items it merged into one line ("• Sommeil |
Réveil"). A landmark is taken from one segment, never the merged line: the
next read may split the items, and a wait on the merged text then times out.

- |
- •
- ·
- ‣

## Exclude Labels

Exact text values that should never be used as landmarks or step labels:

- icon
- Icon
- ICON
