---
version: 1
name: Governance policy denial — default-stance refusal
app: spring-boot-ms-governance-chat
surface: web
tags: ["atmosphere", "governance", "policy", "must-pass"]
---

Open the Atmosphere Console and send a plain prompt without metadata.
Verify the governance plane refuses the request with a policy-named error
rendered in an assistant bubble. The denial is expected behavior — the
sample is a rules-over-context demo whose default stance is "deny without
required metadata."

## Preconditions

The runner boots the JVM via `boot_once`. The boot env declared by `SAMPLE.md`
must include:

- `LLM_MODE=fake`.
- `ATMOSPHERE_AUTH_ENABLED=false`.

Boot ready when:
- `GET http://127.0.0.1:8090/atmosphere/console/` returns 200, AND
- `GET /api/console/info` reports `"endpoint":"/atmosphere/ms-governance"`
  with subtitle
  `"Microsoft Agent Governance Toolkit — rules-over-context demo"`.

Port 8090 (not 8080).

## Steps

1. Open `http://127.0.0.1:8090/atmosphere/console/`.
2. Wait for `[data-testid=status-label]` text to begin with `"Connected"`.
3. Tap `[data-testid=chat-input]` to focus.
4. Type `"Hello — one short sentence please."` (any non-empty prompt; the
   denial is metadata-driven, not content-driven).
5. Tap `[data-testid=chat-send]`.
6. Wait for `[data-testid=message-bubble].message--assistant` to be visible.
7. Verify the bubble renders (visible + non-empty text). Body contains
   `"Denied by policy"`. The full denial body is
   `"Error: Denied by policy 'require-tenant-id': required metadata key
   'tenant-id' is missing"` but the substring `"Denied by policy"` is the
   robust assertion if the policy name changes.
8. Screenshot: `chat-policy-deny-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. The denial happens server-side
before any LLM call so latency is consistent and transport-independent.

## Skip / obstacles

None when both env vars are set. A real-LLM key (`OPENAI_API_KEY` etc.)
does not affect the outcome — the policy plane intercepts before the LLM
is contacted.

## Verify (post-conditions)

- Exactly one `[data-testid=message-bubble].message--user` element.
- At least one `[data-testid=message-bubble].message--assistant` element
  matches and is visible. Body contains `"Denied by policy"`.
- Zero `[data-testid=tool-activity]` panels (denial happens before tool
  dispatch).
- Console nav shows `"Policies 7"` (full Microsoft governance toolkit
  loaded).
- No console errors logged (the policy denial is rendered as a message,
  not a JS error).
