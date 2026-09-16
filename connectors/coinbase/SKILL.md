---
name: "coinbase"
description: "Read Coinbase Exchange account balances and account history via the Exchange REST API (HMAC auth). Trigger phrases: coinbase, coinbase accounts, crypto balance, exchange balances, account ledger."
metadata: { "includeInPrompt": true }
tagline: "Read-only Coinbase Exchange account balances and history. No orders, transfers, or converts."
catalog_auth: "Coinbase Exchange API key (per-user; create with View/read-only permissions; collected as api_key/passphrase/signing_key via the secure credential flow)"
catalog_hosts: ["api.exchange.coinbase.com"]
---

# Coinbase

## Purpose
Read-only access to Coinbase Exchange account data: list trading accounts with balances, read a single account, and read an account's ledger (activity history: transfers, matches, fees, conversions). Reach for this when the user asks for their Coinbase balances or wants to see what happened on an Exchange account.

This connector is READ-ONLY by design. There are no subcommands for orders, transfers, conversions, or anything else that moves funds.

## Tooling
All commands go through `bin/coinbase.py`:

```bash
bin/coinbase.py auth                                              # verify the API key (GET /accounts)
bin/coinbase.py accounts                                          # list accounts with balances (GET /accounts)
bin/coinbase.py account --account-id ACCT_ID                       # one account (GET /accounts/{id})
bin/coinbase.py ledger --account-id ACCT_ID                       # account history (GET /accounts/{id}/ledger)
bin/coinbase.py ledger --account-id ACCT_ID --limit 50            # ledger with pagination limit
bin/coinbase.py ledger --account-id ACCT_ID \
    --start-date 2026-09-01 --end-date 2026-09-15                  # ledger for a date range
bin/coinbase.py ledger --account-id ACCT_ID --before ENTRY_ID      # paginate backwards
```

Ledger entry fields include id, created_at, amount, balance, type (transfer, match, fee, rebate, conversion, and others), and a details object (trade details for match/fee entries).

## Auth
- Provider id: `coinbase` (credential is collected as `custom.coinbase`)
- Collection: Coinbase Exchange API key via the secure credential flow (`credentials.request_api_access`). The user creates the key on the Coinbase Exchange website (API settings); the flow collects ONE JSON object: `{"api_key": "...", "passphrase": "...", "signing_key": "..."}` (apiKey, passphrase, signingKey per the official Exchange REST quickstart).
- Required permissions: the key must be created with the **View** permission (read permissions for all GET endpoints), and nothing else. View-only keys can still list accounts, read accounts, and read ledgers per the official docs.
- Auth scheme (per docs.cdp.coinbase.com/exchange/rest-api/authentication): every request carries `CB-ACCESS-KEY` (the API key string), `CB-ACCESS-SIGN` (base64 of HMAC-SHA256 over `timestamp + METHOD + requestPath + body` using the base64-decoded signing key), `CB-ACCESS-TIMESTAMP` (seconds since Unix epoch UTC, allowed decimals), and `CB-ACCESS-PASSPHRASE`. requestPath is the path only, no base URL or query params; body is empty for GET requests. HMAC-SHA256 and base64 are Python stdlib, so the CLI signs without extra dependencies.
- Allowed hosts: `api.exchange.coinbase.com`
- Status check: `bin/coinbase.py auth` (calls GET /accounts; prints `ok: true` on success)

## Operating Rules
1. **READ-ONLY by design.** This connector has no order, transfer, convert, deposit, withdrawal, or address-generation commands. Do not hand-roll a write request around it: writing requires Trade/Transfer permissions this credential must never have.
2. **Create the key with View permission only.** View covers every endpoint this connector uses. If the user needs trades or transfers, that is out of scope for this connector.
3. **The 30-second timestamp window is real.** `CB-ACCESS-TIMESTAMP` must be within 30 seconds of Coinbase's API server time, so the system clock must be current. If signed calls return timestamp errors, check the local clock against `https://api.exchange.coinbase.com/time` before debugging anything else.
4. **Never exfiltrate the credential.** The CLI only ever handles the JSON surrogate (see `bin/coinbase.py`). Do not print, log, or transmit api_key, passphrase, or signing_key.
5. Honesty flags (unverified while building this connector): the HMAC signature is computed over the credential surrogate value as delivered by the credential store; whether the runtime's egress substitution keeps signed headers valid must be verified in a live test before first signed use. The ledger's no-date-filter behavior (returns the past 1 day only when neither start_date nor end_date is set) comes from the docs changelog, not a live test. `GET /accounts/{id}/holds` and `GET /accounts/{id}/transfers` are documented read endpoints in the same Exchange reference but were deliberately left out to keep this connector minimal; add them in a follow-up if needed.

## Files
- SKILL.md
- bin/coinbase.py

## Maturity
🧪 Draft: built from the official Coinbase Exchange REST docs; not yet live-tested end-to-end.
