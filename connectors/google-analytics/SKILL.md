---
name: "google-analytics"
description: "Read Google Analytics 4 reports: standard reports with dimensions and metrics, realtime reports, and batch reports. Trigger phrases: google analytics, GA4, analytics report, traffic report."
metadata: { "includeInPrompt": true }
tagline: "Query GA4 property reports: dimensions, metrics, realtime activity."
catalog_auth: "Google OAuth 2.0 (per-user) or service account; Analytics Data API enabled in Google Cloud Console"
catalog_hosts: ["analyticsdata.googleapis.com"]
---

# Google Analytics

## Purpose
Pull read-only reports from Google Analytics 4 properties through the Analytics Data API v1: standard reports over any date range with chosen dimensions and metrics, realtime activity for the last 30 minutes, and batched multi-report calls. Use when the user asks about site or app traffic, sessions, users, events, or page performance measured in GA4.

## Tooling
All commands go through `bin/google-analytics.py`:

```bash
bin/google-analytics.py auth --property-id properties/1234     # verify the token can read this property
bin/google-analytics.py report --property-id properties/1234 \
    --start-date 2026-09-01 --end-date 2026-09-16 \
    --metrics sessions,totalUsers --dimensions date             # standard report
bin/google-analytics.py report --property-id properties/1234 \
    --start-date 30daysAgo --end-date today \
    --metrics eventCount --dimensions eventName,country --limit 50
bin/google-analytics.py realtime --property-id properties/1234 \
    --metrics activeUsers --dimensions eventName               # realtime report
bin/google-analytics.py batch --property-id properties/1234 \
    --requests-file requests.json                              # array of runReport request bodies
```

The property ID is the numeric GA4 property ID written as `properties/NNNN` (Admin > Property settings). Dimensions are objects with a `name` field (up to 9 per report), metrics are objects with a `name` field (up to 10), and date ranges accept `YYYY-MM-DD` or relative terms (`NdaysAgo`, `yesterday`, `today`), per the official REST reference. Metric and dimension names follow the GA4 API lists (e.g. `sessions`, `totalUsers`, `eventCount`, `activeUsers`; `date`, `eventName`, `country`, `pagePath`). The realtime method supports a narrower set of dimension and metric names than standard reports; if the API rejects a name, retry with a realtime-supported one from the official docs.

## Auth
- Provider id: `google-analytics` (credential is collected as `custom.google-analytics`)
- Collection: OAuth 2.0 via the secure credential flow (`credentials.request_api_access`); Google Cloud Console project with the Analytics Data API enabled. A service account works too: add its email to the GA4 property (Admin > Property access management, viewer role). The token is sent as `Authorization: Bearer <token>`.
- Required scopes: `https://www.googleapis.com/auth/analytics.readonly`
- Allowed hosts: `analyticsdata.googleapis.com`
- Status check: `bin/google-analytics.py auth --property-id properties/1234` (must return `"ok": true`)

## Operating Rules
1. Read-only: this API exposes no writes. There is nothing to confirm.
2. The property ID must match `properties/<digits>`; the CLI refuses anything else.
3. Dates must be `YYYY-MM-DD` or `NdaysAgo`/`yesterday`/`today`; the CLI refuses anything else.
4. Quotas: the GA4 Data API enforces per-property daily and hourly quotas (property quota is visible in responses), so do not hammer it. Cache results within a session and keep `--limit` modest; the API also caps responses at 250,000 rows per request regardless of what you ask for.
5. Never exfiltrate the credential: the CLI only ever handles surrogates. Do not print, log, or transmit the token value.

## Files
- SKILL.md
- bin/google-analytics.py

## Maturity
🧪 Draft: written from Google's official Analytics Data API v1 REST reference (endpoint paths, request field names, and the response row shape all confirmed against the docs) and not yet live-tested end-to-end against a real property. The `batch` subcommand and the `orderBys` flag have not been verified in a live flow.
