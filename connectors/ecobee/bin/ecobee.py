#!/usr/bin/env python3
"""ecobee v1 API CLI for the muse-connectors ecobee skill.

Reads: runtime report (5-minute interval historical data) via
GET /1/runtimeReport.

Writes: temperature holds via POST /1/thermostat with a setHold
function. Holds require an exact --confirm string echoed by the CLI,
on every call, and a token with the smartWrite scope.

Auth: OAuth 2.0 via the PIN authorization flow. The user approves
access through the secure credential flow
(credentials.request_api_access) and the runtime hands this script a
fresh Bearer token via the bundled dynamic_credentials helper. The
real token never touches this script: the runtime swaps the surrogate
on approved egress, only to api.ecobee.com.

Scopes (ecobee's own names, per the official PIN authorization docs):
  smartRead    (reads)
  smartWrite   (holds)

HONESTY NOTES:
- Only two endpoints are implemented, both verified against the
  official ecobee v1 docs. GET /1/thermostatSummary and the GET
  thermostat detail paths are deliberately omitted: they appear in the
  official operations index but the exact path pattern was not
  confirmed from a primary source.
- The setHold param field names (holdType, heatHoldTemp, coolHoldTemp
  in tenths of a degree F) follow the official set-hold docs, but the
  set-hold page fetch failed while building this connector, so they
  are flagged as unverified; the CLI surfaces ecobee's own error
  message if a field differs.
- Nothing here has been verified in a live flow yet.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.ecobee"
ALLOWED_HOSTS = ("api.ecobee.com",)
BASE = "https://api.ecobee.com"
CONNECT_GUIDANCE = (
    "not connected: approve ecobee access via the secure credential flow "
    "(credentials.request_api_access) as `custom.ecobee` (OAuth 2.0, "
    "ecobee PIN flow; request the smartRead scope for reads and smartWrite "
    "for holds), then retry."
)

# Column names verified from the official GET Runtime Report docs page.
# No spaces are allowed in the CSV columns string.
REPORT_COLUMNS = (
    "auxHeat1", "auxHeat2", "auxHeat3",
    "compCool1", "compCool2", "compHeat1", "compHeat2",
    "dehumidifier", "dmOffset", "economizer", "fan", "humidifier",
    "hvacMode", "outdoorHumidity", "outdoorTemp", "sky", "ventilator",
    "wind", "zoneAveTemp", "zoneCalendarEvent", "zoneClimate",
    "zoneCoolTemp", "zoneHeatTemp", "zoneHumidity", "zoneHumidityHigh",
    "zoneHumidityLow", "zoneHvacMode", "zoneOccupancy",
)
MAX_REPORT_DAYS = 31
MAX_REPORT_THERMOSTATS = 25
HOLD_TYPES = ("nextTransition", "indefinite", "holdHours", "dateTime")

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


def error_exit(exc, provider="ecobee"):
    """Exit with the provider's own error message when available."""
    if isinstance(exc, urllib.error.HTTPError):
        try:
            body = json.loads(exc.read().decode("utf-8", errors="replace"))
            status = body.get("status", {})
            msg = status.get("message") or body.get("message") or str(exc)
        except Exception:
            msg = str(exc)
        sys.exit(f"error: {provider} returned HTTP {exc.code}: {msg}")
    sys.exit(f"error: request failed: {exc}")


def authed_request(url: str, data=None, headers: dict | None = None,
                   method: str | None = None) -> urllib.request.Request:
    """Build a request with the OAuth surrogate attached (Bearer)."""
    req = urllib.request.Request(url, data=data,
                                 headers=headers or {}, method=method)
    try:
        add_surrogate_to_request(req, CREDENTIAL_NAME,
                                 allowed_hosts=ALLOWED_HOSTS)
    except DynamicCredentialError as exc:
        if "missing" in str(exc) or "surrogate" in str(exc):
            sys.exit(CONNECT_GUIDANCE)
        sys.exit(f"error: credential problem: {exc}")
    return req


def call(method: str, url: str, payload: dict | None = None) -> dict:
    """JSON call against the ecobee v1 base."""
    data = None
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = authed_request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return read_json_response(resp)
    except Exception as exc:  # HTTPError and network-level failures
        error_exit(exc)


def need_confirm(args, expected: str, effect: str) -> None:
    """Refuse unless --confirm matches the exact effect string."""
    if args.confirm == expected:
        return
    sys.exit(
        f"refusing: {effect}\n"
        f"Re-run with the exact confirmation string:\n"
        f'  --confirm "{expected}"'
    )


def cmd_auth(_args):
    """Verify the credential is provisioned (presence, not a token ping).

    No lightweight ecobee ping endpoint was verified from a primary
    source, so `auth` checks that the surrogate resolves rather than
    burning a real API call; live validity is confirmed on the first
    real request.
    """
    req = urllib.request.Request(f"{BASE}/1/runtimeReport")
    try:
        add_surrogate_to_request(req, CREDENTIAL_NAME,
                                 allowed_hosts=ALLOWED_HOSTS)
    except DynamicCredentialError as exc:
        if "missing" in str(exc) or "surrogate" in str(exc):
            sys.exit(CONNECT_GUIDANCE)
        sys.exit(f"error: credential problem: {exc}")
    print(json.dumps(
        {"ok": True, "credential": CREDENTIAL_NAME,
         "note": "credential present; live token validity is confirmed "
                 "on the first API call"},
        indent=2))


