#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Google Merchant Center XML Product Feed (RSS 2.0 / g: namespace)
for Livi Jewelry (https://livijewelry.kz)
Fully optimized for Google Shopping, Performance Max, and Google StoreBot.
"""

import json
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

BASE_URL = "https://livijewelry.kz"
PRODUCTS_FILE = "products.json"
FEED_FILE = "google_merchant_feed.xml"

# Category mapping to Google Product Taxonomy (Apparel & Accessories > Jewelry)
# 188: Jewelry, 197: Necklaces, 191: Bracelets, 200: Jewelry Sets, 194: Earrings
GOOGLE_CATEGORIES = {
    "Necklaces": ("197", "Apparel & Accessories > Jewelry > Necklaces", "Украшения > Колье", "Колье"),
    "Bracelets": ("191", "Apparel & Accessories > Jewelry > Bracelets", "Украшения > Браслеты", "Браслет"),
    "Sets": ("200", "Apparel & Accessories > Jewelry > Jewelry Sets", "Украшения > Комплекты", "Комплект"),
    "Lariats": ("197", "Apparel & Accessories > Jewelry > Necklaces", "Украшения > Сотуары", "Сотуар"),
    "Chains": ("197", "Apparel & Accessories > Jewelry > Necklaces", "Украшения > Цепи", "Цепь"),
    "Rings": ("200", "Apparel & Accessories > Jewelry > Rings", "Украшения > Кольца", "Кольцо"),
    "Earrings": ("194", "Apparel & Accessories > Jewelry > Earrings", "Украшения > Серьги", "Серьги"),
}

def detect_color(title, materials):
    text = (title + " " + " ".join(materials)).lower()
    if "малахит" in text:
        return "Изумрудный / Зеленый"
    if "аметист" in text:
        return "Фиолетовый"
    if "тигров" in text:
        return "Коричневый / Золотистый"
    if "жадеит" in text:
        return "Зеленый"
    if "гранат" in text:
        return "Бордовый / Темно-красный"
    if "агат" in text:
        return "Черный"
    if "бирюз" in text:
        return "Бирюзовый / Голубой"
    if any(k in text for k in ["розов", "кварц", "клубнич"]):
        return "Розовый / Перламутровый"
    if "флюорит" in text:
        return "Мятный / Зеленый"
    if "коралл" in text:
        return "Коралловый / Красный"
    if "яшм" in text:
        return "Терракотовый / Разноцветный"
    if "авантюрин" in text:
        return "Синий / Золотисто-коричневый"
    if any(k in text for k in ["позолот", "золот"]):
        return "Золотистый / Перламутровый"
    if any(k in text for k in ["родирован", "гематит", "серебр", "гранж"]):
        return "Серебристый / Металлик"
    return "Белый / Перламутровый"

def generate_feed():
    if not os.path.exists(PRODUCTS_FILE):
        print(f"Error: {PRODUCTS_FILE} not found!")
        return

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    rss = ET.Element("rss", {
        "version": "2.0",
        "xmlns:g": "http://base.google.com/ns/1.0"
    })
    channel = ET.SubElement(rss, "channel")

    title_el = ET.SubElement(channel, "title")
    title_el.text = "Livi Jewelry — Авторские украшения из натурального жемчуга и камней"

    link_el = ET.SubElement(channel, "link")
    link_el.text = BASE_URL

    desc_el = ET.SubElement(channel, "description")
    desc_el.text = "Каталог авторских украшений ручной работы из натурального жемчуга, малахита, агата и кварца с доставкой по Казахстану."

    for p in products:
        item = ET.SubElement(channel, "item")
        pid = str(p.get("id"))

        # 1. Basic ID / SKU
        g_id = ET.SubElement(item, "g:id")
        g_id.text = pid

        # 2. Optimized Title for Google Shopping Algorithm
        # Formula: {title} Livi Jewelry — Натуральный жемчуг ({category_ru})
        title = p.get("title", "Украшение Livi Jewelry")
        cat_key = p.get("category", "Necklaces")
        cat_info = GOOGLE_CATEGORIES.get(cat_key, ("188", "Apparel & Accessories > Jewelry", "Украшения", "Украшение"))
        cat_ru = cat_info[3]

        feed_title = f"{title} Livi Jewelry — Натуральный жемчуг ({cat_ru})"
        if len(feed_title) > 150:
            feed_title = feed_title[:147] + "..."

        g_title = ET.SubElement(item, "g:title")
        g_title.text = feed_title

        # 3. Description
        desc = p.get("description", title)
        g_desc = ET.SubElement(item, "g:description")
        g_desc.text = desc

        # 4. Canonical Link to Static Product Page
        g_link = ET.SubElement(item, "g:link")
        g_link.text = f"{BASE_URL}/product/{pid}.html"

        # 5. Image Link
        img_rel = p.get("image", "").lstrip("/")
        g_img = ET.SubElement(item, "g:image_link")
        g_img.text = f"{BASE_URL}/{img_rel}"

        # 6. Availability & Condition
        g_avail = ET.SubElement(item, "g:availability")
        g_avail.text = "in_stock" if p.get("inStock", True) else "out_of_stock"

        g_cond = ET.SubElement(item, "g:condition")
        g_cond.text = "new"

        # 7. Price in KZT
        price_num = int(p.get("price", 0))
        g_price = ET.SubElement(item, "g:price")
        g_price.text = f"{price_num} KZT"

        # 8. Brand
        g_brand = ET.SubElement(item, "g:brand")
        g_brand.text = "Livi Jewelry"

        # 9. Google Categories & Product Type
        g_cat = ET.SubElement(item, "g:google_product_category")
        g_cat.text = cat_info[0]

        g_prod_type = ET.SubElement(item, "g:product_type")
        g_prod_type.text = cat_info[2]

        # 10. Apparel / Jewelry Attributes: Gender & Age Group
        g_gender = ET.SubElement(item, "g:gender")
        g_gender.text = "female"

        g_age = ET.SubElement(item, "g:age_group")
        g_age.text = "adult"

        # 11. Material & Color
        materials = p.get("materials", [])
        if materials:
            g_mat = ET.SubElement(item, "g:material")
            g_mat.text = " / ".join(materials)

        g_color = ET.SubElement(item, "g:color")
        g_color.text = detect_color(title, materials)

        # 12. Custom Labels for PMax segmentation
        g_label0 = ET.SubElement(item, "g:custom_label_0")
        g_label0.text = "Featured" if p.get("featured", False) else "Standard"

        g_label1 = ET.SubElement(item, "g:custom_label_1")
        if price_num >= 50000:
            g_label1.text = "High_Ticket"
        elif price_num >= 30000:
            g_label1.text = "Mid_Ticket"
        else:
            g_label1.text = "Entry_Ticket"

        # 13. Handmade / Custom product identifier
        g_identifier = ET.SubElement(item, "g:identifier_exists")
        g_identifier.text = "no"

    # Pretty print XML
    xml_str = ET.tostring(rss, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

    with open(FEED_FILE, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"[OK] Successfully generated Google Merchant Feed: {FEED_FILE} ({len(products)} products)")

if __name__ == "__main__":
    generate_feed()
