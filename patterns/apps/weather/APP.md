---
version: 1
app: Weather
spotlight_name: Weather
icon: ☀
---

# Weather

## Structure

Utility app showing weather data for saved locations. Main screen displays
the current city's weather with metric displays. Scroll reveals hourly forecast,
10-day forecast, and detail cards (UV, wind, humidity, etc.).

## Main Screen
- City name at the top as page title
- Large temperature metric display (e.g. "23°")
- Current conditions text (Sunny, Partly Cloudy, etc.)
- Hourly forecast as a horizontal scroll row
- 10-day forecast as a vertical list
- Detail cards below: UV Index, Wind, Humidity, Pressure, Visibility, Feels Like

## City List
- Tap the list icon (bottom-right) to see saved locations
- Each city row shows name + temperature
- Tap a city to view its forecast
- Search bar at top to add new cities

## Obstacles
- Location permission dialog → tap "Allow While Using App"
- Notification prompt → tap "Not Now"

## Skip
- Delete
- Remove

## Tips
- The main screen is a single scrollable page — no drill-down from weather cards
- Detail cards (UV, Wind, etc.) are informational, not tappable
- Navigation depth is minimal: city list → city detail → that's it
- The map view button opens a separate weather map — skip it during exploration

## Simulator
- root: main

## Simulator Screen main
- title: Montréal
- back: null
- tab_bar: false
- element text: "23°"
- element text: "Sunny"
- element text: "H:25° L:14°"
- element text: "Hourly Forecast"
- element text: "10-Day Forecast"
- element text: "UV Index"
- element text: "Wind"
- element text: "Humidity"
- element text: "Pressure"
- element text: "Visibility"
- element text: "Feels Like"
- element row: "Locations" → cities

## Simulator Screen cities
- title: Locations
- back: main
- element row: "Montréal 23°" → main
- element row: "Toronto 21°" → toronto
- element row: "Vancouver 17°" → vancouver

## Simulator Screen toronto
- title: Toronto
- back: cities
- element text: "21°"
- element text: "Partly Cloudy"

## Simulator Screen vancouver
- title: Vancouver
- back: cities
- element text: "17°"
- element text: "Light Rain"

## Simulator Obstacle location_permission
- title: "Allow Weather to use your location?"
- body: "Weather needs your location to show local forecasts."
- buttons: Allow While Using App, Don't Allow
- trigger: on_first_describe

## Simulator Obstacle notifications
- title: "Stay updated on weather"
- body: "Get severe weather alerts and daily forecasts."
- buttons: Turn On Notifications, Not Now
- trigger: after_n_taps:2
