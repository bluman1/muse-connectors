---
name: "neon"
description: "Read and write Neon: list projects, create projects and branches, start compute endpoints. Trigger phrases: neon, postgres database."
metadata: { "includeInPrompt": true }
---

# Neon

## Purpose
Manage Neon Postgres infrastructure through the Neon Management API: list projects, create projects and branches, and start compute endpoints. Use when the user wants to provision or inspect their Neon databases.

## Tooling
All commands go through `bin/neon.py`:

```bash
bin/neon.py auth                                              # verify the API key
bin/neon.py projects                                          # list projects
bin/neon.py create-project --name "my-app"                    # create a project
bin/neon.py create-branch --project <project-id> --name dev   # create a branch
bin/neon.py start-endpoint --project <project-id> --endpoint <endpoint-id>  # start a compute endpoint
```

## Auth
- Provider id: `neon` (credential is collected as `custom.neon`)
- Collection: API key via the secure credential flow (`credentials.request_api_access`); created in the Neon console under Account Settings > API Keys
- Allowed hosts: `console.neon.tech`
- Status check: `bin/neon.py auth` (must return `"ok": true`)

## Operating Rules
1. This is the Management API only. SQL runs over the Postgres wire protocol with a separate connection string, so this connector manages infrastructure; it does not run queries.
2. Project and branch creation is confirmation-gated: confirm the name with the user first, unless standing permission exists.
3. Reads (projects) need no confirmation.
4. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/neon.py`). Do not print, log, or transmit the key value.

## Files
- SKILL.md
- bin/neon.py

## Maturity
🧪 Draft: written from Neon's public API docs; not yet live-tested end-to-end.
