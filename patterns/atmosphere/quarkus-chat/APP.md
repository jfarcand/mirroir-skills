---
version: 1
app: quarkus-chat
archetype: broadcast-chat
runtime: quarkus-3.35 + atmosphere-quarkus-extension
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/chat
console_mode: broadcast
obstacle_mode: auto
---

# quarkus-chat

Quarkus port of `spring-boot-chat` — same `@ManagedService` `Chat` handler, same
broadcast semantics (every post is fanned out to every subscriber), running on
Quarkus 3.35 + the Atmosphere Quarkus extension instead of Spring Boot 4. No
LLM, no `@AiEndpoint`. The Atmosphere Console SPA (`/atmosphere/console/`) ships
with the Quarkus extension and is reachable identically.

## Boot prerequisites

- JVM: JDK 21
- Command:
  `./mvnw -q quarkus:dev -pl samples/quarkus-chat -Dquarkus.console.enabled=false -Dquarkus.http.port=8080`
  from the Atmosphere repo root. The `-Dquarkus.console.enabled=false` flag
  suppresses Quarkus's TUI banner so the harness can scrape stdout cleanly.
- Boot wait: ~5–10 s on a warm JVM (much faster than spring-boot:run — Quarkus
  dev mode JIT). Ready when TCP `:8080` accepts connections AND
  `GET /atmosphere/console/` returns 200 AND `GET /api/console/info` reports
  `"mode":"broadcast"`.
- Env the SKILL.md must set:
  - `ATMOSPHERE_AUTH_ENABLED=false` — same as the Spring Boot variant; Vue
    console does not thread an auth token (`frontend/src/App.tsx:36`).

`LLM_MODE` is not read — no AI module on the classpath.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Multi-client broadcast chat",
  "endpoint": "/atmosphere/chat",
  "runtime": "demo",
  "mode": "broadcast"
}
```

`runtime: demo` and `mode: broadcast` are identical to `spring-boot-chat`; the
subtitle string differs (`"Multi-client broadcast chat"` vs Spring Boot's
`"Real-time chat with WebTransport/HTTP3 and WebSocket fallback"`).

## Structure

Two web surfaces, only **one** of which the SKILL.md should drive:

| Path | Purpose |
|---|---|
| `/atmosphere/console/` | **Atmosphere Console SPA** (Vue.js, bundled with the Atmosphere Quarkus extension — Quarkus parity landed in 4.0.43). Drive the SKILL.md here. |
| `/` | Sample's **bespoke** UI (`<title>Atmosphere 4.0 Chat</title>`, custom Vite build at `/assets/index-*.js`). Pretty, but per `feedback_console_for_samples.md` skill authoring goes through the Console — not the custom UI. |
| `/admin/` | Atmosphere admin dashboard. Operational surface, not driven by SKILL.md. |

### Header (banner — Atmosphere Console)
- "Atmosphere" wordmark image (inline SVG)
- Heading: "Atmosphere AI Console" — yes, the heading says "AI" even on the
  non-AI samples; the Console SPA brand is fixed regardless of `runtime`.
- Subtitle: `"Multi-client broadcast chat"` (from `/api/console/info`)
- Build-version chip: `"v4"`

### Navigation tabs — Quarkus build observed via chrome-devtools-mcp snapshot 2026-05-15

Chat / Policies (0) / Decisions / Commitments / OWASP — **five tabs**.
Notably **no "Sessions" tab** that the Spring Boot console exposes; the Quarkus
extension's Console build does not surface the session-management view.
Match by `button` role + text; do not assume positional indexing across builds.

### Chat tab (default)
- Connection-status pill: `data-testid="status-label"`. Shape:
  `"<state> · <transport>"` — observed value: `"Connected"` (prefix only, the
  transport appendix may or may not render depending on negotiation timing).
- Empty state (observed via snapshot, **drift from spring-boot-chat**):
  - Heading: `"Start a conversation"` (NOT `"Start a broadcast"`)
  - Sub: `"Type a message below to begin chatting with the AI assistant."`
  The Quarkus Console build still uses the AI-archetype empty-state copy even
  though `mode:broadcast`. Capture this in the SKILL.md as a known drift —
  **don't assert against the empty-state text**, only against the post-send
  bubble. (Fix-forward target: pivot empty-state by `mode` in the Quarkus
  Console build the same way Spring Boot did.)
- Chat input: `[data-testid=chat-input]`, `<textarea>`, placeholder
  `"Type a message... (Shift+Enter for newline)"`.
- Send button: `[data-testid=chat-send]`, disabled until input is non-empty.
- After send: only `[data-testid=message-bubble].message--user` appears
  (avatar "U" + body + timestamp `"07:26 PM"` observed in snapshot). The input
  clears and the send button returns to disabled.
- **`.message--assistant` never appears** — broadcast mode, no LLM.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` (production default) → console returns 401,
  Vue app sits at "Connecting" / flips to "Disconnected".
- Quarkus's TUI live-reload banner steals stdin/stdout in interactive terminals.
  Always pass `-Dquarkus.console.enabled=false` when scripting the boot.
- Quarkus dev-mode hot-reload picks up `.java` edits — do not edit handler
  files while a SKILL.md is running, the JVM will rebuild mid-flow.

## Skip

- "Clear" button — wipes session state mid-flow; never tap during a scenario.
- Tabs Policies/Decisions/Commitments/OWASP — empty, no governance hooks wired.
- The bespoke UI at `/` — not the canonical surface; do not drive SKILL.md here.
- Native-image (`-Pnative`) build — out of scope for the must-pass replay set;
  test it in a separate dedicated SKILL once a native-image lane exists.

## Tips

- Boot is fast (~5 s) but `/atmosphere/console/` may briefly return 200 before
  the WebSocket endpoint is wired (`UT026005` log lines). Poll on the
  `Connected` status-label, not just the HTTP 200.
- The 5-tab vs 6-tab nav delta is the most surface-visible difference from
  Spring Boot. If a future Quarkus extension build adds Sessions, the SKILL.md
  doesn't need to change — it only locates Chat by text — but tooling that
  enumerates tabs by index will break.
- Empty-state copy drift may be fixed in a future extension release; the
  SKILL.md should remain robust to either copy by asserting only on the user
  bubble.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index (extension-shipped) |
| `/` | GET | Sample's bespoke chat UI |
| `/admin/` | GET | Admin dashboard |
| `/atmosphere/chat` | WebSocket | Broadcast endpoint (`@ManagedService`) |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/webtransport-info` | GET | `{enabled, port, certificateHash}` (the Quarkus extension may report `enabled:false` — no Netty WT support in Undertow) |
