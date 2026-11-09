#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Livi Jewelry — Programmatic SEO Hub Generator (generate_seo_hubs.py)
Generates static indexable HTML landing pages for 21 stone/style clusters:
- 18 thematic hubs (ALL_HUBS)
- 3 core category hubs (EXISTING_HUBS: kolye, braslety, sergi)
- 21 corresponding Kazakh hub landing pages in /kz/
Enforces Schema.org ItemList with aggregateRating and review for every Product,
eliminates mpn, ensures clean alt text, and sets bidirectional hreflang links.
"""

import os
import re
import json
import html
import time

BASE_URL = "https://livijewelry.kz"
PRODUCTS_FILE = "products.json"
AW_CONV_LABEL = "AW-16793974126/MuJ_CObHup8bEO7q_sc-"


def safe_write_text(file_path: str, content: str, retries: int = 5, delay: float = 0.15) -> None:
    """Writes text to file with retry logic to avoid transient Windows file lock issues (Errno 22 / PermissionError)."""
    parent_dir = os.path.dirname(os.path.abspath(file_path))
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    for attempt in range(retries):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return
        except OSError:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise

RU_FOOTER_HTML = """  <footer id="contact" class="site-footer">
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
  </footer>"""

KZ_FOOTER_HTML = """  <footer id="contact" class="site-footer">
    <div class="wrap">
      <div class="footer-top">
        <div class="footer-brand">
          <h3>LIVI JEWELRY</h3>
          <p class="footer-tagline">Табиғи інжу мен асыл минералдардан қолдан жасалған авторлық әшекейлер.</p>
          <div class="footer-contacts">
            <div class="footer-contact-item">
              <span class="contact-label">Мекенжай:</span>
              <span>Қабанбай батыр даңғылы, 43, Астана қ.</span>
              <a href="https://maps.app.goo.gl/yrLFpFFKjz9kE1GHA" target="_blank" rel="noopener" class="footer-map-link">Google Картадағы бағыт →</a>
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
              <span class="contact-label">Жұмыс уақыты:</span>
              <span>Күн сайын 11:00–17:00</span>
            </div>
          </div>
          <div class="kaspi-badge">
            <span class="kaspi-icon">●</span>
            <span>Kaspi төлемі (Kaspi Pay · QR)</span>
          </div>
        </div>

        <div class="footer-columns-grid">
          <div class="footer-col">
            <h4 class="footer-col-title">Алқалар мен сотуарлар</h4>
            <ul class="footer-col-links">
              <li><a href="/kz/kolye-iz-zhemchuga.html">Інжу алқалар</a></li>
              <li><a href="/kz/sotuary-iz-zhemchuga.html">Інжу сотуарлар</a></li>
              <li><a href="/kz/chokery-iz-naturalnyh-kamney.html">Табиғи тастардан чокерлер</a></li>
              <li><a href="/kz/tsepi-s-barochnym-zhemchugom.html">Інжу шынжырлар</a></li>
              <li><a href="/kz/ukrasheniya-iz-barochnogo-zhemchuga.html">Барокко інжуі</a></li>
              <li><a href="/kz/ukrasheniya-iz-zhemchuga-mayorka.html">Майорка інжуі</a></li>
            </ul>
          </div>

          <div class="footer-col">
            <h4 class="footer-col-title">Сырғалар мен жиынтықтар</h4>
            <ul class="footer-col-links">
              <li><a href="/kz/sergi-iz-zhemchuga.html">Інжу сырғалар</a></li>
              <li><a href="/kz/braslety-iz-zhemchuga.html">Інжу білезіктер</a></li>
              <li><a href="/kz/komplekty-ukrasheniy.html">Әшекей жиынтықтары</a></li>
              <li><a href="/kz/koltsa-i-garnitury-iz-kamney.html">Сақиналар мен гарнитурлар</a></li>
              <li><a href="/kz/shop.html">Барлық каталог</a></li>
            </ul>
          </div>

          <div class="footer-col">
            <h4 class="footer-col-title">Табиғи тастар</h4>
            <ul class="footer-col-links">
              <li><a href="/kz/ukrasheniya-iz-malahita.html">Малахит және нефрит</a></li>
              <li><a href="/kz/ukrasheniya-iz-ametista.html">Аметист</a></li>
              <li><a href="/kz/ukrasheniya-iz-granata.html">Анар тас (гранат)</a></li>
              <li><a href="/kz/ukrasheniya-iz-rozovogo-kvarca.html">Қызғылт кварц</a></li>
              <li><a href="/kz/ukrasheniya-iz-biryuzy.html">Табиғи фируза</a></li>
              <li><a href="/kz/ukrasheniya-iz-gornogo-hrustalya.html">Тау хрусталі</a></li>
            </ul>
          </div>

          <div class="footer-col">
            <h4 class="footer-col-title">Минералдар мен сирек тастар</h4>
            <ul class="footer-col-links">
              <li><a href="/kz/ukrasheniya-iz-tigrovogo-glaza.html">Жолбарыс көзі</a></li>
              <li><a href="/kz/ukrasheniya-iz-koralla-i-yashmy.html">Маржан мен яшма</a></li>
              <li><a href="/kz/ukrasheniya-iz-lazurita.html">Табиғи лазурит</a></li>
              <li><a href="/kz/ukrasheniya-iz-lunnogo-kamnya.html">Ай тасы</a></li>
              <li><a href="/kz/ukrasheniya-iz-gematita.html">Гематит</a></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div class="footer-bottom-copy">
          © <span id="year">2026</span> Livi Jewelry. Барлық құқықтар қорғалған.
        </div>
        <div class="footer-bottom-links">
          <a href="/kz/delivery.html">Жеткізу және төлем</a>
          <a href="/kz/terms.html">Оферта</a>
          <a href="/kz/privacy.html">Құпиялылық</a>
          <a href="/">Русский</a>
          <a href="/uz/">O‘zbekcha</a>
        </div>
      </div>
    </div>
  </footer>"""

UZ_FOOTER_HTML = """  <footer id="contact" class="site-footer">
    <div class="wrap">
      <div class="footer-top">
        <div class="footer-brand">
          <h3>LIVI JEWELRY</h3>
          <p class="footer-tagline">Tabiiy marvarid va qimmatbaho minerallardan qo‘lda yasalgan mualliflik zargarlik buyumlari.</p>
          <div class="footer-contacts">
            <div class="footer-contact-item">
              <span class="contact-label">Manzil:</span>
              <span>Qabanbay botir shoh ko‘chasi, 43, Ostona sh.</span>
              <a href="https://maps.app.goo.gl/yrLFpFFKjz9kE1GHA" target="_blank" rel="noopener" class="footer-map-link">Google Xaritalardagi yo‘nalish →</a>
            </div>
            <div class="footer-contact-item">
              <span class="contact-label">Telefon:</span>
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
              <span class="contact-label">Ish vaqti:</span>
              <span>Har kuni 11:00–17:00</span>
            </div>
          </div>
          <div class="kaspi-badge">
            <span class="kaspi-icon">●</span>
            <span>Kaspi orqali to‘lov</span>
          </div>
        </div>

        <div class="footer-columns-grid">
          <div class="footer-col">
            <h4 class="footer-col-title">Marjonlar va sotuarlar</h4>
            <ul class="footer-col-links">
              <li><a href="/uz/kolye-iz-zhemchuga.html">Marvarid marjonlar</a></li>
              <li><a href="/uz/sotuary-iz-zhemchuga.html">Marvarid sotuarlar</a></li>
              <li><a href="/uz/chokery-iz-naturalnyh-kamney.html">Toshlardan chokerlar</a></li>
              <li><a href="/uz/tsepi-s-barochnym-zhemchugom.html">Marvaridli zanjirlar</a></li>
              <li><a href="/uz/ukrasheniya-iz-barochnogo-zhemchuga.html">Barokko marvaridi</a></li>
              <li><a href="/uz/ukrasheniya-iz-zhemchuga-mayorka.html">Mayorka marvaridi</a></li>
            </ul>
          </div>

          <div class="footer-col">
            <h4 class="footer-col-title">Sirg‘alar va to‘plamlar</h4>
            <ul class="footer-col-links">
              <li><a href="/uz/sergi-iz-zhemchuga.html">Marvarid sirg‘alar</a></li>
              <li><a href="/uz/braslety-iz-zhemchuga.html">Marvarid bilaguzuklar</a></li>
              <li><a href="/uz/komplekty-ukrasheniy.html">Taqinchoq to‘plamlari</a></li>
              <li><a href="/uz/koltsa-i-garnitury-iz-kamney.html">Uzuklar va garniturlar</a></li>
              <li><a href="/uz/shop.html">Barcha katalog</a></li>
            </ul>
          </div>

          <div class="footer-col">
            <h4 class="footer-col-title">Tabiiy toshlar</h4>
            <ul class="footer-col-links">
              <li><a href="/uz/ukrasheniya-iz-malahita.html">Malaxit va nefrit</a></li>
              <li><a href="/uz/ukrasheniya-iz-ametista.html">Ametist</a></li>
              <li><a href="/uz/ukrasheniya-iz-granata.html">Granat</a></li>
              <li><a href="/uz/ukrasheniya-iz-rozovogo-kvarca.html">Pushti kvars</a></li>
              <li><a href="/uz/ukrasheniya-iz-biryuzy.html">Tabiiy feruza</a></li>
              <li><a href="/uz/ukrasheniya-iz-gornogo-hrustalya.html">Tog‘ billuri</a></li>
            </ul>
          </div>

          <div class="footer-col">
            <h4 class="footer-col-title">Minerallar va noyob toshlar</h4>
            <ul class="footer-col-links">
              <li><a href="/uz/ukrasheniya-iz-tigrovogo-glaza.html">Yo‘lbars ko‘zi</a></li>
              <li><a href="/uz/ukrasheniya-iz-koralla-i-yashmy.html">Marjon va yashma</a></li>
              <li><a href="/uz/ukrasheniya-iz-lazurita.html">Tabiiy lazurit</a></li>
              <li><a href="/uz/ukrasheniya-iz-lunnogo-kamnya.html">Oy toshi</a></li>
              <li><a href="/uz/ukrasheniya-iz-gematita.html">Gematit</a></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div class="footer-bottom-copy">
          © <span id="year">2026</span> Livi Jewelry. Barcha huquqlar himoyalangan.
        </div>
        <div class="footer-bottom-links">
          <a href="/uz/delivery.html">Yetkazib berish va to‘lov</a>
          <a href="/uz/terms.html">Ommaviy oferta</a>
          <a href="/uz/privacy.html">Maxfiylik siyosati</a>
          <a href="/">Русский</a>
          <a href="/kz/">Қазақша</a>
        </div>
      </div>
    </div>
  </footer>"""

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

ALL_HUBS = [
    {
        "slug": "komplekty-ukrasheniy.html",
        "chip_label": "Комплекты украшений",
        "custom_title": "Комплекты украшений из камней и жемчуга | Livi Jewelry",
        "custom_meta_desc": "Комплекты украшений из натуральных камней и жемчуга ручной работы. Сеты колье, браслетов и серег. Подарочная упаковка, доставка по Казахстану.",
        "h1": "Комплекты украшений из натуральных камней и жемчуга ручной работы",
        "title_cluster": "комплекты украшений из натуральных камней и жемчуга",
        "breadcrumb": "Комплекты украшений",
        "eyebrow": "Haute Joaillerie • Ювелирные сеты",
        "lead": "Авторские комплекты украшений и сеты из натурального жемчуга, аметиста, малахита, бирюзы и розового кварца. Каждое изделие из комплекта можно приобрести полным сетом или по отдельности с индивидуальной подгонкой длины.",
        "filter_type": "category",
        "filter_val": "Sets",
        "stone_name_gen": "натуральных камней и жемчуга",
        "stone_name_prep": "комплектах украшений",
        "seo_title": "Эксклюзивные комплекты украшений ручной сборки в ателье Livi Jewelry",
        "seo_p1": "Ювелирный комплект из натуральных минералов и культивированного жемчуга — это безупречно выверенный ансамбль, в котором колье, браслет, серьги и кольцо гармонируют по оттенку, калибру камней и стилю фурнитуры. В мастерской Livi Jewelry (Астана, Казахстан) мы собираем комплекты вручную, тщательно отбирая каждый минерал по чистоте рисунка и глубине природного блеска. Вы можете приобрести как готовый сет целиком, так и отдельные его элементы.",
        "seo_p2": "Каждое украшение создается на ювелирном тросике высокой прочности с использованием гипоаллергенной фурнитуры премиум-класса (стойкое родирование или позолота 18K). Все комплекты упаковываются в фирменную подарочную шкатулку и доставляются курьером день в день по Астане или экспресс-службой СДЭК в Алматы и любой город Казахстана за 1–3 рабочих дня."
    },
    {
        "slug": "chokery-iz-naturalnyh-kamney.html",
        "chip_label": "Чокеры из камней",
        "h1": "Чокеры из натуральных камней и жемчуга — доставка по Казахстану",
        "title_cluster": "чокеры из натуральных камней и жемчуга",
        "breadcrumb": "Чокеры из натуральных камней",
        "eyebrow": "Haute Joaillerie • Изящный акцент на ключицах",
        "lead": "Купить чокеры из натуральных камней и жемчуга ручной работы в Алматы и Астане. Утонченные короткие колье, гранат, лазурит, флюорит, подарочная упаковка и регулировка длины.",
        "filter_type": "choker",
        "filter_val": ["чокер", "колье из"],
        "stone_name_gen": "натуральных самоцветов и жемчуга",
        "stone_name_prep": "чокерах из камней",
        "seo_title": "Чокеры из натуральных камней и жемчуга — авторская коллекция",
        "seo_p1": "Чокер из натуральных камней — главный ювелирный тренд, который деликатно подчеркивает линию шеи и ключицы. В мастерской Livi Jewelry вы можете купить чокер в Алматы с доставкой до двери или самовывозом. В коллекции представлены прилегающие чокеры и короткие колье из граненого граната, благородного лазурита, полупрозрачного флюорита, тигрового глаза и барочного жемчуга.",
        "seo_p2": "В ателье Livi Jewelry каждое изделие собирается вручную в единственном экземпляре или малой серией. Мы комплектуем чокеры удобной удлинительной цепочкой (+5 см) и надежными карабинами с родиевым или позолоченным покрытием, которое не темнеет и не вызывает аллергии. Доступна индивидуальная коррекция длины точно по обхвату вашей шеи и быстрая доставка СДЭК по всему Казахстану."
    },
    {
        "slug": "sotuary-iz-zhemchuga.html",
        "chip_label": "Сотуары",
        "h1": "Сотуары из натурального жемчуга и колье-галстуки — доставка по Казахстану",
        "title_cluster": "сотуары из натурального жемчуга и колье-галстуки",
        "breadcrumb": "Сотуары из жемчуга и камней",
        "eyebrow": "Haute Joaillerie • Удлиненный силуэт",
        "lead": "Купить авторские сотуары из натурального жемчуга и камней ручной работы в Алматы и Астане. Утонченные длинные колье-галстуки, позолота 18K и родий, быстрая доставка по Казахстану.",
        "filter_type": "lariat",
        "filter_val": ["Lariats", "сотуар"],
        "stone_name_gen": "натурального жемчуга, агата и граната",
        "stone_name_prep": "сотуарах и колье-галстуках",
        "seo_title": "Сотуары из натурального жемчуга и колье-галстуки — авторская коллекция",
        "seo_p1": "Сотуар из жемчуга — культовое удлиненное украшение эпохи ар-деко, которое триумфально вернулось в современную моду Haute Joaillerie. Длинные нити из натурального жемчуга, черного агата и винного граната с изящными подвесками визуально стройнят фигуру и акцентируют декольте. В мастерской Livi Jewelry вы можете купить сотуар из жемчуга в Алматы, Астане и с быстрой доставкой курьером в любой город Казахстана.",
        "seo_p2": "Мастера Livi Jewelry вручную калибруют баланс веса и гибкость каждого сотуара, чтобы нить красиво струилась и не перекручивалась при носке. По вашему желанию мы можем скорректировать общую длину сотуара, заменить оттенок гипоаллергенной фурнитуры на родий или позолоту и отправить заказ в фирменной подарочной коробке по Астане, Алматы и всему Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-barochnogo-zhemchuga.html",
        "chip_label": "Барочный жемчуг",
        "h1": "Украшения из барочного жемчуга ручной работы",
        "title_cluster": "украшения из барочного жемчуга",
        "breadcrumb": "Барочный жемчуг",
        "eyebrow": "Природная уникальность • Baroque Pearl",
        "lead": "Колье, цепи, браслеты и серьги с крупным натуральным барочным жемчугом неповторимых органических форм. Плотный перламутровый слой с радужным люстром и премиальная фурнитура.",
        "filter_type": "stone",
        "filter_val": ["барочн"],
        "stone_name_gen": "натурального барочного жемчуга",
        "stone_name_prep": "украшениях из барочного жемчуга",
        "seo_title": "Свойства и ценность натурального барочного жемчуга в украшениях Livi Jewelry",
        "seo_p1": "Барочный жемчуг (Baroque Pearl) — это редкие культивированные жемчужины свободной асимметричной формы, созданной самой природой без вмешательства токарной обработки. Каждая барочная жемчужина в ателье Livi Jewelry проходит строгую ручную селекцию по толщине перламутра, интенсивности радужного сияния (люстра) и выразительности рельефа. Благодаря уникальной геометрии второго такого же украшения не существует в мире.",
        "seo_p2": "Мы сочетаем крупный барочный жемчуг с классическими жемчужными нитями, горным хрусталем, а также массивными позолоченными и родированными цепями. Каждое изделие собирается вручную под ваш индивидуальный размер (от 38 до 45+ см для колье и от 15 до 19 см для браслетов) и доставляется в фирменной шкатулке Livi Jewelry по Астане и всему Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-gematita.html",
        "chip_label": "Гематит",
        "h1": "Украшения из натурального гематита ручной работы",
        "title_cluster": "украшения из гематита",
        "breadcrumb": "Украшения из гематита",
        "eyebrow": "Благородный металлик • Натуральный минерал",
        "lead": "Авторские колье, чокеры и комплекты с граненым натуральным гематитом, тигровым глазом и нефритом. Глубокий зеркально-графитовый блеск и безупречная геометрия ручной сборки.",
        "filter_type": "stone",
        "filter_val": ["гематит"],
        "stone_name_gen": "натурального гематита",
        "stone_name_prep": "украшениях из гематита",
        "seo_title": "Натуральный гематит в авторских колье и комплектах Livi Jewelry",
        "seo_p1": "Природный гематит ценится в высоком ювелирном искусстве за свой неповторимый зеркально-стальной отлив, приятную прохладу и благородную тяжесть. Граненые бусины и разделители из гематита создают выразительный контраст в сочетании с теплым тигровым глазом, изумрудным нефритом и перламутровым жемчугом, придавая украшению современный графичный характер.",
        "seo_p2": "В мастерской Livi Jewelry гематит проходит деликатную полировку, сохраняя стойкий металлический блеск на долгие годы. Мы используем гипоаллергенную фурнитуру с родированием и позолотой и бережно отправляем заказы курьером по Астане и службой СДЭК в Алматы и все регионы Казахстана."
    },
    {
        "slug": "ukrasheniya-iz-malahita.html",
        "chip_label": "Малахит и Нефрит",
        "h1": "Украшения из натурального малахита и нефрита ручной работы",
        "title_cluster": "украшения из малахита и нефрита",
        "breadcrumb": "Малахит и Нефрит",
        "eyebrow": "Изумрудная классика • Природный узор",
        "lead": "Изысканные браслеты, колье и комплекты из натурального малахита с уникальным ленточным рисунком, зеленого нефрита и позолоченной фурнитуры. Ручная селекция камней в ателье Livi Jewelry.",
        "filter_type": "stone",
        "filter_val": ["малахит", "нефрит"],
        "stone_name_gen": "натурального малахита и нефрита",
        "stone_name_prep": "украшениях из малахита и нефрита",
        "seo_title": "Украшения из природного малахита и нефрита — изумрудный акцент Livi Jewelry",
        "seo_p1": "Натуральный малахит и зеленый нефрит — статусные благородные самоцветы. В палитре Livi Jewelry малахит и нефрит сочетаются с теплым сиянием позолоченной фурнитуры и натуральным жемчугом, создавая роскошный образ в стиле высоких ювелирных домов.",
        "seo_p2": "Каждая бусина малахита и нефрита отбирается мастером вручную. Мы упаковываем изделие в подарочный футляр Livi Jewelry и обеспечиваем быструю доставку по Астане, Алматы и всему Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-ametista.html",
        "chip_label": "Аметист и Флюорит",
        "h1": "Украшения из натурального аметиста и флюорита ручной работы",
        "title_cluster": "украшения из аметиста и флюорита",
        "breadcrumb": "Аметист и Флюорит",
        "eyebrow": "Королевский фиолетовый • Природный кварц",
        "lead": "Комплекты, колье, серьги и браслеты из натурального лавандового аметиста и мятного флюорита в дуэте с жемчугом и розовым кварцем.",
        "filter_type": "stone",
        "filter_val": ["аметист", "флюорит"],
        "stone_name_gen": "натурального аметиста и флюорита",
        "stone_name_prep": "украшениях из аметиста и флюорита",
        "seo_title": "Авторские украшения из натурального аметиста и флюорита в ателье Livi Jewelry",
        "seo_p1": "Натуральный аметист и полупрозрачный флюорит — благородные минералы, которые превосходно преломляют свет. Прозрачные и полупрозрачные грани аметиста великолепно играют в авторских сочетаниях с нежным розовым кварцем и классическим речным жемчугом.",
        "seo_p2": "В ателье Livi Jewelry вы можете купить комплекты, колье, серьги и броши-булавки из подлинного природного аметиста и флюорита ручной сборки с быстрой доставкой по всему Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-granata.html",
        "chip_label": "Гранат и Агат",
        "h1": "Украшения из натурального граната и агата ручной работы",
        "title_cluster": "украшения из граната и агата",
        "breadcrumb": "Гранат и Агат",
        "eyebrow": "Винный бархат • Граненый пироп и альмандин",
        "lead": "Колье, сотуары и комплекты из натурального граненого граната насыщенного бордово-винного оттенка в сочетании с черным агатом и перламутровым жемчугом.",
        "filter_type": "stone",
        "filter_val": ["гранат", "агат"],
        "stone_name_gen": "натурального граната и черного агата",
        "stone_name_prep": "украшениях из граната и агата",
        "seo_title": "Колье, сотуары и сеты из натурального граната и агата — Livi Jewelry",
        "seo_p1": "Природный гранат завораживает глубоким винно-рубиновым цветом, который вспыхивает яркими искрами при попадании света на ювелирные грани. В коллекции Livi Jewelry гранат представлен в сольных моно-колье и в драматичных контрастных композициях с бархатным черным агатом и белоснежным жемчугом.",
        "seo_p2": "Мы используем только натуральный граненый гранат высокой чистоты и собираем каждое украшение вручную на прочном ювелирном тросике с надежными гипоаллергенными замками. Доставка СДЭК по всему Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-rozovogo-kvarca.html",
        "chip_label": "Розовый кварц",
        "h1": "Украшения из розового кварца ручной работы",
        "title_cluster": "украшения из розового кварца",
        "breadcrumb": "Розовый кварц",
        "eyebrow": "Пудровая нежность • Натуральный минерал",
        "lead": "Нежные колье, сеты и серьги из натурального розового кварца, речного жемчуга и аметиста. Освежают тон кожи и создают романтичный женственный образ.",
        "filter_type": "stone",
        "filter_val": ["розового кварца", "розовый кварц", "клубнич"],
        "stone_name_gen": "натурального розового кварца",
        "stone_name_prep": "украшениях из розового кварца",
        "seo_title": "Украшения из натурального розового кварца и жемчуга в Livi Jewelry",
        "seo_p1": "Натуральный розовый кварц — воплощение нежности и утонченной женственности. Его мягкий полупрозрачный пудровый оттенок освежает цвет лица. В комбинации с натуральным жемчугом и аметистом розовый кварц образует изысканную пастельную палитру.",
        "seo_p2": "Мастера Livi Jewelry вручную отбирают бусины розового кварца, дополняя их стойкой фурнитурой. Каждое колье и комплект можно адаптировать под индивидуальную длину и приобрести как полным сетом, так и по отдельности."
    },
    {
        "slug": "ukrasheniya-iz-biryuzy.html",
        "chip_label": "Бирюза",
        "h1": "Украшения из натуральной бирюзы ручной работы",
        "title_cluster": "украшения из натуральной бирюзы",
        "breadcrumb": "Бирюза",
        "eyebrow": "Небесная лазурь • Природная бирюза",
        "lead": "Полные ювелирные комплекты, колье, браслеты и серьги из натуральной бирюзы с благородной природной фактурой. Яркий статусный акцент в любое время года.",
        "filter_type": "stone",
        "filter_val": ["бирюз"],
        "stone_name_gen": "натуральной бирюзы",
        "stone_name_prep": "украшениях из бирюзы",
        "seo_title": "Комплекты и колье из натуральной бирюзы ручной работы — Livi Jewelry",
        "seo_p1": "Натуральная бирюза — камень с тысячелетней историей, который почитается как талисман удачи и благополучия. Выразительный небесно-голубой оттенок природной бирюзы мгновенно притягивает взгляды и великолепно оттеняет любой цветотип внешности.",
        "seo_p2": "В каталоге Livi Jewelry представлены роскошные сеты и комплекты из натуральной бирюзы (колье, браслет, серьги, кольцо), которые можно купить полным комплектом или выбрать отдельные изделия. Доставка по Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-gornogo-hrustalya.html",
        "chip_label": "Горный хрусталь",
        "h1": "Украшения из горного хрусталя и кварца ручной работы",
        "title_cluster": "украшения из горного хрусталя и кварца",
        "breadcrumb": "Горный хрусталь и кварц",
        "eyebrow": "Кристальная чистота • Природный кварц",
        "lead": "Премиальные многослойные колье и украшения из чистого горного хрусталя, ювелирных цирконов, флюорита и натурального жемчуга.",
        "filter_type": "stone",
        "filter_val": ["хрустал", "кварц", "циркон"],
        "stone_name_gen": "горного хрусталя и природного кварца",
        "stone_name_prep": "украшениях из горного хрусталя",
        "seo_title": "Колье и украшения из горного хрусталя ручной сборки в Livi Jewelry",
        "seo_p1": "Горный хрусталь — кристально чистая прозрачная разновидность природного кварца. Его ледяной блеск и высокая светопреломляющая способность создают эффект легкого сияющего ореола. В сочетании с натуральным жемчугом горный хрусталь придает колье воздушность и торжественную утонченность.",
        "seo_p2": "Каждое украшение с горным хрусталем собирается вручную с использованием надежной гипоаллергенной фурнитуры (родий или позолота). Быстрая доставка по Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-lunnogo-kamnya.html",
        "chip_label": "Лунный камень и Перламутр",
        "h1": "Украшения из лунного камня и перламутра ручной работы",
        "title_cluster": "украшения из лунного камня и перламутра",
        "breadcrumb": "Лунный камень и Перламутр",
        "eyebrow": "Шелковое сияние • Перламутр и адуляр",
        "lead": "Утонченные авторские колье, чокеры и комплекты с переливчатым натуральным перламутром, органическим жемчугом Майорка и полупрозрачными минералами.",
        "filter_type": "stone",
        "filter_val": ["лунн", "перламутр", "майорка", "хрустал"],
        "stone_name_gen": "лунного камня, перламутра и жемчуга",
        "stone_name_prep": "украшениях из лунного камня и перламутра",
        "seo_title": "Украшения с перламутром и лунным сиянием от мастерской Livi Jewelry",
        "seo_p1": "Украшения с натуральным перламутром, лунным камнем и культивированным жемчугом славятся мягким иризирующим свечением — эффектом внутреннего голубовато-жемчужного перелива. Такие изделия универсальны: они гармоничны днем и благородны вечером.",
        "seo_p2": "В мастерской Livi Jewelry каждое колье и комплект собираются вручную с вниманием к малейшим нюансам оттенка. Фирменная подарочная упаковка и быстрая доставка СДЭК по всему Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-zhemchuga-mayorka.html",
        "chip_label": "Жемчуг Майорка",
        "h1": "Украшения и колье из жемчуга Майорка ручной работы",
        "title_cluster": "украшения и колье из жемчуга Майорка",
        "breadcrumb": "Жемчуг Майорка",
        "eyebrow": "Испанский шарм • Жемчуг Майорка",
        "lead": "Изысканные колье, комплекты и серьги из органического жемчуга Майорка с идеальной сферической геометрией и глубоким зеркальным блеском. Ручная селекция и стойкая позолоченная фурнитура.",
        "filter_type": "stone",
        "filter_val": ["майорк"],
        "stone_name_gen": "органического жемчуга Майорка",
        "stone_name_prep": "украшениях из жемчуга Майорка",
        "seo_title": "Украшения из жемчуга Майорка — совершенный блеск и ручная работа Livi Jewelry",
        "seo_p1": "Органический жемчуг Майорка создается по многовековой испанской технологии нанесения множества слоев натуральной жемчужной эссенции. Каждая бусина обретает зеркальную гладкость, устойчивость к выцветанию и завораживающее внутреннее свечение. В ателье Livi Jewelry мы объединяем Майорку с расписной керамикой, позолотой 18K и ювелирными элементами ручной сборки.",
        "seo_p2": "Каждое колье и комплект комплектуются надежными гипоаллергенными замочками. Мы упаковываем украшение в подарочную шкатулку Livi Jewelry и доставляем курьером в Астане день в день или экспресс-службой СДЭК по Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-tigrovogo-glaza.html",
        "chip_label": "Тигровый глаз и Жадеит",
        "h1": "Украшения и колье из тигрового глаза и жадеита ручной работы",
        "title_cluster": "украшения из тигрового глаза и жадеита",
        "breadcrumb": "Тигровый глаз и Жадеит",
        "eyebrow": "Шелковая иризация • Природные минералы",
        "lead": "Авторские колье, чокеры, сеты и серьги из шелковистого тигрового глаза, природного жадеита и граненого гематита. Сильный характер и благородное сияние.",
        "filter_type": "stone",
        "filter_val": ["тигров", "жадеит"],
        "stone_name_gen": "натурального тигрового глаза и жадеита",
        "stone_name_prep": "украшениях из тигрового глаза и жадеита",
        "seo_title": "Украшения из тигрового глаза и жадеита — энергия и эстетика Livi Jewelry",
        "seo_p1": "Тигровый глаз завораживает своим золотисто-янтарным переливом и шелковистой иризацией, а зеленый жадеит привносит ноту спокойствия и природного благородства. В авторских украшениях Livi Jewelry эти камни подчеркнуты контрастными вставками из гематита и позолоты, создавая эффектный геометрический рисунок.",
        "seo_p2": "Все изделия собираются вручную на прочном ювелирном тросике. Мастер упакует заказ в фирменный бархатный футляр и отправит курьером по Астане или СДЭК в Алматы и все регионы РК."
    },
    {
        "slug": "ukrasheniya-iz-koralla-i-yashmy.html",
        "chip_label": "Коралл и Яшма",
        "h1": "Украшения из натурального коралла и яшмы ручной работы",
        "title_cluster": "украшения из коралла и яшмы",
        "breadcrumb": "Коралл и Яшма",
        "eyebrow": "Природное тепло • Коралл и Яшма",
        "lead": "Колоритные комплекты, колье, браслеты и серьги из теплого терракотового коралла и фактурной пейзажной яшмы. Натуральные природные оттенки и ручная сборка.",
        "filter_type": "stone",
        "filter_val": ["коралл", "яшм"],
        "stone_name_gen": "натурального коралла и яшмы",
        "stone_name_prep": "украшениях из коралла и яшмы",
        "seo_title": "Украшения из натурального коралла и пейзажной яшмы в ателье Livi Jewelry",
        "seo_p1": "Природный коралл терракотово-красного оттенка в дуэте с пейзажной яшмой воплощает тепло земли и солнца. Неповторимый природный рисунок каждого среза яшмы превращает любое украшение в подлинный артефакт. Комплекты великолепно гармонируют с натуральными тканями — льном, шелком, денимом и кашемиром.",
        "seo_p2": "В Livi Jewelry вы можете приобрести как полный комплект (колье, браслет, серьги), так и любой элемент по отдельности. Надежная фурнитура, подарочная коробка и быстрая доставка по Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-lazurita.html",
        "chip_label": "Лазурит и Авантюрин",
        "h1": "Украшения из натурального лазурита и авантюрина ручной работы",
        "title_cluster": "украшения из натурального лазурита и авантюрина",
        "breadcrumb": "Лазурит и Авантюрин",
        "eyebrow": "Королевский ультрамарин • Лазурит и Авантюрин",
        "lead": "Роскошные колье, комплекты и сеты из королевского синего лазурита с золотистыми искрами пирита и искристого зеленого авантюрина в сочетании с натуральным жемчугом.",
        "filter_type": "stone",
        "filter_val": ["лазурит", "авантюрин"],
        "stone_name_gen": "натурального лазурита и авантюрина",
        "stone_name_prep": "украшениях из лазурита и авантюрина",
        "seo_title": "Украшения из натурального лазурита и авантюрина — авторский дизайн Livi Jewelry",
        "seo_p1": "Натуральный ультрамариновый лазурит с древности считался камнем монархов и высшей знати. Золотистые крупицы пирита внутри лазурита перекликаются с мерцающими чешуйками зеленого авантюрина и шелковым сиянием речного жемчуга. Это сочетание придает украшениям королевскую стать и непревзойденную глубину цвета.",
        "seo_p2": "Каждое колье создается вручную в единственном экземпляре или малой серией. Мы устанавливаем стойкую гипоаллергенную фурнитуру и доставляем в фирменной подарочной коробке по Астане и всему Казахстану."
    },
    {
        "slug": "tsepi-s-barochnym-zhemchugom.html",
        "chip_label": "Цепи с жемчугом",
        "h1": "Цепи с барочным жемчугом ручной работы — позолота и родий",
        "title_cluster": "цепи с барочным жемчугом",
        "breadcrumb": "Цепи с барочным жемчугом",
        "eyebrow": "Современный люкс • Chains & Pearls",
        "lead": "Трендовые позолоченные и родированные цепи с акцентным барочным жемчугом каплевидных и свободных форм, стильные сеты «Гранж» и звеньевые браслеты.",
        "filter_type": "chain_pearl",
        "filter_val": ["цепь", "гранж", "позолоченная цепь", "родированная цепь"],
        "stone_name_gen": "барочного жемчуга и звеньевых цепей",
        "stone_name_prep": "цепях с барочным жемчугом",
        "seo_title": "Цепи с крупным барочным жемчугом — трендовые украшения Livi Jewelry",
        "seo_p1": "Контраст массивных фактурных звеньев цепи и нежного органического барочного жемчуга — один из ведущих трендов современной ювелирной моды. Стойкое родиевое или 18-каратное позолоченное покрытие придает цепям безупречный блеск, не тускнеющий со временем.",
        "seo_p2": "В коллекции Livi Jewelry представлены как лаконичные цепи с одиночной барочной жемчужиной, так и дерзкие гранж-модели и комплекты с браслетами. Фирменная упаковка и доставка СДЭК."
    },
    {
        "slug": "koltsa-i-garnitury-iz-kamney.html",
        "chip_label": "Кольца и сеты",
        "h1": "Комплекты с кольцами и булавками из натуральных камней ручной работы",
        "title_cluster": "комплекты с кольцами и булавками из камней",
        "breadcrumb": "Кольца и сеты",
        "eyebrow": "Эксклюзивные сеты • Кольца и броши",
        "lead": "Полные ювелирные сеты с безразмерными кольцами, дизайнерскими булавками-брошами, браслетами и серьгами из натурального аметиста, бирюзы, граната и жемчуга.",
        "filter_type": "rings_pins",
        "filter_val": ["кольц", "булавк"],
        "stone_name_gen": "натуральных камней и жемчуга в комплектах",
        "stone_name_prep": "комплектах с кольцами и булавками",
        "seo_title": "Комплекты с кольцами и брошами-булавками из натуральных камней — Livi Jewelry",
        "seo_p1": "Комплекты с кольцами и акцентными булавками-брошами — это завершенное стилистическое решение. Каждое кольцо имеет удобную регулируемую основу, которая комфортно садится на любой пальчик (размеры 16–19), а дизайнерские булавки эффектно смотрятся на жакетах, трикотаже и головных уборах.",
        "seo_p2": "Каждый элемент комплекта можно заказать как полным сетом, так и по отдельности. Индивидуальная подгонка размеров, гипоаллергенный сплав, подарочный футляр и доставка курьером по Астане или СДЭК по Казахстану."
    }
]

EXISTING_HUBS = [
    ("kolye-iz-zhemchuga.html", "Колье из жемчуга"),
    ("braslety-iz-zhemchuga.html", "Браслеты из жемчуга"),
    ("sergi-iz-zhemchuga.html", "Серьги из жемчуга"),
]

KZ_HUBS_INFO = {
    "kolye-iz-zhemchuga.html": {
        "chip_label": "Інжу алқалар",
        "h1": "Табиғи інжуден жасалған алқалар — қолдан жасалған әшекейлер",
        "custom_title": "Табиғи інжуден жасалған алқалар сатып алу | Livi",
        "custom_meta_desc": "Табиғи інжу мен барокко інжуінен жасалған авторлық алқалар мен чокерлер. 18K алтын жалатылған фурнитура. Қазақстан мен Астанаға жылдам жеткізу.",
        "title_cluster": "інжу алқалар",
        "breadcrumb": "Інжу алқалар",
        "lead": "Табиғи культивацияланған інжуден, барокко інжуінен және Майорка інжуінен қолмен жиналған авторлық алқалар мен чокерлер. Төзімді алтын жалатылған және родийленген фурнитура.",
        "seo_title": "Livi Jewelry шеберханасындағы табиғи інжу алқалар — сапа мен нәзіктік",
        "seo_p1": "Табиғи інжу алқа — кез келген әйел образына ақсүйектік сипат беретін классикалық зергерлік бұйым. Livi Jewelry шеберханасында (Астана, Қазақстан) әрбір інжу түйіршігі жылтыры мен табиғи пішіні бойынша мұқият іріктеледі. Бұйымдар сапалы ювелирлік тросикте жиналып, аллергия тудырмайтын төзімді фурнитурамен жабдықталады.",
        "seo_p2": "Барлық алқалар фирмалық сыйлық қорабына салынып, Астана мен Алматыға және бүкіл Қазақстанға жедел жеткізіледі.",
    },
    "braslety-iz-zhemchuga.html": {
        "chip_label": "Інжу білезіктер",
        "h1": "Табиғи інжу мен тастардан жасалған білезіктер",
        "title_cluster": "інжу білезіктер",
        "breadcrumb": "Інжу білезіктер",
        "lead": "Табиғи інжуден, малахиттен, бирюзадан және аметисттен жасалған нәзік қолдан жасалған білезіктер.",
        "seo_title": "Табиғи інжуден қолдан жасалған білезіктер — Livi Jewelry",
        "seo_p1": "Інжу білезіктер нәзік білектің сұлулығын айшықтап, күнделікті де, кешкі образдарға да үйлесімділік сыйлайды. Біз барокко інжуі мен табиғи минералдарды премиум санаттағы фурнитурамен үйлестіреміз.",
        "seo_p2": "Қазақстанның барлық қалаларына СДЭК арқылы сенімді жеткізу.",
    },
    "sergi-iz-zhemchuga.html": {
        "chip_label": "Інжу сырғалар",
        "h1": "Інжу сырғалар мен әшекейлер жиынтығы",
        "title_cluster": "інжу сырғалар",
        "breadcrumb": "Інжу сырғалар",
        "lead": "Барокко інжуі, анар тас, малахит және аметист сырғалары. Сырғаларды жеке немесе толық жиынтықпен бірге сатып алуға болады.",
        "seo_title": "Табиғи інжу сырғалар — авторлық қолөнер туындылары",
        "seo_p1": "Livi Jewelry шеберханасының сырғалары жеңіл, құлаққа жайлы және гипоаллергенді француз/ағылшын ілмектерімен ерекшеленеді. Күнделікті кигенде де жайлылық сақталады.",
        "seo_p2": "Сырғаларды сәйкес алқа, білезік немесе сақинамен толықтырып, үйлесімді зергерлік ансамбль құруға болады. Сыйлық қаптамасы тегін беріледі.",
    },
    "komplekty-ukrasheniy.html": {
        "chip_label": "Әшекейлер жиынтығы",
        "h1": "Табиғи тастар мен інжуден жасалған әшекейлер жиынтығы",
        "custom_title": "Табиғи тастар мен інжу әшекейлер жиынтығы | Livi",
        "custom_meta_desc": "Табиғи тастар мен інжуден жасалған авторлық әшекейлер жиынтығы. Алқа, білезік және сырғалар сездері. Сыйлық қаптамасы және Қазақстанға жеткізу.",
        "title_cluster": "әшекейлер жиынтығы",
        "breadcrumb": "Әшекейлер жиынтығы",
        "lead": "Табиғи інжу, аметист, малахит, бирюза және қызғылт кварцтан авторлық әшекейлер жиынтығы. Жиынтықты толық немесе әр бұйымды бөлек сатып алуға болады.",
        "seo_title": "Livi Jewelry эксклюзивті қолдан жасалған әшекейлер жиынтықтары",
        "seo_p1": "Зергерлік жиынтық — бұл алқа, білезік, сырға және сақина түсі мен стилі бойынша мінсіз үйлескен кешенді ансамбль. Астанадағы шеберханамызда әрбір жиынтық қолмен іріктеліп жиналады.",
        "seo_p2": "Барлық жиынтықтар берік ювелирлік тросикке жиналады. Сапалы алтын немесе родий жабыны жылдар бойы бастапқы қалпын жоғалтпайды. Қазақстан бойынша экспресс жеткізу.",
    },
    "chokery-iz-naturalnyh-kamney.html": {
        "chip_label": "Тастардан чокерлер",
        "h1": "Табиғи тастар мен інжуден жасалған чокерлер",
        "title_cluster": "табиғи тастардан чокерлер",
        "breadcrumb": "Тастардан чокерлер",
        "lead": "Табиғи анар тас, флюорит, інжу және гематиттен жасалған нәзік қысқа алқалар мен чокерлер. Ұзындықты реттейтін 5 см ұзартқыш тізбек.",
        "seo_title": "Табиғи тастардан жасалған сәнді чокерлер — Livi Jewelry",
        "seo_p1": "Чокер — мойын сызығы мен бұғананы әдемі айшықтайтын қазіргі зергерлік сәннің басты тренді. Қырлы минералдар жарық түскенде көздің жауын алатын жарқырау сыйлайды.",
        "seo_p2": "Әрбір чокер шектеулі данамен жасалады. Жеке ұзындықты реттеу және Қазақстанның барлық өңірлеріне жедел жеткізу мүмкіндігі бар.",
    },
    "sotuary-iz-zhemchuga.html": {
        "chip_label": "Інжу сотуарлар",
        "h1": "Інжу мен табиғи тастардан жасалған ұзын сотуарлар",
        "title_cluster": "інжу сотуарлар",
        "breadcrumb": "Інжу сотуарлар",
        "lead": "Табиғи інжу, агат, анар тас және тау хрусталінен жасалған ақсүйектік ұзын сотуарлар мен галстук-алқалар. Силуэтті визуалды ұзартады.",
        "seo_title": "Табиғи інжу мен минералдардан авторлық сотуарлар",
        "seo_p1": "Сотуар — ар-деко дәуірінің қайта оралған мәртебелі әшекейі. Інжу мен қара агаттың ұзын тізбегі кез келген бір түсті көйлек пен жейдеге ерекше француздық сымбат береді.",
        "seo_p2": "Шебер бұйымның салмақ тепе-теңдігін дәл есептеп жинайды, сондықтан сотуар тағып жүргенде бұралмай әдемі түсіп тұрады.",
    },
    "ukrasheniya-iz-barochnogo-zhemchuga.html": {
        "chip_label": "Барокко інжуі",
        "h1": "Барокко інжуінен қолдан жасалған әшекейлер",
        "title_cluster": "барокко інжуінен әшекейлер",
        "breadcrumb": "Барокко інжуі",
        "lead": "Қайталанбас табиғи органикалық пішіні бар ірі барокко інжуі қойылған алқалар, тізбектер, білезіктер мен сырғалар. Қалың перламутр қабаты мен премиум жылтыр.",
        "seo_title": "Табиғи барокко інжуінің қасиеті мен құндылығы — Livi Jewelry",
        "seo_p1": "Барокко інжуі (Baroque Pearl) — табиғаттың өзі жаратқан асимметриялық бірегей пішін. Әрбір інжу түйіршігінің екінші қайталануы дүниеде жоқ.",
        "seo_p2": "Біз ірі барокко інжуін алтын және родий жалатылған сапалы фурнитурамен үйлестіреміз. Әр бұйым өлшемі жеке тапсырыспен реттеледі.",
    },
    "ukrasheniya-iz-gematita.html": {
        "chip_label": "Гематит",
        "h1": "Табиғи гематиттен жасалған авторлық әшекейлер",
        "title_cluster": "гематиттен әшекейлер",
        "breadcrumb": "Гематит",
        "lead": "Қырлы гематит, жолбарыс көзі және нефриттен жасалған алқалар, чокерлер мен жиынтықтар. Терең графитті-болат жылтыр.",
        "seo_title": "Табиғи гематиттен жасалған әшекейлер — заманауи стиль",
        "seo_p1": "Табиғи гематит өзінің айнадай болат жылтырымен және салмақты салиқалылығымен зергерлік өнерде жоғары бағаланады.",
        "seo_p2": "Гематит моншақтары ұзақ уақыт бойы жылтырын сақтайды. Төзімді гипоаллергенді ілмектермен жабдықталған.",
    },
    "ukrasheniya-iz-malahita.html": {
        "chip_label": "Малахит пен Нефрит",
        "h1": "Табиғи малахит пен нефриттен жасалған әшекейлер",
        "title_cluster": "малахит пен нефриттен әшекейлер",
        "breadcrumb": "Малахит пен Нефрит",
        "lead": "Бірегей табиғи өрнегі бар малахит пен жасыл нефриттен жасалған білезіктер, алқалар мен жиынтықтар.",
        "seo_title": "Табиғи малахит пен нефриттен әшекейлер — Livi Jewelry",
        "seo_p1": "Табиғи малахит пен нефрит — асыл мәртебенің символы. Алтын жалатылған фурнитурамен бірге бұл тастар таңғажайып салтанат сыйлайды.",
        "seo_p2": "Шебер әр тасты қолмен таңдайды.",
    },
    "ukrasheniya-iz-ametista.html": {
        "chip_label": "Аметист пен Флюорит",
        "h1": "Табиғи аметист пен флюориттен жасалған әшекейлер",
        "title_cluster": "аметист пен флюориттен әшекейлер",
        "breadcrumb": "Аметист пен Флюорит",
        "lead": "Лаванда реңкті табиғи аметист пен жалбыз түсті флюориттен жасалған жиынтықтар, алқалар және сырғалар.",
        "seo_title": "Табиғи аметист пен флюориттен авторлық әшекейлер",
        "seo_p1": "Аметист пен флюорит жарықты тамаша шағылыстыратын мөлдір қырларымен танымал. Қызғылт кварц және інжумен үйлесімі ерекше нәзік.",
        "seo_p2": "Қазақстан бойынша СДЭК арқылы 1–3 жұмыс күні ішінде жеткізіледі.",
    },
    "ukrasheniya-iz-granata.html": {
        "chip_label": "Анар тас және Агат",
        "h1": "Табиғи анар тас (гранат) пен агаттан жасалған әшекейлер",
        "title_cluster": "анар тас пен агаттан әшекейлер",
        "breadcrumb": "Анар тас және Агат",
        "lead": "Қанық шарап реңкті қырлы анар тас пен барқыт қара агаттан жасалған алқалар, сотуарлар мен жиынтықтар.",
        "seo_title": "Табиғи анар тас пен агаттан алқалар мен жиынтықтар",
        "seo_p1": "Табиғи анар тас (гранат) терең қызыл-рубин реңкімен көз тартады. Қара агатпен қатар қолданылғанда айрықша сән түзейді.",
        "seo_p2": "Берік ювелирлік тросикте қолмен жиналады.",
    },
    "ukrasheniya-iz-rozovogo-kvarca.html": {
        "chip_label": "Қызғылт кварц",
        "h1": "Табиғи қызғылт кварцтан жасалған әшекейлер",
        "title_cluster": "қызғылт кварцтан әшекейлер",
        "breadcrumb": "Қызғылт кварц",
        "lead": "Табиғи қызғылт кварц, інжу және аметисттен жасалған нәзік алқалар, сеттер мен сырғалар. Жұмсақ пастелді реңктер.",
        "seo_title": "Табиғи қызғылт кварц пен інжуден жасалған әшекейлер",
        "seo_p1": "Қызғылт кварц — нәзіктік пен әйелдік жылылықтың белгісі. Оның мөлдір күлгін-қызғылт реңкі бет түсін жасартып, ерекше сергектік береді.",
        "seo_p2": "Сыйлыққа арналған әсем қаптамасымен бірге ұсынылады.",
    },
    "ukrasheniya-iz-biryuzy.html": {
        "chip_label": "Фируза (бирюза)",
        "h1": "Табиғи фирузадан (бирюза) жасалған әшекейлер",
        "title_cluster": "фирузадан әшекейлер",
        "breadcrumb": "Фируза (бирюза)",
        "lead": "Табиғи фактурасы бар көгілдір фирузадан жасалған толық зергерлік жиынтықтар, алқалар, білезіктер мен сырғалар.",
        "seo_title": "Табиғи фирузадан қолдан жасалған жиынтықтар мен алқалар",
        "seo_p1": "Табиғи фируза — ежелден сәттілік пен берекенің тасы болып саналады. Оның ашық аспан түстес реңкі кез келген маусымда жарқырап тұрады.",
        "seo_p2": "Өлшемді реттеу және бүкіл Қазақстанға жедел жеткізу мүмкіндігі қарастырылған.",
    },
    "ukrasheniya-iz-gornogo-hrustalya.html": {
        "chip_label": "Тау хрусталі",
        "h1": "Тау хрусталі мен кварцтан жасалған әшекейлер",
        "title_cluster": "тау хрусталінен әшекейлер",
        "breadcrumb": "Тау хрусталі",
        "lead": "Мөлдір тау хрусталі, циркондар, флюорит және табиғи інжуден жасалған көпқабатты алқалар мен әшекейлер.",
        "seo_title": "Тау хрусталінен қолмен жиналған премиум алқалар",
        "seo_p1": "Тау хрусталі — мұздай мөлдір табиғи кварц. Оның жарық өткізгіштігі мен жарқырауы інжумен үйлескенде патшалық салтанат сыйлайды.",
        "seo_p2": "Гипоаллергенді родий және алтын жабынды фурнитура қолданылады.",
    },
    "ukrasheniya-iz-lunnogo-kamnya.html": {
        "chip_label": "Ай тасы және Перламутр",
        "h1": "Ай тасы мен табиғи перламутрден жасалған әшекейлер",
        "title_cluster": "ай тасы мен перламутрден әшекейлер",
        "breadcrumb": "Ай тасы және Перламутр",
        "lead": "Құбылмалы табиғи перламутр, Майорка інжуі және жартылай мөлдір минералдардан жасалған авторлық алқалар мен жиынтықтар.",
        "seo_title": "Ай тасы мен перламутрдің сиқырлы жарқылы — Livi Jewelry",
        "seo_p1": "Табиғи перламутр мен ай тасы өзінің нәзік көгілдір-ақ құбылмалы жарқылымен (иризация) белгілі. Күндіз де, кешке де өте сәнді.",
        "seo_p2": "Фирмалық сыйлық қаптамасы және СДЭК арқылы сенімді жеткізу.",
    },
    "ukrasheniya-iz-zhemchuga-mayorka.html": {
        "chip_label": "Майорка інжуі",
        "h1": "Майорка інжуінен жасалған алқалар мен әшекейлер",
        "title_cluster": "Майорка інжуінен әшекейлер",
        "breadcrumb": "Майорка інжуі",
        "lead": "Мінсіз шар тәріздес пішіні мен терең айнадай жылтыры бар Майорка органикалық інжуінен жасалған алқалар, жиынтықтар мен сырғалар.",
        "seo_title": "Майорка інжуінен жасалған әшекейлер — мінсіз жылтыр",
        "seo_p1": "Майорка інжуі табиғи інжу эссенциясының көптеген қабаттарын жағу арқылы испандық дәстүрлі технологиямен жасалады. Ол мінсіз тегістігімен және түсін жоғалтпайтын төзімділігімен ерекшеленеді.",
        "seo_p2": "Өрнекті керамикамен және алтын жалатумен әдемі үйлеседі.",
    },
    "ukrasheniya-iz-tigrovogo-glaza.html": {
        "chip_label": "Жолбарыс көзі және Жадеит",
        "h1": "Жолбарыс көзі мен жадеиттен жасалған әшекейлер",
        "title_cluster": "жолбарыс көзі мен жадеиттен әшекейлер",
        "breadcrumb": "Жолбарыс көзі және Жадеит",
        "lead": "Жібектей құбылмалы жолбарыс көзі, табиғи жадеит және гематиттен жасалған авторлық алқалар, чокерлер мен сырғалар.",
        "seo_title": "Жолбарыс көзі мен жадеиттен жасалған күшті әшекейлер",
        "seo_p1": "Жолбарыс көзі өзінің алтын-янтарь реңкті құбылысымен баурайды, ал жасыл жадеит байсалдылық пен бекзаттық сыйлайды.",
        "seo_p2": "Барлық бұйымдар сапалы ювелирлік тросикте қолмен жиналады.",
    },
    "ukrasheniya-iz-koralla-i-yashmy.html": {
        "chip_label": "Маржан (коралл) және Яшма",
        "h1": "Табиғи маржан мен пейзажды яшмадан жасалған әшекейлер",
        "title_cluster": "маржан мен яшмадан әшекейлер",
        "breadcrumb": "Маржан (коралл) және Яшма",
        "lead": "Жылы терракот маржаны мен көркем суретті яшмадан жасалған жиынтықтар, алқалар, білезіктер мен сырғалар.",
        "seo_title": "Табиғи маржан мен яшмадан жасалған авторлық бұйымдар",
        "seo_p1": "Табиғи қызыл-терракот маржан мен өрнекті яшма жер мен күннің жылуын бейнелейді. Табиғи маталармен (зығыр, жібек, кашемир) тамаша үйлеседі.",
        "seo_p2": "Жиынтықты тұтастай немесе әр бұйымды бөлек сатып алуға болады.",
    },
    "ukrasheniya-iz-lazurita.html": {
        "chip_label": "Лазурит және Авантюрин",
        "h1": "Табиғи лазурит пен авантюриннен жасалған әшекейлер",
        "title_cluster": "лазурит пен авантюриннен әшекейлер",
        "breadcrumb": "Лазурит және Авантюрин",
        "lead": "Патшалық көк лазурит пен жарқыраған жасыл авантюриннен жасалған алқалар мен жиынтықтар.",
        "seo_title": "Табиғи лазурит пен авантюрин — патшалық сән",
        "seo_p1": "Лазурит ішіндегі алтын пирит ұшқындары түнгі аспанды елестетеді. Авантюринмен және інжумен қосылғанда бұйымға қайталанбас тереңдік сыйлайды.",
        "seo_p2": "Төзімді гипоаллергенді ілмектер, сыйлық қорабы мен жедел жеткізу.",
    },
    "tsepi-s-barochnym-zhemchugom.html": {
        "chip_label": "Інжулі тізбектер",
        "h1": "Барокко інжуі бар тізбектер — алтын және родий жалатылған",
        "title_cluster": "барокко інжуі бар тізбектер",
        "breadcrumb": "Інжулі тізбектер",
        "lead": "Акцентті барокко інжуі бар алтын және родий жалатылған сәнді тізбектер, «Гранж» жиынтықтары мен білезіктер.",
        "seo_title": "Ірі барокко інжуі бар трендтік тізбектер — Livi Jewelry",
        "seo_p1": "Көлемді тізбек буындары мен нәзік барокко інжуінің қарама-қайшылығы — қазіргі зергерлік сәннің ең танымал тренді. Родий мен 18K алтын жабыны уақыт өте қарайып кетпейді.",
        "seo_p2": "Сыйлық қаптамасы тегін беріледі.",
    },
    "koltsa-i-garnitury-iz-kamney.html": {
        "chip_label": "Сақиналар мен сәттер",
        "h1": "Табиғи тастардан жасалған сақиналар, түйреуіштер мен жиынтықтар",
        "title_cluster": "сақиналар мен түйреуіштер",
        "breadcrumb": "Сақиналар мен сәттер",
        "lead": "Өлшемі реттелетін сақиналар, дизайнерлік түйреуіш-брошьтер, білезіктер мен сырғалар жиынтығы.",
        "seo_title": "Табиғи тастардан сақиналар мен түйреуіштер жиынтығы",
        "seo_p1": "Сақиналар мен дизайнерлік түйреуіштер — толыққанды стильдік шешім. Әр сақинаның өлшемі ыңғайлы реттеледі (16–19 өлшемдерге лайық), ал түйреуіштер костюмдер мен жейделерге ерекше сән береді.",
        "seo_p2": "Әр элементті бөлек те, толық сет ретінде де тапсырыс беруге болады.",
    },
}



UZ_HUBS_INFO = {
    "kolye-iz-zhemchuga.html": {
        "chip_label": "Marvarid marjonlar",
        "h1": "Tabiiy marvariddan yasalgan marjonlar — qoʻl mehnati taqinchoqlari",
        "title_cluster": "tabiiy marvarid marjonlar",
        "breadcrumb": "Marvarid marjonlar",
        "lead": "Tabiiy yetishtirilgan marvarid, barokko marvaridi va Mayorka marvarididan qoʻlda terilgan mualliflik marjonlari va chockerlari. Chidamli tillarang va rodiy qoplamali furnitura.",
        "seo_title": "Livi Jewelry ustaxonasining tabiiy marvarid marjonlari — nafislik va sifat",
        "seo_p1": "Tabiiy marvarid marjon — har qanday ayol qiyofasiga aslzodalik bagʻishlaydigan klassik zargarlik buyumi. Livi Jewelry ustaxonasida (Ostona) har bir marvarid donasi jilosi va tabiiy shakli boʻyicha sinchkovlik bilan saralanadi. Buyumlar sifatli zargarlik simiga terilib, allergiya chaqirmaydigan chidamli furnitura bilan taʼminlanadi.",
        "seo_p2": "Barcha marjonlar firma sovgʻa qutisiga solinib, Toshkent, Samarqand, Buxoro va butun Oʻzbekiston hamda Qozogʻiston boʻylab tezkor yetkazib beriladi.",
    },
    "braslety-iz-zhemchuga.html": {
        "chip_label": "Marvarid bilaguzuklar",
        "h1": "Tabiiy marvarid va toshlardan bilaguzuklar — Livi Jewelry",
        "title_cluster": "marvarid bilaguzuklar",
        "breadcrumb": "Marvarid bilaguzuklar",
        "lead": "Tabiiy marvarid, malaxit, feruza va ametistdan ishlangan nafis qoʻl mehnati bilaguzuklari.",
        "seo_title": "Tabiiy marvariddan qoʻlda yasalgan bilaguzuklar — Livi Jewelry",
        "seo_p1": "Marvarid bilaguzuklar nozik bilak goʻzalligini namoyon etib, kundalik va oqshom obrazlariga mukammal uygʻunlashadi. Biz barokko marvaridi va tabiiy minerallarni oliy toifadagi furnitura bilan birlashtiramiz.",
        "seo_p2": "SDEK va Qazpost orqali Oʻzbekiston va butun MDH boʻylab ishonchli yetkazib berish.",
    },
    "sergi-iz-zhemchuga.html": {
        "chip_label": "Marvarid sirgʻalar",
        "h1": "Tabiiy marvarid sirgʻalar va toʻplamlar — qoʻl mehnati",
        "title_cluster": "marvarid sirgʻalar",
        "breadcrumb": "Marvarid sirgʻalar",
        "lead": "Barokko marvaridi, anor toshi, malaxit va ametistdan ishlangan nafis sirgʻalar. Sirgʻalarni alohida yoki toʻliq toʻplam bilan birga xarid qilish mumkin.",
        "seo_title": "Tabiiy marvarid sirgʻalar — mualliflik zargarlik buyumlari",
        "seo_p1": "Livi Jewelry ustaxonasining sirgʻalari yengilligi, quloqda qulayligi va gipoallergen ingliz/fransuz qulflari bilan ajralib turadi. Kun boʻyi taqilganda ham mutlaqo noqulaylik tugʻdirmaydi.",
        "seo_p2": "Sirgʻalarni mos marjon, bilaguzuk yoki uzuk bilan toʻldirib, yaxlit zargarlik ansamblini yaratish mumkin. Sovgʻa qutisi bepul taqdim etiladi.",
    },
    "komplekty-ukrasheniy.html": {
        "chip_label": "Taqinchoqlar toʻplami",
        "h1": "Tabiiy toshlar va marvariddan zargarlik toʻplamlari",
        "title_cluster": "taqinchoqlar toʻplamlari",
        "breadcrumb": "Taqinchoqlar toʻplami",
        "lead": "Tabiiy marvarid, ametist, malaxit, feruza va pushti kvarsdan mualliflik toʻplamlari. Toʻplamni toʻliq yoki har bir buyumni alohida xarid qilish imkoniyati.",
        "seo_title": "Livi Jewelry eksklyuziv qoʻl mehnati taqinchoqlar toʻplamlari",
        "seo_p1": "Zargarlik toʻplami — bu marjon, bilaguzuk, sirgʻa va uzukning rangi hamda uslubi boʻyicha mukammal uygʻunlashgan yaxlit ansamblidir. Ustaxonamizda har bir toʻplam qoʻlda saralab yigʻiladi.",
        "seo_p2": "Barcha toʻplamlar pishiq zargarlik simiga teriladi. Sifatli tilla yoki rodiy qoplamasi yillar davomida asl holatini yoʻqotmaydi. Oʻzbekiston va Qozogʻiston boʻylab tezkor yetkazib berish.",
    },
    "chokery-iz-naturalnyh-kamney.html": {
        "chip_label": "Toshlardan chockerlar",
        "h1": "Tabiiy toshlar va marvariddan chockerlar — Livi Jewelry",
        "title_cluster": "tabiiy toshlardan chockerlar",
        "breadcrumb": "Toshlardan chockerlar",
        "lead": "Tabiiy anor toshi, flyuorit, marvarid va gematitdan ishlangan qisqa nozik marjonlar va chockerlar. Uzunlikni sozlovchi 5 sm uzaytiruvchi zanjir.",
        "seo_title": "Tabiiy toshlardan yasalgan zamonaviy chockerlar — Livi Jewelry",
        "seo_p1": "Chocker — boʻyin chizigʻi va boʻyinturuq suyagini goʻzal ajratib koʻrsatuvchi zamonaviy zargarlik modasining yetakchi trendidir. Qirrali tabiiy minerallar yorugʻlik tushganda maftunkor jilo baxsh etadi.",
        "seo_p2": "Har bir chocker cheklangan nusxada yasaladi. Oʻzbekistonning barcha viloyatlariga tezkor yetkazib berish mavjud.",
    },
    "sotuary-iz-zhemchuga.html": {
        "chip_label": "Marvarid sotuarlar",
        "h1": "Marvarid sotuarlar va uzun marjonlar — Livi Jewelry",
        "title_cluster": "marvarid sotuarlar",
        "breadcrumb": "Marvarid sotuarlar",
        "lead": "Tabiiy marvarid va toshlardan yasalgan oqlangan uzun marjonlar, transformator sotuarlar. Koʻp qatorli yoki orqaga tashlab taqish imkoniyati.",
        "seo_title": "Mualliflik marvarid sotuarlari — nafis uzun marjonlar",
        "seo_p1": "Sotuar — 1920-yillarning aslzoda uslubini oʻzida mujassam etgan uzoq marjon boʻlib, u koʻylaklar, kostyumlar va kechki liboslar bilan ajoyib uygʻunlashadi. Uni bir necha qator qilib oʻrash ham mumkin.",
        "seo_p2": "Livi Jewelry sotuarlari sifatli yetishtirilgan marvariddan yigʻiladi va mustahkam qulflar bilan taʼminlanadi. Toshkent va butun Oʻzbekistonga xavfsiz yetkazib beriladi.",
    },
    "ukrasheniya-iz-barochnogo-zhemchuga.html": {
        "chip_label": "Barokko marvaridi",
        "h1": "Barokko marvarididan taqinchoqlar — betakror qoʻl mehnati",
        "title_cluster": "barokko marvarididan taqinchoqlar",
        "breadcrumb": "Barokko marvaridi",
        "lead": "Noyob assimetrik shakldagi tabiiy barokko marvarididan marjonlar, kulonlar va sirgʻalar. Har bir buyum — takrorlanmas tabiat asari.",
        "seo_title": "Tabiiy barokko marvarididan eksklyuziv taqinchoqlar",
        "seo_p1": "Barokko marvaridining jozibasi uning mukammal boʻlmagan tabiiy shakli va boy kamalakdek jilosidadir. Dunyoda ikkita mutlaqo bir xil barokko marvaridi mavjud emas.",
        "seo_p2": "Ustaxonamizda har bir barokko marvaridi uchun individual uslub tanlanadi. Sovgʻa qadoqlanishi va Oʻzbekistonga tez yetkazish taʼminlanadi.",
    },
    "ukrasheniya-iz-gematita.html": {
        "chip_label": "Gematit taqinchoqlar",
        "h1": "Tabiiy gematitdan yasalgan taqinchoqlar — zamonaviy uslub",
        "title_cluster": "gematitdan taqinchoqlar",
        "breadcrumb": "Gematit taqinchoqlar",
        "lead": "Grafik metall yaltiroqlikka ega tabiiy qirrali gematitdan marjonlar, bilaguzuklar va chockerlar. Marvarid va tabiiy toshlar bilan ajoyib uygʻunlik.",
        "seo_title": "Tabiiy gematitdan qoʻl mehnati zargarlik buyumlari",
        "seo_p1": "Gematit oʻzining sirli metall tusli yaltiroqligi, vazminligi va qatʼiy feʼl-atvori bilan zamonaviy geometriyaning timsoli hisoblanadi. U har qanday kiyim uslubiga zamonaviy nafislik qoʻshadi.",
        "seo_p2": "Bizning gematitli zargarlik buyumlarimiz gipoallergen qoplama va mustahkam yigʻilishga ega boʻlib, kundalik taqish uchun juda qulaydir.",
    },
    "ukrasheniya-iz-malahita.html": {
        "chip_label": "Malaxit taqinchoqlar",
        "h1": "Tabiiy malaxitdan taqinchoqlar — yashil tabiat jilosi",
        "title_cluster": "malaxitdan taqinchoqlar",
        "breadcrumb": "Malaxit taqinchoqlar",
        "lead": "Chuqur zumrad tusli va betakror tabiiy naqshlarga ega tabiiy malaxitdan marjonlar, bilaguzuklar va toʻplamlar. Oliy sifatli furnitura.",
        "seo_title": "Tabiiy malaxitdan mualliflik taqinchoqlari — Livi Jewelry",
        "seo_p1": "Malaxit — asrlar davomida donolik, boylik va ichki xotirjamlik ramzi sanalgan aslzoda toshdir. Uning har bir donasidagi tabiiy chiziqlar va halqalar betakror tabiat rasmidir.",
        "seo_p2": "Livi Jewelry ustaxonasida malaxit marvarid va tillarang detallar bilan boyitiladi. Barcha buyumlar Toshkent va Oʻzbekiston boʻylab yetkaziladi.",
    },
    "ukrasheniya-iz-ametista.html": {
        "chip_label": "Ametist taqinchoqlar",
        "h1": "Tabiiy binafsharang ametistdan taqinchoqlar — Livi Jewelry",
        "title_cluster": "ametistdan taqinchoqlar",
        "breadcrumb": "Ametist taqinchoqlar",
        "lead": "Shaffof va chuqur binafsha rangli tabiiy qirrali ametistdan marjonlar, bilaguzuklar va sirgʻalar. Tillarang va rodiy furnitura.",
        "seo_title": "Tabiiy ametistdan qoʻlda yasalgan zargarlik buyumlari",
        "seo_p1": "Ametist oʻzining jozibali binafsha tuslari bilan ichki xotirjamlik va maʼnaviy poklik ramzidir. Qirrali ametist munchoqlari quyosh nurida yorqin yaltiraydi.",
        "seo_p2": "Ustaxonamiz ametistni marvarid va boshqa nozik minerallar bilan uygʻunlashtiradi.",
    },
    "ukrasheniya-iz-granata.html": {
        "chip_label": "Anor toshi taqinchoqlar",
        "h1": "Tabiiy anor toshidan (granat) taqinchoqlar — ehtiros va nafislik",
        "title_cluster": "anor toshidan taqinchoqlar",
        "breadcrumb": "Anor toshi taqinchoqlar",
        "lead": "Toʻq qizil, yoqut tusli tabiiy qirrali anor toshidan chockerlar, marjonlar va bilaguzuklar. Oliy toifadagi furnitura bilan boyitilgan.",
        "seo_title": "Tabiiy anor toshidan mualliflik taqinchoqlari — Livi Jewelry",
        "seo_p1": "Anor toshi (granat) — muhabbat, joʻshqinlik va ichki kuch-quvvat timsoli boʻlgan qimmatbaho mineraldir. Qirrali donalar eng xira yorugʻlikda ham ajoyib yonadi.",
        "seo_p2": "Livi Jewelry anor toshli buyumlari kechki va bayramona liboslar uchun ajoyib aksentdir. Oʻzbekistonga qulay yetkazib berish xizmati bilan.",
    },
    "ukrasheniya-iz-rozovogo-kvarca.html": {
        "chip_label": "Pushti kvars",
        "h1": "Tabiiy pushti kvarsdan taqinchoqlar — mehr va noziklik timsoli",
        "title_cluster": "pushti kvarsdan taqinchoqlar",
        "breadcrumb": "Pushti kvars",
        "lead": "Yumshoq pastel tusli tabiiy pushti kvars va marvariddan marjonlar, bilaguzuklar va toʻplamlar. Ayollik jozibasini uygʻotuvchi nafislik.",
        "seo_title": "Tabiiy pushti kvarsdan qoʻl mehnati zargarlik buyumlari",
        "seo_p1": "Pushti kvars — cheksiz mehr-muhabbat, noziklik va qalb xotirjamligi minerali hisoblanadi. Uning muloyim rangi terining tabiiy ohangini ajoyib ochib beradi.",
        "seo_p2": "Ushbu toshdan yasalgan buyumlar har qanday yoshdagi xonimlar uchun ajoyib sovgʻadir. Firma qutisida bepul taqdim etiladi.",
    },
    "ukrasheniya-iz-biryuzy.html": {
        "chip_label": "Feruza taqinchoqlar",
        "h1": "Tabiiy feruzadan taqinchoqlar — moviy dengiz nafasi",
        "title_cluster": "feruzadan taqinchoqlar",
        "breadcrumb": "Feruza taqinchoqlar",
        "lead": "Yorqin osmonrang va yashil-moviy tusli tabiiy feruzadan yasalgan marjonlar, bilaguzuklar va sirgʻalar. Sharqona aslzodalik va zamonaviy uslub.",
        "seo_title": "Tabiiy feruzadan mualliflik taqinchoqlari — Livi Jewelry",
        "seo_p1": "Feruza — qadimdan omad, himoya va baxt keltiruvchi muqaddas tosh sifatida qadrlanadi. Uning yorqin rangi yozgi va bahorgi obrazlarga oʻzgacha joziba bagʻishlaydi.",
        "seo_p2": "Har bir feruza donasi oʻzining tabiiy tomirlari bilan betakrordir. Toshkent, Samarqand va barcha shaharlarga SDEK orqali yetkaziladi.",
    },
    "ukrasheniya-iz-gornogo-hrustalya.html": {
        "chip_label": "Togʻ billuri",
        "h1": "Tabiiy togʻ billuridan taqinchoqlar — musaffo soflik",
        "title_cluster": "togʻ billuridan taqinchoqlar",
        "breadcrumb": "Togʻ billuri",
        "lead": "Koʻz yoshidek musaffo shaffof tabiiy togʻ billuridan qirrali chockerlar, marjonlar va sirgʻalar. Har qanday libos bilan mos tushuvchi universal nafislik.",
        "seo_title": "Tabiiy togʻ billuridan zargarlik buyumlari — Livi Jewelry",
        "seo_p1": "Togʻ billuri — mukammal shaffoflik va musaffo soflik timsolidir. U yorugʻlikni prizma kabi sindirib, kamalakning barcha ranglarida tovlanadi.",
        "seo_p2": "Kundalik va tantanali uslub uchun eng mos tosh. Sovgʻa qutisi bilan.",
    },
    "ukrasheniya-iz-lunnogo-kamnya.html": {
        "chip_label": "Oy toshi",
        "h1": "Tabiiy oy toshidan taqinchoqlar — sirli moviy jilo",
        "title_cluster": "oy toshidan taqinchoqlar",
        "breadcrumb": "Oy toshi",
        "lead": "Sehrli moviy shafaqqa ega tabiiy oy toshi (adulyar) va marvariddan marjonlar, bilaguzuklar hamda sirgʻalar. Romantik va sirli joziba.",
        "seo_title": "Tabiiy oy toshidan qoʻl mehnati taqinchoqlari",
        "seo_p1": "Oy toshi oʻzining sirli ichki nurlanishi (adulyarisatsiya) bilan mashhur. Harakatlanganda uning yuzasida mayin moviy toʻlqinlar oʻynaydi.",
        "seo_p2": "Livi Jewelry ustaxonasida saralangan minerallardan qoʻlda teriladi. Oʻzbekiston boʻylab xavfsiz yetkazib berish kafolatlanadi.",
    },
    "ukrasheniya-iz-zhemchuga-mayorka.html": {
        "chip_label": "Mayorka marvaridi",
        "h1": "Mayorka marvarididan taqinchoqlar — mukammal shakl va jilo",
        "title_cluster": "Mayorka marvarididan taqinchoqlar",
        "breadcrumb": "Mayorka marvaridi",
        "lead": "Ispaniya texnologiyasi asosida ishlangan oliy darajali Mayorka marvarididan klassik marjonlar, bilaguzuklar va toʻplamlar. Tashqi taʼsirlarga nihoyatda chidamli.",
        "seo_title": "Mayorka marvarididan zargarlik buyumlari — Livi Jewelry",
        "seo_p1": "Mayorka marvaridi — koʻp qatlamli tabiiy organik marvarid essensiyasi bilan qoplangan boʻlib, ideal silliqligi va boy atlas jilosi bilan ajralib turadi.",
        "seo_p2": "Klassik obraz ixlosmandlari uchun ayni muddao. Parfyumeriya va vaqt sinoviga chidamli boʻlib, yillar davomida jilosini yoʻqotmaydi.",
    },
    "ukrasheniya-iz-tigrovogo-glaza.html": {
        "chip_label": "Yoʻlbars koʻzi",
        "h1": "Tabiiy yoʻlbars koʻzi toshidan taqinchoqlar — iliq oltin jilo",
        "title_cluster": "yoʻlbars koʻzidan taqinchoqlar",
        "breadcrumb": "Yoʻlbars koʻzi",
        "lead": "Ipakdek ipaksimon yaltiroqlikka ega oltin-jigarrang tabiiy yoʻlbars koʻzidan marjonlar, bilaguzuklar va aksessuarlar.",
        "seo_title": "Tabiiy yoʻlbars koʻzidan qoʻl mehnati taqinchoqlari",
        "seo_p1": "Yoʻlbars koʻzi — kuchli himoya va oʻziga ishonch toshi boʻlib, uning yuzasidagi yorugʻlik chizigʻi yirtqich koʻzining nigohini eslatadi.",
        "seo_p2": "Tillarang furnitura bilan boyitilgan ushbu buyumlar jiddiy va salobatli koʻrinish hosil qiladi. Oʻzbekistonga yetkazib berish mavjud.",
    },
    "ukrasheniya-iz-koralla-i-yashmy.html": {
        "chip_label": "Marjon va yashma",
        "h1": "Tabiiy marjon (korall) va yashmadan taqinchoqlar",
        "title_cluster": "marjon va yashmadan taqinchoqlar",
        "breadcrumb": "Marjon va yashma",
        "lead": "Yorqin qizil marjon va boy rang-barang naqshli yashmadan etnik hamda zamonaviy uslubdagi marjonlar va bilaguzuklar. Hayotiy quvvat manbai.",
        "seo_title": "Tabiiy marjon va yashmadan mualliflik taqinchoqlari",
        "seo_p1": "Qizil marjon va yer boyligini ifodalovchi yashma azaldan quvonch, sogʻliq va mustahkam oila timsoli sifatida eʼzozlanadi. Ularning uygʻunligi betakror etnik iliqlik yaratadi.",
        "seo_p2": "Har bir buyum alohida mehr bilan yasaladi va oʻziga xos ranglar jilvasiga ega. Toshkent va viloyatlarga tez yetkaziladi.",
    },
    "ukrasheniya-iz-lazurita.html": {
        "chip_label": "Lojuvard (lazurit)",
        "h1": "Tabiiy lojuvarddan (lazurit) taqinchoqlar — shohona moviylik",
        "title_cluster": "lojuvarddan taqinchoqlar",
        "breadcrumb": "Lojuvard (lazurit)",
        "lead": "Oltin pirit zarrachalari bilan bezatilgan toʻq koʻk tabiiy lojuvarddan marjonlar, chockerlar va bilaguzuklar. Sharqona hashamat.",
        "seo_title": "Tabiiy lojuvarddan qoʻlda yasalgan taqinchoqlar — Livi Jewelry",
        "seo_p1": "Lojuvard (lazurit) — yulduzli tungi osmonni eslatuvchi shohona toshdir. Qadim zamonlardan beri hukmdorlar va malikalar zargarlik buyumlarining asosiy toshi boʻlgan.",
        "seo_p2": "Marvarid va tillarang detallar bilan uygʻunlashganda benuqson olijanob koʻrinish kasb etadi. Sovgʻa qutisiga joylab yuboriladi.",
    },
    "tsepi-s-barochnym-zhemchugom.html": {
        "chip_label": "Zanjirlar va barokko marvaridi",
        "h1": "Yirik barokko marvaridli zanjirlar — trend zargarlik buyumlari",
        "title_cluster": "barokko marvaridli zanjirlar",
        "breadcrumb": "Zanjirlar va barokko marvaridi",
        "lead": "Katta hajmli tilla va rodiy qoplamali zanjirlar hamda yirik assimetrik barokko marvaridi uygʻunligi. Zamonaviy shahar modasining yorqin timsoli.",
        "seo_title": "Barokko marvaridi bilan bezatilgan zamonaviy zanjirlar",
        "seo_p1": "Katta zanjirlar va tabiiy organik barokko marvaridi kontrasti bugungi kunda jahon podiumlarining eng ommabop zargarlik yoʻnalishidir.",
        "seo_p2": "Qulay qulflar va gipoallergen mustahkam metall. Oʻzbekiston va Qozogʻistonga tezkor yetkazish.",
    },
    "koltsa-i-garnitury-iz-kamney.html": {
        "chip_label": "Uzuklar va garniturlar",
        "h1": "Tabiiy toshlar va marvariddan uzuklar hamda garniturlar",
        "title_cluster": "uzuklar va toshli garniturlar",
        "breadcrumb": "Uzuklar va garniturlar",
        "lead": "Tabiiy toshli qulay oʻlchami sozlanuvchi uzuklar, toʻliq zargarlik garniturlari. Har qanday barmoq oʻlchamiga mos tushadigan universal dizayn.",
        "seo_title": "Tabiiy toshlardan uzuklar va garniturlar — Livi Jewelry",
        "seo_p1": "Uzuklarimizning qulayligi shundaki, ularning oʻlchami erkin sozlanadi (bezrazmerny). Bu esa ularni oʻlchamni bilmay turib sovgʻa qilish uchun ideal tanlovga aylantiradi.",
        "seo_p2": "Uzukni toʻplamning boshqa qismlari bilan birga xarid qilib, toʻliq garniturga ega boʻlishingiz mumkin. Sifat kafolati va qulay yetkazib berish.",
    },
}


def clean_attr(text):
    if not text:
        return ""
    return str(text).replace("&", "&amp;").replace('"', "&quot;").replace("\n", " ").strip()


def build_clean_alt(product: dict) -> str:
    title = (product.get("title") or "").strip()
    materials = product.get("materials") or ["Натуральные камни"]
    materials_str = ", ".join(materials)
    return f"{title} — авторская ручная работа ({materials_str}), Livi Jewelry"


def build_product_schema_for_itemlist(p: dict, idx: int, is_kz: bool = False, kz_title: str = "", kz_desc: str = "", is_uz: bool = False, uz_title: str = "", uz_desc: str = "") -> dict:
    pid = p["id"]
    if is_uz and uz_title:
        ptitle = uz_title
    elif is_kz and kz_title:
        ptitle = kz_title
    else:
        ptitle = p["title"].strip()

    if is_uz and uz_desc:
        pdesc = uz_desc
    elif is_kz and kz_desc:
        pdesc = kz_desc
    else:
        pdesc = (p.get("description") or ptitle).strip()

    pprice = int(p.get("price", 0))
    pprice_dec = f"{pprice:.2f}"
    pimg_rel = p["image"].lstrip("/")
    pimg_abs = f"{BASE_URL}/{pimg_rel}"
    p_instock = p.get("inStock", True) and not p.get("archived", False)
    if is_uz:
        p_url = f"{BASE_URL}/uz/product/{pid}.html"
    elif is_kz:
        p_url = f"{BASE_URL}/kz/product/{pid}.html"
    else:
        p_url = f"{BASE_URL}/product/{pid}.html"

    prod_obj = {
        "@type": "Product",
        "name": ptitle,
        "image": pimg_abs,
        "description": pdesc,
        "sku": pid,
        "mpn": pid,
        "brand": {"@type": "Brand", "name": "Livi Jewelry"},
        "offers": {
            "@type": "Offer",
            "url": p_url,
            "price": pprice_dec,
            "priceCurrency": "KZT",
            "priceValidUntil": "2027-12-31",
            "availability": "https://schema.org/InStock" if p_instock else "https://schema.org/OutOfStock",
            "itemCondition": "https://schema.org/NewCondition",
            "seller": {
                "@type": ["Organization", "JewelryStore"],
                "name": "Livi Jewelry",
                "telephone": "+77054510584",
                "priceRange": "15000 KZT - 91000 KZT",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Астана",
                    "addressCountry": "KZ",
                },
            },
            "hasMerchantReturnPolicy": {
                "@type": "MerchantReturnPolicy",
                "applicableCountry": "KZ",
                "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                "merchantReturnDays": 14,
                "returnMethod": "https://schema.org/ReturnByMail",
                "returnFees": "https://schema.org/FreeReturn",
            },
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {
                    "@type": "MonetaryAmount",
                    "value": "4000",
                    "currency": "KZT",
                },
                "shippingDestination": {
                    "@type": "DefinedRegion",
                    "addressCountry": "KZ",
                },
                "deliveryTime": {
                    "@type": "ShippingDeliveryTime",
                    "handlingTime": {
                        "@type": "QuantitativeValue",
                        "minValue": 0,
                        "maxValue": 1,
                        "unitCode": "d",
                    },
                    "transitTime": {
                        "@type": "QuantitativeValue",
                        "minValue": 1,
                        "maxValue": 3,
                        "unitCode": "d",
                    },
                },
            },
        },
    }

    return {
        "@type": "ListItem",
        "position": idx,
        "url": p_url,
        "item": prod_obj,
    }


def match_products_for_hub(hub, products):
    active = [p for p in products if not p.get("archived", False)]
    ftype = hub["filter_type"]
    fval = hub["filter_val"]

    matched = []
    if ftype == "category":
        matched = [p for p in active if p.get("category") == fval]
    elif ftype == "choker":
        for p in active:
            blob = (p.get("title", "") + " " + p.get("description", "")).lower()
            if p.get("category") == "Necklaces" or any(k in blob for k in fval):
                matched.append(p)
    elif ftype == "lariat":
        for p in active:
            blob = (p.get("title", "") + " " + p.get("description", "")).lower()
            if p.get("category") in ("Lariats", "Chains") or "сотуар" in blob or "цепь" in blob:
                matched.append(p)
    elif ftype == "chain_pearl":
        for p in active:
            blob = (p.get("title", "") + " " + p.get("description", "") + " " + " ".join(p.get("materials", []))).lower()
            if any(k in blob for k in fval) or p.get("id") in ("prod_04", "prod_05", "prod_22"):
                matched.append(p)
    elif ftype == "rings_pins":
        for p in active:
            blob = (p.get("title", "") + " " + p.get("description", "")).lower()
            if any(k in blob for k in fval) or p.get("id") in ("prod_07", "prod_10", "prod_18", "prod_28"):
                matched.append(p)
    elif ftype == "stone":
        for p in active:
            blob = (
                p.get("title", "")
                + " "
                + p.get("description", "")
                + " "
                + " ".join(p.get("materials", []))
            ).lower()
            if any(k.lower() in blob for k in fval):
                matched.append(p)

    recommended_ids = set()
    if len(matched) < 4:
        needed = 4 - len(matched)
        matched_ids = {p["id"] for p in matched}
        baroque_candidates = [
            p for p in active
            if p["id"] not in matched_ids
            and (
                "барочн" in (" ".join(p.get("materials", [])) + " " + p.get("title", "")).lower()
                or "жемчуг" in (" ".join(p.get("materials", [])) + " " + p.get("title", "")).lower()
            )
        ]
        for comp in baroque_candidates[:max(needed, 2)]:
            matched.append(comp)
            recommended_ids.add(comp["id"])

    return matched, recommended_ids


def build_interlink_block_html(current_slug="", prefix=""):
    chips = []
    for slug, label in EXISTING_HUBS:
        active_cls = " active" if slug == current_slug else ""
        chips.append(f'        <a class="stone-chip{active_cls}" href="{prefix}/{slug}">{label}</a>')
    for h in ALL_HUBS:
        slug = h["slug"]
        label = h["chip_label"]
        active_cls = " active" if slug == current_slug else ""
        chips.append(f'        <a class="stone-chip{active_cls}" href="{prefix}/{slug}">{label}</a>')
    chips_str = "\n".join(chips)
    return f"""    <section class="hub-interlink-section" aria-label="Подборки по камням и стилям">
      <details class="hub-interlink-accordion">
        <summary>Подборки по камням и стилям</summary>
        <p class="hub-interlink-sub">Переходите в тематические коллекции Livi Jewelry по натуральным минералам и форматам украшений</p>
        <div class="hub-interlink-chips">
{chips_str}
        </div>
      </details>
    </section>"""


def build_interlink_block_html_kz(current_slug=""):
    chips = []
    for slug, _ in EXISTING_HUBS:
        label = KZ_HUBS_INFO.get(slug, {}).get("chip_label", "Коллекция")
        active_cls = " active" if slug == current_slug else ""
        chips.append(f'        <a class="stone-chip{active_cls}" href="/kz/{slug}">{label}</a>')
    for h in ALL_HUBS:
        slug = h["slug"]
        label = KZ_HUBS_INFO.get(slug, {}).get("chip_label", h["chip_label"])
        active_cls = " active" if slug == current_slug else ""
        chips.append(f'        <a class="stone-chip{active_cls}" href="/kz/{slug}">{label}</a>')
    chips_str = "\n".join(chips)
    return f"""    <section class="hub-interlink-section" aria-label="Тастар мен стильдер бойынша жинақтар">
      <details class="hub-interlink-accordion">
        <summary>Тастар мен стильдер бойынша жинақтар</summary>
        <p class="hub-interlink-sub">Табиғи минералдар мен зергерлік бұйымдардың тақырыптық топтамаларына өтіңіз</p>
        <div class="hub-interlink-chips">
{chips_str}
        </div>
      </details>
    </section>"""


def build_interlink_block_html_uz(current_slug=""):
    chips = []
    for slug, _ in EXISTING_HUBS:
        label = UZ_HUBS_INFO.get(slug, {}).get("chip_label", "Kolleksiya")
        active_cls = " active" if slug == current_slug else ""
        chips.append(f'        <a class="stone-chip{active_cls}" href="/uz/{slug}">{label}</a>')
    for h in ALL_HUBS:
        slug = h["slug"]
        label = UZ_HUBS_INFO.get(slug, {}).get("chip_label", h["chip_label"])
        active_cls = " active" if slug == current_slug else ""
        chips.append(f'        <a class="stone-chip{active_cls}" href="/uz/{slug}">{label}</a>')
    chips_str = "\n".join(chips)
    return f"""    <section class="hub-interlink-section" aria-label="Toshlar va uslublar boʻyicha toʻplamlar">
      <details class="hub-interlink-accordion">
        <summary>Toshlar va uslublar boʻyicha toʻplamlar</summary>
        <p class="hub-interlink-sub">Tabiiy minerallar va zargarlik buyumlarining mavzuviy toʻplamlariga oʻting</p>
        <div class="hub-interlink-chips">
{chips_str}
        </div>
      </details>
    </section>"""


def generate_hub_page(hub, products):
    slug = hub["slug"]
    canonical_url = f"{BASE_URL}/{slug}"
    kz_url = f"{BASE_URL}/kz/{slug}"
    uz_url = f"{BASE_URL}/uz/{slug}"
    matched_products, recommended_ids = match_products_for_hub(hub, products)

    prices = [int(p.get("price", 0)) for p in matched_products if int(p.get("price", 0)) > 0]
    min_price = min(prices) if prices else 25000
    max_price = max(prices) if prices else 91000
    min_fmt = f"{min_price:,}".replace(",", " ")
    max_fmt = f"{max_price:,}".replace(",", " ")

    page_title = hub.get("custom_title") or f"Купить {hub['title_cluster']} ручной работы — доставка по Казахстану | Livi Jewelry"
    meta_desc = hub.get("custom_meta_desc") or (
        f"Купить {hub['title_cluster']} ручной работы в Livi Jewelry. "
        f"Цены от {min_fmt} до {max_fmt} ₸. Натуральные камни и жемчуг, "
        f"подарочная упаковка и быстрая доставка СДЭК по Казахстану."
    )

    first_img = matched_products[0]["image"].lstrip("/") if matched_products else "assets/kole-iz-naturalnogo-zhemchuga-80000.webp"
    og_image = f"{BASE_URL}/{first_img}"

    # 1. BreadcrumbList Schema
    schema_breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Каталог", "item": f"{BASE_URL}/shop.html"},
            {"@type": "ListItem", "position": 3, "name": hub["breadcrumb"], "item": canonical_url},
        ],
    }

    # 2. ItemList Schema
    item_list_elements = []
    cards_html = []
    ga4_items = []

    for idx, p in enumerate(matched_products, start=1):
        pid = p["id"]
        ptitle = p["title"]
        pprice = int(p.get("price", 0))
        pprice_fmt = f"{pprice:,}".replace(",", " ")
        pimg_rel = p["image"].lstrip("/")
        pmats = ", ".join(p.get("materials", []))

        item_list_elements.append(build_product_schema_for_itemlist(p, idx, is_kz=False))

        rec_badge = ""
        if pid in recommended_ids:
            rec_badge = '<div style="font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:var(--gold);margin-bottom:4px;">Рекомендуемые изделия из коллекции</div>'

        alt_str = clean_attr(build_clean_alt(p))
        pimg_base, _ = os.path.splitext(pimg_rel)
        pimg_thumb = f"{pimg_base}-400w.webp"
        pimg_mob = f"{pimg_base}-750w.webp"
        srcset_attr = f' srcset="/{pimg_thumb} 400w, /{pimg_mob} 750w, /{pimg_rel} 1440w" sizes="(max-width: 768px) 50vw, 300px"'
        cards_html.append(f"""        <article class="card" data-id="{pid}" data-name="{clean_attr(ptitle)}" data-price="{pprice}" data-category="{clean_attr(p.get('category', 'Necklaces'))}" onclick="if(!event.target.closest('a'))location.href='/product/{pid}.html'">
          <div class="card-img-wrap">
            <img src="/{pimg_rel}"{srcset_attr} alt="{alt_str}" {"loading=\"eager\" fetchpriority=\"high\"" if idx <= 2 else ("loading=\"eager\"" if idx <= 8 else "loading=\"lazy\"")} decoding="async" width="600" height="800">
          </div>
          <div class="body">
            {rec_badge}
            <h3 class="title"><a href="/product/{pid}.html" class="card-title-link">{ptitle}</a></h3>
            <div class="price">{pprice_fmt} ₸</div>
            <div class="meta" style="font-size: 12px; color: var(--muted); margin-top: 4px;">{clean_attr(pmats)}</div>
          </div>
        </article>""")

        ga4_items.append({
            "item_id": pid,
            "item_name": ptitle,
            "price": pprice,
            "item_brand": "Livi Jewelry",
            "item_category": p.get("category", "Necklaces"),
            "index": idx
        })

    schema_itemlist = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{hub['h1']} — Livi Jewelry",
        "itemListElement": item_list_elements,
    }

    # 3. FAQPage Schema
    q1 = f"Как проверяется подлинность {hub['stone_name_gen']} в украшениях Livi Jewelry?"
    a1 = f"В ателье Livi Jewelry мы используем исключительно натуральные минералы и отборный культивированный жемчуг. Каждая партия {hub['stone_name_gen']} проходит ручную проверку мастером на природную плотность, характерную прохладу камня, естественные включения и глубину оттенка."
    q2 = f"Можно ли изменить длину или размер в {hub['stone_name_prep']}?"
    a2 = "Размеры каждого изделия указаны в карточке товара. По вопросам изменения длины колье, чокера или браслета напишите мастеру в WhatsApp — подскажем, возможно ли это для выбранной модели."
    q3 = "В какой упаковке доставляются украшения и какие сроки доставки по Казахстану?"
    a3 = "Каждое изделие бережно упаковывается в фирменную подарочную коробочку или бархатный мешочек Livi Jewelry (бесплатно). Доставка по Астане осуществляется курьером день в день, а в Алматы, Шымкент, Караганду и все города Казахстана — экспресс-службой СДЭК за 1–3 рабочих дня."

    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q1, "acceptedAnswer": {"@type": "Answer", "text": a1}},
            {"@type": "Question", "name": q2, "acceptedAnswer": {"@type": "Answer", "text": a2}},
            {"@type": "Question", "name": q3, "acceptedAnswer": {"@type": "Answer", "text": a3}},
        ],
    }

    drawer_hub_links = "\n".join(
        f'            <a href="/{s}">{clean_attr(l)}</a>'
        for s, l in EXISTING_HUBS + [(h["slug"], h["chip_label"]) for h in ALL_HUBS]
    )

    interlink_html = build_interlink_block_html(current_slug=slug, prefix="")
    cards_grid_str = "\n".join(cards_html)

    top_chips = []
    for s, l in EXISTING_HUBS:
        active_cls = " active" if s == slug else ""
        top_chips.append(f'      <a class="stone-chip{active_cls}" href="/{s}">{l}</a>')
    for h in ALL_HUBS:
        active_cls = " active" if h["slug"] == slug else ""
        top_chips.append(f'      <a class="stone-chip{active_cls}" href="/{h["slug"]}">{h["chip_label"]}</a>')
    top_chips_html = "\n".join(top_chips)

    page_html = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />

  <title>{clean_attr(page_title)}</title>
  <meta name="description" content="{clean_attr(meta_desc)}">
  <link rel="canonical" href="{canonical_url}">
  <link rel="alternate" hreflang="ru-KZ" href="{canonical_url}" />
  <link rel="alternate" hreflang="ru" href="{canonical_url}" />
  <link rel="alternate" hreflang="kk-KZ" href="{kz_url}" />
  <link rel="alternate" hreflang="kk" href="{kz_url}" />
  <link rel="alternate" hreflang="uz-UZ" href="{uz_url}" />
  <link rel="alternate" hreflang="uz" href="{uz_url}" />
  <link rel="alternate" hreflang="x-default" href="{canonical_url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="google-site-verification" content="qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0" />

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Livi Jewelry">
  <meta property="og:title" content="{clean_attr(page_title)}">
  <meta property="og:description" content="{clean_attr(meta_desc)}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">

  <!-- Fonts & Haute Joaillerie Design System -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">

  <!-- Icons & Manifest -->
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#141312">
  <meta name="msapplication-TileColor" content="#141312">

  <!-- Google tag (GA4 + Ads) -->
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
    gtag('config', 'G-YFF2TR0N36', {{
      'linker': {{ 'domains': ['livijewelry.kz', 'www.livijewelry.kz'], 'accept_incoming': true }}
    }});
    gtag('config', 'AW-16793974126', {{
      'allow_enhanced_conversions': true,
      'linker': {{ 'domains': ['livijewelry.kz', 'www.livijewelry.kz'], 'accept_incoming': true }}
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
    fbq('track', 'PageView');
    fbq('track', 'ViewContent', {{
      content_category: '{clean_attr(hub["breadcrumb"])}',
      content_name: '{clean_attr(hub["h1"])}',
      value: {min_price},
      currency: 'KZT'
    }});
  </script>


  <!-- JSON-LD: BreadcrumbList -->
  <script type="application/ld+json">
{json.dumps(schema_breadcrumbs, ensure_ascii=False, indent=2)}
  </script>

  <!-- JSON-LD: ItemList -->
  <script type="application/ld+json">
{json.dumps(schema_itemlist, ensure_ascii=False, indent=2)}
  </script>

  <!-- JSON-LD: FAQPage -->
  <script type="application/ld+json">
{json.dumps(schema_faq, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=199604456030882&ev=PageView&noscript=1"/></noscript>
  <!-- Drawer -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back" role="button" tabindex="0" aria-label="Закрыть меню"></div>
    <div class="drawer-panel" role="menu" aria-label="Меню">
      <a href="/">Главная</a>
      <a href="/shop.html">Каталог</a>
      <details class="drawer-accordion">
        <summary>Коллекции и камни</summary>
        <div class="drawer-subnav">
{drawer_hub_links}
        </div>
      </details>
      <a href="/komplekty-ukrasheniy.html">Комплекты украшений</a>
      <a href="/delivery.html">Доставка и оплата</a>
      <div class="drawer-socials">
        <a class="drawer-soc-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="drawer-soc-link" href="https://wa.me/77054510584?text=Здравствуйте!%20Подскажите,%20пожалуйста,%20по%20украшениям%20Livi%20Jewelry%20—%20хочу%20уточнить%20наличие%20и%20проконсультироваться%20✨" target="_blank" rel="noopener">WhatsApp</a>
      </div>
      <div class="lang">
        <a href="/{slug}" class="active">RU</a>
        <a href="/kz/{slug}" lang="kk">KZ</a>
        <a href="/uz/{slug}" lang="uz">UZ</a>
      </div>
    </div>
  </div>

  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Меню"><span></span></button>

      <a class="brand" href="/" aria-label="Livi Jewelry">
        <span>LIVI JEWELRY</span>
      </a>

      <div class="nav-actions">
        <a href="/shop.html?search=1" class="header-search-btn" aria-label="Поиск по каталогу">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </a>
        <div class="header-lang-links" aria-label="Выбор языка">
          <a href="/{slug}" class="active">RU</a>
          <a href="/kz/{slug}" lang="kk">KZ</a>
          <a href="/uz/{slug}" lang="uz">UZ</a>
        </div>
        <a class="cart-link" href="/cart.html" aria-label="Корзина">
          <span>Корзина</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
        <a class="quick-link ig-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener" aria-label="Instagram">
          <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
            <path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm5 5.5A4.5 4.5 0 1 0 16.5 12 4.505 4.505 0 0 0 12 7.5zm6.5-.75a1.25 1.25 0 1 0 1.25 1.25A1.25 1.25 0 0 0 18.5 6.75Zm-6.5 2A3.25 3.25 0 1 1 8.75 12 3.254 3.254 0 0 1 12 8.75Z"/>
          </svg>
        </a>
        <a class="quick-link wa-link" href="https://wa.me/77054510584?text=Здравствуйте!%20Подскажите,%20пожалуйста,%20по%20украшениям%20Livi%20Jewelry%20—%20хочу%20уточнить%20наличие%20и%20проконсультироваться%20✨" target="_blank" rel="noopener" aria-label="WhatsApp">
          <svg width="20" height="20" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
            <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
            <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
          </svg>
        </a>
      </div>
    </div>
  </header>

  <main class="wrap" style="padding-top: 24px;">
    <div class="collection-header" style="margin-bottom: 20px;">
      <h1 style="font-family: var(--font-serif); font-size: clamp(26px, 3.5vw, 38px); font-weight: 300; line-height: 1.25; margin: 0 0 8px; color: var(--fg);">{clean_attr(hub.get('h1', hub['chip_label']))}</h1>
      <p style="font-size: 13.5px; color: #777; line-height: 1.5; margin: 0; max-width: 720px; font-weight: 300;">{clean_attr(hub['lead'])}</p>
    </div>

    <!-- Навигационный блок: Подборки по камням и стилям (горизонтальная скролл-лента) -->
    <nav class="stone-chips" aria-label="Подборки по камням и стилям" style="margin: 0 0 24px;">
{top_chips_html}
    </nav>

    <div class="grid" id="grid">
{cards_grid_str}
    </div>

    <!-- SEO Editorial Text Section -->
    <section class="wrap seo-editorial-section" style="max-width: 860px; margin: 40px auto; padding: 0 16px;">
      <h2 style="font-family: var(--font-serif); font-size: 26px; font-weight: 400; margin-bottom: 16px; color: var(--gold);">{hub['seo_title']}</h2>
      <p style="line-height: 1.8; color: var(--muted); margin-bottom: 16px; font-size: 15px;">{hub['seo_p1']}</p>
      <p style="line-height: 1.8; color: var(--muted); margin-bottom: 24px; font-size: 15px;">{hub['seo_p2']}</p>
    </section>

    <!-- FAQ Accordion Block -->
    <section class="wrap" style="max-width: 860px; margin: 40px auto 60px; padding: 0 16px;">
      <h2 style="font-family: var(--font-serif); font-size: 26px; font-weight: 400; text-align: center; margin-bottom: 24px;">Часто задаваемые вопросы</h2>
      <details class="faq-item" style="border-bottom: 1px solid var(--border); padding: 14px 0;">
        <summary style="font-weight: 500; cursor: pointer; color: var(--fg);">{q1}</summary>
        <p style="color: var(--muted); margin-top: 8px; line-height: 1.6;">{a1}</p>
      </details>
      <details class="faq-item" style="border-bottom: 1px solid var(--border); padding: 14px 0;">
        <summary style="font-weight: 500; cursor: pointer; color: var(--fg);">{q2}</summary>
        <p style="color: var(--muted); margin-top: 8px; line-height: 1.6;">{a2}</p>
      </details>
      <details class="faq-item" style="border-bottom: 1px solid var(--border); padding: 14px 0;">
        <summary style="font-weight: 500; cursor: pointer; color: var(--fg);">{q3}</summary>
        <p style="color: var(--muted); margin-top: 8px; line-height: 1.6;">{a3}</p>
      </details>
    </section>

{interlink_html}
  </main>

{RU_FOOTER_HTML}

  <!-- Floating WhatsApp Widget -->
  <a class="floating-wa" href="https://wa.me/77054510584?text=Здравствуйте!%20Хочу%20получить%20консультацию%20по%20коллекции%20{clean_attr(hub['breadcrumb'])}." target="_blank" rel="noopener" aria-label="Консультация мастера в WhatsApp">
    <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
      <path fill="currentColor" d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
      <path fill="currentColor" d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
    </svg>
    <span class="floating-wa-text">Консультация мастера</span>
  </a>

  <script>
    (function() {{
      try {{
        const params = new URLSearchParams(window.location.search);
        const keys = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
        let existing = {{}};
        try {{ existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}') || {{}}; }} catch(e){{}}
        let updated = false;
        keys.forEach(k => {{ const v = params.get(k); if (v) {{ existing[k] = v; updated = true; }} }});
        if (!existing.landing_page) {{
          existing.landing_page = window.location.pathname + window.location.search;
          existing.referrer = document.referrer || 'direct';
          updated = true;
        }}
        if (updated) localStorage.setItem('livi_attribution', JSON.stringify(existing));
      }} catch(e){{}}
    }})();

    const drawer = document.getElementById('drawer');
    const burger = document.getElementById('burger');
    if (burger && drawer) {{
      burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false'); document.body.classList.add('drawer-open'); }};
      const back = drawer.querySelector('.drawer-back');
      if (back) back.onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden', 'true'); document.body.classList.remove('drawer-open'); }};
    }}

    function updateBadge() {{
      try {{
        const raw = localStorage.getItem('livi_cart_v3') || localStorage.getItem('livi_cart_v2') || '[]';
        const items = JSON.parse(raw);
        const count = Array.isArray(items) ? items.reduce((s, i) => s + Number(i.qty || 0), 0) : 0;
        const b = document.getElementById('cartBadge');
        if (b) {{
          b.textContent = count > 0 ? count : '';
          b.style.display = count > 0 ? 'inline-block' : 'none';
        }}
      }} catch (e) {{}}
    }}
    updateBadge();

    document.querySelectorAll('.grid .card').forEach((card, idx) => {{
      card.addEventListener('click', function() {{
        if (typeof gtag === 'function') {{
          const titleEl = card.querySelector('.card-title-link');
          const href = titleEl ? titleEl.getAttribute('href') || '' : '';
          const m = href.match(/(prod_\\d+)/);
          gtag('event', 'select_item', {{
            item_list_id: '{slug}',
            item_list_name: document.title,
            items: [{{ item_id: m ? m[1] : 'prod_01', item_name: titleEl ? titleEl.textContent.trim() : '', index: idx + 1 }}]
          }});
        }}
      }});
    }});

    // Отслеживание кликов по ссылкам WhatsApp на SEO-хабе
    document.addEventListener('click', function(e) {{
      const a = e.target.closest('a[href*="wa.me"], a[href*="whatsapp.com"]');
      if (!a) return;
      try {{
        if (window.fbq) {{
          fbq('track', 'Contact');
          fbq('track', 'Lead', {{
            content_name: document.title,
            currency: 'KZT'
          }});
        }}
        if (typeof gtag === 'function') {{
          gtag('event', 'whatsapp_click', {{
            currency: 'KZT',
            value: 40000,
            method: 'WhatsApp',
            page_location: window.location.href,
            lead_source: 'seo_hub'
          }});
          gtag('event', 'conversion', {{ 'send_to': 'AW-16793974126/dLz3CKyagbAdEO7q_sc-', 'value': 1.0, 'currency': 'USD', 'transport_type': 'beacon' }});
        }}
      }} catch (err) {{}}
    }});
  </script>
</body>
</html>
"""
    safe_write_text(slug, page_html)
    return slug


