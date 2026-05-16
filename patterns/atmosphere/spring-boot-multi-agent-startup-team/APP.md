---
version: 1
app: spring-boot-multi-agent-startup-team
archetype: coordinator-fleet
runtime: spring-boot-4 + atmosphere-agent + atmosphere-coordinator
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/agent/ceo
console_mode: ai
obstacle_mode: auto
---

# spring-boot-multi-agent-startup-team

`@Coordinator` fleet sample. A "CEO" coordinator agent dispatches sub-tasks to
four specialist `@Agent`s (research / strategy / finance / writer) over the
A2A protocol, then synthesizes the per-agent outputs into one executive
briefing streamed back to the chat surface. The distinguishing surface in
the Console is a rich `[data-testid=tool-activity]` panel containing
**multiple tool entries plus a Coordination Journal table** rendered in the
same turn.

## Boot prerequisites

- JVM: JDK 21
- Default port: 8080 (`SERVER_PORT` env override supported).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-multi-agent-startup-team`
  from the Atmosphere repo root.
- Boot wait: ~7–12 s (observed start at 7.3 s — slower than simpler samples
  because it loads the coordinator + 4 agents + SQLite checkpoint store).
- Env the SKILL.md must set:
  - `LLM_MODE=fake` — `FakeLlmClient` so the demo body and the cached web-
    search results are deterministic.
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Runtime: demo",
  "endpoint": "/atmosphere/agent/ceo",
  "runtime": "demo",
  "mode": "ai"
}
```

The endpoint `/atmosphere/agent/ceo` is the runtime-truth signal that the
`@Coordinator(name = "ceo")` registered correctly. The 4 specialist agents
(research / strategy / finance / writer) are dispatched server-side via A2A
and don't get their own console endpoint.

## Structure

### Header / Navigation
- Heading: "Atmosphere AI Console"
- Subtitle: `"Runtime: demo"`
- Build-version chip: `"v4"`
- Six tabs: Chat / Sessions / **Policies 4** / Decisions / Commitments / OWASP.

The `"Policies 4"` badge is unique among samples observed so far — four
governance policies are registered (`@AgentScope` on the coordinator +
`PolicyAdmissionGate` + `GovernanceFleetInterceptor` policies). Use the
badge as a runtime-truth check that the governance plane is wired.

### Chat tab — observed via chrome-devtools-mcp snapshot 2026-05-16

Send any non-empty prompt (e.g. `"Hello team — one short sentence please."`):

- User bubble: `[data-testid=message-bubble].message--user`.
- Tool-activity panel: `[data-testid=tool-activity]` — header `"AGENT
  COLLABORATION"` with **6 tool entries** rendered sequentially:
  1. **Web Search** — `query: <prompt>`, returns 3 cached results (Market
     Overview, Competitive Landscape, Funding Trends).
  2. **Analyze Strategy** — `market: <prompt>`, returns SWOT-ish text with
     `MARKET CONTEXT / OPPORTUNITIES / THREATS / COMPETITIVE POSITIONING`.
  3. **Financial Model** — `market: <prompt>`, returns canned TAM/SAM/SOM +
     revenue projections + cost structure + funding.
  4. **Write Report** — `title: <prompt>`, produces an `EXECUTIVE BRIEFING`
     block.
  5. **Write Report** (second pass) — appears twice in the journal because
     the coordinator re-routes the writer-agent's output.
  6. **Coordination Journal** — `query: all events`, renders the full event
     table with columns `Event / Agent / Detail / Duration` (rows:
     `DISPATCH / DONE / START / COMPLETE / ROUTE` per dispatched agent).
- Assistant bubble: `[data-testid=message-bubble].message--assistant` — the
  synthesized briefing, prefixed with `"You said: \"…\""` followed by the
  full demo-mode marker:
  `"Demo mode — this response is a canned placeholder because no LLM_API_KEY
  is configured. Export a Gemini, OpenAI, or Ollama key (see the sample
  README) and restart to get a real AI reply."`
- Token metrics: `"379 tokens · 13120ms · 28.9 tok/s"` — much higher token
  count than single-agent samples (37x `spring-boot-ai-chat`), and much
  longer latency (~13 s). Both are direct consequences of the 5-agent
  fan-out.

### Coordination Journal (observed)

Sample row sequence captured from snapshot:
- `DISPATCH research-agent web_search —`
- `DONE research-agent web_search 441ms`
- `START — ceo —`
- `DISPATCH strategy-agent analyze_strategy —`
- `DISPATCH finance-agent financial_model —`
- `DONE strategy-agent analyze_strategy 6ms`
- `DONE finance-agent financial_model 6ms`
- `COMPLETE — 2 calls 10ms`
- `DISPATCH writer-agent write_report —`
- `DONE writer-agent write_report 3ms`
- `ROUTE finance-agent route[1] -> writer-agent —`

This event sequence is the runtime-truth signal that parallel dispatch
(strategy + finance fan-out from CEO), sequential dependency (writer-agent
consumes the strategy + finance outputs), and explicit ROUTE markers are
all wired through `AgentFleet`.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401 on the console.
- Without `LLM_MODE=fake`, the coordinator falls back to demo-mode anyway
  (no `GEMINI_API_KEY`/`OPENAI_API_KEY`), but the demo body is still
  served — `LLM_MODE=fake` just shortcircuits the LLM probe.
- Boot is ~7 s — SKILL.md must wait long enough for the `Started …
  Application` log line, not just a port-open probe.

## Skip

- "Clear" button.
- "Cancel inflight" on the Sessions tab — would abort the coordinator mid-
  fan-out, which is a useful SKILL but separate from the must-pass flow.
- Asserting on specific Coordination Journal row counts — the demo mode
  produces a stable count today (10–11 rows) but adding a specialist
  changes that.
- WebTransport HTTP/3 connection — the Alt-Svc header advertises `h3=":4446"`
  but Chrome may negotiate WS first under most boot conditions.

## Tips

- The 6-entry tool-activity panel is the strongest visible signal that the
  coordinator fanout is working. A passing assistant-bubble assertion
  without the panel means the coordinator regressed to a single-shot AI
  endpoint.
- `"Policies 4"` is the cheapest governance-wired check.
- The Coordination Journal rows include `route[N] -> agent-name` strings;
  these are stable identifiers and useful for regression testing the fleet
  routing.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/agent/ceo` | WebSocket | Coordinator endpoint |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/policies` | GET | Lists the 4 registered policies |
| `/api/webtransport-info` | GET | Returns `{enabled, port:4446, certHash}` |
| `/atmosphere/admin/` | GET | Admin dashboard with kill-switch / OWASP |
