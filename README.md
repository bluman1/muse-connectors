# muse-connectors

Open-source, auditable connector skills for Muse. Each connector is a skill any Muse can install with **one pasted prompt** — and every file it installs is right here for anyone to audit.

## Install any connector in one paste

1. Copy the install prompt under the connector you want below.
2. Paste it into a chat with your Muse.
3. Your Muse downloads the skill, verifies it, and walks you through connecting **your own account**. Done.

No app stores, no config files, no tokens in chat. How the one-paste install works is documented in [INSTALL.md](INSTALL.md).

## Security model — auditable by design

- **This repo contains zero secrets.** Skills are code and docs only. Run `tools/audit.sh` to verify; every PR touching `connectors/` must pass it.
- **Credentials never travel with a skill.** When you install a connector, your Muse collects your API key / OAuth through its secure credential flow and stores it in *your* private vault. The skill's code only ever handles single-use surrogates — the real key never touches the skill, this repo, or any chat transcript.
- **Each skill declares its allowed hosts** in its `SKILL.md`. The credential helper refuses to send your credential anywhere else. If a skill's host list looks wrong, that's visible right in the file you're already reading.
- **Installs are file-exact.** Every skill carries a `## Files` manifest; an installing Muse fetches exactly those files and nothing else.

## Catalog

### Slack 🧪 Draft

Read channels, post messages, search history, list users. The most-requested workplace connector.

- Auth: Slack OAuth (per-user) · Allowed hosts: `slack.com`
- Maturity: 🧪 Draft — written from Slack's public Web API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/slack/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/slack/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### GitHub 🧪 Draft

View your profile, list repos, list open issues, and create issues.

- Auth: personal access token (classic, scopes `repo` + `read:user`, per-user) · Allowed hosts: `api.github.com`
- Maturity: 🧪 Draft — written from GitHub's public REST API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/github/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/github/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Notion 🧪 Draft

Search pages and databases, read page properties, query databases (read-only).

- Auth: Notion internal integration token (per-user, created at notion.so/my-integrations) · Allowed hosts: `api.notion.com`
- Maturity: 🧪 Draft — written from Notion's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/notion/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/notion/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Linear 🧪 Draft

View your assigned issues and create issues, over Linear's GraphQL API.

- Auth: Linear personal API key (per-user, linear.app/settings/api) · Allowed hosts: `api.linear.app`
- Maturity: 🧪 Draft — written from Linear's public GraphQL API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/linear/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/linear/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Resend 🧪 Draft

Send email through Resend and check delivery status. Every send is confirmed with you first.

- Auth: Resend API key (per-user, resend.com/api-keys) · Allowed hosts: `api.resend.com`
- Maturity: 🧪 Draft — written from Resend's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/resend/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/resend/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Telegram 🧪 Draft

Send messages and read updates through your own Telegram bot. Bots can't message users who haven't started them first.

- Auth: Telegram bot token from @BotFather (per-user, single token) · Allowed hosts: `api.telegram.org`
- Maturity: 🧪 Draft — written from Telegram's public Bot API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/telegram/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/telegram/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### HubSpot 🧪 Draft

List and search contacts, create contacts, and list deals in your HubSpot CRM.

- Auth: HubSpot private app token (per-user, HubSpot Settings → Integrations → Private Apps) · Allowed hosts: `api.hubapi.com`
- Maturity: 🧪 Draft — written from HubSpot's public CRM API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/hubspot/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/hubspot/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Asana 🧪 Draft

View your assigned Asana tasks and create new ones.

- Auth: Asana personal access token (per-user, My Settings → Apps → Manage Developer Apps) · Allowed hosts: `app.asana.com`
- Maturity: 🧪 Draft — written from Asana's public REST API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/asana/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/asana/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Tavily 🧪 Draft

Fast, clean web research: one call returns an AI answer plus ranked sources with snippets. Read-only.

- Auth: Tavily API key (per-user, tavily.com) · Allowed hosts: `api.tavily.com`
- Maturity: 🧪 Draft — written from Tavily's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/tavily/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/tavily/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Stripe 🧪 Draft

Read-only Stripe visibility: balance, recent charges, customers. No write commands ship — expanding to writes is a deliberate v2.

- Auth: Stripe restricted API key (per-user, Dashboard → Developers → API keys; read-only permissions suffice) · Allowed hosts: `api.stripe.com`
- Maturity: 🧪 Draft — written from Stripe's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/stripe/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/stripe/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

---

### OpenAI 🧪 Draft

Check your OpenAI API access and list the models your key can use. Read-only.

- Auth: OpenAI API key (per-user, platform.openai.com/api-keys) · Allowed hosts: `api.openai.com`
- Maturity: 🧪 Draft — written from OpenAI's public API reference, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/openai/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/openai/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Anthropic 🧪 Draft

Check your Anthropic API access and list available Claude models. Read-only.

- Auth: Anthropic API key (per-user, console.anthropic.com) · Allowed hosts: `api.anthropic.com`
- Maturity: 🧪 Draft — written from Anthropic's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/anthropic/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/anthropic/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Hugging Face 🧪 Draft

Verify your Hugging Face account and search the model hub. Read-only.

- Auth: Hugging Face user access token (per-user, huggingface.co/settings/tokens) · Allowed hosts: `huggingface.co`
- Maturity: 🧪 Draft — written from Hugging Face's public Hub API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/huggingface/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/huggingface/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### ElevenLabs 🧪 Draft

Check your ElevenLabs subscription usage and list available voices. Read-only.

