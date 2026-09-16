---
name: "ecobee"
description: "Work with ecobee thermostats: pull 5-minute interval runtime history and set temperature holds (with confirmation). Trigger phrases: ecobee, thermostat, energy report, hvac runtime, set hold, thermostat history."
metadata: { "includeInPrompt": true }
tagline: "Thermostat runtime history and energy reports, plus temperature holds with confirmation."
catalog_auth: "ecobee OAuth 2.0 (per-user PIN flow; self-serve developer app in ecobee portal; smartRead for reads, smartWrite for holds)"
catalog_hosts: ["api.ecobee.com"]
---

# ecobee

## Purpose
Pull historical thermostat runtime data from ecobee (5-minute interval time series: temperatures, equipment runtimes, outdoor conditions) for energy analysis, and set temperature holds on a thermostat. Reach for this when the user mentions ecobee, their thermostat, HVAC runtime, or energy reports.

## Tooling
All commands go through `bin/ecobee.py`:

```bash
bin/ecobee.py auth                                             # verify the credential is provisioned

bin/ecobee.py runtime-report --thermostat-id 123456789012 \
    --start-date 2026-08-01 --end-date 2026-08-31 \
    --columns zoneAveTemp,outdoorTemp,fan,hvacMode              # one month of history

bin/ecobee.py runtime-report --thermostat-id 111111111111,222222222222 \
    --start-date 2026-09-01 --end-date 2026-09-16 \
    --columns zoneHvacMode,zoneCoolTemp,compCool1,compCool2 \
    --include-sensors                                          # two thermostats, sensor data

bin/ecobee.py hold --thermostat-id 123456789012 --mode cool --temperature 76 \
    --confirm "set hold on thermostat 123456789012: cool to 76F (nextTransition)"
```

`runtime-report` returns `reportList` (one entry per thermostat, `rowList` of CSV rows with Date/Time first, then one value per requested column) plus the provider `status`. For multi-year energy dashboards, page in 31-day chunks. `--columns` only accepts column names verified from the official runtime-report docs (e.g. `zoneAveTemp`, `outdoorTemp`, `fan`, `hvacMode`, `zoneHvacMode`, `compHeat1`, `auxHeat1`, `zoneOccupancy`); unknown columns are refused with the full verified list. `--start-interval`/`--end-interval` (0-287) trim the report to part of a day when given; they default to the full day (0 and 287) when omitted.

`hold` posts a `setHold` function via `POST /1/thermostat`. It sets one setpoint: `--mode heat` sets the heat hold temperature, `--mode cool` sets the cool hold temperature. `--hold-type` controls duration: `nextTransition` (default, ends at the next scheduled climate change), `indefinite`, `holdHours`, or `dateTime`.

## Auth
- Provider id: `ecobee` (credential is collected as `custom.ecobee`)
- Collection: ecobee's self-serve OAuth 2.0 PIN authorization flow via the secure credential flow (`credentials.request_api_access`):
  1. Register a developer app in the ecobee consumer portal (Developer menu) to get an app key.
  2. Request a PIN: `GET https://api.ecobee.com/authorize?response_type=ecobeePin&client_id=APP_KEY&scope=SMARTREAD` (add `smartWrite` when holds are needed).
  3. Enter the PIN in the ecobee portal's My Apps widget.
  4. Exchange for access/refresh tokens via `POST /token` with the app key and the authorization code.
- The token is sent as `Authorization: Bearer <token>` on every request.
- Required scopes: `smartRead` (runtime reports); `smartWrite` (holds). **If reads work but holds return HTTP 403, re-approve with the `smartWrite` scope; a read-only token cannot set holds.**
- Allowed hosts: `api.ecobee.com`
- Status check: `bin/ecobee.py auth` (must return `"ok": true`). This verifies the credential is provisioned; no lightweight ping endpoint was verified from a primary source, so live token validity is confirmed on the first real API call.

## Operating Rules
1. Reads (`auth`, `runtime-report`) need no confirmation.
2. **Holds need exact-match confirmation on every call.** `hold` requires `--confirm` with the exact string the CLI echoes (thermostat ID, mode, temperature, hold type), because it changes the real thermostat in the house.
3. Runtime report limits (from the official docs): at most 31 days per request, at most 25 thermostats per request, and no more than one open report request at a time. Page long ranges in 31-day chunks.
4. Do not poll reports faster than once every 15 minutes: that is the shortest interval at which report data changes. There can also be up to an hour of delay before the most recent data is available.
5. Report dates are UTC; timestamps in the rows are in thermostat time. Temperature values come back in degrees F. Interval values are the reading at the *start* of each 5-minute interval, not an average.
6. Never exfiltrate the credential: the CLI only ever handles surrogates. Do not print, log, or transmit the token value.

## Files
- SKILL.md
- bin/ecobee.py

## Maturity
Draft: written from ecobee's official v1 API docs; not yet live-tested end-to-end. Honesty flags: the `GET /1/thermostatSummary` and GET thermostat detail paths are deliberately omitted (they appear in the official operations index but the exact path pattern was not confirmed from a primary source); the `setHold` param field names in the CLI follow the official docs but were flagged as unverified because the set-hold page fetch failed during this build, so the CLI surfaces ecobee's own error if a field differs.
