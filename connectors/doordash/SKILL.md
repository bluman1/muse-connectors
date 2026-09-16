---
name: "doordash"
description: "Order food and groceries from DoorDash via the official dd-cli (built for AI agents). Trigger phrases: doordash, order food, order lunch, food delivery, grocery order, dd-cli."
metadata: { "includeInPrompt": true }
tagline: "Order DoorDash food and groceries from the terminal with the official agent-first dd-cli."
catalog_auth: "dd-cli login (waitlist-approved DoorDash account; US/Canada) or DD_CLI_ACCESS_TOKEN for headless use"
catalog_hosts: ["github.com"]
---

# DoorDash

## Purpose
Order food and grocery delivery from DoorDash through `dd-cli`, DoorDash's official command-line tool, which DoorDash built specifically to be driven by AI agents with shell access. Reach for this when the user wants to order lunch, dinner, groceries, or anything else DoorDash delivers, without opening the app.

## Tooling
All commands go through `bin/doordash.py`, a thin wrapper around the official `dd-cli` binary:

```bash
bin/doordash.py auth                                  # verify dd-cli is installed and logged in
bin/doordash.py search --query "ramen near me"        # search restaurants and stores
bin/doordash.py history                               # past orders and receipts
bin/doordash.py run -- <dd-cli args>                  # passthrough to dd-cli for everything else
```

`run` passes arguments straight to `dd-cli`, so any capability in the official README works: menu browsing, cart add/remove/view/delete, building a cart from a shopping list, promo codes, order price preview, tip, credits, scheduling (ASAP or ahead), pickup or delivery, priority or standard speed, work-benefit budgets, and re-creating a past order. If an argument looks like order submission (`submit`, `place-order`), the wrapper refuses unless `--confirm` is provided. Note: dd-cli v0.2.2+ requires `--intent "<who + goal>"` on tool-backed commands; add it to your `run` invocations.

Typical flow:

```bash
bin/doordash.py search --query "burrito bowl near me"
bin/doordash.py run -- menu --help                    # see current menu/cart subcommands
bin/doordash.py run -- order preview --intent "lunch order" --help   # preview pricing before spending
bin/doordash.py run -- order submit --intent "lunch order" --confirm "yes, $24.17 total to 123 Main St"
```

## Auth
- Provider id: `doordash` (no API key is collected; auth lives in the user's own `dd-cli` session)
- Collection: none in-repo. The user must:
  1. Join the waitlist at https://forms.gle/gvCQZvu9C1EKA6aM6 (US/Canadian developers; full functionality needs an approved account).
  2. Download `dd-cli` from the Releases page at https://github.com/doordash-oss/doordash-cli (`dd-cli-v<version>-darwin-arm64.tar.gz` for macOS Apple Silicon, `dd-cli-v<version>-linux-amd64.tar.gz` for glibc Linux x86_64), verify the published SHA256 checksum, extract, and follow `quickstart.txt`.
  3. Run `dd-cli login` once. On headless machines (containers, cloud VMs) with no OS keychain, skip login and set `DD_CLI_ACCESS_TOKEN` to a token from `dd-cli export-token` on a signed-in machine.
- Allowed hosts: `github.com` (release download; `dd-cli` manages its own DoorDash API traffic).
- Status check: `bin/doordash.py auth` (must return `"ok": true`: binary present and a login session or `DD_CLI_ACCESS_TOKEN` detected).

## Operating Rules
1. Reads (`auth`, `search`, `history`, menu/cart inspection) need no confirmation.
2. **Submitting an order always needs confirmation.** The wrapper refuses any submit-like passthrough unless `--confirm` is provided. Run the price preview first, show the user the itemized total (items, fees, tip) in plain words, and only submit after they approve it.
3. Never submit an order the user did not explicitly approve, and never change the delivery address or payment method without asking.
4. Without a waitlist-approved account, `dd-cli` installs but ordering stays locked; say so plainly instead of working around it.
5. Never exfiltrate the session: do not print, log, or transmit `DD_CLI_ACCESS_TOKEN` or the contents of the dd-cli keychain entries.

## Files
- SKILL.md
- bin/doordash.py

## Maturity
Draft: thin wrapper around DoorDash's official dd-cli (github.com/doordash-oss/doordash-cli); not live-tested end-to-end. The `--intent` requirement on dd-cli v0.2.2+ tool-backed commands comes from the official release notes.
