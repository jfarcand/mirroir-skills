---
version: 1
app: spring-boot-coding-agent
archetype: agent-headless
runtime: spring-boot-4 + atmosphere-agent + atmosphere-sandbox
surface: web
url_root: http://127.0.0.1:8081/
console_endpoint: /atmosphere/agent/coding-agent
console_mode: ai
obstacle_mode: auto
---

# spring-boot-coding-agent

**Known regression (4.0.47-SNAPSHOT):** every HTTP path returns 404
(including `/`, `/atmosphere/console/`, `/atmosphere/agent/coding-agent`,
`/api/console/info`, `/.well-known/agent.json`, `/actuator/health`). The
JVM starts successfully (`Started CodingAgentApplication in 1.91 s`) and
the JSR-356 WebSocket initializer registers
`Atmosphere AI console available at http://localhost:8081/atmosphere/console/`,
but no Spring MVC or Atmosphere filter actually serves the registered
URLs at request time. Chrome-devtools-mcp confirms a Chrome
`"This 127.0.0.1 page can't be found"` error page when navigating to
`/atmosphere/console/`.

This makes the sample **effectively unreachable through any browser-driven
surface**, so the must-pass SKILL only asserts the JVM boots and the
process listens on port 8081. The agent's WebSocket endpoint
`/atmosphere/agent/coding-agent` may still be callable over a raw
WebSocket protocol that bypasses the broken HTTP servlet path (untested in
this revision); a Java/Node client would have to test it directly.

## Diagnostic summary

Earlier sessions confirmed:
- `atmosphereConsoleFilter urls=[/atmosphere/console/*] order=0` is
  registered in Spring's `Mapping filters:` debug log.
- Adding `System.err.println` to `ConsoleResourceFilter.doFilter()` and
  rebuilding `atmosphere-spring-boot-starter` showed the filter is
  **never invoked** for any `/atmosphere/console/*` request.
- A near-identical Spring Boot sample (`spring-boot-dentist-agent`) works
  correctly with the same starter version on the same machine.
- The difference is not `spring-boot-starter-actuator` (removing it
  doesn't fix the regression).
- The packaged fat-jar reproduces the same 404; not a `spring-boot:run`
  dev-classloader artifact.

Root cause is unresolved — further triage requires either filter-chain
breakpoint debugging (`jdb`) or rebuilding the starter with TRACE-level
filter-invocation logging across the chain ahead of `ConsoleResourceFilter`.

## Boot prerequisites

- JDK 21
- Default port: 8081 (in `application.yml` `server.port=8081`).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-coding-agent`.
- Boot wait: ~1–4 s. Ready when boot log emits
  `Started CodingAgentApplication in N seconds`.
- Env the SKILL.md must set (do not gate on outcome — the regression
  affects HTTP not boot):
  - `LLM_MODE=fake`.
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Served URLs (all 404 under the regression)

| Path | Observed |
|---|---|
| `/` | 404 |
| `/atmosphere/console/` | 404 (Chrome error page in chrome-devtools-mcp) |
| `/atmosphere/agent/coding-agent` | 404 (HTTP); WebSocket may still work |
| `/api/console/info` | 404 (no JSON body, empty response) |
| `/.well-known/agent.json` | 404 |
| `/actuator/health` | 404 |

## Structure

Documented as observed in chrome-devtools-mcp snapshot 2026-05-16:
- Chrome shows the standard `"This 127.0.0.1 page can't be found"` error
  view (RootWebArea title `"127.0.0.1"`, h1
  `"This 127.0.0.1 page can't be found"`, `"HTTP ERROR 404"`).
- No served content reaches the page.

The sample's intent (per its README and source):
- `@Agent(name = "coding-agent")` exposes a sandbox-bearing `@Prompt`.
- `Sandbox` SPI selects Docker if available, in-process fallback otherwise.
- `AgentResumeHandle` registers long-running runs with `RunRegistry`.

None of this is observable through the chat surface under the current
regression.

## Obstacles

- The HTTP-surface regression — sample-blocking for any chrome-devtools-
  driven SKILL.
- Docker sandbox requires Docker daemon to be reachable; falls back to
  in-process otherwise.

## Skip

- All Console-surface SKILLs — nothing is served.
- WebSocket-direct SKILLs — require a non-browser client; out of scope for
  the chrome-devtools-only must-pass set.

## Tips

- Use `Started CodingAgentApplication` log scrape as the boot-readiness
  signal, not HTTP probes (all 404).
- If the regression is fixed in a future version, the canonical surfaces
  to assert would be `/atmosphere/console/` (Console SPA) plus
  `/atmosphere/agent/coding-agent` WebSocket; structure similar to
  `spring-boot-dentist-agent`.

## Test surface

| Path | Method | Expected (once regression resolved) |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/agent/coding-agent` | WebSocket | Agent endpoint |
| `/.well-known/agent.json` | GET | A2A agent card |
| `/actuator/health` | GET | CI readiness probe |
