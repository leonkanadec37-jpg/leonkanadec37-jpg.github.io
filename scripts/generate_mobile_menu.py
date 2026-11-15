#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор унифицированного мобильного меню и навигации LIVI JEWELRY (Задача 007).
Поддерживает 3 языка (RU, KZ, UZ) с точным соответствием макету:
  - Шапка 58px: крестик (44x44), логотип, поиск (44x44), корзина (44x44 с бейджем)
  - Подпись «УКРАШЕНИЯ» (11px, 600, .2em, #85693F)
  - 5 основных категорий (56-58px, Cormorant Garamond 27px, шеврон 18px #9A9389, разделитель)
  - Кнопка «ВЕСЬ КАТАЛОГ →» (48px, рамка 1px #1F1D1A, без заливки, 12px 600 .16em)
  - «ЕЩЁ КАТЕГОРИИ» + ряд таблеток (44px, r22, рамка #DCD5C9, фон #FFFFFF, overflow-x: auto)
  - «ПО КАМНЮ» + ряд таблеток с цветными точками 16px (цвета из спецификации)
  - Разделитель 1px #E8E2D8
  - Служебные ссылки (48px, 15px 400, иконка 20px #85693F): «Доставка и оплата», «Магазин в Астане» (Google Maps)
  - 2 кнопки в ряд: WhatsApp (#2B2620, белый) и Instagram (белый, рамка #DCD5C9)
  - Сегментный переключатель языка на всю ширину (44px, r22, рамка #DCD5C9, активный #1F1D1A)
  - Адрес и телефон (12px, #6B665F, кликабельный tel:)
"""

import html

MENU_DATA = {
    "ru": {
        "home_url": "/",
        "search_url": "/shop.html?search=1",
        "cart_url": "/cart.html",
        "close_label": "Закрыть меню",
        "search_label": "Поиск по каталогу",
        "cart_label": "Корзина",
        "cart_text": "Корзина",
        "catalog_text": "Каталог",
        "menu_text": "Меню",
        "delivery_top_text": "Доставка",
        "jewelry_kicker": "УКРАШЕНИЯ",
        "categories": [
            ("Колье", "/shop.html?cat=Necklaces"),
            ("Серьги", "/sergi-iz-zhemchuga.html"),
            ("Браслеты", "/shop.html?cat=Bracelets"),
            ("Комплекты", "/shop.html?cat=Sets"),
            ("Кольца и сеты", "/koltsa-i-garnitury-iz-kamney.html"),
        ],
        "all_catalog_label": "ВЕСЬ КАТАЛОГ →",
        "all_catalog_url": "/shop.html?cat=All",
        "more_cats_kicker": "ЕЩЁ КАТЕГОРИИ",
        "more_categories": [
            ("Чокеры из камней", "/chokery-iz-naturalnyh-kamney.html"),
            ("Сотуары", "/sotuary-iz-zhemchuga.html"),
            ("Цепи с жемчугом", "/tsepi-s-barochnym-zhemchugom.html"),
        ],
        "by_stone_kicker": "ПО КАМНЮ",
        "stones": [
            ("Барочный жемчуг", "/ukrasheniya-iz-barochnogo-zhemchuga.html", "smm-dot-pearl"),
            ("Гематит", "/ukrasheniya-iz-gematita.html", "smm-dot-hematite"),
            ("Малахит", "/ukrasheniya-iz-malahita.html", "smm-dot-malachite"),
            ("Аметист", "/ukrasheniya-iz-ametista.html", "smm-dot-amethyst"),
            ("Гранат", "/ukrasheniya-iz-granata.html", "smm-dot-garnet"),
            ("Розовый кварц", "/ukrasheniya-iz-rozovogo-kvarca.html", "smm-dot-rosequartz"),
            ("Бирюза", "/ukrasheniya-iz-biryuzy.html", "smm-dot-turquoise"),
            ("Горный хрусталь", "/ukrasheniya-iz-gornogo-hrustalya.html", "smm-dot-crystal"),
            ("Лунный камень", "/ukrasheniya-iz-lunnogo-kamnya.html", "smm-dot-moonstone"),
            ("Жемчуг Майорка", "/ukrasheniya-iz-zhemchuga-mayorka.html", "smm-dot-pearl"),
            ("Тигровый глаз", "/ukrasheniya-iz-tigrovogo-glaza.html", "smm-dot-tigereye"),
            ("Коралл и Яшма", "/ukrasheniya-iz-koralla-i-yashmy.html", "smm-dot-coralyashma"),
            ("Лазурит", "/ukrasheniya-iz-lazurita.html", "smm-dot-lapis"),
        ],
        "delivery_label": "Доставка и оплата",
        "delivery_url": "/delivery.html",
        "store_label": "Магазин в Астане",
        "store_url": "https://maps.app.goo.gl/yrLFpFFKjz9kE1GHA",
        "wa_url": "https://wa.me/77054510584?text=Здравствуйте!%20Подскажите,%20пожалуйста,%20по%20украшениям%20Livi%20Jewelry%20—%20хочу%20уточнить%20наличие%20и%20проконсультироваться%20✨",
        "lang_select_label": "Выбор языка",
        "address": "Астана, пр. Кабанбай Батыра, 43",
        "phone": "+7 705 451 05 84",
        "phone_clean": "+77054510584",
    },
    "kk": {
        "home_url": "/kz/",
        "search_url": "/kz/shop.html?search=1",
        "cart_url": "/kz/cart.html",
        "close_label": "Мәзірді жабу",
        "search_label": "Әшекейлерді іздеу",
        "cart_label": "Себет",
        "cart_text": "Себет",
        "catalog_text": "Каталог",
        "menu_text": "Мәзір",
        "delivery_top_text": "Жеткізу",
        "jewelry_kicker": "ӘШЕКЕЙЛЕР",
        "categories": [
            ("Алқалар", "/kz/shop.html?cat=Necklaces"),
            ("Сырғалар", "/kz/sergi-iz-zhemchuga.html"),
            ("Білезіктер", "/kz/shop.html?cat=Bracelets"),
            ("Жиынтықтар", "/kz/shop.html?cat=Sets"),
            ("Сақиналар мен гарнитурлар", "/kz/koltsa-i-garnitury-iz-kamney.html"),
        ],
        "all_catalog_label": "БАРЛЫҚ КАТАЛОГ →",
        "all_catalog_url": "/kz/shop.html?cat=All",
        "more_cats_kicker": "БАСҚА САНАТТАР",
        "more_categories": [
            ("Табиғи тастардан чокерлер", "/kz/chokery-iz-naturalnyh-kamney.html"),
            ("Сотуарлар", "/kz/sotuary-iz-zhemchuga.html"),
            ("Інжу шынжырлар", "/kz/tsepi-s-barochnym-zhemchugom.html"),
        ],
        "by_stone_kicker": "ТАС БОЙЫНША",
        "stones": [
            ("Барокко інжуі", "/kz/ukrasheniya-iz-barochnogo-zhemchuga.html", "smm-dot-pearl"),
            ("Гематит", "/kz/ukrasheniya-iz-gematita.html", "smm-dot-hematite"),
            ("Малахит", "/kz/ukrasheniya-iz-malahita.html", "smm-dot-malachite"),
            ("Аметист", "/kz/ukrasheniya-iz-ametista.html", "smm-dot-amethyst"),
            ("Гранат", "/kz/ukrasheniya-iz-granata.html", "smm-dot-garnet"),
            ("Қызғылт кварц", "/kz/ukrasheniya-iz-rozovogo-kvarca.html", "smm-dot-rosequartz"),
            ("Бирюза", "/kz/ukrasheniya-iz-biryuzy.html", "smm-dot-turquoise"),
            ("Тау хрусталі", "/kz/ukrasheniya-iz-gornogo-hrustalya.html", "smm-dot-crystal"),
            ("Ай тасы", "/kz/ukrasheniya-iz-lunnogo-kamnya.html", "smm-dot-moonstone"),
            ("Майорка інжуі", "/kz/ukrasheniya-iz-zhemchuga-mayorka.html", "smm-dot-pearl"),
            ("Жолбарыс көзі", "/kz/ukrasheniya-iz-tigrovogo-glaza.html", "smm-dot-tigereye"),
            ("Маржан және яшма", "/kz/ukrasheniya-iz-koralla-i-yashmy.html", "smm-dot-coralyashma"),
            ("Лазурит", "/kz/ukrasheniya-iz-lazurita.html", "smm-dot-lapis"),
        ],
        "delivery_label": "Жеткізу және төлем",
        "delivery_url": "/kz/delivery.html",
        "store_label": "Астанадағы дүкен",
        "store_url": "https://maps.app.goo.gl/yrLFpFFKjz9kE1GHA",
        "wa_url": "https://wa.me/77054510584?text=Сәлеметсіз%20бе!%20Livi%20Jewelry%20әшекейлері%20бойынша%20кеңес%20алғым%20келеді.",
        "lang_select_label": "Тілді таңдау",
        "address": "Астана қ., Қабанбай батыр даңғылы, 43",
        "phone": "+7 705 451 05 84",
        "phone_clean": "+77054510584",
    },
    "uz": {
        "home_url": "/uz/",
        "search_url": "/uz/shop.html?search=1",
        "cart_url": "/uz/cart.html",
        "close_label": "Menyuni yopish",
        "search_label": "Taqinchoqlarni qidirish",
        "cart_label": "Savatcha",
        "cart_text": "Savatcha",
        "catalog_text": "Katalog",
        "menu_text": "Menyu",
        "delivery_top_text": "Yetkazib berish",
        "jewelry_kicker": "TAQINCHOQLAR",
        "categories": [
            ("Marjonlar", "/uz/shop.html?cat=Necklaces"),
            ("Ziraklar", "/uz/sergi-iz-zhemchuga.html"),
            ("Bilasuzuklar", "/uz/shop.html?cat=Bracelets"),
            ("To‘plamlar", "/uz/shop.html?cat=Sets"),
            ("Uzuklar va garniturlar", "/uz/koltsa-i-garnitury-iz-kamney.html"),
        ],
        "all_catalog_label": "BARCHA KATALOG →",
        "all_catalog_url": "/uz/shop.html?cat=All",
        "more_cats_kicker": "BOSHQA TOIFALAR",
        "more_categories": [
            ("Tabiiy toshlardan chokerlar", "/uz/chokery-iz-naturalnyh-kamney.html"),
            ("Sotuarlar", "/uz/sotuary-iz-zhemchuga.html"),
            ("Marvaridli zanjirlar", "/uz/tsepi-s-barochnym-zhemchugom.html"),
        ],
        "by_stone_kicker": "TOSH BOʻYICHA",
        "stones": [
            ("Barokko marvaridi", "/uz/ukrasheniya-iz-barochnogo-zhemchuga.html", "smm-dot-pearl"),
            ("Gematit", "/uz/ukrasheniya-iz-gematita.html", "smm-dot-hematite"),
            ("Malaxit", "/uz/ukrasheniya-iz-malahita.html", "smm-dot-malachite"),
            ("Ametist", "/uz/ukrasheniya-iz-ametista.html", "smm-dot-amethyst"),
            ("Granat", "/uz/ukrasheniya-iz-granata.html", "smm-dot-garnet"),
            ("Pushti kvars", "/uz/ukrasheniya-iz-rozovogo-kvarca.html", "smm-dot-rosequartz"),
            ("Firuza", "/uz/ukrasheniya-iz-biryuzy.html", "smm-dot-turquoise"),
            ("Tog‘ billuri", "/uz/ukrasheniya-iz-gornogo-hrustalya.html", "smm-dot-crystal"),
            ("Oy toshi", "/uz/ukrasheniya-iz-lunnogo-kamnya.html", "smm-dot-moonstone"),
            ("Mayorka marvaridi", "/uz/ukrasheniya-iz-zhemchuga-mayorka.html", "smm-dot-pearl"),
            ("Yo‘lbars ko‘zi", "/uz/ukrasheniya-iz-tigrovogo-glaza.html", "smm-dot-tigereye"),
            ("Marjon va Yashma", "/uz/ukrasheniya-iz-koralla-i-yashmy.html", "smm-dot-coralyashma"),
            ("Lazurit", "/uz/ukrasheniya-iz-lazurita.html", "smm-dot-lapis"),
        ],
        "delivery_label": "Yetkazib berish va to‘lov",
        "delivery_url": "/uz/delivery.html",
        "store_label": "Astanadagi doʻkon",
        "store_url": "https://maps.app.goo.gl/yrLFpFFKjz9kE1GHA",
        "wa_url": "https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20maslahat%20olmoqchiman.",
        "lang_select_label": "Tilni tanlash",
        "address": "Ostona sh., Qabanbay Botir shoh ko‘chasi, 43",
        "phone": "+7 705 451 05 84",
        "phone_clean": "+77054510584",
    },
}


def render_mobile_menu_html(lang: str = "ru", lang_urls: dict = None) -> str:
    """Генерирует HTML разметку мобильного меню согласно макету задачи 007."""
    cfg = MENU_DATA.get(lang, MENU_DATA["ru"])
    if not lang_urls:
        lang_urls = {
            "ru": "/",
            "kk": "/kz/",
            "uz": "/uz/",
        }

    # 3. Categories
    cat_items = []
    for title, url in cfg["categories"]:
        cat_items.append(
            f'        <a href="{url}" class="smm-category-row">\n'
            f'          <span>{html.escape(title)}</span>\n'
            f'          <svg class="smm-category-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#9A9389" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"></polyline></svg>\n'
            f'        </a>'
        )
    cats_html = "\n".join(cat_items)

    # 5. More categories pills
    more_items = []
    for title, url in cfg["more_categories"]:
        more_items.append(f'        <a href="{url}" class="smm-pill">{html.escape(title)}</a>')
    more_html = "\n".join(more_items)

    # 6. Stones pills
    stone_items = []
    for title, url, dot_class in cfg["stones"]:
        stone_items.append(
            f'        <a href="{url}" class="smm-pill"><span class="smm-stone-dot {dot_class}"></span>{html.escape(title)}</a>'
        )
    stones_html = "\n".join(stone_items)

    # 10. Language Switcher segment
    ru_active = ' active" aria-current="true' if lang == "ru" else ""
    kk_active = ' active" aria-current="true' if lang == "kk" else ""
    uz_active = ' active" aria-current="true' if lang == "uz" else ""

    ru_url = lang_urls.get("ru", "/")
    kk_url = lang_urls.get("kk", "/kz/")
    uz_url = lang_urls.get("uz", "/uz/")

    return f"""      <!-- Mobile Menu (Task 007) -->
      <div id="storefrontMobileMenu" class="storefront-mobile-menu storefront-mobile">
        <div class="smm-header">
          <button type="button" class="smm-close-btn" aria-label="{cfg['close_label']}">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
          <a class="smm-logo" href="{cfg['home_url']}" aria-label="Livi Jewelry">LIVI JEWELRY</a>
          <div class="smm-header-actions">
            <a href="{cfg['search_url']}" class="smm-icon-btn" aria-label="{cfg['search_label']}">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </a>
            <a href="{cfg['cart_url']}" class="smm-icon-btn smm-cart-btn" aria-label="{cfg['cart_label']}">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
              <span class="cart-badge smm-cart-badge" style="display:none"></span>
            </a>
          </div>
        </div>

        <div class="smm-content">
          <div class="smm-section-label">{cfg['jewelry_kicker']}</div>
          <div class="smm-categories">
{cats_html}
          </div>

          <a href="{cfg['all_catalog_url']}" class="smm-all-btn">{cfg['all_catalog_label']}</a>

          <div class="smm-section-label smm-scroll-label">{cfg['more_cats_kicker']}</div>
          <div class="smm-pills-scroll">
{more_html}
          </div>

          <div class="smm-section-label smm-scroll-label">{cfg['by_stone_kicker']}</div>
          <div class="smm-pills-scroll">
{stones_html}
          </div>

          <hr class="smm-divider">

          <div class="smm-services">
            <a href="{cfg['delivery_url']}" class="smm-service-link">
              <svg class="smm-service-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <rect x="1" y="3" width="15" height="13"></rect>
                <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                <circle cx="5.5" cy="18.5" r="2.5"></circle>
                <circle cx="18.5" cy="18.5" r="2.5"></circle>
              </svg>
              <span>{html.escape(cfg['delivery_label'])}</span>
            </a>
            <a href="{cfg['store_url']}" target="_blank" rel="noopener" class="smm-service-link">
              <svg class="smm-service-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              <span>{html.escape(cfg['store_label'])}</span>
            </a>
          </div>

          <div class="smm-social-buttons">
            <a href="{cfg['wa_url']}" target="_blank" rel="noopener" class="smm-btn-wa">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91C2.13 13.66 2.59 15.36 3.45 16.86L2.05 22L7.3 20.62C8.75 21.41 10.38 21.83 12.04 21.83C17.5 21.83 21.95 17.38 21.95 11.92C21.95 6.46 17.5 2 12.04 2M12.05 20.15C10.57 20.15 9.12 19.76 7.85 19.01L7.55 18.83L4.43 19.65L5.26 16.61L5.06 16.29C4.24 14.99 3.8 13.47 3.8 11.91C3.8 7.37 7.5 3.67 12.05 3.67C16.6 3.67 20.3 7.37 20.3 11.92C20.3 16.47 16.6 20.15 12.05 20.15M16.57 14.46C16.32 14.33 15.1 13.73 14.88 13.65C14.65 13.56 14.49 13.52 14.32 13.77C14.16 14.02 13.69 14.57 13.55 14.73C13.41 14.9 13.26 14.92 13.01 14.79C12.76 14.67 11.96 14.4 11.01 13.56C10.27 12.9 9.77 12.09 9.53 11.67C9.28 11.26 9.5 11.04 9.63 10.91C9.74 10.8 9.88 10.62 10.01 10.47C10.13 10.32 10.17 10.22 10.26 10.05C10.34 9.89 10.3 9.74 10.24 9.62C10.18 9.5 9.69 8.29 9.48 7.8C9.28 7.31 9.08 7.38 8.92 7.37H8.44C8.28 7.37 8.01 7.43 7.78 7.68C7.55 7.93 6.91 8.53 6.91 9.75C6.91 10.97 7.8 12.14 7.92 12.31C8.04 12.47 9.67 14.98 12.16 16.05C12.75 16.31 13.21 16.46 13.57 16.58C14.17 16.77 14.71 16.74 15.14 16.68C15.62 16.61 16.62 16.08 16.82 15.49C17.03 14.91 17.03 14.42 16.97 14.31C16.91 14.2 16.75 14.14 16.57 14.46Z"/></svg>
              <span>WhatsApp</span>
            </a>
            <a href="https://instagram.com/livi_jwl" target="_blank" rel="noopener" class="smm-btn-ig">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
              </svg>
              <span>Instagram</span>
            </a>
          </div>

          <div class="smm-lang-segment" role="group" aria-label="{cfg['lang_select_label']}">
            <a href="{ru_url}" hreflang="ru" class="smm-lang-btn{ru_active}" onclick="localStorage.setItem('lang','ru')">RU</a>
            <a href="{kk_url}" hreflang="kk" class="smm-lang-btn{kk_active}" onclick="localStorage.setItem('lang','kk')">KZ</a>
            <a href="{uz_url}" hreflang="uz" class="smm-lang-btn{uz_active}" onclick="localStorage.setItem('lang','uz')">UZ</a>
          </div>

          <div class="smm-footer-contacts">
            <p class="smm-address">{html.escape(cfg['address'])}</p>
            <p><a href="tel:{cfg['phone_clean']}" class="smm-phone">{html.escape(cfg['phone'])}</a></p>
          </div>
        </div>
      </div>"""


def render_desktop_menu_inner_html(lang: str = "ru", lang_urls: dict = None) -> str:
    """Генерирует HTML для десктопного каталога (>= 769px), который остается полностью неизменным."""
    cfg = MENU_DATA.get(lang, MENU_DATA["ru"])
    if not lang_urls:
        lang_urls = {"ru": "/", "kk": "/kz/", "uz": "/uz/"}

    cat_links = "\n".join(
        f'          <a href="{url}">{html.escape(title)}</a>'
        for title, url in cfg["categories"]
    )
    more_links = "\n".join(
        f'              <a href="{url}">{html.escape(title)}</a>'
        for title, url in cfg["more_categories"]
    )
    stone_links = "\n".join(
        f'            <a href="{url}">{html.escape(title)}</a>'
        for title, url, _ in cfg["stones"]
    )

    ru_active = ' class="active"' if lang == "ru" else ""
    kk_active = ' class="active"' if lang == "kk" else ""
    uz_active = ' class="active"' if lang == "uz" else ""

    ru_url = lang_urls.get("ru", "/")
    kk_url = lang_urls.get("kk", "/kz/")
    uz_url = lang_urls.get("uz", "/uz/")

    more_summary = "Другие категории" if lang == "ru" else ("Басқа санаттар" if lang == "kk" else "Boshqa toifalar")
    by_stone_summary = "По материалу" if lang == "ru" else ("Тас бойынша" if lang == "kk" else "Tosh bo‘yicha")
    feature_title = "Барочный жемчуг" if lang == "ru" else ("Барокко інжуі" if lang == "kk" else "Barokko marvaridi")
    feature_url = "/ukrasheniya-iz-barochnogo-zhemchuga.html" if lang == "ru" else (f"/{lang}/ukrasheniya-iz-barochnogo-zhemchuga.html")

    return f"""      <!-- Desktop Dropdown (>= 769px) -->
      <div class="storefront-menu-inner storefront-desktop">
        <div class="storefront-menu-types">
          <p class="storefront-kicker">{cfg['jewelry_kicker']}</p>
{cat_links}
          <a class="storefront-all" href="{cfg['all_catalog_url']}">{cfg['all_catalog_label']} <span aria-hidden="true">↗</span></a>
          <details class="storefront-more-types">
            <summary>{more_summary}</summary>
            <div class="storefront-menu-links">
{more_links}
            </div>
          </details>
        </div>
        <details class="storefront-materials" open>
          <summary>{by_stone_summary}</summary>
          <div class="storefront-menu-links">
{stone_links}
          </div>
        </details>
        <a class="storefront-menu-feature storefront-desktop" href="{feature_url}">
          <picture>
            <source media="(min-width: 769px)" srcset="/assets/hero-kole-iz-naturalnogo-zhemchuga-80000-750w.webp">
            <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3C/svg%3E" alt="{feature_title}" width="750" height="1000" loading="lazy">
          </picture>
          {feature_title} <span aria-hidden="true">↗</span>
        </a>
        <div class="storefront-menu-service">
          <a class="storefront-mobile" href="{cfg['delivery_url']}">{cfg['delivery_label']}</a>
          <a href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
          <a href="{cfg['wa_url']}" target="_blank" rel="noopener">WhatsApp</a>
          <div class="storefront-menu-languages storefront-mobile" role="group" aria-label="{cfg['lang_select_label']}">
            <a href="{ru_url}" hreflang="ru"{ru_active} onclick="localStorage.setItem('lang','ru')">RU</a>
            <a href="{kk_url}" hreflang="kk"{kk_active} onclick="localStorage.setItem('lang','kk')">KZ</a>
            <a href="{uz_url}" hreflang="uz"{uz_active} onclick="localStorage.setItem('lang','uz')">UZ</a>
          </div>
        </div>
      </div>"""


def render_storefront_menu(lang: str = "ru", lang_urls: dict = None) -> str:
    """Генерирует полный контейнер nav#storefront-menu, содержащий как десктопное, так и мобильное меню."""
    desktop_html = render_desktop_menu_inner_html(lang, lang_urls)
    mobile_html = render_mobile_menu_html(lang, lang_urls)
    menu_aria = "Разделы каталога" if lang == "ru" else ("Каталог бөлімдері" if lang == "kk" else "Katalog bo‘limlari")

    return f"""    <div class="storefront-menu-backdrop" hidden></div>
    <nav id="storefront-menu" class="storefront-menu" aria-label="{menu_aria}" hidden>
{desktop_html}
{mobile_html}
    </nav>"""


def render_full_storefront_header(lang: str = "ru", lang_urls: dict = None) -> str:
    """Генерирует полную разметку header.storefront-header со всеми дочерними блоками."""
    cfg = MENU_DATA.get(lang, MENU_DATA["ru"])
    if not lang_urls:
        lang_urls = {"ru": "/", "kk": "/kz/", "uz": "/uz/"}

    ru_active = ' class="active"' if lang == "ru" else ""
    kk_active = ' class="active"' if lang == "kk" else ""
    uz_active = ' class="active"' if lang == "uz" else ""

    ru_url = lang_urls.get("ru", "/")
    kk_url = lang_urls.get("kk", "/kz/")
    uz_url = lang_urls.get("uz", "/uz/")

    menu_block = render_storefront_menu(lang, lang_urls)

    return f"""  <header class="storefront-header">
    <div class="nav">
      <div class="storefront-nav-start">
        <button id="burger" class="storefront-menu-toggle" type="button" aria-expanded="false" aria-controls="storefront-menu">
          <span class="storefront-desktop">{cfg['catalog_text']}</span>
          <span class="storefront-mobile">{cfg['menu_text']}</span>
        </button>
        <noscript><a href="{cfg['all_catalog_url']}">{cfg['catalog_text']}</a></noscript>
        <a class="storefront-desktop" href="{cfg['delivery_url']}">{cfg['delivery_top_text']}</a>
      </div>
      <a class="brand" href="{cfg['home_url']}" aria-label="Livi Jewelry">LIVI JEWELRY</a>
      <div class="nav-actions">
        <a href="{cfg['search_url']}" class="header-search-btn" aria-label="{cfg['search_label']}">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </a>
        <nav class="header-lang-links" aria-label="{cfg['lang_select_label']}">
          <a href="{ru_url}" hreflang="ru"{ru_active} onclick="localStorage.setItem('lang','ru')">RU</a>
          <a href="{kk_url}" hreflang="kk"{kk_active} onclick="localStorage.setItem('lang','kk')">KZ</a>
          <a href="{uz_url}" hreflang="uz"{uz_active} onclick="localStorage.setItem('lang','uz')">UZ</a>
        </nav>
        <a class="cart-link" href="{cfg['cart_url']}" aria-label="{cfg['cart_label']}">
          <span data-i18n="nav.cart">{cfg['cart_text']}</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
      </div>
    </div>

{menu_block}
  </header>"""


if __name__ == "__main__":
    print("Testing generate_mobile_menu.py...")
    ru_menu = render_mobile_menu_html("ru")
    kk_menu = render_mobile_menu_html("kk")
    uz_menu = render_mobile_menu_html("uz")
    print(f"RU mobile menu length: {len(ru_menu)} chars")
    print(f"KZ mobile menu length: {len(kk_menu)} chars")
    print(f"UZ mobile menu length: {len(uz_menu)} chars")
    print("Full header sample:")
    print(render_full_storefront_header("ru")[:300] + "...")
