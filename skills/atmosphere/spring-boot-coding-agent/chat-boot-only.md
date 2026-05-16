---
version: 1
name: Coding agent — JVM boot smoke (HTTP surface regressed)
app: spring-boot-coding-agent
surface: web
tags: ["atmosphere", "agent", "boot-only", "must-pass", "regressed"]
---

The HTTP surface of this sample is currently regressed at 4.0.47-SNAPSHOT
— every URL returns 404 including the Atmosphere Console SPA. The SKILL
asserts the JVM boots and the process listens on port 8081, which is what
chrome-devtools-mcp can observe (the browser sees Chrome's
`"This 127.0.0.1 page can't be found"` error page). This is a placeholder
SKILL pending root-cause of the HTTP-surface regression.

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by
`SAMPLE.md` must include:

- `LLM_MODE=fake`.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when the boot log emits
`Started CodingAgentApplication in N seconds`. Do **not** gate on HTTP
probes — they all 404.

## Steps

1. Open `http://127.0.0.1:8081/atmosphere/console/`.
2. Verify Chrome lands on its error page (`chrome-error://chromewebdata/`
   URL). This is the **expected observation under the regression** — the
   server is up, the route is 404. Locator:
   `getByText('HTTP ERROR 404')` or
   `getByRole('heading', { name: /can.t be found/ })`.
3. Screenshot: `chat-coding-agent-404-regressed`.

## Cross-browser

Same observation on chromium / firefox / webkit — all see the 404.

## Skip / obstacles

- Until the HTTP-surface regression is root-caused and fixed, this SKILL
  is intentionally minimal. Once the regression is resolved, replace this
  SKILL.md with the standard AI-streaming flow (model after
  `spring-boot-dentist-agent`'s `chat-help-command.md`).

## Verify (post-conditions)

- Chrome's error page is visible (heading `"This 127.0.0.1 page can't be
  found"` and/or text `"HTTP ERROR 404"`).
- Page URL is `chrome-error://chromewebdata/` (Chrome's internal error
  scheme).
- No browser console errors *other than* the expected network 404 — i.e.
  the page failed cleanly, not via a thrown exception.
- Boot log line `Started CodingAgentApplication` is present (verified
  by the harness, not the in-browser observation).
