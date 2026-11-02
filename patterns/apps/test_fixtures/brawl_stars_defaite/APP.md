---
version: 1
app: Brawl Stars Defaite
spotlight_name: Brawl Stars Defaite
icon: ✪
locale: fr_CA
archetype: game
playable: single-control
---

# Brawl Stars Defaite

## Structure

FakeMirroring fixture: the Brawl Stars shell opened on the result screen a
3v3 loss leaves, so the result-assert flow runs in CI without playing a match.
The same synthetic labels as `patterns/apps/brawl-stars/APP.md`; QUITTER
returns to its main menu. The app name carries no accent: Spotlight is typed
through the Mac keyboard layout, which an accent does not cross on every host.

## Simulator
- root: result

## Simulator Screen result
- title: Brawl Ball
- back: null
- tab_bar: false
- element text: "DÉFAITE"
- element text: "-4"
- element button: "QUITTER" → menu

## Simulator Screen menu
- title: SURVIVANT SOLO
- back: null
- tab_bar: false
- element row: "MAGASIN"
- element row: "BRAWLERS"
- element button: "JOUER"
