---
version: 1
app: spring-boot-durable-sessions
archetype: broadcast-chat-with-durable-sessions
runtime: spring-boot-4 + atmosphere-runtime + atmosphere-durable-sessions-sqlite
surface: web
url_root: http://127.0.0.1:8080/atmosphere/console/
console_endpoint: /atmosphere/chat
console_mode: broadcast
obstacle_mode: auto
---

# spring-boot-durable-sessions

Plain broadcast chat (`@ManagedService` on `/atmosphere/chat`) wired with the
**durable-sessions SQLite store**. Every WebSocket session is persisted; a
client that disconnects and reconnects with the same session id can resume
without losing buffered broadcasts. From the Console-surface SKILL.md
perspective the chat behaves identically to `spring-boot-chat` — durability
shows up in REST/admin surfaces or on a forced disconnect+reconnect.

## Boot prerequisites

- JVM: JDK 21
- Default port: 8080.
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-durable-sessions`.
- Boot wait: ~1–4 s (observed start at 1.64 s). SQLite store
  (`atmosphere-durable-sessions.db` or similar) is created in the working
  directory on first run.
- Env the SKILL.md must set:
  - `ATMOSPHERE_AUTH_ENABLED=false`.
- `LLM_MODE` is not read.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Multi-client broadcast chat",
  "endpoint": "/atmosphere/chat",
  "runtime": "unknown",
  "mode": "broadcast"
}
```

`runtime: unknown` is a runtime-truth oddity — this sample doesn't ship an
`AgentRuntime` (no AI module on the must-pass path), so the advertised
runtime is `unknown`. Use that as the distinguishing signal.

## Structure

### Header / Navigation
- Subtitle: `"Multi-client broadcast chat"` (same as `quarkus-chat` /
  `spring-boot-otel-chat`).
- Six tabs: Chat / Sessions / Policies (0) / Decisions / Commitments / OWASP.

### Chat tab (broadcast variant — observed via chrome-devtools-mcp 2026-05-16)

- Status: `"Connected · websocket"`.
- Empty state:
  - Heading: `"Start a broadcast"`
  - Sub: `"Type a message below — every subscriber on this endpoint will receive it."`
- After send: only `[data-testid=message-bubble].message--user` appears
  (avatar "U" + body + timestamp).
- `.message--assistant` never appears — broadcast mode.

### Durable session surface (out of must-pass scope)

- Sessions persist in the SQLite store across JVM restarts.
- A reconnect SKILL would: send message, kill the JVM, reboot, reconnect
  with the same client id, verify the buffered message replays. Separate
  multi-turn scenario.
- The `Sessions` tab in the Console shows the durable session count when
  the admin plane is wired (it's not exposed on this sample's default
  build, so the badge stays at 0).

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- The SQLite file accumulates session data; clean between runs if
  session-count assertions are added.

## Skip

- "Clear" button.
- Tabs Sessions/Policies/Decisions/Commitments/OWASP — empty.
- Reconnect-and-replay SKILL — separate multi-turn scenario.
- Asserting on `.message--assistant` — broadcast mode never produces one.

## Tips

- `runtime: unknown` in `/api/console/info` is the cheapest distinguisher
  from broadcast siblings (`spring-boot-chat` reports `runtime: demo`).
- The persistence is invisible on the chat surface; the SKILL.md asserts
  the same broadcast post-condition as plain broadcast samples.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/chat` | WebSocket | Broadcast endpoint (`@ManagedService`) |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/durable-sessions` | GET | Lists persisted sessions (when admin exposes it) |
