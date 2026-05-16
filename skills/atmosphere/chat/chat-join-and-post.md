---
version: 1
name: Legacy WAR chat — join + post broadcast
app: chat
surface: web
tags: ["atmosphere", "broadcast", "war", "legacy", "must-pass"]
---

Open the legacy WAR chat at its bespoke UI, enter a name, post one message,
verify both the join system-message and the chat bubble render. The WAR
does not ship the Atmosphere Console; per
`feedback_no_claim_without_e2e_validation.md` the SKILL.md drives the
sample's actual user-facing UI (chrome-devtools-mcp-verified).

## Preconditions

The runner boots the JVM via `boot_once`. No env vars required.

Boot ready when:
- `GET http://127.0.0.1:8080/` returns 200 with HTML containing
  `<title>Atmosphere 4.0 Chat</title>`.

## Steps

1. Open `http://127.0.0.1:8080/`.
2. Wait for status text starting with `"Connected"`. Locator:
   `getByText('Connected', { exact: false })`.
3. Tap the name input: `getByPlaceholder('Enter your name to join…')`.
4. Type `"tester"`.
5. Tap the `Send` button: `getByRole('button', { name: 'Send' })`.
6. Wait for system message `"tester has joined!"`. Locator:
   `getByText('tester has joined!')`.
7. Tap the message input (placeholder has changed):
   `getByPlaceholder('Type a message…')`.
8. Type `"hello from mirroir-skills"`.
9. Tap `Send` again.
10. Wait for the chat bubble: locator
    `getByText('hello from mirroir-skills')`.
11. Verify both texts are visible (`"tester has joined!"` system message and
    `"hello from mirroir-skills"` chat bubble).
12. Screenshot: `chat-war-broadcast-rendered`.

## Cross-browser

Same flow on chromium + firefox + webkit. WebSocket primary with
long-polling fallback.

## Skip / obstacles

- mirroir-run's CSS/text-selector emitter is less complete than its
  `[data-testid]` path; an automated mirroir-run validation of this SKILL.md
  may need direct Playwright-script support rather than the YAML scenario
  format. Chrome-devtools-mcp end-to-end verification is the authoritative
  proof of the flow.

## Verify (post-conditions)

- Text `"tester has joined!"` is visible.
- Text `"hello from mirroir-skills"` is visible.
- Status pill text starts with `"Connected"`.
- No browser console errors logged.
