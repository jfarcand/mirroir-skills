---
version: 1
name: Personal assistant — single-turn demo-mode reply
app: spring-boot-personal-assistant
surface: web
tags: ["atmosphere", "agent", "crew", "must-pass"]
---

Open the Atmosphere Console wired to the `primary-assistant` `@Agent`, send a
prompt, verify the assistant bubble renders. The agent's crew (scheduler /
research / drafter) is dispatched server-side via `InMemoryProtocolBridge`
and is not observable through this single-turn SKILL.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by `SAMPLE.md`
must include:

- `LLM_MODE=fake` — `FakeLlmClient` deterministic streaming for the LLM-
  fallback path.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8080/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports
  `"endpoint":"/atmosphere/agent/primary-assistant"` with
  `"runtime":"demo"`.

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello assistant — one short sentence please."`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text). Do not
   assert on specific copy — demo-mode returns a canned response that may
   change as the crew menu evolves.
8. Screenshot: `chat-stream-personal-assistant-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. `"Connected"` prefix-match is
transport-agnostic.

## Skip / obstacles

None when both env vars are set. With `OPENAI_API_KEY` exported, responses
become non-deterministic — the SKILL.md still passes (assistant bubble
renders) but body varies.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible.
- Zero `[data-testid=tool-activity]` panels (the assistant body in demo mode
  does not invoke crew via the visible tool path).
- No console errors logged.
