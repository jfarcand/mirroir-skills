---
version: 1
name: gRPC chat — static frontend boot smoke
app: grpc-chat
surface: web
tags: ["atmosphere", "grpc", "connect-web", "must-pass"]
---

Open the grpc-chat static frontend and verify the page loads. The bespoke
chat UI **does not** end-to-end work against this server (it expects
WebSocket; this server speaks Connect-Web RPCs only) — so the SKILL
asserts page load and the honest `"Reconnecting…"` state, not chat
delivery. The real chat flow is exercised via a Connect client or the
Java gRPC CLI (separate SKILLs).

## Preconditions

The runner boots the JVM via `boot_once`. No env vars required.

Boot ready when:
- `GET http://127.0.0.1:8080/` returns 302 redirecting to `/index.html`, AND
- `GET http://127.0.0.1:8080/index.html` returns 200 with HTML containing
  `<title>Atmosphere 4.0 Chat</title>`.

The SLF4J `"A service provider failed to instantiate"` warning is normal
and does **not** indicate a boot failure — the server starts but does no
further logging.

## Steps

1. Open `http://127.0.0.1:8080/`.
2. Wait for the page heading `"Atmosphere 4.0 Chat"`. Locator:
   `getByRole('heading', { name: 'Atmosphere 4.0 Chat' })`.
3. Wait for the connection-status text starting with `"Reconnecting…"` (or
   `"Connected"` if atmosphere.js somehow negotiates a transport — neither
   is wrong, but observed behavior is `"Reconnecting…"`).
4. Verify the heading is visible.
5. Verify the name input is **disabled** (atmosphere.js disables the form
   while reconnecting).
6. Screenshot: `chat-grpc-static-page-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. None of them complete the chat
flow because the WebSocket endpoint isn't served.

## Skip / obstacles

- Do NOT attempt to fill the name input or click Send — both are disabled
  in the reconnecting state.
- mirroir-run's emitter doesn't fluently support text/role selectors.
  Chrome-devtools-mcp end-to-end was the authoritative verification.

## Verify (post-conditions)

- Heading `"Atmosphere 4.0 Chat"` is visible.
- Status text starts with `"Reconnecting…"` or `"Connected"` (either is
  acceptable; we are NOT asserting end-to-end chat delivery here).
- Name input has the disabled attribute set.
- No `JavaScript` errors logged in the browser console (the
  reconnect state must be reached gracefully, not via thrown exceptions).
