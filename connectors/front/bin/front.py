#!/usr/bin/env python3
"""Minimal Front Core API CLI for the muse-connectors Front skill.

Auth: loads the per-user `custom.front` credential as a surrogate via the
bundled dynamic_credentials helper. The real token never touches this script:
the runtime swaps the surrogate on approved egress, only to api2.frontapp.com.
Read-only by design.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.front"
ALLOWED_HOSTS = ("api2.frontapp.com",)
API = "https://api2.frontapp.com"

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


def call(path: str, params: dict | None = None) -> dict:
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    try:
        add_surrogate_to_request(req, CREDENTIAL_NAME, allowed_hosts=ALLOWED_HOSTS)
    except DynamicCredentialError as exc:
        sys.exit(f"error: credential problem: {exc}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = read_json_response(resp)
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8", errors="replace")
            detail = json.loads(body).get("message", body)
        except Exception:
            detail = str(exc)
        sys.exit(f"error: front returned HTTP {exc.code}: {detail}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")
    return result


def cmd_inboxes(_args):
    result = call("/inboxes")
    inboxes = [
        {"id": i.get("id"), "name": i.get("name"), "address": i.get("address")}
        for i in result.get("_results", [])
    ]
    print(json.dumps(inboxes, indent=2))


def cmd_conversations(args):
    result = call(f"/inboxes/{args.inbox}/conversations", params={"limit": args.limit})
    convs = [
        {"id": c.get("id"), "subject": c.get("subject"), "status": c.get("status"),
         "created_at": c.get("created_at")}
        for c in result.get("_results", [])
    ]
    print(json.dumps(convs, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Front Core API CLI (muse-connectors, read-only)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("inboxes", help="list inboxes")
    p.set_defaults(func=cmd_inboxes)

    p = sub.add_parser("conversations", help="recent conversations in an inbox")
    p.add_argument("--inbox", required=True, help="inbox id, e.g. inb_123")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_conversations)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
