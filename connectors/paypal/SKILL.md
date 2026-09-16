---
name: "paypal"
description: "PayPal reporting plus confirm-gated money movement: check balances, search transactions, send batch payouts, cancel subscriptions, refund captures. Every write needs an exact --confirm string. Trigger phrases: paypal, paypal balance, paypal transactions, paypal payout, paypal refund."
metadata: { "includeInPrompt": true }
tagline: "PayPal balances and transaction search, plus confirm-gated payouts, subscription cancels, and refunds (all writes need --confirm)."
catalog_auth: "PayPal REST app (per-user; OAuth2 client credentials via developer.paypal.com dashboard)"
catalog_hosts: ["api-m.paypal.com", "api-m.sandbox.paypal.com"]
---

# PayPal

## Purpose
PayPal account reporting plus money movement via the PayPal REST APIs: list balances, search transactions (up to 3 years of history), pull balance net summaries and daily summaries, and, with explicit confirmation, send batch payouts, cancel subscriptions, and refund captured payments.

**MONEY WARNING: `payout-create`, `subscription-cancel`, and `refund` move real money (or stop future billing).** Every write prints the exact amount, recipient, and effect, and refuses to run unless the `--confirm` string matches it exactly. Never skip confirmation, and always state the amount and recipient to the user before they confirm.

## Tooling
All commands go through `bin/paypal.py`:

```bash
bin/paypal.py auth                                                     # verify the credential (test env)
bin/paypal.py balance                                                  # list all balances
bin/paypal.py transactions --start-date 2026-08-01 --end-date 2026-08-31
bin/paypal.py transactions --start-date 2026-08-01 --end-date 2026-08-31 --page-size 500 --page 2
bin/paypal.py balance-summary --start-date 2026-08-01 --end-date 2026-08-31 --currency USD
bin/paypal.py daily-summary --date 2026-09-15

# Writes: each needs the exact --confirm string the CLI prints
bin/paypal.py payout-create --receiver someone@example.com --amount 10.00 --currency USD
bin/paypal.py subscription-cancel --subscription-id I-BWAFV3EHJXK7 --reason "Duplicate plan"
bin/paypal.py refund --capture-id 8F12345678901234X                    # full refund
bin/paypal.py refund --capture-id 8F12345678901234X --amount 10.99 --currency USD  # partial
```

Pass `--env prod` to any command to use production instead of the sandbox (default `--env test`).

## Auth
- Provider id: `paypal` (credential is collected as `custom.paypal`)
- Collection: OAuth 2.0 client credentials via the secure credential flow (`credentials.request_api_access`). Create a REST API app in the developer.paypal.com dashboard to get a client ID and secret. Sandbox is instant; production needs a PayPal business account, no approval needed. The runtime exchanges the credentials at `POST /v1/oauth2/token` and hands the CLI a fresh access token as a Bearer credential.
- Scopes: reporting commands work with the default app scopes. `payout-create` needs the `https://uri.paypal.com/payments/payouts` scope (per the Payouts API reference); `subscription-cancel` needs `https://uri.paypal.com/services/subscriptions`; `refund` needs `https://uri.paypal.com/services/payments/refund` (per PayPal's OAuth scope docs).
- Allowed hosts: `api-m.sandbox.paypal.com`, `api-m.paypal.com`
- Status check: `bin/paypal.py auth` (must return `"ok": true`)

## Operating Rules
1. **Money movement needs exact confirmation.** `payout-create`, `subscription-cancel`, and `refund` require the exact `--confirm` string the CLI prints, stating the amount, currency, and recipient (or subscription/capture id). Never skip it, and state the amount and recipient to the user in plain words before they confirm.
2. **Default to the sandbox.** Stay in `--env test` unless the user explicitly asks for live production. Production calls move or refund real money; report results exactly as returned and never speculate about missing entries.
3. **Payouts on live need approval.** PayPal requires a business account in good standing plus permission to use Payouts on live accounts (per the Payouts Terms and Conditions). Sandbox payouts work without it. If a live payout 403s, tell the user to request Payouts access in their PayPal account.
4. **Date-range limit.** Transaction search allows at most a 31-day range per request. The CLI refuses wider ranges; run multiple requests and combine the results yourself when the user needs a longer window.
5. Transaction history goes back up to 3 years; anything older is not available through this API.
6. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/paypal.py`). Do not print, log, or transmit the client secret.

## Files
- SKILL.md
- bin/paypal.py

## Maturity
🧪 Draft: written from PayPal's public API docs; not yet live-tested end-to-end. Write endpoints verified from developer.paypal.com (Payouts API reference, Subscriptions API reference, issue-refund guide). The `reason` field on subscription-cancel is sent with a default; current docs do not say explicitly whether it is required.
