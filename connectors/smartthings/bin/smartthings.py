#!/usr/bin/env python3
"""Minimal Samsung SmartThings REST API CLI for the muse-connectors skill.

Auth: OAuth 2.0 access token, stored as the per-user `custom.smartthings`
credential and loaded as a surrogate via the bundled dynamic_credentials
helper. The real token never touches this script: the runtime swaps the
surrogate on approved egress, only to api.smartthings.com.

Physical-world safety: lock/unlock and garage open/close are HIGH actuations
and require --confirm "<exact physical effect>" on every run. Switches,
dimmers, thermostats and sirens are MEDIUM: first use per device needs
--confirm, then proceeds (confirmations are recorded locally).
Curtain/window-shade moves are LOW: they proceed with a logged notice.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.smartthings"
ALLOWED_HOSTS = ("api.smartthings.com",)
API = "https://api.smartthings.com/v1"
CONFIRM_FILE = os.path.expanduser("~/.config/muse-connectors/smartthings/confirmed.json")

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


# ---------------------------------------------------------------------------
# Physical-world confirmation gating
# ---------------------------------------------------------------------------

def load_confirmed() -> set:
    try:
        with open(CONFIRM_FILE, encoding="utf-8") as fh:
            data = json.load(fh)
        return set(data) if isinstance(data, list) else set()
    except (OSError, json.JSONDecodeError):
        return set()


def save_confirmed(confirmed: set) -> None:
    os.makedirs(os.path.dirname(CONFIRM_FILE), exist_ok=True)
    with open(CONFIRM_FILE, "w", encoding="utf-8") as fh:
        json.dump(sorted(confirmed), fh, indent=2)


def require_high(confirm: str | None, effect: str) -> None:
    """HIGH actuations (unlock, garage open/close) need --confirm every run."""
    if not confirm or len(confirm.strip()) < 3:
        sys.exit(
            "error: HIGH-RISK actuation blocked. This command would: "
            f"{effect}. Re-run with --confirm \"<exact physical effect>\" "
            f"naming it, e.g. --confirm \"{effect}\"."
        )
    print(f"notice: HIGH actuation confirmed: {confirm.strip()}", file=sys.stderr)


def require_medium(device: str, action_class: str, confirm: str | None,
                   effect: str) -> None:
    """MEDIUM actuations confirm on first use per device, then proceed."""
    confirmed = load_confirmed()
    key = f"{device}:{action_class}"
    if key in confirmed:
        return
    if not confirm or len(confirm.strip()) < 3:
        sys.exit(
            "error: first MEDIUM actuation on this device is confirmation-gated. "
            f"This command would: {effect}. Re-run with --confirm "
            "\"<exact physical effect>\"; later runs on this device proceed "
            "without re-confirming."
        )
    confirmed.add(key)
    save_confirmed(confirmed)
    print(
        f"notice: MEDIUM actuation confirmed and recorded for device "
        f"{device} ({action_class}); future runs on it proceed without "
        f"re-confirming. Said: {confirm.strip()}",
        file=sys.stderr,
    )


def low_notice(effect: str) -> None:
    print(f"notice: LOW actuation proceeding: {effect}", file=sys.stderr)


# ---------------------------------------------------------------------------
# API plumbing
# ---------------------------------------------------------------------------

def call(method: str, path: str, payload: dict | None = None) -> dict:
    url = API + path
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        add_surrogate_to_request(req, CREDENTIAL_NAME, allowed_hosts=ALLOWED_HOSTS)
    except DynamicCredentialError:
        print(
            "not connected: no custom.smartthings credential is stored.\n"
            "Collect it via the secure credential flow "
            "(credentials.request_api_access) as an OAuth 2.0 access token "
            "for the SmartThings app, then retry. "
            "See this skill's SKILL.md Auth section for the app setup.",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return read_json_response(resp)
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8", errors="replace"))
            msg = body.get("message") or body.get("error") or str(exc)
        except Exception:
            msg = str(exc)
        sys.exit(f"error: smartthings returned HTTP {exc.code}: {msg}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def parse_value(text: str):
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return text


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_auth(_args):
    result = call("GET", "/locations")
    locations = result.get("items", [])
    print(json.dumps({
        "ok": True,
        "locations": [{"name": loc.get("name"), "locationId": loc.get("locationId")}
                      for loc in locations],
    }, indent=2))


def cmd_locations(_args):
    result = call("GET", "/locations")
    items = result.get("items", [])
    print(json.dumps([{"name": l.get("name"), "locationId": l.get("locationId"),
                       "countryCode": l.get("countryCode")} for l in items], indent=2))


def cmd_devices(args):
    params = {"max": args.limit}
    result = call("GET", "/devices?" + urllib.parse.urlencode(params))
    items = result.get("items", [])
    print(json.dumps([
        {"deviceId": d.get("deviceId"), "name": d.get("name"),
         "label": d.get("label"), "deviceTypeName": d.get("deviceTypeName"),
         "capabilities": [c.get("id") for c in d.get("components", [{}])[0].get("capabilities", [])]}
        for d in items
    ], indent=2))


def cmd_status(args):
    result = call("GET", f"/devices/{args.id}/status")
    print(json.dumps(result, indent=2))


def cmd_command(args):
    capability = args.capability
    command = args.command
    arguments = [parse_value(v) for v in args.arg]

    # --- actuation-risk grading ---
    if capability == "lock" and command == "unlock":
        require_high(args.confirm, f"unlock the lock device {args.id}")
    elif capability in ("garageDoorControl", "doorControl") and command in ("open", "close"):
        require_high(args.confirm, f"{command} the garage/door device {args.id}")
    elif capability in ("windowShade", "windowShadeLevel", "windowShadePreset"):
        low_notice(f"move the window shade/curtain device {args.id} ({command})")
    else:
        require_medium(args.id, capability, args.confirm,
                       f"send {capability}.{command} to device {args.id}")

    payload = {"commands": [{
        "component": args.component,
        "capability": capability,
        "command": command,
        "arguments": arguments,
    }]}
    result = call("POST", f"/devices/{args.id}/commands", payload)
    print(json.dumps({"ok": True, "results": result.get("results", [])}, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="SmartThings API CLI (muse-connectors). "
                    "Commands drive real hardware: HIGH actuations (unlock, "
                    "garage open/close) always need --confirm; MEDIUM "
                    "actuations need --confirm on first use per device.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth", help="status check: list locations, verify token")
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("locations", help="list locations")
    p.set_defaults(func=cmd_locations)

    p = sub.add_parser("devices", help="list devices")
    p.add_argument("--limit", type=int, default=50, help="max devices (default 50)")
    p.set_defaults(func=cmd_devices)

    p = sub.add_parser("status", help="read full status of a device")
    p.add_argument("--id", required=True, help="deviceId")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("command", help="issue a capability command to a device "
                                       "(confirmation-gated by risk grade)")
    p.add_argument("--id", required=True, help="deviceId")
    p.add_argument("--component", default="main")
    p.add_argument("--capability", required=True,
                   help="e.g. lock, switch, switchLevel, thermostatMode, "
                        "thermostatCoolingSetpoint, alarm, garageDoorControl, "
                        "windowShadeLevel")
    p.add_argument("--command", required=True,
                   help="e.g. lock, unlock, on, off, setLevel, setThermostatMode, "
                        "open, close")
    p.add_argument("--arg", action="append", default=[],
                   help="command argument value (repeatable; JSON-parsed, "
                        "e.g. --arg 72 or --arg '\"heat\"')")
    p.add_argument("--confirm",
                   help="REQUIRED for HIGH actuations (lock unlock, garage "
                        "open/close) every run, and for MEDIUM actuations on "
                        "first use per device. Must name the exact physical "
                        "effect, e.g. --confirm \"unlock front door deadbolt\".")
    p.set_defaults(func=cmd_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
