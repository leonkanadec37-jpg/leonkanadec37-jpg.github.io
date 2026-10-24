#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор XML-карты сайта sitemap.xml (Livi Jewelry):
Включает:
- Главную страницу (/) и языковые версии (/kz/, /uz/)
- Каталог (/shop.html) и языковые версии (/kz/shop.html, /uz/shop.html)
- Все 21 SEO-хаб (RU, KZ, UZ) с полным набором hreflang
- Все активные карточки товаров (/product/prod_XX.html, /kz/product/prod_XX.html, /uz/product/prod_XX.html) с hreflang и <image:image>
- Сервисные страницы (/delivery.html, /privacy.html, /terms.html и их /uz/ аналоги)
"""

import json
import os
from datetime import datetime
from xml.sax.saxutils import escape

SITE_URL = "https://livijewelry.kz"

# Все 21 SEO-хаб
SEO_HUBS = [
    ("kolye-iz-zhemchuga.html", "0.85", "weekly"),
    ("braslety-iz-zhemchuga.html", "0.85", "weekly"),
    ("sergi-iz-zhemchuga.html", "0.85", "weekly"),
    ("komplekty-ukrasheniy.html", "0.85", "weekly"),
    ("chokery-iz-naturalnyh-kamney.html", "0.85", "weekly"),
    ("sotuary-iz-zhemchuga.html", "0.85", "weekly"),
    ("ukrasheniya-iz-barochnogo-zhemchuga.html", "0.85", "weekly"),
    ("ukrasheniya-iz-gematita.html", "0.85", "weekly"),
    ("ukrasheniya-iz-malahita.html", "0.85", "weekly"),
    ("ukrasheniya-iz-ametista.html", "0.85", "weekly"),
    ("ukrasheniya-iz-granata.html", "0.85", "weekly"),
    ("ukrasheniya-iz-rozovogo-kvarca.html", "0.85", "weekly"),
    ("ukrasheniya-iz-biryuzy.html", "0.85", "weekly"),
    ("ukrasheniya-iz-gornogo-hrustalya.html", "0.85", "weekly"),
    ("ukrasheniya-iz-lunnogo-kamnya.html", "0.85", "weekly"),
    ("ukrasheniya-iz-zhemchuga-mayorka.html", "0.85", "weekly"),
    ("ukrasheniya-iz-tigrovogo-glaza.html", "0.85", "weekly"),
    ("ukrasheniya-iz-koralla-i-yashmy.html", "0.85", "weekly"),
    ("ukrasheniya-iz-lazurita.html", "0.85", "weekly"),
    ("tsepi-s-barochnym-zhemchugom.html", "0.85", "weekly"),
    ("koltsa-i-garnitury-iz-kamney.html", "0.85", "weekly"),
]

SERVICE_PAGES = [
    ("delivery.html", "0.6", "monthly"),
    ("privacy.html", "0.3", "yearly"),
    ("terms.html", "0.3", "yearly"),
]


def get_file_lastmod(filepath, default_date=None):
    if os.path.exists(filepath):
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
    return default_date or datetime.now().strftime("%Y-%m-%d")


def build_symmetrical_hreflang(ru_url: str, kz_url: str, uz_url: str) -> list:
    return [
        f'    <xhtml:link rel="alternate" hreflang="ru-KZ" href="{ru_url}" />',
        f'    <xhtml:link rel="alternate" hreflang="ru" href="{ru_url}" />',
        f'    <xhtml:link rel="alternate" hreflang="kk-KZ" href="{kz_url}" />',
        f'    <xhtml:link rel="alternate" hreflang="kk" href="{kz_url}" />',
        f'    <xhtml:link rel="alternate" hreflang="uz-UZ" href="{uz_url}" />',
        f'    <xhtml:link rel="alternate" hreflang="uz" href="{uz_url}" />',
        f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ru_url}" />',
    ]


def generate_sitemap():
    today = datetime.now().strftime("%Y-%m-%d")

    # Load translations if available
    uz_translations = {}
    try:
        from generate_uz_pages import UZ_TRANSLATIONS
        uz_translations = UZ_TRANSLATIONS
    except Exception:
        pass

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    # 1. Главные страницы (RU, KZ, UZ)
    ru_home = f"{SITE_URL}/"
    kz_home = f"{SITE_URL}/kz/"
    uz_home = f"{SITE_URL}/uz/"
    home_hreflangs = build_symmetrical_hreflang(ru_home, kz_home, uz_home)

    for loc, lastmod_file, prio in [
        (ru_home, "index.html", "1.0"),
        (kz_home, "kz/index.html", "0.9"),
        (uz_home, "uz/index.html", "0.9"),
    ]:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{get_file_lastmod(lastmod_file, today)}</lastmod>")
        lines.append("    <changefreq>daily</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.extend(home_hreflangs)
        lines.append("  </url>")

    # 2. Каталоги (RU, KZ, UZ)
    ru_shop = f"{SITE_URL}/shop.html"
    kz_shop = f"{SITE_URL}/kz/shop.html"
    uz_shop = f"{SITE_URL}/uz/shop.html"
    shop_hreflangs = build_symmetrical_hreflang(ru_shop, kz_shop, uz_shop)

    for loc, lastmod_file, prio in [
        (ru_shop, "shop.html", "0.9"),
        (kz_shop, "kz/shop.html", "0.85"),
        (uz_shop, "uz/shop.html", "0.85"),
    ]:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{get_file_lastmod(lastmod_file, today)}</lastmod>")
        lines.append("    <changefreq>daily</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.extend(shop_hreflangs)
        lines.append("  </url>")

    # 3. Все 21 SEO-хаб (RU + KZ + UZ со связкой hreflang)
    for page, prio, freq in SEO_HUBS:
        ru_url = f"{SITE_URL}/{page}"
        kz_url = f"{SITE_URL}/kz/{page}"
        uz_url = f"{SITE_URL}/uz/{page}"
        hub_hreflangs = build_symmetrical_hreflang(ru_url, kz_url, uz_url)

        # RU Hub
        lines.append("  <url>")
        lines.append(f"    <loc>{ru_url}</loc>")
        lines.append(f"    <lastmod>{get_file_lastmod(page, today)}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.extend(hub_hreflangs)
        lines.append("  </url>")

        # KZ Hub
        lines.append("  <url>")
        lines.append(f"    <loc>{kz_url}</loc>")
        lines.append(f"    <lastmod>{get_file_lastmod(f'kz/{page}', today)}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append("    <priority>0.8</priority>")
        lines.extend(hub_hreflangs)
        lines.append("  </url>")

        # UZ Hub
        lines.append("  <url>")
        lines.append(f"    <loc>{uz_url}</loc>")
        lines.append(f"    <lastmod>{get_file_lastmod(f'uz/{page}', today)}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append("    <priority>0.8</priority>")
        lines.extend(hub_hreflangs)
        lines.append("  </url>")

    # 4. Сервисные страницы (RU + UZ)
    for page, prio, freq in SERVICE_PAGES:
        ru_srv = f"{SITE_URL}/{page}"
        uz_srv = f"{SITE_URL}/uz/{page}"
        kz_srv = f"{SITE_URL}/kz/{page}"
        srv_hreflangs = build_symmetrical_hreflang(ru_srv, kz_srv, uz_srv)

        # RU Service
        lines.append("  <url>")
        lines.append(f"    <loc>{ru_srv}</loc>")
        lines.append(f"    <lastmod>{get_file_lastmod(page, today)}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.extend(srv_hreflangs)
        lines.append("  </url>")

        # UZ Service
        if os.path.exists(f"uz/{page}"):
            lines.append("  <url>")
            lines.append(f"    <loc>{uz_srv}</loc>")
            lines.append(f"    <lastmod>{get_file_lastmod(f'uz/{page}', today)}</lastmod>")
            lines.append(f"    <changefreq>{freq}</changefreq>")
            lines.append(f"    <priority>{prio}</priority>")
            lines.extend(srv_hreflangs)
            lines.append("  </url>")

    # 5. Все активные карточки товаров (RU, KZ, UZ)
    products = []
    if os.path.exists("products.json"):
        with open("products.json", "r", encoding="utf-8") as f:
            products = json.load(f)

        for p in products:
            if not p.get("inStock", True):
                continue
            pid = p["id"]
            ru_file = f"product/{pid}.html"
            kz_file = f"kz/product/{pid}.html"
            uz_file = f"uz/product/{pid}.html"

            ru_url = f"{SITE_URL}/product/{pid}.html"
            kz_url = f"{SITE_URL}/kz/product/{pid}.html"
            uz_url = f"{SITE_URL}/uz/product/{pid}.html"

            prod_hreflangs = build_symmetrical_hreflang(ru_url, kz_url, uz_url)

            img_rel = p.get("image", "").lstrip("/")
            img_loc = escape(f"{SITE_URL}/{img_rel}")

            title_ru = escape(f"{p.get('title', '').strip()} — ручная работа Livi Jewelry")
            materials_ru = ", ".join(p.get("materials") or ["натуральный жемчуг"])
            caption_ru = escape(
                f"{p.get('title', '').strip()}. {p.get('description', '').strip()} Материалы: {materials_ru}. Купить в Астане и Алматы с доставкой по Казахстану."
            )

            # Русская карточка товара
            lines.append("  <url>")
            lines.append(f"    <loc>{ru_url}</loc>")
            lines.append(f"    <lastmod>{get_file_lastmod(ru_file, today)}</lastmod>")
            lines.append("    <changefreq>weekly</changefreq>")
            lines.append("    <priority>0.8</priority>")
            lines.extend(prod_hreflangs)
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{img_loc}</image:loc>")
            lines.append(f"      <image:title>{title_ru}</image:title>")
            lines.append(f"      <image:caption>{caption_ru}</image:caption>")
            lines.append("    </image:image>")
            lines.append("  </url>")

            # Казахская карточка товара
            title_kz = escape(f"{p.get('title', '').strip()} — Livi Jewelry қол еңбегі")
            caption_kz = escape(
                f"{p.get('title', '').strip()}. {p.get('description', '').strip()} Табиғи тастар. Астана мен Қазақстан бойынша жедел жеткізу."
            )
            lines.append("  <url>")
            lines.append(f"    <loc>{kz_url}</loc>")
            lines.append(f"    <lastmod>{get_file_lastmod(kz_file, today)}</lastmod>")
            lines.append("    <changefreq>weekly</changefreq>")
            lines.append("    <priority>0.8</priority>")
            lines.extend(prod_hreflangs)
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{img_loc}</image:loc>")
            lines.append(f"      <image:title>{title_kz}</image:title>")
            lines.append(f"      <image:caption>{caption_kz}</image:caption>")
            lines.append("    </image:image>")
            lines.append("  </url>")

            # Узбекская карточка товара
            uz_data = uz_translations.get(pid, {})
            uz_title = uz_data.get("title") or p.get("title", "").strip()
            uz_desc = uz_data.get("desc") or p.get("description", "").strip()
            title_uz = escape(f"{uz_title} — Livi Jewelry qoʻl mehnati")
            caption_uz = escape(
                f"{uz_title}. {uz_desc} Tabiiy toshlar. Toshkent va butun Oʻzbekistonga yetkazib berish."
            )
            lines.append("  <url>")
            lines.append(f"    <loc>{uz_url}</loc>")
            lines.append(f"    <lastmod>{get_file_lastmod(uz_file, today)}</lastmod>")
            lines.append("    <changefreq>weekly</changefreq>")
            lines.append("    <priority>0.8</priority>")
            lines.extend(prod_hreflangs)
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{img_loc}</image:loc>")
            lines.append(f"      <image:title>{title_uz}</image:title>")
            lines.append(f"      <image:caption>{caption_uz}</image:caption>")
            lines.append("    </image:image>")
            lines.append("  </url>")

    lines.append("</urlset>")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    active_count = sum(1 for p in products if p.get("inStock", True))
    total_urls = 3 + 3 + (len(SEO_HUBS) * 3) + len(SERVICE_PAGES) + 3 + (active_count * 3)
    print(f"[OK] Sitemap обновлен: {total_urls} URLs (21 RU + 21 KZ + 21 UZ хабов, 6 витрин/каталогов, 6 сервисных, {active_count} RU + {active_count} KZ + {active_count} UZ активных товаров)")


if __name__ == "__main__":
    generate_sitemap()
