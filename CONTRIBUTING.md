# Contributing a connector

## Don't code? Just bring the API docs

You don't need to write a connector by hand. Paste the prompt below to your Muse along with the service's API docs (a URL or pasted text), and it will build the whole connector for you: the SKILL.md, the CLI, the audit, everything.

```
I want to contribute a connector to the open-source muse-connectors catalog: https://github.com/bluman1/muse-connectors

Here are the API docs for the service: <PASTE THE DOCS URL OR TEXT HERE>

Build the connector for me following the repo's CONTRIBUTING.md:
1. Clone the repo and scaffold from connectors/_template with provider id <pick-a-lowercase-id>.
2. Write SKILL.md (Purpose, Tooling, Auth, Operating Rules, Files manifest, Maturity) and a stdlib-only Python CLI in bin/ that loads the credential as custom.<id> through the dynamic_credentials helper. Never put a secret in the code.
3. Run tools/audit.sh and python3 -m py_compile until both are clean.
4. Mark it Draft in the Maturity section unless you can live-test it against the real API.

If my GitHub account is connected to you, open a pull request against bluman1/muse-connectors with the new connector and work through the PR checklist in CONTRIBUTING.md. If it isn't, tell me exactly which files to submit and where.
```

If your GitHub is connected to your Muse, it can open the PR for you directly. If not, the prompt will tell you what to send in.

## The one rule that matters

**Provider id == credential name suffix.** When a user installs your connector, their Muse collects the credential via `credentials.request_api_access`, which registers it as `custom.<provider-id>`. Your skill's CLIs must load the credential under exactly that name. So pick a lowercase provider id (`slack`, `github`, `notion`) and use it everywhere: directory name, skill name, and credential name.

## Scaffold a new connector

```bash
cp -r connectors/_template connectors/<provider-id>
# then fill in SKILL.md, write bin/, run tools/audit.sh
```

## Skill layout

```
connectors/<provider-id>/
  SKILL.md            # frontmatter + Purpose, Tooling, Auth, Operating Rules, Files, Maturity
  bin/<name>.py       # CLI(s); Python 3, stdlib only (urllib)
  references/...      # optional: API notes, examples, pagination details
```

`SKILL.md` sections (mirror the skill-creator scaffold, plus two):

- `## Purpose`: what the connector does, trigger phrases.
- `## Tooling`: exact CLI commands with examples. Every command a user might want must be documented here; undocumented == unavailable.
- `## Auth`: provider id, how the credential is collected (API key vs provider OAuth), required scopes, allowed hosts, and the status-check command.
- `## Operating Rules`: confirm-before-write rules, rate-limit behavior, what never to do.
- `## Files`: the install manifest. **Every file the skill needs, relative paths, nothing more.** The one-paste installer trusts exactly this list.
- `## Maturity`: 🧪 Draft until installed from a raw URL on a fresh Muse and exercised against the real API, then ✅ Live-tested.

## CLI conventions

- Import the bundled credential helper; fail loudly if the runtime lacks it:
  ```python
  import sys
  sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
  from dynamic_credentials import add_surrogate_to_request, read_json_response, ...
  ```
- Load the credential as `custom.<provider-id>`; never accept a raw key via argv, env, or file.
- Pass `allowed_hosts` from the skill's Auth section; never call other hosts with the credential attached.
- Keep it stdlib-only so any Muse runtime can run it.

## What can and can't be a connector

Works: a single API key, or the provider's own OAuth.
Declined by the credential flow (don't submit these): password logins, session cookies, request signing, or more than one secret.

## PR checklist

- [ ] `tools/audit.sh` passes (no secrets, no suspicious patterns).
- [ ] `## Files` manifest matches the directory exactly.
- [ ] `python3 -m py_compile` passes on all of `bin/`.
- [ ] `## Auth` lists scopes, allowed hosts, and a status-check command.
- [ ] Maturity badge is honest (🧪 Draft until live-tested).
