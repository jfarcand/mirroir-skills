---
version: 1
name: AI chat — single-turn token stream
app: spring-boot-ai-chat
surface: web
tags: ["atmosphere", "ai-chat", "streaming", "must-pass"]
---

Open the Atmosphere AI Console, send one prompt, verify a streamed assistant reply
renders. The canonical happy-path for any `@AiEndpoint`-bearing Spring Boot sample
that exposes the bundled Console.

## Preconditions

The runner boots the JVM via `boot_once`; the SKILL.md does not respawn it. The
boot env declared by `SAMPLE.md` (or the equivalent harness call) must include:

- `LLM_MODE=fake` — routes through `FakeLlmClient` (`AiConfig.configure` line 153,
  module `modules/ai`). Deterministic simulated streaming, no API keys. Other
  legal values are `remote` and `local`; do not use `demo` (not in the switch).
- `ATMOSPHERE_AUTH_ENABLED=false` — Vue console does not thread an auth token in
  `frontend/src/App.tsx:36` (commented out for WebTransport demo). Auth-enabled
  default returns 401 on `/atmosphere/console/`.

Boot ready when `GET http://127.0.0.1:8080/atmosphere/console/` returns 200.

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`
   (the full label appends transport, e.g. `"Connected · websocket"`).
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello — one short sentence please."`.
5. Tap `[data-testid=chat-send]`. (Button is disabled until input is non-empty;
   do not race the click ahead of the keystroke.)
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text). The user-
   echo bubble (`[data-testid=message-bubble].message--user`) is also present —
   never assert on the unscoped `[data-testid=message-bubble]` (strict-mode
   would match both).
8. Screenshot: `chat-stream-assistant-rendered`.

## Cross-browser

The same flow runs on chromium + firefox + webkit. atmosphere.js negotiates
transport per browser: chromium prefers WebTransport over HTTP/3 (when
`atmosphere.web-transport.enabled=true` and a cert hash is offered), falling
back to WebSocket; firefox + webkit go WebSocket primary, SSE / long-poll
fallback if WebSocket is blocked. The `[data-testid=status-label]` "Connected"
prefix-match is transport-agnostic.

## Skip / obstacles

None when the env above is set. If `ATMOSPHERE_AUTH_ENABLED=true` (the default),
the connection never reaches "Connected" — status hangs at "Connecting" or
flips to "Disconnected"; the SKILL.md times out at step 2.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element matches.
- At least one `[data-testid=message-bubble].message--assistant` element matches
  and is visible.
- No console errors logged (use the platform's console-error capture hook).
