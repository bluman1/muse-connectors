---
name: "elevenlabs"
description: "Check your ElevenLabs subscription usage and list available voices. Read-only. Trigger phrases: elevenlabs, eleven labs, voice api, tts voices."
metadata: { "includeInPrompt": true }
---

# ElevenLabs

## Purpose
Check the user's ElevenLabs account: subscription tier and character usage (`me`), and the voices available on the account (`voices`). Read-only — no text-to-speech or other quota-consuming calls ship in this skill.

## Tooling
All commands go through `bin/elevenlabs.py`:

```bash
bin/elevenlabs.py me        # subscription tier, character_count, character_limit
bin/elevenlabs.py voices    # available voices (name, category)
```

## Auth
- Provider id: `elevenlabs` (credential is collected as `custom.elevenlabs`)
- Collection: API key via the secure credential flow (`credentials.request_api_access`) — create one at elevenlabs.io/app/settings/api-keys
- Connect placement: `custom_header:xi-api-key` (ElevenLabs uses `xi-api-key`, not `Authorization: Bearer`)
- Allowed hosts: `api.elevenlabs.io`
- Status check: `bin/elevenlabs.py me` (a successful response proves the key works)

## Operating Rules
1. This skill is read-only. It never consumes characters: no TTS, speech-to-text, or voice-clone calls ship.
2. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/elevenlabs.py`). Do not print, log, or transmit the key value.

## Files
- SKILL.md
- bin/elevenlabs.py

## Maturity
🧪 Draft — written from ElevenLabs' public API docs; not yet live-tested end-to-end.
