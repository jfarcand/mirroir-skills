---
version: 1
name: AG-UI chat — single-turn demo-mode token stream
app: spring-boot-agui-chat
surface: web
tags: ["atmosphere", "agui", "ai-chat", "streaming", "must-pass"]
---

Open the Atmosphere Console wired to the AG-UI-multiplexed streaming
endpoint, send a prompt, verify the assistant bubble renders. The AG-UI
protocol layer is invisible on the Console surface — covered by a separate
CopilotKit-client SKILL.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by
`SAMPLE.md` must include:

- `LLM_MODE=fake`.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8085/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports subtitle `"AG-UI Protocol Demo —
  streaming assistant with tool calls"`.

Port 8085 (not 8080).

## Steps

1. Open `http://127.0.0.1:8085/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello — one short sentence please."`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text).
8. Screenshot: `chat-stream-agui-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. Streaming completes in ~1–2 s.

## Skip / obstacles

None when both env vars are set.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible.
- No console errors logged.
