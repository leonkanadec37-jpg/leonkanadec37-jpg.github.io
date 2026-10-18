#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор статической казахскоязычной витрины Livi Jewelry (Этап 5):
  - kz/index.html (Canonical: https://livijewelry.kz/kz/)
  - kz/shop.html  (Canonical: https://livijewelry.kz/kz/shop.html)

Обеспечивает:
- Полноценную индексацию по казахскоязычным запросам в Google.kz
- Двустороннюю связку hreflang (ru-KZ, ru, kk-KZ, kk, x-default)
- Пререндеринг карточек товаров на казахском языке с точным паритетом цен и SKU (prod_01..prod_28)
- Микроразметку JSON-LD: ["Organization", "JewelryStore"], FAQPage (6 вопросов на казахском), ItemList
- Полную поддержку аналитики GA4, Google Ads, Meta Pixel и сквозной атрибуции livi_attribution
"""

import html
import json
import os
import re

SITE_URL = "https://livijewelry.kz"
GA_ID = "G-YFF2TR0N36"
AW_ID = "AW-16793974126"
AW_CONV_LABEL = "AW-16793974126/MuJ_CObHup8bEO7q_sc-"
FB_PIXEL_1 = "199604456030882"
FB_PIXEL_2 = "4185620171718327"
GOOGLE_VERIFICATION = "qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0"

FEATURED_IDS = [
    "prod_01", "prod_02", "prod_06", "prod_07",
    "prod_10", "prod_11", "prod_16", "prod_17",
    "prod_19", "prod_20", "prod_23", "prod_24",
]

KZ_TRANSLATIONS = {
    "prod_01": {
        "title": "Барокко інжу алқасы бар табиғи інжуден жасалған көпқатарлы алқа",
        "desc": "Ірі барокко інжуінен жасалған акценттік аспасы бар таңдаулы табиғи інжуден құрастырылған сәнді көпқатарлы алқа.",
    },
    "prod_02": {
        "title": "Табиғи інжу мен тау хрусталінен жасалған алқа (Премиум)",
        "desc": "Премиум селекциялы табиғи інжу мен мөлдір тау хрусталінен және барокко інжуінен қолмен жиналған көпқабатты алқа.",
    },
    "prod_03": {
        "title": "Майорка інжуінен жасалған классикалық алқа",
        "desc": "Керамикалық моншақтары мен сәндік ілгегі бар Майорка інжуінен жасалған мінсіз тегіс классикалық алқа.",
    },
    "prod_04": {
        "title": "Жиынтық: алтын жалатылған тізбек және барокко інжулі білезік",
        "desc": "Жиынтықта: Алтын жалатылған тізбек — 25 000 тг, барокко інжулі білезік — 15 000 тг. Жиынтықтың толық бағасы — 40 000 тг. Әр бұйымды бөлек немесе толық сет ретінде сатып алуға болады.",
    },
    "prod_05": {
        "title": "Родий жалатылған тізбек және барокко інжулі білезік",
        "desc": "Жиынтықта: Родий жалатылған тізбек — 25 000 тг, барокко інжулі білезік — 15 000 тг. Жиынтықтың толық бағасы — 40 000 тг. Әр бұйымды бөлек немесе толық сет ретінде алуға болады.",
    },
    "prod_06": {
        "title": "Табиғи малахиттен жасалған білезік",
        "desc": "Фирмалық сәндік ілгегі бар қырлы табиғи малахит тасынан қолмен жасалған білезік.",
    },
    "prod_07": {
        "title": "Гарнитур: аметист пен інжу түйреуіш, білезік, сақина",
        "desc": "Жиынтықта: Аметист пен інжуден жасалған түйреуіш — 40 000 тг, білезік — 24 000 тг, сақина — 10 000 тг. Жиынтықтың толық бағасы — 74 000 тг.",
    },
    "prod_08": {
        "title": "Табиғи інжуден жасалған «Лапы» авторлық алқасы",
        "desc": "Ерекше өрімі мен көлемді фактурасы бар табиғи інжуден жасалған авторлық алқа.",
    },
    "prod_09": {
        "title": "Жиынтық: Табиғи авантюрин алқасы мен сырғалар",
        "desc": "Жиынтықта: Авантюрин алқасы — 34 000 тг, сырғалар — 10 000 тг. Жиынтықтың толық бағасы — 44 000 тг.",
    },
    "prod_10": {
        "title": "Жиынтық: Агат пен анар тастан жасалған алқа және сақина",
        "desc": "Жиынтықта: Агат пен анар тастан (гранат) алқа — 40 000 тг, сақина — 8 000 тг. Жиынтықтың толық бағасы — 48 000 тг.",
    },
    "prod_11": {
        "title": "Жиынтық: Аметист пен қызғылт кварц алқасы және аметист сырғалар",
        "desc": "Жиынтықта: Аметист пен қызғылт кварц алқасы — 45 000 тг, аметист сырғалар — 16 000 тг. Жиынтықтың толық бағасы — 61 000 тг.",
    },
    "prod_12": {
        "title": "Жиынтық: Жадеит пен жолбарыс көзінен алқа және сырғалар",
        "desc": "Жиынтықта: Жадеит пен жолбарыс көзінен алқа — 36 000 тг, сырғалар — 16 000 тг. Жиынтықтың толық бағасы — 52 000 тг.",
    },
    "prod_13": {
        "title": "Жиынтық: Майорка інжуінен алқа және сырғалар",
        "desc": "Жиынтықта: Майорка інжуінен алқа — 35 000 тг, сырғалар — 10 000 тг. Жиынтықтың толық бағасы — 45 000 тг.",
    },
    "prod_14": {
        "title": "Жиынтық: Маржан (коралл) мен яшмадан алқа, білезік, сырғалар",
        "desc": "Жиынтықта: Маржан мен яшма алқасы — 40 000 тг, білезік — 10 000 тг, сырғалар — 10 000 тг. Жиынтықтың толық бағасы — 60 000 тг.",
    },
    "prod_15": {
        "title": "Жиынтық: Қызғылт кварц пен інжуден алқа және сырғалар",
        "desc": "Жиынтықта: Қызғылт кварц пен інжуден алқа — 40 000 тг, сырғалар — 16 000 тг. Жиынтықтың толық бағасы — 56 000 тг.",
    },
    "prod_16": {
        "title": "Табиғи фирузадан (бирюза) жасалған авторлық жиынтық",
        "desc": "Табиғи фируза мен зергерлік фурнитурадан қолмен жиналған сәнді авторлық жиынтық.",
    },
    "prod_17": {
        "title": "Табиғи агат пен анар тастан жасалған сотуар-әшекей",
        "desc": "Табиғи агат пен қырлы анар тастан (гранат) қолмен құрастырылған талғампаз ұзын сотуар.",
    },
    "prod_18": {
        "title": "Гарнитур: түйреуіш, білезік, сырғалар, сақина (тапсырыспен)",
        "desc": "Жиынтықта: Түйреуіш — 30 000 тг, білезік — 24 000 тг, сырғалар — 10 000 тг, сақина — 10 000 тг. Толық бағасы — 74 000 тг (тапсырыспен).",
    },
    "prod_19": {
        "title": "Жолбарыс көзі мен гематиттен жасалған алқа",
        "desc": "Жолбарыс көзі мен графитті гематит тастарынан қолмен жасалған айқын геометриялық алқа.",
    },
    "prod_20": {
        "title": "Табиғи флюорит пен циркондардан жасалған алқа",
        "desc": "Жарқыраған циркон ендірмелері бар табиғи флюорит тасынан жасалған нәзік алқа.",
    },
    "prod_21": {
        "title": "Алқалар сеті: «Құлпынай» және інжу қосылған қызғылт кварц",
        "desc": "Жиынтықта: «Құлпынай» алқасы — 34 000 тг, қызғылт кварц пен інжу алқасы — 40 000 тг. Сеттің толық бағасы — 74 000 тг.",
    },
    "prod_22": {
        "title": "Табиғи інжу қосылған «Гранж» авторлық алқасы",
        "desc": "Ірі тізбек пен табиғи інжу үйлесім тапқан заманауи «Гранж» стиліндегі алқа.",
    },
    "prod_23": {
        "title": "Табиғи анар тастан (гранат) жасалған алқа",
        "desc": "Қанық шарап реңкті қырлы табиғи анар тастан (гранат) қолмен жиналған классикалық алқа.",
    },
    "prod_24": {
        "title": "Табиғи інжу мен лазуриттен жасалған алқа",
        "desc": "Ақ інжу мен терең көк лазурит тасының үйлесімінен туған авторлық алқа.",
    },
    "prod_25": {
        "title": "Анар тас (гранат) пен табиғи інжуден жасалған алқа",
        "desc": "Табиғи інжу мен қырлы анар тастан қолмен жиналған контрастты сәнді алқа.",
    },
    "prod_26": {
        "title": "Жиынтық: Фируза (бирюза) қосылған алқа және сырғалар",
        "desc": "Жиынтықта: Фируза қосылған алқа — 36 000 тг, сырғалар — 14 000 тг. Жиынтықтың толық бағасы — 50 000 тг.",
    },
    "prod_27": {
        "title": "Жиынтық: Нефрит пен гематит алқасы және сырғалар",
        "desc": "Жиынтықта: Нефрит пен гематит алқасы — 45 000 тг, сырғалар — 16 000 тг. Жиынтықтың толық бағасы — 61 000 тг.",
    },
    "prod_28": {
        "title": "Жиынтық: Табиғи фирузадан (бирюза) алқа, білезік, сырғалар, сақина",
        "desc": "Жиынтықта: Фирузадан алқа — 50 000 тг, білезік — 15 000 тг, сырғалар — 16 000 тг, сақина — 10 000 тг. Толық бағасы — 91 000 тг.",
    },
}

MATERIAL_MAP_KZ = {
    "Натуральный жемчуг": "Табиғи інжу",
    "Барочный жемчуг": "Барокко інжуі",
    "Натуральный барочный жемчуг": "Табиғи барокко інжуі",
    "Жемчуг Майорка": "Майорка інжуі",
    "Горный хрусталь": "Тау хрусталі",
    "Керамические бусины": "Керамикалық моншақтар",
    "Ювелирный сплав": "Гипоаллергенді зергерлік қорытпа",
    "Позолота": "Алтын жалату",
    "Натуральный малахит": "Табиғи малахит",
    "Натуральный аметист": "Табиғи аметист",
    "Натуральный авантюрин": "Табиғи авантюрин",
    "Натуральный агат": "Табиғи агат",
    "Натуральный гранат": "Табиғи анар тас (гранат)",
    "Розовый кварц": "Қызғылт кварц",
    "Натуральный жадеит": "Табиғи жадеит",
    "Тигровый глаз": "Жолбарыс көзі",
    "Натуральный коралл": "Табиғи маржан (коралл)",
    "Яшма": "Яшма",
    "Натуральная бирюза": "Табиғи фируза (бирюза)",
    "Натуральные камни": "Табиғи тастар",
    "Гематит": "Гематит",
    "Натуральный флюорит": "Табиғи флюорит",
    "Цирконы": "Циркондар",
    "Натуральный лазурит": "Табиғи лазурит",
    "Натуральный нефрит": "Табиғи нефрит",
}


def format_price_kz(price: int) -> str:
    return f"{int(price):,}".replace(",", " ")


def translate_product_kz(p: dict) -> dict:
    pid = p["id"]
    tr = KZ_TRANSLATIONS.get(pid, {})
    title_kz = tr.get("title") or p.get("title", "")
    desc_kz = tr.get("desc") or p.get("description", "")
    mats_ru = p.get("materials") or ["Натуральный жемчуг"]
    mats_kz = [MATERIAL_MAP_KZ.get(m, m) for m in mats_ru]
    return {
        "id": pid,
        "title": title_kz,
        "description": desc_kz,
        "price": int(p.get("price") or 0),
        "category": p.get("category") or "Necklaces",
        "image": "/" + p["image"].lstrip("/"),
        "materials": mats_kz,
        "inStock": p.get("inStock", True),
    }


def build_kz_card_html(pk: dict, indent: str = "      ") -> str:
    pid = pk["id"]
    title = html.escape(pk["title"])
    price_num = pk["price"]
    price_str = format_price_kz(price_num)
    img = pk["image"]
    stones = ", ".join(pk["materials"]).lower()
    alt = html.escape(f"{pk['title']} — қолмен жасалған ({stones}), Livi Jewelry")
    cat = html.escape(pk["category"])
    return (
        f'{indent}<article class="card" data-id="{pid}">\n'
        f'{indent}  <div class="card-img-wrap"><img src="{img}" alt="{alt}" loading="lazy" decoding="async" width="600" height="800"></div>\n'
        f'{indent}  <div class="body">\n'
        f'{indent}    <div class="title"><a href="/product/{pid}.html" class="card-title-link" data-id="{pid}" data-title="{title}" data-price="{price_num}" data-category="{cat}">{title}</a></div>\n'
        f'{indent}    <div class="price">{price_str} ₸</div>\n'
        f'{indent}  </div>\n'
        f'{indent}</article>'
    )


def generate_kz_index(products_kz: list) -> str:
    by_id = {p["id"]: p for p in products_kz}
    featured = [by_id[pid] for pid in FEATURED_IDS if pid in by_id]
    if len(featured) < 8:
        featured = products_kz[:12]

    feat_cards_html = "\n".join(build_kz_card_html(p, indent="      ") for p in featured)

    faq_items = [
        (
            "Астана, Алматы және бүкіл Қазақстан бойынша жеткізу қалай жүзеге асырылады?",
            "Астана бойынша тапсырыс берілген күні жедел курьерлік жеткізу (сол күні жеткізу) жұмыс істейді. Алматы, Шымкент, Қарағанды және Қазақстанның барлық қалаларына СДЭК курьерлік қызметімен есікке дейін немесе беру пунктіне 1–3 жұмыс күнінде жеткізіледі. Сондай-ақ бүкіл әлем бойынша халықаралық жеткізу (Worldwide shipping) бар."
        ),
        (
            "Әшекейлерде шынайы табиғи інжу мен табиғи тастар қолданыла ма?",
            "Иә, Livi Jewelry шеберханасы тек таңдаулы табиғи культивацияланған және барокко інжуімен, сондай-ақ табиғи минералдармен (малахит, қызғылт кварц, аметист, анар тас, тау хрусталі, гематит, фируза, агат, нефрит) жұмыс істейді. Барлық фурнитура төзімді родий немесе алтын жалатылған гипоаллергенді зергерлік қорытпадан жасалған."
        ),
        (
            "Алқа немесе білезікті жеке өлшем бойынша тапсырыспен жасатуға бола ма?",
            "Иә, әрбір алқа, чокер, білезік, сотуар немесе сақинаны сіздің жеке өлшеміңізге, қалаған ұзындығыңызға (мысалы, 38 см, 40 см, 42 см, 45 см) және фурнитура реңкіне (родий немесе алтын жалату) дәлме-дәл келтіріп жасаймыз."
        ),
        (
            "Әшекейлер қандай қаптамада келеді — сыйлыққа дайын ба?",
            "Әрбір Livi Jewelry әшекейі фирмалық сыйлық қорапшасына және барқыт дорбашаға ұқыпты салынады. Сыйлық қаптамасы бағаға тегін кіреді (0 ₸) және тапсырыс сыйлық ретінде табыстауға толық дайын."
        ),
        (
            "Төлемді Kaspi.kz арқылы қалай жасауға болады?",
            "Тапсырысты рәсімдегеннен кейін сіздің телефон нөміріңізге Kaspi.kz мобильді қосымшасына ИП Livi Jewelry атынан қашықтан төлем шоты жіберіледі."
        ),
        (
            "14 күн ішінде айырбастау және қайтару шарттары қандай?",
            "Қазақстан Республикасының заңнамасына сәйкес, егер бұйым пайдаланылмаған болса және оның тауарлық түрі мен фирмалық қаптамасы сақталса, алған сәттен бастап күнтізбелік 14 күн ішінде айырбастауға немесе қайтаруға болады."
        ),
    ]

    graph_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["Organization", "JewelryStore"],
                "@id": f"{SITE_URL}/kz/#organization",
                "name": "Livi Jewelry",
                "url": f"{SITE_URL}/kz/",
                "logo": f"{SITE_URL}/assets/logo.png",
                "image": f"{SITE_URL}/assets/hero-kole-iz-naturalnogo-zhemchuga-80000.webp",
                "description": "Табиғи інжу мен асыл тастардан қолдан жасалған авторлық әшекейлер шеберханасы. Астана, Алматы және бүкіл Қазақстан бойынша жеткізу.",
                "telephone": "+77054510584",
                "priceRange": "15000 KZT - 85000 KZT",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Астана",
                    "addressCountry": "KZ"
                },
                "sameAs": [
                    "https://instagram.com/livi_jwl",
                    "https://wa.me/77054510584"
                ]
            },
            {
                "@type": "FAQPage",
                "@id": f"{SITE_URL}/kz/#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}
                    }
                    for q, a in faq_items
                ]
            }
        ]
    }

    faq_html = "\n".join(
        f"""      <details class="faq-item"{' open' if i == 0 else ''}>
        <summary>{html.escape(q)}</summary>
        <div class="faq-answer">{html.escape(a)}</div>
      </details>"""
        for i, (q, a) in enumerate(faq_items)
    )

    return f"""<!doctype html>
<html lang="kk">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />

  <title>Табиғи інжу мен тастардан жасалған әшекейлер — алқалар, білезіктер, сырғалар сатып алу | Livi Jewelry Астана, Алматы</title>
  <meta name="description" content="Табиғи інжу мен тастардан қолдан жасалған авторлық әшекейлер: алқалар, білезіктер, сырғалар, сотуарлар және жиынтықтар. Бағасы 25 000 ₸ бастап. Астана бойынша сол күні жеткізу және бүкіл Қазақстанға (Алматы, Шымкент) СДЭК арқылы жеткізу.">
  <link rel="canonical" href="{SITE_URL}/kz/">
  <link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/" />
  <link rel="alternate" hreflang="ru" href="{SITE_URL}/" />
  <link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/" />
  <link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/" />
  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/" />
  <meta name="google-site-verification" content="{GOOGLE_VERIFICATION}" />

  <!-- Open Graph / Twitter -->
  <meta property="og:type" content="website">
  <meta property="og:locale" content="kk_KZ">
  <meta property="og:title" content="Табиғи інжу мен тастардан жасалған әшекейлер | Livi Jewelry Астана, Алматы">
  <meta property="og:description" content="Қолмен жасалған авторлық әшекейлер: алқалар, білезіктер, сырғалар, жиынтықтар. Фирмалық сыйлық қаптамасы және Қазақстан бойынша жеткізу.">
  <meta property="og:url" content="{SITE_URL}/kz/">
  <meta property="og:image" content="{SITE_URL}/assets/hero-kole-iz-naturalnogo-zhemchuga-80000.webp">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE_URL}/assets/hero-kole-iz-naturalnogo-zhemchuga-80000.webp">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">

  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{ dataLayer.push(arguments); }}
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
    fbq('init', '{FB_PIXEL_2}');
    fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={FB_PIXEL_1}&ev=PageView&noscript=1" /></noscript>

  <script type="application/ld+json">
{json.dumps(graph_ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back"></div>
    <div class="drawer-panel" role="menu" aria-label="Мәзір">
      <a href="/kz/">Басты бет</a>
      <a href="/kz/shop.html">Каталог (Дүкен)</a>
      <a href="/kolye-iz-zhemchuga.html">Інжу алқалар</a>
      <a href="/braslety-iz-zhemchuga.html">Білезіктер</a>
      <a href="/sergi-iz-zhemchuga.html">Сырғалар</a>
      <a href="/komplekty-ukrasheniy.html">Жиынтықтар</a>
      <a href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
      <a href="https://wa.me/77054510584?text=Сәлеметсіз%20бе!%20Livi%20Jewelry%20әшекейлері%20бойынша%20кеңес%20алғым%20келеді." target="_blank" rel="noopener">WhatsApp</a>
      <div class="lang">
        <a href="/" id="ruBtn" style="text-align:center;font-family:var(--font-sans);font-size:12px;">RU</a>
        <a href="/kz/" id="kkBtn" class="active" style="text-align:center;font-family:var(--font-sans);font-size:12px;">KZ</a>
      </div>
    </div>
  </div>

  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Мәзір"><span></span></button>
      <a class="brand" href="/kz/" aria-label="Livi Jewelry">
        <span>LIVI JEWELRY</span>
      </a>
      <div class="nav-actions">
        <div class="header-lang-links" aria-label="Тілді таңдау">
          <a href="/" lang="ru">RU</a>
          <a href="/kz/" class="active" lang="kk">KZ</a>
        </div>
        <a class="cart-link" href="/kz/shop.html">Дүкен</a>
        <a class="cart-link" href="/cart.html">
          <span>Себет</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
        <a class="quick-link wa-link" href="https://wa.me/77054510584?text=Сәлеметсіз%20бе!%20Livi%20Jewelry%20әшекейлері%20бойынша%20кеңес%20алғым%20келеді." target="_blank" rel="noopener" aria-label="WhatsApp">
          <span class="ql-text">WhatsApp</span>
        </a>
      </div>
    </div>
  </header>

  <section class="hero">
    <div class="hero-inner">
      <div>
        <h1>Табиғи інжу мен асыл тастардан қолдан жасалған авторлық әшекейлер</h1>
        <p class="lead">
          Қолмен жиналған эксклюзивті алқалар, білезіктер, сырғалар, сотуарлар және жиынтықтар. Гипоаллергенді фурнитура (родий / алтын жалату) және тегін фирмалық сыйлық қаптамасы. Астана бойынша сол күні курьерлік жеткізу, Алматы мен бүкіл Қазақстанға СДЭК арқылы жедел жөнелту.
        </p>
        <a class="btn" href="/kz/shop.html">Каталогқа өту</a>
      </div>
      <div class="hero-media">
        <img
          src="/assets/hero-kole-iz-naturalnogo-zhemchuga-80000.webp"
          alt="Барокко інжу алқасы бар табиғи інжуден жасалған көпқатарлы алқа — Livi Jewelry"
          loading="eager"
          fetchpriority="high"
          width="900"
          height="1200"
        >
      </div>
    </div>
  </section>

  <section class="section" id="featured">
    <h2>Таңдамалы әшекейлер мен табиғи тастар топтамасы</h2>
    <div class="rule"></div>

    <nav class="stone-chips" aria-label="Тастар мен санаттар бойынша топтамалар">
      <a href="/ukrasheniya-iz-barochnogo-zhemchuga.html" class="stone-chip">Барокко інжуі</a>
      <a href="/ukrasheniya-iz-malahita.html" class="stone-chip">Малахит</a>
      <a href="/ukrasheniya-iz-rozovogo-kvarca.html" class="stone-chip">Қызғылт кварц</a>
      <a href="/ukrasheniya-iz-gematita.html" class="stone-chip">Гематит</a>
      <a href="/ukrasheniya-iz-granata.html" class="stone-chip">Анар тас (Гранат)</a>
      <a href="/ukrasheniya-iz-ametista.html" class="stone-chip">Аметист</a>
      <a href="/ukrasheniya-iz-gornogo-hrustalya.html" class="stone-chip">Тау хрусталі</a>
      <a href="/ukrasheniya-iz-biryuzy.html" class="stone-chip">Фируза (Бирюза)</a>
      <a href="/ukrasheniya-iz-lunnogo-kamnya.html" class="stone-chip">Ай тасы және Перламутр</a>
      <a href="/kolye-iz-zhemchuga.html" class="stone-chip">Алқалар</a>
      <a href="/chokery-iz-naturalnyh-kamney.html" class="stone-chip">Чокерлер</a>
      <a href="/sotuary-iz-zhemchuga.html" class="stone-chip">Сотуарлар</a>
      <a href="/braslety-iz-zhemchuga.html" class="stone-chip">Білезіктер</a>
      <a href="/sergi-iz-zhemchuga.html" class="stone-chip">Сырғалар</a>
      <a href="/komplekty-ukrasheniy.html" class="stone-chip">Жиынтықтар</a>
    </nav>

    <div id="featGrid" class="grid" aria-live="polite">
{feat_cards_html}
    </div>
  </section>

  <section class="benefits-section" aria-label="Жеткізу және Livi Jewelry сервисі">
    <h2>Жеткізу географиясы және Livi Jewelry сервисі</h2>
    <div class="rule"></div>
    <div class="benefits-grid">
      <article class="benefit-card">
        <h3>Астана бойынша сол күні жеткізу</h3>
        <p>Тапсырыс берген күні Астананың барлық аудандарына жедел курьерлік жөнелту — маңызды сәтке әшекейді бүгін алыңыз.</p>
      </article>
      <article class="benefit-card">
        <h3>Бүкіл Қазақстан бойынша жеткізу</h3>
        <p>Алматы, Шымкент, Қарағанды, Атырау және ҚР барлық қалаларына СДЭК курьерлік қызметімен 1–3 жұмыс күнінде жеткіземіз.</p>
      </article>
      <article class="benefit-card">
        <h3>Жеке өлшем және гипоаллергенді фурнитура</h3>
        <p>Әрбір бұйымды сіздің мойын немесе білек өлшеміңізге сай дайындаймыз. Төзімді родий немесе алтын жалатылған фурнитура.</p>
      </article>
      <article class="benefit-card">
        <h3>Сыйлық қаптамасы тегін (0 ₸)</h3>
        <p>Фирмалық сыйлық қорапшасы мен барқыт дорбаша әр тапсырысқа тегін кіреді — бірден сыйлауға дайын.</p>
      </article>
    </div>
  </section>

  <section class="about" id="about">
    <div class="about-inner">
      <h2>Біз туралы — Livi Jewelry шеберханасы</h2>
      <div class="rule"></div>
      <p>
        Livi Jewelry — табиғи інжу мен асыл тастардан жасалған авторлық әшекейлер шеберханасы. Біз сырға, білезік, алқа, чокер, сотуар және сақиналарды дайын күйінде де, жеке тапсырыспен де — сіздің өлшеміңіз бен фурнитура реңкіне (родий немесе алтын жалату) сай қолмен жинаймыз.
      </p>
    </div>
  </section>

  <section class="faq-section" id="faq">
    <h2>Жиі қойылатын сұрақтар (FAQ)</h2>
    <div class="rule"></div>
    <div class="faq-list">
{faq_html}
    </div>
  </section>

  <footer id="contact">
    <div class="foot">
      <div class="links">
        <a href="/delivery.html">Жеткізу, төлем және қайтару</a>
        <a href="/privacy.html">Құпиялылық саясаты</a>
        <a href="/terms.html">Пайдалану шарттары</a>
        <a href="/kz/shop.html">Каталог</a>
        <a href="/">Русская версия</a>
      </div>
      <div class="copy">© <span id="year">2026</span> Livi Jewelry — Барлық құқықтар қорғалған.</div>
      <div class="links">
        <a class="tag" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="tag" href="https://wa.me/77054510584" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
  </footer>

  <script>
    (function captureAttribution(){{
      try {{
        const params = new URLSearchParams(window.location.search);
        const existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}');
        const keys = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','fbclid','yclid'];
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

    const drawer = document.getElementById('drawer'), burger = document.getElementById('burger');
    if(burger && drawer){{
      burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden','false'); }};
      drawer.querySelector('.drawer-back').onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden','true'); }};
    }}

    function updateBadge(){{
      try {{
        const raw = localStorage.getItem('livi_cart_v3') || '[]';
        const items = JSON.parse(raw);
        const count = Array.isArray(items) ? items.reduce((s,i)=>s+Number(i.qty||0),0) : 0;
        const b = document.getElementById('cartBadge');
        if(b) {{
          b.textContent = count > 0 ? count : '';
          b.style.display = count > 0 ? 'inline-block' : 'none';
        }}
      }} catch(e){{}}
    }}
    updateBadge();

    document.querySelectorAll('#featGrid .card').forEach((card, idx) => {{
      card.addEventListener('click', (e) => {{
        const pid = card.getAttribute('data-id');
        const link = card.querySelector('.card-title-link');
        if(typeof gtag === 'function' && link){{
          gtag('event', 'select_item', {{
            item_list_name: 'KZ Featured Home',
            items: [{{
              item_id: pid,
              item_name: link.getAttribute('data-title') || link.textContent,
              price: Number(link.getAttribute('data-price') || 0),
              index: idx + 1
            }}]
          }});
        }}
        if(!e.target.closest('a') && pid) {{
          window.location.href = '/product/' + pid + '.html';
        }}
      }});
    }});
  </script>
</body>
</html>
"""


def generate_kz_shop(products_kz: list) -> str:
    all_cards_html = "\n".join(build_kz_card_html(p, indent="      ") for p in products_kz)

    item_list_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "url": f"{SITE_URL}/product/{p['id']}.html",
                "name": p["title"],
                "image": f"{SITE_URL}{p['image']}",
                "description": p["description"],
                "sku": p["id"],
                "mpn": p["id"],
                "offers": {
                    "@type": "Offer",
                    "url": f"{SITE_URL}/product/{p['id']}.html",
                    "price": f"{p['price']:.2f}",
                    "priceCurrency": "KZT",
                    "availability": "https://schema.org/InStock",
                },
            }
            for idx, p in enumerate(products_kz)
        ],
    }

    products_kz_json = json.dumps(products_kz, ensure_ascii=False)

    return f"""<!doctype html>
<html lang="kk">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />

  <title>Інжу және табиғи тастардан жасалған әшекейлер каталогы — бағасы теңгемен | Livi Jewelry</title>
  <meta name="description" content="Табиғи інжу мен асыл тастардан қолдан жасалған әшекейлер каталогы: алқалар, білезіктер, сырғалар, сотуарлар және жиынтықтар. Бағасы 25 000 ₸ — 91 000 ₸. Астана мен Алматыға жедел жеткізу.">
  <link rel="canonical" href="{SITE_URL}/kz/shop.html">
  <link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/shop.html" />
  <link rel="alternate" hreflang="ru" href="{SITE_URL}/shop.html" />
  <link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/shop.html" />
  <link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/shop.html" />
  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/shop.html" />
  <meta name="google-site-verification" content="{GOOGLE_VERIFICATION}" />

  <meta property="og:type" content="website">
  <meta property="og:locale" content="kk_KZ">
  <meta property="og:title" content="Інжу және табиғи тастардан жасалған әшекейлер каталогы | Livi Jewelry">
  <meta property="og:description" content="Сырғалар, білезіктер, алқалар, сақиналар — табиғи інжу мен тастардан қолдан жасалған бижутерия.">
  <meta property="og:url" content="{SITE_URL}/kz/shop.html">
  <meta property="og:image" content="{SITE_URL}/assets/hero-kole-iz-naturalnogo-zhemchuga-80000.webp">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">

  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
  <link rel="icon" href="/favicon.ico" sizes="any">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{ dataLayer.push(arguments); }}
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
    fbq('init', '{FB_PIXEL_2}');
    fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={FB_PIXEL_1}&ev=PageView&noscript=1" /></noscript>

  <script type="application/ld+json">
{json.dumps(item_list_ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back"></div>
    <div class="drawer-panel" role="menu" aria-label="Мәзір">
      <a href="/kz/">Басты бет</a>
      <a href="/kz/shop.html">Каталог (Дүкен)</a>
      <a href="/kolye-iz-zhemchuga.html">Інжу алқалар</a>
      <a href="/braslety-iz-zhemchuga.html">Білезіктер</a>
      <a href="/sergi-iz-zhemchuga.html">Сырғалар</a>
      <a href="/komplekty-ukrasheniy.html">Жиынтықтар</a>
      <a href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
      <a href="https://wa.me/77054510584?text=Сәлеметсіз%20бе!%20Livi%20Jewelry%20әшекейлері%20бойынша%20кеңес%20алғым%20келеді." target="_blank" rel="noopener">WhatsApp</a>
      <div class="lang">
        <a href="/shop.html" id="ruBtn" style="text-align:center;font-family:var(--font-sans);font-size:12px;">RU</a>
        <a href="/kz/shop.html" id="kkBtn" class="active" style="text-align:center;font-family:var(--font-sans);font-size:12px;">KZ</a>
      </div>
    </div>
  </div>

  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Мәзір"><span></span></button>
      <a class="brand" href="/kz/">
        <span>LIVI JEWELRY</span>
      </a>
      <div class="nav-actions">
        <div class="header-lang-links" aria-label="Тілді таңдау">
          <a href="/shop.html" lang="ru">RU</a>
          <a href="/kz/shop.html" class="active" lang="kk">KZ</a>
        </div>
        <a class="cart-link" href="/cart.html">
          <span>Себет</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
        <a class="quick-link wa-link" href="https://wa.me/77054510584?text=Сәлеметсіз%20бе!%20Livi%20Jewelry%20әшекейлері%20бойынша%20кеңес%20алғым%20келеді." target="_blank" rel="noopener">
          <span class="ql-text">WhatsApp</span>
        </a>
      </div>
    </div>
  </header>

  <main class="wrap">
    <h1>Інжу және табиғи тастардан жасалған әшекейлер каталогы: алқалар, білезіктер, сырғалар, жиынтықтар</h1>

    <nav class="stone-chips" aria-label="Тастар мен санаттар бойынша топтамалар" style="margin: 18px 0 22px;">
      <a href="/kolye-iz-zhemchuga.html" class="stone-chip">Інжу алқалар</a>
      <a href="/braslety-iz-zhemchuga.html" class="stone-chip">Білезіктер</a>
      <a href="/sergi-iz-zhemchuga.html" class="stone-chip">Сырғалар</a>
      <a href="/komplekty-ukrasheniy.html" class="stone-chip">Жиынтықтар</a>
      <a href="/chokery-iz-naturalnyh-kamney.html" class="stone-chip">Чокерлер</a>
      <a href="/sotuary-iz-zhemchuga.html" class="stone-chip">Сотуарлар</a>
      <a href="/ukrasheniya-iz-barochnogo-zhemchuga.html" class="stone-chip">Барокко інжуі</a>
      <a href="/ukrasheniya-iz-gematita.html" class="stone-chip">Гематит</a>
      <a href="/ukrasheniya-iz-malahita.html" class="stone-chip">Малахит</a>
      <a href="/ukrasheniya-iz-ametista.html" class="stone-chip">Аметист</a>
      <a href="/ukrasheniya-iz-granata.html" class="stone-chip">Анар тас</a>
      <a href="/ukrasheniya-iz-rozovogo-kvarca.html" class="stone-chip">Қызғылт кварц</a>
      <a href="/ukrasheniya-iz-biryuzy.html" class="stone-chip">Фируза</a>
      <a href="/ukrasheniya-iz-gornogo-hrustalya.html" class="stone-chip">Тау хрусталі</a>
      <a href="/ukrasheniya-iz-lunnogo-kamnya.html" class="stone-chip">Ай тасы</a>
    </nav>

    <div class="grid" id="grid">
{all_cards_html}
    </div>
  </main>

  <footer id="contact">
    <div class="foot">
      <div class="links">
        <a href="/delivery.html">Жеткізу, төлем және қайтару (14 күн)</a>
        <a href="/privacy.html">Құпиялылық саясаты</a>
        <a href="/terms.html">Пайдалану шарттары</a>
        <a href="/kz/">Басты бет</a>
        <a href="/shop.html">Русский каталог</a>
      </div>
      <div class="copy">© <span id="footYear">2026</span> Livi Jewelry — Барлық құқықтар қорғалған.</div>
      <div class="links">
        <a class="tag" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="tag" href="https://wa.me/77054510584" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
  </footer>

  <script>
    const PRODUCTS_KZ = {products_kz_json};

    (function captureAttribution(){{
      try {{
        const params = new URLSearchParams(window.location.search);
        const existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}');
        const keys = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','fbclid','yclid'];
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

    const drawer = document.getElementById('drawer'), burger = document.getElementById('burger');
    if(burger && drawer){{
      burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden','false'); }};
      drawer.querySelector('.drawer-back').onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden','true'); }};
    }}

    function updateBadge(){{
      try {{
        const raw = localStorage.getItem('livi_cart_v3') || '[]';
        const items = JSON.parse(raw);
        const count = Array.isArray(items) ? items.reduce((s,i)=>s+Number(i.qty||0),0) : 0;
        const b = document.getElementById('cartBadge');
        if(b) {{
          b.textContent = count > 0 ? count : '';
          b.style.display = count > 0 ? 'inline-block' : 'none';
        }}
      }} catch(e){{}}
    }}
    updateBadge();

    if(typeof gtag === 'function'){{
      gtag('event', 'view_item_list', {{
        item_list_name: 'KZ Catalog',
        items: PRODUCTS_KZ.map((p, idx) => ({{
          item_id: p.id,
          item_name: p.title,
          item_category: p.category,
          price: p.price,
          index: idx + 1
        }}))
      }});
    }}

    document.querySelectorAll('#grid .card').forEach((card, idx) => {{
      card.addEventListener('click', (e) => {{
        const pid = card.getAttribute('data-id');
        const link = card.querySelector('.card-title-link');
        if(typeof gtag === 'function' && link){{
          gtag('event', 'select_item', {{
            item_list_name: 'KZ Catalog',
            items: [{{
              item_id: pid,
              item_name: link.getAttribute('data-title') || link.textContent,
              price: Number(link.getAttribute('data-price') || 0),
              index: idx + 1
            }}]
          }});
        }}
        if(!e.target.closest('a') && pid) {{
          window.location.href = '/product/' + pid + '.html';
        }}
      }});
    }});
  </script>
</body>
</html>
"""


def generate_kz_pages():
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    active = [p for p in products if p.get("inStock", True)]
    products_kz = [translate_product_kz(p) for p in active]

    os.makedirs("kz", exist_ok=True)
    with open(os.path.join("kz", "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_kz_index(products_kz))
    with open(os.path.join("kz", "shop.html"), "w", encoding="utf-8") as f:
        f.write(generate_kz_shop(products_kz))

    print(f"[OK] Сгенерированы казахскоязычные страницы: kz/index.html и kz/shop.html ({len(products_kz)} товаров)")


if __name__ == "__main__":
    generate_kz_pages()
