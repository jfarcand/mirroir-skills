---
version: 1
app: Santé
locale: fr_CA
archetype: dashboard
obstacle_mode: auto
---

# Santé (Health)

## Structure

Dashboard app with 4 tabs: Résumé, Partage, Parcourir, Profil.
The Résumé tab shows summary cards for key health metrics that drill down to
detail views with charts and historical data.

## Résumé Tab
- Summary cards showing health metrics (Activité, Cœur, Sommeil, Pleine conscience)
- Each card drills down to a detail screen with charts and trends
- Scroll reveals more metric cards below the fold
- Cards often show "Aucune donnée" (No data) on test devices

## Parcourir Tab
- Alphabetical list of all health categories
- Each category drills down to sub-metrics
- Deep hierarchy: category → sub-category → metric → chart
- This is the richest navigation structure in the app

## Partage Tab
- Requires a second user for sharing — skip during solo exploration
- Shows "Commencer" (Get Started) when no sharing is configured

## Profil Tab
- Settings-style drill-down with disclosure rows
- Contains notification preferences, export data, privacy settings

## Obstacles
- Health Access permission dialog → tap "Autoriser"
- Notification permission → tap "Ne pas autoriser"
- "Bienvenue dans Santé" onboarding → tap "Continuer"

## Skip
- Supprimer les données de Santé
- Réinitialiser
- Supprimer le compte

## Credentials
- No login required

## Tips
- Summary cards often show "Aucune donnée" (No data) on simulators — this is normal
- Chart screens have minimal tappable elements — backtrack quickly
- The Partage tab requires a second user — skip during solo exploration
- Parcourir has the deepest navigation structure (4+ levels)
