#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор товарного фида и каталога Livi Jewelry для маркетплейса Kaspi.kz:
  1. kaspi_feed.xml   — Официальный XML-фид прайс-листа (наличие, цены, предзаказ)
                        для автоматической ежечасной синхронизации по URL.
  2. kaspi_catalog.csv — CSV-файл (UTF-8-SIG, разделитель ';') со всеми деталями,
                        характеристиками и ссылками на HD-фото для пакетного
                        создания и модерации карточек товаров в Kaspi Pay.
"""

import os
import sys
import json
import csv
import datetime
from xml.sax.saxutils import escape

SITE_URL = "https://livijewelry.kz"
PRODUCTS_FILE = "products.json"
OUTPUT_XML = "kaspi_feed.xml"
OUTPUT_CSV = "kaspi_catalog.csv"

# Настройки продавца в Kaspi
COMPANY_NAME = "Livi Jewelry"
MERCHANT_ID = os.environ.get("KASPI_MERCHANT_ID", "LiviJewelry")
DEFAULT_STORE_ID = os.environ.get("KASPI_STORE_ID", "PP1")

# Категории Kaspi в классификаторе «Украшения и бижутерия»
KASPI_CATEGORY_MAP = {
    "Necklaces": "Украшения и бижутерия > Колье, бусы и ожерелья",
    "Lariats": "Украшения и бижутерия > Колье, бусы и ожерелья",
    "Chains": "Украшения и бижутерия > Цепи и колье",
    "Bracelets": "Украшения и бижутерия > Браслеты",
    "Earrings": "Украшения и бижутерия > Серьги",
    "Rings": "Украшения и бижутерия > Кольца",
    "Brooches": "Украшения и бижутерия > Броши",
    "Sets": "Украшения и бижутерия > Комплекты украшений",
}


def clean_text(text: str) -> str:
    """Удаляет лишние пробелы, переносы строк и спецсимволы."""
    if not text:
        return ""
    return " ".join(text.split())


def is_preorder(product: dict) -> bool:
    """Определяет, изготавливается ли товар под заказ."""
    title = product.get("title", "").lower()
    desc = product.get("description", "").lower()
    return "под заказ" in title or "под заказ" in desc or product.get("preorder", False)


def get_image_url(product: dict) -> str:
    """Возвращает абсолютную ссылку на основную фотографию товара."""
    img_rel = product.get("image", "").lstrip("/")
    if not img_rel:
        return ""
    return f"{SITE_URL}/{img_rel}"


def get_additional_images(product: dict) -> str:
    """Возвращает дополнительные фото товара через запятую."""
    images = product.get("images", [])
    if not images or len(images) <= 1:
        return ""
    # Исключаем первое фото, если оно совпадает с главным
    extra = [f"{SITE_URL}/{img.lstrip('/')}" for img in images[1:] if img]
    return ", ".join(extra)


def generate_kaspi_xml(products: list, output_file: str = OUTPUT_XML):
    """Генерирует официальный kaspi_catalog XML фид по спецификации Kaspi."""
    now_iso = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    xml_lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        f'<kaspi_catalog date="{now_iso}" xmlns="kaspiShopping" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="kaspiShopping http://kaspi.kz/kaspishopping.xsd">',
        f'  <company>{escape(COMPANY_NAME)}</company>',
        f'  <merchantid>{escape(MERCHANT_ID)}</merchantid>',
        '  <offers>',
    ]

    for p in products:
        sku = escape(str(p.get("sku") or p.get("id", "")))
        title = escape(clean_text(p.get("title", "")))
        price_val = int(p.get("price", 0))
        in_stock = bool(p.get("inStock", True))
        preorder_flag = is_preorder(p)

        available_str = "yes" if in_stock else "no"
        preorder_days = 5 if preorder_flag else 0

        xml_lines.append(f'    <offer sku="{sku}">')
        xml_lines.append(f'      <model>{title}</model>')
        xml_lines.append(f'      <brand>{escape(COMPANY_NAME)}</brand>')
        xml_lines.append('      <availabilities>')
        xml_lines.append(
            f'        <availability available="{available_str}" storeId="{DEFAULT_STORE_ID}" preOrder="{preorder_days}"/>'
        )
        xml_lines.append('      </availabilities>')
        xml_lines.append(f'      <price>{price_val}</price>')
        xml_lines.append('    </offer>')

    xml_lines.append('  </offers>')
    xml_lines.append('</kaspi_catalog>')

    xml_content = "\n".join(xml_lines)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_content)

    print(f"[OK] Kaspi XML фид сгенерирован: {output_file} ({len(products)} предложений)")


def generate_kaspi_csv(products: list, output_file: str = OUTPUT_CSV):
    """Генерирует CSV-файл для пакетной загрузки и создания карточек в кабинете Kaspi."""
    fieldnames = [
        "Артикул (SKU)",
        "Название товара (Модель)",
        "Категория Kaspi",
        "Бренд",
        "Цена (KZT)",
        "Статус наличия",
        "Срок предзаказа (дней)",
        "Основное фото (URL)",
        "Дополнительные фото (URLs)",
        "Материалы и вставки",
        "Фурнитура",
        "Длина / Размер",
        "Тип замка",
        "Упаковка",
        "Страна-производитель",
        "Детальное описание товара",
        "Ссылка на карточку на сайте",
    ]

    with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(fieldnames)

        for p in products:
            sku = p.get("sku") or p.get("id", "")
            title = clean_text(p.get("title", ""))
            cat_key = p.get("category", "Necklaces")
            kaspi_cat = KASPI_CATEGORY_MAP.get(cat_key, "Украшения и бижутерия > Авторские украшения")
            price_val = int(p.get("price", 0))

            in_stock = bool(p.get("inStock", True))
            preorder_flag = is_preorder(p)
            if not in_stock:
                status_str = "Нет в наличии"
                preorder_days = 0
            elif preorder_flag:
                status_str = "Под заказ"
                preorder_days = 5
            else:
                status_str = "В наличии"
                preorder_days = 0

            main_img = get_image_url(p)
            extra_imgs = get_additional_images(p)

            specs = p.get("specs", {})
            materials_list = p.get("materials", [])
            materials_str = specs.get("stones_detail") or ", ".join(materials_list)
            hardware_str = specs.get("hardware", "Ювелирный сплав с родиевым / позолоченным покрытием")
            length_str = specs.get("length_size", "Стандартная (с удлинительной цепочкой)")
            clasp_str = specs.get("clasp", "Карабин")
            packaging_str = specs.get("packaging", "Фирменная подарочная упаковка Livi Jewelry")

            description = clean_text(p.get("description", ""))
            product_url = f"{SITE_URL}/product/{p.get('id')}.html"

            writer.writerow([
                sku,
                title,
                kaspi_cat,
                COMPANY_NAME,
                price_val,
                status_str,
                preorder_days,
                main_img,
                extra_imgs,
                materials_str,
                hardware_str,
                length_str,
                clasp_str,
                packaging_str,
                "Казахстан",
                description,
                product_url,
            ])

    print(f"[OK] Kaspi CSV каталог сгенерирован: {output_file} ({len(products)} товаров)")


def generate_kaspi():
    """Точка входа для запуска из других скриптов и оркестраторов."""
    if not os.path.exists(PRODUCTS_FILE):
        print(f"[FAIL] {PRODUCTS_FILE} не найден!")
        return

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    generate_kaspi_xml(products, OUTPUT_XML)
    generate_kaspi_csv(products, OUTPUT_CSV)


if __name__ == "__main__":
    generate_kaspi()
