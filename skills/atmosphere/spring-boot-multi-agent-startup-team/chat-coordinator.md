---
version: 1
name: Coordinator fleet — single-turn fan-out
app: spring-boot-multi-agent-startup-team
surface: web
tags: ["atmosphere", "coordinator", "fleet", "must-pass"]
---

Open the Atmosphere Console wired to the `ceo` `@Coordinator`, send a prompt,
verify both the assistant bubble and a populated `[data-testid=tool-activity]`
panel render. The panel must contain entries from multiple specialist agents
(research / strategy / finance / writer) plus the Coordination Journal.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by `SAMPLE.md`
must include:

- `LLM_MODE=fake` — deterministic demo-mode bodies + cached web-search
  results, so the SKILL.md observes a fixed shape regardless of LLM key.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8080/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"endpoint":"/atmosphere/agent/ceo"`
  with `"runtime":"demo"`.

Boot itself takes ~7 s — the runner must wait on the `Started
A2aStartupTeamApplication` log line, not just a port-open probe.

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Should we enter the SaaS analytics market?"` (any non-empty
   prompt works — the demo coordinator runs the same fan-out regardless of
   content).
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible
   — this can take up to ~15 s because of the 5-agent fan-out + synthesis
   step. Use a wait_for with `timeout: 20000`.
7. Verify both:
   - `[data-testid=message-bubble].message--assistant` is visible with non-
     empty text.
   - `[data-testid=tool-activity]` is visible (the `"AGENT COLLABORATION"`
     panel populated by the coordinator's fan-out).
8. Screenshot: `chat-coordinator-fanout-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. WebTransport (`h3=":4446"`) is
advertised via Alt-Svc but Chrome usually negotiates WS first; the
`"Connected"` prefix-match is transport-agnostic.

## Skip / obstacles

None when both env vars are set. With a real `GEMINI_API_KEY`/`OPENAI_API_KEY`,
the LLM is invoked for the synthesis step; the fan-out shape stays the same
and the SKILL.md still passes.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible.
- Exactly one `[data-testid=tool-activity]` panel matches and is visible.
  The panel must contain multiple tool entries — a single-entry panel would
  indicate the coordinator regressed to a single-agent path.
- The Console nav shows `"Policies 4"` (the governance plane is wired).
- No console errors logged.
