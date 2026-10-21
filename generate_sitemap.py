#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор XML-карты сайта sitemap.xml (Livi Jewelry):
Включает:
- Главную страницу (/) и казахскую версию (/kz/)
- Каталог (/shop.html) и казахский каталог (/kz/shop.html)
- Все 21 SEO-хаб (15 тематических хабов + 6 новых узкоцелевых кластеров)
- Все 28 русских карточек товаров (/product/prod_01.html ... /product/prod_28.html) с hreflang и <image:image>
- Все 28 казахских карточек товаров (/kz/product/prod_01.html ... /kz/product/prod_28.html) с hreflang и <image:image>
- Сервисные страницы (/delivery.html, /privacy.html, /terms.html, /cart.html)
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
    # 6 новых узкоцелевых SEO-хабов
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


def generate_sitemap():
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    # 1. Главные страницы (RU + KZ)
    lines.append("  <url>")
    lines.append(f"    <loc>{SITE_URL}/</loc>")
    lines.append(f"    <lastmod>{get_file_lastmod('index.html', today)}</lastmod>")
    lines.append("    <changefreq>daily</changefreq>")
    lines.append("    <priority>1.0</priority>")
    lines.append(f'    <xhtml:link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{SITE_URL}/" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/" />')
    lines.append("  </url>")

    lines.append("  <url>")
    lines.append(f"    <loc>{SITE_URL}/kz/</loc>")
    lines.append(f"    <lastmod>{get_file_lastmod('kz/index.html', today)}</lastmod>")
    lines.append("    <changefreq>daily</changefreq>")
    lines.append("    <priority>0.9</priority>")
    lines.append(f'    <xhtml:link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{SITE_URL}/" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/" />')
    lines.append("  </url>")

    # 2. Каталоги (RU + KZ)
    lines.append("  <url>")
    lines.append(f"    <loc>{SITE_URL}/shop.html</loc>")
    lines.append(f"    <lastmod>{get_file_lastmod('shop.html', today)}</lastmod>")
    lines.append("    <changefreq>daily</changefreq>")
    lines.append("    <priority>0.9</priority>")
    lines.append(f'    <xhtml:link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/shop.html" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{SITE_URL}/shop.html" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/shop.html" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/shop.html" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/shop.html" />')
    lines.append("  </url>")

    lines.append("  <url>")
    lines.append(f"    <loc>{SITE_URL}/kz/shop.html</loc>")
    lines.append(f"    <lastmod>{get_file_lastmod('kz/shop.html', today)}</lastmod>")
    lines.append("    <changefreq>daily</changefreq>")
    lines.append("    <priority>0.85</priority>")
    lines.append(f'    <xhtml:link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/shop.html" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{SITE_URL}/shop.html" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/shop.html" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/shop.html" />')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/shop.html" />')
    lines.append("  </url>")

    # 3. Все 21 SEO-хаб (RU + KZ со связкой hreflang)
    for page, prio, freq in SEO_HUBS:
        ru_url = f"{SITE_URL}/{page}"
        kz_url = f"{SITE_URL}/kz/{page}"
        kz_file = f"kz/{page}"

        # RU Hub
        lines.append("  <url>")
        lines.append(f"    <loc>{ru_url}</loc>")
        lines.append(f"    <lastmod>{get_file_lastmod(page, today)}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append(f'    <xhtml:link rel="alternate" hreflang="ru-KZ" href="{ru_url}" />')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{ru_url}" />')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="kk-KZ" href="{kz_url}" />')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="kk" href="{kz_url}" />')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ru_url}" />')
        lines.append("  </url>")

        # KZ Hub
        lines.append("  <url>")
        lines.append(f"    <loc>{kz_url}</loc>")
        lines.append(f"    <lastmod>{get_file_lastmod(kz_file, today)}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>0.8</priority>")
        lines.append(f'    <xhtml:link rel="alternate" hreflang="ru-KZ" href="{ru_url}" />')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{ru_url}" />')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="kk-KZ" href="{kz_url}" />')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="kk" href="{kz_url}" />')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ru_url}" />')
        lines.append("  </url>")

    # 4. Сервисные страницы
    for page, prio, freq in SERVICE_PAGES:
        url = f"{SITE_URL}/{page}"
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{get_file_lastmod(page, today)}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")

    # 5. Все 28 RU и 28 KZ карточек товаров
    if os.path.exists("products.json"):
        with open("products.json", "r", encoding="utf-8") as f:
            products = json.load(f)

        for p in products:
            if not p.get("inStock", True):
                continue
            pid = p["id"]
            ru_file = f"product/{pid}.html"
            kz_file = f"kz/product/{pid}.html"
            ru_url = f"{SITE_URL}/product/{pid}.html"
            kz_url = f"{SITE_URL}/kz/product/{pid}.html"

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
            lines.append(f'    <xhtml:link rel="alternate" hreflang="ru-KZ" href="{ru_url}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{ru_url}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="kk-KZ" href="{kz_url}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="kk" href="{kz_url}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ru_url}" />')
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
            lines.append(f'    <xhtml:link rel="alternate" hreflang="ru-KZ" href="{ru_url}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{ru_url}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="kk-KZ" href="{kz_url}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="kk" href="{kz_url}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ru_url}" />')
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{img_loc}</image:loc>")
            lines.append(f"      <image:title>{title_kz}</image:title>")
            lines.append(f"      <image:caption>{caption_kz}</image:caption>")
            lines.append("    </image:image>")
            lines.append("  </url>")

    lines.append("</urlset>")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    active_count = sum(1 for p in products if p.get("inStock", True)) if os.path.exists("products.json") else 0
    total_urls = 2 + 2 + (len(SEO_HUBS) * 2) + len(SERVICE_PAGES) + (active_count * 2)
    print(f"[OK] Sitemap обновлен: {total_urls} URLs (21 RU + 21 KZ хабов, 4 витрины/каталога, 3 сервисных, {active_count} RU + {active_count} KZ активных товаров)")


if __name__ == "__main__":
    generate_sitemap()
