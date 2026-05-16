---
version: 1
app: spring-boot-checkpoint-agent
archetype: agent-with-checkpoint
runtime: spring-boot-4 + atmosphere-agent + atmosphere-checkpoint
surface: web
url_root: http://127.0.0.1:8095/atmosphere/console/
console_endpoint: /atmosphere/agent/dispatch
console_mode: ai
obstacle_mode: auto
---

# spring-boot-checkpoint-agent

`@Agent` that **persists every dispatch result via `CheckpointStore`** so a
disconnected client (or a human reviewer) can resume the conversation by
checkpoint id. The distinguishing surface in the chat is the assistant body
that explicitly names the REST endpoints for reviewing and approving the
checkpoint (`GET /api/checkpoints`, `POST /api/checkpoints/{id}/approve`).

## Boot prerequisites

- JVM: JDK 21
- **Default port: 8095** (in `application.yml`).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-checkpoint-agent` from
  the Atmosphere repo root.
- Boot wait: ~2–4 s (observed start at 2.15 s — longer than simple samples
  because the checkpoint module initializes the SQLite store).
- Env the SKILL.md must set:
  - `LLM_MODE=fake`.
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Runtime: demo",
  "endpoint": "/atmosphere/agent/dispatch",
  "runtime": "demo",
  "mode": "ai"
}
```

The endpoint `/atmosphere/agent/dispatch` is unique. Subtitle is the generic
fallback.

## Structure

### Header / Navigation
- Subtitle: `"Runtime: demo"`
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab — observed via chrome-devtools-mcp snapshot 2026-05-16

Send `"Hello — one short sentence please."`:
- User bubble: `[data-testid=message-bubble].message--user`.
- Assistant bubble: `[data-testid=message-bubble].message--assistant` —
  body:
  ```
  You said: "Analysis complete.
  Result: Unknown skill: analyze
  This result has been checkpointed. Review at GET /api/checkpoints (filter
  by coordination=dispatch) and POST /api/checkpoints/{id}/approve to resume."
  Demo mode — this response is a canned placeholder because no LLM_API_KEY is
  configured. Export a Gemini, OpenAI, or Ollama key (see the sample README)
  and restart to get a real AI reply.
  ```
- Token metrics: `"61 tokens · 2138ms · 28.5 tok/s"`.

The `"This result has been checkpointed"` substring is the runtime-truth
signal that the checkpoint store wired correctly. A failing assertion here
would mean the checkpoint module silently no-op'd.

### Checkpoint REST surface (out of must-pass scope)

- `GET /api/checkpoints?coordination=dispatch` lists pending checkpoints
  with their stored payloads.
- `POST /api/checkpoints/{id}/approve` resumes the dispatched flow.

Driving these endpoints is a separate must-pass surface (curl-driven
REST SKILL, not console UI).

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- Port 8095 — non-standard, must be set explicitly in scenarios.
- SQLite checkpoint file `atmosphere-checkpoints.db` is created in the
  working directory on first run; subsequent boots **re-read** it, so old
  checkpoints from previous runs may surface. Clean the file between SKILL
  invocations if checkpoint state matters to the assertion.

## Skip

- "Clear" button.
- Sessions/Policies/Decisions/Commitments/OWASP tabs — empty.
- Multi-turn checkpoint→approve REST flow — separate SKILL.

## Tips

- Asserting on the substring `"checkpointed"` in the assistant bubble is
  the cheapest signal that the checkpoint store is wired.
- The reply body includes the literal `"Unknown skill: analyze"` because
  no `@AgentSkill` matches the demo prompt — that's expected demo behavior;
  the checkpointing happens regardless.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/agent/dispatch` | WebSocket | Checkpoint-bearing agent endpoint |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/checkpoints` | GET | List pending checkpoints |
| `/api/checkpoints/{id}/approve` | POST | Resume a checkpoint |
