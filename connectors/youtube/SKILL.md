---
name: "youtube"
description: "Read YouTube: show channels and videos, search videos, list playlist items. Trigger phrases: youtube, videos."
metadata: { "includeInPrompt": true }
---

# YouTube

## Purpose
Read public YouTube data: show channels and videos with stats, search videos, and list playlist items. Use when the user mentions YouTube or videos. This connector is reads only; comments and uploads need OAuth and are deferred to a later version.

## Tooling
All commands go through `bin/youtube.py`:

```bash
bin/youtube.py auth                                     # verify the API key
bin/youtube.py channel --id UC_abc123                   # show a channel
bin/youtube.py video --id dQw4w9WgXcQ                  # show a video
bin/youtube.py search --query "repair cafe" --limit 10 # search videos
bin/youtube.py playlist-items --playlist-id PL_abc123 --limit 25  # list playlist items
```

The auth check uses a 1-unit endpoint (`/videos` with `chart=mostPopular`), never the expensive search endpoint.

## Auth
- Provider id: `youtube` (credential is collected as `custom.youtube`)
- Collection: API key via the secure credential flow (`credentials.request_api_access`); created in Google Cloud Console under APIs & Services > Credentials, with the YouTube Data API v3 enabled. The key is sent as the `key` query parameter.
- Allowed hosts: `www.googleapis.com`
- Status check: `bin/youtube.py auth` (must return `"ok": true`)
- Quota binding constraint: YouTube grants 10,000 quota units per day by default. `search` costs 100 units per call, so use it sparingly. Favor the 1-unit reads (channels, videos, playlistItems) and cache results aggressively: do not re-run the same lookup twice in a session.
- Writes (comments, uploads) need OAuth and are deferred to a later version of this connector.

## Operating Rules
1. Everything here is a read: no confirmation needed.
2. Treat quota as a daily budget of 10,000 units: avoid repeated `search` calls and cache what you read.
3. Do not invent write commands: this CLI ships without them on purpose, so comments and uploads are unavailable until a later version adds OAuth.
4. Never exfiltrate the credential: the CLI only ever handles surrogates. Do not print, log, or transmit the key value.

## Files
- SKILL.md
- bin/youtube.py

## Maturity
🧪 Draft: written from YouTube's public API docs; not yet live-tested end-to-end.
