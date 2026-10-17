#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate comprehensive sitemap.xml for Livi Jewelry (https://livijewelry.kz)
Includes main landing pages, category SEO landing pages, and all static product pages.
"""

import json
import os
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

BASE_URL = "https://livijewelry.kz"
PRODUCTS_FILE = "products.json"
SITEMAP_FILE = "sitemap.xml"

# Static site sections with priority and change frequency
STATIC_PAGES = [
    {
        "loc": f"{BASE_URL}/",
        "priority": "1.0",
        "changefreq": "daily"
    },
    {
        "loc": f"{BASE_URL}/shop.html",
        "priority": "0.9",
        "changefreq": "daily"
    },
    {
        "loc": f"{BASE_URL}/kolye-iz-zhemchuga.html",
        "priority": "0.8",
        "changefreq": "weekly"
    },
    {
        "loc": f"{BASE_URL}/braslety-iz-zhemchuga.html",
        "priority": "0.8",
        "changefreq": "weekly"
    },
    {
        "loc": f"{BASE_URL}/sergi-iz-zhemchuga.html",
        "priority": "0.8",
        "changefreq": "weekly"
    },
    {
        "loc": f"{BASE_URL}/delivery.html",
        "priority": "0.6",
        "changefreq": "monthly"
    },
    {
        "loc": f"{BASE_URL}/privacy.html",
        "priority": "0.5",
        "changefreq": "monthly"
    },
    {
        "loc": f"{BASE_URL}/terms.html",
        "priority": "0.5",
        "changefreq": "monthly"
    }
]

def generate_sitemap():
    today = datetime.now().strftime("%Y-%m-%d")

    urlset = ET.Element("urlset", {
        "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"
    })

    total_urls = 0

    # 1. Main and Category pages
    for p in STATIC_PAGES:
        url_el = ET.SubElement(urlset, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = p["loc"]

        lastmod_el = ET.SubElement(url_el, "lastmod")
        lastmod_el.text = today

        changefreq_el = ET.SubElement(url_el, "changefreq")
        changefreq_el.text = p["changefreq"]

        prio_el = ET.SubElement(url_el, "priority")
        prio_el.text = p["priority"]
        total_urls += 1

    # 2. Product Pages from products.json
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            products = json.load(f)

        for prod in products:
            pid = prod.get("id")
            if not pid:
                continue

            url_el = ET.SubElement(urlset, "url")
            loc_el = ET.SubElement(url_el, "loc")
            loc_el.text = f"{BASE_URL}/product/{pid}.html"

            lastmod_el = ET.SubElement(url_el, "lastmod")
            lastmod_el.text = today

            changefreq_el = ET.SubElement(url_el, "changefreq")
            changefreq_el.text = "weekly"

            prio_el = ET.SubElement(url_el, "priority")
            prio_el.text = "0.8"
            total_urls += 1

    # Format pretty XML
    xml_str = ET.tostring(urlset, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"[OK] Successfully generated sitemap: {SITEMAP_FILE} ({total_urls} URLs)")
    return total_urls

if __name__ == "__main__":
    generate_sitemap()
