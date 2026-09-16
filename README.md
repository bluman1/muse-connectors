# muse-connectors

Open-source, auditable connector skills for Muse. Each connector is a skill any Muse can install with **one pasted prompt**: and every file it installs is right here for anyone to audit.

## Install any connector in one paste

1. Copy the install prompt under the connector you want below.
2. Paste it into a chat with your Muse.
3. Your Muse downloads the skill, verifies it, and walks you through connecting **your own account**. Done.

No app stores, no config files, no tokens in chat. How the one-paste install works is documented in [INSTALL.md](INSTALL.md).

## Security model: auditable by design

- **This repo contains zero secrets.** Skills are code and docs only. Run `tools/audit.sh` to verify; every PR touching `connectors/` must pass it.
- **Credentials never travel with a skill.** When you install a connector, your Muse collects your API key / OAuth through its secure credential flow and stores it in *your* private vault. The skill's code only ever handles single-use surrogates: the real key never touches the skill, this repo, or any chat transcript.
- **Each skill declares its allowed hosts** in its `SKILL.md`. The credential helper refuses to send your credential anywhere else. If a skill's host list looks wrong, that's visible right in the file you're already reading.
- **Installs are file-exact.** Every skill carries a `## Files` manifest; an installing Muse fetches exactly those files and nothing else.

## Catalog

### Slack ✅ Live-tested

Read channels, post messages, list users. The most-requested workplace connector.

- Auth: Slack OAuth (per-user) · Allowed hosts: `slack.com`
- Maturity: ✅ Live-tested: installed from a raw URL and exercised against the real Slack API.

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
- Maturity: 🧪 Draft: written from GitHub's public REST API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Notion's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Linear's public GraphQL API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Resend's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Telegram's public Bot API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from HubSpot's public CRM API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Asana's public REST API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Tavily's public API docs, not yet live-tested end-to-end.

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

Read-only Stripe visibility: balance, recent charges, customers. No write commands ship: expanding to writes is a deliberate v2.

- Auth: Stripe restricted API key (per-user, Dashboard → Developers → API keys; read-only permissions suffice) · Allowed hosts: `api.stripe.com`
- Maturity: 🧪 Draft: written from Stripe's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from OpenAI's public API reference, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Anthropic's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Hugging Face's public Hub API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from ElevenLabs' public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Figma's public REST API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Home Assistant's public REST API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Front's public Core API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Todoist's public REST API v1 docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from ClickUp's public API v2 docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Airtable's public Web API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Vercel's public REST API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Cloudflare's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Supabase's public PostgREST docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Render's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from DigitalOcean's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Netlify's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from GitLab's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from Sentry's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from PostHog's public API docs, not yet live-tested end-to-end.

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
- Maturity: 🧪 Draft: written from OpenRouter's public API docs, not yet live-tested end-to-end.

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

### Mercury 🧪 Draft

View Mercury bank accounts and transactions. Read-only by design.
- Auth: Mercury API token (per-user, app.mercury.com → Settings → API Tokens; a Read-Only token suffices) · Allowed hosts: `api.mercury.com`
- Maturity: 🧪 Draft: written from Mercury's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/mercury/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/mercury/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Wise 🧪 Draft

View Wise profiles and multi-currency balances. Read-only by design.
- Auth: Wise personal API token (per-user, wise.com → Settings → API tokens) · Allowed hosts: `api.wise.com`
- Maturity: 🧪 Draft: written from Wise's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/wise/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/wise/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Shopify 🧪 Draft

