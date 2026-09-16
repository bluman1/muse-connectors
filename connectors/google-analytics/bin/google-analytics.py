#!/usr/bin/env python3
"""Google Analytics Data API v1 (GA4) CLI for the muse-connectors
google-analytics skill.

Read-only reporting: standard reports, realtime reports, and batch
reports over GA4 properties.

Auth: OAuth 2.0 (or a service account added to the GA4 property with
viewer rights). The user approves access through the secure credential
flow (credentials.request_api_access) and the runtime hands this script
a fresh Bearer token via the bundled dynamic_credentials helper. The
real token never touches this script: the runtime swaps the surrogate
on approved egress, only to analyticsdata.googleapis.com.

Scope requested at approval (from Google's public OAuth scope docs):
  https://www.googleapis.com/auth/analytics.readonly

Endpoint paths, request body fields, and the response row shape are
taken from the official Google Analytics Data API v1 REST reference
(developers.google.com/analytics/devguides/reporting/data/v1/rest)
and have not yet been verified in a live flow.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.google-analytics"
ALLOWED_HOSTS = ("analyticsdata.googleapis.com",)
BASE = "https://analyticsdata.googleapis.com"
CONNECT_GUIDANCE = (
    "not connected: approve Google Analytics access via the secure "
    "credential flow (credentials.request_api_access) as "
    "`custom.google-analytics` (OAuth 2.0 with the analytics.readonly "
    "scope; a service account added to the GA4 property also works), "
    "then retry."
)

PROPERTY_RE = re.compile(r"^properties/\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$|^\d+daysAgo$|^(today|yesterday)$")

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


def error_exit(exc, provider="Google Analytics"):
    """Exit with the provider's own error message when available."""
    if isinstance(exc, urllib.error.HTTPError):
        try:
            body = json.loads(exc.read().decode("utf-8", errors="replace"))
            msg = (body.get("error") or {}).get("message", str(exc))
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


def call(path: str, payload: dict | None = None) -> dict:
    """JSON POST against the Analytics Data API v1beta base."""
    url = BASE + path
    data = json.dumps(payload or {}).encode("utf-8")
    req = authed_request(url, data=data,
                         headers={"Content-Type": "application/json"},
                         method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return read_json_response(resp)
    except Exception as exc:  # HTTPError and network-level failures
        error_exit(exc)


def check_property(property_id: str) -> str:
    if not PROPERTY_RE.match(property_id or ""):
        sys.exit(
            "error: --property-id must look like properties/1234 "
            "(the numeric GA4 property ID, found in Admin > Property "
            f"settings). Got: {property_id!r}")
    return property_id


def check_date(value: str, flag: str) -> str:
    if not DATE_RE.match(value or ""):
        sys.exit(
            f"error: {flag} must be YYYY-MM-DD or a relative term "
            f"(NdaysAgo, yesterday, today). Got: {value!r}")
    return value


def parse_names(value: str | None) -> list:
    return [part.strip() for part in (value or "").split(",")
            if part.strip()]


def format_rows(result: dict) -> dict:
    """Flatten a report response into named dimension/metric rows."""
    dim_headers = [(h or {}).get("name") for h in
                   result.get("dimensionHeaders", [])]
    met_headers = [(h or {}).get("name") for h in
                   result.get("metricHeaders", [])]
    rows = []
    for row in result.get("rows", []):
        entry = {}
        for header, val in zip(dim_headers,
                               row.get("dimensionValues", [])):
            entry[header or "?"] = (val or {}).get("value")
        for header, val in zip(met_headers, row.get("metricValues", [])):
            entry[header or "?"] = (val or {}).get("value")
        rows.append(entry)
    out = {"rows": rows, "rowCount": result.get("rowCount"),
           "kind": result.get("kind")}
    if "propertyQuota" in result:
        out["propertyQuota"] = result["propertyQuota"]
    for key in ("totals", "maximums", "minimums"):
        if key in result:
            out[key] = result[key]
    return out


def cmd_auth(args):
    property_id = check_property(args.property_id)
    # Minimal runReport: one dimension, one metric, one row. Verifies the
    # OAuth token is valid and the principal can read this property.
    result = call(
        f"/v1beta/{urllib.parse.quote(property_id, safe='')}:runReport",
        {"dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
         "dimensions": [{"name": "date"}],
         "metrics": [{"name": "sessions"}],
         "limit": "1"})
    print(json.dumps({"ok": True, "property": property_id,
                      "rowCount": result.get("rowCount")}, indent=2))


def cmd_report(args):
    property_id = check_property(args.property_id)
    start = check_date(args.start_date, "--start-date")
    end = check_date(args.end_date, "--end-date")
    dimensions = parse_names(args.dimensions)
    metrics = parse_names(args.metrics) or ["sessions"]
    payload = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": name} for name in dimensions],
        "metrics": [{"name": name} for name in metrics],
        "limit": str(args.limit),
    }
    if args.order_by:
        payload["orderBys"] = [{"desc": args.order_desc,
                                "metric": {"metricName": args.order_by}}]
    result = call(
        f"/v1beta/{urllib.parse.quote(property_id, safe='')}:runReport",
        payload)
    print(json.dumps(format_rows(result), indent=2))


