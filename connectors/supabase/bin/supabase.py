#!/usr/bin/env python3
"""Minimal Supabase PostgREST CLI for the muse-connectors supabase skill.

Auth: loads the per-user `custom.supabase` credential as a surrogate via the
bundled dynamic_credentials helper, placed in the `apikey` header. The real
key never touches this script: the runtime swaps the surrogate on approved
egress, only to <ref>.supabase.co.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.supabase"

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


def call(args, path: str, params: dict | None = None,
         accept: str | None = None):
    host = f"{args.project_ref}.supabase.co"
    url = f"https://{host}/rest/v1" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {}
    if accept:
        headers["Accept"] = accept
    req = urllib.request.Request(url, headers=headers)
    try:
        add_surrogate_to_request(req, CREDENTIAL_NAME, allowed_hosts=(host,))
    except DynamicCredentialError as exc:
        sys.exit(f"error: credential problem: {exc}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return read_json_response(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        sys.exit(f"error: supabase API returned HTTP {exc.code}: {body}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def cmd_tables(args):
    spec = call(args, "/", accept="application/openapi+json")
    tables = sorted((spec.get("definitions") or {}).keys())
    print(json.dumps(tables, indent=2))


def cmd_query(args):
    table = urllib.parse.quote(args.table, safe="")
    rows = call(args, f"/{table}", params={"select": "*", "limit": args.limit})
    print(json.dumps(rows, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Supabase PostgREST CLI (muse-connectors)")
    parser.add_argument("--project-ref", required=True,
                        help="project ref, the <ref> in https://<ref>.supabase.co")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("tables", help="list tables in the database")
    p.set_defaults(func=cmd_tables)

    p = sub.add_parser("query", help="query rows from a table")
    p.add_argument("--table", required=True)
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_query)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