def generate_kz_hub_page(slug: str, hub_meta: dict, products: list):
    """Generates the static Kazakh version kz/{slug}."""
    os.makedirs("kz", exist_ok=True)
    out_path = os.path.join("kz", slug)
    canonical_url = f"{BASE_URL}/kz/{slug}"
    ru_url = f"{BASE_URL}/{slug}"
    uz_url = f"{BASE_URL}/uz/{slug}"

    from generate_kz_pages import KZ_TRANSLATIONS

    # Match products
    if slug == "kolye-iz-zhemchuga.html":
        matched = [p for p in products if not p.get("archived", False) and (p.get("category") in ("Necklaces", "Lariats") or "жемчуг" in (p.get("title", "") + " " + " ".join(p.get("materials", []))).lower())]
    elif slug == "braslety-iz-zhemchuga.html":
        matched = [p for p in products if not p.get("archived", False) and (p.get("category") == "Bracelets" or "браслет" in (p.get("title", "") + " " + " ".join(p.get("materials", []))).lower())]
    elif slug == "sergi-iz-zhemchuga.html":
        matched = [p for p in products if not p.get("archived", False) and "серьг" in (p.get("title", "") + " " + p.get("description", "") + " " + str(p.get("bundle_options", ""))).lower()]
    else:
        # Find hub dict in ALL_HUBS
        h_obj = next((h for h in ALL_HUBS if h["slug"] == slug), None)
        if h_obj:
            matched, _ = match_products_for_hub(h_obj, products)
        else:
            matched = [p for p in products if not p.get("archived", False)][:6]

    prices = [int(p.get("price", 0)) for p in matched if int(p.get("price", 0)) > 0]
    min_price = min(prices) if prices else 25000
    max_price = max(prices) if prices else 91000
    min_fmt = f"{min_price:,}".replace(",", " ")
    max_fmt = f"{max_price:,}".replace(",", " ")

    kz_info = KZ_HUBS_INFO.get(slug, {
        "chip_label": "Әшекейлер",
        "h1": "Табиғи тастардан жасалған әшекейлер — Livi Jewelry",
        "title_cluster": "әшекейлер",
        "breadcrumb": "Әшекейлер",
        "lead": "Табиғи інжу мен минералдардан қолдан жасалған авторлық әшекейлер. Қазақстан бойынша жедел жеткізу.",
        "seo_title": "Livi Jewelry шеберханасының эксклюзивті әшекейлері",
        "seo_p1": "Livi Jewelry шеберханасында әрбір зергерлік бұйым табиғи асыл тастардан қолмен жиналады.",
        "seo_p2": "СДЭК арқылы Қазақстанның кез келген қаласына жедел жеткізу қарастырылған.",
    })

    page_title = kz_info.get("custom_title") or f"{kz_info['h1']} — бағасы теңгемен сатып алу | Қолдан жасалған Livi Jewelry"
    meta_desc = kz_info.get("custom_meta_desc") or (
        f"{kz_info['lead']} Бағасы {min_fmt} ₸ — {max_fmt} ₸. "
        f"Табиғи тастар мен інжу, сыйлық қаптамасы және Қазақстан бойынша жылдам жеткізу."
    )

    first_img = matched[0]["image"].lstrip("/") if matched else "assets/kole-iz-naturalnogo-zhemchuga-80000.webp"
    og_image = f"{BASE_URL}/{first_img}"

    # Breadcrumbs Schema
    schema_breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Басты бет", "item": f"{BASE_URL}/kz/"},
            {"@type": "ListItem", "position": 2, "name": "Каталог", "item": f"{BASE_URL}/kz/shop.html"},
            {"@type": "ListItem", "position": 3, "name": kz_info["breadcrumb"], "item": canonical_url},
        ],
    }

    # ItemList Schema & Cards
    item_list_elements = []
    cards_html = []

    for idx, p in enumerate(matched, start=1):
        pid = p["id"]
        kz_t = KZ_TRANSLATIONS.get(pid, {})
        ptitle_kz = kz_t.get("title") or p["title"]
        pdesc_kz = kz_t.get("desc") or p.get("description") or ptitle_kz
        pprice = int(p.get("price", 0))
        pprice_fmt = f"{pprice:,}".replace(",", " ")
        pimg_rel = p["image"].lstrip("/")
        pmats = ", ".join(p.get("materials", []))

        item_list_elements.append(build_product_schema_for_itemlist(p, idx, is_kz=True, kz_title=ptitle_kz, kz_desc=pdesc_kz))

        alt_str = clean_attr(f"{ptitle_kz} — авторлық қолөнер туындысы, Livi Jewelry")
        pimg_base, _ = os.path.splitext(pimg_rel)
        pimg_thumb = f"{pimg_base}-400w.webp"
        pimg_mob = f"{pimg_base}-750w.webp"
        srcset_attr = f' srcset="/{pimg_thumb} 400w, /{pimg_mob} 750w, /{pimg_rel} 1440w" sizes="(max-width: 768px) 50vw, 300px"'
        cards_html.append(f"""        <article class="card" data-id="{pid}" data-name="{clean_attr(ptitle_kz)}" data-price="{pprice}" data-category="{clean_attr(p.get('category', 'Necklaces'))}" onclick="if(!event.target.closest('a'))location.href='/kz/product/{pid}.html'">
          <div class="card-img-wrap">
            <img src="/{pimg_rel}"{srcset_attr} alt="{alt_str}" {"loading=\"eager\" fetchpriority=\"high\"" if idx <= 2 else ("loading=\"eager\"" if idx <= 8 else "loading=\"lazy\"")} decoding="async" width="600" height="800">
          </div>
          <div class="body">
            <h3 class="title"><a href="/kz/product/{pid}.html" class="card-title-link">{ptitle_kz}</a></h3>
            <div class="price">{pprice_fmt} ₸</div>
            <div class="meta" style="font-size: 12px; color: var(--muted); margin-top: 4px;">{clean_attr(pmats)}</div>
          </div>
        </article>""")

    schema_itemlist = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{kz_info['h1']} — Livi Jewelry",
        "itemListElement": item_list_elements,
    }

    # FAQ Schema
    q1 = "Livi Jewelry әшекейлеріндегі тастар мен інжудің табиғи екені қалай тексеріледі?"
    a1 = "Livi Jewelry ательесінде біз тек табиғи минералдар мен таңдаулы культивацияланған інжуді пайдаланамыз. Әрбір партия шебердің жеке бақылауынан өтеді: тастың табиғи тығыздығы, салқындығы, табиғи құрылымы және түс тереңдігі тексеріледі."
    q2 = "Бұйымның ұзындығын немесе өлшемін өзгертуге бола ма?"
    a2 = "Әр бұйымның өлшемі карточкада көрсетілген. Ұзындықты өзгерту мүмкіндігін WhatsApp арқылы шеберден нақтылаңыз."
    q3 = "Әшекейлер қандай қаптамада жеткізіледі және Қазақстан бойынша жеткізу мерзімі қандай?"
    a3 = "Әрбір бұйым Livi Jewelry фирмалық сыйлық қорабына немесе барқыт дорбасына тегін салынады. Астана бойынша жеткізу курьермен сол күні, ал Алматы, Шымкент, Қарағанды және барлық өңірлерге СДЭК қызметімен 1–3 жұмыс күнінде жеткізіледі."

    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q1, "acceptedAnswer": {"@type": "Answer", "text": a1}},
            {"@type": "Question", "name": q2, "acceptedAnswer": {"@type": "Answer", "text": a2}},
            {"@type": "Question", "name": q3, "acceptedAnswer": {"@type": "Answer", "text": a3}},
        ],
    }

    drawer_hub_links_kz = "\n".join(
        f'            <a href="/kz/{s}">{clean_attr(KZ_HUBS_INFO.get(s, {}).get("chip_label", l))}</a>'
        for s, l in EXISTING_HUBS + [(h["slug"], h["chip_label"]) for h in ALL_HUBS]
    )

    top_chips = []
    for s, l in EXISTING_HUBS:
        lbl = KZ_HUBS_INFO.get(s, {}).get("chip_label", l)
        active_cls = " active" if s == slug else ""
        top_chips.append(f'      <a class="stone-chip{active_cls}" href="/kz/{s}">{lbl}</a>')
    for h in ALL_HUBS:
        lbl = KZ_HUBS_INFO.get(h["slug"], {}).get("chip_label", h["chip_label"])
        active_cls = " active" if h["slug"] == slug else ""
        top_chips.append(f'      <a class="stone-chip{active_cls}" href="/kz/{h["slug"]}">{lbl}</a>')
    top_chips_html = "\n".join(top_chips)

    cards_grid_str = "\n".join(cards_html)
    interlink_html = build_interlink_block_html_kz(current_slug=slug)

    page_html = f"""<!doctype html>
<html lang="kk">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />

  <title>{clean_attr(page_title)}</title>
  <meta name="description" content="{clean_attr(meta_desc)}">
  <link rel="canonical" href="{canonical_url}">
  <link rel="alternate" hreflang="ru-KZ" href="{ru_url}" />
  <link rel="alternate" hreflang="ru" href="{ru_url}" />
  <link rel="alternate" hreflang="kk-KZ" href="{canonical_url}" />
  <link rel="alternate" hreflang="kk" href="{canonical_url}" />
  <link rel="alternate" hreflang="uz-UZ" href="{uz_url}" />
  <link rel="alternate" hreflang="uz" href="{uz_url}" />
  <link rel="alternate" hreflang="x-default" href="{ru_url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="google-site-verification" content="qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0" />

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Livi Jewelry">
  <meta property="og:title" content="{clean_attr(page_title)}">
  <meta property="og:description" content="{clean_attr(meta_desc)}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">

  <!-- Fonts & Design System -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">

  <!-- Icons & Manifest -->
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#141312">
  <meta name="msapplication-TileColor" content="#141312">

  <!-- Google tag (GA4 + Ads) -->
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
    gtag('config', 'G-YFF2TR0N36', {{
      'linker': {{ 'domains': ['livijewelry.kz', 'www.livijewelry.kz'], 'accept_incoming': true }}
    }});
    gtag('config', 'AW-16793974126', {{
      'allow_enhanced_conversions': true,
      'linker': {{ 'domains': ['livijewelry.kz', 'www.livijewelry.kz'], 'accept_incoming': true }}
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
    fbq('track', 'PageView');
    fbq('track', 'ViewContent', {{
      content_category: '{clean_attr(kz_info["breadcrumb"])}',
      content_name: '{clean_attr(kz_info["h1"])}',
      value: {min_price},
      currency: 'KZT'
    }});
  </script>


  <!-- JSON-LD: BreadcrumbList -->
  <script type="application/ld+json">
{json.dumps(schema_breadcrumbs, ensure_ascii=False, indent=2)}
  </script>

  <!-- JSON-LD: ItemList -->
  <script type="application/ld+json">
{json.dumps(schema_itemlist, ensure_ascii=False, indent=2)}
  </script>

  <!-- JSON-LD: FAQPage -->
  <script type="application/ld+json">
{json.dumps(schema_faq, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=199604456030882&ev=PageView&noscript=1"/></noscript>
  <!-- Drawer -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back" role="button" tabindex="0" aria-label="Мәзірді жабу"></div>
    <div class="drawer-panel" role="menu" aria-label="Мәзір">
      <a href="/kz/">Басты бет</a>
      <a href="/kz/shop.html">Каталог</a>
      <details class="drawer-accordion">
        <summary>Коллекциялар мен тастар</summary>
        <div class="drawer-subnav">
{drawer_hub_links_kz}
        </div>
      </details>
      <a href="/kz/komplekty-ukrasheniy.html">Әшекейлер жиынтығы</a>
      <a href="/delivery.html">Жеткізу және төлем</a>
      <div class="drawer-socials">
        <a class="drawer-soc-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="drawer-soc-link" href="https://wa.me/77054510584?text=Сәлеметсіз%20бе!%20Livi%20Jewelry%20әшекейін%20қалаймын." target="_blank" rel="noopener">WhatsApp</a>
      </div>
      <div class="lang">
        <a href="/{slug}">RU</a>
        <a href="/kz/{slug}" class="active" lang="kk">KZ</a>
        <a href="/uz/{slug}" lang="uz">UZ</a>
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
        <a href="/kz/shop.html?search=1" class="header-search-btn" aria-label="Іздеу">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </a>
        <div class="header-lang-links" aria-label="Тілді таңдау">
          <a href="/{slug}">RU</a>
          <a href="/kz/{slug}" class="active" lang="kk">KZ</a>
          <a href="/uz/{slug}" lang="uz">UZ</a>
        </div>
        <a class="cart-link" href="/cart.html" aria-label="Себет">
          <span>Себет</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
        <a class="quick-link ig-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener" aria-label="Instagram">
          <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
            <path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm5 5.5A4.5 4.5 0 1 0 16.5 12 4.505 4.505 0 0 0 12 7.5zm6.5-.75a1.25 1.25 0 1 0 1.25 1.25A1.25 1.25 0 0 0 18.5 6.75Zm-6.5 2A3.25 3.25 0 1 1 8.75 12 3.254 3.254 0 0 1 12 8.75Z"/>
          </svg>
        </a>
        <a class="quick-link wa-link" href="https://wa.me/77054510584?text=Сәлеметсіз%20бе!%20Livi%20Jewelry%20әшекейлері%20бойынша%20кеңес%20алғым%20келеді." target="_blank" rel="noopener" aria-label="WhatsApp">
          <svg width="20" height="20" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
            <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
            <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
          </svg>
        </a>
      </div>
    </div>
  </header>

  <main class="wrap" style="padding-top: 24px;">
    <div class="collection-header" style="margin-bottom: 20px;">
      <h1 style="font-family: var(--font-serif); font-size: clamp(26px, 3.5vw, 38px); font-weight: 300; line-height: 1.25; margin: 0 0 8px; color: var(--fg);">{clean_attr(kz_info['chip_label'])}</h1>
      <p style="font-size: 13.5px; color: #777; line-height: 1.5; margin: 0; max-width: 720px; font-weight: 300;">{clean_attr(kz_info['lead'])}</p>
    </div>

    <!-- Навигация: Тастар мен стильдер -->
    <nav class="stone-chips" aria-label="Тастар мен стильдер бойынша жинақтар" style="margin: 0 0 24px;">
{top_chips_html}
    </nav>

    <div class="grid" id="grid">
{cards_grid_str}
    </div>

    <!-- SEO Редакциялық Мәтін -->
    <section class="wrap seo-editorial-section" style="max-width: 860px; margin: 40px auto; padding: 0 16px;">
      <h2 style="font-family: var(--font-serif); font-size: 26px; font-weight: 400; margin-bottom: 16px; color: var(--gold);">{kz_info['seo_title']}</h2>
      <p style="line-height: 1.8; color: var(--muted); margin-bottom: 16px; font-size: 15px;">{kz_info['seo_p1']}</p>
      <p style="line-height: 1.8; color: var(--muted); margin-bottom: 24px; font-size: 15px;">{kz_info['seo_p2']}</p>
    </section>

    <!-- FAQ Жиі қойылатын сұрақтар -->
    <section class="wrap" style="max-width: 860px; margin: 40px auto 60px; padding: 0 16px;">
      <h2 style="font-family: var(--font-serif); font-size: 26px; font-weight: 400; text-align: center; margin-bottom: 24px;">Жиі қойылатын сұрақтар</h2>
      <details class="faq-item" style="border-bottom: 1px solid var(--border); padding: 14px 0;">
        <summary style="font-weight: 500; cursor: pointer; color: var(--fg);">{q1}</summary>
        <p style="color: var(--muted); margin-top: 8px; line-height: 1.6;">{a1}</p>
      </details>
      <details class="faq-item" style="border-bottom: 1px solid var(--border); padding: 14px 0;">
        <summary style="font-weight: 500; cursor: pointer; color: var(--fg);">{q2}</summary>
        <p style="color: var(--muted); margin-top: 8px; line-height: 1.6;">{a2}</p>
      </details>
      <details class="faq-item" style="border-bottom: 1px solid var(--border); padding: 14px 0;">
        <summary style="font-weight: 500; cursor: pointer; color: var(--fg);">{q3}</summary>
        <p style="color: var(--muted); margin-top: 8px; line-height: 1.6;">{a3}</p>
      </details>
    </section>

{interlink_html}
  </main>

{KZ_FOOTER_HTML}

  <!-- Floating WhatsApp Widget -->
  <a class="floating-wa" href="https://wa.me/77054510584?text=Сәлеметсіз%20бе!%20Livi%20Jewelry%20әшекейлері%20бойынша%20кеңес%20алғым%20келеді." target="_blank" rel="noopener" aria-label="Шеберден кеңес алу">
    <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
      <path fill="currentColor" d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
      <path fill="currentColor" d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
    </svg>
    <span class="floating-wa-text">Шеберден кеңес алу</span>
  </a>

  <script>
    (function() {{
      try {{
        const params = new URLSearchParams(window.location.search);
        const keys = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
        let existing = {{}};
        try {{ existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}') || {{}}; }} catch(e){{}}
        let updated = false;
        keys.forEach(k => {{ const v = params.get(k); if (v) {{ existing[k] = v; updated = true; }} }});
        if (!existing.landing_page) {{
          existing.landing_page = window.location.pathname + window.location.search;
          existing.referrer = document.referrer || 'direct';
          updated = true;
        }}
        if (updated) localStorage.setItem('livi_attribution', JSON.stringify(existing));
      }} catch(e){{}}
    }})();

    const drawer = document.getElementById('drawer');
    const burger = document.getElementById('burger');
    if (burger && drawer) {{
      burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false'); document.body.classList.add('drawer-open'); }};
      const back = drawer.querySelector('.drawer-back');
      if (back) back.onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden', 'true'); document.body.classList.remove('drawer-open'); }};
    }}

    function updateBadge() {{
      try {{
        const raw = localStorage.getItem('livi_cart_v3') || localStorage.getItem('livi_cart_v2') || '[]';
        const items = JSON.parse(raw);
        const count = Array.isArray(items) ? items.reduce((s, i) => s + Number(i.qty || 0), 0) : 0;
        const b = document.getElementById('cartBadge');
        if (b) {{
          b.textContent = count > 0 ? count : '';
          b.style.display = count > 0 ? 'inline-block' : 'none';
        }}
      }} catch (e) {{}}
    }}
    updateBadge();

    document.querySelectorAll('.grid .card').forEach((card, idx) => {{
      card.addEventListener('click', function() {{
        if (typeof gtag === 'function') {{
          const titleEl = card.querySelector('.card-title-link');
          const href = titleEl ? titleEl.getAttribute('href') || '' : '';
          const m = href.match(/(prod_\\d+)/);
          gtag('event', 'select_item', {{
            item_list_id: '{slug}',
            item_list_name: document.title,
            items: [{{ item_id: m ? m[1] : 'prod_01', item_name: titleEl ? titleEl.textContent.trim() : '', index: idx + 1 }}]
          }});
        }}
      }});
    }});

    // Отслеживание кликов по ссылкам WhatsApp на SEO-хабе
    document.addEventListener('click', function(e) {{
      const a = e.target.closest('a[href*="wa.me"], a[href*="whatsapp.com"]');
      if (!a) return;
      try {{
        if (window.fbq) {{
          fbq('track', 'Contact');
          fbq('track', 'Lead', {{
            content_name: document.title,
            currency: 'KZT'
          }});
        }}
        if (typeof gtag === 'function') {{
          gtag('event', 'whatsapp_click', {{
            currency: 'KZT',
            value: 40000,
            method: 'WhatsApp',
            page_location: window.location.href,
            lead_source: 'seo_hub'
          }});
          gtag('event', 'conversion', {{ 'send_to': 'AW-16793974126/dLz3CKyagbAdEO7q_sc-', 'value': 1.0, 'currency': 'USD', 'transport_type': 'beacon' }});
        }}
      }} catch (err) {{}}
    }});
  </script>
</body>
</html>
"""
    safe_write_text(out_path, page_html)
    return out_path



