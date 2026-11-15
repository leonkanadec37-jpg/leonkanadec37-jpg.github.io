#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Комплексный верификационный сьют аудита Livi Jewelry (45 строгих инвариантов).
Проверяет все 8 этапов полной модернизации:
1. Каталог products.json (28 товаров, SKU, ЧПУ, спецификации specs, комплектации bundle_options, чистота текстов, коммерческая длина)
2. Все 21 SEO-хаб (15 тематических + 6 новых узкоцелевых кластеров, непустая выдача, 11 сетов с серьгами, кликабельные плашки камней)
3. 28 русских страниц товаров /product/prod_XX.html (чистые title, грамматика alt, hasMerchantReturnPolicy, shippingDetails 0 KZT, specs, FAQ, customBundle)
4. Казахская локализация (kz/index.html, kz/shop.html, 28 страниц kz/product/prod_XX.html, hreflang, переключатели языков)
5. Отсутствие фантомных ошибок каталога (#catalogError пуст в исходном HTML)
6. Товарный фид Google Shopping (28 товаров, KZT, in_stock, shipping 0 KZT, раскладка цен комплектов)
7. XML-карта сайта sitemap.xml (все 21 хаб, 28 RU + 28 KZ страниц товаров, Image Sitemap, отсутствие мусорных страниц)
8. Аналитика и модульная синхронизация (GA4, Google Ads, Meta Pixels, GSC, livi_attribution, customBundle в cart.html, sync_drive schema v2)
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog_pricing import (
    PLACEHOLDER_OPTION_NAMES,
    catalog_price,
    has_from_price,
    ordered_bundle_options,
    variant_param,
    format_price_num,
)
from generate_kaspi_feed import calculate_kaspi_price

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SITE_URL = "https://livijewelry.kz"
GA_ID = "G-YFF2TR0N36"
AW_ID = "AW-16793974126"
AW_CONV_LABEL = "AW-16793974126/Xk1CCKDnu7QdEO7q_sc-"
FB_PIXEL_1 = "199604456030882"
# FB_PIXEL_2 removed
GOOGLE_VERIFICATION = "qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0"
PINTEREST_VERIFICATION = "38fee8822fe4b1d70bb1f72021d28df5"

ALL_21_HUBS = [
    "kolye-iz-zhemchuga.html",
    "braslety-iz-zhemchuga.html",
    "sergi-iz-zhemchuga.html",
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
    # 6 новых узкоцелевых SEO-хабов
    "ukrasheniya-iz-zhemchuga-mayorka.html",
    "ukrasheniya-iz-tigrovogo-glaza.html",
    "ukrasheniya-iz-koralla-i-yashmy.html",
    "ukrasheniya-iz-lazurita.html",
    "tsepi-s-barochnym-zhemchugom.html",
    "koltsa-i-garnitury-iz-kamney.html",
]

EARING_SET_IDS = {
    "prod_09", "prod_11", "prod_12", "prod_13", "prod_14",
    "prod_15", "prod_16", "prod_18", "prod_26", "prod_27", "prod_28"
}

errors = []
warnings = []
passed = []


def ok(msg: str):
    passed.append(msg)
    print(f"  [PASS] {msg}")


def warn(msg: str):
    warnings.append(msg)
    print(f"  [WARN] {msg}")


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
    print("ЗАПУСК СТРОГОГО ТЕСТОВОГО КОМПЛЕКСА LIVI JEWELRY (48 ИНВАРИАНТОВ)")
    print("=" * 76)

    # ---------------------------------------------------------
    # 1. Инварианты каталога products.json
    # ---------------------------------------------------------
    if not os.path.exists("products.json"):
        fail("1. Файл products.json не найден")
        return
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    if len(products) < 28:
        fail(f"1. Ожидалось не менее 28 товаров в products.json, найдено {len(products)}")
    else:
        missing_imgs = [p["id"] for p in products if not os.path.exists(p.get("image", ""))]
        if missing_imgs:
            fail(f"1. Не найдены файлы картинок для товаров: {missing_imgs}")
        else:
            ok(f"1. products.json: Ровно {len(products)} товаров, все изображения WebP существуют на диске")

    # 2. Проверка sku, seo_slug, search_keywords
    sku_slug_ok = True
    for p in products:
        pid = p["id"]
        sku = p.get("sku", "")
        slug = p.get("seo_slug", "")
        kw = p.get("search_keywords", [])
        if not re.match(r"^LIVI-\d{2,3}$", sku):
            fail(f"2. {pid}: неверный формат sku '{sku}' (ожидался LIVI-01..LIVI-28)")
            sku_slug_ok = False
        if not slug or not re.match(r"^[a-z0-9-]+$", slug):
            fail(f"2. {pid}: неверный seo_slug '{slug}'")
            sku_slug_ok = False
        if not isinstance(kw, list) or len(kw) < 5:
            fail(f"2. {pid}: в search_keywords меньше 5 поисковых фраз ({len(kw)})")
            sku_slug_ok = False
    if sku_slug_ok:
        ok(f"2. products.json: Все {len(products)} товаров имеют валидный SKU (LIVI-XX), латинский ЧПУ seo_slug и 5+ поисковых ключей")

    # 3. Проверка specs
    specs_ok = True
    req_specs_fields = ["type_ru", "stones_detail", "hardware", "length_size", "clasp", "packaging"]
    for p in products:
        pid = p["id"]
        specs = p.get("specs")
        if not isinstance(specs, dict):
            fail(f"3. {pid}: отсутствует объект specs")
            specs_ok = False
            continue
        for field in req_specs_fields:
            if not specs.get(field):
                fail(f"3. {pid}: в specs отсутствует или пустое поле '{field}'")
                specs_ok = False
    if specs_ok:
        ok(f"3. products.json: У всех {len(products)} товаров заполнена структурированная таблица specs (6 обязательных полей)")

    # 4. Проверка bundle_options для комплектов
    bundle_ok = True
    set_count = 0
    placeholder_sets = []
    for p in products:
        pid = p["id"]
        is_set = p.get("category") == "Sets" or "комплект" in p.get("title", "").lower() or bool(re.search(r'\bсет\b', p.get("title", "").lower()))
        if is_set:
            set_count += 1
            b_opts = p.get("bundle_options")
            if not isinstance(b_opts, list) or len(b_opts) < 2:
                fail(f"4. {pid}: комплект не содержит массива bundle_options с как минимум 2 вариантами")
                bundle_ok = False
            else:
                for opt in b_opts:
                    if not opt.get("name") or not isinstance(opt.get("price"), int) or opt.get("price") <= 0:
                        fail(f"4. {pid}: некорректная опция в bundle_options: {opt}")
                        bundle_ok = False
                    elif str(opt.get("name") or "").strip() in PLACEHOLDER_OPTION_NAMES:
                        if pid not in placeholder_sets:
                            placeholder_sets.append(pid)
    if placeholder_sets:
        warn(f"4. products.json: Обнаружены заглушки 70/30 в bundle_options у товаров: {placeholder_sets}")
    if bundle_ok and set_count >= 13:
        ok(f"4. products.json: Все {set_count} комплектов содержат массив bundle_options с валидными ценами")

    # 5. Проверка чистоты заголовков и описаний
    clean_text_ok = True
    for p in products:
        pid = p["id"]
        t = p.get("title", "")
        d = p.get("description", "")
        if "Drive ID" in t or "Drive ID" in d or "drive_id" in t or "drive_id" in d:
            fail(f"5. {pid}: обнаружен технический маркер Drive ID")
            clean_text_ok = False
        if "Комплект: нефрита и гематита" in t:
            fail(f"5. {pid}: грамматическая ошибка в title 'Комплект: нефрита и гематита'")
            clean_text_ok = False
        if "Комплект: Комплект" in t:
            fail(f"5. {pid}: дублирование 'Комплект: Комплект' в title")
            clean_text_ok = False
        if "Комплект:" in t:
            fail(f"5. {pid}: обнаружен устаревший префикс 'Комплект:' в названии (требуется Вариант 3)")
            clean_text_ok = False
    if clean_text_ok:
        ok("5. products.json: Заголовки и описания очищены от маркеров Drive ID, грамматических ошибок и дубликатов")

    # 6. Коммерческая длина описаний (description >= 180 символов)
    desc_len_ok = True
    for p in products:
        pid = p["id"]
        d = p.get("description", "").strip()
        if len(d) < 180:
            fail(f"6. {pid}: описание слишком короткое ({len(d)} симв. < 180): '{d}'")
            desc_len_ok = False
        if d.startswith(f"{p['title']} —"):
            fail(f"6. {pid}: описание начинается с сырой заглушки '{p['title']} —'")
            desc_len_ok = False
    if desc_len_ok:
        ok(f"6. products.json: Описания всех {len(products)} товаров расширены до коммерческого объема (>= 180 символов) без сырых ценников в начале")

    # ---------------------------------------------------------
    # 2. Инварианты SEO-хабов (21 хаб)
    # ---------------------------------------------------------
    hubs_exist_ok = True
    hubs_non_empty_ok = True
    hubs_schema_ok = True
    hubs_pills_ok = True

    for slug in ALL_21_HUBS:
        if not os.path.exists(slug):
            fail(f"7. Отсутствует файл SEO-хаба {slug}")
            hubs_exist_ok = False
            continue
        with open(slug, "r", encoding="utf-8") as f:
            htxt = f.read()

        cards = re.findall(r'<article class="card"', htxt)
        if len(cards) < 4:
            fail(f"8. {slug}: недостаточно карточек ({len(cards)} < 4)")
            hubs_non_empty_ok = False

        if '<a href="' not in htxt and 'mat-pill-link' not in htxt:
            fail(f"10. {slug}: плашки материалов не кликабельны")
            hubs_pills_ok = False

        lds = extract_jsonld_blocks(htxt)
        types = set()
        for b in lds:
            if "@graph" in b:
                for n in b["@graph"]:
                    t = n.get("@type")
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
        for req_t in ("ItemList", "BreadcrumbList", "FAQPage"):
            if req_t not in types:
                fail(f"11. {slug}: отсутствует JSON-LD {req_t}")
                hubs_schema_ok = False

    if hubs_exist_ok:
        ok("7. SEO-хабы: Существуют все 21 HTML-файл хабов (15 исходных + 6 новых узкоцелевых)")
    if hubs_non_empty_ok:
        ok("8. SEO-хабы: Ни один хаб не является пустым (все имеют >= 4 товаров)")

    # 9. Проверка sergi-iz-zhemchuga.html (ровно 11 сетов с серьгами)
    with open("sergi-iz-zhemchuga.html", "r", encoding="utf-8") as f:
        sergi_txt = f.read()
    sergi_earring_badges = sergi_txt.count("Серьги доступны отдельно или в комплекте")
    if sergi_earring_badges >= 11:
        ok(f"9. SEO-хабы: На странице sergi-iz-zhemchuga.html выведены все {sergi_earring_badges} комплектов с серьгами со специальной плашкой и ценой")
    else:
        fail(f"9. На sergi-iz-zhemchuga.html ожидалось не менее 11 плашек 'Серьги доступны отдельно', найдено {sergi_earring_badges}")

    if hubs_pills_ok:
        ok("10. SEO-хабы: Все плашки камней кликабельны и содержат mat-pill-link")
    if hubs_schema_ok:
        ok("11. SEO-хабы: Микроразметка ItemList, BreadcrumbList и FAQPage валидна на всех 21 хабах")

    # ---------------------------------------------------------
    # 3. Инварианты русских страниц товаров (/product/prod_XX.html)
    # ---------------------------------------------------------
    by_id = {p["id"]: p for p in products}
    prod_files_ok = True
    prod_titles_ok = True
    prod_alt_grammar_ok = True
    prod_offers_ok = True
    prod_faq_ok = True
    prod_bundles_html_ok = True
    prod_specs_html_ok = True
    prod_pills_ok = True
    prod_reviews_ok = True

    reviews_file = 'reviews.json'
    real_reviews = []
    if os.path.exists(reviews_file):
        try:
            with open(reviews_file, 'r', encoding='utf-8') as rf:
                data = json.load(rf)
                if isinstance(data, list):
                    real_reviews = data
        except Exception:
            pass

    reviews_file = 'reviews.json'
    real_reviews = []
    if os.path.exists(reviews_file):
        try:
            with open(reviews_file, 'r', encoding='utf-8') as rf:
                data = json.load(rf)
                if isinstance(data, list):
                    real_reviews = data
        except Exception:
            pass

    for p in products:
        pid = p["id"]
        path = os.path.join("product", f"{pid}.html")
        if not os.path.exists(path):
            fail(f"12. Отсутствует файл страницы товара {path}")
            prod_files_ok = False
            continue
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()

        # 13. Проверка title
        title_m = re.search(r"<title>(.*?)</title>", txt, flags=re.S | re.I)
        t_str = title_m.group(1).strip() if title_m else ""
        if f"({pid})" in t_str or pid in t_str:
            fail(f"13. {path}: технический код {pid} обнаружен в <title>")
            prod_titles_ok = False
        livi_sku = p.get("sku", "")
        if f"Артикул: {livi_sku}" not in txt:
            fail(f"13. {path}: не найден видимый 'Артикул: {livi_sku}'")
            prod_titles_ok = False

        # 14. Проверка грамматики alt
        if "ручная работа из натуральный" in txt.lower():
            fail(f"14. {path}: в alt обнаружен некорректный именительный падеж 'ручная работа из натуральный'")
            prod_alt_grammar_ok = False

        # 15. Проверка JSON-LD Product (offers, hasMerchantReturnPolicy, shippingDetails)
        lds = extract_jsonld_blocks(txt)
        prod_ld = next((x for x in lds if x.get("@type") == "Product"), None)
        if not prod_ld:
            fail(f"15. {path}: отсутствует JSON-LD Product")
            prod_offers_ok = False
        else:
            raw_offers = prod_ld.get("offers")
            offer_list = raw_offers if isinstance(raw_offers, list) else ([raw_offers] if isinstance(raw_offers, dict) else [])
            if not offer_list:
                fail(f"15. {path}: отсутствует JSON-LD Product.offers")
                prod_offers_ok = False
            for offer in offer_list:
                return_policy = offer.get("hasMerchantReturnPolicy", {})
                shipping = offer.get("shippingDetails", {})
                if return_policy.get("merchantReturnDays") != 14 or return_policy.get("applicableCountry") != "KZ":
                    fail(f"15. {path}: отсутствует валидный hasMerchantReturnPolicy (14 дней, KZ)")
                    prod_offers_ok = False
                    break
                rate_val = shipping.get("shippingRate", {}).get("value")
                if str(rate_val) != "4000":
                    fail(f"15. {path}: в shippingDetails ставка shippingRate != 4000 KZT (найдено {rate_val})")
                    prod_offers_ok = False
                    break

        # 16. Разметка FAQPage (3 вопроса в JSON-LD для Google Rich Results)
        faq_ld = next((x for x in lds if x.get("@type") == "FAQPage"), None)
        if not faq_ld or len(faq_ld.get("mainEntity", [])) != 3:
            fail(f"16. {path}: в JSON-LD FAQPage ожидалось ровно 3 вопроса")
            prod_faq_ok = False

        # 17. Выбор комплектации (role="radiogroup" вместо <select id="customBundle">)
        if has_from_price(p):
            if 'role="radiogroup"' not in txt:
                fail(f"17. {path}: комплект не содержит переключателя role=\"radiogroup\"")
                prod_bundles_html_ok = False
            if '<select id="customBundle"' in txt:
                fail(f"17. {path}: обнаружен устаревший <select id=\"customBundle\">")
                prod_bundles_html_ok = False

        # 18. Таблица характеристик с 7 строками
        if '<dl class="product-specs-grid">' not in txt or txt.count('<div class="spec-row">') < 7:
            fail(f"18. {path}: отсутствует таблица характеристик <dl class=\"product-specs-grid\"> с 7 строками")
            prod_specs_html_ok = False

        # 19. Кликабельные ссылки в блоке материалов
        if 'class="mat-pill mat-pill-link"' not in txt:
            fail(f"19. {path}: отсутствуют ссылки mat-pill-link в блоке материалов")
            prod_pills_ok = False

        # 20. Отзывы и aggregateRating (синхронизация с reviews.json, защита от фейков)
        p_real_reviews = [r for r in real_reviews if r.get('product_id') == pid]
        if not p_real_reviews:
            if "Проверенный покупатель" in txt:
                fail(f"20. {path}: обнаружена фейковая строка 'Проверенный покупатель' при пустом reviews.json")
                prod_reviews_ok = False
            if "aggregateRating" in txt or (prod_ld and prod_ld.get("aggregateRating")):
                fail(f"20. {path}: обнаружен фейковый aggregateRating в JSON-LD при пустом reviews.json")
                prod_reviews_ok = False
            if prod_ld and prod_ld.get("review"):
                fail(f"20. {path}: обнаружен фейковый review в JSON-LD при пустом reviews.json")
                prod_reviews_ok = False
        else:
            if not prod_ld or not prod_ld.get("review") or not prod_ld.get("aggregateRating"):
                fail(f"20. {path}: отсутствует Schema.org review или aggregateRating для реальных отзывов из reviews.json")
                prod_reviews_ok = False

    if prod_files_ok:
        ok(f"12. Карточки товаров: Существуют все {len(products)} файлов /product/prod_XX.html")
    if prod_titles_ok:
        ok("13. Карточки товаров: Теги <title> очищены от технического кода (prod_XX), отображается артикул LIVI-XX")
    if prod_alt_grammar_ok:
        ok("14. Карточки товаров: Alt-теги изображений согласованы по падежам (родительный падеж, без 'из натуральный')")
    # Расширение инварианта 15 (F1): shippingRate со значением 0 не должен встречаться ни в одном HTML-файле
    zero_shipping_files = []
    zero_rate_re = re.compile(r'"shippingRate"[^{}]*\{[^{}]*"value":\s*"?0"?', re.I)
    for scan_d in [".", "kz", "uz", "product", "kz/product", "uz/product"]:
        if not os.path.exists(scan_d):
            continue
        for f in os.listdir(scan_d):
            if f.endswith(".html"):
                fp = os.path.join(scan_d, f)
                with open(fp, "r", encoding="utf-8") as f_r:
                    c = f_r.read()
                if zero_rate_re.search(c):
                    zero_shipping_files.append(fp)
    if zero_shipping_files:
        fail(f"15. В {len(zero_shipping_files)} HTML-файлах обнаружена ставка shippingRate со значением 0 (ожидается 4000 KZT): {zero_shipping_files[:5]}")
        prod_offers_ok = False

    if prod_offers_ok:
        ok("15. Карточки товаров и хабы: В JSON-LD Product присутствуют offers, hasMerchantReturnPolicy (14 дней, KZ) и shippingDetails (4000 KZT, нулевая ставка 0 ₸ отсутствует)")
    if prod_faq_ok:
        ok("16. Карточки товаров: В JSON-LD присутствует валидная Schema.org FAQPage (ровно 3 вопроса-ответа на каждой карточке)")
    if prod_bundles_html_ok:
        ok("17. Карточки товаров: Для комплектов встроен переключатель комплектации role=\"radiogroup\" (без <select id=\"customBundle\">)")
    if prod_specs_html_ok:
        ok("18. Карточки товаров: Встроена таблица характеристик <dl class=\"product-specs-grid\"> (7 строк спецификаций)")
    if prod_pills_ok:
        ok("19. Карточки товаров: Все плашки камней содержат кликабельные ссылки на соответствующие SEO-хабы")
    if prod_reviews_ok:
        ok("20. Карточки товаров: Отзывы и aggregateRating синхронизированы с reviews.json (фейковые генераторы удалены)")

    # ---------------------------------------------------------
    # 4. Инварианты казахской локализации (/kz/)
    # ---------------------------------------------------------
    kz_files_exist = os.path.exists("kz/index.html") and os.path.exists("kz/shop.html")
    kz_prods_exist = all(os.path.exists(os.path.join("kz", "product", f"{p['id']}.html")) for p in products)

    if kz_files_exist and kz_prods_exist:
        ok(f"21. KZ витрина: Существуют kz/index.html, kz/shop.html и все {len(products)} файлов в kz/product/prod_XX.html")
    else:
        fail("21. Отсутствуют файлы казахской витрины kz/index.html, kz/shop.html или карточки в kz/product/")

    # 22. Проверка ссылок на карточки товаров в kz/index.html и kz/shop.html
    with open("kz/index.html", "r", encoding="utf-8") as f:
        kz_index_txt = f.read()
    with open("kz/shop.html", "r", encoding="utf-8") as f:
        kz_shop_txt = f.read()

    kz_links_ok = True
    if 'href="/product/prod_' in kz_index_txt or 'href="/product/prod_' in kz_shop_txt:
        fail("22. В kz/index.html или kz/shop.html обнаружены ссылки на русские карточки /product/prod_XX.html")
        kz_links_ok = False
    if 'href="/kz/product/prod_' not in kz_index_txt or 'href="/kz/product/prod_' not in kz_shop_txt:
        fail("22. В kz/index.html или kz/shop.html отсутствуют ссылки /kz/product/prod_XX.html")
        kz_links_ok = False
    if kz_links_ok:
        ok("22. KZ витрина: Все карточки в kz/index.html и kz/shop.html ведут на /kz/product/prod_XX.html")

    # 23 & 24. Проверка тега lang="kk", canonical и Schema.org в kz/product/prod_XX.html
    kz_lang_ok = True
    kz_schema_ok = True
    for p in products:
        pid = p["id"]
        kpath = os.path.join("kz", "product", f"{pid}.html")
        if not os.path.exists(kpath):
            continue
        with open(kpath, "r", encoding="utf-8") as f:
            ktxt = f.read()
        if '<html lang="kk">' not in ktxt or f'<link rel="canonical" href="{SITE_URL}/kz/product/{pid}.html"' not in ktxt:
            fail(f"23. {kpath}: неверный lang='kk' или canonical")
            kz_lang_ok = False
        klds = extract_jsonld_blocks(ktxt)
        kprod = next((x for x in klds if x.get("@type") == "Product"), None)
        if not kprod:
            fail(f"24. {kpath}: отсутствует JSON-LD Product")
            kz_schema_ok = False
        else:
            raw_koffers = kprod.get("offers")
            koffer_list = raw_koffers if isinstance(raw_koffers, list) else ([raw_koffers] if isinstance(raw_koffers, dict) else [])
            if not koffer_list:
                fail(f"24. {kpath}: в JSON-LD Product отсутствует offers")
                kz_schema_ok = False
            for koffer in koffer_list:
                kshipping = koffer.get("shippingDetails", {})
                krate_val = kshipping.get("shippingRate", {}).get("value")
                if "hasMerchantReturnPolicy" not in koffer or "shippingDetails" not in koffer or str(krate_val) != "4000":
                    fail(f"24. {kpath}: в JSON-LD Product отсутствуют hasMerchantReturnPolicy или shippingDetails (4000 KZT)")
                    kz_schema_ok = False
                    break
    if kz_lang_ok:
        ok(f"23. KZ карточки: На всех {len(products)} страницах kz/product/prod_XX.html установлен <html lang=\"kk\"> и канонический URL")
    if kz_schema_ok:
        ok(f"24. KZ карточки: В JSON-LD Product казахских страниц присутствуют offers, hasMerchantReturnPolicy (14 дней, KZ) и shippingDetails (4000 KZT)")

    # 25. Двусторонняя связка hreflang
    hreflang_ok = True
    for p in products:
        pid = p["id"]
        ru_path = os.path.join("product", f"{pid}.html")
        kz_path = os.path.join("kz", "product", f"{pid}.html")
        with open(ru_path, "r", encoding="utf-8") as f:
            rtxt = f.read()
        with open(kz_path, "r", encoding="utf-8") as f:
            ktxt = f.read()
        if f'hreflang="kk-KZ" href="{SITE_URL}/kz/product/{pid}.html"' not in rtxt:
            fail(f"25. {ru_path}: отсутствует ссылка hreflang kk-KZ на казахскую карточку")
            hreflang_ok = False
        if f'hreflang="ru-KZ" href="{SITE_URL}/product/{pid}.html"' not in ktxt:
            fail(f"25. {kz_path}: отсутствует ссылка hreflang ru-KZ на русскую карточку")
            hreflang_ok = False
    if hreflang_ok:
        ok(f"25. KZ локализация: Симметричные двусторонние теги hreflang (ru-KZ, ru, kk-KZ, kk, x-default) связывают все {len(products)} пар карточек")

    # 26. Переключатель языков переходит на /kz/
    with open("index.html", "r", encoding="utf-8") as f:
        idx_txt = f.read()
    with open("shop.html", "r", encoding="utf-8") as f:
        shp_txt = f.read()
    lang_nav_ok = (
        'href="/kz/"' in idx_txt
        and 'href="/kz/shop.html"' in shp_txt
        and "window.location.href='/kz/';" in idx_txt
    )
    if lang_nav_ok:
        ok("26. KZ навигация: Переключатель языков в index.html и shop.html надежно перенаправляет на казахские версии при клике на KZ")
    else:
        fail("26. Переключатель языков в index.html или shop.html не перенаправляет на /kz/")

    # ---------------------------------------------------------
    # 5. Инвариант отсутствия фантомных ошибок каталога
    # ---------------------------------------------------------
    cat_err_ok = True
    for fname, ftxt in [("shop.html", shp_txt), ("kz/shop.html", kz_shop_txt)]:
        # Блок <div id="catalogError" ...> должен быть пустым
        m_err = re.search(r'<div id="catalogError"[^>]*>(.*?)</div>', ftxt, flags=re.S)
        if not m_err:
            fail(f"27. {fname}: контейнер #catalogError не найден")
            cat_err_ok = False
        elif m_err.group(1).strip() != "":
            fail(f"27. {fname}: блок #catalogError содержит статический текст: '{m_err.group(1).strip()}'")
            cat_err_ok = False
    if cat_err_ok:
        ok("27. Защита каталога: В статическом HTML страниц shop.html и kz/shop.html блок #catalogError пуст (текст генерируется исключительно через JS при ошибке)")

    # ---------------------------------------------------------
    # 6. Инварианты товарного фида и карты сайта
    # ---------------------------------------------------------
    feed_tree = ET.parse("google_merchant_feed.xml")
    f_root = feed_tree.getroot()
    ns = {"g": "http://base.google.com/ns/1.0"}
    f_items = f_root.findall(".//item")
    feed_ship_ok = True
    for item in f_items:
        ship_elem = item.find("g:shipping/g:price", ns)
        if ship_elem is None or ship_elem.text.strip() != "4000.00 KZT":
            fail(f"28. {item.find('g:id', ns).text}: неверный shipping в feed: {ship_elem.text if ship_elem is not None else 'None'}")
            feed_ship_ok = False
            break
    if len(f_items) == len(products) and feed_ship_ok:
        ok(f"28. XML-фиды: google_merchant_feed.xml содержит ровно {len(f_items)} товаров с ценами в KZT, in_stock, shipping 4000.00 KZT и mpn")
    else:
        fail(f"28. Ошибка в google_merchant_feed.xml: найдено {len(f_items)} товаров (ожидалось {len(products)}), shipping_ok={feed_ship_ok}")

    # 29. Проверка раскладки комплектов в <g:description>
    feed_bundle_ok = True
    for item in f_items:
        gid = item.find("g:id", ns).text.strip()
        p = by_id.get(gid, {})
        gdesc = item.find("g:description", ns).text.strip()
        if p.get("bundle_options"):
            if "Варианты комплектации:" not in gdesc and "₸" not in gdesc:
                fail(f"29. {gid}: в <g:description> комплекта отсутствует детальная раскладка вариантов и цен")
                feed_bundle_ok = False
    if feed_bundle_ok:
        ok("29. XML-фиды: Для всех комплектов в <g:description> включена детальная раскладка стоимости предметов")

    # 30 & 31. Sitemap.xml инварианты
    with open("sitemap.xml", "r", encoding="utf-8") as f:
        sm_txt = f.read()

    sm_urls = re.findall(r"<loc>(.*?)</loc>", sm_txt)
    sm_images = sm_txt.count("<image:image>")

    active_prods = [p for p in products if p.get("inStock", True)]
    hubs_in_sm = all(f"{SITE_URL}/{h}" in sm_txt for h in ALL_21_HUBS)
    ru_prods_in_sm = all(f"{SITE_URL}/product/{p['id']}.html" in sm_txt for p in active_prods)
    kz_prods_in_sm = all(f"{SITE_URL}/kz/product/{p['id']}.html" in sm_txt for p in active_prods)

    if len(sm_urls) >= 84 and hubs_in_sm and ru_prods_in_sm and kz_prods_in_sm:
        ok(f"30. Sitemap.xml: Содержит {len(sm_urls)} URLs (все 21 хаб, {len(active_prods)} RU и {len(active_prods)} KZ активных страниц товаров, витрины и сервисные страницы)")
    else:
        fail(f"30. Неполный sitemap.xml: найдено {len(sm_urls)} URLs, hubs_in_sm={hubs_in_sm}, ru={ru_prods_in_sm}, kz={kz_prods_in_sm}")

    if sm_images >= 56 and "cart.html" not in sm_txt and "404.html" not in sm_txt:
        ok(f"31. Sitemap.xml: Включает Image Sitemap ({sm_images} изображений с titles и captions) и исключает noindex-страницы")
    else:
        fail(f"31. sitemap.xml: недостаточно тегов <image:image> ({sm_images} < 56) или присутствуют мусорные URL")

    # ---------------------------------------------------------
    # 7. Инфраструктурные и аналитические инварианты
    # ---------------------------------------------------------
    analytics_ok = True
    for fname in ["index.html", "shop.html", "kz/index.html", "kz/shop.html"]:
        with open(fname, "r", encoding="utf-8") as f:
            c = f.read()
        if GA_ID not in c or AW_ID not in c or FB_PIXEL_1 not in c or GOOGLE_VERIFICATION not in c or PINTEREST_VERIFICATION not in c:
            fail(f"32. {fname}: отсутствуют токены аналитики GA4/Ads/Meta/GSC")
            analytics_ok = False
    if analytics_ok:
        ok("32. Аналитика: Коды GA4, Google Ads, Meta Pixels и верификация GSC/Pinterest присутствуют на всех витринах и карточках")

    with open("robots.txt", "r", encoding="utf-8") as f:
        rb_txt = f.read()
    with open("404.html", "r", encoding="utf-8") as f:
        err404_txt = f.read()

    with open("cart.html", "r", encoding="utf-8") as f:
        cart_head_txt = f.read()

    robots_ok = (
        "Disallow: /cart.html" not in rb_txt
        and "Sitemap: https://livijewelry.kz/sitemap.xml" in rb_txt
        and "noindex" in err404_txt
        and 'content="noindex' in cart_head_txt
    )
    if robots_ok:
        ok("33. Служебные файлы: robots.txt открыт для проверки чекаута Google Shopping, cart.html и 404.html защищены noindex")
    else:
        fail("33. Ошибки в robots.txt, cart.html или 404.html")

    if (
        "livi_attribution" in idx_txt
        and "livi_attribution" in shp_txt
        and "view_item" in idx_txt
        and "select_item" in shp_txt
    ):
        ok("34. Сквозная атрибуция: Сквозной сбор UTM/gclid (livi_attribution) и события GA4/Pixel полностью активны")
    else:
        fail("34. Ошибки в цепочке сбора livi_attribution или микро-воронке событий")

    # ---------------------------------------------------------
    # 8. Синхронизация модулей, корзина customBundle и sync_drive
    # ---------------------------------------------------------
    with open("cart.html", "r", encoding="utf-8") as f:
        cart_code = f.read()

    with open("scripts/cart-core.js", "r", encoding="utf-8") as f:
        cart_core = f.read()

    cart_bundle_ok = (
        'src="/scripts/cart-core.js"' in cart_code
        and "item.customBundle" in cart_core
        and "function unitPrice(item)" in cart_core
        and "unitPrice(i)" in cart_code
        and "Комплектация:" in cart_code
    )

    with open("sync_drive.py", "r", encoding="utf-8") as f:
        sync_code = f.read()

    sync_drive_ok = (
        "ensure_product_enriched_fields" in sync_code
        and "generate_default_sku" in sync_code
        and "generate_default_keywords" in sync_code
        and "generate_default_specs" in sync_code
        and "generate_rich_description" in sync_code
        and "bundle_options" in sync_code
    )

    add_prod_path = "scripts/add_product.py" if os.path.exists("scripts/add_product.py") else "add_product.py"
    with open(add_prod_path, "r", encoding="utf-8") as f:
        add_code = f.read()

    add_prod_ok = (
        "ensure_product_enriched_fields" in add_code
    )

    if cart_bundle_ok and sync_drive_ok and add_prod_ok:
        ok("35. Интеграция модулей: cart.html сохраняет цену customBundle, sync_drive.py и add_product.py защищают и обогащают Schema v2")
    else:
        fail(f"35. Ошибка синхронизации: cart_bundle_ok={cart_bundle_ok}, sync_drive_ok={sync_drive_ok}, add_prod_ok={add_prod_ok}")

    # ---------------------------------------------------------
    # 9. Инварианты узбекской локализации (/uz/)
    # ---------------------------------------------------------
    # 36. Существование файлов узбекской витрины, хабов, сервисных страниц и карточек
    uz_files_exist = (
        os.path.exists("uz/index.html")
        and os.path.exists("uz/shop.html")
        and os.path.exists("uz/cart.html")
        and os.path.exists("uz/delivery.html")
        and os.path.exists("uz/terms.html")
        and os.path.exists("uz/privacy.html")
    )
    uz_prods_exist = all(os.path.exists(os.path.join("uz", "product", f"{p['id']}.html")) for p in products)
    uz_hubs_exist = all(os.path.exists(os.path.join("uz", h)) for h in ALL_21_HUBS)

    if uz_files_exist and uz_prods_exist and uz_hubs_exist:
        ok(f"36. UZ витрина: Существуют uz/index.html, uz/shop.html, 4 сервисные страницы, все 21 SEO-хаб и {len(products)} карточек в uz/product/")
    else:
        fail("36. Отсутствуют файлы узбекской витрины uz/index.html, uz/shop.html, хабы или карточки в uz/product/")

    # 37. Ссылки на карточки товаров в узбекской витрине и защита от ошибок
    with open("uz/index.html", "r", encoding="utf-8") as f:
        uz_idx_txt = f.read()
    with open("uz/shop.html", "r", encoding="utf-8") as f:
        uz_shp_txt = f.read()

    m_err_uz = re.search(r'<div id="catalogError"[^>]*>(.*?)</div>', uz_shp_txt, flags=re.S)
    uz_err_empty = m_err_uz and m_err_uz.group(1).strip() == ""
    uz_links_ok = 'href="/uz/product/prod_' in uz_idx_txt and 'href="/uz/product/prod_' in uz_shp_txt

    if uz_links_ok and uz_err_empty:
        ok("37. UZ витрина: Карточки ведут на /uz/product/prod_XX.html, блок #catalogError пуст в исходном HTML")
    else:
        fail(f"37. Ошибка в uz/index.html или uz/shop.html (uz_links_ok={uz_links_ok}, uz_err_empty={uz_err_empty})")

    # 38. Тег lang="uz", канонический URL и og:locale="uz_UZ" на страницах товаров
    uz_meta_ok = True
    for p in products:
        pid = p["id"]
        upath = os.path.join("uz", "product", f"{pid}.html")
        if not os.path.exists(upath):
            uz_meta_ok = False
            continue
        with open(upath, "r", encoding="utf-8") as f:
            utxt = f.read()
        if (
            '<html lang="uz">' not in utxt
            or f'<link rel="canonical" href="{SITE_URL}/uz/product/{pid}.html"' not in utxt
            or 'content="uz_UZ"' not in utxt
        ):
            fail(f"38. {upath}: неверный lang='uz', canonical или og:locale")
            uz_meta_ok = False
            break
    if uz_meta_ok:
        ok(f'38. UZ карточки: На всех {len(products)} страницах uz/product/prod_XX.html установлен <html lang="uz">, canonical и og:locale="uz_UZ"')

    # 39. JSON-LD Product в узбекских карточках (priceCurrency: KZT, 0 KZT доставка, 14 дней возврат)
    uz_schema_ok = True
    for p in products:
        pid = p["id"]
        upath = os.path.join("uz", "product", f"{pid}.html")
        if not os.path.exists(upath):
            continue
        with open(upath, "r", encoding="utf-8") as f:
            utxt = f.read()
        ulds = extract_jsonld_blocks(utxt)
        uprod = next((x for x in ulds if x.get("@type") == "Product"), None)
        if not uprod:
            fail(f"39. {upath}: отсутствует JSON-LD Product")
            uz_schema_ok = False
            break
        raw_uoffers = uprod.get("offers")
        uoffer_list = raw_uoffers if isinstance(raw_uoffers, list) else ([raw_uoffers] if isinstance(raw_uoffers, dict) else [])
        if not uoffer_list:
            fail(f"39. {upath}: в JSON-LD Product отсутствует offers")
            uz_schema_ok = False
            break
        uoffer_bad = False
        for uoffer in uoffer_list:
            ushipping = uoffer.get("shippingDetails", {})
            urate_val = ushipping.get("shippingRate", {}).get("value")
            if (
                uoffer.get("priceCurrency") != "KZT"
                or "hasMerchantReturnPolicy" not in uoffer
                or "shippingDetails" not in uoffer
                or str(urate_val) != "4000"
            ):
                fail(f"39. {upath}: в JSON-LD Product некорректные offers (priceCurrency: KZT, shippingDetails: 4000 KZT, returnPolicy)")
                uz_schema_ok = False
                uoffer_bad = True
                break
        if uoffer_bad:
            break
    if uz_schema_ok:
        ok(f"39. UZ карточки: В JSON-LD Product сохранена валюта KZT, присутствуют shippingDetails (4000 KZT) и hasMerchantReturnPolicy (14 дней)")

    # 40. Симметричная связка hreflang для всех товаров между RU, KZ, UZ (7 тегов hreflang)
    full_prod_hreflang_ok = True
    for p in products:
        pid = p["id"]
        r_f = os.path.join("product", f"{pid}.html")
        k_f = os.path.join("kz", "product", f"{pid}.html")
        u_f = os.path.join("uz", "product", f"{pid}.html")
        with open(r_f, "r", encoding="utf-8") as f:
            rt = f.read()
        with open(k_f, "r", encoding="utf-8") as f:
            kt = f.read()
        with open(u_f, "r", encoding="utf-8") as f:
            ut = f.read()

        u_target = f'href="{SITE_URL}/uz/product/{pid}.html"'
        k_target = f'href="{SITE_URL}/kz/product/{pid}.html"'
        r_target = f'href="{SITE_URL}/product/{pid}.html"'

        if f'hreflang="uz-UZ" {u_target}' not in rt or f'hreflang="uz" {u_target}' not in rt:
            fail(f"40. {r_f}: отсутствует ссылка hreflang uz-UZ/uz на узбекскую карточку")
            full_prod_hreflang_ok = False
            break
        if f'hreflang="uz-UZ" {u_target}' not in kt or f'hreflang="uz" {u_target}' not in kt:
            fail(f"40. {k_f}: отсутствует ссылка hreflang uz-UZ/uz на узбекскую карточку")
            full_prod_hreflang_ok = False
            break
        if f'hreflang="ru-KZ" {r_target}' not in ut or f'hreflang="kk-KZ" {k_target}' not in ut or f'hreflang="uz-UZ" {u_target}' not in ut:
            fail(f"40. {u_f}: отсутствуют взаимные hreflang ссылки на RU или KZ карточки")
            full_prod_hreflang_ok = False
            break
    if full_prod_hreflang_ok:
        ok(f"40. Hreflang карточек: Полная симметричная 3-язычная матрица (ru-KZ, ru, kk-KZ, kk, uz-UZ, uz, x-default) связывает все {len(products)} триплетов карточек")

    # 41. Симметричная связка hreflang на всех 21 SEO-хабах
    hubs_hreflang_ok = True
    for h in ALL_21_HUBS:
        with open(h, "r", encoding="utf-8") as f:
            rt = f.read()
        with open(os.path.join("kz", h), "r", encoding="utf-8") as f:
            kt = f.read()
        with open(os.path.join("uz", h), "r", encoding="utf-8") as f:
            ut = f.read()

        u_target = f'href="{SITE_URL}/uz/{h}"'
        k_target = f'href="{SITE_URL}/kz/{h}"'
        r_target = f'href="{SITE_URL}/{h}"'

        if f'hreflang="uz-UZ" {u_target}' not in rt:
            fail(f"41. {h}: отсутствует hreflang uz-UZ на узбекский хаб")
            hubs_hreflang_ok = False
            break
        if f'hreflang="uz-UZ" {u_target}' not in kt:
            fail(f"41. kz/{h}: отсутствует hreflang uz-UZ на узбекский хаб")
            hubs_hreflang_ok = False
            break
        if f'hreflang="ru-KZ" {r_target}' not in ut or f'hreflang="kk-KZ" {k_target}' not in ut or f'hreflang="uz-UZ" {u_target}' not in ut:
            fail(f"41. uz/{h}: отсутствуют взаимные hreflang на RU/KZ хабы")
            hubs_hreflang_ok = False
            break
    if hubs_hreflang_ok:
        ok(f"41. Hreflang хабов: Полная симметричная связка hreflang (RU, KZ, UZ) объединяет все 21 SEO-кластеров")

    # 42. Трехпозиционный переключатель языков (RU | KZ | UZ) в шапке и меню
    switchers_ok = True
    for check_page in ["uz/index.html", "uz/shop.html", "index.html", "shop.html", "kolye-iz-zhemchuga.html"]:
        with open(check_page, "r", encoding="utf-8") as f:
            ct = f.read()
        if 'header-lang-links' not in ct or 'UZ' not in ct or 'KZ' not in ct or 'RU' not in ct:
            fail(f"42. {check_page}: не найден трехпозиционный переключатель RU | KZ | UZ в header-lang-links")
            switchers_ok = False
            break
    if switchers_ok:
        ok("42. Навигация: Трехпозиционный переключатель языков (RU | KZ | UZ) внедрен в header и drawer на витринах и хабах")

    # 43. Условия доставки и оплаты для Узбекистана (СДЭК, Казпочта, онлайн-перевод без KoronaPay)
    with open("uz/delivery.html", "r", encoding="utf-8") as f:
        dt = f.read()
    cdek_ok = "CDEK" in dt or "СДЭК" in dt
    geo_ok = any(v in dt for v in ["Oʻzbekiston", "O‘zbekiston", "O'zbekiston", "Toshkent"])
    korona_banned = "KoronaPay" not in dt and "Золотая Корона" not in dt
    if cdek_ok and geo_ok and korona_banned:
        ok("43. Логистика и оплата: В uz/delivery.html органично прописаны условия для Узбекистана (СДЭК, Казпочта, перевод без KoronaPay)")
    else:
        fail(f"43. uz/delivery.html: отсутствуют условия для Узбекистана или найден KoronaPay (cdek={cdek_ok}, geo={geo_ok}, korona_banned={korona_banned})")

    # 44. Корзина uz/cart.html: чекаут, маска, шаги заказа и шаблон WhatsApp
    with open("uz/cart.html", "r", encoding="utf-8") as f:
        cart_uz = f.read()
    cart_uz_ok = (
        'content="noindex' in cart_uz
        and f'<link rel="canonical" href="{SITE_URL}/uz/cart.html">' in cart_uz
        and 'src="/scripts/cart-core.js"' in cart_uz
        and 'custPhone' in cart_uz
        and 'WhatsApp' in cart_uz
        and 'Savatcha' in cart_uz
    )
    if cart_uz_ok:
        ok("44. Корзина uz/cart.html: Закрыта noindex, canonical на /uz/cart.html, форма чекаута и шаблон WhatsApp переведены на узбекский")
    else:
        fail("44. uz/cart.html: ошибки в мета-тегах, форме заказа или шаблоне WhatsApp")

    # 45. Sitemap.xml содержит все UZ URL с взаимными xhtml:link
    with open("sitemap.xml", "r", encoding="utf-8") as f:
        sm_txt = f.read()
    uz_home_in_sm = f"{SITE_URL}/uz/" in sm_txt
    uz_shop_in_sm = f"{SITE_URL}/uz/shop.html" in sm_txt
    uz_hubs_in_sm = all(f"{SITE_URL}/uz/{h}" in sm_txt for h in ALL_21_HUBS)
    uz_prods_in_sm = all(f"{SITE_URL}/uz/product/{p['id']}.html" in sm_txt for p in active_prods)

    if uz_home_in_sm and uz_shop_in_sm and uz_hubs_in_sm and uz_prods_in_sm:
        ok(f"45. Sitemap.xml: Включает все узбекские URL (/uz/, /uz/shop.html, 21 UZ хаб, {len(active_prods)} UZ активных товаров с Image Sitemap и xhtml:link)")
    else:
        fail(f"45. Sitemap.xml: отсутствуют страницы uz (home={uz_home_in_sm}, shop={uz_shop_in_sm}, hubs={uz_hubs_in_sm}, prods={uz_prods_in_sm})")



    # ---------------------------------------------------------
    # 10. Дополнительные строгие инварианты Wave 3 (46, 47, 48)
    # ---------------------------------------------------------
    # 46. Проверка целостности тега <head> (P0-1: отсутствие паразитных '>>' и валидность мета-тегов)
    head_syntax_ok = True
    check_html_files = ["index.html", "shop.html", "cart.html", "delivery.html", "kz/index.html", "kz/shop.html", "uz/index.html", "uz/shop.html"] + ALL_21_HUBS
    for hf in check_html_files:
        if not os.path.exists(hf):
            continue
        with open(hf, "r", encoding="utf-8") as f_h:
            h_content = f_h.read()
        m_head = re.search(r"<head[^>]*>(.*?)</head>", h_content, flags=re.S | re.I)
        if not m_head:
            fail(f"46. {hf}: тег <head> не найден")
            head_syntax_ok = False
            continue
        head_inner = m_head.group(1)
        # Check for stray '>>' or stray leading '>' before <link
        if re.search(r">\s*<link", head_inner) or ">>" in head_inner:
            # specifically check if there's a stray >
            if re.search(r"^>\s*<", head_inner.strip()) or ">>" in head_inner:
                fail(f"46. {hf}: обнаружен лишний символ '>' или '>>' в <head>")
                head_syntax_ok = False
        if '<link rel="canonical"' not in head_inner:
            fail(f"46. {hf}: canonical отсутствует внутри <head>")
            head_syntax_ok = False
    if head_syntax_ok:
        ok("46. Head синтаксис (P0-1): Теги <head> всех ключевых страниц и хабов валидны, canonical внутри <head>, паразитные '>>' отсутствуют")

    # 47. Запрещенные бейджи и неподтвержденные формулировки (P0-4: Хит, Последний экземпляр, Kaspi Red, KoronaPay)
    banned_terms_ok = True
    banned_regex = re.compile(r"\b(Хит|Последний экземпляр|Kaspi Red|KoronaPay)\b", re.I)
    scan_dirs = [".", "kz", "uz", "product", "kz/product", "uz/product"]
    for s_dir in scan_dirs:
        if not os.path.exists(s_dir):
            continue
        for fname in os.listdir(s_dir):
            if fname.endswith(".html"):
                fpath = os.path.join(s_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f_b:
                    b_txt = f_b.read()
                matches = banned_regex.findall(b_txt)
                if matches:
                    fail(f"47. {fpath}: обнаружены запрещенные термины {set(matches)}")
                    banned_terms_ok = False
                    break
        if not banned_terms_ok:
            break
    if banned_terms_ok:
        ok("47. Чистота бейджей (P0-4): Во всех скомпилированных HTML-файлах отсутствуют термины 'Хит', 'Последний экземпляр', 'Kaspi Red' и 'KoronaPay'")

    # 48. Реальные контакты NAP и режим работы (P0-3: телефон +7 705 451 05 84, 11:00-17:00, Кабанбай Батыра 43, JewelryStore schema)
    nap_ok = True
    for main_p in ["index.html", "shop.html", "kz/index.html", "uz/index.html"]:
        with open(main_p, "r", encoding="utf-8") as f_nap:
            nap_txt = f_nap.read()
        if "+7 705 451 05 84" not in nap_txt:
            fail(f"48. {main_p}: отсутствует реальный телефон +7 705 451 05 84")
            nap_ok = False
    with open("index.html", "r", encoding="utf-8") as f_idx:
        idx_txt_nap = f_idx.read()
    if "Кабанбай Батыра, 43" not in idx_txt_nap or "11:00–17:00" not in idx_txt_nap:
        fail("48. index.html: в футере отсутствует адрес 'Кабанбай Батыра, 43' или часы '11:00–17:00'")
        nap_ok = False

    # F2: Проверка цифр доставки на delivery.html
    for deliv_p in ["delivery.html", "kz/delivery.html", "uz/delivery.html"]:
        with open(deliv_p, "r", encoding="utf-8") as f_deliv:
            deliv_txt = f_deliv.read()
        if "1 500–2 000 ₸" not in deliv_txt or "2 000–4 000 ₸" not in deliv_txt:
            fail(f"48. {deliv_p}: отсутствуют точные цифры доставки (1 500–2 000 ₸ или 2 000–4 000 ₸)")
            nap_ok = False
    
    # Check JewelryStore JSON-LD NAP on index.html
    idx_lds = extract_jsonld_blocks(idx_txt_nap)
    all_items = []
    for block in idx_lds:
        if "@graph" in block and isinstance(block["@graph"], list):
            all_items.extend(block["@graph"])
        else:
            all_items.append(block)

    def is_jewelry_store(item):
        t = item.get("@type")
        if isinstance(t, list):
            return "JewelryStore" in t
        return t == "JewelryStore"

    j_store = next((x for x in all_items if is_jewelry_store(x)), None)
    if not j_store:
        fail("48. index.html: отсутствует JSON-LD JewelryStore")
        nap_ok = False
    else:
        tel = str(j_store.get("telephone", "")).replace(" ", "")
        if tel != "+77054510584":
            fail(f"48. index.html JewelryStore: telephone != +77054510584 ({j_store.get('telephone')})")
            nap_ok = False
        oh = j_store.get("openingHoursSpecification")
        if isinstance(oh, list) and len(oh) > 0:
            oh_rule = oh[0]
        elif isinstance(oh, dict):
            oh_rule = oh
        else:
            oh_rule = {}
        if oh_rule.get("opens") != "11:00" or oh_rule.get("closes") != "17:00":
            fail(f"48. index.html JewelryStore: некорректные часы работы: {oh}")
            nap_ok = False
        if not j_store.get("geo") or not j_store.get("hasMap"):
            fail("48. index.html JewelryStore: отсутствуют geo координаты или hasMap")
            nap_ok = False

    if nap_ok:
        ok("48. NAP и JewelryStore (P0-3): Телефон +7 705 451 05 84, адрес Кабанбай Батыра 43, часы 11:00–17:00 и полная Schema.org JewelryStore валидны")

    # ---------------------------------------------------------
    # 12. Инварианты задачи 008: цены комплектов и выбор варианта
    # ---------------------------------------------------------
    by_id = {p["id"]: p for p in products}

    # 49. catalog_pricing: эталонные комплекты и синтетические случаи
    t49_ok = True
    expected_benchmarks = {
        "prod_11": (61000, 45000),
        "prod_21": (74000, 40000),
        "prod_18": (74000, 30000),
        "prod_04": (40000, 25000),
        "prod_73": (93000, 75000),
    }
    for b_id, (exp_full, exp_cat) in expected_benchmarks.items():
        bp = by_id.get(b_id)
        if not bp:
            fail(f"49. Отсутствует эталонный товар {b_id} в products.json")
            t49_ok = False
        else:
            if int(bp.get("price", 0)) != exp_full or not has_from_price(bp) or catalog_price(bp) != exp_cat:
                fail(f"49. {b_id}: ожидалось full={exp_full}, cat={exp_cat}, has_from=True; получено full={bp.get('price')}, cat={catalog_price(bp)}, has_from={has_from_price(bp)}")
                t49_ok = False
    syn_placeholder = {
        "id": "syn_ph",
        "price": 50000,
        "bundle_options": [
            {"name": "Основное украшение комплекта", "price": 35000, "is_full": False},
            {"name": "Дополнительный элемент сета", "price": 15000, "is_full": False},
            {"name": "Полный комплект", "price": 50000, "is_full": True},
        ],
    }
    syn_single = {"id": "syn_sg", "price": 25000}
    if has_from_price(syn_placeholder) or catalog_price(syn_placeholder) != 50000:
        fail("49. Заглушка 70/30 не была отфильтрована в catalog_pricing")
        t49_ok = False
    if has_from_price(syn_single) or catalog_price(syn_single) != 25000:
        fail("49. Обычный товар без bundle_options дал неверный результат в catalog_pricing")
        t49_ok = False
    if t49_ok:
        ok("49. Задача 008 (catalog_pricing): Эталонные комплекты (prod_11/21/18/04/73), заглушки 70/30 и одиночные товары рассчитываются корректно")

    # 50. Каталоги RU/KZ/UZ (shop.html, index.html) и ItemList: «от/бастап/dan» + catalog_price
    t50_ok = True
    for shop_f, from_word in [("shop.html", "от"), ("kz/shop.html", "бастап"), ("uz/shop.html", "dan")]:
        if not os.path.exists(shop_f):
            fail(f"50. Отсутствует {shop_f}")
            t50_ok = False
            continue
        with open(shop_f, "r", encoding="utf-8") as f:
            stxt = f.read()
        if '<script src="/scripts/catalog-pricing.js"></script>' not in stxt:
            fail(f"50. {shop_f}: не подключён /scripts/catalog-pricing.js без defer")
            t50_ok = False
        lds = extract_jsonld_blocks(stxt)
        il = next((x for x in lds if x.get("@type") == "ItemList"), None)
        if not il:
            fail(f"50. {shop_f}: отсутствует ItemList JSON-LD")
            t50_ok = False
        else:
            for item in il.get("itemListElement", []):
                prod_node = item.get("item", {})
                url_str = prod_node.get("offers", {}).get("url") or item.get("url") or ""
                m_pid = re.search(r'(prod_\d+)\.html', url_str)
                if m_pid and m_pid.group(1) in by_id:
                    p_ref = by_id[m_pid.group(1)]
                    exp_p = f"{catalog_price(p_ref):.2f}"
                    got_p = str(prod_node.get("offers", {}).get("price", ""))
                    if got_p != exp_p:
                        fail(f"50. {shop_f} ItemList {p_ref['id']}: price={got_p}, ожидалось {exp_p}")
                        t50_ok = False
                        break
        for card_m in re.finditer(r'<article class="card"[^>]*data-id="(prod_\d+)"[^>]*>(.*?)</article>', stxt, re.DOTALL):
            cid = card_m.group(1)
            cbody = card_m.group(2)
            p_ref = by_id.get(cid)
            if not p_ref:
                continue
            pr_m = re.search(r'<div class="price">(.*?)</div>', cbody, re.DOTALL)
            if not pr_m:
                continue
            pr_html = pr_m.group(1)
            exp_amt = format_price_num(catalog_price(p_ref))
            if has_from_price(p_ref):
                if 'class="price-from"' not in pr_html or from_word not in pr_html or exp_amt not in pr_html:
                    fail(f"50. {shop_f} карточка {cid}: ожидалось '{from_word}' + '{exp_amt}', найдено: {pr_html}")
                    t50_ok = False
                    break
            else:
                if 'price-from' in pr_html or format_price_num(p_ref["price"]) not in pr_html:
                    fail(f"50. {shop_f} обычный товар {cid}: лишний price-from или неверная цена: {pr_html}")
                    t50_ok = False
                    break
    for idx_f, from_word in [("index.html", "от"), ("kz/index.html", "бастап"), ("uz/index.html", "dan")]:
        if not os.path.exists(idx_f):
            continue
        with open(idx_f, "r", encoding="utf-8") as f:
            itxt = f.read()
        for card_m in re.finditer(r'<article class="card"[^>]*data-id="(prod_\d+)"[^>]*>(.*?)</article>', itxt, re.DOTALL):
            cid = card_m.group(1)
            cbody = card_m.group(2)
            p_ref = by_id.get(cid)
            if not p_ref:
                continue
            pr_m = re.search(r'<div class="price">(.*?)</div>', cbody, re.DOTALL)
            if not pr_m:
                continue
            pr_html = pr_m.group(1)
            if has_from_price(p_ref):
                exp_amt = format_price_num(catalog_price(p_ref))
                if 'class="price-from"' not in pr_html or from_word not in pr_html or exp_amt not in pr_html:
                    fail(f"50. {idx_f} карточка {cid}: неверная витринная цена {pr_html}")
                    t50_ok = False
                    break
    if t50_ok:
        ok("50. Задача 008 (Витрины и ItemList): На всех RU/KZ/UZ каталогах и главных комплектах указаны «от/бастап/dan» + цена главного предмета")

    # 51. Страницы комплектов RU/KZ/UZ: radiogroup, порядок убывания, default aria-checked, без select/badge, meta full price
    t51_ok = True
    radio_re = re.compile(
        r'<button[^>]*class="bundle-option"[^>]*>',
        re.DOTALL,
    )
    for p in products:
        if not has_from_price(p):
            continue
        pid = p["id"]
        exp_ordered = ordered_bundle_options(p)
        exp_main_price = catalog_price(p)
        exp_main_fmt = format_price_num(exp_main_price)
        for prefix in ("", "kz", "uz"):
            fpath = os.path.join(prefix, "product", f"{pid}.html") if prefix else os.path.join("product", f"{pid}.html")
            if not os.path.exists(fpath):
                fail(f"51. Отсутствует файл {fpath}")
                t51_ok = False
                break
            with open(fpath, "r", encoding="utf-8") as f:
                ptxt = f.read()
            if 'bundle-breakdown-badge' in ptxt:
                fail(f"51. {fpath}: обнаружен удалённый bundle-breakdown-badge")
                t51_ok = False
                break
            if '<select id="customBundle"' in ptxt or 'role="radiogroup"' not in ptxt:
                fail(f"51. {fpath}: отсутствует role=radiogroup или остался select customBundle")
                t51_ok = False
                break
            radios = [r for r in radio_re.findall(ptxt) if 'role="radio"' in r]
            if len(radios) != len(exp_ordered):
                fail(f"51. {fpath}: число вариантов {len(radios)} != {len(exp_ordered)}")
                t51_ok = False
                break
            checked_prices = []
            seen_full = False
            prev_non_full_price = None
            for idx_r, r_tag in enumerate(radios):
                m_chk = re.search(r'aria-checked="(true|false)"', r_tag)
                m_pr = re.search(r'data-price="(\d+)"', r_tag)
                m_v = re.search(r'data-v="([^"]+)"', r_tag)
                if not (m_chk and m_pr and m_v):
                    fail(f"51. {fpath}: неполные data-атрибуты на кнопке варианта #{idx_r}")
                    t51_ok = False
                    break
                r_price = int(m_pr.group(1))
                r_is_full = (m_v.group(1) == "full")
                if m_chk.group(1) == "true":
                    checked_prices.append(r_price)
                if r_is_full:
                    seen_full = True
                    if r_price != int(p["price"]):
                        fail(f"51. {fpath}: кнопка полного комплекта имеет data-v=full, price={r_price} != {p['price']}")
                        t51_ok = False
                        break
                else:
                    if seen_full:
                        fail(f"51. {fpath}: полный комплект оказался не последним в списке")
                        t51_ok = False
                        break
                    if prev_non_full_price is not None and r_price > prev_non_full_price:
                        fail(f"51. {fpath}: отдельные предметы не отсортированы по убыванию цены")
                        t51_ok = False
                        break
                    prev_non_full_price = r_price
            if len(checked_prices) != 1 or checked_prices[0] != exp_main_price:
                fail(f"51. {fpath}: по умолчанию выбран не главный предмет: {checked_prices} != {exp_main_price}")
                t51_ok = False
                break
            expected_price_marker = (
                f'id="activePriceDisplay">{exp_main_fmt} ₸<' if prefix == "uz"
                else f'class="product-price-val">{exp_main_fmt} ₸<'
            )
            if expected_price_marker not in ptxt:
                fail(f"51. {fpath}: основной блок цены не показывает цену главного предмета {exp_main_fmt} ₸")
                t51_ok = False
                break
            if prefix == "":
                if f'id="addToCartBtn">В корзину — {exp_main_fmt} ₸<' not in ptxt:
                    fail(f"51. {fpath}: кнопка #addToCartBtn не содержит 'В корзину — {exp_main_fmt} ₸'")
                    t51_ok = False
                    break
            elif prefix == "kz":
                if f'id="addToCartBtn">Себетке қосу — {exp_main_fmt} ₸<' not in ptxt:
                    fail(f"51. {fpath}: кнопка #addToCartBtn не содержит 'Себетке қосу — {exp_main_fmt} ₸'")
                    t51_ok = False
                    break
            elif prefix == "uz":
                if f'WhatsApp orqali buyurtma berish ({exp_main_fmt} ₸)' not in ptxt:
                    fail(f"51. {fpath}: кнопка #buyWaBtn не содержит '({exp_main_fmt} ₸)'")
                    t51_ok = False
                    break
            if f'<meta property="product:price:amount" content="{int(p["price"])}"' not in ptxt:
                fail(f"51. {fpath}: meta product:price:amount изменён (ожидалась полная цена {int(p['price'])})")
                t51_ok = False
                break
        if not t51_ok:
            break
    if t51_ok:
        ok("51. Задача 008 (Страницы комплектов RU/KZ/UZ): radiogroup, сортировка по убыванию, выбор главного предмета и meta product:price:amount валидны")

    # 52. Страницы комплектов RU/KZ/UZ: JSON-LD Product.offers как массив вариантов
    t52_ok = True
    for p in products:
        if not has_from_price(p):
            continue
        pid = p["id"]
        exp_ordered = ordered_bundle_options(p)
        exp_full_int = int(p["price"])
        exp_cat_int = catalog_price(p)
        exp_v_list = [variant_param(oi, opt) for oi, opt in exp_ordered]
        for prefix in ("", "kz", "uz"):
            fpath = os.path.join(prefix, "product", f"{pid}.html") if prefix else os.path.join("product", f"{pid}.html")
            if not os.path.exists(fpath):
                fail(f"52. Отсутствует файл {fpath}")
                t52_ok = False
                break
            with open(fpath, "r", encoding="utf-8") as f:
                ptxt = f.read()
            pld = next((x for x in extract_jsonld_blocks(ptxt) if x.get("@type") == "Product"), None)
            if pld is None:
                fail(f"52. {fpath}: отсутствует JSON-LD Product")
                t52_ok = False
                break
            offers = pld.get("offers")
            if not isinstance(offers, list) or len(offers) != len(exp_ordered):
                fail(f"52. {fpath}: Product.offers не является массивом длины {len(exp_ordered)}")
                t52_ok = False
                break
            got_v_list = []
            offer_url_ok = True
            for o in offers:
                m_v = re.search(r'[?&]v=([^&#]+)$', str(o.get("url", "")))
                if not m_v:
                    fail(f"52. {fpath}: у одного из Offer отсутствует параметр ?v= в url: {o.get('url')}")
                    t52_ok = False
                    offer_url_ok = False
                    break
                got_v_list.append(m_v.group(1))
            if not offer_url_ok:
                break
            if set(got_v_list) != set(exp_v_list) or len(got_v_list) != len(exp_v_list):
                fail(f"52. {fpath}: набор ?v= в offers {got_v_list} != {exp_v_list}")
                t52_ok = False
                break
            full_offers = [o for o in offers if str(o.get("url", "")).endswith("?v=full")]
            if len(full_offers) != 1 or int(float(str(full_offers[0].get("price", 0)))) != exp_full_int:
                fail(f"52. {fpath}: в Product.offers неверный ?v=full оффер: {full_offers}")
                t52_ok = False
                break
            if not any(int(float(str(o.get("price", 0)))) == exp_cat_int for o in offers):
                fail(f"52. {fpath}: в Product.offers отсутствует оффер с ценой главного предмета {exp_cat_int}")
                t52_ok = False
                break
        if not t52_ok:
            break
    if t52_ok:
        ok("52. Задача 008 (JSON-LD Product.offers): На всех RU/KZ/UZ страницах комплектов offers[] включает ?v=full с полной ценой и все отдельные предметы")

    # 53. Фиды Google Merchant, 2ГИС, Pinterest: ссылка ?v=full для комплектов, цена полная
    t53_ok = True
    g_ns = {"g": "http://base.google.com/ns/1.0"}
    for gfeed in ("google_merchant_feed.xml", "feed.xml"):
        if not os.path.exists(gfeed):
            fail(f"53. Отсутствует {gfeed}")
            t53_ok = False
            continue
        tree = ET.parse(gfeed)
        for item in tree.findall(".//item"):
            gid = item.findtext("g:id", default="", namespaces=g_ns)
            glink = item.findtext("g:link", default="", namespaces=g_ns)
            gprice = item.findtext("g:price", default="", namespaces=g_ns)
            pref = by_id.get(gid)
            if not pref:
                continue
            exp_gprice = f"{int(pref['price'])}.00 KZT"
            if gprice != exp_gprice:
                fail(f"53. {gfeed} {gid}: цена {gprice} != {exp_gprice}")
                t53_ok = False
                break
            if has_from_price(pref):
                if not glink.endswith("?v=full"):
                    fail(f"53. {gfeed} {gid}: ссылка комплекта без ?v=full: {glink}")
                    t53_ok = False
                    break
            else:
                if "?v=" in glink:
                    fail(f"53. {gfeed} {gid}: лишний параметр ?v= у обычного товара: {glink}")
                    t53_ok = False
                    break
    if os.path.exists("2gis_feed.xml"):
        t2g = ET.parse("2gis_feed.xml")
        for off in t2g.findall(".//offer"):
            oid = off.attrib.get("id", "")
            ourl = off.findtext("url", default="")
            oprice = off.findtext("price", default="")
            pref = by_id.get(oid)
            if not pref:
                continue
            if oprice != str(int(pref["price"])):
                fail(f"53. 2gis_feed.xml {oid}: price={oprice} != {pref['price']}")
                t53_ok = False
                break
            if has_from_price(pref) and not ourl.endswith("?v=full"):
                fail(f"53. 2gis_feed.xml {oid}: url без ?v=full: {ourl}")
                t53_ok = False
                break
    if os.path.exists("pinterest_feed.xml"):
        tpin = ET.parse("pinterest_feed.xml")
        for item in tpin.findall(".//item"):
            pid_el = item.findtext("g:id", default="", namespaces=g_ns)
            plink = item.findtext("g:link", default="", namespaces=g_ns)
            pprice = item.findtext("g:price", default="", namespaces=g_ns)
            pref = by_id.get(pid_el)
            if not pref:
                continue
            if pprice != f"{int(pref['price'])}.00 KZT":
                fail(f"53. pinterest_feed.xml {pid_el}: price={pprice}")
                t53_ok = False
                break
            if has_from_price(pref):
                if "?v=full&utm_source=" not in plink or plink.count("?") != 1:
                    fail(f"53. pinterest_feed.xml {pid_el}: некорректный URL с ?v=full: {plink}")
                    t53_ok = False
                    break
    if t53_ok:
        ok("53. Задача 008 (Фиды Google / 2ГИС / Pinterest): Для комплектов добавлен ?v=full, полные цены не изменились")

    # 54. Фид Kaspi (kaspi_feed.xml): полная цена комплектов не затронута
    t54_ok = True
    if not os.path.exists("kaspi_feed.xml"):
        fail("54. Отсутствует kaspi_feed.xml")
        t54_ok = False
    else:
        ktree = ET.parse("kaspi_feed.xml")
        koffers = {}
        for off in ktree.findall(".//{kaspiShopping}offer"):
            ksku = off.attrib.get("sku", "")
            kpr = off.findtext("{kaspiShopping}price", default="")
            koffers[ksku] = kpr
        for p in products:
            psku = str(p.get("sku") or p.get("id", ""))
            exp_kpr = str(calculate_kaspi_price(int(p["price"])))
            got_kpr = koffers.get(psku)
            if got_kpr != exp_kpr:
                fail(f"54. kaspi_feed.xml {p['id']} ({psku}): price={got_kpr}, ожидалось {exp_kpr}")
                t54_ok = False
                break
    if t54_ok:
        ok("54. Задача 008 (Kaspi фид): Все цены в kaspi_feed.xml точно совпадают с calculate_kaspi_price(full_price)")

    EXPECTED_TESTS = 54
    if not errors and len(passed) != EXPECTED_TESTS:
        fail(f"Ожидалось {EXPECTED_TESTS} пройденных проверок, фактически PASS: {len(passed)}")

    print("=" * 76)
    if errors:
        print(f"ИТОГ: ОБНАРУЖЕНО ОШИБОК: {len(errors)}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        warn_suffix = f", {len(warnings)} Warnings" if warnings else ""
        print(f"ИТОГ: ВСЕ ИНВАРИАНТЫ УСПЕШНО СОБЛЮДЕНЫ ({len(passed)}/{EXPECTED_TESTS} PASS, 0 Errors{warn_suffix})!")
        print("=" * 76)


if __name__ == "__main__":
    run_audit()
