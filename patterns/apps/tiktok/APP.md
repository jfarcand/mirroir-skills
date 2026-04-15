---
version: 1
app: TikTok
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