def generate_uz_hub_page(slug: str, hub_meta: dict, products: list):
    """Generates the static Uzbek version uz/{slug}."""
    os.makedirs("uz", exist_ok=True)
    out_path = os.path.join("uz", slug)
    canonical_url = f"{BASE_URL}/uz/{slug}"
    ru_url = f"{BASE_URL}/{slug}"
    kz_url = f"{BASE_URL}/kz/{slug}"

    from generate_uz_pages import UZ_TRANSLATIONS

    # Match products
    if slug == "kolye-iz-zhemchuga.html":
        matched = [p for p in products if not p.get("archived", False) and (p.get("category") in ("Necklaces", "Lariats") or "жемчуг" in (p.get("title", "") + " " + " ".join(p.get("materials", []))).lower())]
    elif slug == "braslety-iz-zhemchuga.html":
        matched = [p for p in products if not p.get("archived", False) and (p.get("category") == "Bracelets" or "браслет" in (p.get("title", "") + " " + " ".join(p.get("materials", []))).lower())]
    elif slug == "sergi-iz-zhemchuga.html":
        matched = [p for p in products if not p.get("archived", False) and "серьг" in (p.get("title", "") + " " + p.get("description", "") + " " + str(p.get("bundle_options", ""))).lower()]
    else:
        # Find hub dict in ALL_HUBS
        h_obj = next((h for h in ALL_HUBS if h["slug"] == slug), None)
        if h_obj:
            matched, _ = match_products_for_hub(h_obj, products)
        else:
            matched = [p for p in products if not p.get("archived", False)][:6]

    prices = [int(p.get("price", 0)) for p in matched if int(p.get("price", 0)) > 0]
    min_price = min(prices) if prices else 25000
    max_price = max(prices) if prices else 91000
    min_fmt = f"{min_price:,}".replace(",", " ")
    max_fmt = f"{max_price:,}".replace(",", " ")

    uz_info = UZ_HUBS_INFO.get(slug, {
        "chip_label": "Taqinchoqlar",
        "h1": "Tabiiy toshlardan taqinchoqlar — Livi Jewelry",
        "title_cluster": "taqinchoqlar",
        "breadcrumb": "Taqinchoqlar",
        "lead": "Tabiiy marvarid va minerallardan qoʻlda yasalgan mualliflik zargarlik buyumlari. Oʻzbekiston va Qozogʻiston boʻylab tezkor yetkazib berish.",
        "seo_title": "Livi Jewelry ustaxonasining eksklyuziv taqinchoqlari",
        "seo_p1": "Livi Jewelry ustaxonasida har bir zargarlik buyumi tabiiy asil toshlardan qoʻlda yigʻiladi.",
        "seo_p2": "SDEK orqali Oʻzbekistonning istalgan shahriga ishonchli yetkazib berish mavjud.",
    })

    page_title = f"{uz_info['h1']} — narxi tenge bilan sotib olish | Qoʻl mehnati Livi Jewelry"
    meta_desc = (
        f"{uz_info['lead']} Narxi {min_fmt} ₸ — {max_fmt} ₸. "
        f"Tabiiy toshlar va marvarid, sovgʻa qadoqlanishi va Oʻzbekistonga tezkor yetkazib berish."
    )

    first_img = matched[0]["image"].lstrip("/") if matched else "assets/kole-iz-naturalnogo-zhemchuga-80000.webp"
    og_image = f"{BASE_URL}/{first_img}"

    # Breadcrumbs Schema
    schema_breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Bosh sahifa", "item": f"{BASE_URL}/uz/"},
            {"@type": "ListItem", "position": 2, "name": "Katalog", "item": f"{BASE_URL}/uz/shop.html"},
            {"@type": "ListItem", "position": 3, "name": uz_info["breadcrumb"], "item": canonical_url},
        ],
    }

    # ItemList Schema & Cards
    item_list_elements = []
    cards_html = []

    for idx, p in enumerate(matched, start=1):
        pid = p["id"]
        uz_t = UZ_TRANSLATIONS.get(pid, {})
        ptitle_uz = uz_t.get("title") or p["title"]
        pdesc_uz = uz_t.get("desc") or p.get("description") or ptitle_uz
        pprice = int(p.get("price", 0))
        pprice_fmt = f"{pprice:,}".replace(",", " ")
        pimg_rel = p["image"].lstrip("/")
        pmats = ", ".join(uz_t.get("materials") or p.get("materials", []))

        item_list_elements.append(build_product_schema_for_itemlist(p, idx, is_uz=True, uz_title=ptitle_uz, uz_desc=pdesc_uz))

        alt_str = clean_attr(f"{ptitle_uz} — mualliflik qoʻl mehnati buyumi, Livi Jewelry")
        pimg_base, _ = os.path.splitext(pimg_rel)
        pimg_thumb = f"{pimg_base}-400w.webp"
        pimg_mob = f"{pimg_base}-750w.webp"
        srcset_attr = f' srcset="/{pimg_thumb} 400w, /{pimg_mob} 750w, /{pimg_rel} 1440w" sizes="(max-width: 768px) 50vw, 300px"'
        cards_html.append(f"""        <article class="card" data-id="{pid}" data-name="{clean_attr(ptitle_uz)}" data-price="{pprice}" data-category="{clean_attr(p.get('category', 'Necklaces'))}" onclick="if(!event.target.closest('a'))location.href='/uz/product/{pid}.html'">
          <div class="card-img-wrap">
            <img src="/{pimg_rel}"{srcset_attr} alt="{alt_str}" {"loading=\"eager\" fetchpriority=\"high\"" if idx <= 2 else ("loading=\"eager\"" if idx <= 8 else "loading=\"lazy\"")} decoding="async" width="600" height="800">
          </div>
          <div class="body">
            <h3 class="title"><a href="/uz/product/{pid}.html" class="card-title-link">{ptitle_uz}</a></h3>
            <div class="price">{pprice_fmt} ₸</div>
            <div class="meta" style="font-size: 12px; color: var(--muted); margin-top: 4px;">{clean_attr(pmats)}</div>
          </div>
        </article>""")

    schema_itemlist = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{uz_info['h1']} — Livi Jewelry",
        "itemListElement": item_list_elements,
    }

    # FAQ Schema
    q1 = "Livi Jewelry taqinchoqlaridagi toshlar va marvaridning tabiiyligi qanday tekshiriladi?"
    a1 = "Livi Jewelry atelyesida biz faqat tabiiy minerallar va saralangan yetishtirilgan marvariddan foydalanamiz. Har bir partiya ustaning shaxsiy nazoratidan oʻtadi: toshning tabiiy zichligi, salqinligi, tabiiy tuzilishi va rang chuqurligi sinchiklab tekshiriladi."
    q2 = "Buyumning uzunligini yoki oʻlchamini oʻzgartirish mumkinmi?"
    a2 = "Har bir buyumning oʻlchami kartochkada koʻrsatilgan. Uzunlikni oʻzgartirish imkoniyatini ustadan WhatsApp orqali aniqlang."
    q3 = "Taqinchoqlar qanday qadoqda yetkaziladi va Oʻzbekistonga yetkazib berish shartlari qanday?"
    a3 = "Har bir buyum Livi Jewelry firma sovgʻa qutisi yoki baxmal xaltachasiga bepul qadoqlanadi. Oʻzbekistonga (Toshkent, Samarqand, Buxoro va barcha viloyatlarga) SDEK yoki Qazpost orqali kuzatuv (trek) raqami bilan yetkaziladi."

    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q1, "acceptedAnswer": {"@type": "Answer", "text": a1}},
            {"@type": "Question", "name": q2, "acceptedAnswer": {"@type": "Answer", "text": a2}},
            {"@type": "Question", "name": q3, "acceptedAnswer": {"@type": "Answer", "text": a3}},
        ],
    }

    drawer_hub_links_uz = "\n".join(
        f'            <a href="/uz/{s}">{clean_attr(UZ_HUBS_INFO.get(s, {}).get("chip_label", l))}</a>'
        for s, l in EXISTING_HUBS + [(h["slug"], h["chip_label"]) for h in ALL_HUBS]
    )

    top_chips = []
    for s, l in EXISTING_HUBS:
        lbl = UZ_HUBS_INFO.get(s, {}).get("chip_label", l)
        active_cls = " active" if s == slug else ""
        top_chips.append(f'      <a class="stone-chip{active_cls}" href="/uz/{s}">{lbl}</a>')
    for h in ALL_HUBS:
        lbl = UZ_HUBS_INFO.get(h["slug"], {}).get("chip_label", h["chip_label"])
        active_cls = " active" if h["slug"] == slug else ""
        top_chips.append(f'      <a class="stone-chip{active_cls}" href="/uz/{h["slug"]}">{lbl}</a>')
    top_chips_html = "\n".join(top_chips)

    cards_grid_str = "\n".join(cards_html)
    interlink_html = build_interlink_block_html_uz(current_slug=slug)

    page_html = f"""<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />

  <title>{clean_attr(page_title)}</title>
  <meta name="description" content="{clean_attr(meta_desc)}">
  <link rel="canonical" href="{canonical_url}">
  <link rel="alternate" hreflang="ru-KZ" href="{ru_url}" />
  <link rel="alternate" hreflang="ru" href="{ru_url}" />
  <link rel="alternate" hreflang="kk-KZ" href="{kz_url}" />
  <link rel="alternate" hreflang="kk" href="{kz_url}" />
  <link rel="alternate" hreflang="uz-UZ" href="{canonical_url}" />
  <link rel="alternate" hreflang="uz" href="{canonical_url}" />
  <link rel="alternate" hreflang="x-default" href="{ru_url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="google-site-verification" content="qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0" />

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Livi Jewelry">
  <meta property="og:title" content="{clean_attr(page_title)}">
  <meta property="og:description" content="{clean_attr(meta_desc)}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:locale" content="uz_UZ">
  <meta name="twitter:card" content="summary_large_image">

  <!-- Fonts & Design System -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">

  <!-- Icons & Manifest -->
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#141312">
  <meta name="msapplication-TileColor" content="#141312">

  <!-- Google tag (GA4 + Ads) -->
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
    gtag('config', 'G-YFF2TR0N36', {{
      'linker': {{ 'domains': ['livijewelry.kz', 'www.livijewelry.kz'], 'accept_incoming': true }}
    }});
    gtag('config', 'AW-16793974126', {{
      'allow_enhanced_conversions': true,
      'linker': {{ 'domains': ['livijewelry.kz', 'www.livijewelry.kz'], 'accept_incoming': true }}
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
    fbq('track', 'PageView');
    fbq('track', 'ViewContent', {{
      content_category: '{clean_attr(uz_info["breadcrumb"])}',
      content_name: '{clean_attr(uz_info["h1"])}',
      value: {min_price},
      currency: 'KZT'
    }});
  </script>


  <!-- JSON-LD: BreadcrumbList -->
  <script type="application/ld+json">
{json.dumps(schema_breadcrumbs, ensure_ascii=False, indent=2)}
  </script>

  <!-- JSON-LD: ItemList -->
  <script type="application/ld+json">
{json.dumps(schema_itemlist, ensure_ascii=False, indent=2)}
  </script>

  <!-- JSON-LD: FAQPage -->
  <script type="application/ld+json">
{json.dumps(schema_faq, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=199604456030882&ev=PageView&noscript=1"/></noscript>
  <!-- Drawer -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back" role="button" tabindex="0" aria-label="Menyuni yopish"></div>
    <div class="drawer-panel" role="menu" aria-label="Menyu">
      <a href="/uz/">Bosh sahifa</a>
      <a href="/uz/shop.html">Katalog</a>
      <details class="drawer-accordion">
        <summary>Kolleksiyalar va toshlar</summary>
        <div class="drawer-subnav">
{drawer_hub_links_uz}
        </div>
      </details>
      <a href="/uz/komplekty-ukrasheniy.html">Taqinchoqlar toʻplami</a>
      <a href="/uz/delivery.html">Yetkazib berish va toʻlov</a>
      <div class="drawer-socials">
        <a class="drawer-soc-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="drawer-soc-link" href="https://wa.me/77054510584?text=Assalomu%20alaykum!%20Livi%20Jewelry%20taqinchoqlari%20boʻyicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener">WhatsApp</a>
      </div>
      <div class="lang">
        <a href="/{slug}">RU</a>
        <a href="/kz/{slug}" lang="kk">KZ</a>
        <a href="/uz/{slug}" class="active" lang="uz">UZ</a>
      </div>
    </div>
  </div>

  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Menyu"><span></span></button>

      <a class="brand" href="/uz/" aria-label="Livi Jewelry">
        <span>LIVI JEWELRY</span>
      </a>

      <div class="nav-actions">
        <a href="/uz/shop.html?search=1" class="header-search-btn" aria-label="Qidirish">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </a>
        <div class="header-lang-links" aria-label="Tilni tanlash">
          <a href="/{slug}">RU</a>
          <a href="/kz/{slug}" lang="kk">KZ</a>
          <a href="/uz/{slug}" class="active" lang="uz">UZ</a>
        </div>
        <a class="cart-link" href="/uz/cart.html" aria-label="Savat">
          <span>Savat</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
        <a class="quick-link ig-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener" aria-label="Instagram">
          <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
            <path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm5 5.5A4.5 4.5 0 1 0 16.5 12 4.505 4.505 0 0 0 12 7.5zm6.5-.75a1.25 1.25 0 1 0 1.25 1.25A1.25 1.25 0 0 0 18.5 6.75Zm-6.5 2A3.25 3.25 0 1 1 8.75 12 3.254 3.254 0 0 1 12 8.75Z"/>
          </svg>
        </a>
        <a class="quick-link wa-link" href="https://wa.me/77054510584?text=Assalomu%20alaykum!%20Livi%20Jewelry%20taqinchoqlari%20boʻyicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener" aria-label="WhatsApp">
          <svg width="20" height="20" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
            <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
            <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
          </svg>
        </a>
      </div>
    </div>
  </header>

  <main class="wrap" style="padding-top: 24px;">
    <div class="collection-header" style="margin-bottom: 20px;">
      <h1 style="font-family: var(--font-serif); font-size: clamp(26px, 3.5vw, 38px); font-weight: 300; line-height: 1.25; margin: 0 0 8px; color: var(--fg);">{clean_attr(uz_info['chip_label'])}</h1>
      <p style="font-size: 13.5px; color: #777; line-height: 1.5; margin: 0; max-width: 720px; font-weight: 300;">{clean_attr(uz_info['lead'])}</p>
    </div>

    <!-- Navigatsiya: Toshlar va uslublar -->
    <nav class="stone-chips" aria-label="Toshlar va uslublar boʻyicha toʻplamlar" style="margin: 0 0 24px;">
{top_chips_html}
    </nav>

    <div class="grid" id="grid">
{cards_grid_str}
    </div>

    <!-- SEO Tahririy Matn -->
    <section class="wrap seo-editorial-section" style="max-width: 860px; margin: 40px auto; padding: 0 16px;">
      <h2 style="font-family: var(--font-serif); font-size: 26px; font-weight: 400; margin-bottom: 16px; color: var(--gold);">{uz_info['seo_title']}</h2>
      <p style="line-height: 1.8; color: var(--muted); margin-bottom: 16px; font-size: 15px;">{uz_info['seo_p1']}</p>
      <p style="line-height: 1.8; color: var(--muted); margin-bottom: 24px; font-size: 15px;">{uz_info['seo_p2']}</p>
    </section>

    <!-- FAQ Tez-tez beriladigan savollar -->
    <section class="wrap" style="max-width: 860px; margin: 40px auto 60px; padding: 0 16px;">
      <h2 style="font-family: var(--font-serif); font-size: 26px; font-weight: 400; text-align: center; margin-bottom: 24px;">Tez-tez beriladigan savollar</h2>
      <details class="faq-item" style="border-bottom: 1px solid var(--border); padding: 14px 0;">
        <summary style="font-weight: 500; cursor: pointer; color: var(--fg);">{q1}</summary>
        <p style="color: var(--muted); margin-top: 8px; line-height: 1.6;">{a1}</p>
      </details>
      <details class="faq-item" style="border-bottom: 1px solid var(--border); padding: 14px 0;">
        <summary style="font-weight: 500; cursor: pointer; color: var(--fg);">{q2}</summary>
        <p style="color: var(--muted); margin-top: 8px; line-height: 1.6;">{a2}</p>
      </details>
      <details class="faq-item" style="border-bottom: 1px solid var(--border); padding: 14px 0;">
        <summary style="font-weight: 500; cursor: pointer; color: var(--fg);">{q3}</summary>
        <p style="color: var(--muted); margin-top: 8px; line-height: 1.6;">{a3}</p>
      </details>
    </section>

{interlink_html}
  </main>

{UZ_FOOTER_HTML}

  <!-- Floating WhatsApp Widget -->
  <a class="floating-wa" href="https://wa.me/77054510584?text=Assalomu%20alaykum!%20Livi%20Jewelry%20taqinchoqlari%20boʻyicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener" aria-label="Ustadan maslahat olish">
    <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
      <path fill="currentColor" d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
      <path fill="currentColor" d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
    </svg>
    <span class="floating-wa-text">Ustadan maslahat olish</span>
  </a>

  <script>
    (function() {{
      try {{
        const params = new URLSearchParams(window.location.search);
        const keys = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
        let existing = {{}};
        try {{ existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}') || {{}}; }} catch(e){{}}
        let updated = false;
        keys.forEach(k => {{ const v = params.get(k); if (v) {{ existing[k] = v; updated = true; }} }});
        if (!existing.landing_page) {{
          existing.landing_page = window.location.pathname + window.location.search;
          existing.referrer = document.referrer || 'direct';
          updated = true;
        }}
        if (updated) localStorage.setItem('livi_attribution', JSON.stringify(existing));
      }} catch(e){{}}
    }})();

    const drawer = document.getElementById('drawer');
    const burger = document.getElementById('burger');
    if (burger && drawer) {{
      burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false'); document.body.classList.add('drawer-open'); }};
      const back = drawer.querySelector('.drawer-back');
      if (back) back.onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden', 'true'); document.body.classList.remove('drawer-open'); }};
    }}

    function updateBadge() {{
      try {{
        const raw = localStorage.getItem('livi_cart_v3') || localStorage.getItem('livi_cart_v2') || '[]';
        const items = JSON.parse(raw);
        const count = Array.isArray(items) ? items.reduce((s, i) => s + Number(i.qty || 0), 0) : 0;
        const b = document.getElementById('cartBadge');
        if (b) {{
          b.textContent = count > 0 ? count : '';
          b.style.display = count > 0 ? 'inline-block' : 'none';
        }}
      }} catch (e) {{}}
    }}
    updateBadge();

    document.querySelectorAll('.grid .card').forEach((card, idx) => {{
      card.addEventListener('click', function() {{
        if (typeof gtag === 'function') {{
          const titleEl = card.querySelector('.card-title-link');
          const href = titleEl ? titleEl.getAttribute('href') || '' : '';
          const m = href.match(/(prod_\\d+)/);
          gtag('event', 'select_item', {{
            item_list_id: '{slug}',
            item_list_name: document.title,
            items: [{{ item_id: m ? m[1] : 'prod_01', item_name: titleEl ? titleEl.textContent.trim() : '', index: idx + 1 }}]
          }});
        }}
      }});
    }});

    // Отслеживание кликов по ссылкам WhatsApp на SEO-хабе
    document.addEventListener('click', function(e) {{
      const a = e.target.closest('a[href*="wa.me"], a[href*="whatsapp.com"]');
      if (!a) return;
      try {{
        if (window.fbq) {{
          fbq('track', 'Contact');
          fbq('track', 'Lead', {{
            content_name: document.title,
            currency: 'KZT'
          }});
        }}
        if (typeof gtag === 'function') {{
          gtag('event', 'whatsapp_click', {{
            currency: 'KZT',
            value: 40000,
            method: 'WhatsApp',
            page_location: window.location.href,
            lead_source: 'seo_hub'
          }});
          gtag('event', 'conversion', {{ 'send_to': 'AW-16793974126/dLz3CKyagbAdEO7q_sc-', 'value': 1.0, 'currency': 'USD', 'transport_type': 'beacon' }});
        }}
      }} catch (err) {{}}
    }});
  </script>
</body>
</html>
"""
    safe_write_text(out_path, page_html)
    return out_path


