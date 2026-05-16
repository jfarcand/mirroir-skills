---
version: 1
name: MCP server — broadcast smoke + console boot
app: spring-boot-mcp-server
surface: web
tags: ["atmosphere", "mcp", "broadcast", "must-pass"]
---

Open the Atmosphere Console wired to the broadcast endpoint of the MCP
server sample, post one message, verify the user bubble renders. The MCP
tool-call SKILL is a separate scenario (MCP-client fixture).

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by
`SAMPLE.md` must include:

- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8083/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"mode":"broadcast"`.

Port 8083 (not 8080).

## Steps

1. Open `http://127.0.0.1:8083/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"hello from mcp-server"`.
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--user` to be visible.
7. Verify the user bubble renders (visible + non-empty text). Do not wait
   for or assert on `.message--assistant` — broadcast mode never produces
   one.
8. Screenshot: `chat-broadcast-mcp-server-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit.

## Skip / obstacles

None when `ATMOSPHERE_AUTH_ENABLED=false`. The MCP tool-call SKILL needs an
MCP client connected to `/atmosphere/mcp`; out of scope for the chrome-
devtools-only must-pass set.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element.
- Zero `[data-testid=message-bubble].message--assistant` elements.
- Console nav shows `"Policies 4"` — confirms the MCP governance plane is
  wired.
- No console errors logged.
