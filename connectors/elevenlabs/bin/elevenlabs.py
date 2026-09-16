#!/usr/bin/env python3
"""Minimal ElevenLabs API CLI for the muse-connectors ElevenLabs skill.

Auth: loads the per-user `custom.elevenlabs` credential as a surrogate via
the bundled dynamic_credentials helper. The real key never touches this
script: the runtime swaps the surrogate on approved egress, only to
api.elevenlabs.io. Read-only: no TTS or other quota-consuming calls ship.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.elevenlabs"
ALLOWED_HOSTS = ("api.elevenlabs.io",)
API = "https://api.elevenlabs.io/v1"

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
            detail = json.loads(body).get("detail", {}).get("message", body)
        except Exception:
            detail = str(exc)
        sys.exit(f"error: elevenlabs returned HTTP {exc.code}: {detail}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")
    return result


def cmd_me(_args):
    result = call("/user")
    sub = result.get("subscription") or {}
    print(json.dumps(
        {"tier": sub.get("tier"), "character_count": sub.get("character_count"),
         "character_limit": sub.get("character_limit")},
        indent=2))


def cmd_voices(_args):
    result = call("/voices")
    voices = [
        {"voice_id": v.get("voice_id"), "name": v.get("name"),
         "category": v.get("category")}
        for v in result.get("voices", [])
    ]
    print(json.dumps(voices, indent=2))


def main():
    parser = argparse.ArgumentParser(description="ElevenLabs API CLI (muse-connectors, read-only)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("me", help="subscription tier and character usage")
    p.set_defaults(func=cmd_me)

    p = sub.add_parser("voices", help="list available voices")
    p.set_defaults(func=cmd_voices)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
