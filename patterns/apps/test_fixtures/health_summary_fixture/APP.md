---
version: 1
app: Health Summary
spotlight_name: Health Summary
icon: ❤
---

# Health Summary

Test fixture: Health summary cards layout used by BFS exploration tests.
Cards drill into detail screens.

## Simulator
- root: summary

## Simulator Screen summary
- title: Summary
- back: null
- tab_bar: false
- element row: "Steps" → steps_detail
- element row: "Heart Rate" → heart_detail
- element row: "Sleep" → sleep_detail
- element row: "Mindful Minutes" → mindful_detail
- element row: "Active Energy" → active_detail
- element row: "Exercise Minutes" → exercise_detail
- element row: "Stand Hours" → stand_detail
- element row: "Walking Distance" → walking_detail
- element row: "Flights Climbed" → flights_detail
- element row: "Resting Energy" → resting_detail
- element row: "Body Mass" → body_detail
- element row: "Workouts" → workouts_detail

## Simulator Screen active_detail
- title: Active Energy
- back: summary
- element text: "Average 412 kcal/day"

## Simulator Screen exercise_detail
- title: Exercise Minutes
- back: summary
- element text: "Average 32 min/day"

## Simulator Screen stand_detail
- title: Stand Hours
- back: summary
- element text: "Average 11 hr/day"

## Simulator Screen walking_detail
- title: Walking Distance
- back: summary
- element text: "Average 6.2 km/day"

## Simulator Screen flights_detail
- title: Flights Climbed
- back: summary
- element text: "Average 14 floors/day"

## Simulator Screen resting_detail
- title: Resting Energy
- back: summary
- element text: "Average 1,640 kcal/day"

## Simulator Screen body_detail
- title: Body Mass
- back: summary
- element text: "78.4 kg"

## Simulator Screen workouts_detail
- title: Workouts
- back: summary
- element text: "5 workouts this week"

## Simulator Screen steps_detail
- title: Steps
- back: summary
- element text: "Average 8,432 steps/day"

## Simulator Screen heart_detail
- title: Heart Rate
- back: summary
- element text: "Average 72 bpm"

## Simulator Screen sleep_detail
- title: Sleep
- back: summary
- element text: "Average 7h 24m"

## Simulator Screen mindful_detail
- title: Mindful Minutes
- back: summary
- element text: "Average 12 min/day"
