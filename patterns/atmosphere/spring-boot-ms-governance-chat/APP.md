---
version: 1
app: spring-boot-ms-governance-chat
archetype: governance-policy-denial
runtime: spring-boot-4 + atmosphere-ai + atmosphere-governance
surface: web
url_root: http://127.0.0.1:8090/atmosphere/console/
console_endpoint: /atmosphere/ms-governance
console_mode: ai
obstacle_mode: auto
---

# spring-boot-ms-governance-chat

`@AiEndpoint` plus a **stack of 7 governance policies** modeled on the
Microsoft Agent Governance Toolkit ("rules-over-context"). The default
prompt path **DENIES** every request that doesn't include required metadata
(starting with `tenant-id`). The distinguishing surface is the
**policy-denial error bubble** rendered as a `.message--assistant` bubble
that explicitly names the violating policy.

## Boot prerequisites

- JVM: JDK 21
- **Default port: 8090** (in `application.yml`).
- Command:
  `./mvnw -q spring-boot:run -pl samples/spring-boot-ms-governance-chat` from
  the Atmosphere repo root.
- Boot wait: ~1–4 s (observed start at 0.97 s).
- Env the SKILL.md must set:
  - `LLM_MODE=fake`.
  - `ATMOSPHERE_AUTH_ENABLED=false`.

## Console-info advertisement

`GET /api/console/info` returns:

```json
{
  "subtitle": "Microsoft Agent Governance Toolkit — rules-over-context demo",
  "endpoint": "/atmosphere/ms-governance",
  "runtime": "demo",
  "mode": "ai"
}
```

The endpoint `/atmosphere/ms-governance` is unique to this sample. Subtitle
matches `atmosphere.console-subtitle` in `application.yml`.

## Structure

### Header / Navigation
- Subtitle: `"Microsoft Agent Governance Toolkit — rules-over-context demo"`
- Six tabs: Chat / Sessions / **Policies 7** / Decisions / Commitments / OWASP.

**`Policies 7`** is the highest policy count observed in any sample so far
(multi-agent-startup-team is `Policies 4`, ai-classroom is `Policies 2`).
The 7 policies are the Microsoft Agent Governance Toolkit rule set — use
the badge as a runtime-truth signal that the governance plane is wired with
the full set.

### Chat tab — observed via chrome-devtools-mcp snapshot 2026-05-16

Send `"Hello — one short sentence please."` (no metadata):
- User bubble: `[data-testid=message-bubble].message--user`.
- **Error/assistant bubble**: `[data-testid=message-bubble].message--assistant` —
  body: `"Error: Denied by policy 'require-tenant-id': required metadata
  key 'tenant-id' is missing"`. No token metrics line — the request was
  rejected before any LLM call.
- No `[data-testid=tool-activity]` — denial happens before tool dispatch.

The default denial is **expected behavior**: the sample demonstrates the
policy plane's "fail closed by default" stance. The `.message--assistant`
class is reused for error bubbles, so the standard assertion still applies
— the SKILL only changes from "verify the AI responded" to "verify the
governance plane responded with a denial."

### Passing requests (out of must-pass scope)

To actually receive an LLM response, the client must include the required
metadata. The Vue console doesn't have an obvious metadata-injection
affordance, so the must-pass SKILL asserts the denial. A separate SKILL
could:
- Inject `tenant-id` via a custom client (atmosphere.js with
  `request.metadata`).
- Verify the request is accepted by the next-in-stack policy chain.

Both paths are out of scope for the chrome-devtools-driven must-pass set.

## Obstacles

- `ATMOSPHERE_AUTH_ENABLED=true` → 401.
- Port 8090 — same default as `spring-boot-ai-tools`, can collide if both
  run.

## Skip

- "Clear" button.
- Sessions/Decisions/Commitments/OWASP tabs — empty here.
- Metadata-bearing happy-path SKILL — separate scenario.

## Tips

- The "Error: Denied by policy 'require-tenant-id': ..." string is
  load-bearing for the policy-denial assertion. Asserting the substring
  `"Denied by policy"` is robust if the specific policy name evolves.
- `Policies 7` badge is the cheapest one-line check that the governance
  toolkit loaded.

## Test surface

| Path | Method | Purpose |
|---|---|---|
| `/atmosphere/console/` | GET | Console SPA index |
| `/atmosphere/ms-governance` | WebSocket | Governance-gated AI endpoint |
| `/api/console/info` | GET | `{subtitle, endpoint, runtime, mode}` |
| `/api/policies` | GET | Lists the 7 registered policies |
| `/api/governance/decisions` | GET | Audit trail of allow/deny decisions |
