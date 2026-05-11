---
version: 1
app: Profile
spotlight_name: Profile
icon: ◉
---

# Profile

Test fixture: profile-style screen exercising stat texts, action buttons, a
brightness slider, and image-grid placeholders. Used by integration tests
that drive drag (slider) and tap (Follow/Message buttons).

## Simulator
- root: profile

## Simulator Screen profile
- title: johndoe
- back: null
- tab_bar: true
- element text: "42"
- element text: "Posts"
- element text: "1.2K"
- element text: "Followers"
- element text: "890"
- element text: "Following"
- element text: "Photographer & traveler"
- element button: "Follow"
- element button: "Message"
- element placeholder: 128x128
- element placeholder: 128x128
- element placeholder: 128x128
- element slider: "Brightness" #brightness = 0.5
- element tab: "Home" → profile
- element tab: "Profile" → profile
