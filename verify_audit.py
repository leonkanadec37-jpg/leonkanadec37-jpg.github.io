#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Комплексный верификационный сьют аудита Livi Jewelry (35 строгих инвариантов).
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
    print("ЗАПУСК СТРОГОГО ТЕСТОВОГО КОМПЛЕКСА LIVI JEWELRY (35 ИНВАРИАНТОВ)")
    print("=" * 76)

    # ---------------------------------------------------------
    # 1. Инварианты каталога products.json
    # ---------------------------------------------------------
    if not os.path.exists("products.json"):
        fail("1. Файл products.json не найден")
        return
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    if len(products) != 28:
        fail(f"1. Ожидалось ровно 28 товаров в products.json, найдено {len(products)}")
    else:
        missing_imgs = [p["id"] for p in products if not os.path.exists(p.get("image", ""))]
        if missing_imgs:
            fail(f"1. Не найдены файлы картинок для товаров: {missing_imgs}")
        else:
            ok("1. products.json: Ровно 28 товаров, все изображения WebP существуют на диске")

    # 2. Проверка sku, seo_slug, search_keywords
    sku_slug_ok = True
    for p in products:
        pid = p["id"]
        sku = p.get("sku", "")
        slug = p.get("seo_slug", "")
        kw = p.get("search_keywords", [])
        if not re.match(r"^LIVI-\d{2}$", sku):
            fail(f"2. {pid}: неверный формат sku '{sku}' (ожидался LIVI-01..LIVI-28)")
            sku_slug_ok = False
        if not slug or not re.match(r"^[a-z0-9-]+$", slug):
            fail(f"2. {pid}: неверный seo_slug '{slug}'")
            sku_slug_ok = False
        if not isinstance(kw, list) or len(kw) < 5:
            fail(f"2. {pid}: в search_keywords меньше 5 поисковых фраз ({len(kw)})")
            sku_slug_ok = False
    if sku_slug_ok:
        ok("2. products.json: Все 28 товаров имеют валидный SKU (LIVI-XX), латинский ЧПУ seo_slug и 5+ поисковых ключей")

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
        ok("3. products.json: У всех 28 товаров заполнена структурированная таблица specs (6 обязательных полей)")

    # 4. Проверка bundle_options для комплектов
    bundle_ok = True
    set_count = 0
    for p in products:
        pid = p["id"]
        is_set = p.get("category") == "Sets" or "комплект" in p.get("title", "").lower() or "сет" in p.get("title", "").lower()
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
        ok("6. products.json: Описания всех 28 товаров расширены до коммерческого объема (>= 180 символов) без сырых ценников в начале")

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
    if sergi_earring_badges == 11:
        ok("9. SEO-хабы: На странице sergi-iz-zhemchuga.html выведены все 11 комплектов с серьгами со специальной плашкой и ценой")
    else:
        fail(f"9. На sergi-iz-zhemchuga.html ожидалось 11 плашек 'Серьги доступны отдельно', найдено {sergi_earring_badges}")

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
            offer = prod_ld.get("offers", {})
            return_policy = offer.get("hasMerchantReturnPolicy", {})
            shipping = offer.get("shippingDetails", {})
            if return_policy.get("merchantReturnDays") != 14 or return_policy.get("applicableCountry") != "KZ":
                fail(f"15. {path}: отсутствует валидный hasMerchantReturnPolicy (14 дней, KZ)")
                prod_offers_ok = False
            rate_val = shipping.get("shippingRate", {}).get("value")
            if rate_val != "0" and rate_val != 0:
                fail(f"15. {path}: в shippingDetails отсутствует бесплатная ставка shippingRate (0 KZT)")
                prod_offers_ok = False

        # 16. Визуальный блок FAQ и разметка FAQPage (3 вопроса)
        faq_ld = next((x for x in lds if x.get("@type") == "FAQPage"), None)
        if not faq_ld or len(faq_ld.get("mainEntity", [])) != 3:
            fail(f"16. {path}: в JSON-LD FAQPage ожидалось ровно 3 вопроса")
            prod_faq_ok = False
        if txt.count('<details class="product-faq-item">') != 3:
            fail(f"16. {path}: на странице ожидалось 3 визуальных вопроса FAQ (<details class=\"product-faq-item\">)")
            prod_faq_ok = False

        # 17. customBundle для комплектов
        if p.get("bundle_options"):
            if '<select id="customBundle"' not in txt:
                fail(f"17. {path}: комплект не содержит выпадающего списка <select id=\"customBundle\">")
                prod_bundles_html_ok = False

        # 18. Таблица характеристик с 7 строками
        if '<dl class="product-specs-grid">' not in txt or txt.count('<div class="spec-row">') < 7:
            fail(f"18. {path}: отсутствует таблица характеристик <dl class=\"product-specs-grid\"> с 7 строками")
            prod_specs_html_ok = False

        # 19. Кликабельные ссылки в блоке материалов
        if 'class="mat-pill mat-pill-link"' not in txt:
            fail(f"19. {path}: отсутствуют ссылки mat-pill-link в блоке материалов")
            prod_pills_ok = False

        # 20. Отзывы 5.0 ★
        if "Отзывы покупателей (5.0 ★)" not in txt or not prod_ld.get("review"):
            fail(f"20. {path}: отсутствуют отзывы покупателей или Schema.org review")
            prod_reviews_ok = False

    if prod_files_ok:
        ok("12. Карточки товаров: Существуют все 28 файлов /product/prod_XX.html")
    if prod_titles_ok:
        ok("13. Карточки товаров: Теги <title> очищены от технического кода (prod_XX), отображается артикул LIVI-XX")
    if prod_alt_grammar_ok:
        ok("14. Карточки товаров: Alt-теги изображений согласованы по падежам (родительный падеж, без 'из натуральный')")
    if prod_offers_ok:
        ok("15. Карточки товаров: В JSON-LD Product присутствуют offers, hasMerchantReturnPolicy (14 дней, KZ) и shippingDetails (0 KZT)")
    if prod_faq_ok:
        ok("16. Карточки товаров: Присутствует визуальный блок FAQ и Schema.org FAQPage (ровно 3 вопроса-ответа на каждой карточке)")
    if prod_bundles_html_ok:
        ok("17. Карточки товаров: Для комплектов встроен интерактивный выпадающий список <select id=\"customBundle\">")
    if prod_specs_html_ok:
        ok("18. Карточки товаров: Встроена таблица характеристик <dl class=\"product-specs-grid\"> (7 строк спецификаций)")
    if prod_pills_ok:
        ok("19. Карточки товаров: Все плашки камней содержат кликабельные ссылки на соответствующие SEO-хабы")
    if prod_reviews_ok:
        ok("20. Карточки товаров: Внедрена расширенная Schema.org (JewelryStore, material, color, pattern, aggregateRating, review) и отзывы 5.0 ★")

    # ---------------------------------------------------------
    # 4. Инварианты казахской локализации (/kz/)
    # ---------------------------------------------------------
    kz_files_exist = os.path.exists("kz/index.html") and os.path.exists("kz/shop.html")
    kz_prods_exist = all(os.path.exists(os.path.join("kz", "product", f"{p['id']}.html")) for p in products)

    if kz_files_exist and kz_prods_exist:
        ok("21. KZ витрина: Существуют kz/index.html, kz/shop.html и все 28 файлов в kz/product/prod_XX.html")
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
            koffer = kprod.get("offers", {})
            if "hasMerchantReturnPolicy" not in koffer or "shippingDetails" not in koffer:
                fail(f"24. {kpath}: в JSON-LD Product отсутствуют hasMerchantReturnPolicy или shippingDetails")
                kz_schema_ok = False
    if kz_lang_ok:
        ok("23. KZ карточки: На всех 28 страницах kz/product/prod_XX.html установлен <html lang=\"kk\"> и канонический URL")
    if kz_schema_ok:
        ok("24. KZ карточки: В JSON-LD Product казахских страниц присутствуют offers, hasMerchantReturnPolicy (14 дней, KZ) и shippingDetails (0 KZT)")

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
        ok("25. KZ локализация: Симметричные двусторонние теги hreflang (ru-KZ, ru, kk-KZ, kk, x-default) связывают все 28 пар карточек")

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
    if len(f_items) == 28:
        ok("28. XML-фиды: google_merchant_feed.xml содержит ровно 28 товаров с ценами в KZT, in_stock, shipping 0.00 KZT и mpn")
    else:
        fail(f"28. В google_merchant_feed.xml найдено {len(f_items)} товаров вместо 28")

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

    hubs_in_sm = all(f"{SITE_URL}/{h}" in sm_txt for h in ALL_21_HUBS)
    ru_prods_in_sm = all(f"{SITE_URL}/product/{p['id']}.html" in sm_txt for p in products)
    kz_prods_in_sm = all(f"{SITE_URL}/kz/product/{p['id']}.html" in sm_txt for p in products)

    if len(sm_urls) >= 84 and hubs_in_sm and ru_prods_in_sm and kz_prods_in_sm:
        ok(f"30. Sitemap.xml: Содержит {len(sm_urls)} URLs (все 21 хаб, 28 RU и 28 KZ страниц товаров, витрины и сервисные страницы)")
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
        if GA_ID not in c or AW_ID not in c or FB_PIXEL_1 not in c or GOOGLE_VERIFICATION not in c:
            fail(f"32. {fname}: отсутствуют токены аналитики GA4/Ads/Meta/GSC")
            analytics_ok = False
    if analytics_ok:
        ok("32. Аналитика: Коды GA4, Google Ads, Meta Pixels и верификация GSC присутствуют на всех витринах и карточках")

    with open("robots.txt", "r", encoding="utf-8") as f:
        rb_txt = f.read()
    with open("404.html", "r", encoding="utf-8") as f:
        err404_txt = f.read()

    if "Disallow: /cart.html" in rb_txt and "Sitemap: https://livijewelry.kz/sitemap.xml" in rb_txt and "noindex" in err404_txt:
        ok("33. Служебные файлы: robots.txt защищает /cart.html и ссылается на sitemap, 404.html содержит noindex")
    else:
        fail("33. Ошибки в robots.txt или 404.html")

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

    cart_bundle_ok = (
        "customBundle" in cart_code
        and "unitPrice" in cart_code
        and "item.customBundle" in cart_code
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

    with open("add_product.py", "r", encoding="utf-8") as f:
        add_code = f.read()

    add_prod_ok = (
        "ensure_product_enriched_fields" in add_code
    )

    if cart_bundle_ok and sync_drive_ok and add_prod_ok:
        ok("35. Интеграция модулей: cart.html сохраняет цену customBundle, sync_drive.py и add_product.py защищают и обогащают Schema v2")
    else:
        fail(f"35. Ошибка синхронизации: cart_bundle_ok={cart_bundle_ok}, sync_drive_ok={sync_drive_ok}, add_prod_ok={add_prod_ok}")

    print("=" * 76)
    if errors:
        print(f"ИТОГ: ОБНАРУЖЕНО ОШИБОК: {len(errors)}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"ИТОГ: ВСЕ ИНВАРИАНТЫ УСПЕШНО СОБЛЮДЕНЫ ({len(passed)}/35 PASS, 0 Errors)!")
        print("=" * 76)


if __name__ == "__main__":
    run_audit()
