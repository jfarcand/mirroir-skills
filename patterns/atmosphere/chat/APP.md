---
version: 1
app: chat
archetype: legacy-war-broadcast
runtime: war + atmosphere-runtime
surface: web
url_root: http://127.0.0.1:8080/
console_endpoint: /chat
console_mode: broadcast
obstacle_mode: auto
---

# chat (legacy WAR)

Classic Atmosphere broadcast chat packaged as a **WAR** for deployment to
any Servlet 6.0+ container. Uses `@ManagedService` on `/chat`. Predates the
Spring Boot starter — does **not** ship the Atmosphere Console SPA. Instead
serves its own bespoke chat UI at the WAR's context root.

**Surface deviation**: this is the only sample in the must-pass set whose
must-pass SKILL.md drives a non-Console UI. The bespoke UI is the canonical
delivery surface for the WAR sample (the Console isn't on the classpath),
so per `feedback_no_claim_without_e2e_validation.md` we drive what the user
actually sees.

## Boot prerequisites

- JDK 21 + Maven.
- Default port: 8080 via `jetty:run`.
- Command: `mvn -q jetty:run` (from `samples/chat/`) or
  `./mvnw -q jetty:run -pl samples/chat -am` (from the repo root).
- Boot wait: ~5–15 s (Jetty embedded). Ready when TCP `:8080` accepts
  connections AND `GET /` returns 200 with `<title>Atmosphere 4.0 Chat</title>`.
- No env vars required. The WAR is auth-less; CORS allows all origins.

## Served URLs

| Path | Content |
|---|---|
| `/` | Bespoke chat UI (Vite-bundled SPA, NOT the Atmosphere Console) |
| `/assets/*` | JS/CSS bundles for the bespoke UI |
| `/chat` | WebSocket endpoint (`@ManagedService` on `/chat`) |

`/api/console/info` and `/atmosphere/console/` are **not** served — the WAR
doesn't depend on `atmosphere-spring-boot-starter`.

## Structure (bespoke UI — observed via chrome-devtools-mcp snapshot 2026-05-16)

- Page title: `"Atmosphere 4.0 Chat"`.
- Header heading: `"Atmosphere 4.0 Chat"`.
- Subtitle StaticText:
  `"Managed Service • JDK 21 Virtual Threads • WebSocket with Long-Polling Fallback"`.
- Status pill: `"Connected · websocket"` (mirrors the Console's status-label
  shape but no `data-testid` attribute).
- **Two-step flow**:
  1. Initial state: textbox placeholder `"Enter your name to join…"` +
     `Send` button (disabled until name entered).
  2. After name submit: status message `"<name> has joined!"` rendered as
     a system message; textbox placeholder switches to `"Type a message…"`;
     subsequent messages render as `<name>` + timestamp + body chat bubbles.

The UI has **no `[data-testid]` attributes** — selectors must be text-,
role-, or placeholder-based.

## Obstacles

- `mvn` (not `./mvnw`) — the legacy sample uses the global Maven install.
- Port 8080 — common.
- No Console SPA available.
- mirroir-run's current scenario emitter targets `[data-testid=…]` selectors
  natively; running this sample's SKILL.md needs text/placeholder selectors
  which the emitter handles less consistently. Validation was done via
  chrome-devtools-mcp directly; the Playwright batch run for this scenario
  is non-uniform. Captured as a known harness limitation; the sample itself
  is fully working (verified end-to-end via chrome-devtools-mcp).

## Skip

- Asserting on `/atmosphere/console/*` — that surface doesn't exist here.
- Multi-tab broadcast SKILL — separate scenario.

## Tips

- Use `placeholder=`-based locators in Playwright:
  `getByPlaceholder('Enter your name to join…')` and
  `getByPlaceholder('Type a message…')`.
- The `Send` button is the same button across both steps; it has different
  enable-states (`disabled` until input is non-empty).

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/` | GET | Bespoke chat UI |
| `/chat` | WebSocket | Broadcast endpoint (`@ManagedService`) |
| `/assets/index-*.js` | GET | Vite-bundled SPA bundle |
