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
}

ENTRY_RE = re.compile(
    r"^### (.+?) (✅|🧪|👥).*$"      # name + badge
    r"\n\n(.+?)\n\n"                  # tagline
    r"- Auth: (.+?) · Allowed hosts: `(.+?)`\n"
    r"- Maturity: .*$",
    re.M,
)
ID_RE = re.compile(r"connectors/([a-z0-9-]+)/SKILL\.md")


def main():
    readme = (ROOT / "README.md").read_text()
    connectors = []
    for m in ENTRY_RE.finditer(readme):
        name, badge, tagline, auth, hosts = m.groups()
        id_m = ID_RE.search(readme[m.start(): m.start() + 2000])
        if not id_m:
            continue
        cid = id_m.group(1)
        connectors.append({
            "id": cid,
            "name": name.strip(),
            "tagline": tagline.strip(),
            "auth": auth.strip(),
            "hosts": [h.strip() for h in hosts.split(",")],
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
