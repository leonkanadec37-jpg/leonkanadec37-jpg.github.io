#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Google Merchant Center XML Product Feed (RSS 2.0 / g: namespace)
for Livi Jewelry (https://livijewelry.kz)
"""

import json
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

BASE_URL = "https://livijewelry.kz"
PRODUCTS_FILE = "products.json"
FEED_FILE = "google_merchant_feed.xml"

# Category mapping to Google Product Taxonomy (Apparel & Accessories > Jewelry)
# 188: Jewelry, 197: Necklaces, 191: Bracelets, 200: Jewelry Sets
GOOGLE_CATEGORIES = {
    "Necklaces": ("197", "Apparel & Accessories > Jewelry > Necklaces", "Украшения > Колье"),
    "Bracelets": ("191", "Apparel & Accessories > Jewelry > Bracelets", "Украшения > Браслеты"),
    "Sets": ("200", "Apparel & Accessories > Jewelry > Jewelry Sets", "Украшения > Комплекты"),
    "Lariats": ("197", "Apparel & Accessories > Jewelry > Necklaces", "Украшения > Сотуары"),
    "Chains": ("197", "Apparel & Accessories > Jewelry > Necklaces", "Украшения > Цепи"),
}

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

        # Basic ID
        g_id = ET.SubElement(item, "g:id")
        g_id.text = str(p.get("id"))

        # Title
        title = p.get("title", "Украшение Livi Jewelry")
        g_title = ET.SubElement(item, "g:title")
        g_title.text = f"{title} | Livi Jewelry"

        # Description
        desc = p.get("description", title)
        g_desc = ET.SubElement(item, "g:description")
        g_desc.text = desc

        # Link
        g_link = ET.SubElement(item, "g:link")
        g_link.text = f"{BASE_URL}/shop.html?item={p.get('id')}"

        # Image Link
        img_rel = p.get("image", "").lstrip("/")
        g_img = ET.SubElement(item, "g:image_link")
        g_img.text = f"{BASE_URL}/{img_rel}"

        # Availability & Condition
        g_avail = ET.SubElement(item, "g:availability")
        g_avail.text = "in_stock" if p.get("inStock", True) else "out_of_stock"

        g_cond = ET.SubElement(item, "g:condition")
        g_cond.text = "new"

        # Price in KZT
        price_num = int(p.get("price", 0))
        g_price = ET.SubElement(item, "g:price")
        g_price.text = f"{price_num} KZT"

        # Brand
        g_brand = ET.SubElement(item, "g:brand")
        g_brand.text = "Livi Jewelry"

        # Categories
        cat_key = p.get("category", "Necklaces")
        cat_info = GOOGLE_CATEGORIES.get(cat_key, ("188", "Apparel & Accessories > Jewelry", "Украшения"))
        
        g_cat = ET.SubElement(item, "g:google_product_category")
        g_cat.text = cat_info[0]

        g_prod_type = ET.SubElement(item, "g:product_type")
        g_prod_type.text = cat_info[2]

        # Materials
        materials = p.get("materials", [])
        if materials:
            g_mat = ET.SubElement(item, "g:material")
            g_mat.text = ", ".join(materials)

        # Custom Labels for PMax segmentation
        g_label0 = ET.SubElement(item, "g:custom_label_0")
        g_label0.text = "Featured" if p.get("featured", False) else "Standard"

        g_label1 = ET.SubElement(item, "g:custom_label_1")
        if price_num >= 50000:
            g_label1.text = "High_Ticket"
        elif price_num >= 30000:
            g_label1.text = "Mid_Ticket"
        else:
            g_label1.text = "Entry_Ticket"

        # Handmade / Custom product identifier
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
