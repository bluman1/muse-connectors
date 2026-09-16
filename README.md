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

---

*To add a connector, see [CONTRIBUTING.md](CONTRIBUTING.md).*

## Maturity badges

- ✅ **Live-tested** — installed from a raw URL on a fresh Muse and exercised against the real API.
- 🧪 **Draft** — written from the provider's public docs, awaiting a live test.
- 👥 **Community** — contributed by the community; review the code before connecting.

## License

MIT — see [LICENSE](LICENSE).
