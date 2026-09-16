#!/usr/bin/env python3
"""Minimal YouTube Data API v3 CLI for the muse-connectors youtube skill.

Reads only: this skill covers public read endpoints (channel, video,
search, playlist items). Writes (comments, uploads) need OAuth and are
deferred to a later version.

Auth: loads the per-user `custom.youtube` API key as a surrogate via the
bundled dynamic_credentials helper and appends it to the URL as the `key`
query parameter with url_with_surrogate_query_param. The real API key never
touches this script: the runtime swaps the surrogate on approved egress,
only to www.googleapis.com.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.youtube"
ALLOWED_HOSTS = ("www.googleapis.com",)
API = "https://www.googleapis.com/youtube/v3"

try:
    sys.path.insert(0, HELPER_PATH)
    from dynamic_credentials import (
        DynamicCredentialError,
        read_json_response,
        url_with_surrogate_query_param,
    )
except ImportError:
    sys.exit(
        "error: this CLI needs the Muse dynamic_credentials helper at "
        f"{HELPER_PATH} (install this skill on a Muse runtime to use it)"
    )


def call(path: str, params: dict | None = None) -> dict:
    """GET with the API key appended as the `key` query param."""
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        url = url_with_surrogate_query_param(
            url, CREDENTIAL_NAME, allowed_hosts=ALLOWED_HOSTS)
    except DynamicCredentialError as exc:
        sys.exit(f"error: credential problem: {exc}")
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return read_json_response(resp)
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8", errors="replace"))
            msg = (body.get("error") or {}).get("message", str(exc))
        except Exception:
            msg = str(exc)
        sys.exit(f"error: YouTube returned HTTP {exc.code}: {msg}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def cmd_auth(_args):
    result = call("/videos", params={"part": "snippet",
                                     "chart": "mostPopular",
                                     "maxResults": 1,
                                     "regionCode": "US"})
    items = result.get("items", [])
    print(json.dumps({"ok": True, "items": len(items),
                      "first": (items[0].get("snippet") or {}).get("title")
                      if items else None}, indent=2))


def cmd_channel(args):
    result = call("/channels", params={"part": "snippet,statistics",
                                       "id": args.id})
    items = result.get("items", [])
    out = []
    for c in items:
        snippet, stats = c.get("snippet", {}), c.get("statistics", {})
        out.append({"id": c.get("id"), "title": snippet.get("title"),
                    "description": (snippet.get("description") or "")[:200],
                    "subscribers": stats.get("subscriberCount"),
                    "views": stats.get("viewCount"),
                    "videos": stats.get("videoCount")})
    print(json.dumps(out, indent=2))


def cmd_video(args):
    result = call("/videos", params={"part": "snippet,statistics",
                                     "id": args.id})
    items = result.get("items", [])
    out = []
    for v in items:
        snippet, stats = v.get("snippet", {}), v.get("statistics", {})
        out.append({"id": v.get("id"), "title": snippet.get("title"),
                    "channel": snippet.get("channelTitle"),
                    "published": snippet.get("publishedAt"),
                    "views": stats.get("viewCount"),
                    "likes": stats.get("likeCount"),
                    "comments": stats.get("commentCount")})
    print(json.dumps(out, indent=2))


def cmd_search(args):
    result = call("/search", params={"part": "snippet", "q": args.query,
                                     "type": "video", "maxResults": args.limit})
    out = [
        {"id": (i.get("id") or {}).get("videoId"),
         "title": (i.get("snippet") or {}).get("title"),
         "channel": (i.get("snippet") or {}).get("channelTitle"),
         "published": (i.get("snippet") or {}).get("publishedAt")}
        for i in result.get("items", [])
    ]
    print(json.dumps(out, indent=2))


def cmd_playlist_items(args):
    result = call("/playlistItems",
                  params={"part": "snippet", "playlistId": args.playlist_id,
                          "maxResults": args.limit})
    out = [
        {"id": (i.get("snippet") or {}).get("resourceId", {}).get("videoId"),
         "title": (i.get("snippet") or {}).get("title"),
         "position": (i.get("snippet") or {}).get("position")}
        for i in result.get("items", [])
    ]
    print(json.dumps(out, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Data API v3 CLI, reads only (muse-connectors)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth", help="verify the API key (1 quota unit)")
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("channel", help="show a channel (1 quota unit)")
    p.add_argument("--id", required=True, help="channel ID")
    p.set_defaults(func=cmd_channel)

    p = sub.add_parser("video", help="show a video (1 quota unit)")
    p.add_argument("--id", required=True, help="video ID")
    p.set_defaults(func=cmd_video)

    p = sub.add_parser("search", help="search videos (100 quota units)")
    p.add_argument("--query", required=True)
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("playlist-items", help="list playlist items (1 quota unit)")
    p.add_argument("--playlist-id", required=True)
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(func=cmd_playlist_items)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
