---
version: 1
name: Quarkus broadcast chat — single-turn user post
app: quarkus-chat
surface: web
tags: ["atmosphere", "quarkus", "broadcast", "websocket", "must-pass"]
---

Open the Atmosphere Console wired to the Quarkus broadcast endpoint, post one
message, verify the user bubble renders. Canonical happy-path for the Quarkus
parity of `spring-boot-chat` — identical Console SPA, identical
`@ManagedService` handler, fewer console tabs.

## Preconditions

The runner boots the JVM via `boot_once`; the SKILL.md does not respawn it. The
boot env declared by `SAMPLE.md` (or the equivalent harness call) must include:

- `ATMOSPHERE_AUTH_ENABLED=false` — Vue console does not thread an auth token
  (`frontend/src/App.tsx:36`, commented out for WebTransport demo). The
  auth-enabled default returns 401 on `/atmosphere/console/`.
- Boot command must include `-Dquarkus.console.enabled=false` so Quarkus's
  live-reload TUI does not capture stdin/stdout.

`LLM_MODE` is not read by this sample — no AI module on the classpath.

Boot ready when:
- `GET http://127.0.0.1:8080/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"mode":"broadcast"` and
  `"subtitle":"Multi-client broadcast chat"`.

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`
   (the full label may append transport, e.g. `"Connected · websocket"`;
   prefix-match only).
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"hello from mirroir-skills"`.
5. Tap `[data-testid=chat-send]`. (Button is disabled until input is non-empty;
   do not race the click ahead of the keystroke.)
6. Wait for `[data-testid=message-bubble].message--user` to be visible.
7. Verify the user bubble renders (visible + non-empty text). **Do not** wait
   for or assert on `.message--assistant` — broadcast mode never produces one
   and the wait will time out.
8. Screenshot: `chat-broadcast-user-rendered`.

## Cross-browser

The same flow runs on chromium + firefox + webkit. atmosphere.js negotiates
transport per browser. WebTransport is unlikely to negotiate on the Quarkus
build (Undertow lacks HTTP/3); expect WebSocket primary, SSE / long-poll
fallback. The `"Connected"` prefix-match is transport-agnostic.

## Known drift (do not assert)

- The Quarkus Console build (4.0.46-SNAPSHOT, observed 2026-05-15) still shows
  the AI empty-state copy (`"Start a conversation"` / `"...chatting with the
  AI assistant."`) even though `mode:broadcast`. Do not assert against the
  empty-state text; only assert post-send bubble visibility.
- Console nav has 5 tabs (Chat/Policies/Decisions/Commitments/OWASP) — no
  "Sessions" tab. Do not enumerate tabs by index; locate Chat by text.

## Skip / obstacles

None when `ATMOSPHERE_AUTH_ENABLED=false` and `-Dquarkus.console.enabled=false`
are set. If auth stays enabled, the SKILL.md times out at step 2.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element matches and
  is visible.
- Zero `[data-testid=message-bubble].message--assistant` elements match
  (broadcast mode; assistant bubble would indicate a regression onto an AI
  runtime).
- No console errors logged (use the platform's console-error capture hook).
