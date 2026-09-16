---
name: "typeform"
description: "Work with Typeform: list forms and responses, and (with confirmation) manage response webhooks. Trigger phrases: typeform, form responses, typeform webhook, typeform forms."
metadata: { "includeInPrompt": true }
---

# Typeform

## Purpose
Work with the Typeform API: verify the token, list forms, fetch a form and its fields, list form responses with their answers, list a form's webhooks, and (each behind an exact-match confirmation) create or delete a form webhook. Reach for this when the user wants to see who answered a Typeform or wire form responses into an endpoint.

## Tooling
All commands go through `bin/typeform.py`:

```bash
bin/typeform.py auth                                # verify the token (GET /me)
bin/typeform.py forms --limit 25                    # list forms
bin/typeform.py form-get --form-id FORM_ID          # one form + its fields
bin/typeform.py responses --form-id FORM_ID         # list form responses
bin/typeform.py webhooks-list --form-id FORM_ID     # list the form's webhooks
bin/typeform.py webhook-create --form-id FORM_ID \
    --tag new-responses --url https://example.com/hook \
    --confirm "create webhook new-responses on form FORM_ID for https://example.com/hook"
bin/typeform.py webhook-delete --form-id FORM_ID \
    --tag new-responses \
    --confirm "delete webhook new-responses on form FORM_ID"
```

`responses` accepts `--since` (ISO timestamp) to pull only newer responses. Creating a webhook with an existing `--tag` overwrites it.

## Auth
- Provider id: `typeform` (credential is collected as `custom.typeform`)
- Collection: personal access token (Typeform account > Settings > Personal tokens) via the secure credential flow (`credentials.request_api_access`); the runtime hands the CLI a fresh Bearer token
- Auth scheme: `Authorization: Bearer <token>` on every request
- Allowed hosts: `api.typeform.com`
- Status check: `bin/typeform.py auth`

## Operating Rules
1. **Webhook writes need confirmation on every call.** `webhook-create` requires `--confirm` with the exact string the CLI echoes (it names the tag, the form, and the endpoint URL) because it starts delivering respondent data to an endpoint. `webhook-delete` needs the same, because it silently stops delivery.
2. Creating a webhook with an existing tag overwrites it: confirm the tag is intended before reusing one.
3. Reads (`auth`, `forms`, `form-get`, `responses`, `webhooks-list`) are read-only and need no confirmation.
4. Endpoint honesty flag: the webhook paths used by the CLI (`PUT /forms/{form_id}/webhooks/{tag}`, `DELETE /forms/{form_id}/webhooks/{tag}`) are taken from Typeform's public developer docs and have not been verified in a live flow. Verify against a real form before relying on them.
5. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/typeform.py`). Do not print, log, or transmit the token.

## Files
- SKILL.md
- bin/typeform.py

## Maturity
Draft: written from Typeform's public developer docs; not yet live-tested end-to-end.
