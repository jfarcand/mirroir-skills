---
version: 1
name: Guarded email agent — single-turn demo-mode reply
app: spring-boot-guarded-email-agent
surface: web
tags: ["atmosphere", "agent", "verifier", "must-pass"]
---

Open the Atmosphere Console wired to the verifier-guarded `@Agent`, send a
prompt, verify the assistant bubble renders. Under `LLM_MODE=fake` the
verifier plane is silent — exercise it with the REST surface or a real-LLM
SKILL (separate scenario).

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by
`SAMPLE.md` must include:

- `LLM_MODE=fake`.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8080/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"runtime":"demo"` with `"mode":"ai"`.

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello — one short sentence please."`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text).
8. Screenshot: `chat-stream-guarded-email-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit.

## Skip / obstacles

None when both env vars are set. The verifier plane never fires in
LLM_MODE=fake (the stub LLM doesn't emit a `send_email` tool call); a
verifier-active SKILL needs a real `LLM_API_KEY`.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible.
- No console errors logged.
