---
version: 1
name: Agent slash command — /help round-trip
app: spring-boot-dentist-agent
surface: web
tags: ["atmosphere", "agent", "command", "must-pass"]
---

Open the Atmosphere Console, send the `/help` slash command, verify the
auto-generated command list renders in the assistant bubble. Canonical
happy-path for any `@Agent` sample that ships `@Command` handlers.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by `SAMPLE.md`
must include:

- `LLM_MODE=fake` — required for any **natural-language** prompt fallback;
  technically optional for the slash-command path (which bypasses the LLM),
  but the SKILL.md sets it for consistency with the wider must-pass cohort.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when `GET http://127.0.0.1:8080/atmosphere/console/` returns 200
and `GET /api/console/info` reports `"runtime":"demo"`.

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"/help"` (literal forward-slash + word — the command name is
   load-bearing).
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text). The
   content auto-populates from the registered `@Command`s — must contain
   the string `"Available commands"` and at least the names `/firstaid`,
   `/urgency`, `/pain`, `/help`.
8. Screenshot: `chat-help-command-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. The slash-command path bypasses
the LLM so latency is consistent (~30 ms observed); the assistant bubble
appears almost immediately after click.

## Skip / obstacles

None when both env vars are set. The `@Command` short-circuit runs
synchronously inside the `@Agent` dispatcher, so unlike streaming SKILLs
there is no `~2s` streaming delay to absorb.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element with text
  `"/help"`.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible. Its text contains `"Available commands"` plus the
  four registered command names.
- Token metrics line shows `"1 tokens"` (canonical signal that the LLM was
  bypassed — `@Command` short-circuit). Asserting the literal `"1 tokens"`
  is optional but a strong regression signal: if the LLM was wrongly invoked
  the token count would jump into double digits.
- Zero `[data-testid=tool-activity]` panels (slash commands do not invoke
  `@AiTool`s).
- No console errors logged.
