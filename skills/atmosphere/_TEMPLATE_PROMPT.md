---
version: 1
name: Atmosphere sample authoring prompt
purpose: Tells an LLM how to author APP.md + SKILL.md for an Atmosphere sample
---

# Prompt — author APP.md + SKILL.md for an Atmosphere sample

You are an LLM with chrome-devtools-mcp tools. You're given an Atmosphere sample
name (e.g. `spring-boot-ai-chat`). Your task is to author the two artifacts for
that sample under `mirroir-skills/`:

- `patterns/atmosphere/<sample>/APP.md`
- `skills/atmosphere/<sample>/<flow>.md`

You may **not** infer selectors from grep or from sibling samples. Every claim
in APP.md must come from one of:
1. A chrome-devtools-mcp `take_snapshot` of the live JVM, OR
2. A direct read of the sample's source code (`samples/<sample>/`), OR
3. A `curl` you ran in this session (and you quote the response verbatim).

## Steps

1. **Boot the sample.**
   - Spring Boot samples: `./mvnw -q spring-boot:run -pl samples/<sample>`
   - Quarkus samples: `./mvnw -q -Dquarkus.console.enabled=false quarkus:dev -pl samples/<sample>`
   - WAR (legacy `chat`): `./mvnw -q jetty:run -pl samples/<sample>`
   - Embedded Jetty: `./mvnw -q test -Pserver -pl samples/<sample>`
   - exec:java (legacy embedded / grpc): `./mvnw -q exec:java -pl samples/<sample>`
   - Env: always set `LLM_MODE=fake` and `ATMOSPHERE_AUTH_ENABLED=false`.

2. **Wait for ready.** Poll `GET <url_root>` until 200; ports vary per sample
   (read `application.yml` / `application.properties`).

3. **Probe `/api/console/info`** with curl. Quote the JSON response — that's
   your authoritative source for `console_endpoint` and `console_mode`.

4. **Open Chrome on `<url_root>/atmosphere/console/`** via
   `mcp__chrome-devtools__new_page`.

5. **Snapshot.** Call `mcp__chrome-devtools__take_snapshot`. Read the a11y tree.
   Identify:
   - Header text + subtitle (`atmosphere.console-subtitle` from `application.yml`)
   - Nav tabs (which tabs render — Chat, Sessions, Policies, Decisions, Commitments, OWASP, others?)
   - Status pill text (should begin with `Connected` when WebSocket handshakes)
   - Chat input + send button presence
   - Any sample-specific surfaces (tool-activity, approval-prompt, governance panels, etc.)

6. **Drive the canonical flow.** Use chrome-devtools-mcp's `fill` + `click` +
   `wait_for` to:
   - Click into the chat input
   - Type a one-sentence prompt
   - Click the send button
   - Wait for `[data-testid=message-bubble].message--user` to appear
   - For AI samples: also wait for `[data-testid=message-bubble].message--assistant`
   - For broadcast samples: no assistant; just the user echo
   - For governance samples: assistant may be blocked by interceptors — note honestly
   - Take a second snapshot to confirm the bubble rendered

7. **Author `APP.md`** with sections: front-matter (version, app, archetype,
   runtime, surface, url_root, console_endpoint, console_mode, obstacle_mode),
   Boot prerequisites, Structure (DERIVED FROM YOUR SNAPSHOT — not inferred),
   Obstacles, Skip, Tips, Test surface.

8. **Author `SKILL.md`** as imperative steps an LLM (the deterministic runner
   or another LLM agent) follows. Cross-reference an existing shared SKILL.md
   only when your snapshot proves the flow is byte-equivalent.

9. **Validate end-to-end** by emitting an equivalent scenario YAML and running
   `mirroir-run --run-scenario`. Confirm `playwright batch completed passed>=1`.

10. **Commit** with message stating which evidence sources you used (chrome-devtools
    snapshot + `/api/console/info` curl + source-code grep). Do NOT claim "validated
    1/1" unless step 9 actually passed.

## Anti-patterns to avoid

- Inferring "this sample uses the same Vue Console so selectors must match." Even
  when true, you must snapshot to confirm. Two Atmosphere samples in this session
  diverged from the canonical (ms-governance blocks assistant emit; some samples
  parameterize endpoints).
- Reusing a sibling sample's APP.md "Structure" section without snapshotting
  this one. Tabs and surfaces vary (governance samples gain Policies/Decisions;
  multi-room samples have a room selector; ai-tools has tool-activity).
- Bulk-generating from grep. Discovery is the point.
