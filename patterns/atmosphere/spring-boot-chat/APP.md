---
version: 1
app: spring-boot-chat
archetype: broadcast-chat
runtime: spring-boot-4 + atmosphere-runtime
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/chat
console_mode: broadcast
obstacle_mode: auto
---

# spring-boot-chat

Classic Atmosphere broadcast sample — every message a subscriber posts is fanned
out to every other subscriber on the same endpoint. No LLM, no `@AiEndpoint` —
just plain `@ManagedService` + `@Message` over WebSocket / SSE / long-poll. The
bundled Atmosphere Console SPA (`/atmosphere/console/`) drives this in the same
chat UI used by AI samples, but **without** the assistant-bubble half of the flow.

## Boot prerequisites

- JVM: JDK 21
- Command: `./mvnw -q spring-boot:run -pl samples/spring-boot-chat` from the
  Atmosphere repo root.
- Boot wait: ~30–60 s; ready when TCP `:8080` accepts connections AND
  `GET /atmosphere/console/` returns 200.
- Env the SKILL.md must set:
  - `ATMOSPHERE_AUTH_ENABLED=false` — Vue console does not thread an auth token
    (`frontend/src/App.tsx:36`, the `authToken` line is commented out). With the
    default `atmosphere.auth.enabled: true` (Correctness Invariant #6, fail
    closed), the console hangs at "Connecting" and never reaches "Connected".

`LLM_MODE` is **not** read by this sample — no AI module on the classpath. Set
it or skip it, doesn't matter.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Real-time chat with WebTransport/HTTP3 and WebSocket fallback",
  "endpoint": "/atmosphere/chat",
  "runtime": "demo",
  "mode": "broadcast"
}
```

The `mode: broadcast` field is the runtime-truth signal that the SKILL.md must
assert against the user bubble (`.message--user`), **not** the assistant bubble
(`.message--assistant`) — there is no assistant in broadcast mode.

## Structure

Single Vue SPA at `/atmosphere/console/` (root `/` 302-redirects there). Same
shell as `spring-boot-ai-chat`; the chat tab is the only meaningful surface.

### Header (banner)
- "Atmosphere" wordmark image (SVG, branded)
- Heading: "Atmosphere AI Console"
- Subtitle (from `/api/console/info`): "Real-time chat with WebTransport/HTTP3
  and WebSocket fallback"
- Build-version chip

### Navigation tabs
Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP. Only **Chat**
is relevant for this sample — Policies/Decisions/Commitments/OWASP are
governance surfaces with no data in the broadcast sample.

### Chat tab (default — broadcast variant)
- Connection-status pill (`data-testid="status-label"`). Shape:
  `"<state> · <transport>"` — e.g. `"Connected · websocket"`. Prefix-match only.
- Empty state (observed via chrome-devtools-mcp snapshot, 2026-05-15):
  - Heading: `"Start a broadcast"`
  - Sub: `"Type a message below — every subscriber on this endpoint will receive it."`
  This is the runtime-truth distinguisher from the AI variant
  (`"Start a conversation"` / `"Type a message below to begin chatting with the AI assistant."`).
- Chat input: `[data-testid=chat-input]`, `<textarea>`, placeholder
  `"Type a message... (Shift+Enter for newline)"`.
- Send button: `[data-testid=chat-send]`, disabled until input is non-empty.
- Message bubbles: only `[data-testid=message-bubble].message--user` ever
  appears (confirmed in snapshot: uid="U" + body + timestamp pattern like
  `"07:21 PM"`). `.message--assistant` never appears — there is no assistant.
- The user bubble is also broadcast back over the WebSocket so other connected
  clients see the same `message--user` bubble; this app's UX is "you broadcast,
  everyone (including you) sees it as a user post."

## Obstacles

None during normal boot when `ATMOSPHERE_AUTH_ENABLED=false` is set. If the JVM
starts with `ATMOSPHERE_AUTH_ENABLED=true` (the production default per
Correctness Invariant #6), the console pageload returns 401 — Vue app sits in
"Connecting" / flips to "Disconnected" and the SKILL.md times out at the
status-label wait.

## Skip

- "Clear" button — wipes session state mid-flow; never tap during a scenario.
- "Sessions" tab → "Cancel inflight" — no streaming reply to cancel here, but
  also no need to tap it.
- Tabs Policies/Decisions/Commitments/OWASP — empty, no governance hooks wired.
- **Never assert on `.message--assistant`** — broadcast mode never produces one;
  asserting it would hang the SKILL.md until timeout.

## Tips

- After clicking Send the user bubble appears within ~50 ms; no streaming delay
  to wait through (compare with AI samples where the assistant bubble streams
  over ~2 s).
- Transport negotiation is identical to the AI sample: WebSocket primary, SSE /
  long-poll fallback; WebTransport offered when `atmosphere.web-transport.enabled=true`
  and the browser supports it (Chromium only today).
- The user bubble has three child nodes in the snapshot: avatar ("U"), body
  text, timestamp ("HH:MM AM/PM"). Only assert visibility — not the exact body
  text — to keep the SKILL.md transport- and timezone-stable.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index — boot smoke |
| `/atmosphere/chat` | WebSocket | Broadcast endpoint (`@ManagedService`) |
| `/api/console/info` | GET | Returns `{subtitle, endpoint, runtime, mode}` |
| `/api/webtransport-info` | GET | Console queries this on load; `{enabled, port, certificateHash}` |
