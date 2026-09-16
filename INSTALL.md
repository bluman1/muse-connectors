# How the one-paste install works

Every connector in this repo is installed from a single prompt of the form:

```
Install this connector: <raw-github-url-to-SKILL.md>
<installer instructions>
```

The URL is just the link to the skill file in this repo. Nothing else is needed because of one convention:

## The `## Files` manifest convention

Every `connectors/<name>/SKILL.md` ends with a `## Files` section listing every file the skill needs, as paths relative to the skill directory:

```markdown
## Files
- SKILL.md
- bin/slack.py
- references/api-notes.md
```

An installing Muse resolves each path against the SKILL.md URL (`.../connectors/slack/SKILL.md` → `.../connectors/slack/bin/slack.py`) and downloads exactly those files. The manifest is the audit boundary: if a file isn't listed, it isn't installed.

## What the installing Muse does

1. Fetch the SKILL.md URL.
2. Download every file in the `## Files` manifest into `~/workspace/skills/<name>/`, preserving directory structure.
3. Byte-compile any `bin/*.py` (`python3 -m py_compile`).
4. Follow the skill's `## Auth` section: collect the user's credential via the secure credential flow (`credentials.request_api_access`) for the named provider id. This registers the connector as `custom.<provider-id>` in the user's private vault.
5. Run the skill's status check command and report what the connector can do.

## Why this is safe to paste

- The prompt contains no secrets and asks for none ("never ask me for raw keys in chat" is part of the standard instructions).
- The credential flow is provider OAuth or a hosted API-key form — the key goes straight to the user's secure vault, never through chat.
- The skill code only ever sees surrogate tokens that the runtime swaps for the real credential on approved requests, and only to the skill's declared allowed hosts.

## If installation fails

- **Provider declined by the credential flow:** some providers can't be expressed (password logins, session cookies, request signing, or more than one secret). The flow says so by name — that connector can't ship in this form.
- **A file 404s:** the manifest and the repo are out of sync — file an issue.
- **Status check fails after connecting:** the credential may be under-scoped (see the skill's `## Auth` for required scopes) — reconnect with the listed scopes.
