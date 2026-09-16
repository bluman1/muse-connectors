#!/usr/bin/env python3
"""Minimal Neon Management API CLI for the muse-connectors neon skill.

This is the Neon Management API only (projects, branches, compute
endpoints). SQL queries run over the Postgres wire protocol with a separate
connection string; this CLI never runs queries.

Auth: loads the per-user `custom.neon` credential as a surrogate via the
bundled dynamic_credentials helper. The real API key never touches this
script: the runtime swaps the surrogate on approved egress, only to
console.neon.tech.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.neon"
ALLOWED_HOSTS = ("console.neon.tech",)
API = "https://console.neon.tech/api/v2"

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


def call(method: str, path: str, params: dict | None = None,
         payload: dict | None = None) -> dict:
    url = API + path
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        add_surrogate_to_request(req, CREDENTIAL_NAME, allowed_hosts=ALLOWED_HOSTS)
    except DynamicCredentialError as exc:
        sys.exit(f"error: credential problem: {exc}")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return read_json_response(resp)
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8", errors="replace"))
            msg = body.get("message", body.get("error", str(exc)))
        except Exception:
            msg = str(exc)
        sys.exit(f"error: Neon returned HTTP {exc.code}: {msg}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def summarize_project(p: dict) -> dict:
    return {"id": p.get("id"), "name": p.get("name"),
            "region_id": p.get("region_id"),
            "created_at": p.get("created_at")}


def cmd_auth(_args):
    result = call("GET", "/projects", params={"limit": 1})
    projects = result.get("projects", [])
    print(json.dumps({"ok": True, "projects": len(projects),
                      "first": summarize_project(projects[0])
                      if projects else None}, indent=2))


def cmd_projects(_args):
    result = call("GET", "/projects")
    print(json.dumps([summarize_project(p)
                      for p in result.get("projects", [])], indent=2))


def cmd_create_project(args):
    result = call("POST", "/projects",
                  payload={"project": {"name": args.name}})
    print(json.dumps({"ok": True,
                      "project": summarize_project(result.get("project", {}))},
                     indent=2))


def cmd_create_branch(args):
    result = call("POST", f"/projects/{args.project}/branches",
                  payload={"branch": {"name": args.name}})
    branch = result.get("branch", {})
    print(json.dumps({"ok": True, "id": branch.get("id"),
                      "name": branch.get("name"),
                      "project_id": branch.get("project_id")}, indent=2))


def cmd_start_endpoint(args):
    result = call("POST",
                  f"/projects/{args.project}/endpoints/{args.endpoint}/start")
    ep = result.get("endpoint", {})
    print(json.dumps({"ok": True, "id": ep.get("id"),
                      "state": ep.get("state")}, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Neon Management API CLI (muse-connectors)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth", help="verify the API key")
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("projects", help="list projects")
    p.set_defaults(func=cmd_projects)

    p = sub.add_parser("create-project",
                       help="create a project (confirm first)")
    p.add_argument("--name", required=True, help="project name")
    p.set_defaults(func=cmd_create_project)

    p = sub.add_parser("create-branch",
                       help="create a branch (confirm first)")
    p.add_argument("--project", required=True, help="project ID")
    p.add_argument("--name", required=True, help="branch name")
    p.set_defaults(func=cmd_create_branch)

    p = sub.add_parser("start-endpoint",
                       help="start a compute endpoint (confirm first)")
    p.add_argument("--project", required=True, help="project ID")
    p.add_argument("--endpoint", required=True, help="endpoint ID")
    p.set_defaults(func=cmd_start_endpoint)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
