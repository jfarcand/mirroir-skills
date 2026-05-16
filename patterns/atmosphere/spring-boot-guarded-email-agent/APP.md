---
version: 1
app: spring-boot-guarded-email-agent
archetype: agent-with-verifier
runtime: spring-boot-4 + atmosphere-agent + atmosphere-verifier
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/ai-chat
console_mode: ai
obstacle_mode: auto
---

# spring-boot-guarded-email-agent

`@Agent` that exposes an email-send tool gated by the `atmosphere-verifier`
module. The verifier runs pre-execution checks on tool arguments (recipient
format, content policy, allow-list domains, etc.) before the tool fires.
Under `LLM_MODE=fake`, the LLM is stubbed and the tool is never invoked, so
the SKILL.md surface looks like a plain demo-mode AI chat. The verifier
plane is observable via the REST surface (`/api/verifier/*`).

## Boot prerequisites

- JVM: JDK 21
- Default port: 8080 (no `application.yml` override).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-guarded-email-agent`.
- Boot wait: ~1–4 s (observed start at 1.39 s).
- Env the SKILL.md must set:
  - `LLM_MODE=fake`.
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Runtime: demo",
  "endpoint": "/atmosphere/ai-chat",
  "runtime": "demo",
  "mode": "ai"
}
```

Generic subtitle. The verifier wiring is invisible at the
`/api/console/info` level — confirm via `/api/verifier/info` instead.

## Structure

### Header / Navigation
- Subtitle: `"Runtime: demo"`
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab — observed via chrome-devtools-mcp snapshot 2026-05-16

Send `"Send an email to test@example.com"`:
- User bubble: `[data-testid=message-bubble].message--user` — body
  auto-linkifies the email address to `<a href="mailto:test@example.com">`.
- Assistant bubble: `[data-testid=message-bubble].message--assistant` — body
  echoes back `"You said: \"Send an email to test@example.com\""` plus the
  standard `"Demo mode — this response is a canned placeholder..."` marker.
- Token metrics: `"41 tokens · 1409ms · 29.1 tok/s"`.

The verifier plane does NOT fire on this surface under `LLM_MODE=fake`
because the demo LLM doesn't emit a tool call. To exercise the verifier:
- Boot with a real `LLM_API_KEY` so the LLM emits a `send_email` tool call.
- The verifier runs `EmailRecipientVerifier`, `ContentPolicyVerifier`, etc.
  before letting the tool fire. A denied verification renders an error
  bubble similar to `spring-boot-ms-governance-chat`.

### REST surface (out of must-pass scope)

- `GET /api/verifier/info` — list configured verifiers.
- `GET /api/verifier/decisions` — audit trail of allow/deny verifications.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- The verifier only runs on real tool calls; under demo mode it's silent.
  Do not assert verifier output in the chrome-devtools SKILL.

## Skip

- "Clear" button.
- Sessions/Policies/Decisions/Commitments/OWASP tabs — empty.
- Real-LLM verifier SKILL — separate scenario; needs `LLM_API_KEY`.

## Tips

- The Vue console's email autolink (`<a href="mailto:...">` injected into
  the user bubble) is incidental — markdown rendering, not a sample
  feature. Don't assert on the link.
- `/api/verifier/info` is the cheapest one-line check that the verifier
  registry loaded.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/ai-chat` | WebSocket | AI streaming endpoint with `@AiTool` send_email |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/verifier/info` | GET | Registered verifier list |
| `/api/verifier/decisions` | GET | Verifier audit log |
