---
version: 1
name: Get Directions and Travel Time
app: Maps
ios_min: "17.0"
locale: "en_US"
tags: ["maps", "navigation", "read-only", "remember"]
---

Search for a destination in Maps, get directions, and extract the estimated travel time. The AI reads dynamic routing data from the screen — no Maps API needed.

## Steps

1. Launch **Maps**
2. Wait for "Search Maps" to appear
3. Tap "Search Maps"
4. Type "${DESTINATION:-Central Park}"
5. Wait for "${DESTINATION:-Central Park}" to appear
6. Tap "${DESTINATION:-Central Park}"
7. Wait for "Directions" to appear
8. Tap "Directions"
9. Wait for "min" to appear
10. Remember: Read the estimated travel time, distance, and route summary for each transportation mode shown.
11. Screenshot: "directions"
