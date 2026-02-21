---
version: 1
name: Add City to Weather
app: Weather
ios_min: "17.0"
locale: "en_US"
tags: ["weather", "create"]
---

Search for and add a city to the Weather app

## Steps

1. Launch **Weather**
2. Wait for "Weather" to appear
3. Tap "list"
4. Wait for "Search" to appear
5. Tap "Search"
6. Type "${CITY:-Montreal}"
7. Wait for "${CITY:-Montreal}" to appear
8. Tap "${CITY:-Montreal}"
9. Wait for "Add" to appear
10. Tap "Add"
11. Verify "${CITY:-Montreal}" is visible
12. Screenshot: "city_added"
