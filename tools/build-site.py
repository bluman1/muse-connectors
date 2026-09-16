#!/usr/bin/env python3
"""Generate docs/connectors.json and docs/index.html from the README catalog.

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

# Normalize the working category names to the design's filter taxonomy.
NORMALIZE = {
    "Dev tools": "Developer & Infra",
    "CRM": "Sales & CRM",
    "Sales": "Sales & CRM",
    "AI": "AI & ML",
    "Research": "Search & Data",
    "Finance": "Finance & Commerce",
}

# Filter chip order: the design's categories first, then the rest grouped.
FILTER_ORDER = [
    "Communication", "Productivity", "Email", "Sales & CRM", "AI & ML",
    "Search & Data", "Finance & Commerce", "Developer & Infra",
    "Project management", "Notes & docs", "Cloud & hosting", "Monitoring",
    "Support", "Design", "Smart home", "Energy", "Vehicles", "3D printing",
    "E-commerce", "Logistics", "Marketing", "Newsletters", "Blogging",
    "Social", "Creator", "Video", "Livestreaming", "Podcasting", "Voice AI",
    "Media generation", "Media management", "Stock media", "Translation",
    "Reading", "Scheduling", "Travel", "Health", "Memory", "Jobs",
    "Weather", "Agritech", "Other",
]

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
        hosts = clean_hosts(hosts)
        id_m = ID_RE.search(b)
        if not id_m:
            continue
        entries.append((id_m.group(1), name.strip(), badge, tagline, auth, hosts))
    return entries


def clean_hosts(raw):
    s = raw.replace("`", "")
    s = re.sub(r"\s*\([^)]*\)", "", s)
    out = []
    for h in s.split(","):
        h = h.strip().rstrip(".")
        if h and h not in out:
            out.append(h)
    return out


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Muse Connectors: auditable connector skills for Muse</title>
<meta name="description" content="Browse every open-source Muse connector. Copy a one-paste install prompt, audit the code, connect your own account.">
<link rel="icon" type="image/png" href="avatar/favicon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Muse Connectors">
<meta property="og:title" content="Muse Connectors: auditable connector skills for Muse">
<meta property="og:description" content="Browse every open-source Muse connector. Copy a one-paste install prompt, audit the code, connect your own account.">
<meta property="og:url" content="https://bluman1.github.io/muse-connectors/">
<meta property="og:image" content="https://bluman1.github.io/muse-connectors/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Muse Connectors: auditable connector skills for Muse">
<meta name="twitter:description" content="Browse every open-source Muse connector. Copy a one-paste install prompt, audit the code, connect your own account.">
<meta name="twitter:image" content="https://bluman1.github.io/muse-connectors/og-image.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f7f6fb; --surface:#fff; --code-bg:#f3f1f9; --chip-bg:#eeebf6;
  --border:#e6e2f0; --divider:#efedf5;
  --ink:#17141f; --body:#4b4660; --muted:#6b6580; --faint:#a39db5; --code-text:#2a2538;
  --accent:oklch(0.45 0.2 300); --accent-tint:oklch(0.95 0.03 300); --accent-border:oklch(0.75 0.1 300);
  --live-text:oklch(0.4 0.14 150); --live-bg:oklch(0.95 0.05 150);
  --draft-text:oklch(0.5 0.12 70); --draft-bg:oklch(0.96 0.05 80);
  --dark:#17141f; --dark-card:#221e2d; --dark-code:#2a2538; --dark-body:#b9b3cc;
  --dark-label:oklch(0.8 0.12 300);
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Sora,-apple-system,"Segoe UI",sans-serif;}
.wrap{max-width:1200px;margin:0 auto}
/* ---------- nav ---------- */
.nav{display:flex;justify-content:space-between;align-items:center;padding:20px 40px;border-bottom:1px solid var(--border)}
.brand{display:flex;align-items:center;gap:12px}
.brand video{width:36px;height:36px;border-radius:12px;object-fit:cover;display:block;background:var(--chip-bg)}
.brand .word{font-size:15px;font-weight:600}
.pilltag{font-family:var(--mono);font-size:12px;color:var(--muted);background:var(--chip-bg);border-radius:999px;padding:4px 10px}
.navlinks{display:flex;align-items:center;gap:28px}
.navlinks a{font-size:14px;color:var(--body);text-decoration:none}
.navlinks a:hover{color:var(--ink)}
.btn{display:inline-flex;align-items:center;justify-content:center;font-family:Sora,sans-serif;font-weight:500;cursor:pointer;text-decoration:none;border:0}
.btn-repo{background:var(--ink);color:#fff;font-size:13px;padding:9px 16px;border-radius:999px}
.btn-repo:hover{background:#000}
/* ---------- hero ---------- */
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;padding:64px 40px 40px;align-items:end}
.hero-left{display:flex;flex-direction:column;gap:20px;align-items:flex-start}
.eyebrow{font-size:12px;font-weight:500;color:var(--accent);background:var(--accent-tint);border-radius:999px;padding:6px 12px}
.hero h1{margin:0;font-size:44px;line-height:1.1;font-weight:600;letter-spacing:-0.02em;text-wrap:pretty}
.hero-sub{margin:0;font-size:17px;line-height:1.6;color:var(--body);max-width:540px;text-wrap:pretty}
.hero p{margin:0;font-size:17px;line-height:1.6;color:var(--body);max-width:540px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.step{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:18px;display:flex;flex-direction:column;gap:10px}
.step .n{font-family:var(--mono);font-size:12px;font-weight:500;color:var(--accent)}
.step .t{font-size:14px;font-weight:600}
.step .b{font-size:13px;line-height:1.5;color:var(--muted)}
/* ---------- search + filters ---------- */
.finder{position:sticky;top:0;z-index:2;background:var(--bg);padding:16px 40px;border-bottom:1px solid var(--border);display:flex;flex-direction:column;gap:14px}
.searchrow{display:flex;align-items:center;gap:16px}
.search{flex:1;display:flex;align-items:center;gap:12px;background:var(--surface);border:1px solid var(--border);border-radius:12px;height:44px;padding:0 14px}
.sicon{width:8px;height:8px;border:2px solid var(--muted);border-radius:999px;flex:none}
.search input{flex:1;border:0;outline:0;background:transparent;font-family:Sora,sans-serif;font-size:14px;color:var(--ink);min-width:0}
.search input::placeholder{color:var(--faint)}
.count{font-family:var(--mono);font-size:13px;color:var(--muted);white-space:nowrap}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:var(--surface);border:1px solid var(--border);color:var(--body);font-family:Sora,sans-serif;font-size:13px;font-weight:500;padding:7px 14px;border-radius:999px;cursor:pointer}
.chip:hover{border-color:var(--ink);color:var(--ink)}
.chip.active{background:var(--ink);border-color:var(--ink);color:#fff}
/* ---------- catalog grid ---------- */
.catalog{padding:28px 40px 48px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;align-items:start}
.card{background:var(--surface);border:1px solid var(--border);border-radius:18px;padding:20px;display:flex;flex-direction:column;gap:14px;transition:border-color .12s ease,box-shadow .12s ease}
.card:hover{border-color:var(--accent-border);box-shadow:0 8px 24px rgba(23,20,31,.06)}
.chead{display:flex;gap:12px;align-items:flex-start}
.tile{width:40px;height:40px;flex:none;border-radius:12px;background:var(--accent-tint);color:var(--accent);font-size:16px;font-weight:600;display:flex;align-items:center;justify-content:center}
.cmeta{flex:1;min-width:0}
.cname{background:none;border:0;padding:0;font-family:Sora,sans-serif;font-size:15px;font-weight:600;color:var(--ink);cursor:pointer;text-align:left}
.cname:hover{color:var(--ink);text-decoration:underline}
.ccat{font-size:12px;color:var(--muted);margin-top:2px}
.pill{flex:none;font-size:11px;font-weight:500;padding:4px 9px;border-radius:999px}
.pill.live{color:var(--live-text);background:var(--live-bg)}
.pill.draft{color:var(--draft-text);background:var(--draft-bg)}
.pshort{display:none}
.cdesc{margin:0;font-size:13.5px;line-height:1.55;color:var(--body)}
.hosts{font-family:var(--mono);font-size:12px;color:var(--muted);display:flex;gap:8px;min-width:0}
.hlabel{color:var(--faint);flex:none}
.hval{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cfoot{display:flex;gap:8px;border-top:1px solid var(--divider);padding-top:14px}
.btn-copy{flex:1;background:var(--ink);color:#fff;font-size:13px;padding:10px 14px;border-radius:10px}
.btn-copy:hover{background:#000}
.btn-view{background:var(--surface);border:1px solid var(--border);color:var(--ink);font-size:13px;padding:10px 14px;border-radius:10px}
.btn-view:hover{border-color:var(--ink)}
pre.prompt{background:var(--code-bg);border:1px solid var(--border);border-radius:12px;padding:14px;font-family:var(--mono);font-size:11.5px;line-height:1.6;color:var(--code-text);white-space:pre-wrap;word-break:break-word;margin:0;max-height:320px;overflow:auto}
.empty{padding:40px 0;text-align:center;font-size:14px;color:var(--muted)}
/* ---------- detail panel ---------- */
.detail{margin:28px 40px 0;background:var(--surface);border:1px solid var(--border);border-radius:24px;padding:32px;flex-direction:column;gap:24px;scroll-margin-top:140px}
.detail:not([hidden]){display:flex}
.dtop{display:flex;justify-content:space-between;align-items:center}
.crumb{font-family:var(--mono);font-size:12px;color:var(--muted)}
.x{width:32px;height:32px;border-radius:999px;border:1px solid var(--border);background:var(--surface);color:var(--body);font-size:14px;cursor:pointer;line-height:1}
.x:hover{border-color:var(--ink);color:var(--ink)}
.dident{display:flex;gap:16px;align-items:center}
.dtile{width:52px;height:52px;flex:none;border-radius:16px;background:var(--accent-tint);color:var(--accent);font-size:22px;font-weight:600;display:flex;align-items:center;justify-content:center}
.dname{font-size:24px;font-weight:600;letter-spacing:-0.02em}
.dsub{font-size:13px;color:var(--muted);margin-top:4px}
.ddesc{margin:0;font-size:15px;line-height:1.6;color:var(--body)}
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.fact{background:var(--bg);border-radius:12px;padding:14px;min-width:0}
.flabel{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:8px}
.fval{font-size:13.5px;line-height:1.5;color:var(--ink);overflow-wrap:break-word}
.fval.mono{font-family:var(--mono);font-size:13px}
.plabel{font-size:13px;font-weight:500}
.prow{display:flex;gap:8px}
.prow .btn-copy{padding:12px 14px}
.btn-audit{background:var(--surface);border:1px solid var(--border);color:var(--ink);font-size:13px;padding:12px 18px;border-radius:10px;white-space:nowrap}
.btn-audit:hover{border-color:var(--ink)}
/* ---------- security ---------- */
.security{margin:0 40px;background:var(--dark);color:#fff;border-radius:24px;padding:48px;display:grid;grid-template-columns:1fr 1.4fr;gap:48px}
.slabel{font-family:var(--mono);font-size:12px;font-weight:500;color:var(--dark-label);margin-bottom:16px}
.security h2{margin:0 0 16px;font-size:30px;line-height:1.15;font-weight:600}
.security .sbody{margin:0;font-size:15px;line-height:1.6;color:var(--dark-body)}
code.inline{font-family:var(--mono);font-size:13px;background:var(--dark-code);color:#fff;padding:2px 6px;border-radius:6px}
.seccards{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.seccard{background:var(--dark-card);border-radius:16px;padding:20px}
.seccard .t{font-size:14px;font-weight:600;margin-bottom:8px}
.seccard .b{font-size:13px;line-height:1.5;color:var(--dark-body)}
/* ---------- contribute ---------- */
.contribute{margin:40px 40px 0;padding:40px;border:1px dashed var(--accent-border);border-radius:24px;display:flex;justify-content:space-between;align-items:center;gap:32px}
.contribute .left{max-width:560px}
.contribute h2{margin:0 0 12px;font-size:24px;font-weight:600}
.contribute p{margin:0;font-size:14.5px;line-height:1.6;color:var(--body)}
code.lite{font-family:var(--mono);font-size:13px;background:var(--chip-bg);padding:2px 6px;border-radius:6px;color:var(--code-text)}
.cbtns{display:flex;gap:12px;flex:none}
.btn-ghost{background:var(--surface);border:1px solid var(--border);color:var(--ink);font-size:13px;padding:11px 18px;border-radius:999px}
.btn-ghost:hover{border-color:var(--ink)}
.btn-accent{background:var(--accent);color:#fff;font-size:13px;padding:11px 18px;border-radius:999px}
/* ---------- footer ---------- */
.footer{display:flex;justify-content:space-between;align-items:center;padding:32px 40px;font-size:13px;color:var(--muted)}
.flink{color:var(--muted);text-decoration:none}
.flink:hover{color:var(--ink)}
.fright{display:flex;gap:20px}
/* ---------- mid screens ---------- */
@media (max-width:900px){
  .hero{grid-template-columns:1fr;padding:48px 40px 32px}
  .grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .security{grid-template-columns:1fr;gap:32px}
  .contribute{flex-direction:column;align-items:flex-start}
}
/* ---------- mobile ---------- */
@media (max-width:640px){
  .nav{padding:18px 20px}
  .brand video{width:32px;height:32px;border-radius:10px}
  .brand .word{font-size:14px}
  .navlinks{gap:0}
  .navlinks a{display:none}
  .btn-repo{font-size:12px;padding:8px 14px}
  .btn-repo .full{display:none}
  .hero{padding:28px 20px 20px}
  .eyebrow .full{display:none}
  .hero h1{font-size:28px;line-height:1.15}
  .hero p{font-size:14px}
  .steps{display:none}
  .finder{padding:12px 20px}
  .search{height:46px}
  .chips{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}
  .chips::-webkit-scrollbar{display:none}
  .chip{flex:none;padding:9px 14px}
  .catalog{padding:20px 20px 32px}
  .grid{grid-template-columns:1fr}
  .card{padding:18px}
  .pfull{display:none}
  .pshort{display:inline}
  .hosts{display:none}
  .btn-copy,.btn-view{padding:13px}
  .detail{margin:20px 20px 0;padding:20px}
  .facts{grid-template-columns:1fr}
  .prow{flex-direction:column}
  .btn-audit{text-align:center}
  .security{margin:0 20px;padding:28px}
  .seccards{grid-template-columns:1fr}
  .contribute{margin:28px 20px 0;padding:28px;flex-direction:column;align-items:stretch}
  .cbtns{flex-direction:column}
  .cbtns .btn{width:100%}
  .footer{flex-direction:column;gap:12px;padding:24px 20px;text-align:center}
}
</style>
</head>
<body>
<div class="wrap">
  <nav class="nav">
    <div class="brand">
      <video src="avatar/hatch.mp4" poster="avatar/hatch.jpg" autoplay muted loop playsinline aria-label="Muse avatar"></video>
      <span class="word">Muse Connectors</span>
      <span class="pilltag">catalog</span>
    </div>
    <div class="navlinks">
      <a href="https://github.com/bluman1/muse-connectors/blob/main/INSTALL.md">How it works</a>
      <a href="#security">Security</a>
      <a href="https://github.com/bluman1/muse-connectors/blob/main/CONTRIBUTING.md">Contribute</a>
      <a class="btn btn-repo" href="https://github.com/bluman1/muse-connectors"><span class="full">Repository</span><span class="pshort">Repo</span></a>
    </div>
  </nav>

  <header class="hero">
    <div class="hero-left">
      <span class="eyebrow">Open source &middot; MIT<span class="full"> &middot; zero secrets in repo</span></span>
      <h1>Connect your Muse to anything.<br>One paste. Fully auditable.</h1>
      <p class="hero-sub"><span class="pfull">Pick a connector, copy its install prompt, paste it to your Muse. It downloads the skill, verifies it, and walks you through connecting your own account. No skill ever sees your credentials.</span><span class="pshort">Copy an install prompt, paste it to your Muse, connect your own account. No skill ever sees your credentials.</span></p>
    </div>
    <div class="steps">
      <div class="step"><div class="n">01</div><div class="t">Copy</div><div class="b">the install prompt under any connector.</div></div>
      <div class="step"><div class="n">02</div><div class="t">Paste</div><div class="b">it into a chat with your Muse.</div></div>
      <div class="step"><div class="n">03</div><div class="t">Connect</div><div class="b">your own account through Muse&rsquo;s secure vault.</div></div>
    </div>
  </header>

  <div class="finder" id="finder">
    <div class="searchrow">
      <label class="search"><span class="sicon"></span><input id="q" type="search" placeholder="Search connectors, hosts, capabilities&hellip;" autocomplete="off"></label>
      <div class="count" id="count"></div>
    </div>
    <div class="chips" id="chips"></div>
  </div>

  <main class="catalog" id="catalog">
    <div class="grid" id="grid"></div>
    <div class="empty" id="empty" hidden>No connectors match. Try a different search or category.</div>
  </main>

  <section class="detail" id="detail" hidden></section>

  <section class="security" id="security">
    <div>
      <div class="slabel">security model</div>
      <h2>Auditable by design</h2>
      <p class="sbody">Every file a skill installs is public in the repo. Run <code class="inline">tools/audit.sh</code> to verify; every PR touching connectors must pass it.</p>
    </div>
    <div class="seccards">
      <div class="seccard"><div class="t">Zero secrets in the repo</div><div class="b">Skills are code and docs only.</div></div>
      <div class="seccard"><div class="t">Credentials never travel</div><div class="b">Your key lives in your private vault; skills only handle single-use surrogates.</div></div>
      <div class="seccard"><div class="t">Declared allowed hosts</div><div class="b">Each SKILL.md lists where it may send your credential. Nowhere else.</div></div>
      <div class="seccard"><div class="t">File-exact installs</div><div class="b">A Files manifest means your Muse fetches exactly those files and nothing else.</div></div>
    </div>
  </section>

  <section class="contribute">
    <div class="left">
      <h2>Missing a connector?</h2>
      <p>Someone needs a connector, builds it, and sends it in. The pattern is one <code class="lite">SKILL.md</code> plus one small script, and there&rsquo;s a template waiting for you.</p>
    </div>
    <div class="cbtns">
      <a class="btn btn-ghost" href="https://github.com/bluman1/muse-connectors/tree/main/connectors/_template">Start from the template</a>
      <a class="btn btn-accent" href="https://github.com/bluman1/muse-connectors/blob/main/CONTRIBUTING.md">How to add a connector</a>
    </div>
  </section>

  <footer class="footer">
    <div>Muse Connectors &middot; MIT licensed</div>
    <div class="fright">
      <a class="flink" href="https://github.com/bluman1/muse-connectors">Repository</a>
      <a class="flink" href="https://github.com/bluman1/muse-connectors/blob/main/INSTALL.md">One-paste install</a>
      <a class="flink" href="https://github.com/bluman1/muse-connectors/blob/main/CONTRIBUTING.md">Add a connector</a>
    </div>
  </footer>
</div>
<script>
"use strict";
const FILTER_ORDER = __FILTER_ORDER_JSON__;
const state = { q: "", cat: "All", openSlug: null, copiedSlug: null, detailSlug: null };
let connectors = [];

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

const promptFor = (slug) => `Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/${slug}/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its \`## Files\` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/${slug}/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's \`## Auth\` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.`;

function pill(c) {
  const live = c.maturity === "live";
  const label = live ? "Live-tested" : (c.maturity === "community" ? "Community" : "Draft");
  const short = live ? "Live" : label;
  return `<span class="pill ${live ? "live" : "draft"}"><span class="pfull">${label}</span><span class="pshort">${esc(short)}</span></span>`;
}

function cardHTML(c) {
  const initial = esc(c.name.trim().charAt(0).toUpperCase());
  const open = state.openSlug === c.id;
  const copied = state.copiedSlug === c.id;
  return `<article class="card" data-slug="${esc(c.id)}">
    <div class="chead">
      <div class="tile">${initial}</div>
      <div class="cmeta">
        <button class="cname" data-act="detail">${esc(c.name)}</button>
        <div class="ccat">${esc(c.category)}</div>
      </div>
      ${pill(c)}
    </div>
    <p class="cdesc">${esc(c.tagline)}</p>
    <div class="hosts"><span class="hlabel">hosts</span><span class="hval">${esc(c.hosts.join(", "))}</span></div>
    <div class="cfoot">
      <button class="btn btn-copy" data-act="copy">${copied ? "Copied \u2713" : "Copy install prompt"}</button>
      <button class="btn btn-view" data-act="view">${open ? "Hide" : "View"}</button>
    </div>
    ${open ? `<pre class="prompt">${esc(promptFor(c.id))}</pre>` : ""}
  </article>`;
}

function maturityText(c) {
  if (c.maturity === "live") return "Live-tested: installed from a raw URL on a fresh Muse and exercised against the real API.";
  if (c.maturity === "community") return "Community: contributed by the community. Review the code before connecting.";
  return "Draft: written from the provider's public docs, awaiting a live test. Review the code before connecting.";
}

function detailHTML(c) {
  const initial = esc(c.name.trim().charAt(0).toUpperCase());
  const mat = c.maturity === "live" ? "Live-tested" : (c.maturity === "community" ? "Community" : "Draft");
  return `<div class="dtop">
      <div class="crumb">connectors / ${esc(c.id)}</div>
      <button class="x" data-act="close" aria-label="Close">\u2715</button>
    </div>
    <div class="dident">
      <div class="dtile">${initial}</div>
      <div><div class="dname">${esc(c.name)}</div><div class="dsub">${esc(c.category)} &middot; ${mat}</div></div>
    </div>
    <p class="ddesc">${esc(c.tagline)}</p>
    <div class="facts">
      <div class="fact"><div class="flabel">Auth</div><div class="fval">${esc(c.auth)}</div></div>
      <div class="fact"><div class="flabel">Allowed hosts</div><div class="fval mono">${esc(c.hosts.join(", "))}</div></div>
      <div class="fact"><div class="flabel">Maturity</div><div class="fval">${maturityText(c)}</div></div>
    </div>
    <div class="plabel">Install prompt</div>
    <pre class="prompt">${esc(promptFor(c.id))}</pre>
    <div class="prow">
      <button class="btn btn-copy" data-act="copy">${state.copiedSlug === c.id ? "Copied \u2713" : "Copy install prompt"}</button>
      <a class="btn btn-audit" href="https://github.com/bluman1/muse-connectors/blob/main/connectors/${esc(c.id)}/SKILL.md">Audit SKILL.md</a>
    </div>`;
}

function matches(c) {
  if (state.cat !== "All" && c.category !== state.cat) return false;
  if (!state.q) return true;
  const hay = (c.name + " " + c.tagline + " " + c.hosts.join(" ") + " " + c.auth + " " + c.category).toLowerCase();
  return hay.indexOf(state.q) !== -1;
}

function render() {
  const detail = $("detail"), catalog = $("catalog");
  if (state.detailSlug) {
    const c = connectors.find((x) => x.id === state.detailSlug);
    catalog.hidden = true; detail.hidden = false;
    detail.innerHTML = c ? detailHTML(c) : "";
  } else {
    detail.hidden = true; catalog.hidden = false; detail.innerHTML = "";
    const list = connectors.filter(matches);
    $("count").textContent = list.length + " of " + connectors.length;
    $("grid").innerHTML = list.map(cardHTML).join("");
    $("empty").hidden = list.length > 0;
  }
}

function renderChips() {
  const present = [...new Set(connectors.map((c) => c.category))];
  const ordered = ["All"]
    .concat(FILTER_ORDER.filter((c) => present.indexOf(c) !== -1))
    .concat(present.filter((c) => FILTER_ORDER.indexOf(c) === -1).sort());
  $("chips").innerHTML = ordered.map((c) =>
    `<button class="chip${state.cat === c ? " active" : ""}" data-cat="${esc(c)}">${esc(c)}</button>`).join("");
}

function copyPrompt(slug) {
  const text = promptFor(slug);
  const done = () => {
    state.copiedSlug = slug; render();
    setTimeout(() => { if (state.copiedSlug === slug) { state.copiedSlug = null; render(); } }, 1600);
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
  } else fallbackCopy(text, done);
}
function fallbackCopy(text, done) {
  const ta = document.createElement("textarea");
  ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
  document.body.appendChild(ta); ta.select();
  try { document.execCommand("copy"); } catch (e) {}
  document.body.removeChild(ta); done();
}

function openDetail(slug, scroll) {
  state.detailSlug = slug; state.openSlug = null;
  try { history.replaceState(null, "", "#" + slug); } catch (e) {}
  render();
  if (scroll !== false) {
    const d = $("detail");
    if (d && d.scrollIntoView) d.scrollIntoView({block: "start"});
  }
}
function closeDetail() {
  state.detailSlug = null;
  try { history.replaceState(null, "", location.pathname + location.search); } catch (e) {}
  render();
}

document.addEventListener("click", (e) => {
  const chip = e.target.closest("[data-cat]");
  if (chip) {
    state.cat = chip.getAttribute("data-cat"); state.openSlug = null;
    renderChips(); render(); return;
  }
  const actEl = e.target.closest("[data-act]");
  if (!actEl) return;
  const card = e.target.closest("[data-slug]");
  const slug = card ? card.getAttribute("data-slug") : state.detailSlug;
  if (!slug) return;
  const a = actEl.getAttribute("data-act");
  if (a === "copy") copyPrompt(slug);
  else if (a === "view") { state.openSlug = state.openSlug === slug ? null : slug; render(); }
  else if (a === "detail") openDetail(slug);
  else if (a === "close") closeDetail();
});

$("q").addEventListener("input", (e) => {
  state.q = e.target.value.trim().toLowerCase();
  state.openSlug = null; render();
});

function setMobilePlaceholder() {
  $("q").placeholder = window.matchMedia("(max-width: 640px)").matches
    ? "Search connectors\u2026" : "Search connectors, hosts, capabilities\u2026";
}
window.addEventListener("resize", setMobilePlaceholder);

fetch("connectors.json").then((r) => {
  if (!r.ok) throw new Error("http " + r.status);
  return r.json();
}).then((data) => {
  connectors = data;
  setMobilePlaceholder();
  renderChips(); render();
  const h = location.hash.replace(/^#/, "");
  if (h && connectors.some((c) => c.id === h)) openDetail(h, false);
}).catch(() => {
  $("count").textContent = "";
  $("grid").innerHTML = "";
  const em = $("empty"); em.hidden = false;
  em.textContent = "Could not load the connector catalog. Check your connection and reload.";
});
</script>
</body>
</html>
"""