def cmd_realtime(args):
    property_id = check_property(args.property_id)
    dimensions = parse_names(args.dimensions)
    metrics = parse_names(args.metrics) or ["activeUsers"]
    payload = {
        "dimensions": [{"name": name} for name in dimensions],
        "metrics": [{"name": name} for name in metrics],
        "limit": str(args.limit),
    }
    result = call(
        f"/v1beta/{urllib.parse.quote(property_id, safe='')}"
        ":runRealtimeReport",
        payload)
    print(json.dumps(format_rows(result), indent=2))


def cmd_batch(args):
    property_id = check_property(args.property_id)
    try:
        with open(args.requests_file, "r", encoding="utf-8") as fh:
            requests = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"error: could not read requests file: {exc}")
    if not isinstance(requests, list) or not requests:
        sys.exit("error: requests file must contain a non-empty JSON "
                 "array of runReport request bodies")
    # Per the official docs, within a batch request each item's property
    # should be unspecified or consistent with the batch-level property.
    result = call(
        f"/v1beta/{urllib.parse.quote(property_id, safe='')}"
        ":batchRunReports",
        {"requests": requests})
    reports = [format_rows(r) for r in result.get("reports", [])]
    print(json.dumps({"reports": reports, "kind": result.get("kind")},
                     indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="GA4 Data API v1 CLI (muse-connectors, read-only)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser(
        "auth", help="verify the token can read a GA4 property")
    p.add_argument("--property-id", required=True,
                   help="GA4 property id, e.g. properties/1234")
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("report", help="run a standard GA4 report")
    p.add_argument("--property-id", required=True,
                   help="GA4 property id, e.g. properties/1234")
    p.add_argument("--start-date", required=True,
                   help="YYYY-MM-DD or NdaysAgo, yesterday, today")
    p.add_argument("--end-date", required=True,
                   help="YYYY-MM-DD or NdaysAgo, yesterday, today")
    p.add_argument("--metrics", default="sessions,totalUsers",
                   help="comma-separated metric names")
    p.add_argument("--dimensions", default="date",
                   help="comma-separated dimension names")
    p.add_argument("--limit", type=int, default=100,
                   help="max rows to return")
    p.add_argument("--order-by", default=None,
                   help="metric name to sort by")
    p.add_argument("--order-desc", action="store_true",
                   help="sort descending (default ascending)")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("realtime", help="run a realtime GA4 report "
                                       "(last 30 minutes)")
    p.add_argument("--property-id", required=True,
                   help="GA4 property id, e.g. properties/1234")
    p.add_argument("--metrics", default="activeUsers",
                   help="comma-separated metric names "
                        "(realtime metrics list)")
    p.add_argument("--dimensions", default="",
                   help="comma-separated dimension names "
                        "(realtime dimensions list)")
    p.add_argument("--limit", type=int, default=100,
                   help="max rows to return")
    p.set_defaults(func=cmd_realtime)

    p = sub.add_parser("batch", help="run several reports in one call")
    p.add_argument("--property-id", required=True,
                   help="GA4 property id, e.g. properties/1234")
    p.add_argument("--requests-file", required=True,
                   help="path to a JSON file holding an array of "
                        "runReport request bodies")
    p.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