View open orders, products, and customers in your Shopify store. Read-only by design.
- Auth: Shopify Admin API access token (per-user, Shopify admin → Apps → Develop apps → custom app; scopes read_orders/read_products/read_customers) · Allowed hosts: `<your-shop>.myshopify.com` (your store's domain)
- Maturity: 🧪 Draft: written from Shopify's Admin API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/shopify/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/shopify/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Gumroad 🧪 Draft

View your Gumroad products and sales. Read-only by design.
- Auth: Gumroad access token (per-user, app.gumroad.com → Settings → Advanced) · Allowed hosts: `api.gumroad.com`
- Maturity: 🧪 Draft: written from Gumroad's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/gumroad/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/gumroad/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Paddle 🧪 Draft

View Paddle transactions and customers. Read-only by design.
- Auth: Paddle API key (per-user, Paddle Dashboard → Developer Tools → Authentication) · Allowed hosts: `api.paddle.com`
- Maturity: 🧪 Draft: written from Paddle's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/paddle/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/paddle/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Exa 🧪 Draft

Neural web search with page text: one call returns ranked sources with snippets. Read-only.
- Auth: Exa API key (per-user, dashboard.exa.ai/api-keys) · Allowed hosts: `api.exa.ai`
- Maturity: 🧪 Draft: written from Exa's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/exa/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/exa/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Brave Search 🧪 Draft

Independent web search from Brave's own index. Read-only.
- Auth: Brave Search API key (per-user, brave.com/search/api; free tier 2,000 queries/month) · Allowed hosts: `api.search.brave.com`
- Maturity: 🧪 Draft: written from Brave Search's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/brave-search/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/brave-search/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### OpenWeatherMap 🧪 Draft

Current weather and 5-day forecast for any city. Read-only.
- Auth: OpenWeatherMap API key (per-user, openweathermap.org → API keys; free tier fine) · Allowed hosts: `api.openweathermap.org`
- Maturity: 🧪 Draft: written from OpenWeatherMap's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/openweathermap/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/openweathermap/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Alpha Vantage 🧪 Draft

Stock quotes and daily price history. Read-only.
- Auth: Alpha Vantage API key (per-user, alphavantage.co/support/#api-key; free tier 25 calls/day) · Allowed hosts: `www.alphavantage.co`
- Maturity: 🧪 Draft: written from Alpha Vantage's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/alphavantage/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/alphavantage/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### NewsAPI 🧪 Draft

Top headlines and full-text news search. Read-only.
- Auth: NewsAPI key (per-user, newsapi.org/register; free tier 100 requests/day) · Allowed hosts: `newsapi.org`
- Maturity: 🧪 Draft: written from NewsAPI's public docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/newsapi/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/newsapi/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Coda 🧪 Draft

List docs, read tables and rows, add rows. Your docs as a database.

- Auth: personal API token (per-user) · Allowed hosts: `coda.io`
- Maturity: 🧪 Draft: written from Coda's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/coda/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/coda/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Readwise 🧪 Draft

Search your highlights and books, save new highlights.

- Auth: access token (per-user, from readwise.io/access_token) · Allowed hosts: `readwise.io`
- Maturity: 🧪 Draft: written from Readwise's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/readwise/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/readwise/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Monday 🧪 Draft

List boards, read items, create items. Project management over GraphQL.

- Auth: personal API token (per-user) · Allowed hosts: `api.monday.com`
- Maturity: 🧪 Draft: written from monday.com's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/monday/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/monday/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Cal.com 🧪 Draft

List bookings and event types, create bookings.

- Auth: personal API key (per-user, keys start `cal_` / `cal_live_`) · Allowed hosts: `api.cal.com`
- Maturity: 🧪 Draft: written from Cal.com's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/calcom/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/calcom/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### DeepL 🧪 Draft

Translate text between 30+ languages, check usage.

- Auth: API key (per-user; free keys use api-free.deepl.com, paid keys use api.deepl.com) · Allowed hosts: `api-free.deepl.com`, `api.deepl.com`
- Maturity: 🧪 Draft: written from DeepL's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/deepl/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/deepl/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### SendGrid 🧪 Draft

Send email, check stats and profile.

- Auth: API key (per-user) · Allowed hosts: `api.sendgrid.com`
- Maturity: 🧪 Draft: written from SendGrid's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/sendgrid/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/sendgrid/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Postmark 🧪 Draft

Send transactional email, check delivery and bounces.

- Auth: server API token (per-user) · Allowed hosts: `api.postmarkapp.com`
- Maturity: 🧪 Draft: written from Postmark's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/postmark/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/postmark/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Beehiiv 🧪 Draft

List publications, subscribers, and posts; add subscribers.

- Auth: API key (per-user; Scale plan or higher) · Allowed hosts: `api.beehiiv.com`
- Maturity: 🧪 Draft: written from beehiiv's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/beehiiv/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/beehiiv/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Pipedrive 🧪 Draft

List deals and contacts, create deals. CRM for your pipeline.

- Auth: personal API token (per-user) + company subdomain · Allowed hosts: `{company}.pipedrive.com`
- Maturity: 🧪 Draft: written from Pipedrive's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/pipedrive/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/pipedrive/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Apollo 🧪 Draft

Search B2B contacts and enrich people and companies.

- Auth: API key (per-user; Professional plan or higher) · Allowed hosts: `api.apollo.io`
- Maturity: 🧪 Draft: written from Apollo's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/apollo/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/apollo/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Discord 🧪 Draft

Read servers and channels, send messages and DMs.

- Auth: Bot token (per-server install) · Allowed hosts: `discord.com`
- Maturity: 🧪 Draft: written from Discord's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/discord/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/discord/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Loops 🧪 Draft

Manage email contacts, trigger loops, send transactional email.

- Auth: API key (per-user) · Allowed hosts: `app.loops.so`
- Maturity: 🧪 Draft: written from Loops's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/loops/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/loops/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Dub 🧪 Draft

Create short links, read analytics, track conversions.

- Auth: API key (per-workspace) · Allowed hosts: `api.dub.co`
- Maturity: 🧪 Draft: written from Dub's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/dub/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/dub/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Tally 🧪 Draft

List forms, read submissions, manage form blocks.

- Auth: API key (per-user; free on all plans) · Allowed hosts: `api.tally.so`
- Maturity: 🧪 Draft: written from Tally's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/tally/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/tally/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Firecrawl 🧪 Draft

Scrape pages, crawl sites, search the web.

- Auth: API key (per-user) · Allowed hosts: `api.firecrawl.dev`
- Maturity: 🧪 Draft: written from Firecrawl's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/firecrawl/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/firecrawl/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Perplexity 🧪 Draft

Ask questions with citations, search the web.

- Auth: API key (per-user) · Allowed hosts: `api.perplexity.ai`
- Maturity: 🧪 Draft: written from Perplexity's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/perplexity/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/perplexity/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Replicate 🧪 Draft

Run AI models, poll predictions.

- Auth: API key (per-user) · Allowed hosts: `api.replicate.com`
- Maturity: 🧪 Draft: written from Replicate's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/replicate/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/replicate/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Neon 🧪 Draft

Manage Postgres projects, branches, and compute.

- Auth: API key (per-user) · Allowed hosts: `console.neon.tech`
- Maturity: 🧪 Draft: written from Neon's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/neon/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/neon/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Upstash 🧪 Draft

Run Redis commands over REST.

- Auth: Per-database token (host declared at connect time) · Allowed hosts: `*.upstash.io`
- Maturity: 🧪 Draft: written from Upstash's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/upstash/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/upstash/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Clerk 🧪 Draft

List, create, update, and delete users.

- Auth: Secret API key (per-project) · Allowed hosts: `api.clerk.com`
- Maturity: 🧪 Draft: written from Clerk's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/clerk/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/clerk/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Attio 🧪 Draft

Query CRM records, upsert by matching attribute, add notes and tasks.

- Auth: API key (per-workspace) · Allowed hosts: `api.attio.com`
- Maturity: 🧪 Draft: written from Attio's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/attio/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/attio/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Trigger.dev 🧪 Draft

Trigger background jobs, list runs, manage schedules.

- Auth: API key (per-environment) · Allowed hosts: `api.trigger.dev`
- Maturity: 🧪 Draft: written from Trigger.dev's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/triggerdev/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/triggerdev/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### X 🧪 Draft

Post, search, like, DM. Note: no usable free read tier.

- Auth: OAuth2 PKCE (per-user; paid read access) · Allowed hosts: `api.x.com`
- Maturity: 🧪 Draft: written from X's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/x/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/x/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### YouTube 🧪 Draft

Look up channels and videos, search (reads only).

- Auth: API key (per-user; reads only) · Allowed hosts: `www.googleapis.com`
- Maturity: 🧪 Draft: written from YouTube's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/youtube/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/youtube/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Plain 🧪 Draft

Find customers, manage support threads.

- Auth: Machine-user API key · Allowed hosts: `core-api.uk.plain.com`
- Maturity: 🧪 Draft: written from Plain's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/plain/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/plain/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Railway 🧪 Draft

List projects and deployments, set variables, redeploy.

- Auth: API token (account or workspace) · Allowed hosts: `backboard.railway.com`
- Maturity: 🧪 Draft: written from Railway's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/railway/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/railway/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Fly.io 🧪 Draft

List apps and machines, manage machine lifecycle.

- Auth: API token (app or org scoped) · Allowed hosts: `api.machines.dev`
- Maturity: 🧪 Draft: written from Fly.io's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/flyio/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/flyio/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### n8n 🧪 Draft

List and manage workflows, read executions.

- Auth: API key (instance; host declared at connect time) · Allowed hosts: your n8n instance host
- Maturity: 🧪 Draft: written from n8n's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/n8n/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/n8n/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Langfuse 🧪 Draft

Query traces and observations, manage prompts and scores.

- Auth: Public+secret key pair (per-project; host declared at connect time) · Allowed hosts: `cloud.langfuse.com`, `us.cloud.langfuse.com`
- Maturity: 🧪 Draft: written from Langfuse's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/langfuse/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/langfuse/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Bluesky 🧪 Draft

Read timelines, search posts, post and follow.

- Auth: App password (per-account; session-based) · Allowed hosts: `bsky.social`
- Maturity: 🧪 Draft: written from Bluesky's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/bluesky/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/bluesky/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Mem0 🧪 Draft

Mem0 memory CLI: add memories from messages, semantic search, read or delete memories, poll async events.

- Auth: API key via the secure credential flow · Allowed hosts: `api.mem0.ai`
- Maturity: 🧪 Draft: written from Mem0's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/mem0/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/mem0/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Supermemory 🧪 Draft

Store and recall with Supermemory: add memories and documents, hybrid search, upload files, tune settings.

- Auth: API key via the secure credential flow · Allowed hosts: `api.supermemory.ai`
- Maturity: 🧪 Draft: written from Supermemory's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/supermemory/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/supermemory/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Zep 🧪 Draft

Work with Zep's temporal memory: create users and threads, append messages, read distilled facts and history.

- Auth: API key via the secure credential flow · Allowed hosts: `api.getzep.com`
- Maturity: 🧪 Draft: written from Zep's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/zep/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/zep/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Letta 🧪 Draft

Work with Letta agent memory: list agents, read core-memory blocks, list or add archival passages, create blocks, message an agent to record memory.

- Auth: API key via the secure credential flow · Allowed hosts: `api.letta.com`
- Maturity: 🧪 Draft: written from Letta's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/letta/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/letta/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### TickTick 🧪 Draft

Read and write TickTick: list projects and tasks, create tasks, complete and delete tasks.

- Auth: OAuth 2.0 via the secure credential flow · Allowed hosts: `api.ticktick.com`
- Maturity: 🧪 Draft: written from TickTick's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/ticktick/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/ticktick/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### YNAB 🧪 Draft

Read and write YNAB budgets: list budgets, accounts, balances, transactions, and categories; record transactions.

- Auth: OAuth 2.0 via the secure credential flow · Allowed hosts: `api.ynab.com`
- Maturity: 🧪 Draft: written from YNAB's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/ynab/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/ynab/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Oura 🧪 Draft

Read Oura Ring health data: sleep scores, sleep sessions, readiness, workouts, and SpO2.

- Auth: OAuth 2.0 via the secure credential flow · Allowed hosts: `api.ouraring.com`
- Maturity: 🧪 Draft: written from Oura's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/oura/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/oura/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Philips Hue 🧪 Draft

Control Philips Hue lights locally: list lights and rooms, set brightness/color, activate scenes, read sensors.

- Auth: Bridge pairing (local) or OAuth2 (remote) · Allowed hosts: derived from `--host` at runtime (the bridge's LAN IP or hostname); the CLI refuses to send the key anywhere else
- Maturity: 🧪 Draft: written from Philips Hue's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/philips-hue/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/philips-hue/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Calendly 🧪 Draft

Read and manage Calendly: list scheduled events, event types, invitees, and availability schedules; cancel bookings.

- Auth: OAuth 2.0 via the secure credential flow · Allowed hosts: `api.calendly.com`
- Maturity: 🧪 Draft: written from Calendly's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/calendly/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/calendly/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Amadeus 🧪 Draft

Search travel with Amadeus: flight offers and prices, airport autocomplete, hotel offers, cheapest dates.

- Auth: OAuth 2.0 client credentials via the secure credential flow · Allowed hosts: `test.api.amadeus.com`, `api.amadeus.com`
- Maturity: 🧪 Draft: written from Amadeus's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/amadeus/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/amadeus/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Buttondown 🧪 Draft

Read and write Buttondown: list subscribers and emails, add subscribers, draft emails.

- Auth: API key via the secure credential flow · Allowed hosts: `api.buttondown.com`
- Maturity: 🧪 Draft: written from Buttondown's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/buttondown/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/buttondown/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Lemon Squeezy 🧪 Draft

Read Lemon Squeezy revenue: list orders, subscriptions, customers, products; create checkout links.

- Auth: API key via the secure credential flow · Allowed hosts: `api.lemonsqueezy.com`
- Maturity: 🧪 Draft: written from Lemon Squeezy's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/lemon-squeezy/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/lemon-squeezy/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Polar 🧪 Draft

Read Polar orders, subscriptions, products, and customers; create checkouts and refunds.

- Auth: Organization Access Token via the secure credential flow · Allowed hosts: `api.polar.sh`, `sandbox-api.polar.sh`
- Maturity: 🧪 Draft: written from Polar's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/polar/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/polar/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Etsy 🧪 Draft

Read Etsy shop data: receipts, listings, transactions, payment ledger; create listings.

- Auth: OAuth 2.0 via the secure credential flow · Allowed hosts: `openapi.etsy.com`
- Maturity: 🧪 Draft: written from Etsy's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/etsy/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/etsy/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Kit 🧪 Draft

Read and write Kit (ConvertKit): list subscribers, broadcasts, sequences, tags; draft broadcasts.

- Auth: API key via the secure credential flow · Allowed hosts: `api.kit.com`
- Maturity: 🧪 Draft: written from Kit's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/kit/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/kit/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Printful 🧪 Draft

Read Printful products and orders, create orders and mockups.

- Auth: personal access token via the secure credential flow · Allowed hosts: `api.printful.com`
- Maturity: 🧪 Draft: written from Printful's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/printful/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/printful/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Patreon 🧪 Draft

Read Patreon campaigns, members, tiers, and identity (read-only).

- Auth: Creator's Access Token via the secure credential flow · Allowed hosts: `www.patreon.com`
- Maturity: 🧪 Draft: written from Patreon's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/patreon/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/patreon/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Ashby 🧪 Draft

Search Ashby public job boards (no key needed) and read/write the Ashby ATS: candidates, jobs, applications.

- Auth: API key via the secure credential flow · Allowed hosts: `api.ashbyhq.com`
- Maturity: 🧪 Draft: written from Ashby's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/ashby/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/ashby/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### fal.ai 🧪 Draft

Generate media with fal.ai: images, video, audio, music on one key. Submit jobs to 100s of models, poll status, fetch results, upload files.

- Auth: API key via the secure credential flow · Allowed hosts: `fal.run`, `queue.fal.run`, `rest.alpha.fal.ai`
- Maturity: 🧪 Draft: written from fal.ai's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/fal-ai/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/fal-ai/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Gemini 🧪 Draft

Google Gemini media generation: Nano Banana images, Imagen 4 images, Veo video, TTS, model listing.

- Auth: API key via the secure credential flow · Allowed hosts: `generativelanguage.googleapis.com`
- Maturity: 🧪 Draft: written from Gemini's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/gemini/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/gemini/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Ideogram 🧪 Draft

Ideogram text-to-image generation with the strongest text rendering in the catalog: generate, edit, remix, upscale, describe, balance.

- Auth: API key via the secure credential flow · Allowed hosts: `api.ideogram.ai`
- Maturity: 🧪 Draft: written from Ideogram's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/ideogram/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/ideogram/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Black Forest Labs 🧪 Draft

Black Forest Labs FLUX image generation: flux-2-pro and flux-2-flex text-to-image with async polling.

- Auth: API key via the secure credential flow · Allowed hosts: `api.bfl.ai`, `api.eu.bfl.ai`, `api.us.bfl.ai`
- Maturity: 🧪 Draft: written from Black Forest Labs's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/black-forest-labs/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/black-forest-labs/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### HeyGen 🧪 Draft

HeyGen avatar and talking-head video: prompt-to-video agent, multi-scene avatar video, status polling, avatar and voice lists.

- Auth: API key via the secure credential flow · Allowed hosts: `api.heygen.com`
- Maturity: 🧪 Draft: written from HeyGen's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/heygen/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/heygen/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Luma 🧪 Draft

Luma Dream Machine video generation: text-to-video and image-to-video, status polling, cancel, image upload.

- Auth: API key via the secure credential flow · Allowed hosts: `api.lumalabs.ai`
- Maturity: 🧪 Draft: written from Luma's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/luma/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/luma/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Kling 🧪 Draft

Kling AI video generation with client-side JWT auth: text-to-video, image-to-video, status polling, clip extend, lip-sync.

- Auth: access key + secret key pair via the secure credential flow · Allowed hosts: `api.klingai.com`
- Maturity: 🧪 Draft: written from Kling's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/kling/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/kling/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Runway 🧪 Draft

Runway developer API: text-to-video, image-to-video, task polling, video upscale, lip-sync.

- Auth: API secret via the secure credential flow · Allowed hosts: `api.dev.runwayml.com`
- Maturity: 🧪 Draft: written from Runway's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/runway/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/runway/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Beatoven 🧪 Draft

Beatoven.ai royalty-free music generation: compose tracks, poll tasks, download audio, fetch individual stems.

- Auth: API token via the secure credential flow · Allowed hosts: `public-api.beatoven.ai` (plus the download host Beatoven's own task response returns)
- Maturity: 🧪 Draft: written from Beatoven's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/beatoven/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/beatoven/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Twitch 🧪 Draft

Read and write Twitch via the Helix API: channel profile, follower stats, live stream status, past videos, channel title and game updates, clip creation.

- Auth: provider OAuth via the secure credential flow · Allowed hosts: `api.twitch.tv`
- Maturity: 🧪 Draft: written from Twitch's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/twitch/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/twitch/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Mastodon 🧪 Draft

Read and write Mastodon: verify the account, list own posts and followers, publish toots with native scheduling, upload media.

- Auth: provider OAuth via the secure credential flow · Allowed hosts: your Mastodon instance host, declared at connect time (the `--host` you pass, e.g. `https://mastodon.social`; it must start with `http://` or `https://`). The credential is only ever sent to that host.
- Maturity: 🧪 Draft: written from Mastodon's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/mastodon/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/mastodon/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

### Dev.to 🧪 Draft

Read and write dev.to: own profile, own articles (published, drafts, all), public articles by username, create and update articles with a safe draft default.

- Auth: API key via the secure credential flow · Allowed hosts: `dev.to`
- Maturity: 🧪 Draft: written from Dev.to's public API docs, not yet live-tested end-to-end.

Copy, paste to your Muse:

```
Install this connector: https://raw.githubusercontent.com/bluman1/muse-connectors/main/connectors/devto/SKILL.md
You are Muse. Fetch the URL above: it is a connector skill's SKILL.md.
1. Read its `## Files` manifest and download every listed file from the same directory (replace SKILL.md in the URL with each relative path).
2. Save them under ~/workspace/skills/devto/, preserving paths. Compile any bin/*.py with python3 -m py_compile.
3. Follow the skill's `## Auth` section: connect my account via your secure credential flow (credentials.request_api_access) for the provider id it names.
4. Run the skill's status check and report what the connector can now do.
Never ask me for raw API keys or secrets in chat.
```

*To add a connector, see [CONTRIBUTING.md](CONTRIBUTING.md).*

## Maturity badges

- ✅ **Live-tested**: installed from a raw URL on a fresh Muse and exercised against the real API.
- 🧪 **Draft**: written from the provider's public docs, awaiting a live test.
- 👥 **Community**: contributed by the community; review the code before connecting.

## License

MIT: see [LICENSE](LICENSE).
