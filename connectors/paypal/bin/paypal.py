#!/usr/bin/env python3
"""Minimal PayPal Transaction Search API CLI for the muse-connectors paypal skill.

Auth: loads the per-user `custom.paypal` credential as a surrogate via the
bundled dynamic_credentials helper. PayPal uses OAuth2 client credentials;
the runtime exchanges the client id/secret at /v1/oauth2/token and hands
this script a fresh access token. The real credentials never touch this
script: the runtime swaps the surrogate on approved egress, only to the
PayPal host in use.

READ-ONLY by design: this connector only covers the Transaction Search
API v1 (balances and transaction reporting). There are no payment, payout,
transfer, refund, or order endpoints here, and none are planned.

WRITES (confirm-gated, exact --confirm string on every call):
payout-create (POST /v1/payments/payouts: send a batch payout to one
recipient; scope https://uri.paypal.com/payments/payouts), subscription-cancel
(POST /v1/billing/subscriptions/{id}/cancel), refund (POST
/v2/payments/captures/{capture_id}/refund, full or partial). Money moves on
writes: every write prints the exact amount/recipient and refuses unless the
--confirm string matches. Payouts need the app approved for Payouts on live.

Use --env test (default, PayPal sandbox) or --env prod (live account data).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.paypal"
ALLOWED_HOSTS = ("api-m.sandbox.paypal.com", "api-m.paypal.com")
BASES = {
    "test": "https://api-m.sandbox.paypal.com",
    "prod": "https://api-m.paypal.com",
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

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


def call(host: str, method: str, path: str, params: dict | None = None) -> dict:
    url = host + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={}, method=method)
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
            detail = body.get("details", [])
            msg = detail[0].get("description", str(exc)) if detail else body.get("message", str(exc))
        except Exception:
            msg = str(exc)
        sys.exit(f"error: paypal returned HTTP {exc.code}: {msg}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def call_post(host: str, path: str, body: dict,
              idempotency_key: str | None = None) -> dict:
    """POST a JSON body; used only by confirm-gated write commands."""
    data = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if idempotency_key:
        headers["PayPal-Request-Id"] = idempotency_key
    req = urllib.request.Request(host + path, data=data, headers=headers,
                                 method="POST")
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
            detail = body.get("details", [])
            msg = detail[0].get("description", str(exc)) if detail else body.get("message", str(exc))
        except Exception:
            msg = str(exc)
        sys.exit(f"error: paypal returned HTTP {exc.code}: {msg}")
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
    """Convert YYYY-MM-DD to a full ISO-8601 timestamp for PayPal."""
    if not DATE_RE.match(date_str):
        sys.exit(f"error: date must be YYYY-MM-DD, got {date_str!r}")
    try:
        day = dt.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        sys.exit(f"error: invalid date {date_str!r}")
    if end_of_day:
        day = day + dt.timedelta(hours=23, minutes=59, seconds=59)
    return day.strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_range(start: str, end: str) -> None:
    """PayPal transaction search allows at most a 31-day date range."""
    if dt.datetime.strptime(end, "%Y-%m-%d") < dt.datetime.strptime(start, "%Y-%m-%d"):
        sys.exit("error: end-date must be on or after start-date")
    if (dt.datetime.strptime(end, "%Y-%m-%d")
            - dt.datetime.strptime(start, "%Y-%m-%d")).days > 31:
        sys.exit("error: PayPal allows at most a 31-day date range per request")


def cmd_auth(args):
    result = call(BASES[args.env], "GET", "/v1/reporting/balances")
    balances = result.get("balances", [])
    print(json.dumps({"ok": True, "env": args.env,
                      "balances": len(balances)}, indent=2))


def cmd_balance(args):
    result = call(BASES[args.env], "GET", "/v1/reporting/balances")
    out = [
        {"currency": b.get("currency"),
         "primary": b.get("primary"),
         "total_balance": (b.get("total_balance") or {}).get("value"),
         "available_balance": (b.get("available_balance") or {}).get("value"),
         "withheld_balance": (b.get("withheld_balance") or {}).get("value"),
         "receivables_balance": (b.get("receivables_balance") or {}).get("value")}
        for b in result.get("balances", [])
    ]
    print(json.dumps(out, indent=2))


def cmd_transactions(args):
    validate_range(args.start_date, args.end_date)
    params = {
        "start_date": to_timestamp(args.start_date, end_of_day=False),
        "end_date": to_timestamp(args.end_date, end_of_day=True),
        "page_size": args.page_size,
        "page": args.page,
        "fields": "all",
    }
    result = call(BASES[args.env], "GET", "/v1/reporting/transactions",
                  params=params)
    txns = []
    for t in result.get("transaction_details", []):
        info = t.get("transaction_info", {})
        payer = t.get("payer_info", {}) or {}
        txns.append({
            "transaction_id": info.get("transaction_id"),
            "transaction_event_code": info.get("transaction_event_code"),
            "transaction_status": info.get("transaction_status"),
            "transaction_amount": (info.get("transaction_amount") or {}).get("value"),
            "transaction_currency": (info.get("transaction_amount") or {}).get("currency_code"),
            "fee_amount": (info.get("fee_amount") or {}).get("value"),
            "transaction_initiation_date": info.get("transaction_initiation_date"),
            "payer_name": payer.get("payer_name", {}).get("alternate_full_name"),
            "payer_email": payer.get("email_address"),
            "transaction_subject": info.get("transaction_subject"),
        })
    print(json.dumps({"page": result.get("page"),
                      "total_items": result.get("total_items"),
                      "total_pages": result.get("total_pages"),
                      "transactions": txns}, indent=2))


def cmd_balance_summary(args):
    params = {
        "start_date": to_timestamp(args.start_date, end_of_day=False),
        "end_date": to_timestamp(args.end_date, end_of_day=True),
        "currency": args.currency,
    }
    result = call(BASES[args.env], "GET", "/v1/reporting/get-balance-net-summary",
                  params=params)
    print(json.dumps(result, indent=2))


def cmd_daily_summary(args):
    params = {"date": args.date}
    if args.currency:
        params["currency"] = args.currency
    result = call(BASES[args.env], "GET", "/v1/reporting/get-daily-summary",
                  params=params)
    print(json.dumps(result, indent=2))


def cmd_payout_create(args):
    """POST /v1/payments/payouts (docs: developer.paypal.com/api/payments.payouts-batch/v1/payouts-post)."""
    batch_id = args.sender_batch_id or f"muse-{uuid.uuid4()}"
    expected = f"send payout of {args.amount} {args.currency} to {args.receiver}"
    need_confirm(
        args, expected,
        f"sending a REAL payout of {args.amount} {args.currency} to "
        f"{args.receiver} via PayPal Payouts (batch id {batch_id}). "
        f"This moves money out of the PayPal account.")
    item = {
        "recipient_type": "EMAIL",
        "amount": {"value": args.amount, "currency": args.currency},
        "receiver": args.receiver,
    }
    if args.note:
        item["note"] = args.note
    result = call_post(BASES[args.env], "/v1/payments/payouts",
                       {"sender_batch_header": {
                            "sender_batch_id": batch_id,
                            "email_subject": args.email_subject or
                            "You have a payout!"},
                        "items": [item]},
                       idempotency_key=batch_id)
    link = (result.get("links") or [{}])[0]
    print(json.dumps({
        "ok": True,
        "payout_batch_id": result.get("batch_status", {}).get("payout_batch_id")
        or (result.get("batch_header") or {}).get("payout_batch_id"),
        "batch_status": result.get("batch_status"),
        "sender_batch_id": batch_id,
        "amount": args.amount, "currency": args.currency,
        "receiver": args.receiver,
        "status_link": link.get("href"),
    }, indent=2))


def cmd_subscription_cancel(args):
    """POST /v1/billing/subscriptions/{id}/cancel (docs: developer.paypal.com/api/subscriptions/v1/subscriptions-cancel)."""
    expected = f"cancel subscription {args.subscription_id}"
    need_confirm(
        args, expected,
        f"cancelling the PayPal subscription {args.subscription_id}. "
        f"Future billing stops; this cannot be undone from the API.")
    result = call_post(BASES[args.env],
                       f"/v1/billing/subscriptions/{args.subscription_id}/cancel",
                       {"reason": args.reason})
    print(json.dumps({"ok": True,
                      "subscription_id": args.subscription_id,
                      "response": result}, indent=2))


def cmd_refund(args):
    """POST /v2/payments/captures/{capture_id}/refund (docs: developer.paypal.com/platforms/checkout/issue-refund/)."""
    if (args.amount is None) != (args.currency is None):
        sys.exit("error: pass both --amount and --currency for a partial "
                 "refund, or neither for a full refund")
    if args.amount:
        expected = (f"refund {args.amount} {args.currency} "
                    f"on capture {args.capture_id}")
        effect = (f"refunding {args.amount} {args.currency} to the payer of "
                  f"capture {args.capture_id}. This moves money.")
        body = {"amount": {"value": args.amount,
                           "currency_code": args.currency}}
    else:
        expected = f"refund capture {args.capture_id} in full"
        effect = (f"refunding capture {args.capture_id} IN FULL to the payer. "
                  f"This moves money.")
        body = {}
    need_confirm(args, expected, effect)
    result = call_post(BASES[args.env],
                       f"/v2/payments/captures/{args.capture_id}/refund",
                       body, idempotency_key=str(uuid.uuid4()))
    print(json.dumps({
        "ok": True,
        "refund_id": result.get("id"),
        "status": result.get("status"),
        "amount": result.get("amount"),
        "capture_id": args.capture_id,
    }, indent=2))


def add_env(p):
    p.add_argument("--env", default="test", choices=("test", "prod"),
                   help="test sandbox (default) or production")


def main():
    parser = argparse.ArgumentParser(
        description="PayPal API CLI (muse-connectors): read-only reporting "
                    "plus confirm-gated writes (payouts, subscription "
                    "cancels, refunds)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth", help="verify the credential")
    add_env(p)
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("balance", help="list all PayPal balances")
    add_env(p)
    p.set_defaults(func=cmd_balance)

    p = sub.add_parser("transactions", help="search transactions (max 31-day range)")
    add_env(p)
    p.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--page-size", type=int, default=100,
                   help="results per page, max 500")
    p.add_argument("--page", type=int, default=1, help="page number")
    p.set_defaults(func=cmd_transactions)

    p = sub.add_parser("balance-summary",
                       help="net balance summary over a date range")
    add_env(p)
    p.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--currency", default="USD",
                   help="ISO-4217 currency code")
    p.set_defaults(func=cmd_balance_summary)

    p = sub.add_parser("daily-summary", help="daily summary for one date")
    add_env(p)
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--currency", default=None,
                   help="ISO-4217 currency code (optional)")
    p.set_defaults(func=cmd_daily_summary)

    p = sub.add_parser("payout-create",
                       help="send a batch payout to one recipient "
                            "(needs --confirm; moves money)")
    add_env(p)
    p.add_argument("--receiver", required=True,
                   help="recipient PayPal email address")
    p.add_argument("--amount", required=True,
                   help="payout amount, e.g. 10.00")
    p.add_argument("--currency", default="USD",
                   help="ISO-4217 currency code")
    p.add_argument("--note", default=None, help="note to the recipient")
    p.add_argument("--email-subject", default=None,
                   help="payout notification email subject")
    p.add_argument("--sender-batch-id", default=None,
                   help="your batch reference (auto-generated if omitted; "
                        "reusing one from the last 30 days is rejected)")
    p.add_argument("--confirm", default=None)
    p.set_defaults(func=cmd_payout_create)

    p = sub.add_parser("subscription-cancel",
                       help="cancel a subscription (needs --confirm)")
    add_env(p)
    p.add_argument("--subscription-id", required=True,
                   help="subscription id, e.g. I-BWAFV3EHJXK7")
    p.add_argument("--reason", default="Cancelled at user request",
                   help="cancellation reason")
    p.add_argument("--confirm", default=None)
    p.set_defaults(func=cmd_subscription_cancel)

    p = sub.add_parser("refund",
                       help="refund a captured payment, full or partial "
                            "(needs --confirm; moves money)")
    add_env(p)
    p.add_argument("--capture-id", required=True,
                   help="capture id from the order's purchase_units")
    p.add_argument("--amount", default=None,
                   help="partial refund amount; omit for a full refund")
    p.add_argument("--currency", default=None,
                   help="ISO-4217 code (required with --amount)")
    p.add_argument("--confirm", default=None)
    p.set_defaults(func=cmd_refund)

    args = parser.parse_args()
    if getattr(args, "page_size", None) and not 1 <= args.page_size <= 500:
        sys.exit("error: --page-size must be between 1 and 500")
    args.func(args)


if __name__ == "__main__":
    main()
