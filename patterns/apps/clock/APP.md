---
version: 1
app: Clock
spotlight_name: Clock
icon: ⏰
---

# Clock

## Structure

Stock iOS utility app with 4 tabs: World Clock, Alarms, Stopwatch, Timers.
The app reopens on the last tab used. Each tab is a single screen; the only
drill-down is the Add Alarm sheet, opened from the Alarms tab and closed with
Cancel or Save.

## Tabs
- World Clock
- Alarms
- Stopwatch
- Timers

## Alarms Screen
- Large title "Alarms" with "Edit" (top-left) and "+" (top-right, accessibility label "Add Alarm")
- "Sleep | Wake Up" section, then an "Other" section listing each alarm
- Each alarm row shows its time (e.g. "6:30 AM") above its label and repeat ("Alarm, every weekday")
- A switch on each row enables or disables the alarm

## Add Alarm Sheet
- Header "Add Alarm" with "Cancel" (left) and "Save" (right)
- Time wheel picker
- Rows: Repeat, Label, Sound, Snooze

## Obstacles

Clock shows no permission prompt or dialog on launch.

## Skip
- Delete
- Delete Alarm

## Tips
- Never tap the alarm switches during exploration — they change device state
- Never tap Save on a real device during exploration — it creates a real alarm
- The Stopwatch "Start" and Timers "Start" buttons begin a running timer; tap "Cancel" or "Reset" to leave no trace

## Simulator

The simulator opens on the Alarms tab (the app restores the last tab used),
so the golden journey — Alarms → Add Alarm → Save — needs no tab-bar tap.
The "+" control is rendered as an "Add Alarm" button: that is its
accessibility label, and a lone "+" glyph is not reliably recognized by OCR.
The pack is stateless: Save and Cancel both return to the same Alarms list.
`patterns/apps/test_fixtures/clock_drift/APP.md` ("Clock (Drift)") is this
pack with exactly one Alarms-list label changed, for drift detection.

- root: alarms

## Simulator Screen alarms
- title: Alarms
- back: null
- tab_bar: true
- element text: "Sleep | Wake Up"
- element text: "Other"
- element text: "6:30 AM"
- element text: "Alarm, every weekday"
- element text: "7:45 AM"
- element text: "Gym"
- element button: "Edit"
- element button: "Add Alarm" → add_alarm
- element tab: "World Clock" → world_clock
- element tab: "Alarms" → alarms
- element tab: "Stopwatch" → stopwatch
- element tab: "Timers" → timers

## Simulator Screen add_alarm
- title: Add Alarm
- back: null
- tab_bar: false
- element row: "Repeat"
- element row: "Label"
- element row: "Sound"
- element row: "Snooze"
- element button: "Cancel" → alarms
- element button: "Save" → alarms

## Simulator Screen world_clock
- title: World Clock
- back: null
- tab_bar: true
- element text: "Today, +0HRS"
- element text: "Cupertino"
- element text: "Today, +3HRS"
- element text: "New York"
- element button: "Edit"
- element tab: "World Clock" → world_clock
- element tab: "Alarms" → alarms
- element tab: "Stopwatch" → stopwatch
- element tab: "Timers" → timers

## Simulator Screen stopwatch
- title: Stopwatch
- back: null
- tab_bar: true
- element text: "00:00.00"
- element button: "Lap"
- element button: "Start"
- element tab: "World Clock" → world_clock
- element tab: "Alarms" → alarms
- element tab: "Stopwatch" → stopwatch
- element tab: "Timers" → timers

## Simulator Screen timers
- title: Timers
- back: null
- tab_bar: true
- element text: "0 hours 15 min 0 sec"
- element text: "When Timer Ends"
- element button: "Cancel"
- element button: "Start"
- element tab: "World Clock" → world_clock
- element tab: "Alarms" → alarms
- element tab: "Stopwatch" → stopwatch
- element tab: "Timers" → timers
