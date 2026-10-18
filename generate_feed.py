import json
import os
import re
from xml.sax.saxutils import escape

# Configuration
SITE_URL = "https://livijewelry.kz"
PRODUCTS_FILE = "products.json"
OUTPUT_FILES = ["google_merchant_feed.xml", "feed.xml"]

# Google Product Taxonomy IDs for Jewelry
GOOGLE_CATEGORY_MAP = {
    "Necklaces": "196",   # Apparel & Accessories > Jewelry > Necklaces
    "Lariats": "196",     # Apparel & Accessories > Jewelry > Necklaces
    "Chains": "196",      # Apparel & Accessories > Jewelry > Necklaces
    "Bracelets": "191",   # Apparel & Accessories > Jewelry > Bracelets
    "Earrings": "194",    # Apparel & Accessories > Jewelry > Earrings
    "Rings": "200",       # Apparel & Accessories > Jewelry > Rings
    "Brooches": "192",    # Apparel & Accessories > Jewelry > Brooches & Lapel Pins
    "Sets": "6463",       # Apparel & Accessories > Jewelry > Jewelry Sets
}

PRODUCT_TYPE_MAP = {
    "Necklaces": "Украшения > Колье и бусы из натурального жемчуга и камней",
    "Lariats": "Украшения > Сотуары и галстуки",
    "Chains": "Украшения > Цепочки с натуральным жемчугом",
    "Bracelets": "Украшения > Браслеты из натуральных камней и жемчуга",
    "Earrings": "Украшения > Серьги из натурального жемчуга и камней",
    "Rings": "Украшения > Кольца из натуральных камней",
    "Sets": "Украшения > Ювелирные комплекты и сеты ручной работы",
}

HERO_IDS = {
    "prod_01", "prod_02", "prod_07", "prod_10", "prod_11",
    "prod_14", "prod_15", "prod_16", "prod_18", "prod_19",
    "prod_21", "prod_26", "prod_27", "prod_28"
}


def get_price_tier(price: int) -> str:
    """Assigns Custom Label 0 based on price margin tiers for PMax / Shopping bidding."""
    if price >= 55000:
        return "Tier_1_High_Margin_55k_Plus"
    elif price >= 35000:
        return "Tier_2_Core_35k_to_54k"
    else:
        return "Tier_3_Entry_Under_35k"


def get_main_stone_label(p: dict) -> str:
    """Assigns Custom Label 3 based on the main stone/mineral."""
    text = f"{p.get('title', '')} {p.get('description', '')} {' '.join(p.get('materials') or [])}".lower()
    if "барочн" in text:
        return "Baroque_Pearl"
    if "гематит" in text:
        return "Hematite"
    if "малахит" in text or "нефрит" in text or "жадеит" in text:
        return "Malachite"
    if "аметист" in text or "флюорит" in text:
        return "Amethyst"
    if "гранат" in text or "агат" in text:
        return "Garnet"
    if "бирюз" in text:
        return "Turquoise"
    if "розовый кварц" in text:
        return "Rose_Quartz"
    if "хрустал" in text or "циркон" in text or "кварц" in text:
        return "Crystal"
    return "Pearl"


def infer_color(materials: list, title: str) -> str:
    text = (" ".join(materials) + " " + title).lower()
    colors = []
    if "жемчуг" in text:
        colors.append("Белый перламутр")
    if "малахит" in text or "жадеит" in text or "нефрит" in text or "авантюрин" in text:
        colors.append("Зелёный")
    if "гранат" in text or "коралл" in text or "клубнич" in text:
        colors.append("Красный / Бордовый")
    if "аметист" in text or "флюорит" in text:
        colors.append("Фиолетовый")
    if "розовый кварц" in text:
        colors.append("Нежно-розовый")
    if "бирюз" in text:
        colors.append("Бирюзовый")
    if "позолота" in text or "позолоч" in text:
        colors.append("Золотистый")
    elif "родирован" in text or "сплав" in text:
        colors.append("Серебристый")

    if not colors:
        colors.append("Мультиколор / Перламутр")
    return " / ".join(colors[:3])


def build_enriched_g_title(p: dict) -> str:
    """
    Формирует обогащенный <g:title> до 150 символов:
    {title} — ручная работа ({главный_материал}) | Livi Jewelry
    """
    base_title = (p.get("title") or "").strip()
    materials = p.get("materials") or ["Натуральный жемчуг"]
    stones = [m for m in materials if not re.search(r"сплав|позолота|фурнитура", m, re.I)]
    main_mat = (stones[0] if stones else materials[0]).lower()
    enriched = f"{base_title} — ручная работа ({main_mat}) | Livi Jewelry"
    if len(enriched) > 150:
        enriched = f"{base_title} — ручная работа | Livi Jewelry"
    if len(enriched) > 150:
        enriched = enriched[:147].rstrip() + "..."
    return enriched


