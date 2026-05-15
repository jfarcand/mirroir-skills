---
version: 1
name: AI chat — single-turn tool-call with activity panel
app: spring-boot-ai-tools
surface: web
tags: ["atmosphere", "ai-chat", "tool-calling", "streaming", "must-pass"]
---

Open the Atmosphere Console wired to a tool-bearing `@AiEndpoint`, send a
prompt that triggers a registered `@AiTool`, verify both the assistant bubble
and the tool-activity panel render. Canonical happy-path for any sample that
declares `@AiTool` methods.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by `SAMPLE.md`
must include:

- `LLM_MODE=fake` — routes through `FakeLlmClient`, which simulates tool calls
  deterministically (legal values: `remote`, `local`, `fake`; do **not** use
  `demo`).
- `ATMOSPHERE_AUTH_ENABLED=false` — Vue console does not thread an auth token.

The non-standard port **8090** (set in `application.yml`) is intentional so
the sample can run alongside `spring-boot-ai-chat` on 8080.

Boot ready when `GET http://127.0.0.1:8090/atmosphere/console/` returns 200
and `GET /api/console/info` reports `"runtime":"demo"` with subtitle
`"AI chat with tool calling visualization"`.

## Steps

1. Open `http://127.0.0.1:8090/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"What time is it in Tokyo?"` (routes to `get_city_time`; any of the
   four prompt exemplars in APP.md works, this one is the cheapest).
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify both surfaces render:
   - `[data-testid=message-bubble].message--assistant` is visible
     (non-empty text).
   - `[data-testid=tool-activity]` is visible (the "AGENT COLLABORATION"
     panel with the tool entry the prompt triggered).
8. Screenshot: `chat-tool-call-rendered`.

## Cross-browser

The same flow runs on chromium + firefox + webkit. WebTransport may be
offered on chromium when the cert handshake succeeds; the `"Connected"`
prefix-match is transport-agnostic.

## Skip / obstacles

None when `LLM_MODE=fake` and `ATMOSPHERE_AUTH_ENABLED=false` are set. If
either is missing the SKILL.md times out at the status-label wait or assistant
bubble wait.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element matches.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible.
- Exactly one `[data-testid=tool-activity]` panel matches and is visible —
  the differentiator vs `spring-boot-ai-chat`. A passing assistant-bubble
  assertion without a tool-activity panel would indicate the `@AiTool`
  routing regressed.
- No console errors logged.
