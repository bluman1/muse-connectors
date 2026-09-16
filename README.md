# Muse Connectors

[![MIT License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Connectors](https://img.shields.io/badge/connectors-156-blue)](https://museconnectors.link/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/bluman1/muse-connectors?style=social)](https://github.com/bluman1/muse-connectors/stargazers)

Open-source, auditable connector skills for Muse. Each connector is a skill any Muse can install with **one pasted prompt**: and every file it installs is right here for anyone to audit.

## Install any connector in one paste

1. Find your connector at https://museconnectors.link/ and copy its install prompt.
2. Paste it into a chat with your Muse.
3. Your Muse downloads the skill, verifies it, and walks you through connecting **your own account**. Done.

No app stores, no config files, no tokens in chat. How the one-paste install works is documented in [INSTALL.md](INSTALL.md).

## Security model: auditable by design

- **This repo contains zero secrets.** Skills are code and docs only. Run `tools/audit.sh` to verify; every PR touching `connectors/` must pass it.
- **Credentials never travel with a skill.** When you install a connector, your Muse collects your API key / OAuth through its secure credential flow and stores it in *your* private vault. The skill's code only ever handles single-use surrogates: the real key never touches the skill, this repo, or any chat transcript.
- **Each skill declares its allowed hosts** in its `SKILL.md`. The credential helper refuses to send your credential anywhere else. If a skill's host list looks wrong, that's visible right in the file you're already reading.
- **Installs are file-exact.** Every skill carries a `## Files` manifest; an installing Muse fetches exactly those files and nothing else.

## Catalog

All 156 connectors, searchable with one-click install prompts, at **https://museconnectors.link/**. Each name links straight to its detail page.

| Connector | What it does |
|---|---|
| [Airtable](https://museconnectors.link/#airtable) | List Airtable bases, read table records, and add records. |
| [Alpha Vantage](https://museconnectors.link/#alphavantage) | Stock quotes and daily price history. Read-only. |
| [Amadeus](https://museconnectors.link/#amadeus) | Search travel with Amadeus: flight offers and prices, airport autocomplete, hotel offers, cheapest dates. |
| [Anthropic](https://museconnectors.link/#anthropic) | Check your Anthropic API access and list available Claude models. Read-only. |
| [Apollo](https://museconnectors.link/#apollo) | Search B2B contacts and enrich people and companies. |
| [Aqara](https://museconnectors.link/#aqara) | Read device attributes and send control commands to Aqara devices through the Aqara Open Cloud API: plugs and wall switches, lights (brightness, color temperature), air conditioners, supported locks, curtain motors, and saved scenes, organized by homes and rooms. Use it when the user asks about or wants to change anything in their Aqara setup. Zigbee devices need an Aqara hub online. Commands drive real physical hardware, so writes are confirmation-gated (see Operating Rules). |
| [Asana](https://museconnectors.link/#asana) | View your assigned Asana tasks and create new ones. |
| [Ashby](https://museconnectors.link/#ashby) | Search Ashby public job boards (no key needed) and read/write the Ashby ATS: candidates, jobs, applications. |
| [Attio](https://museconnectors.link/#attio) | Query CRM records, upsert by matching attribute, add notes and tasks. |
| [Beatoven.ai](https://museconnectors.link/#beatoven) | Beatoven.ai royalty-free music generation: compose tracks, poll tasks, download audio, fetch individual stems. |
| [Beehiiv](https://museconnectors.link/#beehiiv) | List publications, subscribers, and posts; add subscribers. |
| [Bluesky](https://museconnectors.link/#bluesky) | Read timelines, search posts, post and follow. |
| [Brave Search](https://museconnectors.link/#brave-search) | Independent web search from Brave's own index. Read-only. |
| [Buttondown](https://museconnectors.link/#buttondown) | Read and write Buttondown: list subscribers and emails, add subscribers, draft emails. |
| [Buzzsprout](https://museconnectors.link/#buzzsprout) | Manage podcast episodes on Buzzsprout: list and fetch episodes, create, update, or delete them, and list embed players. Use when the user wants to publish or manage podcast episodes on a Buzzsprout-hosted show. |
| [Cal.com](https://museconnectors.link/#calcom) | List bookings and event types, create bookings. |
| [Calendly](https://museconnectors.link/#calendly) | Read and manage Calendly: list scheduled events, event types, invitees, and availability schedules; cancel bookings. |
| [Canva](https://museconnectors.link/#canva) | Read and manage Canva designs through the Canva Connect API: list designs and folders, inspect a design, create designs, upload assets, and export designs. Exports are async jobs: submit with export, then poll with export-status until the job succeeds. |
| [Cartesia](https://museconnectors.link/#cartesia) | Generate spoken audio from text with Cartesia's Sonic models (40+ languages) and browse the Cartesia voice library. Reach for this when the user wants narration, voiceovers, or spoken-audio files produced from a script. |
| [Clerk](https://museconnectors.link/#clerk) | List, create, update, and delete users. |
| [ClickUp](https://museconnectors.link/#clickup) | List ClickUp workspaces and tasks, and create tasks. |
| [Cloudflare](https://museconnectors.link/#cloudflare) | List your Cloudflare zones and read DNS records. Read-only. |
| [Cloudinary](https://museconnectors.link/#cloudinary) | Manage media on Cloudinary through the Upload and Admin APIs: upload images and videos, list and inspect assets, update metadata and tags, delete assets, and check plan usage (credits, storage, bandwidth, transformations). |
| [Coda](https://museconnectors.link/#coda) | List docs, read tables and rows, add rows. Your docs as a database. |
| [Coinbase](https://museconnectors.link/#coinbase) | Read-only Coinbase Exchange account balances and history. No orders, transfers, or converts. |
| [Deepgram](https://museconnectors.link/#deepgram) | Transcribe prerecorded audio files to text (with optional diarization, summaries, topics, sentiment) and synthesize speech with Deepgram's Aura voices. Reach for this when the user has an audio file to transcribe or wants spoken audio generated from text. |
| [DeepL](https://museconnectors.link/#deepl) | Translate text between 30+ languages, check usage. |
| [DeepSeek](https://museconnectors.link/#deepseek) | Chat with DeepSeek's models and check account balance: OpenAI-compatible chat completions with thinking mode, model listing, and balance lookup via the official API. |
| [Descript](https://museconnectors.link/#descript) | Work with Descript's API (open beta): list projects, inspect Underlord/agent jobs, submit a publish job, and poll a job until it finishes. Use when the user wants to drive Descript editing or publishing programmatically. |
| [Dev.to](https://museconnectors.link/#devto) | Read and write dev.to: own profile, own articles (published, drafts, all), public articles by username, create and update articles with a safe draft default. |
| [DigitalOcean](https://museconnectors.link/#digitalocean) | List your DigitalOcean droplets and domains. Read-only. |
| [Discord](https://museconnectors.link/#discord) | Read servers and channels, send messages and DMs. |
| [DocuSign](https://museconnectors.link/#docusign) | Draft and send signature envelopes (demo environment by default), check envelope status, and download signed documents. |
| [DoorDash](https://museconnectors.link/#doordash) | Order DoorDash food and groceries from the terminal with the official agent-first dd-cli. |
| [Dub](https://museconnectors.link/#dub) | Create short links, read analytics, track conversions. |
| [ecobee](https://museconnectors.link/#ecobee) | Thermostat runtime history and energy reports, plus temperature holds with confirmation. |
| [Ecovacs](https://museconnectors.link/#ecovacs) | Control Ecovacs DEEBOT robot vacuums through the official Ecovacs Open Platform: list bound robots, read robot state and battery, start/pause/resume/stop cleaning, send the robot back to its dock, and set the sweep/mop work mode. Use when the user mentions their DEEBOT or robot vacuum. |
| [Elai](https://museconnectors.link/#elai) | Build AI avatar presenter videos with Elai: list available avatars, inspect videos and their render status, submit renders, and poll until a render finishes. Reach for this when the user wants a talking-head video generated from a script or slide deck. |
| [ElevenLabs](https://museconnectors.link/#elevenlabs) | Check ElevenLabs subscription usage, list voices, and generate text-to-speech audio (TTS needs --confirm, spends characters). |
| [Etsy](https://museconnectors.link/#etsy) | Read Etsy shop data: receipts, listings, transactions, payment ledger; create listings. |
| [Exa](https://museconnectors.link/#exa) | Neural web search with page text: one call returns ranked sources with snippets. Read-only. |
| [fal.ai](https://museconnectors.link/#fal-ai) | Generate media with fal.ai: images, video, audio, music on one key. Submit jobs to 100s of models, poll status, fetch results, upload files. |
| [Figma](https://museconnectors.link/#figma) | Look up your Figma user, read file metadata, and post comments on files. |
| [Firecrawl](https://museconnectors.link/#firecrawl) | Scrape pages, crawl sites, search the web. |
| [FLUX image API](https://museconnectors.link/#black-forest-labs) | Black Forest Labs FLUX image generation: flux-2-pro and flux-2-flex text-to-image with async polling. |
| [Fly.io](https://museconnectors.link/#flyio) | List apps and machines, manage machine lifecycle. |
| [Framer](https://museconnectors.link/#framer) | Verify a Framer project's Server API connection. Framer's Server API is WebSocket/SDK-only (there is no REST surface): the official framer-api npm package opens a long-lived connection to wss://api.framer.com/channel/headless-plugin with the header Authorization: Token <api_key>, keyed to one project. This connector's CLI performs that same official handshake as a connection check, so auth proves the API key and project pair work. |
| [Front](https://museconnectors.link/#front) | Read your Front shared inbox, and reply, assign teammates, and add tags on conversations (writes need --confirm). |
| [Gemini (media generation)](https://museconnectors.link/#gemini) | Google Gemini media generation: Nano Banana images, Imagen 4 images, Veo video, TTS, model listing. |
| [GitHub](https://museconnectors.link/#github) | View your profile, list repos, list open issues, and create issues. |
| [GitLab](https://museconnectors.link/#gitlab) | Your GitLab user, projects, open merge requests, and issue creation. |
| [Google Analytics](https://museconnectors.link/#google-analytics) | Query GA4 property reports: dimensions, metrics, realtime activity. |
| [Google Nest](https://museconnectors.link/#google-nest) | Read traits and execute commands on Google Nest devices through the Smart Device Management (SDM) API: thermostats (mode, setpoints, ambient readings), cameras and doorbells (events, live-stream generation). Use it when the user asks about their Nest thermostat, wants to change heating/cooling, or wants camera/doorbell state. Thermostat commands start or stop real HVAC, so they are confirmation-gated (see Operating Rules). |
| [Gumroad](https://museconnectors.link/#gumroad) | View your Gumroad products and sales. Read-only by design. |
| [HeyGen](https://museconnectors.link/#heygen) | HeyGen avatar and talking-head video: prompt-to-video agent, multi-scene avatar video, status polling, avatar and voice lists. |
| [Home Assistant](https://museconnectors.link/#home-assistant) | Read entity states and call services on your Home Assistant instance. Service calls are confirmed first. |
| [Homey](https://museconnectors.link/#homey) | Read device state and write capability values on a Homey Pro (local) or Homey cloud account through the Homey Web API: lights and outlets, dimmers and color, thermostats, connected locks, blinds and curtains, plus listing Flows (automations). Use it when the user asks about or wants to change anything paired to their Homey. Writes drive real physical hardware, so they are confirmation-gated (see Operating Rules). |
| [Hubitat](https://museconnectors.link/#hubitat) | Read device states and invoke capability commands on a Hubitat Elevation hub through the official Maker API app: lights and dimmers, deadbolt locks, garage door controllers, thermostats, location modes, and the Hubitat Safety Monitor (HSM). Use it when the user asks about or wants to change anything paired to their Hubitat hub. Commands drive real physical hardware, so writes are confirmation-gated (see Operating Rules). |
| [HubSpot](https://museconnectors.link/#hubspot) | List and search contacts, create contacts, and list deals in your HubSpot CRM. |
| [Hugging Face](https://museconnectors.link/#huggingface) | Verify your Hugging Face account and search the model hub. Read-only. |
| [Hume AI](https://museconnectors.link/#hume-ai) | Synthesize speech with Hume's Octave TTS models and read EVI (Empathic Voice Interface) conversational configs. Reach for this when the user wants expressive TTS audio from text or wants to inspect an EVI voice-agent configuration. |
| [Ideogram](https://museconnectors.link/#ideogram) | Ideogram text-to-image generation with the strongest text rendering in the catalog: generate, edit, remix, upscale, describe, balance. |
| [Kit](https://museconnectors.link/#kit) | Read and write Kit (ConvertKit): list subscribers, broadcasts, sequences, tags; draft broadcasts. |
| [Kling](https://museconnectors.link/#kling) | Kling AI video generation with client-side JWT auth: text-to-video, image-to-video, status polling, clip extend, lip-sync. |
| [Langfuse](https://museconnectors.link/#langfuse) | Query traces and observations, manage prompts and scores. |
| [Leaf Agriculture](https://museconnectors.link/#leaf-agriculture) | Read and manage farm data through Leaf Agriculture, a unified farm-data API that aggregates the partner-gated OEM platforms under self-serve access: John Deere, CNH Industrial (Case IH/New Holland), Climate FieldView, Trimble, Raven and AgLeader. The primitives it exposes (fields, boundaries, machine operation files for planting/harvest/application/tillage, plus as-applied irrigation) are exactly what a farmer-first fintech and supply-chain digitization product consumes. This is the practical route to partner-gated OEM data without a partnership agreement: individual provider connections need that grower's OAuth consent, which is the normal data-access model rather than a partnership gate. |
| [Lemon Squeezy](https://museconnectors.link/#lemon-squeezy) | Read Lemon Squeezy revenue: list orders, subscriptions, customers, products; create checkout links. |
| [Letta](https://museconnectors.link/#letta) | Work with Letta agent memory: list agents, read core-memory blocks, list or add archival passages, create blocks, message an agent to record memory. |
| [Linear](https://museconnectors.link/#linear) | View your assigned issues and create issues, over Linear's GraphQL API. |
| [Lob](https://museconnectors.link/#lob) | Send physical mail through Lob's Print and Mail API: verify US addresses; create postcards and letters that get printed and mailed; list what was sent; cancel a piece while it is still before production. Reach for this when the user wants a real letter or postcard in the mail rather than an email. |
| [Loops](https://museconnectors.link/#loops) | Manage email contacts, trigger loops, send transactional email. |
| [Luma (Dream Machine API)](https://museconnectors.link/#luma) | Luma Dream Machine video generation: text-to-video and image-to-video, status polling, cancel, image upload. |
| [Mastodon](https://museconnectors.link/#mastodon) | Read and write Mastodon: verify the account, list own posts and followers, publish toots with native scheduling, upload media. |
| [mem0](https://museconnectors.link/#mem0) | Mem0 memory CLI: add memories from messages, semantic search, read or delete memories, poll async events. |
| [Mercury](https://museconnectors.link/#mercury) | View Mercury bank accounts and transactions. Read-only by design. |
| [Mistral AI](https://museconnectors.link/#mistral) | Mistral AI's La Plateforme API: chat completions, embeddings, document OCR, and model listing via Bearer API key. |
| [Monday](https://museconnectors.link/#monday) | List boards, read items, create items. Project management over GraphQL. |
| [Moonraker](https://museconnectors.link/#moonraker) | Control a Klipper-based 3D printer through the Moonraker API server (the backend behind Mainsail, Fluidd and RatOS): read server and print status, list and upload gcode files, start/pause/resume/cancel prints, trigger the emergency stop, toggle smart-plug devices, and (gated) run raw G-code. Use when the user mentions Moonraker, Klipper, Mainsail, or Fluidd. |
| [n8n](https://museconnectors.link/#n8n) | List and manage workflows, read executions. |
| [Neon](https://museconnectors.link/#neon) | Inspect Neon serverless Postgres projects, branches, and databases. Branch create and delete need exact-match confirmation; connection passwords are masked. |
| [Netlify](https://museconnectors.link/#netlify) | List your Netlify sites and recent deploys. Read-only. |
| [NewsAPI](https://museconnectors.link/#newsapi) | Top headlines and full-text news search. Read-only. |
| [Notion](https://museconnectors.link/#notion) | Search and query Notion, plus create pages, append blocks, and update page properties (writes need --confirm). |
| [OctoPrint](https://museconnectors.link/#octoprint) | Control an OctoPrint 3D printer over its local REST API: read printer state and temperatures, monitor print progress, start/pause/cancel/restart jobs, upload and select gcode files, set hotend and bed temperatures, jog or home axes, and (gated) run raw G-code. Use when the user mentions their OctoPrint instance or a printer it drives. |
| [OpenAI](https://museconnectors.link/#openai) | Check your OpenAI API access and list the models your key can use. Read-only. |
| [OpenRouter](https://museconnectors.link/#openrouter) | Browse the model catalog with per-token pricing; check your key usage. Read-only. |
| [OpenWeatherMap](https://museconnectors.link/#openweathermap) | Current weather and 5-day forecast for any city. Read-only. |
| [OpusClip](https://museconnectors.link/#opusclip) | Turn long-form videos into short, captioned, vertical clips with OpusClip's API: create a clip project from a video URL, check the project's render status, and list the resulting clips with their virality scores. API access requires a Pro-tier (or higher) OpusClip plan and is in beta. |
| [Oura](https://museconnectors.link/#oura) | Read Oura Ring health data: sleep scores, sleep sessions, readiness, workouts, and SpO2. |
| [Paddle](https://museconnectors.link/#paddle) | View Paddle transactions and customers. Read-only by design. |
| [Patreon](https://museconnectors.link/#patreon) | Read Patreon campaigns, members, tiers, and identity (read-only). |
| [PayPal](https://museconnectors.link/#paypal) | Check PayPal balances and search transactions read-only. No payments, payouts, or transfers. |
| [Perplexity](https://museconnectors.link/#perplexity) | Ask questions with citations, search the web. |
| [Pexels](https://museconnectors.link/#pexels) | Search Pexels' royalty-free stock library: find photos and videos by keyword, browse curated/trending photos and popular videos, look up a single photo or video, and read collection contents. The Pexels API is read-only, so this connector cannot change anything. |
| [Philips Hue](https://museconnectors.link/#philips-hue) | Control Philips Hue lights locally: list lights and rooms, set brightness/color, activate scenes, read sensors. |
| [Pipedrive](https://museconnectors.link/#pipedrive) | List deals and contacts, create deals. CRM for your pipeline. |
| [Plaid](https://museconnectors.link/#plaid) | Sync bank transactions and check account balances through Plaid. |
| [Plain](https://museconnectors.link/#plain) | Find customers, manage support threads. |
| [PlayHT](https://museconnectors.link/#playht) | Generate spoken audio from text with PlayHT voices, browse stock and cloned voices, and create instant voice clones. Reach for this when the user wants narration or voiceovers, a voice library lookup, or a voice cloned from a sample. |
| [Podbean](https://museconnectors.link/#podbean) | Manage podcast hosting on Podbean: list podcasts and their episodes, create, update, or delete episodes. Podbean's analytics endpoints are a differentiator; the download/analytics report paths are not yet mapped in this connector. |
| [Polar](https://museconnectors.link/#polar) | Read Polar orders, subscriptions, products, and customers; create checkouts and refunds. |
| [Polymarket](https://museconnectors.link/#polymarket) | Read-only prediction market data: events, markets, prices, order books. No trading, no API key needed. |
| [PostHog](https://museconnectors.link/#posthog) | Your PostHog user, projects, and saved insights. Read-only. |
| [Postmark](https://museconnectors.link/#postmark) | Send transactional email, check delivery and bounces. |
| [Printful](https://museconnectors.link/#printful) | Read Printful products and orders, create orders and mockups. |
| [Prusa Connect](https://museconnectors.link/#prusa-connect) | Read Prusa 3D printer state through the official Prusa Connect cloud API: list printers and their state, list jobs and files, view cameras, read print statistics, and upload gcode files to printer storage. Use when the user mentions Prusa Connect or a networked Prusa printer (MK3/MK4/CORE One). |
| [Rachio](https://museconnectors.link/#rachio) | Control a Rachio smart irrigation controller through the public Rachio API. Check who is signed in, see what the controller is currently running, start watering a specific zone for a set number of seconds, and shut all water off in an emergency. Reach for this when the user asks about sprinklers, watering schedules, or irrigation zones. |
| [Railway](https://museconnectors.link/#railway) | List projects and deployments, set variables, redeploy. |
| [Ramp](https://museconnectors.link/#ramp) | Read-only view of corporate spend: transactions, cards and limits, users, departments. No spend actions by design. |
| [Readwise](https://museconnectors.link/#readwise) | Search your highlights and books, save new highlights. |
| [remove.bg](https://museconnectors.link/#remove-bg) | Remove the background from an image with the remove.bg API: submit a local file or an image URL, get back a transparent PNG saved to a local path. Also check the account's remaining credits. |
| [Render](https://museconnectors.link/#render) | List your Render services and recent deploys. Read-only. |
| [Replicate](https://museconnectors.link/#replicate) | Run AI models, poll predictions. |
| [Resend](https://museconnectors.link/#resend) | Send email through Resend and check delivery status. Every send is confirmed with you first. |
| [Restream](https://museconnectors.link/#restream) | Manage Restream multistreaming: read your profile, list streaming destinations (channels), toggle destinations or edit channel metadata, and retrieve your stream key. Use when the user wants to control where a livestream goes without opening the Restream dashboard. |
| [Runway](https://museconnectors.link/#runway) | Runway developer API: text-to-video, image-to-video, task polling, video upscale, lip-sync. |
| [SendGrid](https://museconnectors.link/#sendgrid) | Send email, check stats and profile. |
| [Sentry](https://museconnectors.link/#sentry) | List organizations and projects, triage unresolved issues from the last 24h, and resolve/archive/assign issues. |
| [Shippo](https://museconnectors.link/#shippo) | Ship through many carriers (USPS, UPS, FedEx, DHL and others) with one API: get rates for a shipment; buy a printable postage label; track a parcel; refund unused labels. Reach for this when the user needs to price or purchase shipping for a package. |
| [Shopify](https://museconnectors.link/#shopify) | View orders, products, customers; create products and discounts with confirmation. No order or customer writes, ever. |
| [Slack](https://museconnectors.link/#slack) | Read channels, post messages, list users. The most-requested workplace connector. |
| [Smartcar](https://museconnectors.link/#smartcar) | Read and control connected cars across many brands (Tesla, Ford, GM, Toyota, BMW, Hyundai and others) through one standardized API. Read odometer, location, charge and battery level, fuel level and tire pressure; lock/unlock doors; start/stop charging; set charge limits and schedules; route the built-in navigation. Use when the user mentions their car and the brand has no dedicated connector here, or asks for cross-brand vehicle telemetry and control. |
| [SmartThings](https://museconnectors.link/#smartthings) | Read device status and issue capability commands across a Samsung SmartThings account: locations, devices, switches, dimmers, locks, thermostats, sirens, garage door controllers, and window shades. Use it when the user asks about or wants to change the state of anything paired to their SmartThings hub or cloud account. This connector drives real physical hardware, so every write is confirmation-gated (see Operating Rules). |
| [Spotify](https://museconnectors.link/#spotify) | Read your profile, playlists, top tracks and artists, and search the catalog. Playlist and library writes need your confirmation. |
| [Square](https://museconnectors.link/#square) | Work with a Square seller account: list locations and payments, create orders, push a checkout to a physical Square Terminal for in-person payment, charge a payment source directly, cancel a pending Terminal checkout, and refund a payment. Reach for this when the user needs to take or return money through Square. |
| [Stripe](https://museconnectors.link/#stripe) | Read-only Stripe visibility: balance, recent charges, customers. No write commands ship: expanding to writes is a deliberate v2. |
| [Supabase](https://museconnectors.link/#supabase) | List tables, query rows, and insert/update/delete rows in your Supabase Postgres database. |
| [Supermemory](https://museconnectors.link/#supermemory) | Store and recall with Supermemory: add memories and documents, hybrid search, upload files, tune settings. |
| [SwitchBot](https://museconnectors.link/#switchbot) | Read status and send commands to SwitchBot devices over the official OpenAPI v1.1: SwitchBot Bot (physical button presser), SwitchBot Lock, Curtain and Blind Tilt motors, plugs, lights, air conditioners, infrared remotes, and saved scenes. Use it when the user asks about or wants to change anything in their SwitchBot setup. Commands drive real physical hardware, so writes are confirmation-gated (see Operating Rules). |
| [Tally](https://museconnectors.link/#tally) | List forms, read submissions, manage form blocks. |
| [Tavily](https://museconnectors.link/#tavily) | Fast, clean web research: one call returns an AI answer plus ranked sources with snippets. Read-only. |
| [Telegram](https://museconnectors.link/#telegram) | Send messages and read updates through your own Telegram bot. Bots can't message users who haven't started them first. |
| [Tesla Fleet API (vehicles)](https://museconnectors.link/#tesla-fleet-api) | Control Tesla vehicles through the official Tesla Fleet API: read live vehicle state, wake a sleeping car, and send signed commands (lock/unlock, keyless drive, charge control, preconditioning, honk/flash, trunk, sentry/valet, speed limit, navigation). Use when the user mentions their Tesla car or asks for vehicle actuation. |
| [Tesla Powerwall](https://museconnectors.link/#tesla-powerwall) | Monitor and control Tesla energy sites (Powerwall, solar) through the official Tesla Fleet API. Read live power flows, battery state, and site settings; change backup reserve percentage, operation mode, and Storm Watch. Use when the user mentions their Powerwall, Tesla energy site, backup reserve, or storm mode. |
| [TickTick](https://museconnectors.link/#ticktick) | Read and write TickTick: list projects and tasks, create tasks, complete and delete tasks. |
| [TikTok](https://museconnectors.link/#tiktok) | Read your TikTok profile and video list. API access needs TikTok app approval first, and posting is not shipped. |
| [Todoist](https://museconnectors.link/#todoist) | List tasks, create tasks, and mark them done in Todoist. |
| [Transistor](https://museconnectors.link/#transistor) | Manage podcast hosting on Transistor.fm: list shows and episodes, create draft episodes, update or delete them, and upload episode audio via Transistor's two-step upload flow. Use when the user wants to publish or manage podcast episodes programmatically. |
| [trigger.dev](https://museconnectors.link/#triggerdev) | Trigger background jobs, list runs, manage schedules. |
| [Tuya](https://museconnectors.link/#tuya) | Read status and send control commands to Tuya Cloud / Smart Life devices: smart plugs and switches, lights, thermostats, curtain motors, and supported smart locks, plus executing saved scenes. Use it when the user asks about or wants to change anything paired through the Tuya or Smart Life app. Commands drive real physical hardware, so writes are confirmation-gated (see Operating Rules). |
| [Twitch](https://museconnectors.link/#twitch) | Read and write Twitch via the Helix API: channel profile, follower stats, live stream status, past videos, channel title and game updates, clip creation. |
| [Typeform](https://museconnectors.link/#typeform) | List forms and responses, create forms, and manage response webhooks with confirmation. |
| [Uber Direct](https://museconnectors.link/#uber-direct) | Dispatch same-day couriers through Uber Direct for food, retail, grocery, or parcel deliveries. Get a price and time quote without dispatching anyone, create a delivery when the user approves, check its status, and cancel a pending one. Reach for this when the user needs something picked up and dropped off locally today. |
| [UniFi Protect](https://museconnectors.link/#unifi-protect) | Read camera state and still snapshots from a local UniFi Protect console (Protect 5.3+) through the official Integration API, and adjust camera settings: PTZ position, flood lights, chimes, talkback. Use it when the user asks what their UniFi cameras see, wants a snapshot saved, or wants to change camera behavior. Everything runs against the local console; there is no cloud dependency. |
| [Unsplash](https://museconnectors.link/#unsplash) | Search Unsplash's free stock photo library, browse the latest photos, look up a photo's details, browse a photographer's portfolio or a topic, and download an image while honoring Unsplash's API guidelines. At the Client-ID tier this connector is read-only. |
| [Upstash](https://museconnectors.link/#upstash) | Run Redis commands over REST. |
| [Vapi](https://museconnectors.link/#vapi) | Manage voice AI assistants, phone numbers, and calls. Outbound calls need exact-match confirmation; test numbers by default. |
| [VEED](https://museconnectors.link/#veed) | Remove backgrounds from video with VEED's direct developer API (POST /v1/video/background-remove): standard quality, fast throughput and green-screen chroma-key with spill suppression. Outputs are VP9-with-alpha or H.264 RGB+alpha, up to 4K. |
| [Vercel](https://museconnectors.link/#vercel) | See your Vercel account, projects, and recent deployments. |
| [Webflow](https://museconnectors.link/#webflow) | Work with the Webflow Data API v2: list sites, inspect site details, browse CMS collections and items, create/update/delete CMS items, and publish a site. Uses a per-site token from Site Settings. |
| [Wise](https://museconnectors.link/#wise) | View Wise profiles and multi-currency balances. Read-only by design. |
| [X](https://museconnectors.link/#x) | Post, search, like, DM. Note: no usable free read tier. |
| [xAI (Grok)](https://museconnectors.link/#xai) | Query Grok chat completions and list available Grok models through xAI's OpenAI-compatible API, with per-call token usage surfaced so cost is always visible. |
| [YNAB](https://museconnectors.link/#ynab) | Read and write YNAB budgets: list budgets, accounts, balances, transactions, and categories; record transactions. |
| [YouTube](https://museconnectors.link/#youtube) | Read channels and videos, search, plus uploads and comments with confirmation. |
| [Zep](https://museconnectors.link/#zep) | Work with Zep's temporal memory: create users and threads, append messages, read distilled facts and history. |

*To add a connector, see [CONTRIBUTING.md](CONTRIBUTING.md).*

## Something not working?

A connector misbehaving is a bug report, not a dead end. [Open an issue](https://github.com/bluman1/muse-connectors/issues/new) with:

1. The connector name in the title, e.g. `[slack] auth fails on fresh install`
2. What you ran and what happened
3. The error output (paste as much of the log as you can)

Every report gets read, and fixes ship fast.

## License

MIT: see [LICENSE](LICENSE).
