---
name: "coinbase"
description: "Coinbase Exchange accounts plus confirm-gated trading: balances and history read-only; market/limit order placement and order cancels need an exact --confirm string. Trigger phrases: coinbase, coinbase accounts, crypto balance, exchange balances, account ledger, place order."
metadata: { "includeInPrompt": true }
tagline: "Coinbase Exchange balances and history, plus confirm-gated order placement and cancels (all trades need --confirm)."
catalog_auth: "Coinbase Exchange API key (per-user; View permission for reads, Trade permission for orders; collected as api_key/passphrase/signing_key via the secure credential flow)"
catalog_hosts: ["api.exchange.coinbase.com"]
---

# Coinbase

## Purpose
Work with Coinbase Exchange accounts: list trading accounts with balances, read a single account, read an account's ledger (activity history), and, with explicit confirmation, place market/limit orders and cancel open orders.

**MONEY WARNING: `order-place` trades real funds and `order-cancel` stops unfilled portions from executing.** Every write prints the exact side, product, and amount, and refuses to run unless the `--confirm` string matches it exactly. Never skip confirmation, and state the trade in plain words to the user before they confirm.

## Tooling
All commands go through `bin/coinbase.py`. Default `--env test` uses the public Exchange sandbox (fake funds); pass `--env prod` for live trading.

```bash
bin/coinbase.py auth                                              # verify the API key (GET /accounts)
bin/coinbase.py accounts                                          # list accounts with balances (GET /accounts)
bin/coinbase.py account --account-id ACCT_ID                       # one account (GET /accounts/{id})
bin/coinbase.py ledger --account-id ACCT_ID                       # account history (GET /accounts/{id}/ledger)
bin/coinbase.py ledger --account-id ACCT_ID --limit 50            # ledger with pagination limit
bin/coinbase.py ledger --account-id ACCT_ID \
    --start-date 2026-09-01 --end-date 2026-09-15                  # ledger for a date range
bin/coinbase.py ledger --account-id ACCT_ID --before ENTRY_ID      # paginate backwards

# Writes: each needs the exact --confirm string the CLI prints
bin/coinbase.py order-place --side buy --product-id BTC-USD --funds 100.00
bin/coinbase.py order-place --side sell --product-id BTC-USD --type limit --price 100000.00 --size 0.001
bin/coinbase.py order-cancel --order-id ORDER_ID
```

Ledger entry fields include id, created_at, amount, balance, type (transfer, match, fee, rebate, conversion, and others), and a details object (trade details for match/fee entries).

## Auth
- Provider id: `coinbase` (credential is collected as `custom.coinbase`)
- Collection: Coinbase Exchange API key via the secure credential flow (`credentials.request_api_access`). The user creates the key on the Coinbase Exchange website (API settings); the flow collects ONE JSON object: `{"api_key": "...", "passphrase": "...", "signing_key": "..."}` (apiKey, passphrase, signingKey per the official Exchange REST quickstart).
- Required permissions: reads need the **View** permission (read permissions for all GET endpoints). `order-place` and `order-cancel` need the **Trade** permission ("Key can post orders and get data", per the Exchange API docs); View-only keys get 403s on POST/DELETE /orders. If the user only wants reads, create the key with View only.
- Auth scheme (per docs.cdp.coinbase.com/exchange/rest-api/authentication): every request carries `CB-ACCESS-KEY` (the API key string), `CB-ACCESS-SIGN` (base64 of HMAC-SHA256 over `timestamp + METHOD + requestPath + body` using the base64-decoded signing key), `CB-ACCESS-TIMESTAMP` (seconds since Unix epoch UTC, allowed decimals), and `CB-ACCESS-PASSPHRASE`. requestPath is the path only, no base URL or query params; body is the JSON body for POST requests, empty for GET/DELETE. HMAC-SHA256 and base64 are Python stdlib, so the CLI signs without extra dependencies.
- Environments: `--env test` (default) hits the public Exchange sandbox at `api-public.sandbox.exchange.coinbase.com` (same paths, same signing; fake funds). `--env prod` hits `api.exchange.coinbase.com`.
- Allowed hosts: `api.exchange.coinbase.com`, `api-public.sandbox.exchange.coinbase.com`
- Status check: `bin/coinbase.py auth` (calls GET /accounts; prints `ok: true` on success)

## Operating Rules
1. **Real money needs exact confirmation.** `order-place` and `order-cancel` require the exact `--confirm` string the CLI prints, stating side, product, and amount. Never skip it, and state the trade in plain words to the user before they confirm.
2. **Default to the sandbox.** Stay in `--env test` (public Exchange sandbox, fake funds) unless the user explicitly asks for live trading. Live orders move real funds; report results exactly as returned and never speculate.
3. **Trade permission is a separate decision.** Read-only keys (View) cannot place or cancel orders. Only collect a Trade-permissioned key when the user explicitly wants trading; for balance checks, View-only keys are the right choice.
4. **The 30-second timestamp window is real.** `CB-ACCESS-TIMESTAMP` must be within 30 seconds of Coinbase's API server time, so the system clock must be current. If signed calls return timestamp errors, check the local clock against `https://api.exchange.coinbase.com/time` before debugging anything else.
5. **Never exfiltrate the credential.** The CLI only ever handles the JSON surrogate (see `bin/coinbase.py`). Do not print, log, or transmit api_key, passphrase, or signing_key.
6. Honesty flags (unverified while building this connector): the HMAC signature is computed over the credential surrogate value as delivered by the credential store; whether the runtime's egress substitution keeps signed headers valid must be verified in a live test before first signed use. The ledger's no-date-filter behavior (returns the past 1 day only when neither start_date nor end_date is set) comes from the docs changelog, not a live test. `GET /accounts/{id}/holds` and `GET /accounts/{id}/transfers` are documented read endpoints in the same Exchange reference but were deliberately left out to keep this connector minimal; add them in a follow-up if needed.

## Files
- SKILL.md
- bin/coinbase.py

## Maturity
🧪 Draft: built from the official Coinbase Exchange REST docs; not yet live-tested end-to-end. Order endpoints verified from the Exchange API reference (create-new-order, cancel-an-order pages); market-buy `funds` / market-sell `size` rules come from the docs' Funds section.
