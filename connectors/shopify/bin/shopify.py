#!/usr/bin/env python3
"""Minimal Shopify Admin API CLI for the muse-connectors Shopify skill.

Read-only: shop info, open orders, products, customers. Auth: loads the
per-user `custom.shopify` credential as a surrogate via the bundled
dynamic_credentials helper. The real token never touches this script:
the runtime swaps the surrogate on approved egress, only to the store's
own .myshopify.com host (placement: custom header X-Shopify-Access-Token).
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

HELPER_PATH = "/opt/hatch/skills/skill-creator/bin"
CREDENTIAL_NAME = "custom.shopify"
API_VERSION = "2024-01"

try:
    sys.path.insert(0, HELPER_PATH)
    from dynamic_credentials import (
        DynamicCredentialError,
        add_surrogate_to_request,
        read_json_response,
    )
except ImportError:
    sys.exit(
        "error: this CLI needs the Muse dynamic_credentials helper at "
        f"{HELPER_PATH} (install this skill on a Muse runtime to use it)"
    )


def normalize_shop(shop: str) -> str:
    """Accept 'mystore', 'mystore.myshopify.com', or a full URL; return the host."""
    host = shop.strip()
    if "://" in host:
        host = host.split("://", 1)[1]
    host = host.split("/")[0].strip().rstrip("/").lower()
    if not host.endswith(".myshopify.com"):
        host += ".myshopify.com"
    return host


def call(path: str, shop_host: str, params: dict | None = None):
    url = f"https://{shop_host}/admin/api/{API_VERSION}" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={})
    try:
        add_surrogate_to_request(
            req, CREDENTIAL_NAME, allowed_hosts=(shop_host,)
        )
    except DynamicCredentialError as exc:
        sys.exit(f"error: credential problem: {exc}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return read_json_response(resp)
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        sys.exit(f"error: HTTP {exc.code}: {body[:300]}")
    except Exception as exc:  # network-level failure
        sys.exit(f"error: request failed: {exc}")


def cmd_auth(args):
    shop_host = normalize_shop(args.shop)
    result = call("/shop.json", shop_host)
    shop = result.get("shop", {}) if isinstance(result, dict) else {}
    print(json.dumps({"ok": True, "name": shop.get("name"), "domain": shop.get("domain")}, indent=2))


def cmd_orders(args):
    shop_host = normalize_shop(args.shop)
    result = call("/orders.json", shop_host, params={"status": "open", "limit": args.limit})
    orders = result.get("orders", []) if isinstance(result, dict) else []
    out = [
        {"name": o.get("name"), "total_price": o.get("total_price"),
         "financial_status": o.get("financial_status")}
        for o in orders
    ]
    print(json.dumps(out, indent=2))


def cmd_products(args):
    shop_host = normalize_shop(args.shop)
    result = call("/products.json", shop_host, params={"limit": args.limit})
    products = result.get("products", []) if isinstance(result, dict) else []
    out = [{"title": p.get("title"), "status": p.get("status")} for p in products]
    print(json.dumps(out, indent=2))


def cmd_customers(args):
    shop_host = normalize_shop(args.shop)
    result = call("/customers.json", shop_host, params={"limit": args.limit})
    customers = result.get("customers", []) if isinstance(result, dict) else []
    out = [
        {"first_name": c.get("first_name"), "last_name": c.get("last_name"),
         "email": c.get("email")}
        for c in customers
    ]
    print(json.dumps(out, indent=2))


def add_shop_arg(p):
    p.add_argument("--shop", required=True,
                   help="store, e.g. 'mystore' or 'mystore.myshopify.com'")
    return p


def main():
    parser = argparse.ArgumentParser(description="Shopify Admin API CLI (muse-connectors, read-only)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = add_shop_arg(sub.add_parser("auth", help="verify the connection"))
    p.set_defaults(func=cmd_auth)

    p = add_shop_arg(sub.add_parser("orders", help="open orders"))
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_orders)

    p = add_shop_arg(sub.add_parser("products", help="products"))
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_products)

    p = add_shop_arg(sub.add_parser("customers", help="customers"))
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_customers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
