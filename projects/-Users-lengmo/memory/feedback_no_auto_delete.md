---
name: No auto delete dev data
description: Never auto-delete user's development data without explicit permission
type: feedback
---

Never automatically delete the user's development data (database records, test users, etc.) to fix startup errors. Instead, find the root cause or add the data-clearing as a user-facing feature.

**Why:** User had development data (test users) that was deleted without permission to fix an API startup error.

**How to apply:** When encountering data conflicts during startup, fix the code/schema rather than deleting existing data. If cleanup is needed, always ask the user first or provide a UI/API for them to do it manually.
