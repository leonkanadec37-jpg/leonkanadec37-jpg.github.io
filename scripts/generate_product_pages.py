#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор статических SEO-страниц товаров:
  product/prod_01.html ... product/prod_28.html
а также синхронизация пререндеринга карточек в shop.html и index.html.

Обеспечивает:
- Коммерческий <title> без технического шума (prod_XX):
  {title} — купить по цене {price_formatted} ₸ в Астане и Алматы | Ручная работа Livi Jewelry
- Видимый человекопонятный артикул: Артикул: LIVI-{XX}
- Прямые кликабельные ссылки <a href="/ukrasheniya-iz-..."> в блоке материалов для ВСЕХ камней
- Расширенную микроразметку Schema.org: ["Organization", "JewelryStore"], material, color, pattern, aggregateRating, review,
  hasMerchantReturnPolicy и полный shippingDetails со shippingRate 0 KZT
- Визуальную таблицу характеристик изделия (<dl class="product-specs-grid">)
- Визуальный и Schema.org блок FAQPage (3 индивидуальных вопроса-ответа с названием изделия и камней)
- Выбор комплектации (bundle_options) с обновлением цены и заказа
- Двусторонние hreflang связки с казахскими страницами /kz/product/prod_XX.html и прямой переход в переключателе языка
- Сквозную атрибуцию UTM/gclid/fbclid (livi_attribution) и события GA4/Ads/Meta
"""

import html
import json
import os
import re

SITE_URL = "https://livijewelry.kz"
GA_ID = "G-YFF2TR0N36"
AW_ID = "AW-16793974126"
AW_CONV_LABEL = "AW-16793974126/Xk1CCKDnu7QdEO7q_sc-"
FB_PIXEL_1 = "199604456030882"
GOOGLE_VERIFICATION = "qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0"

CATEGORY_NAMES_RU = {
    "Necklaces": "Колье",
    "Lariats": "Сотуары",
    "Chains": "Цепочки и чокеры",
    "Bracelets": "Браслеты",
    "Earrings": "Серьги",
    "Rings": "Кольца",
    "Sets": "Комплекты украшений",
}

CATEGORY_HUB_LINKS = {
    "Necklaces": ("/kolye-iz-zhemchuga.html", "Колье из жемчуга"),
    "Lariats": ("/sotuary-iz-zhemchuga.html", "Сотуары и галстуки"),
    "Chains": ("/chokery-iz-naturalnyh-kamney.html", "Чокеры и цепочки"),
    "Bracelets": ("/braslety-iz-zhemchuga.html", "Браслеты из жемчуга"),
    "Earrings": ("/sergi-iz-zhemchuga.html", "Серьги из жемчуга"),
    "Rings": ("/koltsa-i-garnitury-iz-kamney.html", "Кольца и сеты"),
    "Sets": ("/komplekty-ukrasheniy.html", "Комплекты украшений"),
}

FEATURED_IDS = ["prod_01", "prod_06", "prod_11", "prod_24", "prod_04", "prod_08", "prod_17", "prod_16"]

GENITIVE_STONE_MAP = {
    "натуральный жемчуг": "натурального жемчуга",
    "барочный жемчуг": "барочного жемчуга",
    "натуральный барочный жемчуг": "натурального барочного жемчуга",
    "жемчуг майорка": "жемчуга Майорка",
    "горный хрусталь": "горного хрусталя",
    "керамические бусины": "керамических бусин",
    "натуральный малахит": "натурального малахита",
    "натуральный аметист": "натурального аметиста",
    "натуральный авантюрин": "натурального авантюрина",
    "натуральный агат": "натурального агата",
    "натуральный гранат": "натурального граната",
    "розовый кварц": "розового кварца",
    "натуральный жадеит": "натурального жадеита",
    "тигровый глаз": "тигрового глаза",
    "натуральный коралл": "натурального коралла",
    "яшма": "яшмы",
    "натуральная бирюза": "натуральной бирюзы",
    "натуральные камни": "натуральных камней",
    "гематит": "гематита",
    "натуральный флюорит": "натурального флюорита",
    "цирконы": "цирконов",
    "натуральный лазурит": "натурального лазурита",
    "натуральный нефрит": "натурального нефрита",
}

ALL_21_HUBS = [
    ("/kolye-iz-zhemchuga.html", "Колье из жемчуга"),
    ("/braslety-iz-zhemchuga.html", "Браслеты из жемчуга"),
    ("/sergi-iz-zhemchuga.html", "Серьги из жемчуга"),
    ("/komplekty-ukrasheniy.html", "Комплекты украшений"),
    ("/chokery-iz-naturalnyh-kamney.html", "Чокеры из камней"),
    ("/sotuary-iz-zhemchuga.html", "Сотуары и галстуки"),
    ("/ukrasheniya-iz-barochnogo-zhemchuga.html", "Барочный жемчуг"),
    ("/ukrasheniya-iz-gematita.html", "Гематит"),
    ("/ukrasheniya-iz-malahita.html", "Малахит и Нефрит"),
    ("/ukrasheniya-iz-ametista.html", "Аметист и Флюорит"),
    ("/ukrasheniya-iz-granata.html", "Гранат и Агат"),
    ("/ukrasheniya-iz-rozovogo-kvarca.html", "Розовый кварц"),
    ("/ukrasheniya-iz-biryuzy.html", "Бирюза"),
    ("/ukrasheniya-iz-gornogo-hrustalya.html", "Горный хрусталь"),
    ("/ukrasheniya-iz-lunnogo-kamnya.html", "Лунный камень и Перламутр"),
    ("/ukrasheniya-iz-zhemchuga-mayorka.html", "Жемчуг Майорка"),
    ("/ukrasheniya-iz-tigrovogo-glaza.html", "Тигровый глаз и Жадеит"),
    ("/ukrasheniya-iz-koralla-i-yashmy.html", "Коралл и Яшма"),
    ("/ukrasheniya-iz-lazurita.html", "Лазурит и Авантюрин"),
    ("/tsepi-s-barochnym-zhemchugom.html", "Цепи с барочным жемчугом"),
    ("/koltsa-i-garnitury-iz-kamney.html", "Кольца и сеты"),
]

def load_reviews() -> list:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rev_path = os.path.join(root_dir, "reviews.json")
    if os.path.exists(rev_path):
        try:
            with open(rev_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []


ALL_REVIEWS = load_reviews()


def get_product_reviews(pid: str) -> list:
    """Возвращает список реальных отзывов для данного товара из reviews.json."""
    return [r for r in ALL_REVIEWS if r.get("product_id") == pid]


def format_price_ru(price: int) -> str:
    return f"{int(price):,}".replace(",", " ")


def get_livi_sku(pid: str) -> str:
    m = re.search(r"(\d+)", pid)
    num = m.group(1) if m else pid
    return f"LIVI-{int(num):02d}"


def get_stone_hub_url(material_name: str) -> str:
    low = material_name.lower()
    if "майорк" in low:
        return "/ukrasheniya-iz-zhemchuga-mayorka.html"
    if "барочн" in low:
        return "/ukrasheniya-iz-barochnogo-zhemchuga.html"
    if "тигров" in low or "жадеит" in low:
        return "/ukrasheniya-iz-tigrovogo-glaza.html"
    if "коралл" in low or "яшм" in low:
        return "/ukrasheniya-iz-koralla-i-yashmy.html"
    if "лазурит" in low or "авантюрин" in low:
        return "/ukrasheniya-iz-lazurita.html"
    if "малахит" in low or "нефрит" in low:
        return "/ukrasheniya-iz-malahita.html"
    if "гематит" in low:
        return "/ukrasheniya-iz-gematita.html"
    if "аметист" in low or "флюорит" in low:
        return "/ukrasheniya-iz-ametista.html"
    if "гранат" in low or "агат" in low:
        return "/ukrasheniya-iz-granata.html"
    if "розов" in low and "кварц" in low:
        return "/ukrasheniya-iz-rozovogo-kvarca.html"
    if "бирюз" in low:
        return "/ukrasheniya-iz-biryuzy.html"
    if "хрустал" in low or "циркон" in low or ("кварц" in low and "розов" not in low):
        return "/ukrasheniya-iz-gornogo-hrustalya.html"
    if "лунн" in low or "перламутр" in low:
        return "/ukrasheniya-iz-lunnogo-kamnya.html"
    if "керамическ" in low:
        return "/ukrasheniya-iz-zhemchuga-mayorka.html"
    if "жемчуг" in low:
        return "/kolye-iz-zhemchuga.html"
    return ""


def infer_color(product: dict) -> str:
    text = f"{product.get('title', '')} {product.get('description', '')} {' '.join(product.get('materials') or [])}".lower()
    colors = []
    if "жемчуг" in text or "перламутр" in text:
        colors.append("Белый перламутровый")
    if "гематит" in text:
        colors.append("Графитовый металлик")
    if "малахит" in text or "нефрит" in text or "жадеит" in text:
        colors.append("Изумрудно-зелёный")
    if "гранат" in text or "коралл" in text:
        colors.append("Глубокий бордовый")
    if "аметист" in text or "флюорит" in text:
        colors.append("Фиолетово-лавандовый")
    if "розовый кварц" in text:
        colors.append("Нежно-розовый")
    if "бирюз" in text:
        colors.append("Бирюзово-голубой")
    if "хрустал" in text or "циркон" in text:
        colors.append("Прозрачный кристальный")
    if "позолота" in text:
        colors.append("Золотистый")
    elif "сплав" in text or "родий" in text:
        colors.append("Серебристый")
    if not colors:
        colors.append("Белый перламутровый / Серебристый")
    return ", ".join(dict.fromkeys(colors[:2]))



def build_clean_alt(product: dict) -> str:
    title = (product.get("title") or "").strip()
    materials = product.get("materials") or []
    materials_str = ", ".join(materials) if materials else "натуральный жемчуг"
    return f"{title} — авторская ручная работа ({materials_str}), Livi Jewelry"


def build_meta_description(product: dict) -> str:
    title = (product.get("title") or "").strip()
    price_str = format_price_ru(product.get("price") or 0)
    materials = ", ".join(product.get("materials") or ["натуральный жемчуг"])
    raw = f"Купить «{title}» за {price_str} ₸ в Livi Jewelry. Ручная работа, {materials}. Доставка СДЭК по Казахстану и курьером по Астане."
    if len(raw) > 160:
        raw = raw[:157].rstrip(" ,.") + "..."
    return raw


def build_customizer_html(product: dict) -> str:
    bundle_options = product.get("bundle_options") or []
    if not bundle_options:
        return ""

    options = "\n".join(
        f'              <option value="{html.escape(opt["name"])}" data-price="{opt["price"]}"{" selected" if opt.get("is_full") else ""}>{html.escape(opt["name"])} — {format_price_ru(opt["price"])} ₸</option>'
        for opt in bundle_options
    )
    return f"""        <div class="product-customizer">
          <label class="customizer-label" for="customBundle">Выберите комплектацию</label>
          <select id="customBundle" class="customizer-select">
{options}
          </select>
        </div>"""


def storefront_header(home_html: str, language_paths: dict[str, str]) -> str:
    start = home_html.index('  <header class="storefront-header">')
    end = home_html.index('</header>', start) + len('</header>')
    header = home_html[start:end]
    return re.sub(
        r'href="[^"]+"(?=[^>]*hreflang="(ru|kk|uz)")',
        lambda match: f'href="{language_paths[match[1]]}"',
        header,
    )


HARDWARE_MATERIALS = {'ювелирный сплав', 'позолота', 'родированная фурнитура', 'родий', 'серебро', 'эмаль'}

STONE_ROOTS = [
    'жемчуг', 'перламутр', 'малахит', 'агат', 'бирюз', 'гранат', 'кварц', 
    'аметист', 'хрустал', 'амазонит', 'гематит', 'коралл', 'лазурит', 
    'нефрит', 'жадеит', 'тигров', 'флюорит', 'яшм', 'циркон', 'авантюрин', 
    'стекл'
]

def get_stones_set(p):
    mats = set(m.lower().strip() for m in p.get("materials_ru", p.get("materials", []))) - HARDWARE_MATERIALS
    text = (p.get("title", "") + " " + " ".join(mats)).lower()
    found_roots = set()
    for root in STONE_ROOTS:
        if root in text:
            found_roots.add(root)
    return mats, found_roots

def find_pairs_with_products(target: dict, all_products: list, limit: int = 3) -> list:
    """Подбирает гармонирующие изделия из того же камня/минерала или серии (Complete the look).
    Правило R4:
    1. Ручные связки target.get('pairs_with') имеют наивысший приоритет.
    2. Сначала товары другой категории с тем же камнем/материалом (колье -> серьги, браслет; серьги -> колье).
    3. Исключается текущий товар и товары не в наличии.
    4. Если товаров другой категории с тем же камнем меньше 2, добираются товары той же категории.
    """
    manual = target.get("pairs_with", [])
    selected = []
    prod_map = {p["id"]: p for p in all_products}

    # 1. Manual links from target.pairs_with
    if isinstance(manual, list):
        for pid in manual:
            if pid in prod_map and prod_map[pid].get("inStock", True) and pid != target.get("id"):
                selected.append(prod_map[pid])
                if len(selected) >= limit:
                    return selected

    t_id = target.get("id")
    t_cat = target.get("category", "")
    t_mats, t_roots = get_stones_set(target)

    def calc_score(p):
        p_mats, p_roots = get_stones_set(p)
        score = 0
        common_mats = t_mats.intersection(p_mats)
        score += len(common_mats) * 50
        common_roots = t_roots.intersection(p_roots)
        score += len(common_roots) * 100
        p_title = p.get("title", "").lower()
        if t_cat in ["Necklaces", "Lariats"]:
            if "серьг" in p_title or "пусет" in p_title:
                score += 40
            if "браслет" in p_title:
                score += 35
            if "кольц" in p_title:
                score += 25
        elif t_cat in ["Earrings"]:
            if "колье" in p_title or "цеп" in p_title:
                score += 40
            if "браслет" in p_title:
                score += 35
            if "кольц" in p_title:
                score += 25
        elif t_cat in ["Bracelets"]:
            if "серьг" in p_title:
                score += 40
            if "колье" in p_title:
                score += 35
        return score

    already_ids = set(p["id"] for p in selected)
    already_ids.add(t_id)

    tier1 = []  # Different category with matching stone
    tier2 = []  # Same category with matching stone
    tier3 = []  # Different category without matching stone

    for p in all_products:
        pid = p.get("id")
        if pid in already_ids or not p.get("inStock", True):
            continue
        p_cat = p.get("category", "")
        score = calc_score(p)
        p_mats, p_roots = get_stones_set(p)
        has_stone_match = bool(t_mats.intersection(p_mats) or t_roots.intersection(p_roots))
        if has_stone_match:
            if p_cat != t_cat:
                tier1.append((score, p))
            else:
                tier2.append((score, p))
        else:
            if p_cat != t_cat:
                tier3.append((score, p))

    tier1.sort(key=lambda x: x[0], reverse=True)
    tier2.sort(key=lambda x: x[0], reverse=True)
    tier3.sort(key=lambda x: x[0], reverse=True)

    for _, p in tier1:
        selected.append(p)
        if len(selected) >= limit:
            return selected

    # If < 2 from different category, fill from same category with matching stone
    if len(selected) < 2:
        for _, p in tier2:
            if p["id"] not in set(x["id"] for x in selected):
                selected.append(p)
                if len(selected) >= limit:
                    return selected

    # If still not enough, fill from tier3 (different category)
    if len(selected) < limit:
        for _, p in tier3:
            if p["id"] not in set(x["id"] for x in selected):
                selected.append(p)
                if len(selected) >= limit:
                    break

    # Final fill from tier2
    if len(selected) < limit:
        for _, p in tier2:
            if p["id"] not in set(x["id"] for x in selected):
                selected.append(p)
                if len(selected) >= limit:
                    break

    return selected

def build_product_page_html(product: dict, all_products: list, home_html: str) -> str:
    pid = product["id"]
    livi_sku = product.get("sku") or get_livi_sku(pid)
    title = product["title"].strip()
    price = int(product.get("price") or 0)
    price_fmt = format_price_ru(price)
    category = product.get("category") or "Necklaces"
    cat_ru = CATEGORY_NAMES_RU.get(category, "Украшения")
    cat_hub_url, cat_hub_label = CATEGORY_HUB_LINKS.get(category, ("/shop.html", "Каталог"))

    img_rel = product["image"].lstrip("/")
    img_abs = f"{SITE_URL}/{img_rel}"
    base_rel, _ = os.path.splitext(img_rel)
    mob_img_rel = f"{base_rel}-750w.webp"
    thumb_img_rel = f"{base_rel}-400w.webp"
    page_url = f"{SITE_URL}/product/{pid}.html"
    instagram_url = html.escape(product.get("instagram_url") or "https://www.instagram.com/livi_jwl/")
    kz_page_url = f"{SITE_URL}/kz/product/{pid}.html"
    uz_page_url = f"{SITE_URL}/uz/product/{pid}.html"

    description = (product.get("description") or "").strip()
    materials = product.get("materials") or ["Натуральный жемчуг", "Ювелирный сплав"]
    materials_str = ", ".join(materials)
    color_str = infer_color(product)
    alt_text = build_clean_alt(product)
    meta_desc = build_meta_description(product)
    specs = product.get("specs") or {}
    bundle_options = product.get("bundle_options") or []

    # Коммерческий <title> без городов и тех. кода
    page_title = f"{title} — {price_fmt} ₸ | Livi Jewelry"

    # Умная перелинковка камней из карточки товара
    material_pills_list = []
    has_stone_hub_link = False
    for m in materials:
        hub_url = get_stone_hub_url(m)
        if hub_url:
            has_stone_hub_link = True
            material_pills_list.append(
                f'<a href="{hub_url}" class="mat-pill mat-pill-link" title="Смотреть все украшения: {html.escape(m)}">{html.escape(m)}</a>'
            )
        else:
            material_pills_list.append(f'<span class="mat-pill">{html.escape(m)}</span>')

    if not has_stone_hub_link:
        material_pills_list.insert(
            0,
            '<a href="/kolye-iz-zhemchuga.html" class="mat-pill mat-pill-link">Натуральный жемчуг</a>'
        )
    material_pills = "\n            ".join(material_pills_list)

    # Отзывы и рейтинг (только реальные отзывы из reviews.json)
    product_reviews = get_product_reviews(pid)
    reviews_accordion_html = ""
    if product_reviews:
        rev_count = len(product_reviews)
        avg_rating = sum(float(r.get("rating", 5.0)) for r in product_reviews) / rev_count
        rating_val = f"{avg_rating:.1f}"
        reviews_items_html = "\n".join([
            f"""                <div class="product-review-item">
                  <div class="review-header">
                    <strong class="review-author">{html.escape(r.get('author', 'Покупатель'))}</strong>
                    <span class="review-date">{html.escape(r.get('date', ''))}</span>
                  </div>
                  <div class="review-stars-row">{'★' * int(float(r.get('rating', 5.0)))}</div>
                  <p class="review-text">{html.escape(r.get('text', r.get('body', '')))}</p>
                </div>"""
            for r in product_reviews
        ])
        reviews_accordion_html = f"""          <details class="product-accordion">
            <summary>Отзывы покупателей (★ {rating_val} · {rev_count} отзывов)</summary>
            <div class="product-accordion-content">
              <div class="reviews-summary-line">
                <span class="reviews-stars">★★★★★</span>
                <strong>{rating_val} из 5.0</strong>
                <span class="reviews-count-badge">на основе {rev_count} оценок покупателей</span>
              </div>
              <div class="product-reviews-list">
{reviews_items_html}
              </div>
            </div>
          </details>"""

    # 3 индивидуальных FAQ вопроса-ответа
    faq_q1 = f"Натуральные ли камни используются в модели «{title}»?"
    faq_a1 = f"Да, в модели «{title}» используются исключительно натуральные камни и минералы: {materials_str}. Каждый камень проходит ручную селекцию мастера Livi Jewelry по плотности, естественной фактуре и природному блеску."

    if bundle_options:
        faq_q2 = f"Можно ли изменить длину или купить предмет из комплекта «{title}» отдельно?"
        faq_a2 = f"Да! Вы можете приобрести как полный комплект «{title}», так и любой отдельный предмет (выберите нужный вариант в выпадающем списке комплектации выше). По вопросам длины колье или браслета напишите мастеру в WhatsApp."
    else:
        faq_q2 = f"Можно ли изменить длину или размер модели «{title}»?"
        faq_a2 = f"Размер модели «{title}»: {specs.get('length_size', '38–45 см')}. По вопросам изменения длины напишите мастеру в WhatsApp — подскажем, возможно ли это для данной модели."

    faq_q3 = f"Как быстро доставляется «{title}» в Астану, Алматы и по Казахстану?"
    faq_a3 = f"По Астане доставка «{title}» осуществляется курьером день в день при заказе до 16:00. В Алматы, Шымкент, Караганду и все города Казахстана отправляем экспресс-службой СДЭК за 1–3 рабочих дня с трек-номером. Оплата возможна картой и Kaspi Pay."

    # Похожие товары (4 штуки)
    same_cat = [p for p in all_products if p["id"] != pid and p.get("category") == category]
    others = [p for p in all_products if p["id"] != pid and p.get("category") != category]
    related = (same_cat + others)[:4]

    related_cards_html = []
    for rp in related:
        r_id = rp["id"]
        r_title = html.escape(rp["title"].strip())
        r_price = format_price_ru(rp.get("price") or 0)
        r_price_num = int(rp.get("price") or 0)
        r_img = "/" + rp["image"].lstrip("/")
        r_base, _ = os.path.splitext(r_img)
        r_mob = f"{r_base}-750w.webp"
        r_thumb = f"{r_base}-400w.webp"
        r_alt = html.escape(build_clean_alt(rp))
        r_cat = html.escape(rp.get("category") or "")
        related_cards_html.append(f"""      <article class="card" data-rel-id="{r_id}" data-rel-title="{r_title}" data-rel-price="{r_price_num}" data-rel-category="{r_cat}">
        <a href="/product/{r_id}.html" class="card-img-wrap" style="display:block;">
          <img src="{r_img}" srcset="{r_thumb} 400w, {r_mob} 750w, {r_img} 1440w" sizes="(max-width: 768px) 50vw, 300px" alt="{r_alt}" loading="lazy" decoding="async" width="600" height="800">
        </a>
        <div class="body">
          <div class="title"><a href="/product/{r_id}.html" class="card-title-link">{r_title}</a></div>
          <div class="price">{r_price} ₸</div>
        </div>
      </article>""")
    related_html = "\n".join(related_cards_html)

    # JSON-LD Product (Merchant Listing)
    product_ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "@id": f"{page_url}#product",
        "name": title,
        "sku": pid,
        "mpn": pid,
        "image": [img_abs],
        "description": f"{description} Материалы: {materials_str}. Ручная работа Livi Jewelry, гипоаллергенная фурнитура, подарочная упаковка.",
        "material": materials_str,
        "color": color_str,
        "pattern": "Ручная работа (Handmade)",
        "brand": {
            "@type": "Brand",
            "name": "Livi Jewelry"
        },
        "category": cat_ru,
        "offers": {
            "@type": "Offer",
            "url": page_url,
            "priceCurrency": "KZT",
            "price": str(price),
            "priceValidUntil": "2027-12-31",
            "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition",
            "seller": {
                "@type": ["Organization", "JewelryStore"],
                "name": "Livi Jewelry",
                "url": f"{SITE_URL}/",
                "telephone": "+77054510584",
                "priceRange": "15000 KZT - 91000 KZT",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Астана",
                    "addressCountry": "KZ"
                }
            },
            "hasMerchantReturnPolicy": {
                "@type": "MerchantReturnPolicy",
                "applicableCountry": "KZ",
                "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                "merchantReturnDays": 14,
                "returnMethod": "https://schema.org/ReturnByMail",
                "returnFees": "https://schema.org/FreeReturn"
            },
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {
                    "@type": "MonetaryAmount",
                    "value": "4000",
                    "currency": "KZT"
                },
                "shippingDestination": {
                    "@type": "DefinedRegion",
                    "addressCountry": "KZ"
                },
                "deliveryTime": {
                    "@type": "ShippingDeliveryTime",
                    "handlingTime": {
                        "@type": "QuantitativeValue",
                        "minValue": 0,
                        "maxValue": 1,
                        "unitCode": "d"
                    },
                    "transitTime": {
                        "@type": "QuantitativeValue",
                        "minValue": 1,
                        "maxValue": 3,
                        "unitCode": "d"
                    }
                }
            }
        }
    }

    if product_reviews:
        product_ld["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": rating_val,
            "reviewCount": str(rev_count),
            "bestRating": "5",
            "worstRating": "1"
        }
        product_ld["review"] = [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": r.get("author", "Покупатель")},
                "datePublished": r.get("date", ""),
                "reviewBody": r.get("text", r.get("body", "")),
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": str(r.get("rating", 5)),
                    "bestRating": "5",
                    "worstRating": "1"
                }
            }
            for r in product_reviews
        ]

    # JSON-LD BreadcrumbList
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Главная",
                "item": f"{SITE_URL}/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Каталог",
                "item": f"{SITE_URL}/shop.html"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": cat_hub_label,
                "item": f"{SITE_URL}{cat_hub_url}"
            },
            {
                "@type": "ListItem",
                "position": 4,
                "name": title,
                "item": page_url
            }
        ]
    }

    # JSON-LD FAQPage
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq_q1,
                "acceptedAnswer": {"@type": "Answer", "text": faq_a1}
            },
            {
                "@type": "Question",
                "name": faq_q2,
                "acceptedAnswer": {"@type": "Answer", "text": faq_a2}
            },
            {
                "@type": "Question",
                "name": faq_q3,
                "acceptedAnswer": {"@type": "Answer", "text": faq_a3}
            }
        ]
    }

    wa_text = (
        f"Здравствуйте! Хочу уточнить наличие и заказать: {title} (Артикул: {livi_sku}) за {price_fmt} ₸ ✨\n"
        f"Ссылка: {page_url}"
    )
    wa_href = f"https://wa.me/77054510584?text={html.escape(re.sub(r' ', '%20', wa_text.replace(chr(10), '%0A')))}"

    customizer_html = build_customizer_html(product)

    interlink_chips_html = "\n".join(
        f'        <a href="{h_url}" class="stone-chip">{html.escape(h_lbl)}</a>'
        for h_url, h_lbl in ALL_21_HUBS
    )

    bundle_badge_html = ""
    if bundle_options:
        opts_summary = " • ".join(
            f"{opt['name']} — {format_price_ru(opt['price'])} ₸"
            for opt in bundle_options
            if not opt.get("is_full")
        )
        if opts_summary:
            bundle_badge_html = f'        <div class="bundle-breakdown-badge">В комплекте: {html.escape(opts_summary)} (можно приобрести отдельно)</div>\n'

    # D4. Быстрые чипсы характеристик под ценой (длина / фурнитура)
    quick_chips = []
    length_val = specs.get("length_size")
    if length_val and length_val != "Уточнить у мастера":
        quick_chips.append(f'<span class="quick-chip"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21.3 8.7 8.7 21.3a1 1 0 0 1-1.4 0l-6-6a1 1 0 0 1 0-1.4L13.9 1.3a1 1 0 0 1 1.4 0l6 6a1 1 0 0 1 0 1.4Z"/></svg> {html.escape(length_val)}</span>')
    hardware_val = specs.get("hardware")
    if hardware_val:
        quick_chips.append(f'<span class="quick-chip"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg> {html.escape(hardware_val)}</span>')
    quick_chips_html = f'        <div class="product-quick-chips">\n          ' + "\n          ".join(quick_chips) + '\n        </div>\n' if quick_chips else ""

    trust_badges_html = """        <div class="product-trust-badges">
          <div class="trust-badge-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
            <span>Сегодня по Астане при заказе до 16:00</span>
          </div>
          <div class="trust-badge-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><polyline points="3 3 3 8 8 8"></polyline></svg>
            <span>Обмен 14 дней</span>
          </div>
          <div class="trust-badge-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="20 12 20 22 4 22 4 12"></polyline><rect x="2" y="7" width="20" height="5"></rect><line x1="12" y1="22" x2="12" y2="7"></line><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"></path><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"></path></svg>
            <span>Подарочная шкатулка</span>
          </div>
        </div>\n"""

    # D4. Блок «С этим носят» (Complete the look) — 2–3 изделия того же камня/серии
    pairs = find_pairs_with_products(product, all_products, limit=3)
    pairs_cards = []
    for pr in pairs:
        pr_id = pr["id"]
        pr_title = html.escape(pr["title"].strip())
        pr_price_num = int(pr.get("price") or 0)
        pr_price_fmt = format_price_ru(pr_price_num)
        pr_img = "/" + pr["image"].lstrip("/")
        pr_base, _ = os.path.splitext(pr_img)
        pr_thumb = f"{pr_base}-400w.webp"
        pr_mob = f"{pr_base}-750w.webp"
        pr_alt = html.escape(build_clean_alt(pr))
        pairs_cards.append(f"""          <article class="pair-card" data-id="{pr_id}">
            <a href="/product/{pr_id}.html" class="pair-img-link">
              <img src="{pr_thumb}" srcset="{pr_thumb} 400w, {pr_mob} 750w, {pr_img} 1440w" sizes="140px" alt="{pr_alt}" class="pair-img" width="140" height="186" loading="lazy" decoding="async">
            </a>
            <a href="/product/{pr_id}.html" class="pair-title">{pr_title}</a>
            <div class="pair-price">{pr_price_fmt} ₸</div>
            <button type="button" class="pair-add-btn" data-id="{pr_id}" data-title="{pr_title}" data-price="{pr_price_num}" data-image="{pr_img}" data-url="/product/{pr_id}.html">+ Добавить</button>
          </article>""")
    pairs_block_html = f"""        <section class="product-pairs-with" aria-label="С этим носят">
          <h2 class="product-pairs-title">С этим носят</h2>
          <div class="pairs-grid">
{"\n".join(pairs_cards)}
          </div>
        </section>\n""" if pairs_cards else ""

    # D5. Рекомендации для мини-корзины (R4: до 4 кандидатов, исключая текущий и уже добавленный товар)
    mini_recs = find_pairs_with_products(product, all_products, limit=4)
    mini_rec_items = []
    for mr in mini_recs:
        mr_id = mr["id"]
        mr_title = html.escape(mr["title"].strip())
        mr_price_num = int(mr.get("price") or 0)
        mr_price_fmt = format_price_ru(mr_price_num)
        mr_img = "/" + mr["image"].lstrip("/")
        mr_base, _ = os.path.splitext(mr_img)
        mr_thumb = f"{mr_base}-400w.webp"
        mini_rec_items.append(f"""          <div class="mini-rec-card">
            <img src="{mr_thumb}" alt="{mr_title}" width="48" height="64" class="mini-rec-img" loading="lazy">
            <div class="mini-rec-info">
              <div class="mini-rec-title">{mr_title}</div>
              <div class="mini-rec-price">{mr_price_fmt} ₸</div>
            </div>
            <button type="button" class="mini-rec-add" data-id="{mr_id}" data-title="{mr_title}" data-price="{mr_price_num}" data-image="{mr_img}" data-url="/product/{mr_id}.html">+ Добавить</button>
          </div>""")
    mini_rec_html = "\n".join(mini_rec_items)

    # Воздушный абзац описания (без сырых ценников комплекта в начале)
    about_text = description
    m_split = re.search(r'(?:сетом|отдельно)\.\s*(.*)', description, flags=re.S | re.I)
    if m_split and len(m_split.group(1).strip()) >= 40:
        about_text = m_split.group(1).strip()

    product_js_obj = json.dumps({
        "id": pid,
        "sku": livi_sku,
        "title": title,
        "price": price,
        "category": category,
        "image": "/" + img_rel,
        "url": page_url,
        "bundle_options": bundle_options
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('consent', 'default', {{
      'ad_storage': 'granted',
      'analytics_storage': 'granted',
      'ad_user_data': 'granted',
      'ad_personalization': 'granted',
      'wait_for_update': 500
    }});
    gtag('set', 'url_passthrough', true);
    gtag('set', 'ads_data_redaction', false);
    gtag('js', new Date());

    gtag('config', '{GA_ID}', {{ 'linker': {{ 'domains': ['livijewelry.kz'] }} }});
    gtag('config', '{AW_ID}', {{ 'allow_enhanced_conversions': true, 'linker': {{ 'domains': ['livijewelry.kz'] }} }});
  </script>

  <!-- Meta Pixel Code -->
  <script>
  !function(f,b,e,v,n,t,s)
  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');

  fbq('init', '{FB_PIXEL_1}');
  fbq('track', 'PageView');
  </script>
  <!-- End Meta Pixel Code -->

  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="google-site-verification" content="{GOOGLE_VERIFICATION}" />

  <title>{html.escape(page_title)}</title>
  <meta name="description" content="{html.escape(meta_desc)}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{page_url}" />
  <link rel="alternate" hreflang="ru-KZ" href="{page_url}" />
  <link rel="alternate" hreflang="ru" href="{page_url}" />
  <link rel="alternate" hreflang="kk-KZ" href="{kz_page_url}" />
  <link rel="alternate" hreflang="kk" href="{kz_page_url}" />
  <link rel="alternate" hreflang="uz-UZ" href="{uz_page_url}" />
  <link rel="alternate" hreflang="uz" href="{uz_page_url}" />
  <link rel="alternate" hreflang="x-default" href="{page_url}" />

  <!-- Open Graph / Product -->
  <meta property="og:type" content="product" />
  <meta property="og:site_name" content="Livi Jewelry" />
  <meta property="og:locale" content="ru_KZ" />
  <meta property="og:title" content="{html.escape(page_title)}" />
  <meta property="og:description" content="{html.escape(meta_desc)}" />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:image" content="{img_abs}" />
  <meta property="product:price:amount" content="{price}" />
  <meta property="product:price:currency" content="KZT" />
  <meta property="product:availability" content="in stock" />
  <meta property="product:condition" content="new" />
  <meta property="product:retailer_item_id" content="{pid}" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(page_title)}" />
  <meta name="twitter:description" content="{html.escape(meta_desc)}" />
  <meta name="twitter:image" content="{img_abs}" />

  <link rel="icon" type="image/png" href="/assets/logo.png">
  <link rel="apple-touch-icon" href="/assets/logo.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,600&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v=4">
  <script src="/scripts/storefront-menu.js" defer></script>

  <!-- Schema.org JSON-LD: Product (Merchant Listing) -->
  <script type="application/ld+json">
{json.dumps(product_ld, ensure_ascii=False, indent=2)}
  </script>

  <!-- Schema.org JSON-LD: BreadcrumbList -->
  <script type="application/ld+json">
{json.dumps(breadcrumb_ld, ensure_ascii=False, indent=2)}
  </script>

  <!-- Schema.org JSON-LD: FAQPage -->
  <script type="application/ld+json">
{json.dumps(faq_ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={FB_PIXEL_1}&ev=PageView&noscript=1"/></noscript>
{storefront_header(home_html, {"ru": page_url, "kk": kz_page_url, "uz": uz_page_url})}

  <main class="product-page storefront-product">
    <!-- Хлебные крошки -->
    <nav class="breadcrumbs" aria-label="Хлебные крошки">
      <a href="/">Главная</a>
      <span class="sep">/</span>
      <a href="/shop.html">Каталог</a>
      <span class="sep">/</span>
      <a href="{cat_hub_url}">{html.escape(cat_hub_label)}</a>
      <span class="sep">/</span>
      <span aria-current="page">{html.escape(title)}</span>
    </nav>

    <div class="product-detail-grid">
      <div class="product-gallery">
        <img src="/{img_rel}" srcset="/{thumb_img_rel} 400w, /{mob_img_rel} 750w, /{img_rel} 1440w" sizes="(max-width: 640px) 100vw, 50vw" alt="{html.escape(alt_text)}" width="900" height="1200" fetchpriority="high" decoding="async" />
        <a href="{instagram_url}" class="product-ig-btn" id="igModelBtn" target="_blank" rel="noopener" data-item-id="{pid}" aria-label="Смотреть украшение на модели в Instagram">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
            <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
            <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
          </svg>
          <span>Смотреть на модели в Instagram</span>
        </a>
      </div>

      <div class="product-info-col">
        <div class="product-sku-badge">Артикул: {livi_sku} · В наличии · Ручная работа</div>
        <h1 class="product-h1">{html.escape(title)}</h1>
        <div class="product-price-val">{price_fmt} ₸</div>
{quick_chips_html}{trust_badges_html}
{customizer_html}

        <div class="product-cta-group">
          <button type="button" class="btn primary" id="addToCartBtn">В корзину — {price_fmt} ₸</button>
          <a class="btn outline" id="waOrderBtn" href="{wa_href}" target="_blank" rel="noopener">
            <svg width="18" height="18" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
              <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
              <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
            </svg>
            <span>Заказать в 1 клик в WhatsApp</span>
          </a>
        </div>
        <div id="addedToast" class="added-toast" role="status" aria-live="polite" style="display:none;">
          ✓ Украшение добавлено в корзину! <a href="/cart.html" style="text-decoration:underline;font-weight:600;margin-left:6px;">Перейти к оформлению →</a>
        </div>

{bundle_badge_html}{pairs_block_html}        <!-- Блок «Об украшении» -->
        <section class="product-about-block" aria-label="Об украшении">
          <h2 class="product-about-title">Об украшении</h2>
          <p class="product-about-text">{html.escape(about_text)}</p>
        </section>

        <div class="product-accordions-group">
          <details class="product-accordion">
            <summary>Характеристики и материалы</summary>
            <div class="product-accordion-content">
              <dl class="product-specs-grid">
                <div class="spec-row"><dt>Артикул</dt><dd>{livi_sku}</dd></div>
                <div class="spec-row"><dt>Тип украшения</dt><dd>{html.escape(specs.get('type_ru', cat_ru))}</dd></div>
                <div class="spec-row"><dt>Основные камни и минералы</dt><dd><div class="mat-pills" style="margin-top:2px;">{material_pills}</div></dd></div>
                <div class="spec-row"><dt>Фурнитура и покрытие</dt><dd>{html.escape(specs.get('hardware', 'Гипоаллергенный ювелирный сплав (родий / позолота)'))}</dd></div>
                <div class="spec-row"><dt>Размер и посадка</dt><dd>{html.escape(specs.get('length_size') or 'Уточнить у мастера')}</dd></div>
                <div class="spec-row"><dt>Застежка</dt><dd>{html.escape(specs.get('clasp', 'Ювелирный карабин с удлинителем'))}</dd></div>
                <div class="spec-row"><dt>Комплектация и упаковка</dt><dd>{html.escape(specs.get('packaging', 'Фирменная подарочная шкатулка и бархатный мешочек Livi Jewelry'))}</dd></div>
              </dl>
            </div>
          </details>

          <details class="product-accordion">
            <summary>Доставка и гарантия</summary>
            <div class="product-accordion-content">
              <ul class="product-trust-list">
                <li><strong>Доставка день-в-день по Астане:</strong> отправка курьером в день заказа при оформлении до 16:00.</li>
                <li><strong>Доставка по всему Казахстану:</strong> Алматы, Шымкент, Караганда и все города РК экспресс-службой СДЭК (1–3 рабочих дня).</li>
                <li><strong>Международная доставка:</strong> бережная отправка по всему миру с трек-номером.</li>
                <li><strong>Гарантия и возврат:</strong> обмен или возврат в течение 14 дней согласно законодательству РК.</li>
              </ul>
            </div>
          </details>
{reviews_accordion_html}
        </div>
      </div>
    </div>

    <section class="related-section" aria-label="Похожие украшения">
      <h2>Похожие украшения ручной работы</h2>
      <div class="grid">
{related_html}
      </div>
    </section>

    <section class="hub-interlink-section" aria-label="Подборки по камням и стилям">
      <details class="hub-interlink-accordion">
        <summary>Подборки по камням и стилям</summary>
        <p class="hub-interlink-sub">Переходите в тематические коллекции Livi Jewelry по натуральным минералам и форматам украшений</p>
        <div class="hub-interlink-chips">
{interlink_chips_html}
        </div>
      </details>
    </section>

    <!-- Mobile Sticky Bottom Bar (Quick Actions) -->
    <aside class="mobile-sticky-bar" aria-label="Быстрый заказ">
      <div class="sticky-bar-inner">
        <div class="sticky-bar-info">
          <span class="sticky-bar-label">Цена:</span>
          <span class="sticky-bar-price">{price_fmt} ₸</span>
        </div>
        <div class="sticky-bar-actions">
          <button type="button" class="btn-sticky-cart" id="stickyCartBtn">
            <span>В корзину</span>
          </button>
          <a class="btn-sticky-wa" id="stickyWaBtn" href="{wa_href}" target="_blank" rel="noopener" aria-label="Заказать в WhatsApp">
            <svg width="18" height="18" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
              <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
              <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
            </svg>
            <span>WhatsApp</span>
          </a>
        </div>
      </div>
    </aside>
  </main>

  <footer id="contact" class="site-footer">
    <div class="wrap">
      <div class="footer-top">
        <div class="footer-brand">
          <h3>LIVI JEWELRY</h3>
          <p class="footer-tagline">Авторские украшения из натурального жемчуга и драгоценных минералов ручной работы.</p>
          <div class="footer-contacts">
            <div class="footer-contact-item">
              <span class="contact-label">Адрес:</span>
              <span>просп. Кабанбай Батыра, 43, г. Астана</span>
              <a href="https://maps.app.goo.gl/yrLFpFFKjz9kE1GHA" target="_blank" rel="noopener" class="footer-map-link">Маршрут в Google Картах →</a>
            </div>
            <div class="footer-contact-item">
              <span class="contact-label">Телефон:</span>
              <a href="tel:+77054510584">+7 705 451 05 84</a>
            </div>
            <div class="footer-contact-item">
              <span class="contact-label">WhatsApp:</span>
              <a href="https://wa.me/77054510584" target="_blank" rel="noopener">+7 705 451 05 84</a>
            </div>
            <div class="footer-contact-item">
              <span class="contact-label">Instagram:</span>
              <a href="https://www.instagram.com/livi_jwl/" target="_blank" rel="noopener">@livi_jwl</a>
            </div>
            <div class="footer-contact-item">
              <span class="contact-label">Режим работы:</span>
              <span>Ежедневно 11:00–17:00</span>
            </div>
          </div>
          <div class="kaspi-badge">
            <span class="kaspi-icon">●</span>
            <span>Оплата Kaspi (Kaspi Pay · QR)</span>
          </div>
        </div>

        <div class="footer-columns-grid">
          <div class="footer-col">
            <h4 class="footer-col-title">Колье и сотуары</h4>
            <ul class="footer-col-links">
              <li><a href="/kolye-iz-zhemchuga.html">Колье из жемчуга</a></li>
              <li><a href="/sotuary-iz-zhemchuga.html">Сотуары из жемчуга</a></li>
              <li><a href="/chokery-iz-naturalnyh-kamney.html">Чокеры из камней</a></li>
              <li><a href="/tsepi-s-barochnym-zhemchugom.html">Цепи с жемчугом</a></li>
              <li><a href="/ukrasheniya-iz-barochnogo-zhemchuga.html">Барочный жемчуг</a></li>
              <li><a href="/ukrasheniya-iz-zhemchuga-mayorka.html">Жемчуг Майорка</a></li>
            </ul>
          </div>

          <div class="footer-col">
            <h4 class="footer-col-title">Серьги и сеты</h4>
            <ul class="footer-col-links">
              <li><a href="/sergi-iz-zhemchuga.html">Серьги из жемчуга</a></li>
              <li><a href="/braslety-iz-zhemchuga.html">Браслеты из жемчуга</a></li>
              <li><a href="/komplekty-ukrasheniy.html">Комплекты украшений</a></li>
              <li><a href="/koltsa-i-garnitury-iz-kamney.html">Кольца и гарнитуры</a></li>
              <li><a href="/shop.html">Весь каталог</a></li>
            </ul>
          </div>

          <div class="footer-col">
            <h4 class="footer-col-title">Натуральные камни</h4>
            <ul class="footer-col-links">
              <li><a href="/ukrasheniya-iz-malahita.html">Малахит и нефрит</a></li>
              <li><a href="/ukrasheniya-iz-ametista.html">Аметист</a></li>
              <li><a href="/ukrasheniya-iz-granata.html">Гранат</a></li>
              <li><a href="/ukrasheniya-iz-rozovogo-kvarca.html">Розовый кварц</a></li>
              <li><a href="/ukrasheniya-iz-biryuzy.html">Натуральная бирюза</a></li>
              <li><a href="/ukrasheniya-iz-gornogo-hrustalya.html">Горный хрусталь</a></li>
            </ul>
          </div>

          <div class="footer-col">
            <h4 class="footer-col-title">Минералы и редкое</h4>
            <ul class="footer-col-links">
              <li><a href="/ukrasheniya-iz-tigrovogo-glaza.html">Тигровый глаз</a></li>
              <li><a href="/ukrasheniya-iz-koralla-i-yashmy.html">Коралл и яшма</a></li>
              <li><a href="/ukrasheniya-iz-lazurita.html">Натуральный лазурит</a></li>
              <li><a href="/ukrasheniya-iz-lunnogo-kamnya.html">Лунный камень</a></li>
              <li><a href="/ukrasheniya-iz-gematita.html">Гематит</a></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div class="footer-bottom-copy">
          © <span id="year">2026</span> Livi Jewelry. Все права защищены.
        </div>
        <div class="footer-bottom-links">
          <a href="/delivery.html">Доставка и оплата</a>
          <a href="/terms.html">Оферта</a>
          <a href="/privacy.html">Конфиденциальность</a>
          <a href="/kz/">Қазақша</a>
          <a href="/uz/">O‘zbekcha</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Floating WhatsApp Widget -->
  <a class="floating-wa" href="https://wa.me/77054510584?text=Здравствуйте!%20Подскажите,%20пожалуйста,%20по%20украшениям%20Livi%20Jewelry%20—%20хочу%20уточнить%20наличие%20и%20проконсультироваться%20✨" target="_blank" rel="noopener" aria-label="Консультация мастера в WhatsApp">
    <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
      <path fill="currentColor" d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
      <path fill="currentColor" d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
    </svg>
    <span class="floating-wa-text">Консультация мастера</span>
  </a>

  <script>
    const PRODUCT = {product_js_obj};
    let currentActivePrice = PRODUCT.price;
    let currentActiveTitle = PRODUCT.title;

    /* ===== Сквозная атрибуция (UTM / GCLID / FBCLID) ===== */
    (function captureAttribution(){{
      try {{
        const params = new URLSearchParams(window.location.search);
        const existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}');
        const keys = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','gbraid','wbraid','fbclid','yclid'];
        let hasNew = false;
        keys.forEach(k => {{
          const val = params.get(k);
          if(val) {{ existing[k] = val; hasNew = true; }}
        }});
        if(!existing.landing_page) existing.landing_page = window.location.pathname + window.location.search;
        if(!existing.referrer && document.referrer) existing.referrer = document.referrer;
        if(!existing.first_visit) existing.first_visit = new Date().toISOString();
        if(hasNew || !localStorage.getItem('livi_attribution')) {{
          localStorage.setItem('livi_attribution', JSON.stringify(existing));
        }}
      }} catch(e){{}}
    }})();

    function getAttributionSummary(txId){{
      return '';
    }}

    // Отправка события view_item при открытии страницы товара
    try {{
      if (typeof gtag === 'function') {{
        gtag('event', 'view_item', {{
          currency: 'KZT',
          value: PRODUCT.price,
          items: [{{
            item_id: PRODUCT.id,
            item_name: PRODUCT.title,
            item_category: PRODUCT.category,
            price: PRODUCT.price,
            quantity: 1
          }}]
        }});
      }}
      if (window.fbq) {{
        fbq('track', 'ViewContent', {{
          content_ids: [PRODUCT.id],
          content_name: PRODUCT.title,
          content_type: 'product',
          value: Math.max(1, Number(PRODUCT.price || 40000)),
          currency: 'KZT'
        }});
      }}
    }} catch (e) {{}}

    function readCart() {{
      try {{
        const raw = localStorage.getItem('livi_cart_v3') || localStorage.getItem('livi_cart_v2') || '[]';
        const arr = JSON.parse(raw);
        return Array.isArray(arr) ? arr.filter(it => it && typeof it === 'object' && (it.id || it.title)) : [];
      }} catch (e) {{ return []; }}
    }}

    function writeCart(items) {{
      try {{
        localStorage.setItem('livi_cart_v3', JSON.stringify(items));
        updateBadge();
      }} catch (e) {{}}
    }}

    function updateBadge() {{
      const count = readCart().reduce((s, i) => s + Number(i.qty || 0), 0);
      const b = document.getElementById('cartBadge');
      if (!b) return;
      if (count > 0) {{
        b.textContent = count;
        b.style.display = 'inline-block';
      }} else {{
        b.textContent = '';
        b.style.display = 'none';
      }}
    }}

    // Динамическое обновление WhatsApp и цены при выборе комплектации (bundle_options)
    const customBundleEl = document.getElementById('customBundle');
    const waBtn = document.getElementById('waOrderBtn');
    const stickyWaBtn = document.getElementById('stickyWaBtn');
    const addToCartBtn = document.getElementById('addToCartBtn');
    const stickyCartBtn = document.getElementById('stickyCartBtn');
    const priceDisplayEl = document.querySelector('.product-price-val');
    const stickyPriceEl = document.querySelector('.sticky-bar-price');

    function syncBundleSelection() {{
      if (customBundleEl) {{
        const opt = customBundleEl.options[customBundleEl.selectedIndex];
        const optPrice = parseInt(opt.getAttribute('data-price'), 10) || PRODUCT.price;
        currentActivePrice = optPrice;
        currentActiveTitle = opt.value;
        if (priceDisplayEl) {{
          priceDisplayEl.textContent = currentActivePrice.toLocaleString('ru-RU') + ' ₸';
        }}
        if (stickyPriceEl) {{
          stickyPriceEl.textContent = currentActivePrice.toLocaleString('ru-RU') + ' ₸';
        }}
        if (addToCartBtn) {{
          addToCartBtn.textContent = 'В корзину — ' + currentActivePrice.toLocaleString('ru-RU') + ' ₸';
        }}
      }}
      syncWhatsAppLink();
    }}

    function buildWhatsAppHref() {{
      const bundleVal = customBundleEl ? customBundleEl.value : currentActiveTitle;
      const priceFormatted = currentActivePrice.toLocaleString('ru-RU');
      const msg = `Здравствуйте! Хочу уточнить наличие и заказать: ${{bundleVal}} (Артикул: ${{PRODUCT.sku}}) за ${{priceFormatted}} ₸ ✨\\nСсылка: ${{PRODUCT.url}}`;
      return 'https://wa.me/77054510584?text=' + encodeURIComponent(msg);
    }}

    function syncWhatsAppLink() {{
      const link = buildWhatsAppHref();
      if (waBtn) {{
        waBtn.setAttribute('href', link);
      }}
      if (stickyWaBtn) {{
        stickyWaBtn.setAttribute('href', link);
      }}
    }}

    if (customBundleEl) customBundleEl.addEventListener('change', syncBundleSelection);
    syncBundleSelection();

    function handleAddToCart() {{
      const bundleVal = customBundleEl ? customBundleEl.value : currentActiveTitle;
      const items = readCart();
      const itemUniqueId = PRODUCT.id + (customBundleEl ? '-' + customBundleEl.selectedIndex : '');
      const idx = items.findIndex(x => x.id === itemUniqueId && !(x.customSize || x.size));
      if (idx >= 0) {{
        items[idx].qty = Number(items[idx].qty || 1) + 1;
      }} else {{
        items.push({{
          id: itemUniqueId,
          sku: PRODUCT.sku,
          title: bundleVal,
          price: currentActivePrice,
          unit: currentActivePrice,
          image: PRODUCT.image,
          qty: 1,
          customBundle: customBundleEl ? customBundleEl.value : '',
          url: PRODUCT.url
        }});
      }}
      writeCart(items);
      const toast = document.getElementById('addedToast');
      if (toast) toast.style.display = 'block';

      try {{
        if (typeof gtag === 'function') {{
          gtag('event', 'add_to_cart', {{
            currency: 'KZT',
            value: currentActivePrice,
            items: [{{
              item_id: PRODUCT.id,
              item_name: bundleVal,
              item_category: PRODUCT.category,
              price: currentActivePrice,
              quantity: 1
            }}],
            transport_type: 'beacon'
          }});
        }}
        if (window.fbq) {{
          fbq('track', 'AddToCart', {{
            content_ids: [PRODUCT.id],
            content_name: bundleVal,
            content_type: 'product',
            value: Math.max(1, Number(currentActivePrice || PRODUCT.price || 40000)),
            currency: 'KZT'
          }});
        }}
      }} catch (e) {{}}

      // D5. Открываем мини-корзину без принудительного перехода
      openMiniCart({{
        title: bundleVal,
        price: currentActivePrice,
        image: PRODUCT.image
      }});
    }}

    function openMiniCart(item) {{
      const modal = document.getElementById('miniCartModal');
      if (!modal) return;
      const titleEl = document.getElementById('miniCartItemTitle');
      const priceEl = document.getElementById('miniCartItemPrice');
      const imgEl = document.getElementById('miniCartItemImg');
      if (titleEl) titleEl.textContent = item.title;
      if (priceEl) priceEl.textContent = Number(item.price).toLocaleString('ru-RU') + ' ₸';
      if (imgEl && item.image) {{
        const thumb = item.image.replace('.webp', '-400w.webp');
        imgEl.src = thumb;
      }}
      // R4: Filter out items already in cart from recommendations
      try {{
        const currentCart = readCart();
        const cartIds = new Set(currentCart.map(function(c) {{ return c.id; }}));
        const recCards = modal.querySelectorAll('.mini-rec-card');
        let shownCount = 0;
        recCards.forEach(function(card) {{
          const addBtn = card.querySelector('.mini-rec-add');
          const recId = addBtn ? addBtn.getAttribute('data-id') : null;
          if (recId && cartIds.has(recId)) {{
            card.style.display = 'none';
          }} else if (shownCount < 2) {{
            card.style.display = 'flex';
            shownCount++;
          }} else {{
            card.style.display = 'none';
          }}
        }});
        const recsContainer = modal.querySelector('.mini-cart-recs');
        if (recsContainer) {{
          recsContainer.style.display = shownCount > 0 ? 'block' : 'none';
        }}
      }} catch (e) {{}}
      modal.style.display = 'flex';
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }}

    function closeMiniCart() {{
      const modal = document.getElementById('miniCartModal');
      if (!modal) return;
      modal.style.display = 'none';
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }}

    const miniClose = document.getElementById('miniCartClose');
    const miniCont = document.getElementById('miniCartContinue');
    const miniModal = document.getElementById('miniCartModal');
    if (miniClose) miniClose.addEventListener('click', closeMiniCart);
    if (miniCont) miniCont.addEventListener('click', closeMiniCart);
    if (miniModal) {{
      miniModal.addEventListener('click', function(e) {{
        if (e.target === miniModal) closeMiniCart();
      }});
    }}
    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') closeMiniCart();
    }});

    // Быстрое добавление из «С этим носят» и рекомендаций мини-корзины
    function attachQuickAdd(btn) {{
      btn.addEventListener('click', function(e) {{
        e.preventDefault();
        e.stopPropagation();
        const pId = btn.getAttribute('data-id');
        const pTitle = btn.getAttribute('data-title');
        const pPrice = Number(btn.getAttribute('data-price') || 0);
        const pImage = btn.getAttribute('data-image');
        const pUrl = btn.getAttribute('data-url');
        const items = readCart();
        const idx = items.findIndex(x => x.id === pId);
        if (idx >= 0) {{
          items[idx].qty = Number(items[idx].qty || 1) + 1;
        }} else {{
          items.push({{
            id: pId,
            sku: pId.replace('prod_', 'LIVI-'),
            title: pTitle,
            price: pPrice,
            unit: pPrice,
            image: pImage,
            qty: 1,
            url: pUrl
          }});
        }}
        writeCart(items);
        btn.textContent = '✓ В корзине';
        btn.classList.add('added');
        try {{
          if (typeof gtag === 'function') {{
            gtag('event', 'add_to_cart', {{
              currency: 'KZT',
              value: pPrice,
              items: [{{ item_id: pId, item_name: pTitle, price: pPrice, quantity: 1 }}],
              transport_type: 'beacon'
            }});
          }}
          if (window.fbq) {{
            fbq('track', 'AddToCart', {{
              content_ids: [pId],
              content_name: pTitle,
              content_type: 'product',
              value: pPrice,
              currency: 'KZT'
            }});
          }}
        }} catch(err) {{}}
      }});
    }}
    document.querySelectorAll('.pair-add-btn, .mini-rec-add').forEach(attachQuickAdd);

    // D3. Трекинг клика по кнопке Instagram на модели
    const igBtn = document.getElementById('igModelBtn');
    if (igBtn) {{
      igBtn.addEventListener('click', function() {{
        try {{
          if (typeof gtag === 'function') {{
            gtag('event', 'instagram_click', {{
              item_id: PRODUCT.id,
              item_name: PRODUCT.title,
              transport_type: 'beacon'
            }});
          }}
        }} catch(e) {{}}
      }});
    }}

    if (addToCartBtn) addToCartBtn.addEventListener('click', handleAddToCart);
    if (stickyCartBtn) stickyCartBtn.addEventListener('click', handleAddToCart);

    const stickyBar = document.querySelector('.mobile-sticky-bar');
    const mainCtaGroup = document.querySelector('.product-cta-group');
    if (stickyBar && mainCtaGroup && 'IntersectionObserver' in window) {{
      const stickyObs = new IntersectionObserver(function(entries) {{
        entries.forEach(function(entry) {{
          stickyBar.classList.toggle('is-hidden', entry.isIntersecting);
        }});
      }}, {{ threshold: 0.1 }});
      stickyObs.observe(mainCtaGroup);
    }}

    function handleWhatsAppClick(e) {{
      const txId = 'LIVI-WA-' + PRODUCT.id + '-' + Date.now();
      const targetUrl = buildWhatsAppHref(txId);
      if (waBtn) waBtn.setAttribute('href', targetUrl);
      if (stickyWaBtn) stickyWaBtn.setAttribute('href', targetUrl);
      try {{
        const orderTotal = Math.max(1, Number(currentActivePrice || PRODUCT.price || 40000));
        if (window.fbq) {{
          fbq('track', 'Contact');
          fbq('track', 'Lead', {{
            content_name: PRODUCT.title,
            content_ids: [PRODUCT.id],
            content_type: 'product',
            value: orderTotal,
            currency: 'KZT'
          }});
        }}
        if (typeof gtag === 'function') {{
          gtag('event', 'generate_lead', {{
            currency: 'KZT',
            value: orderTotal,
            method: 'WhatsApp',
            page_location: window.location.href,
            item_id: PRODUCT.id,
            lead_source: 'product_page_' + PRODUCT.id,
            transport_type: 'beacon'
          }});
          gtag('event', 'whatsapp_click', {{
            currency: 'KZT',
            value: currentActivePrice,
            method: 'WhatsApp',
            page_location: window.location.href,
            lead_source: 'product_page_' + PRODUCT.id,
            transport_type: 'beacon'
          }});
          gtag('event', 'conversion', {{
            'send_to': 'AW-16793974126/dLz3CKyagbAdEO7q_sc-',
            'value': 1.0,
            'currency': 'USD',
            'transport_type': 'beacon'
          }});
        }}
      }} catch (err) {{}}
      // Нативный синхронный переход: БЕЗ e.preventDefault() и БЕЗ setTimeout!
    }}

    if (waBtn) waBtn.addEventListener('click', handleWhatsAppClick);
    if (stickyWaBtn) stickyWaBtn.addEventListener('click', handleWhatsAppClick);

    // Сквозное отслеживание любых кликов по ссылкам WhatsApp на карточке товара (плавающая кнопка и др.)
    document.addEventListener('click', function(e) {{
      const a = e.target.closest('a[href*="wa.me"], a[href*="whatsapp.com"]');
      if (!a || a.id === 'waOrderBtn' || a.id === 'stickyWaBtn') return;
      try {{
        const orderTotal = Math.max(1, Number(typeof currentActivePrice !== 'undefined' ? currentActivePrice : (PRODUCT.price || 40000)));
        if (window.fbq) {{
          fbq('track', 'Contact');
          fbq('track', 'Lead', {{
            content_name: PRODUCT.title,
            content_ids: [PRODUCT.id],
            content_type: 'product',
            value: orderTotal,
            currency: 'KZT'
          }});
        }}
        if (typeof gtag === 'function') {{
          gtag('event', 'generate_lead', {{
            currency: 'KZT',
            value: orderTotal,
            method: 'WhatsApp',
            page_location: window.location.href,
            item_id: PRODUCT.id,
            lead_source: 'product_page_wa_link',
            transport_type: 'beacon'
          }});
          gtag('event', 'whatsapp_click', {{
            currency: 'KZT',
            value: (typeof currentActivePrice !== 'undefined' ? currentActivePrice : 40000),
            method: 'WhatsApp',
            page_location: window.location.href,
            lead_source: 'product_page_wa_link',
            transport_type: 'beacon'
          }});
          gtag('event', 'conversion', {{
            'send_to': 'AW-16793974126/dLz3CKyagbAdEO7q_sc-',
            'value': 1.0,
            'currency': 'USD',
            'transport_type': 'beacon'
          }});
        }}
      }} catch (err) {{}}
      // Нативный переход: БЕЗ e.preventDefault() и БЕЗ setTimeout!
    }});

    // Событие select_item при клике на похожие товары
    document.querySelectorAll('.related-section .card').forEach((card, idx) => {{
      card.addEventListener('click', function() {{
        try {{
          if (typeof gtag === 'function') {{
            gtag('event', 'select_item', {{
              item_list_name: 'Related Products',
              items: [{{
                item_id: card.getAttribute('data-rel-id') || '',
                item_name: card.getAttribute('data-rel-title') || '',
                item_category: card.getAttribute('data-rel-category') || '',
                price: Number(card.getAttribute('data-rel-price') || 0),
                index: idx + 1
              }}]
            }});
          }}
        }} catch (e) {{}}
      }});
    }});

    const yrEl = document.getElementById('year');
    if (yrEl) yrEl.textContent = new Date().getFullYear();
    updateBadge();
  </script>
  <!-- Mini-Cart Modal (D5 / R3) -->
  <div id="miniCartModal" class="mini-cart-backdrop mini-cart-modal" style="display:none;" aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="miniCartTitle">
    <div class="mini-cart-dialog">
      <div class="mini-cart-header">
        <h3 class="mini-cart-title" id="miniCartTitle">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true" style="color:var(--gold-text);"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <span>Добавлено в корзину</span>
        </h3>
        <button type="button" class="mini-cart-close" id="miniCartClose" aria-label="Закрыть">✕</button>
      </div>
      <div class="mini-cart-added-item">
        <img id="miniCartItemImg" src="/{thumb_img_rel}" alt="" width="56" height="74" class="mini-cart-item-img">
        <div class="mini-cart-item-info">
          <div id="miniCartItemTitle" class="mini-cart-item-title">{html.escape(title)}</div>
          <div id="miniCartItemPrice" class="mini-cart-item-price">{price_fmt} ₸</div>
        </div>
      </div>
      <div class="mini-cart-actions">
        <a href="/cart.html" class="btn primary mini-cart-btn-checkout">Оформить заказ →</a>
        <button type="button" class="btn outline mini-cart-btn-continue" id="miniCartContinue">Продолжить покупки</button>
      </div>
      <div class="mini-cart-recs">
        <h3 class="mini-cart-recs-title">С этим украшением рекомендуем:</h3>
        <div class="mini-rec-list">
{mini_rec_html}
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""


def build_static_card_html(product: dict, indent: str = "    ", is_first_row: bool = False, priority_high: bool = False) -> str:
    pid = product["id"]
    title = html.escape(product["title"].strip())
    price_num = int(product.get("price") or 0)
    price = format_price_ru(price_num)
    img = product["image"].lstrip("/")
    alt = html.escape(build_clean_alt(product))
    cat = html.escape(product.get("category") or "")
    base_img, _ = os.path.splitext(img)
    mob_img = f"{base_img}-750w.webp"
    thumb_img = f"{base_img}-400w.webp"
    if os.path.exists(thumb_img):
        srcset_attr = f' srcset="/{thumb_img} 400w, /{mob_img} 750w, /{img} 1440w" sizes="(max-width: 768px) 50vw, 300px"'
    elif os.path.exists(mob_img):
        srcset_attr = f' srcset="/{mob_img} 750w, /{img} 1440w" sizes="(max-width: 768px) 50vw, 300px"'
    else:
        srcset_attr = ""
    loading_attr = 'loading="eager" fetchpriority="high"' if priority_high else ('loading="eager"' if is_first_row else 'loading="lazy"')
    badge_html = ""
    return (
        f'{indent}<article class="card" data-id="{pid}">\n'
        f'{indent}  <a href="/product/{pid}.html" class="card-img-wrap">{badge_html}<img src="{img}"{srcset_attr} alt="{alt}" {loading_attr} decoding="async" width="600" height="800"></a>\n'
        f'{indent}  <div class="body">\n'
        f'{indent}    <div class="title"><a href="/product/{pid}.html" class="card-title-link" data-id="{pid}" data-title="{title}" data-price="{price_num}" data-category="{cat}">{title}</a></div>\n'
        f'{indent}    <div class="price">{price} ₸</div>\n'
        f'{indent}  </div>\n'
        f'{indent}</article>'
    )


def sync_static_catalogs(products: list):
    """Встраивает статическую HTML-разметку карточек и JSON-LD ItemList в shop.html и index.html для Googlebot без JS."""
    # 1. shop.html
    if os.path.exists("shop.html"):
        with open("shop.html", "r", encoding="utf-8") as f:
            shop_html = f.read()

        item_list_ld = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": idx + 1,
                    "url": f"{SITE_URL}/product/{p['id']}.html",
                    "item": {
                        "@type": "Product",
                        "name": p["title"].strip(),
                        "image": f"{SITE_URL}/{p['image'].lstrip('/')}",
                        "description": (p.get("description") or p["title"]).strip(),
                        "sku": p["id"],
                        "mpn": p["id"],
                        "brand": {"@type": "Brand", "name": "Livi Jewelry"},
                        "offers": {
                            "@type": "Offer",
                            "url": f"{SITE_URL}/product/{p['id']}.html",
                            "price": f"{int(p.get('price') or 0):.2f}",
                            "priceCurrency": "KZT",
                            "availability": "https://schema.org/InStock",
                        },
                    },
                }
                for idx, p in enumerate(products)
            ],
        }
        ld_script = f'<script type="application/ld+json" id="shopItemListLd">\n{json.dumps(item_list_ld, ensure_ascii=False, indent=2)}\n  </script>'
        shop_html = re.sub(
            r'<script type="application/ld\+json"(?:\s+id="shopItemListLd")?>\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"ItemList".*?</script>',
            lambda _: ld_script,
            shop_html,
            count=1,
            flags=re.DOTALL,
        )

        cards_block = "\n".join(build_static_card_html(p, indent="      ", is_first_row=(idx < 8), priority_high=(idx < 2)) for idx, p in enumerate(products))
        new_grid = f'<div class="grid" id="grid">\n{cards_block}\n    </div>'
        shop_html = re.sub(
            r'<div class="grid" id="grid">.*?</div>\s*(?=(?:<div id="catalogError"|<section|</main>))',
            lambda _: f"{new_grid}\n    ",
            shop_html,
            count=1,
            flags=re.DOTALL,
        )

        # Ensure catalogError is completely empty in raw HTML
        shop_html = re.sub(
            r'<div id="catalogError"[^>]*>.*?</div>',
            '<div id="catalogError" class="empty-state" hidden style="display:none" aria-hidden="true"></div>',
            shop_html,
            count=1,
            flags=re.DOTALL
        )

        with open("shop.html", "w", encoding="utf-8") as f:
            f.write(shop_html)
        print(f"[OK] Пререндеринг {len(products)} карточек и ItemList встроен в shop.html")

    # 2. index.html (один ряд избранных карточек)
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            index_html = f.read()

        by_id = {p["id"]: p for p in products if "id" in p}
        featured = [by_id[pid] for pid in FEATURED_IDS if pid in by_id]
        featured_ids = {p["id"] for p in featured}
        featured.extend(p for p in products if p["id"] not in featured_ids)
        featured = featured[:len(FEATURED_IDS)]

        feat_cards = "\n".join(build_static_card_html(p, indent="      ", is_first_row=True, priority_high=(idx < 2)) for idx, p in enumerate(featured))
        new_feat = f'<div id="featGrid" class="grid" aria-live="polite">\n{feat_cards}\n    </div>'
        index_html = re.sub(
            r'<div id="featGrid" class="grid" aria-live="polite">.*?</div>(?=\s*(?:<div class="catalog-more-wrap"|</section>))',
            lambda _: new_feat,
            index_html,
            count=1,
            flags=re.DOTALL,
        )

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(index_html)
        print(f"[OK] Пререндеринг {len(featured)} избранных карточек встроен в index.html")


def generate_all():
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    active = [p for p in products if p.get("inStock", True)]
    with open("index.html", encoding="utf-8") as f:
        home_html = f.read()
    os.makedirs("product", exist_ok=True)

    for p in products:
        out_path = os.path.join("product", f"{p['id']}.html")
        page_html = build_product_page_html(p, products, home_html)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)

    print(f"[OK] Сгенерировано {len(active)} страниц товаров в папке product/")
    sync_static_catalogs(active)


generate_product_pages = generate_all


if __name__ == "__main__":
    generate_all()
