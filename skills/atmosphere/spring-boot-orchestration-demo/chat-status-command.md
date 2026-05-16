---
version: 1
name: Support desk — /status round-trip
app: spring-boot-orchestration-demo
surface: web
tags: ["atmosphere", "agent", "command", "must-pass"]
---

Open the Atmosphere Console wired to the `SupportAgent` and send `/status`;
verify the canned account-status response renders in the assistant bubble.
The slash-command short-circuit bypasses the LLM and exercises the
`@Command` path. Handoff and approval-gate flows are covered by separate
SKILLs.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by `SAMPLE.md`
must include:

- `LLM_MODE=fake`.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when `GET /api/console/info` reports
`"endpoint":"/atmosphere/agent/support"` with subtitle
`"Support Desk — handoffs, approval gates, commands"`.

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"/status"`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text). Body
   contains `"Account status"`.
8. Screenshot: `chat-status-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. Slash-command latency is
consistent (~20 ms observed).

## Skip / obstacles

None when both env vars are set.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element with text
  `"/status"`.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible. Body contains `"Account status"`.
- Token metrics show `"1 tokens"` — bypass signal.
- Zero `[data-testid=tool-activity]` panels.
- Zero `[data-testid=approval-prompt]` affordances.
- No console errors logged.
