---
name: "front"
description: "List Front inboxes and read conversations. Read-only. Trigger phrases: front, front inbox, shared inbox, support inbox."
metadata: { "includeInPrompt": true }
tagline: "List Front inboxes and read conversations in your shared inbox. Read-only."
catalog_auth: "Front API token (per-user, Front Settings \u2192 API)"
catalog_hosts: ["api2.frontapp.com"]
---

# Front

## Purpose
Read the user's Front (shared-inbox) account: list inboxes (`inboxes`: name, address) and list conversations in an inbox (`conversations`: subject, status). Read-only: no reply, assign, or other write calls ship in this skill.

## Tooling
All commands go through `bin/front.py`:

```bash
bin/front.py inboxes                        # list inboxes (name, address)
bin/front.py conversations --inbox inb_123  # recent conversations (subject, status)
```

Use `inboxes` first to resolve an inbox name to its id.

## Auth
- Provider id: `front` (credential is collected as `custom.front`)
- Collection: API token via the secure credential flow (`credentials.request_api_access`): create one in Front → Settings → API (needs API access enabled)
- Connect placement: `bearer_header`
- Allowed hosts: `api2.frontapp.com`
- Status check: `bin/front.py inboxes` (a successful list proves the token works)

## Operating Rules
1. This skill is read-only. No replies, assignments, tags, or conversation mutations ship.
2. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/front.py`). Do not print, log, or transmit the token value.

## Files
- SKILL.md
- bin/front.py

## Maturity
🧪 Draft: written from Front's public Core API docs; not yet live-tested end-to-end.
