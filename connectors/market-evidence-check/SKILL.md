---
name: "market-evidence-check"
description: "Read-only client for server-computed OKX cost and freshness evidence; requires trust in the service operator. Trigger phrases: OKX cost check, order book impact, quote freshness, market evidence check."
metadata: { "includeInPrompt": true }
tagline: "Server-computed OKX evidence via a temporary demo service. No key, no trading."
catalog_auth: "None (calls the operator-hosted API; no API key, account, or wallet)"
catalog_hosts: ["devday.167-179-82-72.nip.io"]
---

# Market Evidence Check

## Purpose
The CLI sends the supplied instrument, side, hypothetical USDT notional, and cost limit to our server at https://devday.167-179-82-72.nip.io/v1/evidence/check. Our server fetches public OKX instrument metadata and order-book data and computes the evidence and GO/WATCH/REJECT result. The CLI does not fetch OKX data directly or independently verify the calculation. The report includes server-computed spread, estimated price impact, estimated one-way cost, quote age, and displayed-depth checks. Use it to explain the server's assessment of the user's stated hypothetical size.

GO means only that our server reports that its snapshot passed the declared checks. It is not a buy/sell recommendation, trading signal, profit prediction, fill guarantee, or permission to trade.

## Trust and availability
The decision is only as trustworthy as our server and its upstream data. A compromised server can fabricate GO and the accompanying evidence. The server-generated SHA-256 digest is not a signature or proof of OKX origin, and the CLI does not verify it.

The configured host is a temporary demo deployment with no availability commitment. If it is withdrawn or unavailable, this connector cannot perform checks; it has no direct-OKX fallback.

## Tooling
All commands go through `bin/market_evidence_check.py` (Python standard library only):

```bash
bin/market_evidence_check.py health
bin/market_evidence_check.py check --instrument BTC-USDT --side buy --notional-usdt 1000 --max-cost-bps 30
```

The CLI parses and prints the server response, normally with an added `http_status`; it does not validate the report schema or recompute the evidence. A complete server report is expected to include `decision`, `reason_codes`, `market_evidence`, `execution_cost`, `policy_checks`, `policy_version`, and `evidence_hash`. These are server assertions, not independently verified OKX evidence.

## Auth
- Provider id: `market-evidence-check`
- Collection: none. Never ask for an API key, exchange credential, account login, wallet, password, seed phrase, or private key. If any step appears to require credentials, stop and report that as a blocker.
- Required scopes: none
- Allowed hosts: `devday.167-179-82-72.nip.io`
- Status check: `bin/market_evidence_check.py health` (expect HTTP 200 and `status: "ok"`)
- API contract: https://raw.githubusercontent.com/yijigao/market-evidence-check-devday/main/connectors/muse/openapi.json
- Server computation source: https://github.com/yijigao/market-evidence-check-devday/blob/main/evidence_api.py. This source is publicly readable; correspondence between that revision and the running demo deployment has not been verified. The OpenAPI document describes the interface, not the implementation.

## Operating Rules
1. Read-only: this connector sends hypothetical check parameters to our API and displays its server-computed report. The published server implementation queries public OKX market data. Neither the client nor that implementation places, modifies, or cancels orders, accesses accounts or wallets, or signs transactions.
2. Treat WATCH, REJECT, non-success HTTP responses, missing or inconsistent report fields, invalid JSON, and timeouts as unsuccessful checks. Never reinterpret an error as GO. The CLI generates WATCH for caught transport/JSON failures; it cannot detect a fabricated successful response from a compromised server. Never suggest placing an order.
3. HTTP 200 alone is not GO; always inspect `decision` and `report_status`.
4. Describe snapshot values as server-reported observations. Distinguish them from fee and slippage assumptions (policy defaults 10 bps and 2 bps). The direct API supports `cost_assumptions`, but this CLI exposes only instrument, side, notional, and max cost; it does not accept custom fee or slippage flags. Never present assumptions as the user's actual account fees.
5. Do not change the user's stated `max_cost_bps` limit without telling them first.
6. This is market evidence, not financial advice.

## Files
- SKILL.md
- bin/market_evidence_check.py

## Maturity
🧪 Draft: depends on a temporary operator-hosted demo API. Historical CLI checks recorded on 2026-10-06 returned health HTTP 200, a sample GO, and invalid-side HTTP 400/REJECT. Current uptime, independent catalog installation, and correspondence between the public server source and the deployed service have not been established by this review.
