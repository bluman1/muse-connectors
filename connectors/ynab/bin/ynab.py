#!/usr/bin/env python3
"""Minimal YNAB API CLI for the muse-connectors ynab skill.

Auth: loads the per-user `custom.ynab` credential as a surrogate via the
bundled dynamic_credentials helper. The real OAuth token never touches this
script: the runtime swaps the surrogate on approved egress, only to
api.ynab.com.

The YNAB API is bookkeeping only: it can read and record transactions, but it
cannot move money, make transfers, or touch bank accounts.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.ynab"
ALLOWED_HOSTS = ("api.ynab.com",)
API = "https://api.ynab.com/v1"

try:
    sys.path.insert(0, HELPER_PATH)
    from dynamic_credentials import (
        DynamicCredentialError,
        add_surrogate_to_request,
        read_json_response,
    )
except ImportError:
    sys.exit(
        "error: this CLI needs the Muse dynamic_credentials helper at "
        f"{HELPER_PATH} (install this skill on a Muse runtime to use it)"
    )


def call(method: str, path: str, params: dict | None = None,
         payload: dict | None = None) -> dict:
    url = API + path
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        add_surrogate_to_request(req, CREDENTIAL_NAME, allowed_hosts=ALLOWED_HOSTS)
    except DynamicCredentialError as exc:
        sys.exit(f"error: credential problem: {exc}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return read_json_response(resp)
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8", errors="replace"))
            detail = body.get("error", {}).get("detail", body.get("error", str(exc)))
            msg = detail if isinstance(detail, str) else str(exc)
        except Exception:
            msg = str(exc)
        sys.exit(f"error: ynab returned HTTP {exc.code}: {msg}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def cmd_auth(_args):
    result = call("GET", "/budgets")
    budgets = result.get("data", {}).get("budgets", [])
    print(json.dumps({"ok": True, "budgets": len(budgets)}, indent=2))


def cmd_budgets(args):
    result = call("GET", "/budgets")
    budgets = [
        {"id": b["id"], "name": b.get("name"),
         "last_modified_on": b.get("last_modified_on")}
        for b in result.get("data", {}).get("budgets", [])
    ]
    print(json.dumps(budgets, indent=2))


def cmd_accounts(args):
    result = call("GET", f"/budgets/{args.budget}/accounts")
    accounts = [
        {"id": a["id"], "name": a.get("name"), "type": a.get("type"),
         "balance": a.get("balance"), "cleared_balance": a.get("cleared_balance")}
        for a in result.get("data", {}).get("accounts", [])
    ]
    print(json.dumps(accounts, indent=2))


def cmd_transactions(args):
    params = {}
    if args.since_date:
        params["since_date"] = args.since_date
    result = call("GET", f"/budgets/{args.budget}/transactions", params=params)
    txns = [
        {"id": t["id"], "date": t.get("date"), "amount": t.get("amount"),
         "payee_name": t.get("payee_name"), "category_name": t.get("category_name"),
         "memo": t.get("memo")}
        for t in result.get("data", {}).get("transactions", [])
    ]
    print(json.dumps(txns, indent=2))


def cmd_transaction_create(args):
    payload = {"transaction": {
        "account_id": args.account_id,
        "date": args.date,
        "amount": int(round(args.amount * 1000)),
        "cleared": "cleared",
    }}
    if args.payee_name:
        payload["transaction"]["payee_name"] = args.payee_name
    if args.category_id:
        payload["transaction"]["category_id"] = args.category_id
    if args.memo:
        payload["transaction"]["memo"] = args.memo
    result = call("POST", f"/budgets/{args.budget}/transactions", payload=payload)
    txn = result.get("data", {}).get("transaction", {})
    print(json.dumps({"ok": True, "id": txn.get("id"),
                      "date": txn.get("date"), "amount": txn.get("amount")},
                     indent=2))


def cmd_categories(args):
    result = call("GET", f"/budgets/{args.budget}/categories")
    groups = [
        {"name": g.get("name"),
         "categories": [{"id": c["id"], "name": c.get("name"),
                         "budgeted": c.get("budgeted"),
                         "balance": c.get("balance")}
                        for c in g.get("categories", [])]}
        for g in result.get("data", {}).get("category_groups", [])
    ]
    print(json.dumps(groups, indent=2))


def main():
    parser = argparse.ArgumentParser(description="YNAB API CLI (muse-connectors)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth", help="verify the OAuth token")
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("budgets", help="list budgets")
    p.set_defaults(func=cmd_budgets)

    p = sub.add_parser("accounts", help="list accounts and balances")
    p.add_argument("--budget", default="last-used",
                   help="budget ID, or 'last-used' (default)")
    p.set_defaults(func=cmd_accounts)

    p = sub.add_parser("transactions", help="list transactions")
    p.add_argument("--budget", default="last-used")
    p.add_argument("--since-date", default=None, help="YYYY-MM-DD")
    p.set_defaults(func=cmd_transactions)

    p = sub.add_parser("transaction-create",
                       help="record a transaction (confirm first)")
    p.add_argument("--budget", default="last-used")
    p.add_argument("--account-id", required=True)
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--amount", type=float, required=True,
                   help="in budget currency units; negative = outflow, positive = inflow")
    p.add_argument("--payee-name", default=None)
    p.add_argument("--category-id", default=None)
    p.add_argument("--memo", default=None)
    p.set_defaults(func=cmd_transaction_create)

    p = sub.add_parser("categories", help="list category groups and balances")
    p.add_argument("--budget", default="last-used")
    p.set_defaults(func=cmd_categories)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
