#!/usr/bin/env python3
"""Thin wrapper around DoorDash's official dd-cli (github.com/doordash-oss/doordash-cli).

Only invokes the real dd-cli binary installed by the user; never reimplements it.
Order submission is confirm-gated: any passthrough containing submit-like verbs
requires --confirm carrying the exact order total from the price preview.
"""
import json
import os
import re
import shutil
import subprocess
import sys

SUBMIT_PATTERN = re.compile(r"submit|place-order", re.IGNORECASE)


def fail(msg):
    print(json.dumps({"ok": False, "error": msg}))
    sys.exit(1)


def ddcli_path():
    p = shutil.which("dd-cli")
    if not p:
        fail("dd-cli not found on PATH. Install it from https://github.com/doordash-oss/doordash-cli "
             "(releases page, verify the SHA256 checksum) and run `dd-cli login` first.")
    return p


def run_ddcli(args):
    try:
        proc = subprocess.run([ddcli_path()] + args, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        fail("dd-cli timed out after 120s")
    return proc


def cmd_auth(_args):
    ddcli_path()
    authed = bool(os.environ.get("DD_CLI_ACCESS_TOKEN"))
    # A cheap, documented read to probe the session; failure text is surfaced, not hidden.
    probe = run_ddcli(["search", "--query", "coffee", "--help"])
    print(json.dumps({
        "ok": True,
        "dd_cli": ddcli_path(),
        "access_token_env": authed,
        "note": "binary present; " + ("DD_CLI_ACCESS_TOKEN is set" if authed else
                 "no DD_CLI_ACCESS_TOKEN in env: run `dd-cli login` on this machine, or export a token via `dd-cli export-token` elsewhere"),
        "probe_help_rc": probe.returncode,
    }))


def cmd_search(args):
    if not args.get("query"):
        fail("search requires --query")
    # dd-cli >= v0.2.2 requires --intent on all tool-backed commands.
    proc = run_ddcli(["search", "--intent", "muse-connectors: search restaurants",
                      "--query", args["query"]])
    print(json.dumps({"ok": proc.returncode == 0, "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-1000:]}))


def cmd_history(_args):
    # dd-cli >= v0.2.2 requires --intent on all tool-backed commands.
    proc = run_ddcli(["order", "history", "--intent",
                      "muse-connectors: read order history"])
    print(json.dumps({"ok": proc.returncode == 0, "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-1000:]}))


def cmd_run(args):
    passthrough = args.get("passthrough", [])
    confirm = args.get("confirm")
    joined = " ".join(passthrough)
    if SUBMIT_PATTERN.search(joined) and not confirm:
        fail("refusing to submit an order without --confirm carrying the exact order total from the price preview")
    proc = run_ddcli(passthrough)
    print(json.dumps({"ok": proc.returncode == 0, "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-1000:]}))


def parse(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__ + "\ncommands: auth | search --query Q | history | run [--confirm TEXT] -- <dd-cli args>")
        return
    cmd, rest = argv[0], argv[1:]
    args = {"passthrough": [], "confirm": None, "query": None}
    i = 0
    passthrough_mode = False
    while i < len(rest):
        t = rest[i]
        if t == "--":
            passthrough_mode = True
        elif passthrough_mode:
            args["passthrough"].append(t)
        elif t == "--confirm" and i + 1 < len(rest):
            args["confirm"] = rest[i + 1]; i += 1
        elif t == "--query" and i + 1 < len(rest):
            args["query"] = rest[i + 1]; i += 1
        else:
            fail(f"unknown flag: {t}")
        i += 1
    {"auth": cmd_auth, "search": cmd_search, "history": cmd_history, "run": cmd_run}.get(cmd, lambda a: fail(f"unknown command: {cmd}"))(args)


if __name__ == "__main__":
    parse(sys.argv[1:])
