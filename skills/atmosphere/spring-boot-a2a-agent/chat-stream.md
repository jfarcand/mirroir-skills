---
version: 1
name: A2A agent — single-turn chat surface
app: spring-boot-a2a-agent
surface: web
tags: ["atmosphere", "agent", "a2a", "must-pass"]
---

Open the Atmosphere Console wired to an A2A-protocol-bearing `@Agent`,
send a prompt, verify the assistant bubble renders. The A2A JSON-RPC
surface (`/a2a`, `/.well-known/agent.json`) is a separate SKILL.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by
`SAMPLE.md` must include:

- `LLM_MODE=fake`.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8084/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports subtitle starting with `"A2A Agent —"`.

Port 8084 (not 8080).

## Steps

1. Open `http://127.0.0.1:8084/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello — one short sentence please."`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text).
8. Screenshot: `chat-stream-a2a-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit.

## Skip / obstacles

None when both env vars are set. A2A protocol SKILL (POST to `/a2a` with a
JSON-RPC `tasks/send` frame) is a separate scenario.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible.
- No console errors logged.
