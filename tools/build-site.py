#!/usr/bin/env python3
"""Generate docs/connectors.json from the README catalog.

Run this before pushing whenever connectors change, so the GitHub Pages
site always matches the repo. Usage: python3 tools/build-site.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATEGORIES = {
    # communication
    "slack": "Communication", "telegram": "Communication",
    # dev
    "github": "Dev tools", "gitlab": "Dev tools",
    # project management
    "linear": "Project management", "asana": "Project management",
    "monday": "Project management",
    # notes & docs
    "notion": "Notes & docs", "coda": "Notes & docs",
    # email
    "resend": "Email", "sendgrid": "Email", "postmark": "Email",
    # crm / sales
    "hubspot": "CRM", "pipedrive": "CRM", "apollo": "Sales",
    # research
    "tavily": "Research", "exa": "Research", "brave-search": "Research",
    "newsapi": "Research",
    # finance
    "stripe": "Finance", "mercury": "Finance", "wise": "Finance",
    "alphavantage": "Finance",
    # ai
    "openai": "AI", "anthropic": "AI", "huggingface": "AI",
    "elevenlabs": "AI", "openrouter": "AI",
    # cloud & hosting
    "vercel": "Cloud & hosting", "cloudflare": "Cloud & hosting",
    "supabase": "Cloud & hosting", "render": "Cloud & hosting",
    "digitalocean": "Cloud & hosting", "netlify": "Cloud & hosting",
    # monitoring
    "sentry": "Monitoring", "posthog": "Monitoring",
    # support
    "front": "Support",
    # productivity
    "todoist": "Productivity", "clickup": "Productivity",
    "airtable": "Productivity",
    # misc
    "figma": "Design", "home-assistant": "Smart home",
    "shopify": "E-commerce", "gumroad": "E-commerce", "paddle": "E-commerce",
    "openweathermap": "Weather", "readwise": "Reading",
    "calcom": "Scheduling", "deepl": "Translation", "beehiiv": "Newsletters",
    "discord": "Communication",
    "loops": "Email",
    # batch E: memory
    "mem0": "Memory", "supermemory": "Memory", "zep": "Memory", "letta": "Memory",
    # batch E: daily life
    "ticktick": "Productivity", "ynab": "Finance", "oura": "Health",
    "philips-hue": "Smart home", "calendly": "Scheduling", "amadeus": "Travel",
    # batch E: money
    "buttondown": "Newsletters", "lemon-squeezy": "E-commerce", "polar": "E-commerce",
    "etsy": "E-commerce", "kit": "Newsletters", "printful": "E-commerce",
    "patreon": "Creator", "ashby": "Jobs",
    # batch E: media generation
    "fal-ai": "Media generation", "gemini": "Media generation", "ideogram": "Media generation",
    "black-forest-labs": "Media generation", "heygen": "Media generation",
    "luma": "Media generation", "kling": "Media generation", "runway": "Media generation",
    "beatoven": "Media generation",
    # batch E: creator
    "twitch": "Creator", "mastodon": "Social", "devto": "Blogging",
    "dub": "Marketing",
    "tally": "Productivity",
    "firecrawl": "Research",
    "perplexity": "AI",
    "replicate": "AI",
    "neon": "Cloud & hosting",
    "upstash": "Cloud & hosting",
    "clerk": "Dev tools",
    "attio": "CRM",
    "triggerdev": "Dev tools",
    "x": "Social",
    "youtube": "Video",
    "plain": "Support",
    "railway": "Cloud & hosting",
    "flyio": "Cloud & hosting",
    "n8n": "Productivity",
    "langfuse": "AI",
    "bluesky": "Social",
    # batch F: design / stock / media management
    "canva": "Design", "webflow": "Design", "framer": "Design",
    "pexels": "Stock media", "unsplash": "Stock media",
    "cloudinary": "Media management", "remove-bg": "Design",
    # batch F: podcasting
    "transistor": "Podcasting", "buzzsprout": "Podcasting",
    "podbean": "Podcasting",
    # batch F: video / livestreaming
    "descript": "Video", "opusclip": "Video", "veed": "Video",
    "restream": "Livestreaming",
    # batch F: voice AI / avatar video
    "cartesia": "Voice AI", "hume-ai": "Voice AI", "playht": "Voice AI",
    "deepgram": "Voice AI", "elai": "Media generation",
    # batch F: smart home
    "smartthings": "Smart home", "tuya": "Smart home",
    "switchbot": "Smart home", "google-nest": "Smart home",
    "aqara": "Smart home", "hubitat": "Smart home", "homey": "Smart home",
    "unifi-protect": "Smart home", "ecovacs": "Smart home",
    "rachio": "Smart home",
    # batch F: energy / vehicles / 3d printing
    "tesla-powerwall": "Energy", "tesla-fleet-api": "Vehicles",
    "smartcar": "Vehicles", "octoprint": "3D printing",
    "moonraker": "3D printing", "prusa-connect": "3D printing",
    # batch F: logistics / commerce / agritech
    "shippo": "Logistics", "uber-direct": "Logistics", "lob": "Logistics",
    "square": "E-commerce", "leaf-agriculture": "Agritech",
}

ID_RE = re.compile(r"connectors/([a-z0-9-]+)/SKILL\.md")


def parse_entries(readme):
    entries = []
    blocks = re.split(r"(?m)^### ", readme)[1:]
    for b in blocks:
        header, rest = b.split("\n", 1)
        hm = re.match(r"(.+?)\s+(✅|🧪|👥)", header)
        if not hm:
            continue
        name, badge = hm.groups()
        tagline = next((ln.strip() for ln in rest.split("\n") if ln.strip()), "")
        am = re.search(r"^- Auth:\s+(.*?)\s+·\s+Allowed hosts:\s+(.*?)\s*$",
                       rest, re.M)
        if not am:
            continue
        auth, hosts = am.groups()
        hosts = hosts.strip().strip("`")
        id_m = ID_RE.search(b)
        if not id_m:
            continue
        entries.append((id_m.group(1), name.strip(), badge, tagline, auth,
                        [h.strip().strip("`") for h in hosts.split(",")]))
    return entries


def main():
    readme = (ROOT / "README.md").read_text()
    connectors = []
    for cid, name, badge, tagline, auth, hosts in parse_entries(readme):
        connectors.append({
            "id": cid,
            "name": name.strip(),
            "tagline": tagline.strip(),
            "auth": auth.strip(),
            "hosts": hosts,
            "maturity": {"✅": "live", "🧪": "draft", "👥": "community"}[badge],
            "category": CATEGORIES.get(cid, "Other"),
        })
    connectors.sort(key=lambda c: c["name"].lower())
    out = ROOT / "docs" / "connectors.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(connectors, indent=2) + "\n")
    print(f"wrote {out} ({len(connectors)} connectors)")


if __name__ == "__main__":
    main()
