---
version: 1
app: Settings
spotlight_name: Settings
icon: ⚙
---

# Settings

## Structure

Classic iOS Settings app with grouped sections of disclosure rows.
Deep drill-down hierarchy (3-8 levels). Every row with a chevron (>)
leads to a sub-screen.

## Main Screen
- Apple ID card at the top (profile header)
- Grouped sections: Airplane Mode, Wi-Fi, Bluetooth, Cellular, etc.
- Each section has disclosure rows with chevrons
- Toggle rows for Airplane Mode, Wi-Fi, Bluetooth

## Key Sections
- General: About, Software Update, Storage, Background App Refresh
- Privacy & Security: Location Services, Camera, Microphone, Photos
- Display & Brightness: Text Size, Bold Text, Dark Mode
- Accessibility: VoiceOver, Display & Text Size, Motion

## Obstacles
- Software Update dialog → tap "Later"
- Apple ID sign-in prompt → tap "Cancel"

## Skip
- Reset All Settings
- Erase All Content and Settings
- Sign Out
- Delete Account
- Transfer or Reset iPhone

## Tips
- Toggle rows (Airplane Mode, Wi-Fi, Bluetooth) change device state — skip them
- The General section has the deepest hierarchy (5+ levels)
- About screen shows device info — good landmark screen
- Search bar at top enables shortcut to any setting

## Simulator
- root: main

## Simulator Screen main
- title: Settings
- back: null
- tab_bar: false
- element row: "Apple ID" → apple_id
- element row: "Airplane Mode"
- element row: "Wi-Fi" → wifi
- element row: "Bluetooth" → bluetooth
- element row: "General" → general
- element row: "Display & Brightness" → display
- element row: "Privacy & Security" → privacy
- element row: "Accessibility" → accessibility

## Simulator Screen apple_id
- title: Apple ID
- back: main
- element text: "Cheffamille"
- element text: "iCloud and subscriptions"

## Simulator Screen wifi
- title: Wi-Fi
- back: main
- element text: "Home Network"
- element text: "Visible Networks"

## Simulator Screen bluetooth
- title: Bluetooth
- back: main
- element text: "My Devices"
- element text: "Other Devices"

## Simulator Screen general
- title: General
- back: main
- element row: "About" → about
- element row: "Software Update" → software_update
- element row: "Storage" → storage
- element row: "Background App Refresh" → bgapp
- element row: "Date & Time" → date_time
- element row: "Keyboard" → keyboard

## Simulator Screen about
- title: About
- back: general
- element text: "iPhone"
- element text: "iOS Version 18.4"
- element text: "Model Number"
- element text: "Serial Number"

## Simulator Screen software_update
- title: Software Update
- back: general
- element text: "iOS is up to date"

## Simulator Screen storage
- title: iPhone Storage
- back: general
- element text: "128 GB Available"
- element text: "Photos 24.1 GB"
- element text: "Apps 18.7 GB"

## Simulator Screen bgapp
- title: Background App Refresh
- back: general
- element text: "Refresh apps in the background"

## Simulator Screen date_time
- title: Date & Time
- back: general
- element text: "Set Automatically"

## Simulator Screen keyboard
- title: Keyboard
- back: general
- element row: "Keyboards" → keyboards_list
- element text: "Auto-Capitalization"

## Simulator Screen keyboards_list
- title: Keyboards
- back: keyboard
- element text: "English"
- element text: "Français (Canada)"

## Simulator Screen display
- title: Display & Brightness
- back: main
- element row: "Text Size" → text_size
- element text: "Bold Text"
- element text: "Dark Mode"

## Simulator Screen text_size
- title: Text Size
- back: display
- element text: "Drag to adjust"

## Simulator Screen privacy
- title: Privacy & Security
- back: main
- element row: "Location Services" → location_services
- element row: "Camera" → camera_perm
- element row: "Microphone" → microphone_perm
- element row: "Photos" → photos_perm

## Simulator Screen location_services
- title: Location Services
- back: privacy
- element text: "Location Services On"

## Simulator Screen camera_perm
- title: Camera
- back: privacy
- element text: "Apps allowed to use the camera"

## Simulator Screen microphone_perm
- title: Microphone
- back: privacy
- element text: "Apps allowed to use the microphone"

## Simulator Screen photos_perm
- title: Photos
- back: privacy
- element text: "Apps allowed to access photos"

## Simulator Screen accessibility
- title: Accessibility
- back: main
- element row: "VoiceOver" → voiceover
- element row: "Display & Text Size" → ax_display
- element row: "Motion" → motion

## Simulator Screen voiceover
- title: VoiceOver
- back: accessibility
- element text: "Spoken descriptions of items on the screen"

## Simulator Screen ax_display
- title: Display & Text Size
- back: accessibility
- element text: "Bold Text"
- element text: "Larger Text"

## Simulator Screen motion
- title: Motion
- back: accessibility
- element text: "Reduce Motion"

## Simulator Obstacle software_update
- title: "Software Update Available"
- body: "iOS 18.5 is available for your iPhone."
- buttons: Install Now, Later
- trigger: on_first_describe

## Simulator Obstacle signin
- title: "Sign in to your Apple ID"
- body: "Sign in to use iCloud, the App Store, and more."
- buttons: Sign In, Cancel
- trigger: after_n_taps:3
