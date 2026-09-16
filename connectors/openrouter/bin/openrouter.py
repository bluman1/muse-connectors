#!/usr/bin/env python3
"""Minimal OpenRouter API CLI for the muse-connectors openrouter skill.

Auth: loads the per-user `custom.openrouter` credential as a surrogate via the
bundled dynamic_credentials helper. The real key never touches this script:
the runtime swaps the surrogate on approved egress, only to openrouter.ai.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.openrouter"
ALLOWED_HOSTS = ("openrouter.ai",)
API = "https://openrouter.ai/api/v1"

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
            return read_json_response(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        sys.exit(f"error: openrouter API returned HTTP {exc.code}: {body}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def cmd_models(args):
    result = call("/models")
    models = result.get("data", [])
    if args.filter:
        needle = args.filter.lower()
        models = [m for m in models if needle in m.get("id", "").lower()]
    out = [{"id": m.get("id"), "name": m.get("name"),
            "prompt_price": str((m.get("pricing") or {}).get("prompt", ""))[:40]}
           for m in models[: args.limit]]
    print(json.dumps(out, indent=2))


def cmd_key(_args):
    key = call("/auth/key").get("data", {})
    print(json.dumps(
        {"label": key.get("label"), "usage": key.get("usage"),
         "limit": key.get("limit")},
        indent=2,
    ))


def main():
    parser = argparse.ArgumentParser(description="OpenRouter API CLI (muse-connectors)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("models", help="model catalog with prompt pricing")
    p.add_argument("--filter", default="", help="substring filter on model id")
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(func=cmd_models)

    p = sub.add_parser("key", help="your key's label, usage, limit")
    p.set_defaults(func=cmd_key)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
