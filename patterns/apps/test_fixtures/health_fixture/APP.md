---
version: 1
app: Health
spotlight_name: Health
icon: ❤
---

# Health

Test fixture: Health-style summary with stat texts. Used by integration
tests that drive scroll/tap on Health-like content.

## Simulator
- root: health

## Simulator Screen health
- title: Summary
- back: null
- tab_bar: false
- element row: "Steps" → steps_detail
- element text: "8,432"
- element text: "Heart Rate"
- element text: "72 bpm"
- element text: "Sleep"
- element text: "7h 24m"
- element text: "Mindful Minutes"
- element text: "12 min"

## Simulator Screen steps_detail
- title: Steps
- back: health
- element text: "Daily Average"
- element text: "8,432 steps"
- element text: "Weekly Total"
- element text: "59,024 steps"
