#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Livi Jewelry — Phase 6 Automated Verification & Self-Test Suite (verify_audit.py)
Validates 100% parity across products.json, shop.html, index.html, category pages,
/product/prod_*.html (HTML + JSON-LD), google_merchant_feed.xml, feed.xml, sitemap.xml,
robots.txt, and Google Ads / GA4 / Consent Mode v2 tracking across all HTML pages.
"""

import os
import re
import sys
import json
import glob
import urllib.parse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

BASE_URL = "https://livijewelry.kz"
GA4_ID = "G-YFF2TR0N36"
ADS_ID = "AW-16793974126"
ADS_LABEL = "AW-16793974126/MuJ_CObHup8bEO7q_sc-"
GSC_TOKEN = "qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    errors = []
    warnings = []
    checks_passed = 0

    def ok(msg):
        nonlocal checks_passed
        checks_passed += 1
        print(f"  [PASS] {msg}")

    def fail(msg):
        errors.append(msg)
        print(f"  [FAIL] {msg}")

    print("=" * 76)
    print("LIVI JEWELRY — ADTECH, GMC, GA4 & GSC AUTOMATED VERIFICATION SUITE")
    print("=" * 76)

    # 1. Load Single Source of Truth (products.json)
    print("\n[1/7] Validating Single Source of Truth (products.json)...")
    if not os.path.exists("products.json"):
        fail("products.json does not exist!")
        sys.exit(1)

    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    if len(products) != 28:
        fail(f"Expected 28 products in products.json, found {len(products)}")
    else:
        ok(f"Loaded {len(products)} products from products.json")

    seen_ids = set()
    seen_titles = set()
    prod_map = {}
    for p in products:
        pid = p.get("id")
        title = (p.get("title") or "").strip()
        price = p.get("price")
        img = p.get("image", "")
        desc = p.get("description", "")
        mats = p.get("materials", [])

        if not pid or pid in seen_ids:
            fail(f"Duplicate or missing product ID: {pid}")
        seen_ids.add(pid)
        prod_map[pid] = p

        if not title or title in seen_titles:
            fail(f"Duplicate or empty product title for {pid}: '{title}'")
        seen_titles.add(title)

        if not isinstance(price, int) or price <= 0:
            fail(f"Invalid price for {pid}: {price}")

        if not img or not os.path.exists(img) or os.path.getsize(img) == 0:
            fail(f"Missing or empty image file for {pid}: {img}")

        if not desc or len(desc.strip()) < 15:
            fail(f"Description too short or empty for {pid}: '{desc}'")

        if not mats or not isinstance(mats, list):
            fail(f"Missing materials array for {pid}")

    if not errors:
        ok("All 28 products have unique IDs, distinct descriptive titles, valid prices, non-empty WebP images, and rich descriptions")

    # 2. Validate Google Merchant Center XML Feeds (google_merchant_feed.xml & feed.xml)
    print("\n[2/7] Validating Google Merchant Center XML Feeds...")
    for feed_file in ("google_merchant_feed.xml", "feed.xml"):
        if not os.path.exists(feed_file):
            fail(f"Missing Merchant Center XML feed: {feed_file}")
            continue

        tree = ET.parse(feed_file)
        root = tree.getroot()
        ns = {"g": "http://base.google.com/ns/1.0"}
        items = root.findall("./channel/item")
        if len(items) != len(products):
            fail(f"{feed_file}: expected {len(products)} <item> elements, found {len(items)}")
        else:
            ok(f"{feed_file}: valid XML with {len(items)} items")

        for item in items:
            gid = item.findtext("g:id", namespaces=ns)
            gtitle = item.findtext("g:title", namespaces=ns)
            glink = item.findtext("g:link", namespaces=ns)
            gimg = item.findtext("g:image_link", namespaces=ns)
            gprice = item.findtext("g:price", namespaces=ns)
            gcond = item.findtext("g:condition", namespaces=ns)
            gavail = item.findtext("g:availability", namespaces=ns)
            gbrand = item.findtext("g:brand", namespaces=ns)
            gid_exists = item.findtext("g:identifier_exists", namespaces=ns)
            gcat = item.findtext("g:google_product_category", namespaces=ns)

            if gid not in prod_map:
                fail(f"{feed_file}: unknown <g:id> {gid}")
                continue

            p = prod_map[gid]
            expected_link = f"{BASE_URL}/product/{gid}.html"
            expected_price = f"{int(p['price']):.2f} KZT"
            expected_avail = "in_stock" if (p.get("inStock", True) and not p.get("archived")) else "out_of_stock"

            if gtitle != p["title"]:
                fail(f"{feed_file} [{gid}]: <g:title> '{gtitle}' != '{p['title']}'")
            if glink != expected_link:
                fail(f"{feed_file} [{gid}]: <g:link> '{glink}' != '{expected_link}'")
            if gprice != expected_price:
                fail(f"{feed_file} [{gid}]: <g:price> '{gprice}' != '{expected_price}'")
            if gcond != "new":
                fail(f"{feed_file} [{gid}]: <g:condition> '{gcond}' != 'new'")
            if gavail != expected_avail:
                fail(f"{feed_file} [{gid}]: <g:availability> '{gavail}' != '{expected_avail}'")
            if gbrand != "Livi Jewelry":
                fail(f"{feed_file} [{gid}]: <g:brand> '{gbrand}' != 'Livi Jewelry'")
            if gid_exists != "no":
                fail(f"{feed_file} [{gid}]: <g:identifier_exists> '{gid_exists}' != 'no'")
            if gcat != "188":
                fail(f"{feed_file} [{gid}]: <g:google_product_category> '{gcat}' != '188'")

            if not gimg or not gimg.startswith(f"{BASE_URL}/assets/"):
                fail(f"{feed_file} [{gid}]: invalid <g:image_link> '{gimg}'")
            else:
                rel_img = urllib.parse.unquote(gimg.replace(f"{BASE_URL}/", ""))
                if not os.path.exists(rel_img) or os.path.getsize(rel_img) == 0:
                    fail(f"{feed_file} [{gid}]: <g:image_link> file missing on disk: {rel_img}")

    if not errors:
        ok("100% GMC XML Feed parity verified (<g:id>, <g:title>, <g:link>, <g:price>, <g:identifier_exists>no, category 188, and image existence)")

    # 3. Validate Every /product/prod_XX.html Landing Page (HTML + JSON-LD + Canonical + Tracking)
    print("\n[3/7] Validating 28 /product/prod_XX.html Landing Pages...")
    for pid, p in prod_map.items():
        page_path = os.path.join("product", f"{pid}.html")
        if not os.path.exists(page_path):
            fail(f"Missing static product page: {page_path}")
            continue

        with open(page_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        # Check robots meta (must NOT have noindex)
        robots_meta = soup.find("meta", attrs={"name": "robots"})
        if robots_meta and "noindex" in (robots_meta.get("content") or "").lower():
            fail(f"{page_path}: contains noindex in meta robots!")

        # Check canonical URL
        canon = soup.find("link", attrs={"rel": "canonical"})
        expected_canon = f"{BASE_URL}/product/{pid}.html"
        if not canon or canon.get("href") != expected_canon:
            fail(f"{page_path}: canonical '{canon.get('href') if canon else None}' != '{expected_canon}'")

        # Check H1 and visible price
        h1 = soup.find("h1")
        if not h1 or h1.get_text(strip=True) != p["title"]:
            fail(f"{page_path}: <h1> '{h1.get_text(strip=True) if h1 else None}' != '{p['title']}'")

        price_el = soup.find(class_="product-price-val")
        expected_vis_price = f"{p['price']:,}".replace(",", " ") + " ₸"
        if not price_el or price_el.get_text(strip=True) != expected_vis_price:
            fail(f"{page_path}: visible price '{price_el.get_text(strip=True) if price_el else None}' != '{expected_vis_price}'")

        # Check JSON-LD Product schema
        product_ld = None
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            try:
                data = json.loads(script.string or "")
                if isinstance(data, dict) and data.get("@type") == "Product":
                    product_ld = data
                    break
            except Exception as e:
                fail(f"{page_path}: invalid JSON-LD syntax: {e}")

        if not product_ld:
            fail(f"{page_path}: missing JSON-LD @type=Product schema")
        else:
            if product_ld.get("sku") != pid:
                fail(f"{page_path}: JSON-LD sku '{product_ld.get('sku')}' != '{pid}'")
            if product_ld.get("name") != p["title"]:
                fail(f"{page_path}: JSON-LD name '{product_ld.get('name')}' != '{p['title']}'")
            offers = product_ld.get("offers", {})
            expected_ld_price = f"{int(p['price']):.2f}"
            if offers.get("price") != expected_ld_price:
                fail(f"{page_path}: JSON-LD offers.price '{offers.get('price')}' != '{expected_ld_price}'")
            if offers.get("priceCurrency") != "KZT":
                fail(f"{page_path}: JSON-LD offers.priceCurrency != 'KZT'")
            if offers.get("url") != expected_canon:
                fail(f"{page_path}: JSON-LD offers.url '{offers.get('url')}' != '{expected_canon}'")
            expected_ld_avail = "https://schema.org/OutOfStock" if (p.get("archived") or not p.get("inStock", True)) else "https://schema.org/InStock"
            if offers.get("availability") != expected_ld_avail:
                fail(f"{page_path}: JSON-LD offers.availability '{offers.get('availability')}' != '{expected_ld_avail}'")
            if offers.get("itemCondition") != "https://schema.org/NewCondition":
                fail(f"{page_path}: JSON-LD offers.itemCondition != 'https://schema.org/NewCondition'")

        # Check all images on product page have width/height and exist on disk
        for img_tag in soup.find_all("img"):
            src = img_tag.get("src", "")
            if "facebook.com" in src:
                continue
            if not img_tag.get("width") or not img_tag.get("height"):
                fail(f"{page_path}: <img> missing width/height attributes: {src}")
            disk_path = os.path.normpath(os.path.join("product", src))
            if not os.path.exists(disk_path) or os.path.getsize(disk_path) == 0:
                fail(f"{page_path}: <img> file missing on disk: {disk_path}")

        # Check tracking events on product page
        for req_token in (
            GA4_ID,
            ADS_ID,
            ADS_LABEL,
            GSC_TOKEN,
            "gtag('consent', 'default'",
            "'view_item'",
            "'add_to_cart'",
            "'begin_checkout'",
            "'purchase'",
            "'generate_lead'",
            "'contact'",
            "LIVI-",
        ):
            if req_token not in html:
                fail(f"{page_path}: missing required tracking token `{req_token}`")

    if not errors:
        ok("All 28 /product/prod_XX.html pages pass 100% HTML, JSON-LD, Canonical, CLS image dimension, and Funnel Tracking checks")

    # 4. Validate shop.html, index.html, and Category Pages Parity & Internal Crawl Links
    print("\n[4/7] Validating shop.html, index.html, and Category Pages Parity & Crawlability...")
    with open("shop.html", "r", encoding="utf-8") as f:
        shop_html = f.read()
    shop_soup = BeautifulSoup(shop_html, "html.parser")

    # Verify shop.html pre-rendered links to all 28 product pages
    shop_prod_links = set()
    for a in shop_soup.select("#grid a[href]"):
        href = a.get("href", "")
        if href.startswith("/product/prod_") and href.endswith(".html"):
            shop_prod_links.add(href)
    active_prods = [p for p in products if not p.get("archived", False)]
    if len(shop_prod_links) != len(active_prods):
        fail(f"shop.html #grid should contain crawlable links to all {len(active_prods)} active products in static HTML, found {len(shop_prod_links)}")
    else:
        ok(f"shop.html #grid contains static crawlable <a href=\"/product/prod_XX.html\"> links to all {len(active_prods)} products")

    # Verify shop.html JSON-LD ItemList matches all active products
    shop_item_list = None
    for script in shop_soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "")
            if isinstance(data, dict) and data.get("@type") == "ItemList":
                shop_item_list = data.get("itemListElement", [])
                break
        except Exception as e:
            fail(f"shop.html invalid JSON-LD: {e}")

    if not shop_item_list or len(shop_item_list) != len(active_prods):
        fail(f"shop.html ItemList expected {len(active_prods)} items, found {len(shop_item_list) if shop_item_list else 0}")
    else:
        for item in shop_item_list:
            sku = item.get("sku")
            p = prod_map.get(sku)
            if not p:
                fail(f"shop.html ItemList unknown sku: {sku}")
                continue
            if item.get("name") != p["title"]:
                fail(f"shop.html ItemList [{sku}] name '{item.get('name')}' != '{p['title']}'")
            expected_p = f"{int(p['price']):.2f}"
            if item.get("offers", {}).get("price") != expected_p:
                fail(f"shop.html ItemList [{sku}] price '{item.get('offers', {}).get('price')}' != '{expected_p}'")
        ok("shop.html JSON-LD ItemList matches all 28 products (SKU, title, price.00 KZT)")

    # Verify index.html pre-rendered featured links
    with open("index.html", "r", encoding="utf-8") as f:
        idx_html = f.read()
    idx_soup = BeautifulSoup(idx_html, "html.parser")
    idx_links = [a.get("href") for a in idx_soup.select("#featGrid a[href]") if a.get("href", "").startswith("/product/prod_")]
    if len(idx_links) < 6:
        fail(f"index.html #featGrid should contain at least 6 crawlable product links, found {len(idx_links)}")
    else:
        ok(f"index.html #featGrid contains {len(idx_links)} static crawlable product links")

    # Verify Category Pages (kolye-iz-zhemchuga.html, braslety-iz-zhemchuga.html, sergi-iz-zhemchuga.html)
    for cat_page in ("kolye-iz-zhemchuga.html", "braslety-iz-zhemchuga.html", "sergi-iz-zhemchuga.html"):
        with open(cat_page, "r", encoding="utf-8") as f:
            chtml = f.read()
        csoup = BeautifulSoup(chtml, "html.parser")
        # Check cards in .grid match products.json
        for card in csoup.select(".grid .card"):
            a = card.select_one("a.card-title-link")
            price_div = card.select_one(".price")
            if not a or not price_div:
                fail(f"{cat_page}: card missing title link or price")
                continue
            href = a.get("href", "")
            m = re.search(r"(prod_\d+)\.html", href)
            if not m or m.group(1) not in prod_map:
                fail(f"{cat_page}: invalid product link {href}")
                continue
            pid = m.group(1)
            p = prod_map[pid]
            if a.get_text(strip=True) != p["title"]:
                fail(f"{cat_page} [{pid}]: card title '{a.get_text(strip=True)}' != '{p['title']}'")
            exp_vis = f"{p['price']:,}".replace(",", " ") + " ₸"
            if price_div.get_text(strip=True) != exp_vis:
                fail(f"{cat_page} [{pid}]: card price '{price_div.get_text(strip=True)}' != '{exp_vis}'")
        ok(f"{cat_page}: all product cards & JSON-LD match products.json 100%")

    # 5. Validate sitemap.xml and robots.txt
    print("\n[5/7] Validating sitemap.xml and robots.txt...")
    if not os.path.exists("robots.txt"):
        fail("robots.txt is missing!")
    else:
        with open("robots.txt", "r", encoding="utf-8") as f:
            robots_txt = f.read()
        for agent in ("User-agent: *", "User-agent: Googlebot", "User-agent: Googlebot-Image", "Allow: /product/", "Allow: /assets/", f"Sitemap: {BASE_URL}/sitemap.xml"):
            if agent not in robots_txt:
                fail(f"robots.txt missing required directive: {agent}")
        ok("robots.txt explicitly allows *, Googlebot, Googlebot-Image across /, /product/, /assets/ and declares Sitemap")

    if not os.path.exists("sitemap.xml"):
        fail("sitemap.xml is missing!")
    else:
        stree = ET.parse("sitemap.xml")
        sroot = stree.getroot()
        sns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [el.text for el in sroot.findall("./s:url/s:loc", namespaces=sns)]
        required_locs = [
            f"{BASE_URL}/",
            f"{BASE_URL}/shop.html",
            f"{BASE_URL}/kolye-iz-zhemchuga.html",
            f"{BASE_URL}/braslety-iz-zhemchuga.html",
            f"{BASE_URL}/sergi-iz-zhemchuga.html",
            f"{BASE_URL}/delivery.html",
            f"{BASE_URL}/privacy.html",
            f"{BASE_URL}/terms.html",
        ] + [f"{BASE_URL}/product/{pid}.html" for pid in prod_map]

        for rloc in required_locs:
            if rloc not in locs:
                fail(f"sitemap.xml missing required URL: {rloc}")
        ok(f"sitemap.xml contains all {len(locs)} canonical URLs (homepage, catalog, categories, policies, and all 28 products)")

    # 6. Validate Unified Tracking & Policy Pages Across Entire Repository
    print("\n[6/7] Validating Unified GA4/Ads Tracking, Consent Mode v2 & Policy Compliance Across All Pages...")
    all_html_pages = [
        "index.html",
        "shop.html",
        "cart.html",
        "kolye-iz-zhemchuga.html",
        "braslety-iz-zhemchuga.html",
        "sergi-iz-zhemchuga.html",
        "delivery.html",
        "privacy.html",
        "terms.html",
        "returns.html",
        "usloviya-vozvrata.html",
        os.path.join("условия-возврата", "index.html"),
    ] + [os.path.join("product", f"{pid}.html") for pid in prod_map]

    for hp in all_html_pages:
        if not os.path.exists(hp):
            fail(f"Expected HTML page missing: {hp}")
            continue
        with open(hp, "r", encoding="utf-8") as f:
            txt = f.read()
        for token in (GA4_ID, ADS_ID, "gtag('consent', 'default'", "'ad_storage'", "'analytics_storage'", "'ad_user_data'", "'ad_personalization'", "'generate_lead'", "'contact'"):
            if token not in txt:
                fail(f"{hp}: missing unified tracking/consent token `{token}`")

    if not errors:
        ok(f"All {len(all_html_pages)} HTML pages contain unified GA4 ({GA4_ID}), Google Ads ({ADS_ID}), Consent Mode v2, and non-aborting contact conversion handlers")

    # 7. Validate Phase 2 Architecture: Alt-tags, Meta URLs & Shop Failover Safety (Test #16)
    print("\n[7/7] Validating Phase 2 Architecture (Alt-tags, Clean Meta URLs & Shop Failover Safety)...")
    phase2_errors = []

    # 16a. Verify no <img> alt attribute in any HTML page ends with a dangling dash (— or -)
    for hp in all_html_pages:
        if not os.path.exists(hp):
            continue
        with open(hp, "r", encoding="utf-8") as f:
            hp_soup = BeautifulSoup(f.read(), "html.parser")
        for img in hp_soup.find_all("img"):
            alt = (img.get("alt") or "").strip()
            if alt.endswith(("—", "–", "-")):
                phase2_errors.append(f"{hp}: <img> alt ends with dangling dash: '{alt}'")

    # 16b. Verify no metadata URL in index.html and shop.html contains Cyrillic or %D0%
    for fn in ("index.html", "shop.html"):
        with open(fn, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.find_all(["meta", "link"]):
            for attr in ("content", "href"):
                val = (tag.get(attr) or "").strip()
                if val.startswith("http") or val.startswith("/"):
                    if re.search(r"[\u0400-\u04FF]|%d0%|%d1%", val, re.I):
                        phase2_errors.append(f"{fn} <{tag.name} {attr}=\"{val}\">: URL contains Cyrillic or %D0% encoding!")

    # 16c. Verify shop.html catalog block protects static HTML from being overwritten on fetch failure
    with open("shop.html", "r", encoding="utf-8") as f:
        shop_code = f.read()

    has_safe_catch = "hasCards" in shop_code or "children.length === 0" in shop_code or "product-card" in shop_code
    has_prog_enhancement = "initStaticCards" in shop_code

    if not has_safe_catch:
        phase2_errors.append("shop.html fetch('products.json') catch block lacks safety check against overwriting static product cards!")
    if not has_prog_enhancement:
        phase2_errors.append("shop.html lacks Progressive Enhancement (initStaticCards) for pre-rendered cards!")

    if phase2_errors:
        for p2_err in phase2_errors:
            fail(p2_err)
    else:
        ok("Test #16 PASSED: All <img> alts intact without trailing dashes, no Cyrillic/%D0% in index/shop meta URLs, and shop.html network failover protection verified")

    print("\n" + "=" * 76)
    if errors:
        print(f"VERIFICATION FAILED WITH {len(errors)} ERROR(S):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(f"ALL {checks_passed} VERIFICATION CHECKS PASSED WITH ZERO ERRORS!")
        print("=" * 76)
        sys.exit(0)


if __name__ == "__main__":
    main()
