#!/usr/bin/env python3
"""Minimal Google Gemini API CLI (media generation) for the muse-connectors gemini skill.

Auth: loads the per-user `custom.gemini` credential (Google AI Studio API key)
as a surrogate via the bundled dynamic_credentials helper. The real key never
touches this script: the runtime swaps the surrogate on approved egress, only
to generativelanguage.googleapis.com, and the CLI sends it verbatim as the
`x-goog-api-key` header.

COST WARNING: all media generation requires a BILLING-ENABLED project;
free-tier media quota is 0. Every generation command spends real money.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.gemini"
ALLOWED_HOSTS = ("generativelanguage.googleapis.com",)
BASE = "https://generativelanguage.googleapis.com/v1beta"

IMAGE_MODEL = "gemini-2.5-flash-image"        # Nano Banana, text-to-image/edit, sync
IMAGEN_MODEL = "imagen-4.0-generate-001"      # Imagen 4, sync
VEO_MODEL = "veo-3.1-generate-preview"       # Veo 3.1, async long-running op
TTS_MODEL = "gemini-2.5-flash-preview-tts"   # TTS, sync

try:
    sys.path.insert(0, HELPER_PATH)
    from dynamic_credentials import (
        DynamicCredentialError,
        dynamic_credential_entry,
        ensure_allowed_url,
    )
except ImportError:
    sys.exit(
        "error: this CLI needs the Muse dynamic_credentials helper at "
        f"{HELPER_PATH} (install this skill on a Muse runtime to use it)"
    )


def api_key() -> str:
    try:
        return str(dynamic_credential_entry(CREDENTIAL_NAME)["surrogate"]).strip()
    except DynamicCredentialError as exc:
        sys.exit(f"error: credential problem: {exc}")


def call(method: str, path: str, payload: dict | None = None,
         params: dict | None = None) -> dict:
    url = BASE + path
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif params:
        url += "?" + urllib.parse.urlencode(params)
    ensure_allowed_url(url, allowed_hosts=ALLOWED_HOSTS)
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    req.add_header("x-goog-api-key", api_key())
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"raw": raw}
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8", errors="replace"))
            msg = body.get("error", {}).get("message", str(exc))
        except Exception:
            msg = str(exc)
        sys.exit(f"error: Gemini API returned HTTP {exc.code}: {msg}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def _merge_json(extra: str | None, base: dict) -> dict:
    if not extra:
        return base
    try:
        obj = json.loads(extra)
    except json.JSONDecodeError as exc:
        sys.exit(f"error: --json is not valid JSON: {exc}")
    if not isinstance(obj, dict):
        sys.exit("error: --json must be a JSON object")
    base.update(obj)
    return base


def _file_part(path: str) -> dict:
    with open(path, "rb") as fh:
        blob = fh.read()
    return {"inlineData": {"mimeType": "image/png",
                           "data": base64.b64encode(blob).decode("ascii")}}


def _save_inline_images(result: dict, out_prefix: str) -> list[str]:
    saved = []
    idx = 0
    for cand in result.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                mime = inline.get("mimeType", "image/png")
                ext = {"image/png": "png", "image/jpeg": "jpg",
                       "audio/wav": "wav", "audio/mpeg": "mp3",
                       "audio/x-wav": "wav"}.get(mime, "bin")
                path = f"{out_prefix}-{idx}.{ext}"
                with open(path, "wb") as fh:
                    fh.write(base64.b64decode(inline["data"]))
                saved.append(path)
                idx += 1
    return saved


def cmd_auth(_args):
    result = call("GET", "/models", params={"pageSize": 1})
    models = result.get("models", [])
    print(json.dumps({"ok": True, "models": len(models)}, indent=2))


def cmd_models(args):
    result = call("GET", "/models", params={"pageSize": args.limit})
    out = [{"name": m.get("name"), "displayName": m.get("displayName")}
           for m in result.get("models", [])]
    print(json.dumps(out, indent=2))


def cmd_image(args):
    """Nano Banana text-to-image (or edit when --image is given), sync."""
    parts: list[dict] = [{"text": args.prompt}]
    if args.image:
        parts.append(_file_part(args.image))
    payload = _merge_json(args.json, {"contents": [{"parts": parts}]})
    result = call("POST", f"/models/{IMAGE_MODEL}:generateContent", payload=payload)
    saved = _save_inline_images(result, args.out)
    print(json.dumps({"ok": True, "saved": saved}, indent=2))


def cmd_imagen(args):
    """Imagen 4 predict, sync."""
    payload = _merge_json(args.json, {
        "instances": [{"prompt": args.prompt}],
        "parameters": {"sampleCount": args.count}})
    result = call("POST", f"/models/{IMAGEN_MODEL}:predict", payload=payload)
    saved = []
    for i, pred in enumerate(result.get("predictions", [])):
        b64 = pred.get("bytesBase64Encoded")
        if b64:
            path = f"{args.out}-{i}.png"
            with open(path, "wb") as fh:
                fh.write(base64.b64decode(b64))
            saved.append(path)
    print(json.dumps({"ok": True, "saved": saved}, indent=2))


def cmd_video(args):
    """Veo 3.1: async long-running operation. Prints the operation id."""
    payload = _merge_json(args.json, {"instances": [{"prompt": args.prompt}]})
    result = call("POST", f"/models/{VEO_MODEL}:predictLongRunning", payload=payload)
    name = result.get("name", "")
    print(json.dumps({"ok": True, "operation": name,
                      "poll": f"bin/gemini.py op-status --op {name}"}, indent=2))
    print("note: Veo renders take minutes; poll op-status until done, then download the video file (files.download).",
          file=sys.stderr)


def cmd_op_status(args):
    name = args.op.lstrip("/")
    result = call("GET", f"/{name}")
    done = result.get("done", False)
    out = {"done": done}
    if done:
        out["response"] = result.get("response")
        out["error"] = result.get("error")
    else:
        out["metadata"] = result.get("metadata")
    print(json.dumps(out, indent=2))


def cmd_tts(args):
    """TTS via generateContent, sync; audio saved to --out."""
    payload = _merge_json(args.json, {
        "contents": [{"parts": [{"text": args.text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {
                "prebuiltVoiceConfig": {"voiceName": args.voice}}}},
    })
    result = call("POST", f"/models/{TTS_MODEL}:generateContent", payload=payload)
    saved = _save_inline_images(result, args.out)
    print(json.dumps({"ok": True, "saved": saved}, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Gemini media API CLI (muse-connectors)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth", help="verify the API key (free models list read)")
    p.set_defaults(func=cmd_auth)

    p = sub.add_parser("models", help="list available models")
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(func=cmd_models)

    p = sub.add_parser("image", help="Nano Banana text-to-image / edit (confirm first; billed)")
    p.add_argument("--prompt", required=True)
    p.add_argument("--image", default=None, help="input image for editing")
    p.add_argument("--out", required=True, help="output path prefix, e.g. /tmp/thumb")
    p.add_argument("--json", default=None, help="extra JSON fields merged into the request")
    p.set_defaults(func=cmd_image)

    p = sub.add_parser("imagen", help="Imagen 4 text-to-image (confirm first; billed)")
    p.add_argument("--prompt", required=True)
    p.add_argument("--count", type=int, default=1)
    p.add_argument("--out", required=True, help="output path prefix")
    p.add_argument("--json", default=None, help="extra JSON fields merged into the request")
    p.set_defaults(func=cmd_imagen)

    p = sub.add_parser("video", help="Veo 3.1 text-to-video (confirm first; billed per second)")
    p.add_argument("--prompt", required=True)
    p.add_argument("--json", default=None, help="extra JSON fields merged into the request")
    p.set_defaults(func=cmd_video)

    p = sub.add_parser("op-status", help="poll a Veo long-running operation")
    p.add_argument("--op", required=True, help="operation id, e.g. operations/abc123")
    p.set_defaults(func=cmd_op_status)

    p = sub.add_parser("tts", help="text-to-speech (confirm first; billed)")
    p.add_argument("--text", required=True)
    p.add_argument("--voice", default="Kore", help="prebuilt voice name")
    p.add_argument("--out", required=True, help="output path prefix")
    p.add_argument("--json", default=None, help="extra JSON fields merged into the request")
    p.set_defaults(func=cmd_tts)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
