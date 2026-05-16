---
version: 1
app: spring-boot-mcp-server
archetype: mcp-server-with-broadcast
runtime: spring-boot-4 + atmosphere-runtime + atmosphere-mcp
surface: web
url_root: http://127.0.0.1:8083/atmosphere/console/
console_endpoint: /atmosphere/ai-chat
console_mode: broadcast
obstacle_mode: auto
---

# spring-boot-mcp-server

Atmosphere as a Model Context Protocol (MCP) **server** — exposes a set of
`@AiTool` methods to remote MCP clients (Claude Desktop, IDE plugins, etc.).
The Console-surface chat is a **broadcast** sample because the LLM is on the
client side; the server's responsibility is to advertise tools and serve
their results over the MCP-over-WebSocket transport. The chat endpoint
shown in the Console is the auxiliary `/atmosphere/ai-chat` broadcast — the
MCP traffic itself flows on `/atmosphere/mcp` or similar.

## Boot prerequisites

- JVM: JDK 21
- **Default port: 8083** (in `application.properties`).
- Command: `./mvnw -q spring-boot:run -pl samples/spring-boot-mcp-server`.
- Boot wait: ~2–5 s (observed start at 2.18 s).
- Env the SKILL.md must set:
  - `LLM_MODE=fake` (not load-bearing for broadcast surface).
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Multi-client broadcast chat",
  "endpoint": "/atmosphere/ai-chat",
  "runtime": "demo",
  "mode": "broadcast"
}
```

`mode: broadcast` — must assert on the user bubble. The MCP plane is
NOT advertised here; query `/api/mcp/info` for the tool registry.

## Structure

### Header / Navigation
- Subtitle: `"Multi-client broadcast chat"`
- Six tabs: Chat / Sessions / **Policies 4** / Decisions / Commitments / OWASP.

`"Policies 4"` indicates four governance policies on tool exposure
(safe-tool allow-list, rate-limit, etc.).

### Chat tab (broadcast — observed via chrome-devtools-mcp snapshot 2026-05-16)

- Status: `"Connected · websocket"`.
- Empty state: `"Start a broadcast"` / `"Type a message below — every
  subscriber on this endpoint will receive it."`.
- After send: only `[data-testid=message-bubble].message--user` appears.
- `.message--assistant` never appears.

### MCP surface (out of must-pass scope)

- `/atmosphere/mcp` — MCP-over-WebSocket transport for tool calls.
- `/api/mcp/tools` — REST listing of exposed `@AiTool` methods.
- An MCP client (Claude Desktop config, IDE plugin, custom test client)
  would connect to `/atmosphere/mcp`, list tools, and invoke them. The
  chat-surface SKILL doesn't exercise this path.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- Port 8083 — non-standard.

## Skip

- "Clear" button.
- Tabs Sessions/Decisions/Commitments/OWASP — empty.
- MCP tool-call SKILL — separate scenario, MCP-client fixture.
- Asserting on `.message--assistant` — broadcast mode never produces one.

## Tips

- The presence of `Policies 4` is the cheapest signal that the MCP
  governance plane is wired (without query'ing `/api/mcp/tools`).
- The broadcast surface is incidental — the MCP server's real value is
  on the `/atmosphere/mcp` path. A SKILL.md that only validates broadcast
  proves the server booted and the console is reachable, not that MCP
  tools are callable.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/ai-chat` | WebSocket | Broadcast endpoint (auxiliary) |
| `/atmosphere/mcp` | WebSocket | MCP-over-WebSocket transport |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/mcp/tools` | GET | Lists exposed `@AiTool`s |
| `/api/policies` | GET | Lists the 4 tool-exposure policies |
