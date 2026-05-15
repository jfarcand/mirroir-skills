---
version: 1
app: quarkus-ai-chat
archetype: chat-streaming
runtime: quarkus-3.35 + atmosphere-quarkus-langchain4j
surface: web
url_root: http://127.0.0.1:18810/atmosphere/console/
console_endpoint: /atmosphere/ai-chat
console_mode: ai
obstacle_mode: auto
---

# quarkus-ai-chat

Quarkus AI streaming chat — exposes an `@AiEndpoint` over WebSocket and streams
LLM tokens through `atmosphere-quarkus-langchain4j` → Quarkus LangChain4j → an
OpenAI-compatible provider (Gemini's compat endpoint by default; works with any
provider Quarkus LangChain4j supports). Five total `@AiEndpoint`s ship in this
sample but only the basic `/atmosphere/ai-chat` is the must-pass surface.

## Boot prerequisites

- JVM: JDK 21
- Default port: **18810** (intentionally not 8080 so quarkus-ai-chat can run
  side-by-side with `spring-boot-ai-chat`; declared in `application.properties`).
- Command:
  `./mvnw -q quarkus:dev -pl samples/quarkus-ai-chat -Dquarkus.console.enabled=false`
  from the Atmosphere repo root.
- Boot wait: ~4–8 s on a warm JVM. Ready when TCP `:18810` accepts connections
  AND `GET /atmosphere/console/` returns 200 AND `GET /api/console/info`
  reports `"runtime":"demo"`.
- Env the SKILL.md must set:
  - `ATMOSPHERE_AUTH_ENABLED=false` — same as the Spring Boot AI sample; Vue
    console does not thread an auth token.
- Env the SKILL.md must **un-set** (or leave unset) for demo-mode:
  - `LLM_API_KEY` — must be empty for `DemoResponseProducer` to take over.
    If set to a real key the sample makes a real Gemini API call and the
    SKILL.md becomes non-deterministic (variable latency, rate-limit
    sensitive, costs real money).
  - `GEMINI_API_KEY` — same trigger; both keys default the
    `quarkus.langchain4j.openai.api-key` property to `dummy` when unset.

**Note**: `LLM_MODE=fake` is **not honored** here — that switch lives in
`org.atmosphere.ai.AiConfig.configure` which is the Spring-Boot wiring path.
The Quarkus port uses `DemoResponseProducer` gated on the api-key being
`dummy` instead.

## Console-info advertisement

`GET /api/console/info` returns (with no API key set):

```json
{
  "subtitle": "Runtime: demo",
  "endpoint": "/atmosphere/ai-chat",
  "runtime": "demo",
  "mode": "ai"
}
```

`runtime: demo` is the runtime-truth signal that `DemoResponseProducer` is
active. `mode: ai` means the SKILL.md must assert against the assistant bubble.

## Structure

Atmosphere Console SPA at `/atmosphere/console/` is the canonical surface
(Quarkus extension parity per 4.0.43). The sample's bespoke
`META-INF/resources/index.html` is a meta-redirect to the same Console — so
opening `/` also lands you there.

### Header (banner)
- Heading: "Atmosphere AI Console"
- Subtitle: `"Runtime: demo"` (observed via chrome-devtools-mcp snapshot
  2026-05-15 with no `LLM_API_KEY`).
- Build-version chip: `"v4"`

### Navigation tabs

Chat / Policies (0) / Decisions / Commitments / OWASP — same **five tabs** as
`quarkus-chat`; no "Sessions" tab. (Locate Chat by text, not by index.)

### Chat tab (default)
- Connection-status pill: `data-testid="status-label"`. Shape:
  `"<state> · <transport>"` — observed value: `"Connected"`.
- Empty state:
  - Heading: `"Start a conversation"`
  - Sub: `"Type a message below to begin chatting with the AI assistant."`
  Same copy as `quarkus-chat` (Quarkus Console build doesn't pivot by mode);
  here it actually matches the archetype.
- Chat input: `[data-testid=chat-input]`, `<textarea>`, placeholder
  `"Type a message... (Shift+Enter for newline)"`.
- Send button: `[data-testid=chat-send]`, disabled until input is non-empty.
- After send (demo-mode body observed via snapshot):
  - User bubble: `[data-testid=message-bubble].message--user` — avatar "U" +
    prompt text + timestamp.
  - Assistant bubble: `[data-testid=message-bubble].message--assistant` —
    streams word-by-word; content shape is:
    `"You said: \"<prompt>\""` then `"Demo mode — this response is a canned
    placeholder because no LLM_API_KEY is configured. Export a Gemini, OpenAI,
    or Ollama key (see the sample README) and restart to get a real AI reply."`
    plus timestamp.
  - Stream completes in ~2 s (50 ms per word via `Thread.sleep(50)` in
    `DemoResponseProducer.stream`).

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` (production default) → 401 on the console.
- Quarkus TUI hot-reload banner — pass `-Dquarkus.console.enabled=false`.
- If an `LLM_API_KEY` is present in the environment the sample makes a real
  Gemini API call — assistant content will vary, no `"Demo mode"` marker, and
  rate limits may cause flakes. SKILL.md must assert structure (presence of
  `.message--assistant`), **not** specific copy.
- The Quarkus L4j extension auto-publishes a `StreamingChatModel` bean even
  when api-key is `dummy`; the demo-mode branch fires inside the `@Prompt`
  body before any LangChain4j call is made, so network calls only happen when
  a real key is set.

## Skip

- "Clear" button — wipes session state mid-flow; never tap during a scenario.
- Tabs Policies/Decisions/Commitments/OWASP — empty.
- The four secondary `@AiEndpoint`s (`/atmosphere/ai-chat-with-cache`,
  `/atmosphere/ai-chat-with-retry`, `/atmosphere/ai-chat-multimodal`,
  `/atmosphere/review-extractor`) — out of scope for this must-pass SKILL; the
  basic `/atmosphere/ai-chat` is enough to prove the streaming path is wired.
- Native-image build (`-Pnative`) — separate lane.

## Tips

- Assistant streaming under demo mode takes ~2 s; wait on the assistant bubble
  rather than a specific terminal token, so the SKILL.md works under both demo
  and real-key boots.
- The Quarkus L4j `log-requests=true` flag dumps the full HTTP request body to
  the JVM log — useful for upstream debugging but **does not** trigger a real
  network call in demo mode (the request would be built only on the
  real-LLM path).
- `runtime: demo` in `/api/console/info` is the cheapest precondition check;
  use it instead of pattern-matching on assistant copy.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/` | GET | Meta-redirects to `/atmosphere/console/` |
| `/atmosphere/ai-chat` | WebSocket | Basic streaming AI endpoint |
| `/atmosphere/ai-chat-with-cache` | WebSocket | Prompt-cache demo |
| `/atmosphere/ai-chat-with-retry` | WebSocket | Retry-policy demo |
| `/atmosphere/ai-chat-multimodal` | WebSocket | Multi-modal (image + text) |
| `/atmosphere/review-extractor` | WebSocket | Structured-output demo |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/admin/` | GET | Admin dashboard (read-only by default) |
