#!/usr/bin/env python3
"""Minimal Sentry API CLI for the muse-connectors sentry skill.

Auth: loads the per-user `custom.sentry` credential as a surrogate via the
bundled dynamic_credentials helper. The real token never touches this script:
the runtime swaps the surrogate on approved egress, only to sentry.io.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.sentry"
ALLOWED_HOSTS = ("sentry.io",)
API = "https://sentry.io/api/0"

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


def call(path: str, params: dict | None = None):
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
            return read_json_response(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        sys.exit(f"error: sentry API returned HTTP {exc.code}: {body}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def cmd_orgs(_args):
    orgs = call("/organizations/")
    out = [{"slug": o.get("slug"), "name": o.get("name")} for o in orgs]
    print(json.dumps(out, indent=2))


def cmd_projects(args):
    org = urllib.parse.quote(args.org, safe="")
    projects = call(f"/organizations/{org}/projects/")
    out = [{"slug": p.get("slug"), "name": p.get("name"), "platform": p.get("platform")}
           for p in projects]
    print(json.dumps(out, indent=2))


def cmd_issues(args):
    org = urllib.parse.quote(args.org, safe="")
    issues = call(f"/organizations/{org}/issues/", params={
        "query": args.query, "sort": "freq",
        "statsPeriod": args.period, "limit": args.limit})
    out = [{"id": i.get("id"), "title": i.get("title"),
            "level": i.get("level"), "count": i.get("count")}
           for i in issues]
    print(json.dumps(out, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Sentry API CLI (muse-connectors)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("orgs", help="your organizations")
    p.set_defaults(func=cmd_orgs)

    p = sub.add_parser("projects", help="projects in an org")
    p.add_argument("--org", required=True, help="organization slug")
    p.set_defaults(func=cmd_projects)

    p = sub.add_parser("issues", help="unresolved issues, last 24h, by frequency")
    p.add_argument("--org", required=True, help="organization slug")
    p.add_argument("--query", default="is:unresolved",
                   help="Sentry search syntax (default: is:unresolved)")
    p.add_argument("--period", default="24h",
                   help="stats window, e.g. 1h, 24h, 14d")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_issues)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
