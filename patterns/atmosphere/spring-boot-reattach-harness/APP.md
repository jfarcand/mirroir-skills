---
version: 1
app: spring-boot-reattach-harness
archetype: agent-with-reattach
runtime: spring-boot-4 + atmosphere-agent
surface: web
url_root: http://127.0.0.1:8096/atmosphere/console/
console_endpoint: /atmosphere/agent/harness
console_mode: ai
obstacle_mode: auto
---

# spring-boot-reattach-harness

`@Agent` test harness that streams **5 deterministically-numbered events**
(`event-0` through `event-4`) for any prompt. Designed so a reattach-aware
client can disconnect mid-stream, reconnect with the last-seen event index,
and verify replay+resume. From the Console-surface SKILL.md perspective the
chat behaves like an AI streaming sample; the deterministic event sequence
is the regression signal that the harness is wired.

## Boot prerequisites

- JVM: JDK 21
- **Default port: 8096** (in `application.yml`).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-reattach-harness`.
- Boot wait: ~3–6 s (observed start at 3.86 s).
- Env the SKILL.md must set:
  - `LLM_MODE=fake`.
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Runtime: demo",
  "endpoint": "/atmosphere/agent/harness",
  "runtime": "demo",
  "mode": "ai"
}
```

Endpoint `/atmosphere/agent/harness` is unique among samples.

## Structure

### Header / Navigation
- Subtitle: `"Runtime: demo"`
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab — observed via chrome-devtools-mcp snapshot 2026-05-16

Send any non-empty prompt:
- User bubble: `[data-testid=message-bubble].message--user`.
- Assistant bubble: `[data-testid=message-bubble].message--assistant` — body
  is the literal concatenated string `"event-0event-1event-2event-3event-4"`
  (5 streamed tokens, no whitespace between them — they're sent as
  individual `session.send()` calls without separators).
- Token metrics: `"6 tokens · 2572ms · 2.3 tok/s"`. The 6-token count
  (5 events + 1 completion) and ~2.5 s latency are deterministic
  regression signals; ~500 ms per event matches the harness's internal
  `Thread.sleep` between sends.

### Reattach SKILL (out of must-pass scope)

A reattach SKILL would:
1. Send a prompt and wait for `event-2` to appear.
2. Force-disconnect (kill the WebSocket).
3. Reconnect with the last-seen event index.
4. Verify the harness resumes from `event-3`.

Driving this requires a custom client that controls the disconnect+resume
handshake — out of scope for the chrome-devtools-only must-pass set.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- Port 8096 — non-standard.

## Skip

- "Clear" button.
- Tabs Sessions/Policies/Decisions/Commitments/OWASP — empty.
- Reattach resume SKILL — separate scenario, custom client.

## Tips

- The literal `"event-0"` substring in the assistant bubble is the strongest
  regression signal that the harness handler is wired. If the bubble shows
  any other content, the test agent has been replaced.
- `6 tokens` (not the usual `1 token` for short or `30+ tokens` for streamed)
  is a useful secondary check.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/agent/harness` | WebSocket | Reattach harness agent endpoint |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
