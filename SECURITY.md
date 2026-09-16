# Security policy

## Reporting a vulnerability

Do not open a public issue. Use GitHub's private vulnerability reporting
(Security tab > Report a vulnerability) so it can be fixed before disclosure.

## What this repo guarantees

- **Zero secrets in the repo.** Skills are code and docs only; `tools/audit.sh`
  verifies this and every PR touching `connectors/` must pass it in CI.
- **Credentials never travel with a skill.** API keys and OAuth tokens live in
  the installing user's private vault; skills only handle single-use surrogates.
- **Each skill declares its allowed hosts** in `SKILL.md`. The credential helper
  refuses to send a credential anywhere else.
