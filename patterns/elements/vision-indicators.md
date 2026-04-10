---
version: 1
name: vision-indicators
platform: ios
---

# Vision Indicator Mappings

Maps vision model icon descriptions to OCR-compatible characters.
When a vision element's text ends with an indicator suffix (e.g. "Entraînements chevron"),
the suffix is stripped and a separate element with the mapped character is added
(e.g. "Entraînements" + ">"). This allows the component detection pipeline to match
vision output the same way it matches OCR output.

## Indicators
- chevron: >
- chevron_right: >
- disclosure: >
- arrow_right: >
- dismiss: ×
- close_button: ×
- back: <
- xmark: ×
