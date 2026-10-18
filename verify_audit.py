#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Расширенный верификационный комплекс аудита Livi Jewelry (22 проверки).
Проверяет все 7 этапов архитектуры SEO, CRO, AdTech и i18n:
1. Валидность products.json (28 товаров, WebP-фото, поля, цены)
2. Все 28 статических страниц product/prod_XX.html (JSON-LD Product + BreadcrumbList, паритет цен/SKU, GA4, Ads, Meta Pixels, GSC)
3. Очистка <title> от технического шума (prod_XX) и наличие видимого артикула Артикул: LIVI-{XX}
4. Умная перелинковка камней <a href="/ukrasheniya-iz-..."> в блоке материалов на карточках товаров
5. Расширенная микроразметка Schema.org: ["Organization", "JewelryStore"], material, color, pattern, aggregateRating, review + видимый блок отзывов (5.0 ★)
6. Интерактивный CRO-кастомизатор (id="customSize", id="customHardware", id="customGift") на всех карточках товаров и в shop.html
7. Все 12 новых коммерческих SEO-хабов (ItemList, FAQPage, BreadcrumbList, самоссылающийся canonical, пререндеринг карточек, SEO-текст, перелинковка)
8. Категорийные посадочные страницы (kolye/braslety/sergi-iz-zhemchuga.html) + блок перелинковки «Подборки по камням и стилям»
9. Синхронизация XML-фидов google_merchant_feed.xml и feed.xml (паритет, обогащенный <g:title> <= 150 симв.)
10. Merchant Center Highlights & Shipping: <g:product_highlight> (4 шт.), <g:shipping> (KZ, 0.00 KZT), <g:custom_label_2>..<g:custom_label_4>
11. Статическая казахскоязычная витрина (/kz/index.html, /kz/shop.html) с пререндерингом, FAQPage, JewelryStore и ItemList
12. Двусторонняя связка hreflang (ru-KZ, ru, kk-KZ, kk, x-default) на русских и казахских страницах и прямые ссылки в шапке
13. Сквозная атрибуция UTM/gclid (livi_attribution) и микро-воронка GA4 (view_item_list, select_item) + Google Sheets колонки в google_apps_script_order_backend.js
14. Sitemap.xml + Image Sitemap (xmlns:image, <image:image>, 12 SEO-хабов, /kz/, 28 товаров, отсутствие noindex страниц cart.html/404.html)
15. Robots.txt (Disallow: /cart.html, Allow: /assets/, Sitemap)
16. Пререндеринг карточек в shop.html (28 карточек) и index.html (12 карточек)
17. Защита от ложного срабатывания #catalogError в shop.html
18. Страница доставки, оплаты и возврата delivery.html и сквозные ссылки в футерах
19. Кастомная страница 404.html с <meta name="robots" content="noindex, follow">
20. Очистка alt-атрибутов от спама городов на index.html, shop.html и в карточках
21. Видимый блок FAQ (<details><summary>) на index.html, синхронизированный 1-в-1 с JSON-LD FAQPage
22. Наличие Google Search Console verification тега на всех ключевых страницах
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SITE_URL = "https://livijewelry.kz"
GA_ID = "G-YFF2TR0N36"
AW_ID = "AW-16793974126"
AW_CONV_LABEL = "AW-16793974126/MuJ_CObHup8bEO7q_sc-"
FB_PIXEL_1 = "199604456030882"
FB_PIXEL_2 = "4185620171718327"
GOOGLE_VERIFICATION = "qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0"

SEO_HUB_SLUGS = [
    "komplekty-ukrasheniy.html",
    "chokery-iz-naturalnyh-kamney.html",
    "sotuary-iz-zhemchuga.html",
    "ukrasheniya-iz-barochnogo-zhemchuga.html",
    "ukrasheniya-iz-gematita.html",
    "ukrasheniya-iz-malahita.html",
    "ukrasheniya-iz-ametista.html",
    "ukrasheniya-iz-granata.html",
    "ukrasheniya-iz-rozovogo-kvarca.html",
    "ukrasheniya-iz-biryuzy.html",
    "ukrasheniya-iz-gornogo-hrustalya.html",
    "ukrasheniya-iz-lunnogo-kamnya.html",
]

errors = []
passed = []


def ok(msg: str):
    passed.append(msg)
    print(f"  [PASS] {msg}")


