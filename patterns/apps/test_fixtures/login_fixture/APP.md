---
version: 1
app: Login
spotlight_name: Login
icon: ⌨
---

# Login

Test fixture: form with two text fields (username, password) and a submit
button. Used by integration tests to verify keyboard input handling and
field activation/deactivation.

## Simulator
- root: login

## Simulator Screen login
- title: Sign In
- back: null
- tab_bar: false
- element textfield: "Username" #username
- element textfield: "Password" #password
- element button: "Log In" → feed
- element button: "Cancel"

## Simulator Screen feed
- title: Feed
- back: null
- tab_bar: false
- element text: "johndoe"
- element text: "Welcome back"
