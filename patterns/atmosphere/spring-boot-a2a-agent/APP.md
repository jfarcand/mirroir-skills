---
version: 1
app: spring-boot-a2a-agent
archetype: a2a-agent
runtime: spring-boot-4 + atmosphere-agent + atmosphere-a2a
surface: web
url_root: http://127.0.0.1:8084/atmosphere/console/
console_endpoint: /atmosphere/ai-chat
console_mode: ai
obstacle_mode: auto
---

# spring-boot-a2a-agent

`@Agent` reachable over both the chat surface AND the A2A
(Agent-to-Agent) protocol. The A2A protocol lets a remote agent host
discover this agent via `.well-known/agent.json` and dispatch tasks
through structured JSON-RPC frames. Tools advertised: `weather`, `time`.
On the chat surface the behavior is standard demo-mode AI; A2A clients
get the agent card + RPC frames.

## Boot prerequisites

- JVM: JDK 21
- **Default port: 8084** (in `application.yml`).
- Command: `./mvnw -q spring-boot:run -pl samples/spring-boot-a2a-agent`.
- Boot wait: ~1–4 s (observed start at 1.32 s).
- Env the SKILL.md must set:
  - `LLM_MODE=fake`.
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "A2A Agent — weather and time via Agent-to-Agent protocol",
  "endpoint": "/atmosphere/ai-chat",
  "runtime": "demo",
  "mode": "ai"
}
```

Subtitle is the distinguishing signal that the A2A plane is wired
(matches `application.yml` console-subtitle).

## Structure

### Header / Navigation
- Subtitle: `"A2A Agent — weather and time via Agent-to-Agent protocol"`
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab — observed via chrome-devtools-mcp snapshot 2026-05-16

Send any non-empty prompt:
- User bubble: `[data-testid=message-bubble].message--user`.
- Assistant bubble: `[data-testid=message-bubble].message--assistant` —
  standard demo-mode body `"You said: …"` + `"Demo mode — ..."` marker.
- Token metrics: `"41 tokens · 1405ms · 29.2 tok/s"`.

Note: prompts like `"What's the weather in Paris?"` do NOT trigger the
`weather` tool on the chat surface under `LLM_MODE=fake` — the stub LLM
doesn't emit tool calls. A real LLM (`OPENAI_API_KEY` set) would surface
the tool call in the chat AND the same tool would be invocable via the
A2A protocol from a remote agent host.

### A2A surface (out of must-pass scope)

- `/.well-known/agent.json` — Agent card (discoverable agent metadata
  including tool schemas).
- `/a2a` — A2A JSON-RPC transport (HTTP POST endpoint for `tasks/send`,
  `tasks/get`, etc.).

A2A SKILL would POST a `tasks/send` JSON-RPC frame and verify the agent
returns a streamed task result. Separate fixture-based scenario.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- Port 8084 — non-standard.

## Skip

- "Clear" button.
- Tabs Sessions/Policies/Decisions/Commitments/OWASP — empty.
- A2A protocol SKILL — separate JSON-RPC fixture scenario.
- Asserting on weather/time tool output — needs real LLM.

## Tips

- The subtitle `"A2A Agent — weather and time…"` is the cheapest signal
  that the A2A plane is wired without needing to query `.well-known/agent.json`.
- For an A2A interop SKILL, `curl -s /.well-known/agent.json | jq .name`
  is the cheapest dependency-free verification.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/ai-chat` | WebSocket | Chat-surface AI endpoint |
| `/.well-known/agent.json` | GET | A2A agent card (discoverable metadata) |
| `/a2a` | POST | A2A JSON-RPC transport (`tasks/send`, etc.) |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
