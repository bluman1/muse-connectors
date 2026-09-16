---
name: "slack"
description: "Read and write Slack: list channels, read history, post messages, search, list users. Trigger phrases: slack, slack channel, post to slack, search slack."
metadata: { "includeInPrompt": true }
---

# Slack

## Purpose
Read and write the user's Slack workspace: list channels, read recent history, post messages, search messages, list users. Use when the user mentions Slack or wants something sent to / found in a Slack channel.

## Tooling
All commands go through `bin/slack.py`:

```bash
bin/slack.py auth                                        # verify the connection (auth.test)
bin/slack.py channels                                    # list channels (public + private)
bin/slack.py history --channel C0123456789 --limit 20    # recent messages in a channel
bin/slack.py post --channel C0123456789 --text "hello"    # post a message
bin/slack.py users                                       # list workspace users
bin/slack.py search --query "deploy friday"              # search messages
```

Channel arguments accept channel IDs (`C...`). Use `channels` to resolve a `#name` to its ID first.

## Auth
- Provider id: `slack` (credential is collected as `custom.slack`)
- Collection: provider OAuth via the secure credential flow (`credentials.request_api_access`)
- Required scopes: `channels:read`, `channels:history`, `groups:read`, `groups:history`, `chat:write`, `users:read`, `search:read`
- Allowed hosts: `slack.com`
- Status check: `bin/slack.py auth` (must return `"ok": true`)

## Operating Rules
1. `post` is a write: confirm the exact text and destination channel with the user before sending, unless standing permission to post exists.
2. Reading (channels, history, users, search) needs no confirmation.
3. Slack rate-limits aggressively on bursts; if a call returns `ratelimited`, wait the `Retry-After` seconds and continue — do not hammer.
4. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/slack.py`). Do not print, log, or transmit the token value.

## Files
- SKILL.md
- bin/slack.py

## Maturity
🧪 Draft — written from Slack's public Web API docs; not yet live-tested end-to-end.
