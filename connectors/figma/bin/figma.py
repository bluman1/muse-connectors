#!/usr/bin/env python3
"""Minimal Figma REST API CLI for the muse-connectors Figma skill.

Auth: loads the per-user `custom.figma` credential as a surrogate via the
bundled dynamic_credentials helper. The real token never touches this script:
the runtime swaps the surrogate on approved egress, only to api.figma.com.
Read-only by design.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.figma"
ALLOWED_HOSTS = ("api.figma.com",)
API = "https://api.figma.com/v1"

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


def call(path: str) -> dict:
    url = API + path
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
        sys.exit(f"error: figma returned HTTP {exc.code}: {detail}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")
    return result


def cmd_me(_args):
    result = call("/me")
    print(json.dumps(
        {"id": result.get("id"), "handle": result.get("handle"),
         "email": result.get("email")},
        indent=2))


def cmd_file(args):
    # Intentionally metadata-only: the full document payload is huge.
    result = call(f"/files/{args.key}")
    print(json.dumps(
        {"name": result.get("name"), "lastModified": result.get("lastModified"),
         "version": result.get("version"),
         "thumbnailUrl": result.get("thumbnailUrl")},
        indent=2))


def main():
    parser = argparse.ArgumentParser(description="Figma REST API CLI (muse-connectors, read-only)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("me", help="authenticated user")
    p.set_defaults(func=cmd_me)

    p = sub.add_parser("file", help="file metadata (name, lastModified, version, thumbnailUrl)")
    p.add_argument("--key", required=True, help="file key from the Figma URL")
    p.set_defaults(func=cmd_file)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
