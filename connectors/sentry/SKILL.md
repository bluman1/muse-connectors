---
name: "sentry"
description: "Triage Sentry errors: list organizations, projects, and recent issues. Trigger phrases: sentry, sentry errors, error tracking."
metadata: { "includeInPrompt": true }
tagline: "List organizations and projects, triage unresolved issues from the last 24h. Read-only."
catalog_auth: "auth token (per-user, sentry.io \u2192 Settings \u2192 Auth Tokens)"
catalog_hosts: ["sentry.io"]
---

# Sentry

## Purpose
Read-only error triage for the user's Sentry: list organizations, list projects in an org, and list unresolved issues from the last 24 hours sorted by frequency. Use when the user asks what's broken, what's new in Sentry, or wants an error triaged.

## Tooling
All commands go through `bin/sentry.py`:

```bash
bin/sentry.py orgs                   # your organizations
bin/sentry.py projects --org myorg   # projects in an org
bin/sentry.py issues --org myorg     # unresolved issues, last 24h, by frequency
```

## Auth
- Provider id: `sentry` (credential is collected as `custom.sentry`)
- Collection: auth token from sentry.io → Settings → Auth Tokens (scopes `org:read`, `project:read`, `event:read`), via the secure credential flow (`credentials.request_api_access`)
- Connect placement: bearer_header
- Allowed hosts: `sentry.io`
- Status check: `bin/sentry.py orgs` (must return your organizations)

## Operating Rules
1. This skill is read-only by design: no issue resolve/assign/archive commands ship.
2. Reading needs no confirmation.
3. This skill targets sentry.io (US SaaS). EU-region (`de.sentry.io`) and self-hosted Sentry use a different host and are out of scope for this skill.
4. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/sentry.py`). Do not print, log, or transmit the token value.

## Files
- SKILL.md
- bin/sentry.py

## Maturity
🧪 Draft: written from Sentry's public API docs; not yet live-tested end-to-end.
