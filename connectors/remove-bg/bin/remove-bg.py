#!/usr/bin/env python3
"""Minimal remove.bg API CLI for the muse-connectors remove-bg skill.

Auth: API key loaded as a surrogate for `custom.remove-bg` via the bundled
dynamic_credentials helper, sent as `X-Api-Key: YOUR_API_KEY` (placement
resolved by the helper from the credential config). The real key never
touches this script: the runtime swaps the surrogate on approved egress,
only to api.remove.bg.

The /removebg response is image BINARY, not JSON: `process` saves it to the
--out path and prints the path. Every call burns paid credit, so confirm
before processing.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.remove-bg"
ALLOWED_HOSTS = ("api.remove.bg",)
API = "https://api.remove.bg/v1.0"

try:
    sys.path.insert(0, HELPER_PATH)
    from dynamic_credentials import (
        DynamicCredentialError,
        add_surrogate_to_request,
        read_json_response,
        read_response_body,
    )
except ImportError:
    sys.exit(
        "error: this CLI needs the Muse dynamic_credentials helper at "
        f"{HELPER_PATH} (install this skill on a Muse runtime to use it)"
    )


def credential_error(exc: Exception) -> None:
    sys.exit(
        "error: no stored credential for custom.remove-bg "
        f"({exc}). To connect, ask Muse to connect a remove.bg API key via "
        "the secure credential flow, then retry."
    )


def api_error(exc: urllib.error.HTTPError) -> None:
    try:
        body = json.loads(exc.read().decode("utf-8", errors="replace"))
        errors = body.get("errors") or []
        msg = "; ".join(e.get("title", "") for e in errors) if errors else str(exc)
    except Exception:
        msg = str(exc)
    sys.exit(f"error: remove.bg returned HTTP {exc.code}: {msg}")


def authed_request(url: str, data: bytes | None, content_type: str | None):
    headers: dict[str, str] = {"Accept": "application/json"}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        add_surrogate_to_request(req, CREDENTIAL_NAME, allowed_hosts=ALLOWED_HOSTS)
    except (DynamicCredentialError, OSError) as exc:
        credential_error(exc)
    return req


def cmd_auth(_args):
    cmd_account(_args)


def cmd_account(_args):
    req = authed_request(API + "/account", None, None)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = read_json_response(resp)
    except urllib.error.HTTPError as exc:
        api_error(exc)
    except Exception as exc:
        sys.exit(f"error: request failed: {exc}")
    data = result.get("data", {})
    attrs = data.get("attributes", {})
    print(json.dumps({"ok": True, "credits": (attrs.get("credits") or {}).get("total")}, indent=2))


def encode_multipart(fields: dict, files: dict) -> tuple[bytes, str]:
    """Build a multipart/form-data body. files: name -> (filename, bytes, mime)."""
    boundary = uuid.uuid4().hex
    parts: list[bytes] = []
    for name, value in fields.items():
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"'
            f"\r\n\r\n{value}\r\n".encode("utf-8")
        )
    for name, (filename, content, mime) in files.items():
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; '
            f'filename="{filename}"\r\nContent-Type: {mime}\r\n\r\n'.encode("utf-8")
            + content + b"\r\n"
        )
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def cmd_process(args):
    fields = {"size": args.size, "type": args.type}
    files: dict = {}
    if args.file:
        try:
            with open(args.file, "rb") as fh:
                content = fh.read()
        except OSError as exc:
            sys.exit(f"error: cannot read file: {exc}")
        files["image_file"] = (args.file.split("/")[-1], content, "application/octet-stream")
    else:
        fields["image_url"] = args.url
    body, ctype = encode_multipart(fields, files)
    req = authed_request(API + "/removebg", body, ctype)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            image = read_response_body(resp)
    except urllib.error.HTTPError as exc:
        api_error(exc)
    except Exception as exc:
        sys.exit(f"error: request failed: {exc}")
    try:
        with open(args.out, "wb") as fh:
            fh.write(image)
    except OSError as exc:
        sys.exit(f"error: cannot write file: {exc}")
    print(json.dumps({"saved_to": args.out, "bytes": len(image)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description="remove.bg API CLI (muse-connectors)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth", help="verify the connection (shows remaining credits)")
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("account", help="credit balance and account info")
    p.set_defaults(func=cmd_account)

    p = sub.add_parser("process", help="remove the background from an image")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="local image file path")
    group.add_argument("--url", help="image URL to process")
    p.add_argument("--out", required=True, help="local path to save the result PNG")
    p.add_argument("--size", default="auto",
                   help="preview, regular, hd, 4k, auto (default: auto)")
    p.add_argument("--type", default="auto",
                   help="auto, person, product, car (default: auto)")
    p.set_defaults(func=cmd_process)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
