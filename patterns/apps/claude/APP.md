---
version: 1
app: Claude
spotlight_name: Claude
icon: ✦
locale: fr_CA
archetype: chat
obstacle_mode: auto
---

# Claude

## Structure

Chat-based assistant app. Empty state shows the Anthropic asterisk and a
greeting; tapping the input bar opens a composer for a new conversation.
The hamburger menu in the top-left opens a Conversations sidebar listing
prior chats; the model picker in the top-center toggles between Opus, Sonnet,
and Haiku; the ghost icon in the top-right opens a settings drawer.

## Main Screen
- Hamburger menu icon (top-left) → opens Conversations sidebar
- Model picker "Opus 4.7 ▼" (top-center) → opens model menu
- Ghost / settings icon (top-right) → opens settings drawer
- Greeting text "Bon après-midi, Cheffamille" centered when no chat is active
- Composer at the bottom: "Discuter avec Claude" placeholder, "+" attach button,
  microphone icon, voice/audio button on the right

## Conversations Sidebar
- Header "Conversations"
- Search bar at the bottom
- "+" icon to start a new chat
- List of prior chats, newest first, with relative timestamps
- Tapping a chat opens it in the main view

## Model Picker
- Three model entries: Opus, Sonnet, Haiku
- Tapping one switches the active model and dismisses the picker

## Settings Drawer
- Account row
- Subscription row
- Default model row
- Sign out (skip during exploration)

## Obstacles
- Login wall → tap "Se connecter avec votre compte"
- Notification permission → tap "Pas maintenant"
- "Disclaimer" footer → not an obstacle, just informational

## Skip
- Se déconnecter
- Supprimer la conversation
- Supprimer le compte
- Envoyer
- Voice mode
- Microphone

## Tips
- Never type into the composer during exploration — would send a real message and burn tokens
- The "+" attach button opens a file/photo picker — skip it
- The voice/audio button on the right of the composer triggers voice mode — skip it
- Conversations contain user data — don't tap individual chat rows to open them
- The model picker is safe to interact with (no side effects)

## Simulator
- root: home

## Simulator Screen home
- title: Opus 4.7
- back: null
- tab_bar: false
- element row: "Conversations" → conversations
- element text: "Bon après-midi, Cheffamille"
- element row: "Discuter avec Claude" → composer
- element row: "Paramètres" → settings_drawer

## Simulator Screen conversations
- title: Conversations
- back: home
- element row: "Résumé détaillé des deux premiers..." → chat_resume
- element row: "Récupération après trail à jeun" → chat_trail
- element row: "Identification des pneus Subaru" → chat_subaru
- element row: "Recharger batterie DuroMax" → chat_battery
- element text: "Rechercher"

## Simulator Screen chat_resume
- title: Conversation
- back: conversations
- element text: "Résumé du document"

## Simulator Screen chat_trail
- title: Conversation
- back: conversations
- element text: "Hydratation et électrolytes"

## Simulator Screen chat_subaru
- title: Conversation
- back: conversations
- element text: "Pneu de spécification"

## Simulator Screen chat_battery
- title: Conversation
- back: conversations
- element text: "Procédure de chargement"

## Simulator Screen composer
- title: Discuter avec Claude
- back: home
- element text: "Tapez votre message ici"
- element button: "Annuler" → home

## Simulator Screen settings_drawer
- title: Paramètres
- back: home
- element row: "Compte" → settings_account
- element row: "Abonnement" → settings_sub
- element row: "Modèle par défaut" → settings_model

## Simulator Screen settings_account
- title: Compte
- back: settings_drawer
- element text: "Cheffamille"

## Simulator Screen settings_sub
- title: Abonnement
- back: settings_drawer
- element text: "Pro plan"

## Simulator Screen settings_model
- title: Modèle par défaut
- back: settings_drawer
- element row: "Opus" → settings_drawer
- element row: "Sonnet" → settings_drawer
- element row: "Haiku" → settings_drawer

## Simulator Obstacle notifications_claude
- title: "Recevoir des notifications de Claude?"
- buttons: Activer, Pas maintenant
- trigger: after_n_taps:3
