---
version: 1
app: spring-boot-channels-chat
archetype: chat-with-channels
runtime: spring-boot-4 + atmosphere-ai + atmosphere-channels
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/ai-chat
console_mode: ai
obstacle_mode: auto
---

# spring-boot-channels-chat

AI chat wired to `atmosphere-channels` — the same `@AiEndpoint` reachable from
the web Console **and** from Slack/Telegram/Discord/WhatsApp/Messenger when
the respective adapter env vars are set. On the Console surface the chat
behaves like a plain Built-in-runtime AI chat. The channel webhooks are
registered at boot but no-op when channel credentials are absent.

## Boot prerequisites

- JVM: JDK 21
- Default port: 8080.
- Command: `./mvnw -q spring-boot:run -pl samples/spring-boot-channels-chat`.
- Boot wait: ~2–4 s (observed start at 1.93 s).
- Env the SKILL.md must set:
  - `LLM_MODE=fake`.
  - `ATMOSPHERE_AUTH_ENABLED=false`.
- Channel adapter env vars (Slack/Telegram/Discord/WhatsApp/Messenger) — all
  optional. With none set, channel webhooks register at boot but receive no
  events.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Runtime: built-in",
  "endpoint": "/atmosphere/ai-chat",
  "runtime": "built-in",
  "mode": "ai"
}
```

**`runtime: built-in`** is the distinguishing signal — most other samples
report `runtime: demo`. This sample uses Atmosphere's Built-in `AgentRuntime`
which ships its own short-reply demo path (without the
`DemoAgentRuntime` fallback marker).

## Structure

### Header / Navigation
- Subtitle: `"Runtime: built-in"`
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab — observed via chrome-devtools-mcp snapshot 2026-05-16

Send `"Hello channels — one short sentence please."`:
- User bubble: `[data-testid=message-bubble].message--user`.
- Assistant bubble: `[data-testid=message-bubble].message--assistant` — body
  is the **short canned reply** `"Hello there!"` (NOT the `"You said: …
  Demo mode"` echo seen in `runtime: demo` samples). This is the Built-in
  runtime's response shape.
- Token metrics: `"1 tokens · 989ms · 1.0 tok/s"`. The `"1 tokens"` count
  matches the short reply — Built-in runtime emits a single output token.

### Channel surface (out of must-pass scope)

- `/webhook/slack`, `/webhook/telegram`, etc. are registered at boot.
- A SKILL that exercises a channel would need to POST a webhook payload
  representing the channel's event (e.g. Slack Events API JSON) — a
  separate fixture-based scenario, not chrome-devtools-driven.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- The Built-in runtime's `"Hello there!"` reply is hardcoded for short
  prompts. Longer/more specific prompts may surface different built-in
  responses; SKILL.md should assert structure (`.message--assistant`
  visible), not specific copy.

## Skip

- "Clear" button.
- Sessions/Policies/Decisions/Commitments/OWASP tabs — empty.
- Channel webhook SKILLs — separate scenarios, channel-specific fixtures.

## Tips

- `runtime: built-in` is the cheapest distinguisher from the `runtime: demo`
  cohort.
- The Built-in runtime's `"1 tokens"` short reply doesn't include the
  `"Demo mode"` marker — useful as a regression signal (if the marker
  appears, the sample regressed to demo).

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/ai-chat` | WebSocket | Built-in-runtime AI endpoint |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/webhook/slack` | POST | Slack Events API webhook (no-op without `SLACK_BOT_TOKEN`) |
| `/webhook/telegram` | POST | Telegram webhook |
| `/webhook/discord` | POST | Discord webhook |
| `/webhook/whatsapp` | POST | WhatsApp webhook |
| `/webhook/messenger` | POST | Messenger webhook |
