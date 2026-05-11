---
version: 1
app: TikTok
spotlight_name: TikTok
icon: ♪
archetype: social-feed
reset_before_explore: true
obstacle_mode: auto
---

# TikTok

## Structure

Full-screen video feed app with 5 tabs: Pour toi (For You), Explorer (Explore),
+ (Create), Boite de reception (Inbox), Profil (Profile).

## Pour toi Tab
- Full-screen video player — minimal text overlay
- Swipe up to see next video (NOT tap)
- Overlay shows: username, description, music name, engagement buttons on right
- Do NOT scroll through videos — navigate via tabs instead

## Explorer Tab
- Search bar at top
- Trending topics and category tiles
- Good navigation structure for exploration

## Profil Tab
- User profile with follower/following counts
- Video grid below (collection cells)
- Settings gear icon in top-right → drill-down settings

## Obstacles
- Login prompt → tap "Fermer"
- Notification permission → tap "Ne pas autoriser"
- Personnaliser votre fil → tap "Ignorer"
- Content warning → tap "OK"
- DIRECT populaires → tap "X"
- Rejoindre → tap "X"
- Al Jaze → tap "X"

## Skip
- Publier
- Acheter
- Recharger
- S'abonner
- Supprimer le compte

## Tips
- The Pour toi feed is infinite video — do NOT scroll or tap content
- Navigate exclusively via bottom tabs to discover app structure
- Explorer and Profil have the richest navigation hierarchies
- The + tab opens camera — skip it during exploration
- Right-side icons (heart, comment, share, bookmark) are engagement, not navigation

## Simulator
- root: pour_toi

## Simulator Screen pour_toi
- title: Pour toi
- back: null
- tab_bar: true
- element text: "@username"
- element text: "Description de la vidéo"
- element text: "Musique originale"
- element tab: "Pour toi" → pour_toi
- element tab: "Explorer" → explorer
- element tab: "Boite de reception" → inbox
- element tab: "Profil" → profil

## Simulator Screen explorer
- title: Explorer
- back: null
- tab_bar: true
- element row: "Tendances" → tendances
- element row: "Voyage" → voyage
- element row: "Cuisine" → cuisine
- element row: "Animaux" → animaux
- element tab: "Pour toi" → pour_toi
- element tab: "Explorer" → explorer
- element tab: "Boite de reception" → inbox
- element tab: "Profil" → profil

## Simulator Screen tendances
- title: Tendances
- back: explorer
- element text: "Vidéos populaires aujourd'hui"

## Simulator Screen voyage
- title: Voyage
- back: explorer
- element text: "Destinations populaires"

## Simulator Screen cuisine
- title: Cuisine
- back: explorer
- element text: "Recettes virales"

## Simulator Screen animaux
- title: Animaux
- back: explorer
- element text: "Vidéos d'animaux"

## Simulator Screen inbox
- title: Boite de reception
- back: null
- tab_bar: true
- element text: "Aucun message"
- element tab: "Pour toi" → pour_toi
- element tab: "Explorer" → explorer
- element tab: "Boite de reception" → inbox
- element tab: "Profil" → profil

## Simulator Screen profil
- title: Profil
- back: null
- tab_bar: true
- element text: "0 abonnements"
- element text: "0 abonnés"
- element text: "0 J'aime"
- element row: "Paramètres" → parametres
- element tab: "Pour toi" → pour_toi
- element tab: "Explorer" → explorer
- element tab: "Boite de reception" → inbox
- element tab: "Profil" → profil

## Simulator Screen parametres
- title: Paramètres
- back: profil
- element row: "Compte" → compte
- element row: "Confidentialité" → confidentialite_tt
- element row: "Notifications" → notif_tt

## Simulator Screen compte
- title: Compte
- back: parametres
- element text: "Nom d'utilisateur"

## Simulator Screen confidentialite_tt
- title: Confidentialité
- back: parametres
- element text: "Compte privé"

## Simulator Screen notif_tt
- title: Notifications
- back: parametres
- element text: "Activité"

## Simulator Obstacle login
- title: "Connectez-vous à TikTok"
- body: "Suivez des créateurs et aimez des vidéos"
- buttons: Se connecter, Fermer
- trigger: on_first_describe

## Simulator Obstacle notifications_tt
- title: "Activer les notifications?"
- buttons: Activer, Ne pas autoriser
- trigger: after_n_taps:3

## Simulator Obstacle personnaliser
- title: "Personnaliser votre fil"
- body: "Choisissez vos centres d'intérêt"
- buttons: Continuer, Ignorer
- trigger: after_n_taps:5