- Auth: ElevenLabs API key (per-user, elevenlabs.io/app/settings/api-keys) · Allowed hosts: `api.elevenlabs.io`
- Maturity: 🧪 Draft — written from ElevenLabs' public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/elevenlabs/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/elevenlabs/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Figma 🧪 Draft

Look up your Figma user and read file metadata. Read-only.

- Auth: Figma personal access token (per-user, Figma Settings → Personal access tokens) · Allowed hosts: `api.figma.com`
- Maturity: 🧪 Draft — written from Figma's public REST API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/figma/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/figma/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Home Assistant 🧪 Draft

Read entity states and call services on your Home Assistant instance. Service calls are confirmed first.

- Auth: Home Assistant long-lived access token (per-user, Profile → Security → Long-Lived Access Tokens) · Allowed hosts: your instance host (declared at connect time)
- Maturity: 🧪 Draft — written from Home Assistant's public REST API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/home-assistant/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/home-assistant/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Front 🧪 Draft

List Front inboxes and read conversations in your shared inbox. Read-only.

- Auth: Front API token (per-user, Front Settings → API) · Allowed hosts: `api2.frontapp.com`
- Maturity: 🧪 Draft — written from Front's public Core API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/front/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/front/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Todoist 🧪 Draft

List tasks, create tasks, and mark them done in Todoist.

- Auth: Todoist API token (per-user, Settings → Integrations → Developer) · Allowed hosts: `api.todoist.com`
- Maturity: 🧪 Draft — written from Todoist's public REST API v1 docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/todoist/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/todoist/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### ClickUp 🧪 Draft

List ClickUp workspaces and tasks, and create tasks.

- Auth: ClickUp personal API token (per-user, Settings → Apps → API Token) · Allowed hosts: `api.clickup.com`
- Maturity: 🧪 Draft — written from ClickUp's public API v2 docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/clickup/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/clickup/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Airtable 🧪 Draft

List Airtable bases, read table records, and add records.

- Auth: Airtable personal access token (per-user, airtable.com/create/tokens) · Allowed hosts: `api.airtable.com`
- Maturity: 🧪 Draft — written from Airtable's public Web API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/airtable/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/airtable/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Vercel 🧪 Draft

See your Vercel account, projects, and recent deployments.

- Auth: personal token (per-user, vercel.com/account/tokens) · Allowed hosts: `api.vercel.com`
- Maturity: 🧪 Draft — written from Vercel's public REST API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/vercel/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/vercel/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Cloudflare 🧪 Draft

List your Cloudflare zones and read DNS records. Read-only.

- Auth: API token (per-user, dash.cloudflare.com → My Profile → API Tokens; needs Zone:Read + DNS:Read) · Allowed hosts: `api.cloudflare.com`
- Maturity: 🧪 Draft — written from Cloudflare's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/cloudflare/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/cloudflare/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Supabase 🧪 Draft

List tables and query rows in your Supabase Postgres database. Read-only.

- Auth: service_role key (per-user, project Settings → API) · Allowed hosts: `<ref>.supabase.co`
- Maturity: 🧪 Draft — written from Supabase's public PostgREST docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/supabase/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/supabase/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Render 🧪 Draft

List your Render services and recent deploys. Read-only.

- Auth: API key (per-user, dashboard.render.com → Account Settings → API Keys) · Allowed hosts: `api.render.com`
- Maturity: 🧪 Draft — written from Render's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/render/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/render/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### DigitalOcean 🧪 Draft

List your DigitalOcean droplets and domains. Read-only.

- Auth: personal access token (per-user, cloud.digitalocean.com → API) · Allowed hosts: `api.digitalocean.com`
- Maturity: 🧪 Draft — written from DigitalOcean's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/digitalocean/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/digitalocean/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Netlify 🧪 Draft

List your Netlify sites and recent deploys. Read-only.

- Auth: personal access token (per-user, app.netlify.com → User settings → Applications) · Allowed hosts: `api.netlify.com`
- Maturity: 🧪 Draft — written from Netlify's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/netlify/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/netlify/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### GitLab 🧪 Draft

Your GitLab user, projects, open merge requests, and issue creation.

- Auth: personal access token (per-user, gitlab.com → Preferences → Access Tokens; `read_api` for reads, `api` to create issues) · Allowed hosts: `gitlab.com`
- Maturity: 🧪 Draft — written from GitLab's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/gitlab/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/gitlab/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Sentry 🧪 Draft

List organizations and projects, triage unresolved issues from the last 24h. Read-only.

- Auth: auth token (per-user, sentry.io → Settings → Auth Tokens) · Allowed hosts: `sentry.io`
- Maturity: 🧪 Draft — written from Sentry's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/sentry/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/sentry/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### PostHog 🧪 Draft

Your PostHog user, projects, and saved insights. Read-only.

- Auth: personal API key (per-user, PostHog Settings → Personal API keys; starts `phx_`) · Allowed hosts: configurable, default `app.posthog.com`
- Maturity: 🧪 Draft — written from PostHog's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/posthog/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/posthog/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### OpenRouter 🧪 Draft

Browse the model catalog with per-token pricing; check your key usage. Read-only.

- Auth: API key (per-user, openrouter.ai/keys) · Allowed hosts: `openrouter.ai`
- Maturity: 🧪 Draft — written from OpenRouter's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/openrouter/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/openrouter/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

*To add a connector, see [CONTRIBUTING.md](CONTRIBUTING.md).*

## Maturity badges

- ✅ **Live-tested** — installed from a raw URL on a fresh Muse and exercised against the real API.
- 🧪 **Draft** — written from the provider's public docs, awaiting a live test.
- 👥 **Community** — contributed by the community; review the code before connecting.

## License

MIT — see [LICENSE](LICENSE).
