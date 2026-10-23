---
version: 1
name: Result Screen Assert
app: Brawl Stars
ios_min: "17.0"
locale: "fr_CA"
tags: ["brawl-stars", "game", "shell", "result", "assert", "read-only"]
---

Assert that the end-of-match result screen renders, read its outcome, then
return to the main menu. Read-only and shell-only: it runs AFTER a match has
already ended (the result screen is on-screen) and never plays or starts a
match itself. The deterministic pass/fail is the result screen's universal
"QUITTER" (proceed) button and the main-menu "JOUER" after it; the outcome read
is informational.

Precondition: a result screen is showing (any mode). Outcome labels: 3v3 modes
show "VICTOIRE" / "DÉFAITE"; ranked modes (Showdown / Survivant) show
"Rang : N" with a trophy delta. On this fixture only the ranked "Rang" screen is
OCR-verified; "VICTOIRE" / "DÉFAITE" are Brawl Stars' standard French 3v3 labels,
read defensively here and pending on-device confirmation.

## Steps

1. Wait for "QUITTER" to appear
2. Verify "QUITTER" is visible
3. If "VICTOIRE" is visible, remember the outcome as "win"
4. If "DÉFAITE" is visible, remember the outcome as "loss"
5. If "Rang" is visible, remember the placement shown next to "Rang"
6. Screenshot: "result_screen"
7. Tap "QUITTER"
8. Wait for "JOUER" to appear
9. Verify "JOUER" is visible
10. Screenshot: "result_back_at_menu"
