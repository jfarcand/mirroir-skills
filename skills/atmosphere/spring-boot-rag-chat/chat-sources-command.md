---
version: 1
name: RAG agent — /sources lists ingested documents
app: spring-boot-rag-chat
surface: web
tags: ["atmosphere", "agent", "command", "rag", "must-pass"]
---

Open the Atmosphere Console, send `/sources`, verify the assistant bubble
enumerates the ingested knowledge-base documents. Canonical happy-path for
the RAG `@Agent` sample; uses the slash-command short-circuit so it does not
depend on the LLM.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by `SAMPLE.md`
must include:

- `LLM_MODE=fake` — for any LLM-fallback prompt (`/sources` itself bypasses
  the LLM and would work without it, but keep it set for consistency).
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8080/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports
  `"endpoint":"/atmosphere/agent/rag-assistant"` with
  `"subtitle":"RAG-powered AI chat with document retrieval"`. The endpoint
  string is unique to this sample.

Vector-store ingestion happens during boot — the `Started RagChatApplication`
log line fires after the 5 doc Markdown files are embedded into Spring AI's
`SimpleVectorStore`. Do not start the SKILL before that line.

## Steps

1. Open `http://127.0.0.1:8080/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"/sources"`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the assistant bubble renders (visible + non-empty text). Content
   contains `"Knowledge Base"` plus at least one `docs/...md` filename.
8. Screenshot: `chat-sources-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. Slash-command path bypasses the
LLM so latency is consistent (~25 ms observed).

## Skip / obstacles

None when both env vars are set. Cold-boot vector-store ingestion is the only
slow step (~1–2 s for 5 docs); the runner already waits for boot ready, so
the SKILL.md sees a warm system.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element with text
  `"/sources"`.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible. Body contains `"Knowledge Base"` plus the literal
  `docs/` prefix for at least one ingested document.
- Token metrics show `"1 tokens"` — the runtime-truth bypass signal. A
  higher count would mean the LLM was wrongly invoked.
- Zero `[data-testid=tool-activity]` panels (slash command, no tool calls).
- No console errors.
