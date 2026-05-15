---
version: 1
name: Classroom AI — single-client streaming reply
app: spring-boot-ai-classroom
surface: web
tags: ["atmosphere", "ai-chat", "streaming", "multi-room", "must-pass"]
---

Open the Atmosphere Console wired to the `/atmosphere/classroom/{room}`
streaming endpoint, send one prompt, verify the assistant bubble renders.
Single-client variant of the multi-room broadcast sample. The room-broadcast
dimension is not exercised here (would need two clients).

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by `SAMPLE.md`
must include:

- `LLM_MODE=fake` — `FakeLlmClient` deterministic streaming.
- `ATMOSPHERE_AUTH_ENABLED=false` — Vue console does not thread an auth token.

Boot ready when `GET http://127.0.0.1:8080/atmosphere/console/` returns 200
and `GET /api/console/info` reports `"endpoint":"/atmosphere/classroom/{room}"`
with `"runtime":"demo"`.

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello classroom — one short sentence please."`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text). Do not
   assert on `[data-testid=tool-activity]` — this endpoint has no `@AiTool`s.
8. Screenshot: `chat-stream-classroom-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. `"Connected"` prefix-match is
transport-agnostic.

## Skip / obstacles

None when both env vars are set. Multi-room broadcast SKILL (two clients in
the same room, both see the same stream) is out of scope here — a separate
SKILL.md should cover that.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element matches.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible.
- Zero `[data-testid=tool-activity]` panels (this endpoint has no tools).
- No console errors logged.
