---
name: "plaid"
description: "Read bank accounts and transactions through Plaid: sync transactions, list accounts, fetch balances. Trigger phrases: plaid, bank transactions, account balances."
metadata: { "includeInPrompt": true }
tagline: "Sync bank transactions and check account balances through Plaid."
catalog_auth: "Plaid client_id + secret (per-user; dashboard.plaid.com; Sandbox instant, Production needs Plaid approval) plus the user's own Plaid Link access_token per call"
catalog_hosts: ["sandbox.plaid.com", "production.plaid.com"]
---

# Plaid

## Purpose
Read-only bank data aggregation through the Plaid API: cursor-based transaction sync, account lists with cached balances, and real-time balance checks. Reach for this when the user wants their bank transactions or balances pulled into Muse, e.g. reconciling spending, watching an account, or building a budget summary. This connector cannot move money; transfers and payments are not implemented.

## Tooling
All commands go through `bin/plaid.py`. Every data call needs the user's bank-link `access_token`, passed per invocation via `--access-token` and never written to disk.

```bash
bin/plaid.py auth --access-token ACCESS_TOKEN                          # verify credential + token
bin/plaid.py transactions-sync --access-token ACCESS_TOKEN --count 100 # first sync (no cursor)
bin/plaid.py transactions-sync --access-token ACCESS_TOKEN --cursor CURSOR  # incremental sync
bin/plaid.py accounts --access-token ACCESS_TOKEN                      # accounts with cached balances
bin/plaid.py balances --access-token ACCESS_TOKEN                      # real-time balances
bin/plaid.py accounts --access-token ACCESS_TOKEN --env prod           # production host
```

`transactions-sync` loops on `has_more` automatically and returns all pages at once, plus `next_cursor` to store for the next incremental sync.

## Auth
- Provider id: `plaid` (credential is collected as `custom.plaid`)
- Collection: ONE combined value `client_id:secret` from the Plaid dashboard (dashboard.plaid.com) via the secure credential flow (`credentials.request_api_access`). Sandbox keys are instant and free; production requires Plaid approval and is billed per product.
- The per-bank `access_token` is NOT part of the stored credential. The user links their bank through Plaid Link externally (per plaid.com docs: create a link token, the user completes Link, then exchange the public token via `/item/public_token/exchange`), and passes the resulting `access_token` per invocation with `--access-token`. The CLI never persists it.
- Auth scheme: `client_id` and `secret` go in every POST JSON body (Plaid's documented scheme). All Plaid API calls are HTTP POST with a JSON body.
- Allowed hosts: `sandbox.plaid.com` (default, `--env test`), `production.plaid.com` (`--env prod`)
- Status check: `bin/plaid.py auth --access-token ACCESS_TOKEN` (there is no documented credential-only probe endpoint, so auth verifies by calling `/accounts/get`)

## Operating Rules
1. **READ-ONLY by design.** No transfers, payments, or account changes exist in this connector. It reads transactions, accounts, and balances only.
2. **Default to `--env test`.** Sandbox is free and immediate. Production needs Plaid approval plus paid products; switch to `--env prod` only when the user explicitly asks for live bank data.
3. **Never exfiltrate credentials.** The CLI only ever handles surrogates (see `bin/plaid.py`). Do not print, log, or transmit the client_id or secret.
4. **Never persist access tokens.** `--access-token` values stay in memory for one invocation. Do not write them to files, logs, or memory.
5. Transaction sync is cursor-based: store the returned `next_cursor` and pass it back next time for an incremental sync. The first call omits `--cursor`.
6. Honesty flags (unverified while building this connector): the body-based credential scheme depends on the runtime swapping the credential surrogate on egress; whether the split client_id/secret survive substitution inside a JSON body must be confirmed in a live test. No production call has been made through this connector.

## Files
- SKILL.md
- bin/plaid.py

## Maturity
Draft: written from plaid.com's public API docs; not yet live-tested end-to-end.
