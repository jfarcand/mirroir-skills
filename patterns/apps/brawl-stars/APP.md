---
version: 1
app: Brawl Stars
spotlight_name: Brawl Stars
icon: ✪
locale: fr_CA
archetype: game
reset_before_explore: false
obstacle_mode: auto
---

# Brawl Stars

## Structure

Mobile arena brawler. The app is **forced landscape** — every screen is wide
and `describe_screen` reports the window in landscape.

`archetype: game` is **documentary only**: a game has no single recipe. Its
screens split into two kinds, and only the first is covered here.

- **Shell** — ordinary text UI that the existing archetype models already handle:
  - **Main menu** → `detail-form`: the brawler/mode dashboard (JOUER, mode
    selector, resource bars, left and right nav).
  - **Magasin** (Shop) → `content-grid`: a scrollable offer/category grid.
  - **Settings** (the `≡` menu, top-right) → `settings-list`.
  - **Brawlers** → `content-grid`: the brawler collection.
- **Scene** — the playfield after tapping JOUER (a live match, with the virtual
  joystick and fire controls). A scene is `kind: game`, interpreted by a model
  loop, **not** a recipe. No shell skill ever enters a scene.

**First-run gate.** A fresh / guest account (it shows "Vous avez déjà un
compte ?" / "Supercell ID") is dropped into a one-time onboarding **scene**:
Shelly's "collect the power cubes" tutorial, then a scripted tutorial match.
The main-menu shell appears only **after** that tutorial is finished; every
later launch opens straight to the main menu. Shell skills assume a returning
player (tutorial complete).

## Main Menu (detail-form)

- Center: the active brawler on display.
- Bottom-right: **JOUER** (Play) — starts a match. **Never tap it in a shell
  skill**: it leaves the shell and enters a `scene`.
- Bottom-center: the mode selector (e.g. "SURVIVANT SOLO", "Lac d'acide") —
  tapping it also leads into a scene; off-limits for shell coverage.
- Left nav: the brawler/event tile (top), BUFFIES, **MAGASIN** (Shop), BRAWLERS.
- Right nav: INFOS, AMIS, CLUB.
- Bottom-left: the XP bar and QUÊTES (Quests).
- Top bar: resource counters (energy, coins, gems) and the **≡** menu (Settings).

## Magasin / Shop (content-grid)

- Header reads "MAGASIN" with a back chevron (top-left) and a home icon
  (top-right); both return to the main menu.
- Left categories: "OFFRES À L'AFFICHE", a seasonal tab (e.g. "BRAWLOWEEN" —
  the name changes by season, so do not key on it), "SKINS", "MAGASIN DE
  CURIOSITÉS", and "RESSOURCES" (permanent — a stable anchor for "shop
  rendered").
- Center/right: offer tiles, most of them **paid**: "PASS BRAWL", "MEILLEURE
  OFFRE DE BRAWL STARS !", prices like "11,99 $", and an "ACTIVER" (activate /
  buy) button. All of these are Skip targets (see `## Skip`).

## Settings (≡ menu, settings-list)

- Opened from the `≡` icon in the top-right of the main menu.
- A plain settings list (account, sound, language, support). Safe to read; do
  not change account or device state.

## Brawlers (content-grid)

- Opened from the BRAWLERS tile in the left nav.
- A grid of owned and locked brawlers. Read-only for shell coverage; tapping a
  brawler opens its detail card, not a scene.

## Obstacles

- Login prompt "Vous avez déjà un compte ?" / "Supercell ID" → never log in;
  leave it, do not tap it.
- Trophy-reward nudge "Nouvelle récompense des trophées !" (a pointing-finger
  hint on the main menu) → non-blocking; navigation works with it up, ignore it.
- First-run tutorial / tutorial match → a `scene`, out of shell scope; a human
  must finish it before shell skills run (see the First-run gate above).

## Skip

- Buy
- Purchase
- Gems
- Offers
- ACTIVER
- PASS BRAWL
- OFFRES À L'AFFICHE
- MAGASIN DE CURIOSITÉS
- Supercell ID
- JOUER
- SURVIVANT SOLO
- /\d+,\d+\s*\$/
