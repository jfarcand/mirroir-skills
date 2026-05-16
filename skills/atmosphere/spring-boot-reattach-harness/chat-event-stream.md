---
version: 1
name: Reattach harness — deterministic event sequence
app: spring-boot-reattach-harness
surface: web
tags: ["atmosphere", "reattach", "harness", "must-pass"]
---

Open the Atmosphere Console wired to the reattach test harness, send a
prompt, verify the assistant bubble contains the deterministic event
sequence `event-0…event-4`. Reattach resume SKILL is a separate scenario.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by
`SAMPLE.md` must include:

- `LLM_MODE=fake`.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8096/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"endpoint":"/atmosphere/agent/harness"`.

Port 8096 (not 8080).

## Steps

1. Open `http://127.0.0.1:8096/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello — one short sentence please."` (any non-empty prompt
   produces the same event sequence).
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible
   (allow ~3 s — harness throttles ~500 ms per event).
7. Verify the assistant bubble renders (visible + non-empty text). Body
   contains the substring `"event-0"` (the first deterministic event).
   Asserting only `"event-0"` is robust — the bubble may still be
   streaming and not yet contain all 5 events.
8. Screenshot: `chat-event-stream-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. Latency is ~2.5 s consistently
(harness uses fixed sleeps between sends).

## Skip / obstacles

None when both env vars are set. The reattach resume SKILL requires a
disconnect-aware client and is out of scope here.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible. Body contains `"event-0"`.
- Token metrics show `"6 tokens"` — deterministic count (5 events + 1
  completion).
- No console errors logged.