def build_rich_description(p: dict) -> str:
    base_desc = p.get("description", "").strip()
    materials = p.get("materials", [])
    mat_str = ", ".join(materials) if materials else "Натуральный жемчуг, ювелирный сплав"
    rich = (
        f"{base_desc} "
        f"Авторское украшение ручной работы от казахстанского бренда Livi Jewelry. "
        f"Материалы: {mat_str}. "
        f"Фирменная подарочная упаковка в комплекте. Быстрая доставка СДЭК по Астане, Алматы и всему Казахстану."
    )
    return rich.strip()


def generate_feed():
    if not os.path.exists(PRODUCTS_FILE):
        print(f"Error: {PRODUCTS_FILE} not found.")
        return

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">',
        '  <channel>',
        '    <title>Livi Jewelry — Украшения ручной работы из натурального жемчуга и камней</title>',
        f'    <link>{SITE_URL}</link>',
        '    <description>Официальный товарный фид Livi Jewelry (Астана, Алматы, Казахстан) для Google Merchant Center и Meta Catalog. Изделия из натурального жемчуга и полудрагоценных камней.</description>',
    ]

    for p in products:
        prod_id = escape(str(p.get("id", "")))
        g_title = escape(build_enriched_g_title(p))
        description = escape(build_rich_description(p))

        category = p.get("category", "Necklaces")
        google_cat = GOOGLE_CATEGORY_MAP.get(category, "188")
        product_type = escape(PRODUCT_TYPE_MAP.get(category, "Украшения > Ручная работа"))

        # Canonical static product URL (100% synced with JSON-LD Offer and Sitemap)
        item_link = escape(f"{SITE_URL}/product/{p.get('id')}.html")

        img_rel = p.get("image", "").lstrip("/")
        image_link = escape(f"{SITE_URL}/{img_rel}")

        price_val = int(p.get("price", 0))
        price_str = f"{price_val}.00 KZT"

        availability = "in_stock" if p.get("inStock", True) else "out_of_stock"

        materials = p.get("materials", [])
        material_str = escape(" / ".join(materials[:3])) if materials else "Натуральный жемчуг / Ювелирный сплав"
        color_str = escape(infer_color(materials, p.get("title", "")))

        custom_label_0 = get_price_tier(price_val)
        custom_label_1 = "Hero_Bestseller" if p.get("id") in HERO_IDS else "Catalog_Standard"
        custom_label_2 = escape(category)
        custom_label_3 = get_main_stone_label(p)
        custom_label_4 = "Handmade_KZ"

        item_xml = f"""    <item>
      <g:id>{prod_id}</g:id>
      <g:title>{g_title}</g:title>
      <g:description>{description}</g:description>
      <g:link>{item_link}</g:link>
      <g:image_link>{image_link}</g:image_link>
      <g:condition>new</g:condition>
      <g:availability>{availability}</g:availability>
      <g:price>{price_str}</g:price>
      <g:brand>Livi Jewelry</g:brand>
      <g:mpn>{prod_id}</g:mpn>
      <g:identifier_exists>no</g:identifier_exists>
      <g:google_product_category>{google_cat}</g:google_product_category>
      <g:product_type>{product_type}</g:product_type>
      <g:age_group>adult</g:age_group>
      <g:gender>female</g:gender>
      <g:color>{color_str}</g:color>
      <g:material>{material_str}</g:material>
      <g:product_highlight>100% натуральные камни и культивированный жемчуг</g:product_highlight>
      <g:product_highlight>Гипоаллергенная фурнитура со стойким покрытием (родий / позолота)</g:product_highlight>
      <g:product_highlight>Фирменная подарочная упаковка включена в стоимость</g:product_highlight>
      <g:product_highlight>Доставка день-в-день по Астане и СДЭК по всему Казахстану</g:product_highlight>
      <g:shipping>
        <g:country>KZ</g:country>
        <g:service>Курьер / СДЭК</g:service>
        <g:price>0.00 KZT</g:price>
      </g:shipping>
      <g:custom_label_0>{custom_label_0}</g:custom_label_0>
      <g:custom_label_1>{custom_label_1}</g:custom_label_1>
      <g:custom_label_2>{custom_label_2}</g:custom_label_2>
      <g:custom_label_3>{custom_label_3}</g:custom_label_3>
      <g:custom_label_4>{custom_label_4}</g:custom_label_4>
    </item>"""
        xml_lines.append(item_xml)

    xml_lines.extend([
        '  </channel>',
        '</rss>'
    ])

    xml_output = "\n".join(xml_lines) + "\n"

    for out_file in OUTPUT_FILES:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(xml_output)
        print(f"Successfully generated {out_file} with {len(products)} products.")


if __name__ == "__main__":
    generate_feed()
