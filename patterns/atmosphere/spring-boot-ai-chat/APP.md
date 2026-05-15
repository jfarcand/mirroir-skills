---
version: 1
app: spring-boot-ai-chat
archetype: chat-streaming
runtime: spring-boot-4 + atmosphere-ai
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
obstacle_mode: auto
---

# spring-boot-ai-chat

Atmosphere AI Chat sample — streams LLM responses token-by-token through Atmosphere's
`@AiEndpoint` into the bundled Atmosphere AI Console (Vue.js SPA shipped in
`atmosphere-spring-boot-starter`). The same Console UI is used by every Spring Boot
sample that exposes a chat-style endpoint; selectors below are stable across them.

## Boot prerequisites

- JVM: JDK 21
- Command: `./mvnw -q spring-boot:run -pl samples/spring-boot-ai-chat` from the
  Atmosphere repo root.
- Boot wait: ~30–90 s; ready when TCP `:8080` accepts connections AND
  `GET /atmosphere/console/` returns 200.
- Env that the SKILL.md must set:
  - `LLM_MODE=fake` — routes through `FakeLlmClient`
    (`modules/ai/src/main/java/org/atmosphere/ai/AiConfig.java:153`); deterministic
    simulated streaming, zero API keys required. Supported modes are
    `remote` / `local` / `fake`. **Do not** use `demo` — that string is not in
    `AiConfig.configure`'s switch and falls through to `remote` with no key.
  - `ATMOSPHERE_AUTH_ENABLED=false` — the Vue console does **not** thread an auth
    token (line 36 of `frontend/src/App.tsx` has `authToken: 'demo-token'` commented
    out for the WebTransport demo), so the auth-enabled default returns 401 on the
    console pageload. Sample's `application.yml` ships `atmosphere.auth.enabled: true`
    fail-closed per Correctness Invariant #6; the override is for replay only.

## Structure

Single Vue SPA at `/atmosphere/console/` (root `/` 302-redirects there). One header,
six navigation tabs, one main pane that swaps per tab.

### Header (banner)
- "Atmosphere" wordmark image (SVG, branded)
- Heading: "Atmosphere AI Console"
- Subtitle (from `application.yml` → `atmosphere.console-subtitle`):
  "Real-time AI chat with Gemini, OpenAI, or Ollama — WebTransport/HTTP3"
- Build-version chip e.g. "v4"

### Navigation tabs
1. **Chat** — default tab on load. The chat UI lives here.
2. **Sessions** — list of active Atmosphere sessions (cancel-inflight etc.).
3. **Policies** — governance policies (count badge if any).
4. **Decisions** — governance decisions log.
5. **Commitments** — governance commitments.
6. **OWASP** — OWASP detector findings.

### Chat tab (default)
- Connection-status pill (top of main): `data-testid="status-label"`.
  Text shape: `"<state> · <transport>"` — e.g. `"Connected · websocket"`,
  `"Connecting · websocket"`, `"Reconnecting · websocket"`, `"Disconnected"`.
  Match the prefix only — transport segment may vary
  (`websocket` / `webtransport` / `sse` / `long-polling`).
- "Clear" button to wipe the message list (`data-testid` not set on the button;
  text-locator works: `button:has-text('Clear')`).
- Welcome panel before any message: "Start a conversation" + "Type a message
  below to begin chatting with the AI assistant."
- Chat input: `[data-testid=chat-input]`, multiline `<textarea>`, placeholder
  `"Type a message... (Shift+Enter for newline)"`.
- Send button: `[data-testid=chat-send]`, disabled until input is non-empty.
- Keyboard hint: "Press Enter to send, Shift+Enter for a new line."
- Message bubbles (`data-testid="message-bubble"`) appear in order: user, assistant.
  Class `.message--user` vs `.message--assistant` disambiguates strict-mode locators.
  Verified shipped in `/atmosphere/console/assets/index-*.js` (live grep, this
  session) — strings `chat-input`, `chat-send`, `message-bubble`, `status-label`,
  `tool-activity`, `console-tabs`, `approval-prompt`, plus CSS classes
  `message--user` and `message--assistant`. Bodies render markdown.
- Optional tool-activity panel (`data-testid="tool-activity"`) shows tool calls
  ahead of the assistant bubble for `@AiTool`-bearing endpoints. Empty on this
  sample (no tools wired) but present in `spring-boot-ai-tools`.

## Obstacles

None during normal boot when both env overrides are set. If the JVM starts with
`ATMOSPHERE_AUTH_ENABLED=true` (default), the console pageload returns 401 — the
Vue app shows a "Disconnected" status and never wires the WebSocket.

## Skip

- "Clear" button — wipes session state mid-flow; never tap during a scenario.
- "Sessions" tab "Cancel inflight" — aborts the streaming reply; only tap when
  explicitly asserting cancel behavior.
- Tabs Policies/Decisions/Commitments/OWASP — exist for governance samples,
  empty here.

## Tips

- `Send` button is disabled until input is non-empty. Type the prompt first,
  then click — do not race the click ahead of the keystroke.
- After send, **two** bubbles appear (user echo + streaming assistant). A strict
  locator on `[data-testid=message-bubble]` will trip Playwright strict-mode;
  always scope: `[data-testid=message-bubble].message--user` or `.message--assistant`.
- Assistant streaming under `LLM_MODE=fake` completes within ~2 s on a warm JVM.
- The Vue app handles transport fallback automatically: WebSocket primary,
  SSE / long-poll fallback when the browser blocks WebSocket. WebTransport (HTTP/3)
  is offered when `atmosphere.web-transport.enabled=true` and the browser supports
  it; today only Chromium has reliable WT support, so Firefox + WebKit projects
  always degrade gracefully.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index — boot smoke |
| `/atmosphere/ai-chat` | WebSocket | Streaming AI endpoint (`@AiEndpoint(path)`) |
| `/api/webtransport-info` | GET | Console queries this on load; returns `{enabled, port, certificateHash}` |
| `/atmosphere/ai-chat-with-cache` | WebSocket | `PromptCacheDemoChat` — cache-hint demo |
| `/atmosphere/ai-chat-with-retry` | WebSocket | `RetryDemoChat` — retry-policy demo |
| `/atmosphere/ai-chat-multimodal` | WebSocket | `MultiModalChat` — image + text |
| `/multimodal.html` | GET | Standalone picker page (not in console) |
