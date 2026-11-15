#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Патчит статические корневые страницы RU новым меню (Задача 007).
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_mobile_menu import render_full_storefront_header

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_FILES = {
    "index.html": {"ru": "/", "kk": "/kz/", "uz": "/uz/"},
    "shop.html": {"ru": "/shop.html", "kk": "/kz/shop.html", "uz": "/uz/shop.html"},
    "delivery.html": {"ru": "/delivery.html", "kk": "/kz/delivery.html", "uz": "/uz/delivery.html"},
    "cart.html": {"ru": "/cart.html", "kk": "/kz/cart.html", "uz": "/uz/cart.html"},
    "privacy.html": {"ru": "/privacy.html", "kk": "/kz/privacy.html", "uz": "/uz/privacy.html"},
    "terms.html": {"ru": "/terms.html", "kk": "/kz/terms.html", "uz": "/uz/terms.html"},
    "404.html": {"ru": "/", "kk": "/kz/", "uz": "/uz/"},
}


def patch_files():
    for filename, lang_urls in STATIC_FILES.items():
        filepath = os.path.join(ROOT_DIR, filename)
        if not os.path.exists(filepath):
            print(f"[SKIP] {filename} does not exist")
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        new_header = render_full_storefront_header("ru", lang_urls)

        # Replace existing <header class="storefront-header">...</header>
        pat = re.compile(r'  <header class="storefront-header">.*?</header>', re.DOTALL)
        if not pat.search(content):
            print(f"[WARN] No storefront-header match in {filename}")
            continue

        patched = pat.sub(new_header, content, count=1)
        if "/scripts/storefront-menu.js" not in patched:
            patched = patched.replace("</body>", '  <script src="/scripts/storefront-menu.js" defer></script>\n</body>')

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(patched)
        print(f"[OK] Patched {filename} with new mobile menu")


if __name__ == "__main__":
    patch_files()
