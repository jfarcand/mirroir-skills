---
version: 1
app: spring-boot-agui-chat
archetype: chat-streaming-with-agui-protocol
runtime: spring-boot-4 + atmosphere-ai + atmosphere-agui
surface: web
url_root: http://127.0.0.1:8085/atmosphere/console/
console_endpoint: /atmosphere/ai-chat
console_mode: ai
obstacle_mode: auto
---

# spring-boot-agui-chat

AI streaming chat that **also speaks the AG-UI protocol** on the same
WebSocket. AG-UI (CopilotKit's agent-frontend protocol) is a structured
JSON event stream for tool-call activity, state snapshots, and approval
gates. On the Atmosphere Console surface the behavior is identical to
`spring-boot-ai-chat` — the AG-UI events only surface to AG-UI-aware
clients (e.g. CopilotKit React apps).

## Boot prerequisites

- JVM: JDK 21
- **Default port: 8085** (in `application.yml`).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-agui-chat` from the
  Atmosphere repo root.
- Boot wait: ~1–4 s (observed start at 0.92 s).
- Env the SKILL.md must set:
  - `LLM_MODE=fake`.
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "AG-UI Protocol Demo — streaming assistant with tool calls",
  "endpoint": "/atmosphere/ai-chat",
  "runtime": "demo",
  "mode": "ai"
}
```

The subtitle matches `atmosphere.console-subtitle` in `application.yml`.

## Structure

### Header / Navigation
- Subtitle: `"AG-UI Protocol Demo — streaming assistant with tool calls"`
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab — observed via chrome-devtools-mcp snapshot 2026-05-16

Send `"Hello AG-UI — one short sentence please."`:
- User bubble: `[data-testid=message-bubble].message--user`.
- Assistant bubble: `[data-testid=message-bubble].message--assistant` —
  demo-mode body `"You said: \"…\""` + the standard `"Demo mode — this
  response is a canned placeholder because no LLM_API_KEY is configured…"`
  marker.
- Token metrics: `"43 tokens · 1466ms · 29.3 tok/s"`.

On the Atmosphere Console, the AG-UI protocol is **transparent** — the chat
surface looks exactly like a plain AI streaming sample. The AG-UI events
(`TextMessageStart` / `TextMessageContent` / `TextMessageEnd` /
`ToolCallStart` / `StateSnapshot` etc.) are emitted on the same WebSocket
but the Vue console doesn't render them as distinct UI affordances; an
AG-UI-aware client (CopilotKit React) consumes them.

### AG-UI client (out of must-pass scope)

A CopilotKit React frontend pointed at this sample's WebSocket would
observe the full AG-UI event vocabulary. The console-driven must-pass
SKILL only proves the same WebSocket also speaks plain Atmosphere AI
streaming — i.e. the protocol multiplexing works.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- Port 8085 (not 8080).

## Skip

- "Clear" button.
- Sessions/Policies/Decisions/Commitments/OWASP tabs — empty.
- AG-UI-aware client SKILL (verify the `TextMessageStart` event sequence
  on the WebSocket) — separate scenario; would need a CopilotKit fixture.

## Tips

- Subtitle is the cheapest way to disambiguate from plain
  `spring-boot-ai-chat`.
- The AG-UI protocol layer doesn't affect the Console-surface SKILL — same
  selectors, same flow, same demo-mode body.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/ai-chat` | WebSocket | AI streaming + AG-UI multiplexed endpoint |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/agui/info` | GET | AG-UI protocol info (event vocabulary, version) |
