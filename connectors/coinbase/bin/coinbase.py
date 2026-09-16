#!/usr/bin/env python3
"""Minimal Coinbase Exchange REST API CLI for the muse-connectors skill.

Reads (View permission): list accounts, read one account, read an account's
ledger (history).

WRITES (confirm-gated, exact --confirm string on every call; the API key
needs the Trade permission): order-place (POST /orders: market/limit
buy/sell), order-cancel (DELETE /orders/{id}).

Auth: the per-user `custom.coinbase` credential stores a JSON object with
{"api_key": ..., "passphrase": ..., "signing_key": ...} (base64 signing key),
as described in the official Exchange REST quickstart
(docs.cdp.coinbase.com/exchange/introduction/rest-quickstart). The runtime
swaps the surrogate on approved egress, only to api.exchange.coinbase.com.

Signing (docs.cdp.coinbase.com/exchange/rest-api/authentication):
prehash = timestamp + METHOD + requestPath + body; HMAC-SHA256 over the
prehash with the base64-decoded secret, then base64-encode the digest.
CB-ACCESS-TIMESTAMP is seconds since Unix epoch UTC and must be within 30
seconds of API server time, so the system clock must be current.

Honesty note: the HMAC signature is computed over the credential surrogate
value as delivered by the credential store. Whether the runtime's egress
substitution keeps signed headers valid must be verified in a live test
before first signed use. Draft, untested.

Use --env test (default, public sandbox) or --env prod (live trading).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.coinbase"
ALLOWED_HOSTS = ("api.exchange.coinbase.com",
                 "api-public.sandbox.exchange.coinbase.com")
BASES = {
    "test": "https://api-public.sandbox.exchange.coinbase.com",
    "prod": "https://api.exchange.coinbase.com",
}

try:
    sys.path.insert(0, HELPER_PATH)
    from dynamic_credentials import (
        DynamicCredentialError,
        dynamic_credential_entry,
        ensure_allowed_url,
    )
except ImportError:
    sys.exit(
        "error: this CLI needs the Muse dynamic_credentials helper at "
        f"{HELPER_PATH} (install this skill on a Muse runtime to use it)"
    )


# ---------------------------------------------------------------------------
# Auth + API plumbing
# ---------------------------------------------------------------------------

def credentials():
    try:
        surrogate = dynamic_credential_entry(CREDENTIAL_NAME)["surrogate"]
    except DynamicCredentialError:
        print(
            "not connected: no custom.coinbase credential is stored.\n"
            "Collect it via the secure credential flow "
            "(credentials.request_api_access) as a JSON object "
            '{"api_key": "...", "passphrase": "...", "signing_key": "..."} '
            "created on the Coinbase Exchange website (API key settings). "
            "Create the key with View (read-only) permissions. "
            "See this skill's SKILL.md Auth section.",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        creds = json.loads(str(surrogate))
    except (json.JSONDecodeError, ValueError):
        sys.exit("error: credential must be a JSON object with api_key, "
                 "passphrase, and signing_key")
    missing = [k for k in ("api_key", "passphrase", "signing_key")
               if not str(creds.get(k) or "").strip()]
    if missing:
        sys.exit(f"error: credential JSON is missing: {', '.join(missing)}")
    return (str(creds["api_key"]).strip(),
            str(creds["passphrase"]).strip(),
            str(creds["signing_key"]).strip())


def sign_request(api_key: str, passphrase: str, signing_key_b64: str,
                 method: str, path: str, body: str = "") -> dict:
    timestamp = str(time.time())
    try:
        key = base64.b64decode(signing_key_b64, validate=True)
    except Exception:
        sys.exit("error: signing_key is not valid base64")
    prehash = timestamp + method.upper() + path + body
    signature = base64.b64encode(
        hmac.new(key, prehash.encode("utf-8"), hashlib.sha256).digest()
    ).decode("utf-8")
    return {
        "CB-ACCESS-KEY": api_key,
        "CB-ACCESS-SIGN": signature,
        "CB-ACCESS-TIMESTAMP": timestamp,
        "CB-ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json",
    }


def call(env: str, method: str, path: str, params: dict | None = None,
         payload: dict | None = None):
    api_key, passphrase, signing_key = credentials()
    query = ""
    if params:
        clean = {k: str(v) for k, v in params.items() if v is not None}
        if clean:
            query = "?" + urllib.parse.urlencode(clean)
    # Verified scheme: requestPath is the path only (no base URL, no query
    # params); body is the JSON body string, empty for GET requests.
    body = json.dumps(payload) if payload is not None else ""
    headers = sign_request(api_key, passphrase, signing_key, method, path,
                           body)
    url = BASES[env] + path + query
    ensure_allowed_url(url, allowed_hosts=ALLOWED_HOSTS)
    data = body.encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers,
                                 method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8", errors="replace")
            msg = json.loads(body).get("message", body) \
                if body.strip().startswith("{") else body
        except Exception:
            msg = str(exc)
        sys.exit(f"error: coinbase returned HTTP {exc.code}: {msg}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def need_confirm(args, expected: str, effect: str) -> None:
    """Refuse unless --confirm matches the exact effect string."""
    if args.confirm == expected:
        return
    sys.exit(
        f"refusing: {effect}\n"
        f"Re-run with the exact confirmation string:\n"
        f'  --confirm "{expected}"'
    )


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_auth(args):
    body = call(args.env, "GET", "/accounts")
    print(json.dumps({"ok": True, "env": args.env,
                      "accounts": len(body) if isinstance(body, list) else 0},
                     indent=2))


def cmd_accounts(args):
    body = call(args.env, "GET", "/accounts")
    if isinstance(body, list):
        body = [{"id": a.get("id"), "currency": a.get("currency"),
                 "balance": a.get("balance"), "hold": a.get("hold"),
                 "available": a.get("available"),
                 "profile_id": a.get("profile_id"),
                 "trading_enabled": a.get("trading_enabled")}
                for a in body]
    print(json.dumps(body, indent=2))


def cmd_account(args):
    body = call(args.env, "GET", f"/accounts/{args.account_id}")
    print(json.dumps(body, indent=2))


def cmd_ledger(args):
    params = {}
    if args.limit is not None:
        params["limit"] = args.limit
    if args.before is not None:
        params["before"] = args.before
    if args.after is not None:
        params["after"] = args.after
    if args.start_date is not None:
        params["start_date"] = args.start_date
    if args.end_date is not None:
        params["end_date"] = args.end_date
    body = call(args.env, "GET", f"/accounts/{args.account_id}/ledger", params)
    print(json.dumps(body, indent=2))


def cmd_order_place(args):
    """POST /orders (docs: docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/orders/create-new-order).

    Market orders take exactly one of --funds (market buy, quote currency)
    or --size (market sell, base currency). Limit orders need --price plus
    exactly one of --size or --funds.
    """
    order_type = args.type
    if order_type == "market":
        if bool(args.funds) == bool(args.size):
            sys.exit("error: market orders need exactly one of --funds "
                     "(buy) or --size (sell)")
        amount_desc = (f"{args.funds} (quote currency)" if args.funds
                       else f"{args.size} (base currency)")
    else:  # limit
        if not args.price:
            sys.exit("error: limit orders need --price")
        if bool(args.funds) == bool(args.size):
            sys.exit("error: limit orders need exactly one of --funds or "
                     "--size")
        amount_desc = (f"{args.funds or args.size} @ {args.price}")
    expected = (f"place {order_type} {args.side} order on {args.product_id} "
                f"for {args.funds or args.size}")
    need_confirm(
        args, expected,
        f"placing a REAL {order_type} {args.side} order on {args.product_id}: "
        f"{amount_desc}. This trades real funds.")
    payload = {
        "side": args.side,
        "product_id": args.product_id,
        "type": order_type,
        "client_oid": str(uuid.uuid4()),
    }
    if args.price:
        payload["price"] = args.price
    if args.funds:
        payload["funds"] = args.funds
    if args.size:
        payload["size"] = args.size
    result = call(args.env, "POST", "/orders", payload=payload)
    print(json.dumps({
        "ok": True,
        "order_id": result.get("id"),
        "client_oid": payload["client_oid"],
        "side": args.side, "product_id": args.product_id,
        "type": order_type,
        "status": result.get("status"),
    }, indent=2))


def cmd_order_cancel(args):
    """DELETE /orders/{id} (docs: docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/orders/cancel-an-order)."""
    expected = f"cancel order {args.order_id}"
    need_confirm(
        args, expected,
        f"cancelling order {args.order_id}. Unfilled portions will not "
        f"execute.")
    result = call(args.env, "DELETE", f"/orders/{args.order_id}")
    print(json.dumps({"ok": True, "cancelled_order_id": result}, indent=2))


def add_env(p):
    p.add_argument("--env", default="test", choices=("test", "prod"),
                   help="test sandbox (default; free, fake funds) or "
                        "production (live trading)")


def main():
    parser = argparse.ArgumentParser(
        description="Coinbase Exchange REST API CLI (muse-connectors). "
                    "Reads: accounts, ledger. Writes (needs --confirm): "
                    "order-place, order-cancel.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth", help="status check: verify the API key")
    add_env(p)
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("accounts", help="list accounts (GET /accounts)")
    add_env(p)
    p.set_defaults(func=cmd_accounts)

    p = sub.add_parser("account", help="one account (GET /accounts/{id})")
    add_env(p)
    p.add_argument("--account-id", required=True, help="account id")
    p.set_defaults(func=cmd_account)

    p = sub.add_parser("ledger", help="account history "
                                      "(GET /accounts/{id}/ledger)")
    add_env(p)
    p.add_argument("--account-id", required=True, help="account id")
    p.add_argument("--limit", type=int, default=None,
                   help="results per page (default 100)")
    p.add_argument("--before", default=None,
                   help="pagination: start cursor (entry id)")
    p.add_argument("--after", default=None,
                   help="pagination: end cursor (entry id)")
    p.add_argument("--start-date", default=None,
                   help="inclusive minimum posted date (RFC3339, date, or "
                        "datetime)")
    p.add_argument("--end-date", default=None,
                   help="inclusive maximum posted date (RFC3339, date, or "
                        "datetime)")
    p.set_defaults(func=cmd_ledger)

    p = sub.add_parser("order-place",
                       help="place a market or limit order "
                            "(needs --confirm; trades real funds)")
    add_env(p)
    p.add_argument("--side", required=True, choices=("buy", "sell"))
    p.add_argument("--product-id", required=True,
                   help="e.g. BTC-USD")
    p.add_argument("--type", default="market", choices=("market", "limit"))
    p.add_argument("--funds", default=None,
                   help="market buy: amount of QUOTE currency, e.g. 100.00")
    p.add_argument("--size", default=None,
                   help="market sell or limit: amount of BASE currency, "
                        "e.g. 0.001")
    p.add_argument("--price", default=None,
                   help="limit orders: price per unit of base currency")
    p.add_argument("--confirm", default=None)
    p.set_defaults(func=cmd_order_place)

    p = sub.add_parser("order-cancel",
                       help="cancel an open order (needs --confirm)")
    add_env(p)
    p.add_argument("--order-id", required=True, help="order id")
    p.add_argument("--confirm", default=None)
    p.set_defaults(func=cmd_order_cancel)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