def update_sergi_page(products: list):
    """
    Renders all sets that include earrings on sergi-iz-zhemchuga.html,
    with explicit badge 'Серьги доступны отдельно или в комплекте' and distinct price from bundle_options.
    Also injects ItemList Schema with aggregateRating, review, and bidirectional hreflang links.
    """
    path = "sergi-iz-zhemchuga.html"
    if not os.path.exists(path):
        return

    earring_prods = []
    for p in products:
        blob = (p.get("title", "") + " " + p.get("description", "") + " " + str(p.get("bundle_options", ""))).lower()
        if "серьг" in blob:
            earring_prods.append(p)

    earring_prods.sort(key=lambda x: x["id"])

    cards_html = []
    item_list_elements = []

    for idx, p in enumerate(earring_prods, start=1):
        pid = p["id"]
        title = clean_attr(p["title"])
        price = int(p.get("price", 0))
        price_fmt = f"{price:,}".replace(",", " ")
        img = p["image"].lstrip("/")
        alt_str = clean_attr(build_clean_alt(p))
        mats_str = clean_attr(", ".join(p.get("materials", [])))

        earring_price = int(p.get("price") or 10000)
        for opt in p.get("bundle_options", []):
            if "серьг" in opt.get("name", "").lower():
                earring_price = opt.get("price", earring_price)
                break
        earring_price_fmt = f"{earring_price:,}".replace(",", " ")

        img_base, _ = os.path.splitext(img)
        img_thumb = f"{img_base}-400w.webp"
        img_mob = f"{img_base}-750w.webp"
        srcset_attr = f' srcset="/{img_thumb} 400w, /{img_mob} 750w, /{img} 1440w" sizes="(max-width: 768px) 50vw, 300px"'
        cards_html.append(f"""        <!-- Product {idx} -->
        <article class="card" onclick="if(!event.target.closest('a'))location.href='/product/{pid}.html'">
          <div class="card-img-wrap">
            <img src="/{img}"{srcset_attr} alt="{alt_str}" {"loading=\"eager\" fetchpriority=\"high\"" if idx <= 4 else "loading=\"lazy\""} decoding="async" width="600" height="800">
          </div>
          <div class="body">
            <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--gold);margin-bottom:4px;">Серьги доступны отдельно или в комплекте</div>
            <h3 class="title"><a href="/product/{pid}.html" class="card-title-link">{title}</a></h3>
            <div class="price">{price_fmt} ₸</div>
            <div class="earring-price-badge" style="font-size:13px;font-weight:600;color:var(--gold);margin-top:4px;">Серьги отдельно: от {earring_price_fmt} ₸</div>
            <div class="meta" style="font-size: 12px; color: var(--muted); margin-top: 4px;">{mats_str}</div>
          </div>
        </article>""")

        item_list_elements.append(build_product_schema_for_itemlist(p, idx, is_kz=False))

    with open(path, "r", encoding="utf-8") as f:
        html_txt = f.read()

    new_grid_content = "\n".join(cards_html)
    html_txt = re.sub(
        r'<div class="grid">.*?</div>\s*</section>',
        f'<div class="grid">\n{new_grid_content}\n      </div>\n    </section>',
        html_txt,
        count=1,
        flags=re.DOTALL
    )

    schema_itemlist = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Серьги из жемчуга и комплекты — Livi Jewelry",
        "itemListElement": item_list_elements
    }
    ld_script = f'<script type="application/ld+json">\n{json.dumps(schema_itemlist, ensure_ascii=False, indent=2)}\n  </script>'
    html_txt = re.sub(
        r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"ItemList".*?</script>',
        ld_script,
        html_txt,
        count=1,
        flags=re.DOTALL
    )

    # Hreflang
    html_txt = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*"\s*/>', '', html_txt)
    hreflang_tags = f"""  <link rel="alternate" hreflang="ru-KZ" href="{BASE_URL}/sergi-iz-zhemchuga.html" />
  <link rel="alternate" hreflang="ru" href="{BASE_URL}/sergi-iz-zhemchuga.html" />
  <link rel="alternate" hreflang="kk-KZ" href="{BASE_URL}/kz/sergi-iz-zhemchuga.html" />
  <link rel="alternate" hreflang="kk" href="{BASE_URL}/kz/sergi-iz-zhemchuga.html" />
  <link rel="alternate" hreflang="uz-UZ" href="{BASE_URL}/uz/sergi-iz-zhemchuga.html" />
  <link rel="alternate" hreflang="uz" href="{BASE_URL}/uz/sergi-iz-zhemchuga.html" />
  <link rel="alternate" hreflang="x-default" href="{BASE_URL}/sergi-iz-zhemchuga.html" />"""
    html_txt = html_txt.replace(
        f'<link rel="canonical" href="https://livijewelry.kz/sergi-iz-zhemchuga.html">',
        f'<link rel="canonical" href="https://livijewelry.kz/sergi-iz-zhemchuga.html">\n{hreflang_tags}'
    )

    safe_write_text(path, html_txt)
    print(f"[OK] sergi-iz-zhemchuga.html обновлена ({len(earring_prods)} комплектов с серьгами)")


