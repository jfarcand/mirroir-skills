---
version: 1
name: Quarkus AI chat — single-turn demo-mode token stream
app: quarkus-ai-chat
surface: web
tags: ["atmosphere", "quarkus", "ai-chat", "streaming", "must-pass"]
---

Open the Atmosphere Console wired to the Quarkus AI streaming endpoint, send
one prompt, verify the assistant bubble renders. Canonical happy-path for the
Quarkus port of `spring-boot-ai-chat`; uses `DemoResponseProducer` so no API
key is needed.

## Preconditions

The runner boots the JVM via `boot_once`; the SKILL.md does not respawn it.
The boot env declared by `SAMPLE.md` (or the equivalent harness call) must
include:

- `ATMOSPHERE_AUTH_ENABLED=false` — Vue console does not thread an auth token;
  auth-enabled default returns 401.
- Boot command must include `-Dquarkus.console.enabled=false`.

The boot env declared by `SAMPLE.md` must **leave unset / unexport**:

- `LLM_API_KEY` and `GEMINI_API_KEY` — both must be empty for the
  `quarkus.langchain4j.openai.api-key` property to default to `dummy`, which
  is the `DemoResponseProducer` trigger. If either is set the assistant body
  will come from a real Gemini call and the SKILL.md becomes non-deterministic.

**`LLM_MODE=fake` is not honored** in the Quarkus port — that switch is the
Spring Boot `AiConfig.configure` path; do not waste time setting it.

Boot ready when:
- `GET http://127.0.0.1:18810/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"runtime":"demo"` and `"mode":"ai"`.

The non-standard port **18810** (not 8080) is declared in `application.properties`
to avoid collision with `spring-boot-ai-chat`.

## Steps

1. Open `http://127.0.0.1:18810/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`
   (prefix-match only; full label appends transport, e.g. `"Connected · websocket"`).
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello — one short sentence please."`.
5. Tap `[data-testid=chat-send]`. (Disabled until input is non-empty; do not
   race the click ahead of the keystroke.)
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
   Streaming completes in ~2 s under demo-mode.
7. Verify the assistant bubble renders (visible + non-empty text). The user-
   echo bubble (`[data-testid=message-bubble].message--user`) is also present;
   never assert on the unscoped `[data-testid=message-bubble]` (strict-mode
   would match both).
8. Screenshot: `chat-stream-assistant-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. The Quarkus extension does not
negotiate WebTransport (Undertow lacks HTTP/3), so expect WebSocket primary
with SSE / long-poll fallback. `"Connected"` prefix-match is
transport-agnostic.

## Skip / obstacles

None when `ATMOSPHERE_AUTH_ENABLED=false`, `-Dquarkus.console.enabled=false`,
and both api-key env vars are unset. If a real key is configured, the SKILL.md
still passes (assistant bubble renders) but content varies — do not assert on
specific copy.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element matches.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible.
- No console errors logged (use the platform's console-error capture hook).
