---
name: "paypal"
description: "Read-only PayPal reporting: check balances, search transactions, pull balance and daily summaries via the Transaction Search API. Trigger phrases: paypal, paypal balance, paypal transactions."
metadata: { "includeInPrompt": true }
tagline: "Check PayPal balances and search transactions read-only. No payments, payouts, or transfers."
catalog_auth: "PayPal REST app (per-user; OAuth2 client credentials via developer.paypal.com dashboard)"
catalog_hosts: ["api-m.paypal.com", "api-m.sandbox.paypal.com"]
---

# PayPal

## Purpose
Read-only access to PayPal account reporting via the Transaction Search API v1: list balances, search transactions (up to 3 years of history), and pull balance net summaries and daily summaries. Reach for this when the user wants to check a PayPal balance or look up past transactions.

**This connector cannot move money.** It has no payment, payout, transfer, refund, or order endpoints. If the user asks to send money or pay someone, say plainly that this connector cannot do that and suggest the PayPal app or dashboard instead.

## Tooling
All commands go through `bin/paypal.py`:

```bash
bin/paypal.py auth                                                     # verify the credential (test env)
bin/paypal.py balance                                                  # list all balances
bin/paypal.py transactions --start-date 2026-08-01 --end-date 2026-08-31
bin/paypal.py transactions --start-date 2026-08-01 --end-date 2026-08-31 --page-size 500 --page 2
bin/paypal.py balance-summary --start-date 2026-08-01 --end-date 2026-08-31 --currency USD
bin/paypal.py daily-summary --date 2026-09-15
```

Pass `--env prod` to any command to use production instead of the sandbox (default `--env test`).

## Auth
- Provider id: `paypal` (credential is collected as `custom.paypal`)
- Collection: OAuth 2.0 client credentials via the secure credential flow (`credentials.request_api_access`). Create a REST API app in the developer.paypal.com dashboard to get a client ID and secret. Sandbox is instant; production needs a PayPal business account, no approval needed. The runtime exchanges the credentials at `POST /v1/oauth2/token` and hands the CLI a fresh access token as a Bearer credential.
- Allowed hosts: `api-m.sandbox.paypal.com`, `api-m.paypal.com`
- Status check: `bin/paypal.py auth` (must return `"ok": true`)

## Operating Rules
1. **Read-only by design.** This connector has no way to send, request, or refund money. Never present it as able to make payments or payouts, and never hand-roll a payment against a PayPal endpoint outside this connector.
2. **Default to the sandbox.** Stay in `--env test` unless the user explicitly asks for live production data. Production results reflect real money movements, so report them exactly as returned and never speculate about missing entries.
3. **Date-range limit.** Transaction search allows at most a 31-day range per request. The CLI refuses wider ranges; run multiple requests and combine the results yourself when the user needs a longer window.
4. Transaction history goes back up to 3 years; anything older is not available through this API.
5. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/paypal.py`). Do not print, log, or transmit the client secret.

## Files
- SKILL.md
- bin/paypal.py

## Maturity
🧪 Draft: written from PayPal's public Transaction Search API docs; not yet live-tested end-to-end.
