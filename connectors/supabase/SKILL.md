---
name: "supabase"
description: "Read a Supabase Postgres database over PostgREST: list tables, query rows. Trigger phrases: supabase, supabase table, query supabase."
metadata: { "includeInPrompt": true }
---

# Supabase

## Purpose
Read-only access to the user's Supabase project database through PostgREST: list tables and query rows. Use when the user asks what's in their Supabase database or wants to inspect table contents.

## Tooling
All commands go through `bin/supabase.py`. Every command takes the global `--project-ref` (the 20-character ref in the project URL `https://<ref>.supabase.co`):

```bash
bin/supabase.py --project-ref abcdefghijklmnopqrst tables
bin/supabase.py --project-ref abcdefghijklmnopqrst query --table profiles --limit 20
```

## Auth
- Provider id: `supabase` (credential is collected as `custom.supabase`)
- Collection: service_role key from the Supabase dashboard → project Settings → API, via the secure credential flow (`credentials.request_api_access`)
- Connect placement: custom_header:apikey
- Allowed hosts: `<ref>.supabase.co` (per project ref)
- Status check: `bin/supabase.py --project-ref <ref> tables` (must return table names)

## Operating Rules
1. This skill is read-only by design: no insert, update, or delete commands ship.
2. Reading needs no confirmation.
3. The service_role key bypasses Row Level Security: it sees everything in the database. Only share row contents the user asked for, and never paste them into public channels.
4. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/supabase.py`). Do not print, log, or transmit the key value.

## Files
- SKILL.md
- bin/supabase.py

## Maturity
🧪 Draft: written from Supabase's public PostgREST docs; not yet live-tested end-to-end.
