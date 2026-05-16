---
version: 1
app: spring-boot-otel-chat
archetype: broadcast-chat-with-otel
runtime: spring-boot-4 + atmosphere-runtime + opentelemetry-sdk
surface: web
url_root: http://127.0.0.1:8084/atmosphere/console/
console_endpoint: /atmosphere/ai-chat
console_mode: broadcast
obstacle_mode: auto
---

# spring-boot-otel-chat

Broadcast chat surface (same as `spring-boot-chat` and `quarkus-chat`) **plus**
full OpenTelemetry distributed tracing — every WebSocket connect, message,
suspend, and disconnect creates an OTel span. `AtmosphereTracing` is the
auto-configured interceptor; the chat itself behaves identically to the
plain broadcast sample. Span destination is configured via standard OTel env
vars (default `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`).

## Boot prerequisites

- JVM: JDK 21
- **Default port: 8084** (declared in `application.properties` as
  `server.port=8084` — NOT 8080).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-otel-chat` from the
  Atmosphere repo root.
- Boot wait: ~1–4 s (observed start at 1.22 s).
- Env the SKILL.md must set:
  - `ATMOSPHERE_AUTH_ENABLED=false`.
- `LLM_MODE` is not read — no AI module on the must-pass code path (the
  chat is `@ManagedService`-based broadcast).
- **Jaeger is OPTIONAL for the SKILL** — the OTel SDK is loaded but the
  tracing flow doesn't block on the exporter being reachable. Span data
  is dropped silently if no collector is at `localhost:4317`. To observe
  spans, `docker compose up -d` boots a Jaeger instance per the sample
  README, but this is out of scope for the must-pass chat SKILL.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Multi-client broadcast chat",
  "endpoint": "/atmosphere/ai-chat",
  "runtime": "demo",
  "mode": "broadcast"
}
```

Same subtitle string as `quarkus-chat` (`"Multi-client broadcast chat"`).
`mode: broadcast` is the runtime-truth signal that the SKILL.md must assert
on the user bubble, not the assistant bubble.

WebTransport sidecar is enabled (`atmosphere.web-transport.enabled=true` +
`port=4449` in `application.properties`); Chrome may negotiate HTTP/3 here.

## Structure

### Header / Navigation
- Subtitle: `"Multi-client broadcast chat"`
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab (broadcast variant)
- Status: `"Connected · websocket"`.
- Empty state (observed via chrome-devtools-mcp snapshot 2026-05-16):
  - Heading: `"Start a broadcast"`
  - Sub: `"Type a message below — every subscriber on this endpoint will receive it."`
  Same broadcast-aware copy as `spring-boot-chat` (Spring Console pivots on
  the `mode:broadcast` advertisement).
- After send: only `[data-testid=message-bubble].message--user` appears.
- **`.message--assistant` never appears** — broadcast mode, no LLM.

### OTel-specific surface (out of must-pass scope)

- Every chat round-trip emits OTel spans with attributes including
  `atmosphere.transport`, `atmosphere.resource_uuid`, `broadcaster.id`,
  `disconnect.reason`. Observable via Jaeger UI (`http://localhost:16686`)
  when the docker-compose collector is up.
- `actuator.endpoints.web.exposure.include=*` exposes the full actuator —
  health/metrics/info — but driving those is a separate SKILL surface.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- Port 8084 (not 8080) — common cause of "wrong sample replay" failures.

## Skip

- "Clear" button.
- Sessions/Policies/Decisions/Commitments/OWASP tabs — empty.
- Jaeger trace assertions — separate must-pass surface; require docker.
- Asserting on `.message--assistant` — broadcast mode never produces one.

## Tips

- The chat surface is identical to `spring-boot-chat` and `quarkus-chat`;
  the OTel layer is invisible in the SKILL.md surface. If you want to
  prove tracing wired, query `/actuator/metrics` for an `atmosphere.*`
  meter or hit Jaeger's API directly.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/ai-chat` | WebSocket | Broadcast endpoint |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/actuator/health` | GET | Health probe (all endpoints exposed) |
| `/actuator/metrics` | GET | Metrics including `atmosphere.*` meters |
| `/api/webtransport-info` | GET | WT info (port 4449) |
