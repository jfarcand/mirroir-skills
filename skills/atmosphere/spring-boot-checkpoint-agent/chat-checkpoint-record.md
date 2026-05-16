---
version: 1
name: Checkpoint agent — single-turn dispatch with checkpoint marker
app: spring-boot-checkpoint-agent
surface: web
tags: ["atmosphere", "agent", "checkpoint", "must-pass"]
---

Open the Atmosphere Console wired to the dispatch `@Agent`, send a prompt,
verify the assistant bubble reports that the result has been checkpointed.
The full REST checkpoint→approve flow is covered by a separate SKILL.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by
`SAMPLE.md` must include:

- `LLM_MODE=fake`.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8095/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"endpoint":"/atmosphere/agent/dispatch"`.

Port 8095 (not 8080).

## Steps

1. Open `http://127.0.0.1:8095/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello — one short sentence please."`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text). Body
   contains the substring `"checkpointed"`.
8. Screenshot: `chat-checkpoint-record-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. Streaming completes in ~2 s.

## Skip / obstacles

None when both env vars are set. SQLite checkpoint file persists between
runs in the working directory; clean `atmosphere-checkpoints.db` between
invocations if checkpoint-count assertions are added in future SKILLs.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible. Body contains `"checkpointed"`.
- No console errors logged.
