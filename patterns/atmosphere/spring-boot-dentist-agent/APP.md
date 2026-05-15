---
version: 1
app: spring-boot-dentist-agent
archetype: agent-with-commands
runtime: spring-boot-4 + atmosphere-ai + atmosphere-channels
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/ai-chat
console_mode: ai
obstacle_mode: auto
---

# spring-boot-dentist-agent

`@Agent` with **slash-command short-circuit** plus AI tools. "Dr. Molar" handles
dental-emergency triage. The distinguishing feature vs `spring-boot-ai-chat` /
`spring-boot-ai-tools` is the **`@Command` annotation** — slash-prefixed inputs
(`/firstaid`, `/urgency`, `/pain`, `/help`) bypass the LLM entirely and return
deterministic canned responses in ~27 ms (observed) instead of streaming
through the model. Natural-language prompts still fall through to `@Prompt`
and may invoke the two registered `@AiTool`s (`assess_emergency`,
`pain_relief`).

The sample also wires `atmosphere-channels` so the same `@Command` handlers
are reachable from Slack/Telegram/Discord/WhatsApp/Messenger when channel
adapters are configured — out of scope for the web SKILL.md.

## Boot prerequisites

- JVM: JDK 21
- Default port: 8080 (no override in `application.yml`).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-dentist-agent` from the
  Atmosphere repo root.
- Boot wait: ~1–5 s on a warm JVM (observed start at 1.51 s). Ready when TCP
  `:8080` accepts connections AND `GET /atmosphere/console/` returns 200 AND
  `GET /api/console/info` reports `"endpoint":"/atmosphere/ai-chat"` with
  `"runtime":"demo"`.
- Env the SKILL.md must set:
  - `LLM_MODE=fake` — `FakeLlmClient` for the LLM fallback path. The
    slash-command path doesn't need the LLM, so `LLM_MODE` is **only** load-
    bearing if you intend to send a natural-language prompt.
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

The endpoint reports as a regular `/atmosphere/ai-chat`; the `@Command`
dispatch is internal to the agent and not advertised. Subtitle is the
generic `"Runtime: demo"` fallback.

## Structure

### Header / Navigation
- Heading: "Atmosphere AI Console", subtitle "Runtime: demo", chip "v4".
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab — `/help` flow observed via chrome-devtools-mcp snapshot 2026-05-15

Send `/help`:
- User bubble: `[data-testid=message-bubble].message--user` — "U" / "/help" / timestamp.
- Assistant bubble: `[data-testid=message-bubble].message--assistant` — multi-line:
  ```
  Available commands:
  /pain — Pain management tips
  /firstaid — Quick first-aid steps for a broken tooth
  /urgency — Help determine how urgently you need a dentist
  /help — Show this help message
  ```
  (line breaks are rendered as `<br>` in the markdown body; the snapshot
  shows them as four `LineBreak` nodes between text blobs).
- Token metrics: `"1 tokens · 27ms · 37.0 tok/s"` — **1 token** and **27ms**
  are the runtime-truth signals that this turn bypassed the LLM. A real LLM
  invocation would be ~30+ tokens / ~1000+ms (see `spring-boot-ai-chat`).

The four `@Command`-annotated methods auto-populate the `/help` output —
adding a new `@Command` automatically updates `/help` without any code in
the help handler itself.

### Natural-language prompts (not driven by must-pass SKILL)

A non-slash prompt like `"My tooth is throbbing, what should I do?"` would
fall through to `@Prompt`, may trigger the `assess_emergency` or `pain_relief`
`@AiTool`s via LLM tool-calls (rendering a `[data-testid=tool-activity]`
panel like `spring-boot-ai-tools`), and stream a normal assistant body.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401 on the console.
- Channel adapters (Slack/Telegram/Discord/WhatsApp/Messenger) require
  per-channel tokens (`SLACK_BOT_TOKEN`, `TELEGRAM_BOT_TOKEN`, etc.). With
  none set, the web surface still works; channel adapters silently no-op at
  boot.

## Skip

- "Clear" button.
- Sessions/Policies/Decisions/Commitments/OWASP tabs — empty in this sample.
- Channel adapter SKILLs — separate must-pass set; require per-channel auth.
- Natural-language prompt SKILL — covered by the `spring-boot-ai-tools`
  pattern; not duplicated here.

## Tips

- `/help` is the cheapest must-pass surface because:
  - It is auto-generated from the registered `@Command`s — text changes if
    commands are added/removed, so asserting `"Available commands"` plus
    presence of `/firstaid`, `/urgency`, `/pain` covers regressions.
  - It does not depend on `LLM_MODE` — bypasses the LLM entirely.
- If you want to verify the `@AiTool` path on this sample, send
  `"My tooth is throbbing, level 9 pain"` and wait on
  `[data-testid=tool-activity]` in addition to the assistant bubble.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/ai-chat` | WebSocket | Agent endpoint (`@Command` + `@Prompt`) |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/commands` | GET | Lists registered `@Command`s (admin/observability) |
| `/api/tools` | GET | Lists registered `@AiTool`s |
