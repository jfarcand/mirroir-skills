---
version: 1
name: Durable-sessions broadcast — single-turn user post
app: spring-boot-durable-sessions
surface: web
tags: ["atmosphere", "broadcast", "durable-sessions", "must-pass"]
---

Open the Atmosphere Console wired to a broadcast endpoint backed by durable-
session storage. Post one message, verify the user bubble renders. The
durable-session reconnect+replay flow is covered by a separate SKILL.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by
`SAMPLE.md` must include:

- `ATMOSPHERE_AUTH_ENABLED=false`.

`LLM_MODE` is not read by this sample.

Boot ready when:
- `GET http://127.0.0.1:8080/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"mode":"broadcast"` with
  `"runtime":"unknown"` (the distinct signal that no AgentRuntime is
  registered).

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"hello from durable-sessions"`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--user` to be visible.
7. Verify the user bubble renders (visible + non-empty text). Do not wait
   for or assert on `.message--assistant` — broadcast mode never produces
   one.
8. Screenshot: `chat-broadcast-durable-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit.

## Skip / obstacles

None when `ATMOSPHERE_AUTH_ENABLED=false`. Reconnect-and-replay SKILL is a
separate multi-turn scenario.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element matches.
- Zero `[data-testid=message-bubble].message--assistant` elements match.
- No console errors logged.
