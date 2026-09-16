#!/usr/bin/env python3
"""Minimal Plaid API CLI for the muse-connectors plaid skill.

Read-only bank aggregation: cursor-based transaction sync, account list
with cached balances, and real-time balances.

Auth: the per-user `custom.plaid` credential stores ONE combined value
"client_id:secret" (from dashboard.plaid.com). The CLI splits it on the
first colon (switchbot pattern) and sends both fields in every POST body,
per Plaid's documented auth scheme. The per-bank access_token is supplied
per call via --access-token: the user links their bank through Plaid Link
externally (per plaid.com/docs) and passes the resulting token here; the
CLI never persists it to disk. The real credentials never touch this
script: the runtime swaps the surrogate on approved egress, only to the
Plaid hosts in use.

All Plaid API calls are HTTP POST with a JSON body. There is no verified
credential-only probe endpoint, so `auth` requires --access-token and calls
POST /accounts/get; an HTTP 401 means the client_id/secret or token is bad.

Use --env test (default, free sandbox) or --env prod (requires Plaid
approval and is billed per product).
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.plaid"
ALLOWED_HOSTS = ("sandbox.plaid.com", "production.plaid.com")
BASES = {
    "test": "https://sandbox.plaid.com",
    "prod": "https://production.plaid.com",
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


def credentials() -> tuple[str, str]:
    """Return (client_id, secret) from the combined custom.plaid value."""
    try:
        surrogate = dynamic_credential_entry(CREDENTIAL_NAME)["surrogate"]
    except DynamicCredentialError:
        print(
            "not connected: no custom.plaid credential is stored.\n"
            "Collect it via the secure credential flow "
            "(credentials.request_api_access) as ONE combined value "
            "\"client_id:secret\" from the Plaid dashboard "
            "(dashboard.plaid.com), then retry. "
            "See this skill's SKILL.md Auth section.",
            file=sys.stderr,
        )
        sys.exit(1)
    surrogate = str(surrogate).strip()
    if ":" not in surrogate:
        sys.exit("error: credential must be in 'client_id:secret' format")
    client_id, _, secret = surrogate.partition(":")
    return client_id.strip(), secret.strip()


def call(env: str, path: str, payload: dict) -> dict:
    client_id, secret = credentials()
    body = {"client_id": client_id, "secret": secret}
    body.update(payload)
    url = BASES[env] + path
    ensure_allowed_url(url, allowed_hosts=ALLOWED_HOSTS)
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8", errors="replace"))
            msg = body.get("error_message") or body.get("error_code") or str(exc)
        except Exception:
            msg = str(exc)
        sys.exit(f"error: plaid returned HTTP {exc.code}: {msg}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def cmd_auth(args):
    result = call(args.env, "/accounts/get", {"access_token": args.access_token})
    accounts = result.get("accounts", [])
    print(
        json.dumps(
            {"ok": True, "env": args.env, "accounts": len(accounts)},
            indent=2,
        )
    )


def cmd_transactions_sync(args):
    cursor = args.cursor
    added, modified, removed = [], [], []
    while True:
        payload = {
            "access_token": args.access_token,
            "count": args.count,
        }
        if cursor:
            payload["cursor"] = cursor
        result = call(args.env, "/transactions/sync", payload)
        added.extend(result.get("added", []))
        modified.extend(result.get("modified", []))
        removed.extend(result.get("removed", []))
        cursor = result.get("next_cursor")
        if not result.get("has_more"):
            break
    print(
        json.dumps(
            {
                "env": args.env,
                "added": added,
                "modified": modified,
                "removed": removed,
                "next_cursor": cursor,
                "has_more": False,
            },
            indent=2,
        )
    )


def cmd_accounts(args):
    result = call(args.env, "/accounts/get", {"access_token": args.access_token})
    accounts = [
        {
            "account_id": a.get("account_id"),
            "name": a.get("name"),
            "official_name": a.get("official_name"),
            "type": a.get("type"),
            "subtype": a.get("subtype"),
            "balances": a.get("balances"),
        }
        for a in result.get("accounts", [])
    ]
    print(json.dumps({"env": args.env, "accounts": accounts}, indent=2))


def cmd_balances(args):
    result = call(args.env, "/accounts/balance/get", {"access_token": args.access_token})
    accounts = [
        {
            "account_id": a.get("account_id"),
            "name": a.get("name"),
            "balances": a.get("balances"),
        }
        for a in result.get("accounts", [])
    ]
    print(json.dumps({"env": args.env, "accounts": accounts}, indent=2))


def add_env(p):
    p.add_argument(
        "--env",
        default="test",
        choices=("test", "prod"),
        help="test sandbox (default, free) or production (needs Plaid approval, billed)",
    )


def add_token(p):
    p.add_argument(
        "--access-token",
        required=True,
        help="user's Plaid Link access token for one bank item (never persisted)",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Plaid bank-data API CLI (muse-connectors, read-only)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser(
        "auth", help="verify the client_id/secret and access token"
    )
    add_env(p)
    add_token(p)
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser(
        "transactions-sync",
        help="cursor-based transaction sync (loops has_more automatically)",
    )
    add_env(p)
    add_token(p)
    p.add_argument(
        "--cursor",
        default=None,
        help="cursor from a previous sync (omit on the first call)",
    )
    p.add_argument("--count", type=int, default=100, help="results per page")
    p.set_defaults(func=cmd_transactions_sync)

    p = sub.add_parser(
        "accounts", help="list accounts with cached balances"
    )
    add_env(p)
    add_token(p)
    p.set_defaults(func=cmd_accounts)

    p = sub.add_parser(
        "balances", help="real-time account balances"
    )
    add_env(p)
    add_token(p)
    p.set_defaults(func=cmd_balances)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