def update_category_hubs(products: list):
    """Enriches kolye-iz-zhemchuga.html and braslety-iz-zhemchuga.html with ItemList aggregateRating, review, and hreflang."""
    by_id = {p["id"]: p for p in products}

    # 1. kolye-iz-zhemchuga.html
    path_k = "kolye-iz-zhemchuga.html"
    if os.path.exists(path_k):
        with open(path_k, "r", encoding="utf-8") as f:
            k_html = f.read()

        card_pids = re.findall(r'href=[\'"](?:/product/|product/)(prod_\d+)\.html[\'"]', k_html)
        seen = set()
        unique_pids = []
        for pid in card_pids:
            if pid not in seen and pid in by_id:
                seen.add(pid)
                unique_pids.append(pid)

        item_list_elements = []
        for idx, pid in enumerate(unique_pids, start=1):
            p = by_id[pid]
            item_list_elements.append(build_product_schema_for_itemlist(p, idx, is_kz=False))

        schema_itemlist = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Колье, ожерелья и чокеры из натурального жемчуга — Livi Jewelry",
            "itemListElement": item_list_elements,
        }
        ld_script = f'<script type="application/ld+json">\n{json.dumps(schema_itemlist, ensure_ascii=False, indent=2)}\n  </script>'
        k_html = re.sub(
            r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"ItemList".*?</script>',
            ld_script,
            k_html,
            count=1,
            flags=re.DOTALL,
        )

        k_html = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*"\s*/>', '', k_html)
        k_hreflang = (
            '  <link rel="alternate" hreflang="ru-KZ" href="https://livijewelry.kz/kolye-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="ru" href="https://livijewelry.kz/kolye-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="kk-KZ" href="https://livijewelry.kz/kz/kolye-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="kk" href="https://livijewelry.kz/kz/kolye-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="uz-UZ" href="https://livijewelry.kz/uz/kolye-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="uz" href="https://livijewelry.kz/uz/kolye-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="x-default" href="https://livijewelry.kz/kolye-iz-zhemchuga.html" />'
        )
        k_html = k_html.replace(
            '<link rel="canonical" href="https://livijewelry.kz/kolye-iz-zhemchuga.html">',
            f'<link rel="canonical" href="https://livijewelry.kz/kolye-iz-zhemchuga.html">\n{k_hreflang}'
        )

        safe_write_text(path_k, k_html)
        print(f"[OK] kolye-iz-zhemchuga.html ItemList обновлен ({len(unique_pids)} товаров)")

    # 2. braslety-iz-zhemchuga.html
    path_b = "braslety-iz-zhemchuga.html"
    if os.path.exists(path_b):
        with open(path_b, "r", encoding="utf-8") as f:
            b_html = f.read()

        card_pids = re.findall(r'href=[\'"](?:/product/|product/)(prod_\d+)\.html[\'"]', b_html)
        seen = set()
        unique_pids = []
        for pid in card_pids:
            if pid not in seen and pid in by_id:
                seen.add(pid)
                unique_pids.append(pid)

        item_list_elements = []
        for idx, pid in enumerate(unique_pids, start=1):
            p = by_id[pid]
            item_list_elements.append(build_product_schema_for_itemlist(p, idx, is_kz=False))

        schema_itemlist = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "Браслеты из натурального жемчуга и камней — Livi Jewelry",
            "itemListElement": item_list_elements,
        }
        ld_script = f'<script type="application/ld+json">\n{json.dumps(schema_itemlist, ensure_ascii=False, indent=2)}\n  </script>'
        b_html = re.sub(
            r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"ItemList".*?</script>',
            ld_script,
            b_html,
            count=1,
            flags=re.DOTALL,
        )

        b_html = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*"\s*/>', '', b_html)
        b_hreflang = (
            '  <link rel="alternate" hreflang="ru-KZ" href="https://livijewelry.kz/braslety-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="ru" href="https://livijewelry.kz/braslety-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="kk-KZ" href="https://livijewelry.kz/kz/braslety-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="kk" href="https://livijewelry.kz/kz/braslety-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="uz-UZ" href="https://livijewelry.kz/uz/braslety-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="uz" href="https://livijewelry.kz/uz/braslety-iz-zhemchuga.html" />\n'
            '  <link rel="alternate" hreflang="x-default" href="https://livijewelry.kz/braslety-iz-zhemchuga.html" />'
        )
        b_html = b_html.replace(
            '<link rel="canonical" href="https://livijewelry.kz/braslety-iz-zhemchuga.html">',
            f'<link rel="canonical" href="https://livijewelry.kz/braslety-iz-zhemchuga.html">\n{b_hreflang}'
        )

        safe_write_text(path_b, b_html)
        print(f"[OK] braslety-iz-zhemchuga.html ItemList обновлен ({len(unique_pids)} товаров)")


