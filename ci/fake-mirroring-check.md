---
version: 1
name: FakeMirroring smoke test
app: FakeMirroring
---

Validates test runner against FakeMirroring in CI (OCR-based assertions only)

## Steps

1. Wait for "Settings" to appear
2. Verify "Settings" is visible
3. Verify "Safari" is visible
4. Verify "Photos" is visible
5. Verify "Camera" is visible
6. Verify "Messages" is visible
7. Verify "NonExistent" is NOT visible
8. Verify "Instagram" is NOT visible
9. Press Home
10. Screenshot: "smoke_test"
