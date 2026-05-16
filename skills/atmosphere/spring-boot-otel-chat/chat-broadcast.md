---
version: 1
name: OTel broadcast chat — single-turn user post
app: spring-boot-otel-chat
surface: web
tags: ["atmosphere", "broadcast", "opentelemetry", "must-pass"]
---

Open the Atmosphere Console wired to the OTel-instrumented broadcast endpoint,
post one message, verify the user bubble renders. The OpenTelemetry tracing
layer is server-side and invisible to the chat surface — covered by a
separate trace-verification SKILL.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by `SAMPLE.md`
must include:

- `ATMOSPHERE_AUTH_ENABLED=false`.

`LLM_MODE` is not read by this sample.

Boot ready when:
- `GET http://127.0.0.1:8084/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"mode":"broadcast"` with subtitle
  `"Multi-client broadcast chat"`.

**Port 8084** (not 8080) — declared in `application.properties` as
`server.port=8084`.

## Steps

1. Open `http://127.0.0.1:8084/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"hello from otel-chat"`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--user` to be visible.
7. Verify the user bubble renders (visible + non-empty text). **Do not**
   wait for or assert on `.message--assistant` — broadcast mode never
   produces one.
8. Screenshot: `chat-broadcast-otel-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. WebTransport (`port=4449`) is
offered to Chrome; others fall back to WebSocket.

## Skip / obstacles

None when `ATMOSPHERE_AUTH_ENABLED=false`. Jaeger collector at
`localhost:4317` is optional — span data is dropped silently if absent,
which does not affect chat behavior.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element matches.
- Zero `[data-testid=message-bubble].message--assistant` elements match.
- No console errors logged.
