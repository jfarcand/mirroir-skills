---
version: 1
app: spring-boot-rag-chat
archetype: rag-agent
runtime: spring-boot-4 + atmosphere-ai + spring-ai-vector-store
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/agent/rag-assistant
console_mode: ai
obstacle_mode: auto
---

# spring-boot-rag-chat

RAG-powered `@Agent` over the bundled Atmosphere documentation. Combines four
surfaces in one sample:
1. `@Agent` persona-driven dispatch.
2. `@Command` slash commands (`/sources`, `/help`) that bypass the LLM.
3. `@AiTool` methods (`search_knowledge_base`, `list_sources`,
   `get_document_excerpt`) the LLM can invoke for multi-hop retrieval.
4. Automatic Spring AI `VectorStore` augmentation — `RagChunker` chunks each
   Markdown source, embedds it, and the framework injects retrieved context
   before every `@Prompt` call.

The console endpoint reports `/atmosphere/agent/rag-assistant` (under the
`/atmosphere/agent/...` namespace, not the `/atmosphere/ai-chat` default) —
this is the runtime-truth signal that the endpoint is `@Agent`-routed.

## Boot prerequisites

- JVM: JDK 21
- Default port: 8080 (`server.port` in `application.yml`).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-rag-chat` from the
  Atmosphere repo root.
- Boot wait: ~2–6 s (observed start at 1.74 s). Vector-store ingestion of the
  5 Markdown docs happens during boot — `Started RagChatApplication` fires
  after ingestion completes.
- Env the SKILL.md must set:
  - `LLM_MODE=fake` — for LLM-fallback prompts (slash commands bypass).
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "RAG-powered AI chat with document retrieval",
  "endpoint": "/atmosphere/agent/rag-assistant",
  "runtime": "demo",
  "mode": "ai"
}
```

Subtitle matches `atmosphere.console-subtitle` in `application.yml`. The
endpoint string is unique to this sample (no other sample registers
`/atmosphere/agent/rag-assistant`).

## Structure

### Header / Navigation
- Heading: "Atmosphere AI Console"
- Subtitle: `"RAG-powered AI chat with document retrieval"`
- Build-version chip: `"v4"`
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab — `/sources` flow observed via chrome-devtools-mcp 2026-05-15

Send `/sources`:
- User bubble: `[data-testid=message-bubble].message--user` — "U" / "/sources".
- Assistant bubble: `[data-testid=message-bubble].message--assistant` —
  ```
  Knowledge Base (5 documents):
  docs/atmosphere-overview.md (195 words)
  docs/atmosphere-transports.md (398 words)
  docs/atmosphere-ai-module.md (339 words)
  docs/atmosphere-getting-started.md (185 words)
  docs/atmosphere-agents.md (394 words)
  Ask me anything about these documents, or use /help for more commands.
  ```
  Token metrics: `"1 tokens · 23ms · 43.5 tok/s"` — bypass signal (slash
  command short-circuit, no LLM call).

### Natural-language prompt flow (out of must-pass scope)

A natural prompt like `"What transports does Atmosphere support?"` would:
1. Retrieve relevant chunks from the VectorStore (automatic, opaque to UI).
2. Pass the prompt + retrieved context to the LLM.
3. The LLM may emit tool calls (`search_knowledge_base`, etc.), which render
   in the `[data-testid=tool-activity]` panel.
4. The assistant bubble streams the final answer with inline citations.

This path is identical to `spring-boot-ai-tools` plus the implicit
context-injection step — covered by that sample's must-pass SKILL.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- Vector-store ingestion is in-memory (Spring AI's `SimpleVectorStore`); a
  cold boot re-ingests every time. Adding more `.md` files to the
  `src/main/resources/docs/` classpath path extends boot.
- Embedding API is also stubbed under `LLM_MODE=fake` — no external embeddings
  network call. With a real `LLM_API_KEY` the embed step would hit the
  provider.

## Skip

- "Clear" button.
- Sessions/Policies/Decisions/Commitments/OWASP tabs — empty here.
- Multi-hop RAG SKILL — covered by `spring-boot-ai-tools` pattern.

## Tips

- `/sources` is the cheapest must-pass surface: it bypasses both LLM and
  vector-store retrieval (only enumerates the ingested document set). The
  "5 documents" count is the runtime-truth signal that ingestion succeeded.
- The endpoint string `/atmosphere/agent/rag-assistant` is unique to this
  sample — assert on it in `console-info` to disambiguate from any other
  `@Agent` sample.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/agent/rag-assistant` | WebSocket | RAG `@Agent` endpoint |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/commands` | GET | Lists registered `@Command`s |
| `/api/tools` | GET | Lists registered `@AiTool`s |
| `/api/rag/sources` | GET | Lists ingested vector-store documents |