def parse_ymd(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError:
        sys.exit(f"error: date must be YYYY-MM-DD, got {value!r}")


def cmd_runtime_report(args):
    start = parse_ymd(args.start_date)
    end = parse_ymd(args.end_date)
    if end < start:
        sys.exit("error: --end-date must be on or after --start-date")
    days = (end - start).days + 1
    if days > MAX_REPORT_DAYS:
        sys.exit(
            f"error: runtime reports are limited to {MAX_REPORT_DAYS} days "
            f"per request (asked for {days}); page multi-month ranges in "
            f"{MAX_REPORT_DAYS}-day chunks")
    ids = [t.strip() for t in args.thermostat_id.split(",") if t.strip()]
    if not ids:
        sys.exit("error: supply at least one --thermostat-id")
    if len(ids) > MAX_REPORT_THERMOSTATS:
        sys.exit(
            f"error: runtime reports are limited to "
            f"{MAX_REPORT_THERMOSTATS} thermostats per request")
    columns = [c.strip() for c in args.columns.split(",") if c.strip()]
    if not columns:
        sys.exit("error: supply at least one column via --columns")
    bad = [c for c in columns if c not in REPORT_COLUMNS]
    if bad:
        sys.exit(
            f"error: unknown column(s): {', '.join(bad)}. "
            f"Verified columns: {', '.join(REPORT_COLUMNS)}")
    body = {
        "startDate": args.start_date,
        "endDate": args.end_date,
        "columns": ",".join(columns),  # no spaces per the ecobee docs
        "selection": {
            "selectionType": "thermostats",
            "selectionMatch": ",".join(ids),
        },
    }
    if args.start_interval is not None:
        body["startInterval"] = args.start_interval
    if args.end_interval is not None:
        body["endInterval"] = args.end_interval
    if args.include_sensors:
        body["includeSensors"] = True
    url = (f"{BASE}/1/runtimeReport?format=json&body="
           f"{urllib.parse.quote(json.dumps(body), safe='')}")
    result = call("GET", url)
    print(json.dumps(result, indent=2))


def cmd_hold(args):
    temp_f = args.temperature
    tenths = int(round(temp_f * 10))
    temp_param = "heatHoldTemp" if args.mode == "heat" else "coolHoldTemp"
    expected = (f"set hold on thermostat {args.thermostat_id}: "
                f"{args.mode} to {temp_f:g}F ({args.hold_type})")
    need_confirm(
        args, expected,
        f"setting a {args.mode} hold of {temp_f:g}F on thermostat "
        f"{args.thermostat_id} (hold type {args.hold_type}); this changes "
        f"the real thermostat in the house.")
    payload = {
        "selection": {
            "selectionType": "thermostats",
            "selectionMatch": args.thermostat_id,
        },
        "functions": [
            {
                "type": "setHold",
                "params": {
                    "holdType": args.hold_type,
                    temp_param: tenths,
                },
            }
        ],
    }
    result = call("POST", f"{BASE}/1/thermostat", payload)
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="ecobee v1 API CLI (muse-connectors)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth",
                       help="verify the ecobee credential is provisioned")
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("runtime-report",
                       help="5-minute interval historical runtime report")
    p.add_argument("--thermostat-id", required=True,
                   help="thermostat identifier(s); repeat with commas for "
                        "up to 25")
    p.add_argument("--start-date", required=True,
                   help="UTC start date, YYYY-MM-DD")
    p.add_argument("--end-date", required=True,
                   help="UTC end date, YYYY-MM-DD (max 31 days after start)")
    p.add_argument("--columns", required=True,
                   help="CSV of report columns (no spaces), e.g. "
                        '"zoneAveTemp,outdoorTemp,fan,hvacMode"')
    p.add_argument("--start-interval", type=int, default=None,
                   help="5-minute interval 0-287 to begin on (default 0)")
    p.add_argument("--end-interval", type=int, default=None,
                   help="5-minute interval 0-287 to end on (default 287)")
    p.add_argument("--include-sensors", action="store_true",
                   help="include remote sensor runtime data")
    p.set_defaults(func=cmd_runtime_report)

    p = sub.add_parser("hold",
                       help="set a temperature hold (needs --confirm, "
                            "smartWrite scope)")
    p.add_argument("--thermostat-id", required=True,
                   help="thermostat identifier")
    p.add_argument("--temperature", type=float, required=True,
                   help="hold temperature in degrees F")
    p.add_argument("--mode", required=True, choices=("heat", "cool"),
                   help="which setpoint the hold sets")
    p.add_argument("--hold-type", default="nextTransition",
                   choices=HOLD_TYPES,
                   help="how long the hold lasts (default nextTransition)")
    p.add_argument("--confirm", default=None)
    p.set_defaults(func=cmd_hold)

    args = parser.parse_args()
    for interval in ("start_interval", "end_interval"):
        value = getattr(args, interval, None)
        if value is not None and not 0 <= value <= 287:
            sys.exit(f"error: --{interval.replace('_', '-')} must be 0-287")
    args.func(args)


if __name__ == "__main__":
    main()
