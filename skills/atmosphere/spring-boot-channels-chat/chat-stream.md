---
version: 1
name: Channels chat — single-turn Built-in runtime reply
app: spring-boot-channels-chat
surface: web
tags: ["atmosphere", "ai-chat", "channels", "built-in", "must-pass"]
---

Open the Atmosphere Console wired to a Built-in-runtime `@AiEndpoint`, send
a prompt, verify the assistant bubble renders. Channel webhooks (Slack /
Telegram / etc.) are registered at boot but driven by separate fixture-based
SKILLs.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by
`SAMPLE.md` must include:

- `LLM_MODE=fake`.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8080/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"runtime":"built-in"` (NOT the more
  common `"demo"`).

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello — one short sentence please."`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text). Body is
   short — Built-in runtime emits a one-token reply like `"Hello there!"`.
8. Screenshot: `chat-stream-channels-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit.

## Skip / obstacles

None when both env vars are set.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible.
- No console errors logged.
- Optional regression check: body does NOT contain `"Demo mode"` — Built-in
  runtime should not surface the demo-mode fallback marker. If it does,
  the sample regressed to the `DemoAgentRuntime` path.
