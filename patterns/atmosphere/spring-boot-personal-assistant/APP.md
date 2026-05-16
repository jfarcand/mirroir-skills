---
version: 1
app: spring-boot-personal-assistant
archetype: agent-with-crew
runtime: spring-boot-4 + atmosphere-agent + atmosphere-coordinator
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/agent/primary-assistant
console_mode: ai
obstacle_mode: auto
---

# spring-boot-personal-assistant

Long-lived memory-bearing `@Agent` with a three-member crew (scheduler /
research / drafter) dispatched through `InMemoryProtocolBridge`. Exercises the
v0.5 foundation primitives: `AgentState`, `AgentWorkspace`, `AgentIdentity`,
`ToolExtensibilityPoint`, `AiGateway`, `ProtocolBridge`. Same Console SPA + AI
streaming surface as `spring-boot-ai-chat`; the crew dispatch is server-side
and not observable through the chat surface in a single SKILL turn.

## Boot prerequisites

- JVM: JDK 21
- Default port: 8080 (no `application.yml` override).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-personal-assistant` from
  the Atmosphere repo root.
- Boot wait: ~1–5 s (observed start at 1.34 s).
- Env the SKILL.md must set:
  - `LLM_MODE=fake` — `FakeLlmClient` deterministic streaming.
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Runtime: demo",
  "endpoint": "/atmosphere/agent/primary-assistant",
  "runtime": "demo",
  "mode": "ai"
}
```

The endpoint `/atmosphere/agent/primary-assistant` is the runtime-truth signal
that the `@Agent(name = "primary-assistant")` registered correctly. Subtitle
is the generic `"Runtime: demo"` fallback (no `atmosphere.console-subtitle`
override).

## Structure

### Header / Navigation
- Heading: "Atmosphere AI Console"
- Subtitle: `"Runtime: demo"`
- Build-version chip: `"v4"`
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab — observed via chrome-devtools-mcp snapshot 2026-05-16

Send `"Hello assistant — one short sentence please."`:
- User bubble: `[data-testid=message-bubble].message--user` — "U" / prompt / timestamp.
- Assistant bubble: `[data-testid=message-bubble].message--assistant` — demo-mode body:
  ```
  I can schedule meetings, research topics, or draft messages.
  Configure OPENAI_API_KEY to let me pick the right tool automatically;
  otherwise try keywords like 'schedule', 'research', or 'draft'.
  ```
  Token metrics: `"1 tokens · 31ms · 32.3 tok/s"` — the `"1 tokens"` count is
  the bypass signal that this turn came from the demo-mode short-circuit,
  not from the LLM. A real-LLM boot (with `OPENAI_API_KEY` set) would stream
  tokens through the model and show higher counts.

The assistant body invites three crew-dispatch keywords (`schedule`, `research`,
`draft`). Each keyword triggers a different crew member via
`InMemoryProtocolBridge`. Asserting on specific crew dispatch shape is out of
scope for the must-pass replay (would couple the SKILL.md to crew-internal
behavior).

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401 on the console.
- Real-LLM mode (`OPENAI_API_KEY` set) makes assistant responses non-
  deterministic and rate-limit-sensitive; SKILL.md asserts structure only.
- The bundled `agent-workspace/` directory is **seed data** — at runtime each
  `userId × agent` combination writes to its own subtree under
  `users/<userId>/agents/primary-assistant/`. Don't mutate the seed during
  SKILL.md runs; the harness should treat the workspace as immutable.

## Skip

- "Clear" button.
- Sessions/Policies/Decisions/Commitments/OWASP tabs — empty here.
- Crew-dispatch SKILLs (verifying the scheduler / research / drafter crew
  members receive sub-tasks via `InMemoryProtocolBridge`) — server-side
  behavior, not observable through the chat surface in one turn.
- Multi-turn workspace-memory SKILL — would require sequential prompts and
  cross-turn state assertion; out of scope for the must-pass set.

## Tips

- The default reply is the cheapest reproducible surface. Any non-empty prompt
  returns the same canned demo-mode response — assert on `.message--assistant`
  visibility, not on specific keywords (which would lock the SKILL to the
  current crew menu).
- `endpoint:/atmosphere/agent/primary-assistant` is unique to this sample;
  use it in `console-info` to distinguish from siblings like `dentist-agent`
  or `coding-agent`.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/agent/primary-assistant` | WebSocket | Agent endpoint |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/agents` | GET | Lists registered `@Agent`s + crew members |
| `/actuator/health` | GET | CI readiness probe |
