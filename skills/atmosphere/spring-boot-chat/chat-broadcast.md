---
version: 1
name: Broadcast chat — single-turn user post
app: spring-boot-chat
surface: web
tags: ["atmosphere", "broadcast", "websocket", "must-pass"]
---

Open the Atmosphere Console wired to a broadcast endpoint, post one message,
verify the user bubble renders. The canonical happy-path for any
`@ManagedService`-backed Spring Boot sample exposing the bundled Console in
broadcast mode (no LLM, no assistant reply).

## Preconditions

The runner boots the JVM via `boot_once`; the SKILL.md does not respawn it. The
boot env declared by `SAMPLE.md` (or the equivalent harness call) must include:

- `ATMOSPHERE_AUTH_ENABLED=false` — Vue console does not thread an auth token
  in `frontend/src/App.tsx:36` (commented out for WebTransport demo). The
  auth-enabled default returns 401 on `/atmosphere/console/` and the SKILL.md
  hangs at the status wait.

`LLM_MODE` is not read by this sample — no AI module on the classpath.

Boot ready when `GET http://127.0.0.1:8080/atmosphere/console/` returns 200
and `GET /api/console/info` reports `"mode":"broadcast"`.

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`
   (the full label appends transport, e.g. `"Connected · websocket"`).
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
transport per browser; the `"Connected"` prefix-match on `[data-testid=status-label]`
is transport-agnostic. WebTransport requires Chromium today.

## Skip / obstacles

None when `ATMOSPHERE_AUTH_ENABLED=false`. If auth stays enabled (the
production default), the connection never reaches "Connected" — the
status-label hangs at "Connecting" or flips to "Disconnected" and the SKILL.md
times out at step 2.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element matches and
  is visible.
- Zero `[data-testid=message-bubble].message--assistant` elements match
  (broadcast samples must never produce an assistant bubble; a match would
  indicate the sample regressed onto an AI runtime).
- No console errors logged (use the platform's console-error capture hook).
