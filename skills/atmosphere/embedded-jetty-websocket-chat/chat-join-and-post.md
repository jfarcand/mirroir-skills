---
version: 1
name: Embedded Jetty chat — join + post broadcast
app: embedded-jetty-websocket-chat
surface: web
tags: ["atmosphere", "broadcast", "embedded-jetty", "websocket-handler-service", "must-pass"]
---

Open the programmatically-launched Jetty embedded chat, enter a name, post
one message, verify both the join system-message and the chat bubble
render. Same canonical flow as the legacy WAR sample — they share the
bespoke chat UI.

## Preconditions

The runner boots the JVM via `boot_once`. No env vars required.

Boot ready when:
- The boot log emits `Server started on port 8080`, AND
- `GET http://127.0.0.1:8080/` returns 302 redirecting to `/index.html`, AND
- `GET http://127.0.0.1:8080/index.html` returns 200 with HTML containing
  `<title>Atmosphere 4.0 Chat</title>`.

## Steps

Identical to the `chat` (WAR) SKILL.md — same UI, same selectors:

1. Open `http://127.0.0.1:8080/` (browser follows 302 to `/index.html`).
2. Wait for status text starting with `"Connected"`.
3. Fill `getByPlaceholder('Enter your name to join…')` with `"embedded-tester"`.
4. Click `getByRole('button', { name: 'Send' })`.
5. Wait for `getByText('embedded-tester has joined!')`.
6. Fill `getByPlaceholder('Type a message…')` with
   `"hello from mirroir-skills"`.
7. Click `Send` again.
8. Wait for `getByText('hello from mirroir-skills')`.
9. Verify both texts visible.
10. Screenshot: `chat-embedded-jetty-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. HTTP/3 connector at 4443 is
experimental — Chromium may attempt HTTP/3 negotiation via Alt-Svc, but
the chat flow runs over WebSocket on the HTTP/1.1 connector regardless.

## Skip / obstacles

Same as the WAR sample — mirroir-run's emitter targets `[data-testid]`
natively; this sample's text/placeholder selectors need direct Playwright
script support. Chrome-devtools-mcp end-to-end verification is the
authoritative proof.

## Verify (post-conditions)

- Text `"embedded-tester has joined!"` is visible.
- Text `"hello from mirroir-skills"` is visible.
- Status pill text starts with `"Connected"`.
- No browser console errors logged.
