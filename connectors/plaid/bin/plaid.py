#!/usr/bin/env python3
"""Minimal Plaid API CLI for the muse-connectors plaid skill.

Bank aggregation: cursor-based transaction sync, account list with cached
balances, and real-time balances (reads).

WRITES (confirm-gated, exact --confirm string on every call): Transfer API
-- transfer-authorize (POST /transfer/authorization/create: runs Plaid's
risk checks and returns a decision), transfer-create (POST /transfer/create:
moves money), transfer-cancel (POST /transfer/cancel). Production transfers
need Plaid's Transfer approval; the sandbox (default --env test) is open.

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


def need_confirm(args, expected: str, effect: str) -> None:
    """Refuse unless --confirm matches the exact effect string."""
    if args.confirm == expected:
        return
    sys.exit(
        f"refusing: {effect}\n"
        f"Re-run with the exact confirmation string:\n"
        f'  --confirm "{expected}"'
    )


def cmd_transfer_authorize(args):
    """POST /transfer/authorization/create (docs: plaid.com/docs/transfer/creating-transfers/).

    Runs Plaid's Signal risk checks. Returns decision: approved, declined,
    or user_action_required. Approved authorizations expire after 1 hour.
    """
    if args.network in ("ach", "same-day-ach") and not args.ach_class:
        sys.exit("error: --ach-class is required for ach networks "
                 "(ccd, ppd, tel, web)")
    expected = (f"authorize {args.type} of {args.amount} "
                f"via {args.network} on account {args.account_id}")
    need_confirm(
        args, expected,
        f"authorizing a {args.type} of {args.amount} via {args.network} "
        f"against account {args.account_id}. This starts a money-movement "
        f"flow; the transfer itself still needs a separate confirmation.")
    payload = {
        "access_token": args.access_token,
        "account_id": args.account_id,
        "type": args.type,
        "network": args.network,
        "amount": args.amount,
        "user": {"legal_name": args.legal_name},
    }
    if args.ach_class:
        payload["ach_class"] = args.ach_class
    if args.idempotency_key:
        payload["idempotency_key"] = args.idempotency_key
    result = call(args.env, "/transfer/authorization/create", payload)
    authz = result.get("authorization", {})
    print(json.dumps({
        "env": args.env,
        "authorization_id": authz.get("id"),
        "decision": authz.get("decision"),
        "decision_rationale": authz.get("decision_rationale"),
    }, indent=2))


def cmd_transfer_create(args):
    """POST /transfer/create (docs: plaid.com/docs/api/products/transfer/initiating-transfers/).

    The authorization_id doubles as the idempotency key: re-using it
    returns the already-created transfer, never a duplicate.
    """
    expected = (f"create transfer of {args.amount or 'authorized amount'} "
                f"from authorization {args.authorization_id}")
    need_confirm(
        args, expected,
        f"creating a REAL transfer against authorization "
        f"{args.authorization_id} ({args.amount or 'full authorized amount'}). "
        f"This moves money out of the bank account.")
    payload = {
        "access_token": args.access_token,
        "account_id": args.account_id,
        "authorization_id": args.authorization_id,
        "description": args.description,
    }
    if args.amount:
        payload["amount"] = args.amount
    result = call(args.env, "/transfer/create", payload)
    transfer = result.get("transfer", {})
    print(json.dumps({
        "env": args.env,
        "transfer_id": transfer.get("id"),
        "status": transfer.get("status"),
        "amount": transfer.get("amount"),
        "network": transfer.get("network"),
        "cancellable": transfer.get("cancellable"),
    }, indent=2))


def cmd_transfer_cancel(args):
    """POST /transfer/cancel. Only works while the transfer is cancellable
    (check /transfer/get). RTP/FedNow instant payouts cannot be cancelled."""
    expected = f"cancel transfer {args.transfer_id}"
    need_confirm(
        args, expected,
        f"cancelling transfer {args.transfer_id}. Only pending transfers "
        f"can be cancelled; once submitted to the payment network it is "
        f"final.")
    result = call(args.env, "/transfer/cancel",
                  {"transfer_id": args.transfer_id})
    print(json.dumps({"env": args.env, "result": result}, indent=2))


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
        description="Plaid bank-data API CLI (muse-connectors): reads plus "
                    "confirm-gated Transfer API writes (moves money)"
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

    p = sub.add_parser(
        "transfer-authorize",
        help="authorize a transfer: runs Plaid risk checks, returns "
             "approved/declined (needs --confirm)",
    )
    add_env(p)
    add_token(p)
    p.add_argument("--account-id", required=True,
                   help="end-user account to debit/credit")
    p.add_argument("--type", required=True, choices=("debit", "credit"),
                   help="debit: into the origination account; credit: out "
                        "of it")
    p.add_argument("--network", required=True,
                   choices=("ach", "same-day-ach", "rtp", "wire"),
                   help="payment network")
    p.add_argument("--amount", required=True,
                   help="max amount to authorize, e.g. 12.34")
    p.add_argument("--ach-class", default=None,
                   help="required for ach networks: ccd, ppd, tel, web")
    p.add_argument("--legal-name", required=True,
                   help="account holder legal name")
    p.add_argument("--idempotency-key", default=None,
                   help="dedupe key (max 50 chars)")
    p.add_argument("--confirm", default=None)
    p.set_defaults(func=cmd_transfer_authorize)

    p = sub.add_parser(
        "transfer-create",
        help="create the transfer from an authorization (needs --confirm; "
             "moves money)",
    )
    add_env(p)
    add_token(p)
    p.add_argument("--account-id", required=True,
                   help="end-user account to debit/credit")
    p.add_argument("--authorization-id", required=True,
                   help="authorization id (also the idempotency key)")
    p.add_argument("--description", required=True,
                   help="bank-statement description (10 chars max for ACH)")
    p.add_argument("--amount", default=None,
                   help="defaults to the full authorized amount")
    p.add_argument("--confirm", default=None)
    p.set_defaults(func=cmd_transfer_create)

    p = sub.add_parser(
        "transfer-cancel",
        help="cancel a pending transfer (needs --confirm)",
    )
    add_env(p)
    add_token(p)
    p.add_argument("--transfer-id", required=True, help="transfer id")
    p.add_argument("--confirm", default=None)
    p.set_defaults(func=cmd_transfer_cancel)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
