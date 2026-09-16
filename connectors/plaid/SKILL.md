---
name: "plaid"
description: "Plaid bank data plus confirm-gated money movement: sync transactions, check balances, and authorize/create/cancel bank transfers. Every transfer needs an exact --confirm string. Trigger phrases: plaid, bank transactions, account balances, bank transfer."
metadata: { "includeInPrompt": true }
tagline: "Sync bank transactions and balances through Plaid, plus confirm-gated bank transfers (all writes need --confirm)."
catalog_auth: "Plaid client_id + secret (per-user; dashboard.plaid.com; Sandbox instant, Production needs Plaid approval) plus the user's own Plaid Link access_token per call"
catalog_hosts: ["sandbox.plaid.com", "production.plaid.com"]
---

# Plaid

## Purpose
Bank data aggregation plus money movement through the Plaid API: cursor-based transaction sync, account lists with cached balances, real-time balance checks, and, with explicit confirmation, the Transfer API: authorize a transfer (runs Plaid's risk checks), create it, and cancel it while it is still pending.

**MONEY WARNING: `transfer-create` moves real money out of the bank account.** Every write prints the exact amount, network, and account, and refuses to run unless the `--confirm` string matches it exactly. Never skip confirmation, and state the amount and destination in plain words to the user before they confirm.

## Tooling
All commands go through `bin/plaid.py`. Every data call needs the user's bank-link `access_token`, passed per invocation via `--access-token` and never written to disk.

```bash
bin/plaid.py auth --access-token ACCESS_TOKEN                          # verify credential + token
bin/plaid.py transactions-sync --access-token ACCESS_TOKEN --count 100 # first sync (no cursor)
bin/plaid.py transactions-sync --access-token ACCESS_TOKEN --cursor CURSOR  # incremental sync
bin/plaid.py accounts --access-token ACCESS_TOKEN                      # accounts with cached balances
bin/plaid.py balances --access-token ACCESS_TOKEN                      # real-time balances
bin/plaid.py accounts --access-token ACCESS_TOKEN --env prod           # production host

# Writes: each needs the exact --confirm string the CLI prints
bin/plaid.py transfer-authorize --access-token ACCESS_TOKEN --account-id ACCT \
    --type debit --network ach --amount 12.34 --ach-class ppd --legal-name "Jane Doe"
bin/plaid.py transfer-create --access-token ACCESS_TOKEN --account-id ACCT \
    --authorization-id AUTH_ID --description "Rent" --amount 12.34
bin/plaid.py transfer-cancel --access-token ACCESS_TOKEN --transfer-id TRANSFER_ID
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
1. **Money movement needs exact confirmation.** `transfer-authorize`, `transfer-create`, and `transfer-cancel` require the exact `--confirm` string the CLI prints, stating amount, network, and account. Never skip it, and state the amount and destination to the user in plain words before they confirm.
2. **Default to `--env test`.** Sandbox is free and immediate; production needs Plaid's Transfer approval (application process) plus paid products, and unapproved production accounts are throttled to $1/transfer, $10/day, $100/month. Switch to `--env prod` only when the user explicitly asks for live bank transfers.
3. **Authorization is step one, not the transfer.** `transfer-authorize` only runs the risk checks and returns approved/declined; approved authorizations expire after 1 hour. Money moves only when `transfer-create` runs with the authorization id.
4. **Never exfiltrate credentials.** The CLI only ever handles surrogates (see `bin/plaid.py`). Do not print, log, or transmit the client_id or secret.
5. **Never persist access tokens.** `--access-token` values stay in memory for one invocation. Do not write them to files, logs, or memory.
6. Transaction sync is cursor-based: store the returned `next_cursor` and pass it back next time for an incremental sync. The first call omits `--cursor`.
7. Honesty flags (unverified while building this connector): the body-based credential scheme depends on the runtime swapping the credential surrogate on egress; whether the split client_id/secret survive substitution inside a JSON body must be confirmed in a live test. No production call has been made through this connector. The `/transfer/cancel` reason field's exact name was not readable in the docs' text rendering, so it is intentionally omitted.

## Files
- SKILL.md
- bin/plaid.py

## Maturity
Draft: written from plaid.com's public API docs; not yet live-tested end-to-end. Transfer endpoints verified from the Transfer guide and API reference (creating-transfers, initiating-transfers pages).
