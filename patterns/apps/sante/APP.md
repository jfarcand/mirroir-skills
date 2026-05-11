---
version: 1
app: Santé
spotlight_name: Sante
icon: ❤
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

## Simulator
- root: resume

## Simulator Screen resume
- title: Résumé
- back: null
- tab_bar: true
- element row: "Activité" → activite
- element row: "Cœur" → coeur
- element row: "Sommeil" → sommeil
- element row: "Pleine conscience" → pleine_conscience
- element tab: "Résumé" → resume
- element tab: "Partage" → partage
- element tab: "Parcourir" → parcourir
- element tab: "Profil" → profil

## Simulator Screen activite
- title: Activité
- back: resume
- element text: "Aucune donnée"
- element text: "Pas par jour"

## Simulator Screen coeur
- title: Cœur
- back: resume
- element text: "Aucune donnée"
- element text: "Battements par minute"

## Simulator Screen sommeil
- title: Sommeil
- back: resume
- element text: "Aucune donnée"
- element text: "Heures de sommeil"

## Simulator Screen pleine_conscience
- title: Pleine conscience
- back: resume
- element text: "Aucune donnée"
- element text: "Minutes de pleine conscience"

## Simulator Screen partage
- title: Partage
- back: null
- tab_bar: true
- element button: "Commencer"
- element tab: "Résumé" → resume
- element tab: "Partage" → partage
- element tab: "Parcourir" → parcourir
- element tab: "Profil" → profil

## Simulator Screen parcourir
- title: Parcourir
- back: null
- tab_bar: true
- element row: "Activité" → activite
- element row: "Audition" → audition
- element row: "Cœur" → coeur
- element row: "Mobilité" → mobilite
- element row: "Nutrition" → nutrition
- element row: "Respiration" → respiration
- element row: "Signes vitaux" → signes_vitaux
- element row: "Sommeil" → sommeil
- element tab: "Résumé" → resume
- element tab: "Partage" → partage
- element tab: "Parcourir" → parcourir
- element tab: "Profil" → profil

## Simulator Screen audition
- title: Audition
- back: parcourir
- element text: "Niveau sonore environnemental"

## Simulator Screen mobilite
- title: Mobilité
- back: parcourir
- element text: "Vitesse de marche"

## Simulator Screen nutrition
- title: Nutrition
- back: parcourir
- element text: "Glucides"
- element text: "Protéines"

## Simulator Screen respiration
- title: Respiration
- back: parcourir
- element text: "Fréquence respiratoire"

## Simulator Screen signes_vitaux
- title: Signes vitaux
- back: parcourir
- element text: "Tension artérielle"
- element text: "Glycémie"

## Simulator Screen profil
- title: Profil
- back: null
- tab_bar: true
- element row: "Notifications" → notifications_pref
- element row: "Confidentialité" → confidentialite
- element row: "Exporter les données" → exporter
- element tab: "Résumé" → resume
- element tab: "Partage" → partage
- element tab: "Parcourir" → parcourir
- element tab: "Profil" → profil

## Simulator Screen notifications_pref
- title: Notifications
- back: profil
- element text: "Recevoir des rappels"

## Simulator Screen confidentialite
- title: Confidentialité
- back: profil
- element text: "Apps autorisées à lire les données"

## Simulator Screen exporter
- title: Exporter
- back: profil
- element button: "Exporter toutes les données de Santé"

## Simulator Obstacle health_access
- title: "Santé voudrait accéder à vos données"
- body: "Pour suivre votre activité, Santé a besoin d'accéder à vos données."
- buttons: Autoriser, Refuser
- trigger: on_first_describe

## Simulator Obstacle notifications_perm
- title: "Recevoir des notifications de Santé?"
- buttons: Autoriser, Ne pas autoriser
- trigger: after_n_taps:2

## Simulator Obstacle bienvenue
- title: "Bienvenue dans Santé"
- body: "Suivez vos activités et votre santé en un seul endroit."
- buttons: Continuer
- trigger: never