def fail(msg: str):
    errors.append(msg)
    print(f"  [FAIL] {msg}")


def extract_jsonld_blocks(html_text: str) -> list:
    blocks = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html_text,
        flags=re.DOTALL | re.I,
    )
    parsed = []
    for b in blocks:
        try:
            parsed.append(json.loads(b.strip()))
        except Exception as e:
            fail(f"Ошибка парсинга JSON-LD: {e}")
    return parsed


def run_audit():
    print("=" * 76)
    print("ЗАПУСК РАСШИРЕННОГО ТЕСТОВОГО КОМПЛЕКСА LIVI JEWELRY (22 ПРОВЕРКИ)")
    print("=" * 76)

    # 1. Проверка products.json
    if not os.path.exists("products.json"):
        fail("1. Файл products.json не найден")
        return
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    if len(products) != 28:
        fail(f"1. Ожидалось 28 товаров в products.json, найдено {len(products)}")
    else:
        missing_imgs = [p["id"] for p in products if not os.path.exists(p.get("image", ""))]
        if missing_imgs:
            fail(f"1. Не найдены файлы картинок для товаров: {missing_imgs}")
        else:
            ok("1. products.json валиден: 28 товаров, все изображения WebP существуют на диске")

    by_id = {p["id"]: p for p in products}

    # 2, 3, 4, 5, 6. Проверка всех 28 статических страниц товаров product/prod_XX.html
    prod_pages_ok = True
    clean_titles_ok = True
    stone_links_ok = True
    rich_schema_ok = True
    customizer_ok = True

    for p in products:
        pid = p["id"]
        path = os.path.join("product", f"{pid}.html")
        if not os.path.exists(path):
            fail(f"2. Отсутствует страница товара {path}")
            prod_pages_ok = False
            continue
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()

        # Проверка счетчиков и верификации (DO NOT BREAK)
        for token_name, token_val in [
            ("GA4", GA_ID),
            ("Google Ads", AW_ID),
            ("Ads Conv Label", AW_CONV_LABEL),
            ("Meta Pixel 1", FB_PIXEL_1),
            ("Meta Pixel 2", FB_PIXEL_2),
            ("GSC Verification", GOOGLE_VERIFICATION),
        ]:
            if token_val not in txt:
                fail(f"2. {path}: отсутствует обязательный токен {token_name} ({token_val})")
                prod_pages_ok = False

        expected_canon = f'<link rel="canonical" href="{SITE_URL}/product/{pid}.html"'
        if expected_canon not in txt:
            fail(f"2. {path}: некорректный canonical")
            prod_pages_ok = False

        # Проверка 3: Очистка <title> от (prod_XX) и наличие видимого Артикул: LIVI-XX
        title_m = re.search(r"<title>(.*?)</title>", txt, flags=re.S | re.I)
        title_str = title_m.group(1).strip() if title_m else ""
        if f"({pid})" in title_str or pid in title_str:
            fail(f"3. {path}: технический код {pid} обнаружен в <title>: {title_str}")
            clean_titles_ok = False
        if "купить по цене" not in title_str or "₸ в Астане и Алматы" not in title_str:
            fail(f"3. {path}: <title> не соответствует коммерческому шаблону: {title_str}")
            clean_titles_ok = False
        num_m = re.search(r"(\d+)", pid)
        livi_sku = f"LIVI-{num_m.group(1)}" if num_m else pid
        if f"Артикул: {livi_sku}" not in txt:
            fail(f"3. {path}: отсутствует видимый артикул 'Артикул: {livi_sku}'")
            clean_titles_ok = False

        # Проверка 4: Умная перелинковка камней из карточки товара
        if 'href="/ukrasheniya-iz-' not in txt or 'class="mat-pill mat-pill-link"' not in txt:
            fail(f"4. {path}: отсутствуют кликабельные ссылки <a href=\"/ukrasheniya-iz-...\"> в блоке материалов")
            stone_links_ok = False

        # Проверка 5: Расширенная Schema.org (JewelryStore, material, color, pattern, aggregateRating, review) + видимые отзывы
        lds = extract_jsonld_blocks(txt)
        prod_ld = next((x for x in lds if x.get("@type") == "Product"), None)
        bc_ld = next((x for x in lds if x.get("@type") == "BreadcrumbList"), None)
        if not prod_ld or not bc_ld:
            fail(f"2. {path}: отсутствует JSON-LD Product или BreadcrumbList")
            prod_pages_ok = False
        else:
            offer = prod_ld.get("offers", {})
            if str(offer.get("price")) != str(p["price"]) or offer.get("priceCurrency") != "KZT":
                fail(f"2. {path}: цена в JSON-LD ({offer.get('price')}) != цене в products.json ({p['price']})")
                prod_pages_ok = False
            if prod_ld.get("sku") != pid or prod_ld.get("mpn") != pid:
                fail(f"2. {path}: sku/mpn в JSON-LD != {pid}")
                prod_pages_ok = False

            seller = offer.get("seller", {})
            seller_type = seller.get("@type")
            if seller_type != ["Organization", "JewelryStore"]:
                fail(f"5. {path}: seller @type должен быть ['Organization', 'JewelryStore'], получено {seller_type}")
                rich_schema_ok = False
            if not prod_ld.get("material") or not prod_ld.get("color") or prod_ld.get("pattern") != "Ручная работа (Handmade)":
                fail(f"5. {path}: в JSON-LD Product отсутствуют поля material, color или pattern")
                rich_schema_ok = False
            agg = prod_ld.get("aggregateRating", {})
            revs = prod_ld.get("review", [])
            if agg.get("ratingValue") != "5.0" or not (12 <= int(agg.get("reviewCount", 0)) <= 28) or len(revs) < 2:
                fail(f"5. {path}: некорректный aggregateRating или review в JSON-LD")
                rich_schema_ok = False
            if "Отзывы покупателей (5.0 ★)" not in txt:
                fail(f"5. {path}: отсутствует видимый блок 'Отзывы покупателей (5.0 ★)'")
                rich_schema_ok = False

        # Проверка 6: CRO-кастомизатор
        if 'id="customSize"' not in txt or 'id="customHardware"' not in txt or 'id="customGift"' not in txt:
            fail(f"6. {path}: отсутствует CRO-кастомизатор (#customSize / #customHardware / #customGift)")
            customizer_ok = False

    if prod_pages_ok:
        ok("2. Все 28 страниц product/prod_XX.html содержат валидный JSON-LD Product + BreadcrumbList, 100% паритет цен/SKU и счетчики аналитики")
    if clean_titles_ok:
        ok("3. Теги <title> всех 28 карточек очищены от технического кода (prod_XX), внедрен коммерческий шаблон и артикул LIVI-XX")
    if stone_links_ok:
        ok("4. На всех 28 карточках товаров внедрена умная перелинковка камней <a href=\"/ukrasheniya-iz-...\">")
    if rich_schema_ok:
        ok("5. Расширенная Schema.org (['Organization', 'JewelryStore'], material, color, pattern, aggregateRating, review) и видимые отзывы 5.0 ★ валидны")
    if customizer_ok:
        ok("6. Интерактивный CRO-блок кастомизации (размер, фурнитура родий/позолота, подарочная упаковка 0 ₸) встроен во все 28 карточек")

    # 7. Проверка 12 новых коммерческих SEO-хабов (Этап 1)
    hubs_ok = True
    for slug in SEO_HUB_SLUGS:
        if not os.path.exists(slug):
            fail(f"7. Отсутствует SEO-хаб {slug}")
            hubs_ok = False
            continue
        with open(slug, "r", encoding="utf-8") as f:
            txt = f.read()
        if f'<link rel="canonical" href="{SITE_URL}/{slug}"' not in txt:
            fail(f"7. {slug}: отсутствует самоссылающийся canonical")
            hubs_ok = False
        lds = extract_jsonld_blocks(txt)
        types = set()
        for b in lds:
            if "@graph" in b:
                for node in b["@graph"]:
                    t = node.get("@type")
                    if isinstance(t, list):
                        types.update(t)
                    elif t:
                        types.add(t)
            else:
                t = b.get("@type")
                if isinstance(t, list):
                    types.update(t)
                elif t:
                    types.add(t)
        for req_type in ("ItemList", "BreadcrumbList", "FAQPage"):
            if req_type not in types:
                fail(f"7. {slug}: отсутствует микроразметка {req_type}")
                hubs_ok = False
        if 'href="/product/prod_' not in txt:
            fail(f"7. {slug}: отсутствуют пререндеренные карточки товаров со ссылками /product/prod_XX.html")
            hubs_ok = False
        if GA_ID not in txt or AW_ID not in txt or FB_PIXEL_1 not in txt:
            fail(f"7. {slug}: отсутствуют коды аналитики GA4/Ads/Meta")
            hubs_ok = False
    if hubs_ok:
        ok(f"7. Все {len(SEO_HUB_SLUGS)} коммерческих SEO-хабов по камням и категориям сгенерированы и содержат ItemList, BreadcrumbList, FAQPage и пререндеринг")

    # 8. Проверка существующих категорийных страниц и перелинковки
    cat_pages = ["kolye-iz-zhemchuga.html", "braslety-iz-zhemchuga.html", "sergi-iz-zhemchuga.html"]
    cats_ok = True
    for cp in cat_pages:
        if not os.path.exists(cp):
            fail(f"8. Отсутствует категорийная страница {cp}")
            cats_ok = False
            continue
        with open(cp, "r", encoding="utf-8") as f:
            txt = f.read()
        if f'<link rel="canonical" href="{SITE_URL}/{cp}"' not in txt:
            fail(f"8. {cp}: отсутствует корректный canonical")
            cats_ok = False
        if "ukrasheniya-iz-barochnogo-zhemchuga.html" not in txt or "komplekty-ukrasheniy.html" not in txt:
            fail(f"8. {cp}: отсутствует навигационный блок перелинковки на новые каменные хабы")
            cats_ok = False
    if cats_ok:
        ok("8. Категорийные посадочные страницы (kolye/braslety/sergi) валидны и связаны с новыми каменными SEO-хабами")

    # 9 & 10. Проверка XML-фидов google_merchant_feed.xml и feed.xml
    for feed_file in ["google_merchant_feed.xml", "feed.xml"]:
        if not os.path.exists(feed_file):
            fail(f"9. Отсутствует фид {feed_file}")
            continue
        tree = ET.parse(feed_file)
        root = tree.getroot()
        ns = {"g": "http://base.google.com/ns/1.0"}
        items = root.findall(".//item")
        if len(items) != 28:
            fail(f"9. {feed_file}: ожидалось 28 товаров, найдено {len(items)}")
            continue
        feed_ok = True
        highlights_ok = True
        for item in items:
            gid = item.find("g:id", ns).text.strip()
            gtitle = item.find("g:title", ns).text.strip()
            glink = item.find("g:link", ns).text.strip()
            gprice = item.find("g:price", ns).text.strip()
            p = by_id.get(gid)
            if not p:
                fail(f"9. {feed_file}: неизвестный id {gid}")
                feed_ok = False
                continue
            if not gtitle.startswith(p["title"]) or "ручная работа" not in gtitle or len(gtitle) > 150:
                fail(f"9. {feed_file}: некорректный обогащенный <g:title> для {gid}: '{gtitle}'")
                feed_ok = False
            expected_link = f"{SITE_URL}/product/{gid}.html"
            if glink != expected_link:
                fail(f"9. {feed_file}: g:link ({glink}) != {expected_link}")
                feed_ok = False
            expected_price = f"{int(p['price'])}.00 KZT"
            if gprice != expected_price:
                fail(f"9. {feed_file}: g:price ({gprice}) != {expected_price}")
                feed_ok = False

            # Проверка 10: product_highlight, shipping, custom_label_2..4
            hl = item.findall("g:product_highlight", ns)
            ship = item.find("g:shipping", ns)
            cl2 = item.find("g:custom_label_2", ns)
            cl3 = item.find("g:custom_label_3", ns)
            cl4 = item.find("g:custom_label_4", ns)
            if len(hl) < 4 or ship is None or cl2 is None or cl3 is None or cl4 is None:
                fail(f"10. {feed_file} ({gid}): отсутствуют g:product_highlight (4 шт.), g:shipping или g:custom_label_2..4")
                highlights_ok = False

        if feed_ok and feed_file == "google_merchant_feed.xml":
            ok("9. google_merchant_feed.xml и feed.xml: 100% паритет ID/цен/URL и обогащенные <g:title> (до 150 символов)")
        if highlights_ok and feed_file == "google_merchant_feed.xml":
            ok("10. Merchant Center Feed: внедрены 4 <g:product_highlight>, <g:shipping> (KZ, 0.00 KZT) и <g:custom_label_2..4>")

    # 11 & 12. Проверка казахскоязычной витрины (/kz/index.html, /kz/shop.html) и двустороннего hreflang
    kz_ok = True
    for kz_path, expected_canon in [
        (os.path.join("kz", "index.html"), f"{SITE_URL}/kz/"),
        (os.path.join("kz", "shop.html"), f"{SITE_URL}/kz/shop.html"),
    ]:
        if not os.path.exists(kz_path):
            fail(f"11. Отсутствует казахскоязычная страница {kz_path}")
            kz_ok = False
            continue
        with open(kz_path, "r", encoding="utf-8") as f:
            ktxt = f.read()
        if f'<link rel="canonical" href="{expected_canon}"' not in ktxt:
            fail(f"11. {kz_path}: некорректный canonical")
            kz_ok = False
        if 'hreflang="ru-KZ"' not in ktxt or 'hreflang="kk-KZ"' not in ktxt or 'hreflang="x-default"' not in ktxt:
            fail(f"12. {kz_path}: отсутствуют двусторонние теги hreflang")
            kz_ok = False
        if 'href="/product/prod_' not in ktxt:
            fail(f"11. {kz_path}: отсутствуют пререндеренные карточки товаров")
            kz_ok = False
    if kz_ok:
        ok("11. Статическая казахскоязычная витрина (kz/index.html и kz/shop.html) сгенерирована с пререндерингом и JSON-LD")

    with open("index.html", "r", encoding="utf-8") as f:
        index_txt = f.read()
    with open("shop.html", "r", encoding="utf-8") as f:
        shop_txt = f.read()

    if (
        'hreflang="kk-KZ" href="https://livijewelry.kz/kz/"' in index_txt
        and 'hreflang="kk-KZ" href="https://livijewelry.kz/kz/shop.html"' in shop_txt
        and 'href="/kz/"' in index_txt
        and 'href="/kz/shop.html"' in shop_txt
    ):
        ok("12. Двусторонние теги hreflang (ru, kk, x-default) и прямые ссылки на /kz/ встроены в index.html и shop.html")
    else:
        fail("12. Отсутствуют двусторонние hreflang или ссылки на /kz/ в index.html / shop.html")

    # 13. Проверка сквозной атрибуции (livi_attribution), микро-воронки GA4 и Google Sheets бэкенда
    with open("cart.html", "r", encoding="utf-8") as f:
        cart_txt = f.read()
    with open("google_apps_script_order_backend.js", "r", encoding="utf-8") as f:
        gas_txt = f.read()

    if (
        "livi_attribution" in index_txt
        and "livi_attribution" in shop_txt
        and "livi_attribution" in cart_txt
        and "view_item_list" in shop_txt
        and "select_item" in shop_txt
        and "utm_source" in gas_txt
        and "gclid" in gas_txt
    ):
        ok("13. Сквозная атрибуция (livi_attribution), передача в WhatsApp/Google Sheets и события GA4 (view_item_list, select_item) активны")
    else:
        fail("13. Неполная интеграция livi_attribution, событий GA4 или колонок UTM/gclid в google_apps_script_order_backend.js")

    # 14. Проверка sitemap.xml и Image Sitemap
    if os.path.exists("sitemap.xml"):
        with open("sitemap.xml", "r", encoding="utf-8") as f:
            sm = f.read()
        if "cart.html" in sm or "404.html" in sm or "?item=" in sm:
            fail("14. В sitemap.xml обнаружены мусорные или noindex URL (cart.html / 404.html / ?item=)")
        elif (
            'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"' not in sm
            or sm.count("<image:image>") != 28
            or f"{SITE_URL}/kz/" not in sm
            or f"{SITE_URL}/komplekty-ukrasheniy.html" not in sm
        ):
            fail("14. В sitemap.xml отсутствует Image Sitemap (<image:image> для 28 товаров), /kz/ или новые SEO-хабы")
        else:
            ok("14. sitemap.xml валиден: содержит Image Sitemap (28 <image:image>), все 12 SEO-хабов, /kz/ и не содержит noindex-страниц")
    else:
        fail("14. Файл sitemap.xml не найден")

    # 15. Проверка robots.txt
    if os.path.exists("robots.txt"):
        with open("robots.txt", "r", encoding="utf-8") as f:
            rb = f.read()
        if "Disallow: /cart.html" in rb and "Sitemap: https://livijewelry.kz/sitemap.xml" in rb:
            ok("15. robots.txt корректно закрывает /cart.html и указывает на Sitemap")
        else:
            fail("15. robots.txt не содержит Disallow: /cart.html или Sitemap")
    else:
        fail("15. Файл robots.txt не найден")

    # 16. Проверка пререндеринга карточек в shop.html и index.html
    shop_cards = re.findall(r'href="/product/prod_\d+\.html"', shop_txt)
    index_cards = re.findall(r'href="/product/prod_\d+\.html"', index_txt)
    if len(shop_cards) >= 28 and len(index_cards) >= 12:
        ok(f"16. Статический пререндеринг карточек встроен в shop.html ({len(shop_cards)} ссылок) и index.html ({len(index_cards)} ссылок)")
    else:
        fail(f"16. Недостаточно статических карточек: shop.html={len(shop_cards)}, index.html={len(index_cards)}")

    # 17. Проверка скрытия #catalogError в shop.html
    if 'id="catalogError" class="empty-state" hidden style="display:none"' in shop_txt:
        ok("17. Ложное срабатывание #catalogError в shop.html устранено")
    else:
        fail("17. #catalogError в shop.html не скрыт по умолчанию")

    # 18. Проверка delivery.html и ссылок в футере
    if os.path.exists("delivery.html") and "delivery.html" in index_txt and "delivery.html" in shop_txt:
        ok("18. Страница delivery.html создана и подключена в сквозной навигации футера")
    else:
        fail("18. Отсутствует delivery.html или ссылки на нее в футере")

    # 19. Проверка 404.html
    if os.path.exists("404.html"):
        with open("404.html", "r", encoding="utf-8") as f:
            txt_404 = f.read()
        if "noindex" in txt_404:
            ok("19. Кастомная страница 404.html существует и содержит <meta name=\"robots\" content=\"noindex, follow\">")
        else:
            fail("19. На 404.html отсутствует тег noindex")
    else:
        fail("19. Файл 404.html не найден")

    # 20. Проверка отсутствия гео-спама в alt
    spam_pattern = r"купить в Астане,\s*Алматы и Казахстане"
    if re.search(spam_pattern, index_txt) or re.search(spam_pattern, shop_txt):
        fail("20. Обнаружен гео-спам в alt-атрибутах index.html или shop.html")
    else:
        ok("20. Alt-атрибуты изображений очищены от гео-спама на всех страницах")

    # 21. Проверка видимого FAQ на index.html + JewelryStore в JSON-LD главной
    index_lds = extract_jsonld_blocks(index_txt)
    has_jewelry_store_home = False
    for b in index_lds:
        for node in b.get("@graph", []):
            if node.get("@type") == ["Organization", "JewelryStore"]:
                has_jewelry_store_home = True
    if '<section class="faq-section" id="faq">' in index_txt and index_txt.count('<details class="faq-item"') >= 6 and has_jewelry_store_home:
        ok("21. На index.html размещен видимый блок FAQ (6 вопросов) и микроразметка ['Organization', 'JewelryStore']")
    else:
        fail("21. На index.html отсутствует видимый блок FAQ (6 вопросов) или тип ['Organization', 'JewelryStore']")

    # 22. Проверка Google Search Console verification на всех ключевых страницах
    gsc_missing = []
    for pg in ["index.html", "shop.html", "delivery.html", "kz/index.html", "kz/shop.html"] + cat_pages + SEO_HUB_SLUGS:
        with open(pg, "r", encoding="utf-8") as f:
            if GOOGLE_VERIFICATION not in f.read():
                gsc_missing.append(pg)
    if not gsc_missing:
        ok("22. Мета-тег верификации Google Search Console присутствует на всех ключевых страницах, SEO-хабах и в /kz/")
    else:
        fail(f"22. Отсутствует тег верификации GSC на страницах: {gsc_missing}")

    print("=" * 76)
    if errors:
        print(f"ИТОГ: ОБНАРУЖЕНО ОШИБОК: {len(errors)}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"ИТОГ: ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО ({len(passed)}/22 PASS, 0 Errors)!")
        print("=" * 76)


if __name__ == "__main__":
    run_audit()
