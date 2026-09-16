---
name: "notion"
description: "Work with Notion: search pages, read page properties, query databases. Trigger phrases: notion, notion page, notion database."
metadata: { "includeInPrompt": true }
tagline: "Search pages and databases, read page properties, query databases (read-only)."
catalog_auth: "Notion internal integration token (per-user, created at notion.so/my-integrations)"
catalog_hosts: ["api.notion.com"]
---

# Notion

## Purpose
Work with the user's Notion workspace: search pages and databases, read page properties, and query databases. Use when the user mentions Notion or wants something looked up in their Notion.

## Tooling
All commands go through `bin/notion.py`:

```bash
bin/notion.py auth                              # verify the connection (search with page_size 1)
bin/notion.py search --query "roadmap"           # search pages and databases
bin/notion.py page --id PAGE_ID                  # read a page's properties
bin/notion.py query-db --id DATABASE_ID          # query a database (first 20 rows)
```

IDs are the 32-hex-character Notion IDs (with or without dashes).

## Auth
- Provider id: `notion` (credential is collected as `custom.notion`)
- Collection: Notion internal integration token via the secure credential flow (`credentials.request_api_access`); create one at notion.so/my-integrations → New integration → copy the "Internal Integration Secret", then share the pages/databases you need with that integration inside Notion
- Required scopes: n/a (integration capabilities are set at notion.so/my-integrations)
- Allowed hosts: `api.notion.com`
- Status check: `bin/notion.py auth` (must return `"ok": true`)

## Operating Rules
1. This skill is read-only: it has no write commands. If the user asks for writes, say so plainly instead of improvising one.
2. Reading needs no confirmation.
3. Notion rate-limits to ~3 requests/second; if a call returns 429, wait the `Retry-After` seconds and continue.
4. Pages and databases must be explicitly shared with the integration inside Notion, or they will not appear in search results: if a known page is missing, tell the user to share it with the integration.
5. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/notion.py`). Do not print, log, or transmit the token value.

## Files
- SKILL.md
- bin/notion.py

## Maturity
🧪 Draft: written from Notion's public API docs; not yet live-tested end-to-end.
