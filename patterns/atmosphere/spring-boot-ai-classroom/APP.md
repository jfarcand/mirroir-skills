---
version: 1
app: spring-boot-ai-classroom
archetype: chat-streaming-multi-room
runtime: spring-boot-4 + atmosphere-ai
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/classroom/{room}
console_mode: ai
obstacle_mode: auto
---

# spring-boot-ai-classroom

AI streaming with **multi-client room broadcast** — same `@AiEndpoint`/Atmosphere
plumbing as `spring-boot-ai-chat`, but the endpoint path is templated with a
`{room}` placeholder and the assistant stream is broadcast to every client
subscribed to that room. From a single-client SKILL.md perspective the surface
behaves identically to `spring-boot-ai-chat` (user bubble + assistant bubble);
the broadcast dimension only becomes observable with two clients on the same
room, which is out of scope for the must-pass replay set.

This sample also ships **two governance policies** that appear as a count
badge on the Console "Policies" tab.

## Boot prerequisites

- JVM: JDK 21
- Default port: 8080 (default Spring Boot; `application.yml` overrides
  `atmosphere.web-transport.port` to 4446 only).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-ai-classroom` from the
  Atmosphere repo root.
- Boot wait: ~1–10 s on a warm JVM (fastest of the samples observed so far —
  the snapshot captured a 1.47-second start). Ready when TCP `:8080` accepts
  connections AND `GET /atmosphere/console/` returns 200 AND
  `GET /api/console/info` reports `"endpoint":"/atmosphere/classroom/{room}"`.
- Env the SKILL.md must set:
  - `LLM_MODE=fake` — `FakeLlmClient` deterministic streaming.
  - `ATMOSPHERE_AUTH_ENABLED=false` — bypass auth (default would 401 the
    console).

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Runtime: demo",
  "endpoint": "/atmosphere/classroom/{room}",
  "runtime": "demo",
  "mode": "ai"
}
```

The literal `{room}` in `endpoint` is the runtime-truth signal that the
endpoint is templated. The Console resolves a default room internally — no
room selector renders in the Chat tab.

Subtitle `"Runtime: demo"` is the generic fallback (no
`atmosphere.console-subtitle` override in `application.yml`).

## Structure

### Header (banner)
- Heading: "Atmosphere AI Console"
- Subtitle: `"Runtime: demo"`
- Build-version chip: `"v4"`

### Navigation tabs

Six tabs: Chat / Sessions / **Policies 2** / Decisions / Commitments / OWASP.
The `"Policies 2"` badge is the runtime-truth signal that two governance
policies are registered (most other samples show `"Policies 0"`).

### Chat tab (default)
- Status: `"Connected · websocket"`.
- Same selector vocabulary as the other AI samples (`chat-input`,
  `chat-send`, `message-bubble`, `.message--user`, `.message--assistant`).
- Assistant streaming body observed via chrome-devtools-mcp snapshot
  2026-05-15 for prompt `"Hello classroom — one short sentence please."`:
  `"Classroom AI: Every student in this room is seeing this response stream
  in real time — that's Atmosphere's broadcaster at work! Set LLM_API_KEY to
  connect to a real AI model."`
- Token metrics: `"31 tokens · 1095ms · 28.3 tok/s"` (FakeLlmClient stream).
- No tool-activity panel (no `@AiTool`s on this endpoint).

### Policies tab (badge "2")

Out of scope for the must-pass streaming SKILL, but worth knowing: the badge
reflects `PolicyRegistry` content from the `RoomContextInterceptor` /
`ClassroomPolicy*` beans. Asserting on the badge count would couple the
SKILL.md to governance config, so the streaming SKILL.md does **not** check it.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401 on the console; status hangs at
  "Connecting".
- The Expo sibling (`samples/spring-boot-ai-classroom/expo-client/`) connects
  to this server but lives in its own subdirectory; do **not** boot it as part
  of this SKILL.md — it is a separate must-pass surface for the Expo runtime.

## Skip

- "Clear" button.
- Sessions / Decisions / Commitments / OWASP tabs — empty here.
- Multi-room SKILL.md — would need two browser contexts on different rooms;
  out of scope for the single-client replay.

## Tips

- The endpoint advertisement keeps the literal `{room}` in the string — this
  is correct behavior (the Console resolves it server-side), not a leakage.
- No tool calls means **no** `[data-testid=tool-activity]` panel rendered;
  asserting one would be wrong here.
- `"Policies 2"` badge is the cheapest signal that the classroom-specific
  policy beans loaded; if you ever see `"Policies 0"`, the
  `ClassroomPolicy*Configuration` is not picking up.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/classroom/{room}` | WebSocket | Per-room AI streaming endpoint |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/policies` | GET | Lists the two registered governance policies |
