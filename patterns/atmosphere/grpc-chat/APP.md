---
version: 1
app: grpc-chat
archetype: grpc-connect-web
runtime: programmatic-jetty + atmosphere-grpc + netty-grpc
surface: web
url_root: http://127.0.0.1:8080/
console_endpoint: /atmosphere.AtmosphereService/*
console_mode: connect-web
obstacle_mode: auto
---

# grpc-chat

Atmosphere's **gRPC transport** sample. The server speaks two protocols
simultaneously:

1. **Connect-Web over HTTP/1.1** on port 8080 (browser-friendly POST RPCs
   like `POST /atmosphere.AtmosphereService/Subscribe`).
2. **Native gRPC over HTTP/2** on port 9090 (for Java CLI / native gRPC
   clients).

Both transports share the same `Broadcaster` instance, so a Java gRPC
client and a browser Connect-Web client see each other's broadcasts.

**Important surface limitation**: the bundled static frontend at `/` is the
same "Atmosphere 4.0 Chat" Vite SPA used by `chat` (WAR) and
`embedded-jetty-websocket-chat`. That UI was built against
**WebSocket transport** and atmosphere.js — it does **NOT** speak
Connect-Web RPCs. When pointed at this grpc-chat server it stays stuck at
`"Reconnecting… · websocket"` indefinitely (no WebSocket endpoint is
served). The canonical chat surface for this sample is the
Connect-Web RPC itself, driven by either a Connect client or the Java
gRPC CLI.

## Boot prerequisites

- JDK 21 + Maven.
- Default ports: 8080 (Connect-Web + static frontend), 9090 (native gRPC).
- Command: `./mvnw -q exec:java -pl samples/grpc-chat` from the repo root.
- Boot wait: ~5–10 s. Ready when:
  - `GET http://127.0.0.1:8080/` returns 200.
  - `POST /atmosphere.AtmosphereService/Subscribe` (with valid Connect body)
    streams broadcasts.
- No env vars required.
- Known boot quirk: SLF4J emits `"A service provider failed to instantiate:
  ch.qos.logback.classic.spi.LogbackServiceProvider"` and defaults to NOP
  logger — the server is up but produces no further log output. Use the
  HTTP probes above to confirm boot, not log scraping.

## Served URLs

| Path | Content |
|---|---|
| `/` | 302 → `/index.html` |
| `/index.html` | Bespoke chat UI (DOES NOT work against grpc-chat — expects WebSocket) |
| `/atmosphere.AtmosphereService/Subscribe` | Connect-Web RPC (POST JSON) |
| `/atmosphere.AtmosphereService/Send` | Connect-Web RPC (POST JSON) |
| (HTTP/2 on 9090) `atmosphere.AtmosphereService` | Native gRPC bidi stream |

## Structure (observed via chrome-devtools-mcp snapshot 2026-05-16)

Browser opens `/` and lands on the bespoke UI. atmosphere.js fails its
WebSocket handshake (no `/chat` endpoint on this server) and stays in
`"Reconnecting…"` state. The textbox and `Send` button are **disabled**
while the connection retries. From a chrome-devtools-only must-pass
perspective the visible signal is: the static frontend is served, the
page loads, and atmosphere.js correctly detects the unavailability of its
expected transport (an honest "Reconnecting" state, not a JS error).

## Obstacles

- The bespoke frontend is **not usable** for end-to-end chat with this
  server. Must-pass SKILL asserts the static HTML loads only.
- mirroir-run's emitter targets `[data-testid]`; this UI has none.
- SLF4J broken — boot log is empty after SLF4J warnings. Use HTTP probes.
- The Java gRPC CLI client is the canonical interactive surface; it lives
  alongside the server (`samples/grpc-chat/src/main/java/.../GrpcChatClient.java`
  or similar) and is invoked via `./mvnw exec:java
  -Dexec.mainClass=...GrpcChatClient`. Out of scope for chrome-devtools.

## Skip

- Driving the bespoke UI past page-load — won't succeed against this server.
- Asserting on `/atmosphere/console/*` — not served.
- Native gRPC interop SKILL — separate scenario, gRPC CLI fixture.

## Tips

- The cleanest chrome-devtools-observable signal is the page-load and the
  honest `"Reconnecting…"` state — proves both the HTTP server is up and
  that atmosphere.js's reconnect loop is wired.
- For a Connect-Web SKILL, `curl -sS -X POST
  http://127.0.0.1:8080/atmosphere.AtmosphereService/Subscribe -H
  'Content-Type: application/json' -d '{}'` returns a streamed response
  when the server is healthy.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/` | GET | Static frontend (does not connect to this server) |
| `/atmosphere.AtmosphereService/Subscribe` | POST | Connect-Web subscribe |
| `/atmosphere.AtmosphereService/Send` | POST | Connect-Web send |
| (9090 gRPC) | gRPC bidi | Native gRPC chat stream |
