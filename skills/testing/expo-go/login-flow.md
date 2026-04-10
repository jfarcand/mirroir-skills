---
version: 1
name: Expo Go Login Flow
app: Expo Go
ios_min: "17.0"
locale: "en_US"
tags: ["testing", "expo", "authentication", "conditional"]
---

Test the login screen of an Expo Go app. Handles both fresh signup and existing account cases using conditional branching — the AI adapts to whichever state it encounters.

## Steps

1. Launch **Expo Go**
2. Wait for "${APP_SCREEN:-LoginDemo}" to appear
3. Tap "${APP_SCREEN:-LoginDemo}"
4. Wait for "Email" to appear
5. Tap "Email"
6. Type "${TEST_EMAIL}"
7. Tap "Password"
8. Type "${TEST_PASSWORD}"
9. Tap "Sign In"
10. If "Invalid" is visible:
   1. Screenshot: "login_failed"
   2. Tap "Sign Up"
   3. Tap "Email"
   4. Type "${TEST_EMAIL}"
   5. Tap "Password"
   6. Type "${TEST_PASSWORD}"
   7. Tap "Create Account"
   Otherwise:
   1. Wait for "Welcome" to appear
11. Verify "Welcome" is visible
12. Screenshot: "login_success"
