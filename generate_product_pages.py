#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Livi Jewelry — Static Site Generation (SSG) for Product Pages.
Generates individual, ultra-optimized static HTML pages for Google StoreBot,
Google Merchant Center, Google Ads Quality Score and organic SEO.
"""

import os
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
        title = p.get("title", "Украшение Livi Jewelry")
        price = int(p.get("price", 0))
        price_fmt = f"{price:,}".replace(",", " ")
        image_rel = p.get("image", "").lstrip("/")
        image_abs = f"{BASE_URL}/{image_rel}"
        cat_key = p.get("category", "Necklaces")
        cat_info = CATEGORY_MAP.get(cat_key, ("Украшения", "/shop.html"))
        cat_name = cat_info[0]
        cat_url = cat_info[1]
        materials = p.get("materials", [])
        desc = p.get("description", title)
        in_stock = p.get("inStock", True)
        canonical_url = f"{BASE_URL}/product/{pid}.html"

        # SEO meta content
        clean_desc = clean_for_attr(desc)
        meta_desc = f"{clean_desc} Цена: {price_fmt} ₸. Натуральный жемчуг, ручная работа, доставка по Казахстану."
        if len(meta_desc) > 280:
            meta_desc = meta_desc[:277] + "..."

        # Schema.org structured data
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
                "price": str(price),
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
                    "returnFees": "https://schema.org/FreeReturn"
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
        if in_stock:
            stock_badge_html = '<span class="product-stock-pill in-stock"><span class="stock-dot"></span>В наличии (отправка день в день)</span>'
        else:
            stock_badge_html = '<span class="product-stock-pill out-stock"><span class="stock-dot"></span>Под заказ (изготовление 1–3 дня)</span>'

        # WhatsApp prefilled URL
        wa_text = (
            f"Здравствуйте! Хочу оформить заказ на украшение в Livi Jewelry:\n\n"
            f"• {title}\n"
            f"• Стоимость: {price_fmt} тг\n"
            f"• Код товара: {pid}\n"
            f"• Ссылка: {canonical_url}\n\n"
            f"Подскажите, пожалуйста, наличие и условия доставки."
        )
        wa_order_url = f"https://wa.me/77054510584?text={urllib.parse.quote(wa_text)}"

        # Related products (3 other items)
        related = [other for other in products if other.get("id") != pid]
        # Prioritize same category
        same_cat = [other for other in related if other.get("category") == cat_key]
        diff_cat = [other for other in related if other.get("category") != cat_key]
        chosen_related = (same_cat + diff_cat)[:3]

        related_cards_html = []
        for r in chosen_related:
            r_id = r.get("id")
            r_title = r.get("title", "")
            r_price = int(r.get("price", 0))
            r_price_fmt = f"{r_price:,}".replace(",", " ")
            r_img = r.get("image", "").lstrip("/")
            related_cards_html.append(f"""        <article class="card">
          <a href="{r_id}.html" class="card-link" aria-label="{clean_for_attr(r_title)}">
            <div class="card-img-wrap">
              <img src="../{r_img}" alt="{clean_for_attr(r_title)} — Livi Jewelry" loading="lazy" decoding="async">
            </div>
            <div class="body">
              <div class="title">{r_title}</div>
              <div class="price">{r_price_fmt} тг</div>
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

  <!-- Primary SEO -->
  <title>{clean_for_attr(title)} — купить в Астане и Казахстане | Livi Jewelry</title>
  <meta name="description" content="{clean_desc} Цена: {price_fmt} ₸. Натуральный жемчуг, ручная работа, доставка по Казахстану.">
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
  <meta property="og:image:alt" content="{clean_for_attr(title)} — авторские украшения Livi Jewelry">
  <meta property="product:price:amount" content="{price}">
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

  <!-- Google tag (gtag.js): GA4 + Google Ads -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-YFF2TR0N36"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{ dataLayer.push(arguments); }}
    gtag('js', new Date());
    // GA4 Measurement
    gtag('config', 'G-YFF2TR0N36');
    // Google Ads Conversions & Dynamic Remarketing
    gtag('config', 'AW-16793974126', {{ allow_enhanced_conversions: true }});

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
               alt="{clean_for_attr(title)} — авторские украшения Livi Jewelry"
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

          <button type="button" class="btn-add-cart-main" id="addToCartBtn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
            <span id="addToCartText">Добавить в корзину</span>
          </button>

          <a href="{wa_order_url}" class="btn-wa-single-order" id="buyWaBtn" target="_blank" rel="noopener">
            <svg width="20" height="20" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
              <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
              <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
            </svg>
            <span>Заказать в 1 клик через WhatsApp</span>
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
      <h2 class="related-h2">Вам также может понравиться</h2>
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
        <div class="foot-title">Навигация</div>
        <div class="foot-links">
          <a href="../index.html">Главная страница</a>
          <a href="../shop.html">Каталог украшений</a>
          <a href="../delivery.html">Доставка, оплата и возврат (14 дней)</a>
          <a href="../privacy.html">Политика конфиденциальности</a>
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
        const raw2 = localStorage.getItem('livi_cart_v2');
        const raw1 = localStorage.getItem('livi_cart');
        let items = [];
        if (raw3) {{
          try {{ items = JSON.parse(raw3); }} catch(e){{}}
        }}
        if ((!items || !items.length) && raw2) {{
          try {{ items = JSON.parse(raw2); }} catch(e){{}}
        }}
        if ((!items || !items.length) && raw1) {{
          try {{ items = JSON.parse(raw1); }} catch(e){{}}
        }}
        if (!Array.isArray(items)) return [];
        return items.filter(it => it && typeof it === 'object' && (it.id || it.title));
      }} catch(e){{
        return [];
      }}
    }}
    function writeCart(cart){{
      try {{
        const json = JSON.stringify(cart);
        localStorage.setItem('livi_cart_v3', json);
        localStorage.setItem('livi_cart_v2', json);
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
      const unit = CURRENT_PRODUCT.price;
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
          img: CURRENT_PRODUCT.image,
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

    // WhatsApp Click Tracking (Dynamic Remarketing + Lead)
    document.getElementById('buyWaBtn').onclick = () => {{
      try {{
        if(typeof gtag === 'function'){{
          gtag('event', 'whatsapp_click', {{
            currency: 'KZT',
            value: CURRENT_PRODUCT.price * currentQty,
            lead_source: 'product_page_direct',
            items: [{{
              id: CURRENT_PRODUCT.id,
              item_id: CURRENT_PRODUCT.id,
              item_name: CURRENT_PRODUCT.title,
              price: CURRENT_PRODUCT.price,
              item_brand: 'Livi Jewelry',
              item_category: CURRENT_PRODUCT.category,
              quantity: currentQty,
              google_business_vertical: 'retail'
            }}]
          }});
          gtag('event', 'conversion', {{
            'send_to': 'AW-16793974126/MuJ_CObHup8bEO7q_sc-',
            'value': Math.round((CURRENT_PRODUCT.price * currentQty) * 0.2),
            'currency': 'KZT',
            'transaction_id': 'WA-' + CURRENT_PRODUCT.id + '-' + Date.now()
          }});
        }}
        if(window.fbq) fbq('track', 'Contact');
      }} catch(e){{}}
    }};

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

    print(f"[OK] Successfully generated {len(generated_files)} static product pages in '{OUTPUT_DIR}/'")
    return generated_files

if __name__ == "__main__":
    generate_product_pages()