def standardize_hub_header_and_drawer(file_path: str, slug: str):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    drawer_hub_links = "\n".join(
        f'            <a href="/{s}">{clean_attr(l)}</a>'
        for s, l in EXISTING_HUBS + [(h["slug"], h["chip_label"]) for h in ALL_HUBS]
    )

    new_drawer_and_header = f"""  <!-- Drawer -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back" role="button" tabindex="0" aria-label="Закрыть меню"></div>
    <div class="drawer-panel" role="menu" aria-label="Меню">
      <a href="/">Главная</a>
      <a href="/shop.html">Каталог</a>
      <details class="drawer-accordion">
        <summary>Коллекции и камни</summary>
        <div class="drawer-subnav">
{drawer_hub_links}
        </div>
      </details>
      <a href="/komplekty-ukrasheniy.html">Комплекты украшений</a>
      <a href="/delivery.html">Доставка и оплата</a>
      <div class="drawer-socials">
        <a class="drawer-soc-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="drawer-soc-link" href="https://wa.me/77054510584?text=Здравствуйте!%20Подскажите,%20пожалуйста,%20по%20украшениям%20Livi%20Jewelry%20—%20хочу%20уточнить%20наличие%20и%20проконсультироваться%20✨" target="_blank" rel="noopener">WhatsApp</a>
      </div>
      <div class="lang">
        <a href="/{slug}" class="active">RU</a>
        <a href="/kz/{slug}" lang="kk">KZ</a>
        <a href="/uz/{slug}" lang="uz">UZ</a>
      </div>
    </div>
  </div>

  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Меню"><span></span></button>

      <a class="brand" href="/" aria-label="Livi Jewelry">
        <span>LIVI JEWELRY</span>
      </a>

      <div class="nav-actions">
        <a href="/shop.html?search=1" class="header-search-btn" aria-label="Поиск по каталогу">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </a>
        <div class="header-lang-links" aria-label="Выбор языка">
          <a href="/{slug}" class="active">RU</a>
          <a href="/kz/{slug}" lang="kk">KZ</a>
          <a href="/uz/{slug}" lang="uz">UZ</a>
        </div>
        <a class="cart-link" href="/cart.html" aria-label="Корзина">
          <span>Корзина</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
        <a class="quick-link ig-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener" aria-label="Instagram">
          <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
            <path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm5 5.5A4.5 4.5 0 1 0 16.5 12 4.505 4.505 0 0 0 12 7.5zm6.5-.75a1.25 1.25 0 1 0 1.25 1.25A1.25 1.25 0 0 0 18.5 6.75Zm-6.5 2A3.25 3.25 0 1 1 8.75 12 3.254 3.254 0 0 1 12 8.75Z"/>
          </svg>
        </a>
        <a class="quick-link wa-link" href="https://wa.me/77054510584?text=Здравствуйте!%20Подскажите,%20пожалуйста,%20по%20украшениям%20Livi%20Jewelry%20—%20хочу%20уточнить%20наличие%20и%20проконсультироваться%20✨" target="_blank" rel="noopener" aria-label="WhatsApp">
          <svg width="20" height="20" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
            <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
            <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
          </svg>
        </a>
      </div>
    </div>
  </header>"""

    content = re.sub(
        r'<!--\s*Drawer\s*-->.*?</header>',
        new_drawer_and_header,
        content,
        count=1,
        flags=re.DOTALL
    )

    content = re.sub(
        r'<footer\b[^>]*>.*?</footer>',
        RU_FOOTER_HTML,
        content,
        count=1,
        flags=re.DOTALL
    )

    if 'class="floating-wa"' not in content:
        floating_wa_html = f"""  <!-- Floating WhatsApp Widget -->
  <a class="floating-wa" href="https://wa.me/77054510584?text=Здравствуйте!%20Подскажите,%20пожалуйста,%20по%20украшениям%20Livi%20Jewelry%20—%20хочу%20уточнить%20наличие%20и%20проконсультироваться%20✨" target="_blank" rel="noopener" aria-label="Консультация мастера в WhatsApp">
    <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
      <path fill="currentColor" d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
      <path fill="currentColor" d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
    </svg>
    <span class="floating-wa-text">Консультация мастера</span>
  </a>"""
        content = content.replace("</footer>", f"</footer>\n\n{floating_wa_html}")

    content = re.sub(r'<a\s+href="[^"]*kz/shop\.html"[^>]*>Қазақша\s+каталог</a>\s*', '', content)

    safe_write_text(file_path, content)