def build_og_image(count):
    """Regenerate docs/og-image.png with the current connector count.

    build-site.py runs whenever connectors change, so the social preview
    number can never go stale: it always matches the live catalog.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("warning: Pillow not installed, skipping og-image.png")
        return
    import math

    def find_font(bold):
        candidates = [
            "/usr/share/fonts/truetype/dejavu/"
            + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
            "/usr/share/fonts/truetype/liberation/"
            + ("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"),
        ]
        for c in candidates:
            if Path(c).exists():
                return c
        return None

    fb_path, fr_path = find_font(True), find_font(False)
    if not fb_path or not fr_path:
        print("warning: no suitable fonts found, skipping og-image.png")
        return
    avatar_src = ROOT / "docs" / "avatar" / "hatch.jpg"
    if not avatar_src.exists():
        print("warning: docs/avatar/hatch.jpg missing, skipping og-image.png")
        return

    W, H = 1200, 630
    BG = (13, 17, 23)
    BLUE = (88, 166, 255)
    TITLE_C = (230, 237, 243)
    BODY_C = (139, 148, 158)
    LINE_C = (64, 72, 82)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # avatar in blue ring
    av = Image.open(avatar_src).convert("RGB")
    s = min(av.size)
    av = av.crop(((av.width - s) // 2, (av.height - s) // 2,
                  (av.width + s) // 2, (av.height + s) // 2))
    r_in = 173
    av = av.resize((2 * r_in, 2 * r_in), Image.LANCZOS)
    mask = Image.new("L", (2 * r_in, 2 * r_in), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 2 * r_in, 2 * r_in), fill=255)
    img.paste(av, (270 - r_in, 315 - r_in), mask)

    # ring + satellite nodes
    r, rw = 178, 5
    d.ellipse((270 - r, 315 - r, 270 + r, 315 + r), outline=BLUE, width=rw)
    for nx, ny in [(365, 110), (96, 169), (443, 169),
                   (65, 410), (474, 410), (270, 541)]:
        d.ellipse((nx - 11, ny - 11, nx + 11, ny + 11), outline=BLUE, width=3)
        dx, dy = 270 - nx, 315 - ny
        ln = math.hypot(dx, dy)
        ux, uy = dx / ln, dy / ln
        d.line((nx + ux * 14, ny + uy * 14, nx + ux * 40, ny + uy * 40),
               fill=LINE_C, width=2)

    def size_for(text, target_w, font_path):
        lo, hi = 1, 300
        while lo < hi:
            mid = (lo + hi + 1) // 2
            f = ImageFont.truetype(font_path, mid)
            if d.textlength(text, font=f) <= target_w:
                lo = mid
            else:
                hi = mid - 1
        return lo

    def draw_at(x, y_top, text, font, fill):
        bb = d.textbbox((0, 0), text, font=font)
        d.text((x - bb[0], y_top - bb[1]), text, font=font, fill=fill)

    x = 522
    wordmark = "Muse Connectors"
    draw_at(x + 4, 169, wordmark,
            ImageFont.truetype(fb_path, size_for(wordmark, 614, fb_path)),
            TITLE_C)
    sub = "Auditable connector skills for Muse."
    draw_at(x - 2, 261, sub,
            ImageFont.truetype(fr_path, size_for(sub, 597, fr_path)), BODY_C)
    line1 = f"{count} open-source connectors. One pasted"
    # size from the original "50..." width so the line keeps its measure
    ref1 = "50 open-source connectors. One pasted"
    fs1 = size_for(ref1, 593, fr_path)
    draw_at(x, 340, line1, ImageFont.truetype(fr_path, fs1), BODY_C)
    line2 = "prompt installs each in your Muse."
    draw_at(x + 1, 385, line2,
            ImageFont.truetype(fr_path, size_for(line2, 576, fr_path)), BODY_C)
    d.rectangle((520, 440, 670, 447), fill=BLUE)
    url = "github.com/bluman1/muse-connectors"
    draw_at(x, 472, url,
            ImageFont.truetype(fr_path, size_for(url, 586, fr_path)), BLUE)

    out = ROOT / "docs" / "og-image.png"
    img.save(out)
    print(f"wrote {out} ({count} connectors)")


def main():
    readme = (ROOT / "README.md").read_text()
    connectors = []
    for cid, name, badge, tagline, auth, hosts in parse_entries(readme):
        raw_cat = CATEGORIES.get(cid, "Other")
        connectors.append({
            "id": cid,
            "name": name.strip(),
            "tagline": tagline.strip(),
            "auth": auth.strip(),
            "hosts": hosts,
            "maturity": {"✅": "live", "🧪": "draft", "👥": "community"}[badge],
            "category": NORMALIZE.get(raw_cat, raw_cat),
        })
    connectors.sort(key=lambda c: c["name"].lower())
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    out = docs / "connectors.json"
    out.write_text(json.dumps(connectors, indent=2) + "\n")
    html = TEMPLATE.replace("__FILTER_ORDER_JSON__", json.dumps(FILTER_ORDER))
    (docs / "index.html").write_text(html)
    stray = docs / "media-generation-last-upload-handles.json"
    if stray.exists():
        stray.unlink()
        print(f"removed stray {stray.name}")
    print(f"wrote {out} ({len(connectors)} connectors)")
    print(f"wrote {docs / 'index.html'}")
    build_og_image(len(connectors))


if __name__ == "__main__":
    main()
