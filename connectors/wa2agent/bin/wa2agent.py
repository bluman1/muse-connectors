#!/usr/bin/env python3
"""Minimal wa2agent MCP CLI for the muse-connectors wa2agent skill.

Auth: loads the per-user `custom.wa2agent` credential (the vault's MCP access
key) as a surrogate via the bundled dynamic_credentials helper. The real key
never touches this script: the runtime swaps the surrogate on approved egress,
only to the user's own vault host (taken from --vault).

Read-only: wa2agent has no send or settings tools. Message text arrives
encrypted; open the returned reading link and type the key from the user's
saved note. Never pass that encryption key to this script.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.wa2agent"

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


def vault_host(vault: str) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(vault if "://" in vault else "https://" + vault)
    host = parsed.hostname or ""
    if parsed.scheme not in ("https", "") or not (host.startswith("vault-") and host.endswith(".wa2agent.link")):
        sys.exit("error: --vault must be your vault address, e.g. https://vault-abc1234.wa2agent.link")
    return "https://" + host, host


def call(vault: str, tool: str, arguments: dict) -> dict:
    base, host = vault_host(vault)
    body = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool, "arguments": arguments}}
    req = urllib.request.Request(
        base + "/mcp", data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    try:
        add_surrogate_to_request(req, CREDENTIAL_NAME, allowed_hosts=(host,))
    except DynamicCredentialError as exc:
        sys.exit(f"error: credential problem: {exc}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            reply = read_json_response(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            sys.exit("error: the vault rejected the access key (HTTP 401); create a new one under Connect your agent")
        sys.exit(f"error: wa2agent returned HTTP {exc.code}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")
    if "error" in reply:
        sys.exit(f"error: {reply['error'].get('message', 'MCP error')}")
    result = reply.get("result", {})
    if result.get("isError"):
        text = " ".join(c.get("text", "") for c in result.get("content", []))
        sys.exit(f"error: {text or 'tool error'}")
    if "structuredContent" in result:
        return result["structuredContent"]
    return json.loads(result["content"][0]["text"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Read shared WhatsApp chats from a wa2agent vault (read-only).")
    parser.add_argument("--vault", required=True, help="vault address, e.g. https://vault-abc1234.wa2agent.link")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("auth", help="check that the access key works")
    chats = sub.add_parser("chats", help="list shared chats")
    chats.add_argument("--kind", choices=["group", "dm"])
    chats.add_argument("--limit", type=int)
    chats.add_argument("--cursor")
    msgs = sub.add_parser("messages", help="read one shared chat")
    msgs.add_argument("--chat", required=True, help="chat jid from `chats`")
    msgs.add_argument("--after", type=int, help="Unix seconds; oldest first after this time")
    msgs.add_argument("--limit", type=int)
    msgs.add_argument("--cursor")
    args = parser.parse_args()

    if args.command == "auth":
        out = call(args.vault, "list_chats", {"limit": 1})
        print(json.dumps({"ok": True, "chats_visible": len(out.get("chats", []))}))
        return
    if args.command == "chats":
        params = {k: v for k, v in {"kind": args.kind, "limit": args.limit, "cursor": args.cursor}.items() if v is not None}
        print(json.dumps(call(args.vault, "list_chats", params), indent=2))
        return
    params = {k: v for k, v in {"chat_id": args.chat, "after": args.after, "limit": args.limit, "cursor": args.cursor}.items() if v is not None}
    print(json.dumps(call(args.vault, "get_messages", params), indent=2))


if __name__ == "__main__":
    main()
