---
version: 1
app: Brawl Stars Victoire
spotlight_name: Brawl Stars Victoire
icon: ✪
locale: fr_CA
archetype: game
playable: single-control
---

# Brawl Stars Victoire

## Structure

FakeMirroring fixture: the Brawl Stars shell opened on the result screen a
3v3 win leaves, so the result-assert flow runs in CI without playing a match.
The same synthetic labels as `patterns/apps/brawl-stars/APP.md`; QUITTER
returns to its main menu.

## Simulator
- root: result

## Simulator Screen result
- title: Brawl Ball
- back: null
- tab_bar: false
- element text: "VICTOIRE"
- element text: "+8"
- element button: "QUITTER" → menu

## Simulator Screen menu
- title: SURVIVANT SOLO
- back: null
- tab_bar: false
- element row: "MAGASIN"
- element row: "BRAWLERS"
- element button: "JOUER"
