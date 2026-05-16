---
version: 1
app: spring-boot-orchestration-demo
archetype: agent-with-handoff
runtime: spring-boot-4 + atmosphere-agent + atmosphere-langchain4j
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/agent/support
console_mode: ai
obstacle_mode: auto
---

# spring-boot-orchestration-demo

Two-`@Agent` support-desk demo. A `SupportAgent` answers general queries and
hands off to `BillingAgent` over the same Atmosphere streaming session when
the message contains billing-related keywords (`bill`/`invoice`/`payment`/
`charge`/`refund`). The sample exercises three orchestration primitives in
one place:

1. **Plain-intent handoff** — `session.handoff("billing", message)` inside
   `SupportAgent.onPrompt()`. **Not** `@Fleet` / `LlmJudge` /
   declarative-routing — just a keyword check.
2. **`@Command` slash commands** — `/status`, `/hours`, `/purge` (the
   `confirm` attribute requires a second click).
3. **`@RequiresApproval` admin gate** — `SupportAgent.cancelAccount()` is
   `@AiTool`-callable but blocks for explicit user confirmation before
   running.

## Boot prerequisites

- JVM: JDK 21
- Default port: 8080.
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-orchestration-demo` from
  the Atmosphere repo root.
- Boot wait: ~1–4 s (observed start at 0.99 s).
- Env the SKILL.md must set:
  - `LLM_MODE=fake` — required for LLM-fallback prompts and `@AiTool` calls.
    Slash commands bypass the LLM entirely.
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Support Desk — handoffs, approval gates, commands",
  "endpoint": "/atmosphere/agent/support",
  "runtime": "demo",
  "mode": "ai"
}
```

The `/atmosphere/ai-chat` path is **aliased** to `/atmosphere/agent/support`
server-side so the console UI talks to one endpoint while the agent class
registers under its name-derived path. Subtitle matches
`atmosphere.console-subtitle` in `application.yml`.

## Structure

### Header / Navigation
- Subtitle: `"Support Desk — handoffs, approval gates, commands"`
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab — `/status` flow observed via chrome-devtools-mcp snapshot 2026-05-16

Send `/status`:
- User bubble: `[data-testid=message-bubble].message--user` — `/status`.
- Assistant bubble: `[data-testid=message-bubble].message--assistant` —
  body: `"Account status: Active. Plan: Professional. Next billing: April 15, 2026."`
- Token metrics: `"1 tokens · 19ms · 52.6 tok/s"` — bypass signal
  (`@Command` short-circuit).

### Other surfaces (out of must-pass scope)

- **`/hours`** — instant canned response with support-team hours.
- **`/purge`** — slash command with `confirm` attribute; first click warns,
  second click runs. Separate SKILL surface (multi-turn approval).
- **Plain prompt with billing keyword** — e.g. `"Where can I see my invoice?"`
  triggers `session.handoff("billing", …)`. The conversation transfers to
  `BillingAgent` over the same WebSocket. Surface signal: agent name changes
  in subsequent turns; not asserted in single-turn SKILL.
- **`"Cancel my account"`** — fires the `cancel_account` `@AiTool` which is
  `@RequiresApproval`-gated. Renders an `[data-testid=approval-prompt]`
  affordance for the user to confirm. Separate SKILL surface (multi-turn
  approval).

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- The handoff and approval flows are stateful within the WebSocket session —
  reloading the page between steps drops the session.

## Skip

- "Clear" button.
- Sessions/Policies/Decisions/Commitments/OWASP tabs — empty here.
- Handoff multi-turn SKILL — separate scenario.
- Approval-gate multi-turn SKILL — separate scenario.

## Tips

- `/status` is the cheapest must-pass surface: deterministic, single-turn,
  no LLM, no approval, no handoff. Asserting `"Account status"` substring
  is robust to copy edits on the date or plan tier.
- Subtitle `"Support Desk — handoffs, approval gates, commands"` is unique
  to this sample; use it in `console-info` to disambiguate.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/agent/support` | WebSocket | SupportAgent endpoint |
| `/atmosphere/agent/billing` | WebSocket | BillingAgent endpoint (handoff target) |
| `/atmosphere/ai-chat` | WebSocket | Alias → `/atmosphere/agent/support` |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/commands` | GET | Lists `@Command`s on both agents |
| `/api/tools` | GET | Lists `@AiTool`s on both agents |
