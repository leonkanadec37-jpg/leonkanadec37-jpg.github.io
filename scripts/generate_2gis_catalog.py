#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор каталога товаров Livi Jewelry для 2ГИС:
  1. 2gis_feed.xml  — YML-фид (Yandex Market Language) для автоматической синхронизации по постоянному URL
  2. 2gis_catalog.csv — CSV-файл (разделитель ';', UTF-8-SIG) для мгновенной ручной загрузки в кабинет 2ГИС
"""

import json
import os
import csv
import datetime
from xml.sax.saxutils import escape

SITE_URL = "https://livijewelry.kz"
PRODUCTS_FILE = "products.json"
OUTPUT_YML = "2gis_feed.xml"
OUTPUT_CSV = "feeds/2gis_catalog.csv"
os.makedirs("feeds", exist_ok=True)

CATEGORY_MAP = {
    "Necklaces": {"id": "1", "name": "Колье и бусы"},
    "Bracelets": {"id": "2", "name": "Браслеты"},
    "Earrings": {"id": "3", "name": "Серьги"},
    "Sets": {"id": "4", "name": "Комплекты украшений"},
    "Lariats": {"id": "5", "name": "Сотуары и галстуки"},
}


def clean_text(text: str) -> str:
    """Удаляет лишние пробелы и переносы для аккуратного отображения."""
    if not text:
        return ""
    return " ".join(text.split())


def generate():
    if not os.path.exists(PRODUCTS_FILE):
        print(f"Ошибка: {PRODUCTS_FILE} не найден!")
        return

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 1. Генерация YML для 2ГИС
    yml_lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE yml_catalog SYSTEM "shops.dtd">',
        f'<yml_catalog date="{now_str}">',
        '  <shop>',
        '    <name>Livi Jewelry</name>',
        '    <company>Livi Jewelry — Авторские украшения ручной работы</company>',
        f'    <url>{SITE_URL}</url>',
        '    <currencies>',
        '      <currency id="KZT" rate="1"/>',
        '    </currencies>',
        '    <categories>',
    ]

    for cat_key, cat_data in CATEGORY_MAP.items():
        yml_lines.append(f'      <category id="{cat_data["id"]}">{escape(cat_data["name"])}</category>')

    yml_lines.append('    </categories>')
    yml_lines.append('    <offers>')

    # 2. Подготовка строк для CSV
    csv_rows = []

    for p in products:
        p_id = p.get("id", "")
        title = clean_text(p.get("title", ""))
        price = p.get("price", 0)
        cat_key = p.get("category", "Necklaces")
        cat_info = CATEGORY_MAP.get(cat_key, {"id": "1", "name": "Украшения"})
        cat_id = cat_info["id"]
        cat_name = cat_info["name"]

        raw_img = p.get("image", "").lstrip("/")
        image_url = f"{SITE_URL}/{raw_img}" if raw_img else ""
        product_url = f"{SITE_URL}/product/{p_id}.html"

        description = clean_text(p.get("description", ""))
        in_stock = p.get("inStock", True)
        avail_str_yml = "true" if in_stock else "false"
        avail_str_csv = "в наличии" if in_stock else "под заказ"

        # Добавляем в YML
        yml_lines.append(f'      <offer id="{p_id}" available="{avail_str_yml}">')
        yml_lines.append(f'        <name>{escape(title)}</name>')
        yml_lines.append(f'        <url>{product_url}</url>')
        yml_lines.append(f'        <price>{price}</price>')
        yml_lines.append('        <currencyId>KZT</currencyId>')
        yml_lines.append(f'        <categoryId>{cat_id}</categoryId>')
        if image_url:
            yml_lines.append(f'        <picture>{image_url}</picture>')
        yml_lines.append('        <vendor>Livi Jewelry</vendor>')
        yml_lines.append(f'        <description><![CDATA[{description}]]></description>')
        yml_lines.append('      </offer>')

        # Добавляем в CSV (колонки: name;price;currency;category;url;picture;description;vendor;availability)
        csv_rows.append({
            "name": title,
            "price": price,
            "currency": "KZT",
            "category": cat_name,
            "url": product_url,
            "picture": image_url,
            "description": description,
            "vendor": "Livi Jewelry",
            "availability": avail_str_csv,
        })

    yml_lines.append('    </offers>')
    yml_lines.append('  </shop>')
    yml_lines.append('</yml_catalog>')

    # Запись YML
    with open(OUTPUT_YML, "w", encoding="utf-8") as f:
        f.write("\n".join(yml_lines) + "\n")
    print(f"Успешно сгенерирован YML: {OUTPUT_YML} ({len(products)} товаров)")

    # Запись CSV (UTF-8-SIG для корректного открытия в Excel)
    fieldnames = ["name", "price", "currency", "category", "url", "picture", "description", "vendor", "availability"]
    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"Успешно сгенерирован CSV: {OUTPUT_CSV} ({len(csv_rows)} товаров)")


if __name__ == "__main__":
    generate()
