---
version: 1
app: embedded-jetty-websocket-chat
archetype: embedded-jetty-broadcast
runtime: programmatic-jetty-12 + atmosphere-runtime
surface: web
url_root: http://127.0.0.1:8080/
console_endpoint: /chat
console_mode: broadcast
obstacle_mode: auto
---

# embedded-jetty-websocket-chat

Programmatic embedded Jetty (no WAR, no Spring Boot) demonstrating the
**lower-level `@WebSocketHandlerService`** approach (vs `@ManagedService`).
Server is wired in Java (`EmbeddedJettyWebSocketChat.java` configures
`Server`, `ServerConnector`, `JakartaWebSocketServletContainerInitializer`,
then mounts an `AtmosphereServlet`). Bundled is the same Vite-based
"Atmosphere 4.0 Chat" UI used by the WAR sample.

This sample also enables **Jetty HTTP/3 + QUIC** on port 4443 alongside the
HTTP/1.1 connector on 8080 — observable in the boot log via
`"HTTP/3+QUIC support is experimental and not suited for production use."`.

## Boot prerequisites

- JDK 21 + Maven.
- Default port: 8080 for HTTP/1.1, 4443 for HTTP/3+QUIC.
- Command:
  `./mvnw -q test -pl samples/embedded-jetty-websocket-chat -Pserver`
  from the repo root. The `-Pserver` profile activates the
  `exec-maven-plugin` execution that runs the `EmbeddedJettyWebSocketChat`
  main class in the `test` phase.
- Boot wait: ~5–10 s. Ready when the log shows
  `Server started on port 8080`.
- No env vars required. The sample is auth-less.

## Served URLs

| Path | Content |
|---|---|
| `/` | 302 redirect to `/index.html` |
| `/index.html` | Bespoke chat UI (same Vite SPA as `chat` WAR) |
| `/assets/*` | JS/CSS bundles |
| `/chat` | WebSocket endpoint (`@WebSocketHandlerService`) |

`/api/console/info` and `/atmosphere/console/` are not served.

## Structure (observed via chrome-devtools-mcp snapshot 2026-05-16)

Same UI as the `chat` WAR sample — `frontend/` is a symlink or copy of the
WAR sample's webapp. Specifically:

- Page title: `"Atmosphere 4.0 Chat"`.
- Heading: `"Atmosphere 4.0 Chat"`.
- Subtitle: `"Managed Service • JDK 21 Virtual Threads • WebSocket with
  Long-Polling Fallback"`. Note: the subtitle still says "Managed Service"
  even though this sample uses `@WebSocketHandlerService` — the frontend is
  shared with the `@ManagedService` WAR sample.
- Status pill: `"Connected · websocket"`.
- Two-step flow (name → chat) identical to WAR sample.
- No `[data-testid]` attributes — selectors must be text/placeholder/role-based.

## Obstacles

- The `-Pserver` profile is the canonical run mode (the sample doesn't use
  `jetty:run` or `spring-boot:run`).
- mirroir-run's emitter doesn't fluently handle text-based selectors —
  same limitation as the legacy `chat` WAR sample. Chrome-devtools-mcp
  was the authoritative verification.

## Skip

- HTTP/3 connectivity SKILL — separate scenario, requires a chromium HTTP/3
  client setup.
- Asserting on `/atmosphere/console/*` — not served.

## Tips

- Same locators as the `chat` WAR SKILL.md — text/placeholder/role-based.
- The Jetty HTTP/3 log line is the cheapest signal that the experimental
  HTTP/3 connector is wired.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/` | GET | 302 → `/index.html` |
| `/index.html` | GET | Bespoke chat UI |
| `/chat` | WebSocket | Broadcast endpoint (`@WebSocketHandlerService`) |
| (HTTP/3) 4443 | UDP/QUIC | Experimental HTTP/3 connector |
