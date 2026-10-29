---
version: 1
app: Clock (Drift)
spotlight_name: Clock (Drift)
icon: ⏰
---

# Clock (Drift)

Test fixture: the Clock simulator pack (`patterns/apps/clock/APP.md`) with
exactly ONE label changed — the second alarm on the Alarms screen reads
"Swim" instead of "Gym". Every other screen, element, and navigation edge is
identical. Drift tests capture a baseline against "Clock", then replay the
same steps against "Clock (Drift)" (launch it by that name, or pick it from
FakeMirroring's Scenario menu) and expect the one-label difference to be
reported as drift.

The pack carries its own app name because FakeMirroring keys packs by app
name and mirroir-mcp matches APP.md files by app name: a second pack named
"Clock" would make both lookups ambiguous.

## Simulator
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
- element text: "Swim"
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
