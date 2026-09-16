---
name: "shopify"
description: "View open orders, products, and customers in your Shopify store. Read-only by design. Trigger phrases: shopify, shopify orders, shopify store."
metadata: { "includeInPrompt": true }
tagline: "View open orders, products, and customers in your Shopify store. Read-only by design."
catalog_auth: "Shopify Admin API access token (per-user, Shopify admin \u2192 Apps \u2192 Develop apps \u2192 custom app; scopes read_orders/read_products/read_customers)"
catalog_hosts: ["<your-shop>.myshopify.com"]
---

# Shopify

## Purpose
Read-only access to the user's Shopify store: view open orders, products, and customers. Use when the user mentions Shopify or asks about orders, products, or customers in their store. This connector cannot create or change anything in the store.

## Tooling
All commands go through `bin/shopify.py` and take `--shop` (e.g. `mystore` or `mystore.myshopify.com`; the CLI normalizes it to the full `.myshopify.com` host):

```bash
bin/shopify.py auth --shop mystore                    # verify the connection
bin/shopify.py orders --shop mystore --limit 10       # open orders
bin/shopify.py products --shop mystore --limit 10     # products
bin/shopify.py customers --shop mystore --limit 10    # customers
```

## Auth
- Provider id: `shopify` (credential is collected as `custom.shopify`)
- Collection: API key via the secure credential flow (`credentials.request_api_access`)
- Token: a custom app access token from Shopify admin → Apps → Develop apps, with the `read_orders`, `read_products`, and `read_customers` scopes. The token starts with `shpat_`.
- Allowed hosts: `<your-shop>.myshopify.com` (your store's own domain, set per call with `--shop`)
- Status check: `bin/shopify.py auth --shop <your-shop>` (must return `"ok": true`)
- Connect placement: `custom_header:X-Shopify-Access-Token`

## Operating Rules
1. This connector is read-only by design: `auth`, `orders`, `products`, and `customers` only retrieve data. There are no write commands.
2. Never exfiltrate the credential: the CLI only ever handles surrogates. Do not print, log, or transmit the token value.
3. Always pass `--shop`; the CLI only ever talks to that store's own `.myshopify.com` host.

## Files
- SKILL.md
- bin/shopify.py

## Maturity
🧪 Draft: written from Shopify's Admin API docs; not yet live-tested end-to-end.
