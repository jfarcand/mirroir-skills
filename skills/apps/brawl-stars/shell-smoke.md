---
version: 1
name: Shell Smoke
app: Brawl Stars
ios_min: "17.0"
locale: "fr_CA"
tags: ["brawl-stars", "game", "shell", "smoke", "read-only"]
---

Smoke-test the Brawl Stars main-menu shell: confirm the menu renders, open the
Shop and confirm it renders, then return to the menu. Touches only the shell —
it never taps JOUER, a game mode, or any purchase, so no scene or paid flow is
entered. Precondition: a returning player (the one-time first-run tutorial is
already complete, so launching lands on the main menu).

## Steps

1. Launch **Brawl Stars**
2. Wait for "JOUER" to appear
3. Verify "JOUER" is visible
4. Screenshot: "shell_main_menu"
5. Tap "MAGASIN"
6. Wait for "RESSOURCES" to appear
7. Verify "RESSOURCES" is visible
8. Screenshot: "shell_shop"
9. Press back to return to the main menu
10. Wait for "JOUER" to appear
11. Verify "JOUER" is visible
12. Screenshot: "shell_back_at_menu"