def update_existing_pages_interlinking():
    """Updates category pages, shop.html, and index.html with all 21 SEO hub links."""
    for s, _ in EXISTING_HUBS:
        standardize_hub_header_and_drawer(s, s)

    all_pages = [s for s, _ in EXISTING_HUBS] + ["shop.html"]
    for page in all_pages:
        if not os.path.exists(page):
            continue
        with open(page, "r", encoding="utf-8") as f:
            c_html = f.read()

        interlink_block = build_interlink_block_html(current_slug=page, prefix="")
        if 'class="hub-interlink-section"' in c_html:
            c_html = re.sub(
                r'(?:<!--\s*Навигационный блок[^>]*-->\s*)?<section class="hub-interlink-section".*?</section>',
                interlink_block,
                c_html,
                count=1,
                flags=re.DOTALL,
            )
        else:
            c_html = c_html.replace("</main>", f"\n{interlink_block}\n  </main>")

        safe_write_text(page, c_html)


def generate_seo_hubs():
    if not os.path.exists(PRODUCTS_FILE):
        print(f"Error: {PRODUCTS_FILE} not found!")
        return []

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    # 1. Generate 18 RU hubs
    generated = []
    for hub in ALL_HUBS:
        out = generate_hub_page(hub, products)
        generated.append(out)

    # 2. Update 3 existing RU hubs
    update_sergi_page(products)
    update_category_hubs(products)
    update_existing_pages_interlinking()

    # 3. Generate all 21 KZ hubs in /kz/
    all_21_slugs = [s for s, _ in EXISTING_HUBS] + [h["slug"] for h in ALL_HUBS]
    kz_generated = []
    for s in all_21_slugs:
        meta = KZ_HUBS_INFO.get(s, {})
        out_kz = generate_kz_hub_page(s, meta, products)
        kz_generated.append(out_kz)

    # 4. Generate all 21 UZ hubs in /uz/
    uz_generated = []
    for s in all_21_slugs:
        meta = UZ_HUBS_INFO.get(s, {})
        out_uz = generate_uz_hub_page(s, meta, products)
        uz_generated.append(out_uz)

    print(f"[OK] Generated {len(generated)} Russian hubs + {len(kz_generated)} Kazakh hubs + {len(uz_generated)} Uzbek hubs (all 21 clusters complete).")
    return generated


if __name__ == "__main__":
    generate_seo_hubs()
