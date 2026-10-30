#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор ассетов для автоматической выгрузки каталога Livi Jewelry в Pinterest:
1. pinterest_bulk_pins.csv — готовый CSV-файл для функции «Массовое создание пинов» в Pinterest Business.
2. pinterest_feed.xml — товарный фид (Product Feed), совместимый со спецификацией Pinterest Catalogs.

Использование:
    python generate_pinterest_assets.py
"""

import csv
import json
import os
from xml.sax.saxutils import escape

SITE_URL = "https://livijewelry.kz"
PRODUCTS_FILE = "products.json"
CSV_OUTPUT = "feeds/pinterest_bulk_pins.csv"
XML_OUTPUT = "pinterest_feed.xml"
os.makedirs("feeds", exist_ok=True)

BOARD_MAP = {
    "Sets": "Комплекты украшений ручной работы",
    "Necklaces": "Колье и чокеры из натурального жемчуга",
    "Bracelets": "Браслеты из натуральных камней",
    "Lariats": "Сотуары и длинные украшения",
    "Earrings": "Серьги и сеты с натуральным жемчугом",
}

HASHTAGS_BASE = "#украшенияручнойработы #авторскиеукрашения #натуральныйжемчуг #барочныйжемчуг #натуральныекамни #чокер #колье #браслет #бижутерияказахстан #подарокдевушке #астана #алматы"


PINTEREST_UTM = "?utm_source=pinterest&utm_medium=social&utm_campaign=product_pins"


def clean_text(s: str) -> str:
    if not s:
        return ""
    return " ".join(s.strip().split())


def generate_pinterest_assets():
    if not os.path.exists(PRODUCTS_FILE):
        print(f"[FAIL] Файл {PRODUCTS_FILE} не найден.")
        return

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    active_products = [p for p in products if p.get("inStock", True)]
    print(f"Найдено {len(active_products)} активных товаров для экспорта в Pinterest.")

    # ---------------------------------------------------------
    # 1. Генерация Pinterest Bulk Upload CSV
    # ---------------------------------------------------------
    csv_rows = []
    for p in active_products:
        pid = p["id"]
        title = clean_text(p.get("title", ""))
        price = p.get("price", 0)
        category = p.get("category", "Necklaces")
        board = BOARD_MAP.get(category, "Украшения Livi Jewelry")
        
        img_rel = p.get("image", "").lstrip("/")
        image_url = f"{SITE_URL}/{img_rel}"
        product_url = f"{SITE_URL}/product/{pid}.html{PINTEREST_UTM}"

        desc_raw = clean_text(p.get("description", ""))
        materials = ", ".join(p.get("materials") or ["натуральный жемчуг"])

        # Описание пина (до 500 символов под требования Pinterest SEO)
        pin_desc = f"{title}. {desc_raw} Материалы: {materials}. Цена: {price:,} ₸. Доставка день-в-день по Астане, 1–3 дня экспресс СДЭК по Казахстану. {HASHTAGS_BASE}".replace(",", " ")

        if len(pin_desc) > 490:
            pin_desc = pin_desc[:487] + "..."

        csv_rows.append({
            "Title": title[:100],
            "Media URL": image_url,
            "Pinterest board": board,
            "Thumbnail": "",
            "Description": pin_desc,
            "Link": product_url,
            "Publish date": "",
            "Keywords": f"украшения, натуральный жемчуг, {materials}, колье, подарок",
        })

    with open(CSV_OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
        fieldnames = ["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"[OK] Создан {CSV_OUTPUT} ({len(csv_rows)} пинов, разложенных по {len(set(r['Pinterest board'] for r in csv_rows))} доскам)")

    # ---------------------------------------------------------
    # 2. Генерация Pinterest Catalogs XML Feed (RSS 2.0 Product Feed)
    # ---------------------------------------------------------
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">',
        '  <channel>',
        '    <title>Livi Jewelry — Авторские украшения ручной работы</title>',
        f'    <link>{SITE_URL}</link>',
        '    <description>Товарный каталог авторских украшений из натурального жемчуга и камней Livi Jewelry</description>',
    ]

    for p in active_products:
        pid = p["id"]
        title = escape(clean_text(p.get("title", "")))
        desc = escape(clean_text(p.get("description", "")))
        price = p.get("price", 0)
        img_rel = p.get("image", "").lstrip("/")
        image_url = f"{SITE_URL}/{img_rel}"
        product_url = f"{SITE_URL}/product/{pid}.html{PINTEREST_UTM}"
        category = p.get("category", "Necklaces")
        board_type = BOARD_MAP.get(category, "Украшения")

        xml_lines.append("    <item>")
        xml_lines.append(f"      <g:id>{pid}</g:id>")
        xml_lines.append(f"      <g:title>{title}</g:title>")
        xml_lines.append(f"      <g:description>{desc}</g:description>")
        xml_lines.append(f"      <g:link>{escape(product_url)}</g:link>")
        xml_lines.append(f"      <g:image_link>{image_url}</g:image_link>")
        xml_lines.append(f"      <g:price>{price}.00 KZT</g:price>")
        xml_lines.append("      <g:availability>in stock</g:availability>")
        xml_lines.append("      <g:condition>new</g:condition>")
        xml_lines.append("      <g:brand>Livi Jewelry</g:brand>")
        xml_lines.append(f"      <g:product_type>{escape(board_type)}</g:product_type>")
        xml_lines.append("      <g:google_product_category>196</g:google_product_category>")
        xml_lines.append("    </item>")

    xml_lines.append("  </channel>")
    xml_lines.append("</rss>")

    with open(XML_OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines) + "\n")

    print(f"[OK] Создан {XML_OUTPUT} ({len(active_products)} товаров со статусом in stock и ценами в KZT)")


if __name__ == "__main__":
    generate_pinterest_assets()
