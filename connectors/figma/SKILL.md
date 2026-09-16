---
name: "figma"
description: "Look up your Figma user and read file metadata. Read-only. Trigger phrases: figma, figma file, design file."
metadata: { "includeInPrompt": true }
---

# Figma

## Purpose
Read from the user's Figma: the authenticated user (`me`) and file metadata (`file`: name, lastModified, version, thumbnailUrl). Read-only: no comment, component, or file-write calls ship. The full file document is intentionally not returned: it is too large to be useful in chat, so `file` surfaces metadata only.

## Tooling
All commands go through `bin/figma.py`:

```bash
bin/figma.py me                 # authenticated user (handle, email)
bin/figma.py file --key KEY     # file metadata: name, lastModified, version, thumbnailUrl
```

Get the file key from a Figma URL: it is the segment after `/file/` or `/design/`.

## Auth
- Provider id: `figma` (credential is collected as `custom.figma`)
- Collection: personal access token via the secure credential flow (`credentials.request_api_access`): create one in Figma → Settings → Personal access tokens (needs at least the `file_content:read` scope for `file`)
- Connect placement: `custom_header:X-Figma-Token` (Figma PATs use `X-Figma-Token`, not `Authorization: Bearer`)
- Allowed hosts: `api.figma.com`
- Status check: `bin/figma.py me` (a successful response proves the token works)

## Operating Rules
1. This skill is read-only. No writes, comments, or webhooks ship.
2. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/figma.py`). Do not print, log, or transmit the token value.

## Files
- SKILL.md
- bin/figma.py

## Maturity
🧪 Draft: written from Figma's public REST API docs; not yet live-tested end-to-end.
