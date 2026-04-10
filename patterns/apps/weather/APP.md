---
version: 1
app: Weather
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
