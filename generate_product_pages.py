#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Livi Jewelry — Static Site Generation (SSG) for Product Pages.
Generates individual, ultra-optimized static HTML pages for Google StoreBot,
Google Merchant Center, Google Ads Quality Score and organic SEO.
"""

import os
import re
import json
import urllib.parse

BASE_URL = "https://livijewelry.kz"
PRODUCTS_FILE = "products.json"
OUTPUT_DIR = "product"

CATEGORY_MAP = {
    "Necklaces": ("Колье", "/kolye-iz-zhemchuga.html"),
    "Bracelets": ("Браслеты", "/braslety-iz-zhemchuga.html"),
    "Sets": ("Комплекты", "/shop.html"),
    "Chains": ("Цепи", "/shop.html"),
    "Lariats": ("Сотуары", "/shop.html"),
    "Rings": ("Кольца", "/shop.html"),
    "Earrings": ("Серьги", "/sergi-iz-zhemchuga.html"),
}

def clean_for_attr(text):
    if not text:
        return ""
    return text.replace('"', '&quot;').replace('\n', ' ').strip()

def generate_product_pages():
    if not os.path.exists(PRODUCTS_FILE):
        print(f"Error: {PRODUCTS_FILE} not found!")
        return []

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_files = []

    for idx, p in enumerate(products):
        pid = p.get("id")
        title = p.get("title", "Украшение Livi Jewelry").strip()
        price = int(p.get("price", 0))
        price_fmt = f"{price:,}".replace(",", " ")
        price_decimal = f"{price:.2f}"
        image_rel = p.get("image", "").lstrip("/")
        image_abs = f"{BASE_URL}/{image_rel}"
        cat_key = p.get("category", "Necklaces")
        cat_info = CATEGORY_MAP.get(cat_key, ("Украшения", "/shop.html"))
        cat_name = cat_info[0]
        cat_url = cat_info[1]
        materials = p.get("materials", [])
        desc = p.get("description", title).strip()
        is_archived = p.get("archived", False)
        in_stock = p.get("inStock", True) and not is_archived
        canonical_url = f"{BASE_URL}/product/{pid}.html"

        # SEO meta content
        clean_desc = clean_for_attr(desc)
        mat_summary = ", ".join(materials[:2]) if materials else "Натуральные материалы"
        meta_desc = f"{clean_desc} Цена: {price_fmt} ₸. Материалы: { clean_for_attr(mat_summary) }. Ручная работа, доставка по Казахстану."
        if len(meta_desc) > 280:
            meta_desc = meta_desc[:277] + "..."

        # Schema.org structured data (100% parity with Google Merchant Center feed)
        schema_product = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": title,
            "image": image_abs,
            "description": desc,
            "sku": pid,
            "mpn": pid,
            "brand": {
                "@type": "Brand",
                "name": "Livi Jewelry"
            },
            "offers": {
                "@type": "Offer",
                "url": canonical_url,
                "priceCurrency": "KZT",
                "price": price_decimal,
                "priceValidUntil": "2027-12-31",
                "availability": "https://schema.org/InStock" if in_stock else "https://schema.org/OutOfStock",
                "itemCondition": "https://schema.org/NewCondition",
                "seller": {
                    "@type": "Organization",
                    "name": "Livi Jewelry"
                },
                "shippingDetails": {
                    "@type": "OfferShippingDetails",
                    "shippingRate": {
                        "@type": "MonetaryAmount",
                        "value": "0",
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
                            "unitCode": "DAY"
                        },
                        "transitTime": {
                            "@type": "QuantitativeValue",
                            "minValue": 1,
                            "maxValue": 3,
                            "unitCode": "DAY"
                        }
                    }
                },
                "hasMerchantReturnPolicy": {
                    "@type": "MerchantReturnPolicy",
                    "applicableCountry": "KZ",
                    "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                    "merchantReturnDays": 14,
                    "returnMethod": [
                        "https://schema.org/ReturnByMail",
                        "https://schema.org/ReturnInStore"
                    ],
                    "returnFees": "https://schema.org/ReturnShippingFees",
                    "restockingFee": {
                        "@type": "MonetaryAmount",
                        "value": 0,
                        "currency": "KZT"
                    },
                    "itemCondition": "https://schema.org/NewCondition",
                    "returnPolicyUrl": f"{BASE_URL}/delivery.html"
                }
            }
        }

        schema_breadcrumbs = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": f"{BASE_URL}/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Каталог",
                    "item": f"{BASE_URL}/shop.html"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": cat_name,
                    "item": f"{BASE_URL}{cat_url}"
                },
                {
                    "@type": "ListItem",
                    "position": 4,
                    "name": title,
                    "item": canonical_url
                }
            ]
        }

        # Material badges HTML
        mat_pills_html = "\n".join([f'            <span class="mat-pill">{clean_for_attr(m)}</span>' for m in materials])

        # Stock badge
        if is_archived:
            stock_badge_html = '<span class="product-stock-pill out-stock"><span class="stock-dot"></span>Продано — доступно повторение на заказ в WhatsApp</span>'
        elif in_stock:
            stock_badge_html = '<span class="product-stock-pill in-stock"><span class="stock-dot"></span>В наличии (отправка день в день)</span>'
        else:
            stock_badge_html = '<span class="product-stock-pill out-stock"><span class="stock-dot"></span>Под заказ (изготовление 1–3 дня)</span>'

        # WhatsApp prefilled URL & CTA label
        if is_archived:
            wa_text = (
                f"Здравствуйте! Интересует повторение на заказ украшения в Livi Jewelry:\n\n"
                f"• {title}\n"
                f"• Стоимость: {price_fmt} тг\n"
                f"• Код товара: {pid}\n"
                f"• Ссылка: {canonical_url}\n\n"
                f"Подскажите, пожалуйста, возможно ли повторение на заказ и какие сроки изготовления?"
            )
            wa_btn_text = "Повторить на заказ в WhatsApp"
        else:
            wa_text = (
                f"Здравствуйте! Хочу оформить заказ на украшение в Livi Jewelry:\n\n"
                f"• {title}\n"
                f"• Стоимость: {price_fmt} тг\n"
                f"• Код товара: {pid}\n"
                f"• Ссылка: {canonical_url}\n\n"
                f"Подскажите, пожалуйста, наличие и условия доставки."
            )
            wa_btn_text = "Заказать в 1 клик через WhatsApp"
        wa_order_url = f"https://wa.me/77054510584?text={urllib.parse.quote(wa_text)}"

        # Related products (3 other items from active in-stock products)
        active_candidates = [other for other in products if other.get("id") != pid and not other.get("archived", False) and other.get("inStock", True)]
        same_cat = [other for other in active_candidates if other.get("category") == cat_key]
        diff_cat = [other for other in active_candidates if other.get("category") != cat_key]
        chosen_related = (same_cat + diff_cat)[:3]

        related_cards_html = []
        for r in chosen_related:
            r_id = r.get("id")
            r_title = r.get("title", "")
            r_price = int(r.get("price", 0))
            r_price_fmt = f"{r_price:,}".replace(",", " ")
            r_img = r.get("image", "").lstrip("/")
            related_cards_html.append(f"""        <article class="card">
          <a href="/product/{r_id}.html" class="card-link" aria-label="{clean_for_attr(r_title)}">
            <div class="card-img-wrap">
              <img src="../{r_img}" alt="{clean_for_attr(r_title)} — ручная работа Livi Jewelry ({r_price_fmt} тг)" loading="lazy" decoding="async" width="600" height="800">
            </div>
            <div class="body">
              <div class="title">{r_title}</div>
              <div class="price">{r_price_fmt} ₸</div>
            </div>
          </a>
        </article>""")
        related_cards_str = "\n".join(related_cards_html)

        # JSON objects for client script
        product_json_str = json.dumps({
            "id": pid,
            "title": title,
            "price": price,
            "image": f"../{image_rel}",
            "category": cat_key
        }, ensure_ascii=False)

        html_content = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
  <meta name="google-site-verification" content="qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0" />

  <!-- Primary SEO -->
  <title>{clean_for_attr(title)} ({pid}) — купить в Астане и Казахстане | Livi Jewelry</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

  <!-- Open Graph / Facebook / WhatsApp -->
  <meta property="og:type" content="product">
  <meta property="og:site_name" content="Livi Jewelry">
  <meta property="og:title" content="{clean_for_attr(title)} — Livi Jewelry">
  <meta property="og:description" content="{clean_desc}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{image_abs}">
  <meta property="og:image:secure_url" content="{image_abs}">
  <meta property="og:image:alt" content="{clean_for_attr(title)} — ручная работа Livi Jewelry ({price_fmt} тг)">
  <meta property="product:price:amount" content="{price_decimal}">
  <meta property="product:price:currency" content="KZT">
  <meta property="product:availability" content="{"in stock" if in_stock else "out of stock"}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{clean_for_attr(title)} — Livi Jewelry">
  <meta name="twitter:description" content="{clean_desc}">
  <meta name="twitter:image" content="{image_abs}">

  <!-- Fonts & Stylesheet -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">

  <!-- Icons & Manifest -->
  <link rel="icon" type="image/png" sizes="48x48" href="../favicon-48.png">
  <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="../favicon-16.png">
  <link rel="icon" href="../favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
  <link rel="manifest" href="../site.webmanifest">
  <meta name="theme-color" content="#141312">
  <meta name="msapplication-TileColor" content="#141312">

  <!-- Google tag (gtag.js): Consent Mode v2 + GA4 + Google Ads -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-YFF2TR0N36"></script>
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
    // GA4 Measurement
    gtag('config', 'G-YFF2TR0N36', {{
      'linker': {{ 'domains': ['livijewelry.kz'] }}
    }});
    // Google Ads Conversions & Dynamic Remarketing
    gtag('config', 'AW-16793974126', {{
      'allow_enhanced_conversions': true,
      'linker': {{ 'domains': ['livijewelry.kz'] }}
    }});

    // Immediate E-Commerce view_item for Google Analytics & Google Ads Dynamic Remarketing
    gtag('event', 'view_item', {{
      currency: 'KZT',
      value: {price},
      items: [{{
        id: '{pid}',
        item_id: '{pid}',
        item_name: {json.dumps(title, ensure_ascii=False)},
        price: {price},
        item_brand: 'Livi Jewelry',
        item_category: '{cat_key}',
        quantity: 1,
        google_business_vertical: 'retail'
      }}]
    }});
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
    fbq('init', '199604456030882');
    fbq('init', '4185620171718327');
    fbq('track', 'PageView');
    fbq('track', 'ViewContent', {{
      content_name: {json.dumps(title, ensure_ascii=False)},
      content_ids: ['{pid}'],
      content_type: 'product',
      value: {price},
      currency: 'KZT'
    }});
  </script>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=199604456030882&ev=PageView&noscript=1" alt="" /></noscript>

  <!-- Schema.org Microdata for Single Product (Google Merchant Center & Rich Results Compliant) -->
  <script type="application/ld+json">
{json.dumps(schema_breadcrumbs, ensure_ascii=False, indent=2)}
  </script>

  <script type="application/ld+json">
{json.dumps(schema_product, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <!-- Mobile Drawer Menu -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back"></div>
    <div class="drawer-panel" role="menu" aria-label="Меню навигации">
      <a href="../index.html">Главная</a>
      <a href="../shop.html">Каталог</a>
      <a href="../delivery.html">Доставка и оплата</a>
      <a href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
      <a href="https://wa.me/77054510584?text=Здравствуйте!%20Хочу%20украшение%20Livi%20Jewelry." target="_blank" rel="noopener">WhatsApp</a>
      <div class="lang">
        <button id="ruBtn">RU</button><button id="kkBtn">KZ</button><button id="enBtn">EN</button>
      </div>
    </div>
  </div>

  <!-- Header -->
  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Открыть меню"><span></span></button>

      <a class="brand" href="../index.html" aria-label="Livi Jewelry Главная">
        <span>LIVI JEWELRY</span>
      </a>

      <div class="nav-actions">
        <a class="cart-link" href="../cart.html">
          <span>Корзина</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
        <a class="quick-link ig-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener" aria-label="Instagram">
          <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
            <path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm5 5.5A4.5 4.5 0 1 0 16.5 12 4.505 4.505 0 0 0 12 7.5zm6.5-.75a1.25 1.25 0 1 0 1.25 1.25A1.25 1.25 0 0 0 18.5 6.75Zm-6.5 2A3.25 3.25 0 1 1 8.75 12 3.254 3.254 0 0 1 12 8.75Z"/>
          </svg>
        </a>
        <a class="quick-link wa-link" href="https://wa.me/77054510584?text=Здравствуйте!%20Хочу%20украшение%20Livi%20Jewelry." target="_blank" rel="noopener" aria-label="WhatsApp">
          <svg width="20" height="20" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
            <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
            <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
          </svg>
        </a>
      </div>
    </div>
  </header>

  <!-- Product Detail Section -->
  <main class="product-page-wrap">
    <!-- Breadcrumbs -->
    <nav class="breadcrumbs" aria-label="Навигационная цепочка">
      <a href="../index.html">Главная</a>
      <span class="sep">/</span>
      <a href="../shop.html">Каталог</a>
      <span class="sep">/</span>
      <a href="..{cat_url}">{cat_name}</a>
      <span class="sep">/</span>
      <span class="current" aria-current="page">{title}</span>
    </nav>

    <div class="product-detail-grid">
      <!-- Media Column -->
      <div class="product-detail-media">
        <div class="product-main-image-wrap">
          <img src="../{image_rel}"
               alt="{clean_for_attr(title)} — ручная работа Livi Jewelry ({price_fmt} тг)"
               loading="eager"
               fetchpriority="high"
               decoding="async"
               width="800"
               height="1067">
          <div class="product-badge-overlay">Livi Atelier • Ручная работа</div>
        </div>
      </div>

      <!-- Info Column -->
      <div class="product-detail-info">
        <div class="product-cat-tag">{cat_name} • Артикул {pid}</div>
        <h1 class="product-h1">{title}</h1>

        <div class="product-price-box">
          <span class="product-price-val">{price_fmt} ₸</span>
          {stock_badge_html}
        </div>

        <!-- Materials -->
        <div class="product-materials-block">
          <div class="product-materials-label">Материалы и ювелирная селекция:</div>
          <div class="product-materials-list">
{mat_pills_html}
          </div>
        </div>

        <!-- Description -->
        <div class="product-description-block">
          <div class="product-desc-text">{desc}</div>
        </div>

        <!-- Purchase & Actions -->
        <div class="product-cta-section">
          <div class="product-qty-row">
            <span class="qty-label">Количество:</span>
            <div class="qty-stepper">
              <button type="button" class="qty-btn" id="qtyMinus" aria-label="Уменьшить количество">−</button>
              <span class="qty-val" id="qtyVal">1</span>
              <button type="button" class="qty-btn" id="qtyPlus" aria-label="Увеличить количество">+</button>
            </div>
          </div>

          {('<button type="button" class="btn-add-cart-main" id="addToCartBtn" disabled style="opacity:0.6;cursor:not-allowed;"><span id="addToCartText">Продано (только на заказ)</span></button>' if is_archived else """<button type="button" class="btn-add-cart-main" id="addToCartBtn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
            <span id="addToCartText">Добавить в корзину</span>
          </button>""")}

          <a href="{wa_order_url}" class="btn-wa-single-order" id="buyWaBtn" target="_blank" rel="noopener">
            <svg width="20" height="20" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
              <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
              <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
            </svg>
            <span>{wa_btn_text}</span>
          </a>
        </div>

        <!-- Trust Badges -->
        <ul class="product-trust-list">
          <li class="product-trust-item">
            <span class="product-trust-icon">✨</span>
            <div><strong>100% натуральные материалы</strong> — отборный культивированный и барочный жемчуг, природные полудрагоценные минералы.</div>
          </li>
          <li class="product-trust-item">
            <span class="product-trust-icon">🎁</span>
            <div><strong>Фирменная люкс-упаковка</strong> — брендовая шкатулка или бархатный мешочек Livi Jewelry к каждому заказу.</div>
          </li>
          <li class="product-trust-item">
            <span class="product-trust-icon">🚚</span>
            <div><strong>Быстрая доставка по Казахстану</strong> — день в день курьером по Астане, 1–3 дня СДЭК до двери или пункта выдачи по всей стране.</div>
          </li>
          <li class="product-trust-item">
            <span class="product-trust-icon">💳</span>
            <div><strong>Безопасная оплата Kaspi Pay</strong> — выставление официального счета в приложении Kaspi.kz после подтверждения всех параметров.</div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Related Jewelry Section -->
    <section class="related-section">
      <h2 class="related-h2">Похожие украшения в наличии</h2>
      <div class="rule"></div>
      <div class="grid">
{related_cards_str}
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer>
    <div class="foot">
      <div class="foot-col">
        <div class="foot-brand">LIVI JEWELRY</div>
        <div class="foot-desc">Авторские украшения из натурального жемчуга и камней. Ручная работа с вниманием к каждой детали. Доставка по всему Казахстану.</div>
      </div>
      <div class="foot-col">
        <div class="foot-title">Навигация и правила</div>
        <div class="foot-links">
          <a href="../index.html">Главная страница</a>
          <a href="../shop.html">Каталог украшений</a>
          <a href="../delivery.html">Доставка, оплата и возврат (14 дней)</a>
          <a href="../privacy.html">Политика конфиденциальности</a>
          <a href="../terms.html">Условия использования (Оферта)</a>
        </div>
      </div>
      <div class="foot-col">
        <div class="foot-title">Связь с мастером</div>
        <div class="foot-links">
          <a href="https://wa.me/77054510584" target="_blank" rel="noopener">WhatsApp: +7 705 451 05 84</a>
          <a href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram: @livi_jwl</a>
          <span style="color:var(--muted);font-size:13px;">г. Астана, Казахстан</span>
        </div>
      </div>
    </div>
    <div class="foot-bot">
      <span>© <span id="footYear">2026</span> Livi Jewelry. Все права защищены.</span>
    </div>
  </footer>

  <!-- Floating WhatsApp Contact Button -->
  <a class="floating-wa" href="https://wa.me/77054510584?text=Здравствуйте!%20Хочу%20получить%20консультацию%20по%20украшениям%20Livi%20Jewelry." target="_blank" rel="noopener" aria-label="Консультация мастера в WhatsApp">
    <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
      <path fill="currentColor" d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
      <path fill="currentColor" d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
    </svg>
    <span class="floating-wa-text">Консультация мастера</span>
  </a>

  <!-- Interactive Logic -->
  <script>
    const CURRENT_PRODUCT = {product_json_str};

    // Cart management
    function readCart(){{
      try{{
        const raw3 = localStorage.getItem('livi_cart_v3');
        if (raw3 !== null) {{
          const items = JSON.parse(raw3);
          if (Array.isArray(items)) {{
            return items.filter(it => it && typeof it === 'object' && (it.id || it.title));
          }}
        }}
        const raw2 = localStorage.getItem('livi_cart_v2');
        if (raw2 !== null) {{
          const items = JSON.parse(raw2);
          if (Array.isArray(items)) {{
            const valid = items.filter(it => it && typeof it === 'object' && (it.id || it.title));
            if (valid.length > 0) {{
              localStorage.setItem('livi_cart_v3', JSON.stringify(valid));
            }}
            return valid;
          }}
        }}
        const raw1 = localStorage.getItem('livi_cart');
        if (raw1 !== null) {{
          const items = JSON.parse(raw1);
          if (Array.isArray(items)) {{
            const valid = items.filter(it => it && typeof it === 'object' && (it.id || it.title));
            if (valid.length > 0) {{
              localStorage.setItem('livi_cart_v3', JSON.stringify(valid));
            }}
            return valid;
          }}
        }}
        return [];
      }} catch(e){{
        return [];
      }}
    }}
    function writeCart(cart){{
      try {{
        const json = JSON.stringify(cart);
        localStorage.setItem('livi_cart_v3', json);
        localStorage.setItem('livi_cart_v2', json);
        localStorage.removeItem('livi_cart');
      }} catch(e){{}}
      updateBadge();
    }}
    function updateBadge(){{
      const count = readCart().reduce((sum, item) => sum + Number(item.qty || 0), 0);
      const b = document.getElementById('cartBadge');
      if(!b) return;
      if(count > 0){{
        b.textContent = count;
        b.style.display = 'inline-block';
      }} else {{
        b.textContent = '';
        b.style.display = 'none';
      }}
    }}
    window.addEventListener('storage', e => {{
      if(!e.key || e.key === 'livi_cart_v3' || e.key === 'livi_cart_v2') updateBadge();
    }});
    window.addEventListener('pageshow', updateBadge);
    document.addEventListener('visibilitychange', () => {{ if(!document.hidden) updateBadge(); }});

    // Quantity Stepper
    let currentQty = 1;
    const qtyValEl = document.getElementById('qtyVal');
    document.getElementById('qtyMinus').onclick = () => {{
      if(currentQty > 1){{
        currentQty--;
        qtyValEl.textContent = currentQty;
      }}
    }};
    document.getElementById('qtyPlus').onclick = () => {{
      currentQty++;
      qtyValEl.textContent = currentQty;
    }};

    // Add to Cart Action
    const addBtn = document.getElementById('addToCartBtn');
    const addText = document.getElementById('addToCartText');
    let addedTimeout = null;

    addBtn.onclick = () => {{
      const cart = readCart();
      const existingIdx = cart.findIndex(it => it.id === CURRENT_PRODUCT.id);
      const unit = Number(CURRENT_PRODUCT.price) || 0;
      const priceStr = unit ? `${{unit.toLocaleString('ru-RU')}} тг` : 'Цена по запросу';

      if(existingIdx > -1){{
        cart[existingIdx].qty = Number(cart[existingIdx].qty || 0) + currentQty;
        cart[existingIdx].title = CURRENT_PRODUCT.title;
        cart[existingIdx].unit = unit;
      }} else {{
        cart.push({{
          id: CURRENT_PRODUCT.id,
          title: CURRENT_PRODUCT.title,
          price: priceStr,
          img: (CURRENT_PRODUCT.image || '').replace(/^\\.\\.\\//, ''),
          qty: currentQty,
          unit: unit
        }});
      }}
      writeCart(cart);

      // GA4 & Google Ads Dynamic Remarketing Event
      if(typeof gtag === 'function'){{
        gtag('event', 'add_to_cart', {{
          currency: 'KZT',
          value: unit * currentQty,
          items: [{{
            id: CURRENT_PRODUCT.id,
            item_id: CURRENT_PRODUCT.id,
            item_name: CURRENT_PRODUCT.title,
            price: unit,
            item_brand: 'Livi Jewelry',
            quantity: currentQty,
            item_category: CURRENT_PRODUCT.category,
            google_business_vertical: 'retail'
          }}]
        }});
      }}

      // Meta Pixel Event
      if(window.fbq){{
        fbq('track', 'AddToCart', {{
          content_name: CURRENT_PRODUCT.title,
          content_ids: [CURRENT_PRODUCT.id],
          content_type: 'product',
          value: unit * currentQty,
          currency: 'KZT'
        }});
      }}

      // Visual Feedback
      addBtn.classList.add('added');
      addText.textContent = `✓ В корзине (${{currentQty}} шт.) — Перейти →`;
      clearTimeout(addedTimeout);
      addedTimeout = setTimeout(() => {{
        addBtn.onclick = () => {{ window.location.href = '../cart.html'; }};
      }}, 100);
    }};

    // Direct 1-Click Order via WhatsApp (Primary Conversion #1: purchase + Primary Conversion #2: generate_lead / contact)
    document.getElementById('buyWaBtn').addEventListener('click', function() {{
      try {{
        const totalValue = Number(CURRENT_PRODUCT.price) * currentQty;
        const txId = 'LIVI-' + Date.now();
        const itemsArr = [{{
          id: CURRENT_PRODUCT.id,
          item_id: CURRENT_PRODUCT.id,
          item_name: CURRENT_PRODUCT.title,
          price: Number(CURRENT_PRODUCT.price),
          item_brand: 'Livi Jewelry',
          item_category: CURRENT_PRODUCT.category,
          quantity: currentQty,
          google_business_vertical: 'retail'
        }}];

        if(typeof gtag === 'function'){{
          gtag('event', 'begin_checkout', {{
            currency: 'KZT',
            value: totalValue,
            items: itemsArr
          }});
          gtag('event', 'purchase', {{
            transaction_id: txId,
            currency: 'KZT',
            value: totalValue,
            affiliation: 'Livi Jewelry Direct Order',
            items: itemsArr
          }});
          gtag('event', 'conversion', {{
            'send_to': 'AW-16793974126/MuJ_CObHup8bEO7q_sc-',
            'value': totalValue,
            'currency': 'KZT',
            'transaction_id': txId
          }});
          gtag('event', 'generate_lead', {{
            currency: 'KZT',
            value: totalValue,
            method: 'WhatsApp',
            page_location: window.location.href,
            item_id: CURRENT_PRODUCT.id,
            lead_source: 'product_page_direct',
            items: itemsArr
          }});
          gtag('event', 'contact', {{
            currency: 'KZT',
            value: totalValue,
            method: 'WhatsApp',
            page_location: window.location.href,
            item_id: CURRENT_PRODUCT.id
          }});
        }}
        if(window.fbq) {{
          fbq('track', 'Purchase', {{ value: totalValue, currency: 'KZT', content_ids: [CURRENT_PRODUCT.id], content_type: 'product' }});
          fbq('track', 'Contact');
        }}
      }} catch(e){{}}
    }});

    // Global Contact Tracking for Header, Footer, Drawer & Floating WhatsApp / Instagram Links
    document.addEventListener('click', function(e) {{
      const a = e.target.closest('a[href]');
      if (!a || a.id === 'buyWaBtn') return;
      const href = a.getAttribute('href') || '';
      const isWa = href.includes('wa.me') || href.includes('whatsapp.com');
      const isIg = href.includes('instagram.com');
      if (!isWa && !isIg) return;

      const method = isWa ? 'WhatsApp' : 'Instagram';
      const val = Number(CURRENT_PRODUCT.price) * currentQty;
      try {{
        if (typeof gtag === 'function') {{
          gtag('event', 'generate_lead', {{
            currency: 'KZT',
            value: val,
            method: method,
            page_location: window.location.href,
            item_id: CURRENT_PRODUCT.id
          }});
          gtag('event', 'contact', {{
            currency: 'KZT',
            value: val,
            method: method,
            page_location: window.location.href,
            item_id: CURRENT_PRODUCT.id
          }});
          if (isWa) {{
            gtag('event', 'conversion', {{
              'send_to': 'AW-16793974126/MuJ_CObHup8bEO7q_sc-',
              'value': Math.round(val * 0.2),
              'currency': 'KZT',
              'transaction_id': 'LIVI-LEAD-' + Date.now()
            }});
          }}
        }}
        if (window.fbq) fbq('track', 'Contact');
      }} catch(err) {{}}

      // If link does not open in new tab, delay 150ms so beacon flushes reliably
      if (a.getAttribute('target') !== '_blank' && !e.ctrlKey && !e.metaKey) {{
        e.preventDefault();
        setTimeout(function() {{ window.location.href = href; }}, 150);
      }}
    }});

    // Mobile Drawer
    const drawer = document.getElementById('drawer');
    const burger = document.getElementById('burger');
    burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false'); }};
    drawer.querySelector('.drawer-back').onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden', 'true'); }};

    // Footer year & init badge
    const yr = document.getElementById('footYear');
    if(yr) yr.textContent = new Date().getFullYear();
    updateBadge();
  </script>
</body>
</html>
"""
        out_path = os.path.join(OUTPUT_DIR, f"{pid}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        generated_files.append(out_path)

    sync_static_catalogs(products)
    print(f"[OK] Successfully generated {len(generated_files)} static product pages in '{OUTPUT_DIR}/' and synced shop.html + index.html")
    return generated_files


def sync_static_catalogs(products):
    """Synchronizes shop.html JSON-LD ItemList, shop.html static #grid, and index.html static #featGrid from products.json."""
    # 1. Update shop.html JSON-LD ItemList and pre-rendered #grid
    if os.path.exists("shop.html"):
        active_products = [p for p in products if not p.get("archived", False)]
        item_list = []
        cards_html = []
        for idx, p in enumerate(active_products, start=1):
            pid = p.get("id", "")
            title = p.get("title", "")
            desc = p.get("description") or title
            price_num = int(p.get("price", 0))
            price_str = f"{price_num:.2f}"
            price_fmt = f"{price_num:,}".replace(",", " ")
            img_url = p.get("image", "").lstrip("/")
            in_stock = p.get("inStock", True)
            canonical_url = f"https://livijewelry.kz/product/{pid}.html" if pid else "https://livijewelry.kz/shop.html"
            item_list.append({
                "@type": "Product",
                "position": idx,
                "name": title,
                "image": f"https://livijewelry.kz/{img_url}",
                "description": desc,
                "sku": pid or "LV-01",
                "mpn": pid or "LV-01",
                "brand": {
                    "@type": "Brand",
                    "name": "Livi Jewelry"
                },
                "offers": {
                    "@type": "Offer",
                    "url": canonical_url,
                    "price": price_str,
                    "priceCurrency": "KZT",
                    "priceValidUntil": "2027-12-31",
                    "availability": "https://schema.org/InStock" if in_stock else "https://schema.org/OutOfStock",
                    "itemCondition": "https://schema.org/NewCondition",
                    "seller": {
                        "@type": "Organization",
                        "name": "Livi Jewelry"
                    },
                    "shippingDetails": {
                        "@type": "OfferShippingDetails",
                        "shippingRate": {
                            "@type": "MonetaryAmount",
                            "value": "0",
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
                                "unitCode": "DAY"
                            },
                            "transitTime": {
                                "@type": "QuantitativeValue",
                                "minValue": 1,
                                "maxValue": 3,
                                "unitCode": "DAY"
                            }
                        }
                    },
                    "hasMerchantReturnPolicy": {
                        "@type": "MerchantReturnPolicy",
                        "applicableCountry": "KZ",
                        "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                        "merchantReturnDays": 14,
                        "returnMethod": "https://schema.org/ReturnByMail",
                        "returnFees": "https://schema.org/ReturnShippingFees"
                    }
                }
            })
            alt_text = clean_for_attr(f"{title} — ручная работа Livi Jewelry ({price_fmt} тг)")
            cards_html.append(
                f'      <article class="card" data-id="{pid}">\n'
                f'        <div class="card-img-wrap"><img src="{img_url}" alt="{alt_text}" loading="lazy" decoding="async" width="600" height="800"></div>\n'
                f'        <div class="body">\n'
                f'          <div class="title"><a href="/product/{pid}.html" class="card-title-link">{title}</a></div>\n'
                f'          <div class="price">{price_fmt} ₸</div>\n'
                f'        </div>\n'
                f'      </article>'
            )

        schema_obj = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "itemListElement": item_list
        }
        schema_json = json.dumps(schema_obj, ensure_ascii=False, indent=2)
        with open("shop.html", "r", encoding="utf-8") as f:
            shop_html = f.read()

        pattern_schema = r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema.org",\s*"@type":\s*"ItemList".*?</script>'
        replacement_schema = f'<script type="application/ld+json">\n{schema_json}\n</script>'
        shop_html, _ = re.subn(pattern_schema, lambda m: replacement_schema, shop_html, flags=re.DOTALL)

        grid_inner = "\n".join(cards_html)
        pattern_grid = r'<div class="grid" id="grid">.*?</div>\s*</main>'
        replacement_grid = f'<div class="grid" id="grid">\n{grid_inner}\n    </div>\n  </main>'
        shop_html, _ = re.subn(pattern_grid, lambda m: replacement_grid, shop_html, flags=re.DOTALL)

        with open("shop.html", "w", encoding="utf-8") as f:
            f.write(shop_html)

    # 2. Update index.html pre-rendered #featGrid
    if os.path.exists("index.html"):
        active_products = [p for p in products if not p.get("archived", False)]
        feat_items = [p for p in active_products if p.get("featured")]
        if not feat_items:
            feat_items = active_products[:6]
        feat_cards = []
        for p in feat_items:
            pid = p.get("id", "")
            title = p.get("title", "")
            price_num = int(p.get("price", 0))
            price_fmt = f"{price_num:,}".replace(",", " ")
            img_url = p.get("image", "").lstrip("/")
            alt_text = clean_for_attr(f"{title} — ручная работа Livi Jewelry ({price_fmt} тг)")
            feat_cards.append(
                f'      <article class="card" onclick="if(!event.target.closest(\'a\'))location.href=\'/product/{pid}.html\'">\n'
                f'        <div class="card-img-wrap"><img src="{img_url}" alt="{alt_text}" loading="lazy" decoding="async" width="600" height="800"></div>\n'
                f'        <div class="body">\n'
                f'          <div class="title"><a href="/product/{pid}.html" class="card-title-link">{title}</a></div>\n'
                f'          <div class="price">{price_fmt} ₸</div>\n'
                f'        </div>\n'
                f'      </article>'
            )
        feat_inner = "\n".join(feat_cards)
        with open("index.html", "r", encoding="utf-8") as f:
            idx_html = f.read()
        pattern_feat = r'<div id="featGrid" class="grid" aria-live="polite">.*?</div>\s*</section>'
        replacement_feat = f'<div id="featGrid" class="grid" aria-live="polite">\n{feat_inner}\n    </div>\n  </section>'
        idx_html, _ = re.subn(pattern_feat, lambda m: replacement_feat, idx_html, flags=re.DOTALL)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(idx_html)

    # 3. Synchronize Category Landing Pages (kolye-iz-zhemchuga.html, braslety-iz-zhemchuga.html, sergi-iz-zhemchuga.html)
    prod_by_id = {p["id"]: p for p in products if p.get("id")}
    for cat_page in ("kolye-iz-zhemchuga.html", "braslety-iz-zhemchuga.html", "sergi-iz-zhemchuga.html"):
        if not os.path.exists(cat_page):
            continue
        with open(cat_page, "r", encoding="utf-8") as f:
            chtml = f.read()

        # Sync JSON-LD ItemList in category page
        def replace_cat_itemlist(match):
            raw_script = match.group(0)
            m_json = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', raw_script, flags=re.DOTALL)
            if not m_json:
                return raw_script
            try:
                data = json.loads(m_json.group(1))
                if data.get("@type") != "ItemList":
                    return raw_script
                for elem in data.get("itemListElement", []):
                    sku = elem.get("sku")
                    if sku in prod_by_id:
                        p = prod_by_id[sku]
                        elem["name"] = p["title"]
                        elem["description"] = p.get("description") or p["title"]
                        elem["image"] = f"https://livijewelry.kz/{p['image'].lstrip('/')}"
                        if "offers" in elem:
                            elem["offers"]["price"] = f"{int(p['price']):.2f}"
                            elem["offers"]["url"] = f"https://livijewelry.kz/product/{sku}.html"
                new_json = json.dumps(data, ensure_ascii=False, indent=2)
                return f'  <script type="application/ld+json">\n{new_json}\n  </script>'
            except Exception:
                return raw_script

        chtml = re.sub(
            r'  <script type="application/ld\+json">\s*\{\s*"@context"\s*:\s*"https://schema.org"\s*,\s*"@type"\s*:\s*"ItemList".*?</script>',
            replace_cat_itemlist,
            chtml,
            flags=re.DOTALL
        )

        # Sync product cards in category page
        def replace_cat_card(match):
            block = match.group(0)
            m_id = re.search(r'product/(prod_\d+)\.html', block)
            if not m_id or m_id.group(1) not in prod_by_id:
                return block
            pid = m_id.group(1)
            p = prod_by_id[pid]
            title = p["title"]
            price_fmt = f"{int(p['price']):,}".replace(",", " ") + " ₸"
            img_rel = p["image"].lstrip("/")
            alt_clean = clean_for_attr(f"{title} — ручная работа Livi Jewelry ({price_fmt})")
            block = re.sub(r'<img\s+[^>]*>', f'<img src="{img_rel}" alt="{alt_clean}" loading="lazy" width="600" height="800">', block)
            block = re.sub(
                r'<a href="product/' + re.escape(pid) + r'\.html" class="card-title-link">.*?</a>',
                f'<a href="product/{pid}.html" class="card-title-link">{title}</a>',
                block
            )
            block = re.sub(r'<div class="price">.*?</div>', f'<div class="price">{price_fmt}</div>', block)
            return block

        chtml = re.sub(r'<article class="card".*?</article>', replace_cat_card, chtml, flags=re.DOTALL)
        with open(cat_page, "w", encoding="utf-8") as f:
            f.write(chtml)


if __name__ == "__main__":
    generate_product_pages()
