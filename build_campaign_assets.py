import csv
import json

# ==============================================================================
# LIVI JEWELRY - CAMPAIGN ASSETS GENERATOR v2.0
# Generates:
#  1. master_negative_keywords_kz.csv (250+ targeted negatives)
#  2. 1_google_ads_keywords.csv (Keywords with product-level Final URLs)
#  3. google_ads_campaign_import.csv (Ready for Google Ads Editor / Bulk Upload)
#  4. import_all_negative_keywords.js (Google Ads Script to attach negative list)
# ==============================================================================

# ==========================================
# 1. МИНУС-СЛОВА: 250+ фильтров по 8 категориям
# ==========================================
negatives = [
    # 1. DIY, Рукоделие, Хобби
    "своими руками", "как сделать", "как сплести", "как собрать", "схема", "схемы", 
    "мастер класс", "мк", "бисероплетение", "бисер", "плетение", "вязание", 
    "бусины поштучно", "бусины оптом", "бусины для рукоделия", "фурнитура", 
    "застежка для колье", "карабин ювелирный", "швензы", "штифты", "пины", 
    "леска для бус", "ювелирная проволока", "тросик", "инструменты для бижутерии", 
    "круглогубцы", "плоскогубцы", "эпоксидная смола", "полимерная глина", "бейлы", 
    "концевики", "каллоты", "кримпы", "разделители бусин", "шапочки для бусин", 
    "силиконовая нить", "спандекс", "паракорд", "макраме", "вышивка", "пайетки", 
    "стеклярус", "мулине", "пряжа", "кабошон", "заготовки для колец", "основы для броши", 
    "форма для смолы", "молд", "станок для бисероплетения", "сборка на дому",

    # 2. Дешевые маркетплейсы, секонд-хенд, халява, опт
    "дешево", "недорого", "самый дешевый", "бесплатно", "даром", "отдам даром", 
    "в дар", "подарок бесплатно", "садовод", "тяк москва", "алиэкспресс", "aliexpress", 
    "temu", "тему", "shein", "шейн", "таобао", "taobao", "1688", "оптом", "опт", 
    "крупный опт", "дропшиппинг", "барахолка", "барахолка бу", "секонд хенд", "бу", 
    "б у", "б/у", "авито", "olx", "olx бу", "satu kz", "конфискат", "таможенный конфискат", 
    "китайский ширпотреб", "ликвидация магазина", "фикс прайс", "fix price",

    # 3. Металлы не нашего профиля, ломбарды, скупка
    "золото 585", "золото 750", "белое золото", "червонное золото", "ломбард", 
    "скупка", "скупка золота", "лом золота", "сдать золото", "грамм золота", 
    "цена за грамм", "курс золота", "проба 585", "проба 925", "клеймо", "слитки", 
    "слиток золота", "инвестиционные монеты", "платина", "палладий", "титан", 
    "медицинская сталь", "нержавеющая сталь", "вольфрам", "серебро 925 ломбард", 
    "залог золота", "займ под залог",

    # 4. Дешевые ненатуральные материалы
    "пластик", "пластиковые", "дерево", "деревянные", "стекло", "стеклянные", 
    "акрил", "акриловые", "силикон", "силиконовые", "эпоксидка", "смола", 
    "янтарь лечебный", "янтарные бусы от щитовидки", "фианит", "фианиты оптом", 
    "искусственный жемчуг дешевый", "пластиковый жемчуг",

    # 5. Неподходящие типы изделий
    "пирсинг", "пирсинг пупка", "септум", "микродермал", "тоннели в уши", "плаги", 
    "обручальные кольца", "помолвочное кольцо", "мужская печатка", "печатка мужская", 
    "мужская цепь золото", "цепочка бисмарк", "панцирное плетение", "крестик золотой", 
    "крестик серебряный", "нательный крест", "ладанка", "иконка", "полумесяц кулон", 
    "мусульманские кулоны", "аят аль курси", "четки", "четки перекидные", "тасбих", 
    "часы", "наручные часы", "смарт часы", "apple watch", "ремешок для часов", 
    "запонки", "зажим для галстука", "детские украшения", "набор для девочки", 
    "игрушечная бижутерия",

    # 6. Ремонт, уход, чистка, экспертиза
    "ремонт", "ремонт бижутерии", "ювелирная мастерская", "реставрация", "пайка", 
    "лазерная пайка", "перетяжка бус", "перевязать бусы", "замена замка", 
    "уменьшить кольцо", "увеличить кольцо", "ультразвуковая чистка", "чистка золота", 
    "как почистить жемчуг", "как отбелить жемчуг", "как отличить натуральный жемчуг", 
    "тест на подлинность", "экспертиза камней", "геммолог", "оценка ювелирных",

    # 7. Конкуренты и масс-маркет сети
    "пандора", "pandora", "шармы пандора", "санлайт", "sunlight", "соколов", 
    "sokolov", "адамас", "585 золотой", "tiffany", "тиффани", "картье", "cartier", 
    "гвоздь картье", "van cleef", "ван клиф", "клевер ван клиф", "chopard", 
    "шопард", "булгари", "bulgari", "swarovski", "сваровски", "tous", "тоус мишка", 
    "казахювелир", "алтын", "эпл даймонд",

    # 8. Информационные, эзотерика, вакансии
    "гороскоп", "знак зодиака", "магия камней", "магические свойства", 
    "лечебные свойства", "заговор", "приворот", "чакры", "амулет от сглаза", 
    "реферат", "курсовая", "википедия", "доклад", "презентация", 
    "фото высокого разрешения", "картинки", "обои на телефон", "раскраска", 
    "скачать", "видео", "youtube", "тикток", "книга", "курсы", "обучение", 
    "работа", "вакансии", "резюме", "зарплата", "продавец консультант вакансии"
]

with open("master_negative_keywords_kz.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Campaign", "Keyword", "Criterion Type"])
    for kw in negatives:
        writer.writerow(["[Account]", kw, "Negative Phrase"])

print(f"[OK] master_negative_keywords_kz.csv: {len(negatives)} negative keywords")

# ==============================================================================
# 2. КЛЮЧЕВЫЕ СЛОВА С ТОЧЕЧНОЙ ПРИВЯЗКОЙ К СТАТИЧЕСКИМ СТРАНИЦАМ ТОВАРОВ v2.0
# ==============================================================================
CAMPAIGN_NAME = "Livi Jewelry - Поиск Казахстан"

ad_groups_data = [
    {
        "name": "Колье и чокеры из жемчуга",
        "url": "https://livijewelry.kz/kolye-iz-zhemchuga.html",
        "keywords": [
            ("колье из натурального жемчуга", "Phrase", "https://livijewelry.kz/product/prod_01.html"),
            ("колье из натурального жемчуга", "Exact", "https://livijewelry.kz/product/prod_01.html"),
            ("купить колье из жемчуга", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("чокер из жемчуга алматы", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("чокер из жемчуга алматы", "Exact", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("чокер из жемчуга астана", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("барочный жемчуг колье", "Phrase", "https://livijewelry.kz/product/prod_01.html"),
            ("барочный жемчуг колье", "Exact", "https://livijewelry.kz/product/prod_01.html"),
            ("колье из барочного жемчуга алматы", "Phrase", "https://livijewelry.kz/product/prod_01.html"),
            ("многорядное колье из жемчуга", "Phrase", "https://livijewelry.kz/product/prod_02.html"),
            ("колье из жемчуга майорка", "Phrase", "https://livijewelry.kz/product/prod_03.html"),
            ("колье из жемчуга майорка", "Exact", "https://livijewelry.kz/product/prod_03.html"),
            ("купить жемчужное колье", "Exact", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("жемчужный чокер купить казахстан", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("бусы из натурального жемчуга алматы", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("авторское колье из жемчуга", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("колье лапы купить", "Phrase", "https://livijewelry.kz/product/prod_08.html"),
            ("колье гранж купить", "Phrase", "https://livijewelry.kz/product/prod_22.html")
        ],
        "headlines": [
            "Колье из натурального жемчуга", "Livi Jewelry — Ручная работа", "Жемчуг премиальной селекции",
            "Чокеры и колье из жемчуга", "Барочный жемчуг отборный", "Доставка СДЭК по Казахстану",
            "Идеальный подарок в коробке", "Быстрый счёт в Kaspi.kz", "В наличии и на заказ",
            "Подбор длины под ваш размер", "Заказ и примерка в WhatsApp", "Видео украшений перед заказом",
            "Бутик Livi Jewelry", "100% натуральный жемчуг", "Каталог колье 2026"
        ],
        "descriptions": [
            "Авторские колье из отборного барочного и натурального жемчуга. Ручная работа мастера.",
            "Быстрая доставка СДЭК до двери по всему Казахстану. Удобная оплата через Kaspi Pay.",
            "Роскошные многорядные колье и чокеры. Фирменная подарочная упаковка к каждому заказу.",
            "Консультация мастера и видео изделий в WhatsApp. Подберём идеальный размер под вас."
        ]
    },
    {
        "name": "Браслеты и минералы",
        "url": "https://livijewelry.kz/braslety-iz-zhemchuga.html",
        "keywords": [
            ("браслет из малахита алматы", "Phrase", "https://livijewelry.kz/product/prod_06.html"),
            ("браслет из малахита алматы", "Exact", "https://livijewelry.kz/product/prod_06.html"),
            ("браслет из натурального малахита", "Phrase", "https://livijewelry.kz/product/prod_06.html"),
            ("браслет из натуральных камней купить", "Phrase", "https://livijewelry.kz/braslety-iz-zhemchuga.html"),
            ("браслет из натуральных камней купить", "Exact", "https://livijewelry.kz/braslety-iz-zhemchuga.html"),
            ("украшения из натуральной бирюзы", "Phrase", "https://livijewelry.kz/product/prod_16.html"),
            ("украшения из натуральной бирюзы", "Exact", "https://livijewelry.kz/product/prod_16.html"),
            ("браслет из бирюзы алматы", "Phrase", "https://livijewelry.kz/product/prod_16.html"),
            ("браслет из жемчуга алматы", "Phrase", "https://livijewelry.kz/braslety-iz-zhemchuga.html"),
            ("браслет из жемчуга алматы", "Exact", "https://livijewelry.kz/braslety-iz-zhemchuga.html"),
            ("украшения из аметиста алматы", "Phrase", "https://livijewelry.kz/product/prod_07.html"),
            ("украшения из розового кварца алматы", "Phrase", "https://livijewelry.kz/product/prod_15.html"),
            ("украшения из натурального агата", "Phrase", "https://livijewelry.kz/product/prod_10.html"),
            ("колье из авантюрина купить", "Phrase", "https://livijewelry.kz/product/prod_09.html"),
            ("колье из коралла купить", "Phrase", "https://livijewelry.kz/product/prod_14.html"),
            ("украшения из граната алматы", "Phrase", "https://livijewelry.kz/product/prod_10.html"),
            ("украшение сотуар из агата", "Phrase", "https://livijewelry.kz/product/prod_17.html"),
            ("браслет из натуральных минералов казахстан", "Phrase", "https://livijewelry.kz/braslety-iz-zhemchuga.html")
        ],
        "headlines": [
            "Браслеты из камней и жемчуга", "Браслет из малахита Алматы", "Украшения из бирюзы и агата",
            "Livi Jewelry — Ручная сборка", "100% натуральные минералы", "Доставка СДЭК по Казахстану",
            "Браслеты ручной работы", "Удаленный счёт Kaspi Pay", "Подарочная шкатулка к заказу",
            "В наличии с быстрой доставкой", "Подбор размера на запястье", "Заказ и примерка в WhatsApp",
            "Видео перелива минералов в чат", "Бутик украшений Livi", "Каталог браслетов 2026"
        ],
        "descriptions": [
            "Браслеты ручной работы из натурального малахита, бирюзы и жемчуга. Отборные камни.",
            "Экспресс-доставка СДЭК до двери или в ПВЗ. Удобная оплата через счёт Kaspi Pay.",
            "Изысканные браслеты с натуральными минералами. Подарочная шкатулка к каждому заказу.",
            "Свяжитесь с мастером в WhatsApp: пришлем видео перелива камней и поможем с выбором."
        ]
    },
    {
        "name": "Серьги из жемчуга и камней",
        "url": "https://livijewelry.kz/sergi-iz-zhemchuga.html",
        "keywords": [
            ("серьги из жемчуга алматы", "Phrase", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги из жемчуга алматы", "Exact", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги из натурального жемчуга купить", "Phrase", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги из натурального жемчуга", "Exact", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги с барочным жемчугом", "Phrase", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги с барочным жемчугом", "Exact", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги ручной работы алматы", "Phrase", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги из жемчуга астана", "Phrase", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги из жемчуга астана", "Exact", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("длинные серьги с жемчугом", "Phrase", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги с натуральными камнями купить", "Phrase", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги пусеты из жемчуга алматы", "Phrase", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги из аметиста купить", "Phrase", "https://livijewelry.kz/product/prod_11.html"),
            ("серьги из тигрового глаза купить", "Phrase", "https://livijewelry.kz/product/prod_12.html")
        ],
        "headlines": [
            "Серьги из жемчуга в Алматы", "Серьги с барочным жемчугом", "Livi Jewelry — Авторские серьги",
            "Натуральный отборный жемчуг", "Гипоаллергенная фурнитура", "Стойкая позолота и родий",
            "Доставка СДЭК по Казахстану", "Подарочная коробка в комплекте", "Счёт в приложении Kaspi Pay",
            "Серьги ручной сборки мастера", "Подбор комплекта к колье", "Видео сережек перед покупкой",
            "Бутик Livi Jewelry", "В наличии с отправкой сегодня", "Каталог сережек 2026"
        ],
        "descriptions": [
            "Элегантные серьги из натурального барочного жемчуга и минералов. Стойкая фурнитура.",
            "Быстрая доставка СДЭК в любой город Казахстана. Оплата через безопасный счёт Kaspi.",
            "Авторские серьги ручной работы. Премиальная подарочная упаковка к каждому заказу.",
            "Напишите нам в WhatsApp: снимем видео посадки сережек и покажем перелив жемчуга."
        ]
    },
    {
        "name": "Комплекты и ювелирные сеты",
        "url": "https://livijewelry.kz/shop.html",
        "keywords": [
            ("комплект украшений из жемчуга", "Phrase", "https://livijewelry.kz/product/prod_04.html"),
            ("комплект украшений из жемчуга", "Exact", "https://livijewelry.kz/product/prod_04.html"),
            ("набор украшений ручной работы", "Phrase", "https://livijewelry.kz/shop.html"),
            ("набор украшений ручной работы", "Exact", "https://livijewelry.kz/shop.html"),
            ("ювелирный гарнитур алматы", "Phrase", "https://livijewelry.kz/product/prod_07.html"),
            ("ювелирный гарнитур алматы", "Exact", "https://livijewelry.kz/product/prod_07.html"),
            ("гарнитур из натуральных камней", "Phrase", "https://livijewelry.kz/shop.html"),
            ("гарнитур из натуральных камней", "Exact", "https://livijewelry.kz/shop.html"),
            ("комплект колье и серьги из жемчуга", "Phrase", "https://livijewelry.kz/product/prod_13.html"),
            ("набор украшений с натуральными камнями", "Phrase", "https://livijewelry.kz/shop.html"),
            ("комплект украшений алматы купить", "Phrase", "https://livijewelry.kz/shop.html"),
            ("комплект украшений алматы купить", "Exact", "https://livijewelry.kz/shop.html"),
            ("гарнитур из жемчуга астана", "Phrase", "https://livijewelry.kz/product/prod_04.html"),
            ("сет украшений ручной работы", "Phrase", "https://livijewelry.kz/product/prod_21.html"),
            ("комплект колье и браслет", "Phrase", "https://livijewelry.kz/product/prod_04.html"),
            ("комплект из коралла и яшмы", "Phrase", "https://livijewelry.kz/product/prod_14.html"),
            ("комплект из бирюзы купить", "Phrase", "https://livijewelry.kz/product/prod_16.html")
        ],
        "headlines": [
            "Комплекты украшений ручной работы", "Ювелирные гарнитуры Алматы", "Сеты из жемчуга и камней",
            "Livi Jewelry — Сеты мастера", "Колье + Серьги + Браслет", "100% натуральные камни",
            "Доставка СДЭК по Казахстану", "Фирменная подарочная упаковка", "Счёт в Kaspi Pay за минуту",
            "В наличии с быстрой доставкой", "Подбор украшений под ваш образ", "Заказ и видео в WhatsApp",
            "Идеальный готовый образ", "Бутик авторских гарнитуров", "Каталог сетов 2026"
        ],
        "descriptions": [
            "Роскошные гарнитуры из жемчуга, агата, аметиста и коралла. Ручная сборка мастера.",
            "Каждое изделие сета можно приобрести отдельно или полным комплектом со скидкой.",
            "Премиальная подарочная шкатулка к каждому сету. Экспресс-доставка СДЭК по Казахстану.",
            "Напишите в WhatsApp: покажем посадку всего комплекта на видео и подберем размер."
        ]
    },
    {
        "name": "Подарки и авторские украшения",
        "url": "https://livijewelry.kz/shop.html",
        "keywords": [
            ("подарок девушке украшения алматы", "Phrase", "https://livijewelry.kz/shop.html"),
            ("подарок девушке украшения алматы", "Exact", "https://livijewelry.kz/shop.html"),
            ("подарок жене на день рождения украшения", "Phrase", "https://livijewelry.kz/product/prod_02.html"),
            ("подарок маме украшения алматы", "Phrase", "https://livijewelry.kz/product/prod_01.html"),
            ("авторские украшения ручной работы", "Phrase", "https://livijewelry.kz/shop.html"),
            ("авторские украшения ручной работы", "Exact", "https://livijewelry.kz/shop.html"),
            ("ювелирная бижутерия алматы", "Phrase", "https://livijewelry.kz/shop.html"),
            ("дизайнерские украшения ручной работы казахстан", "Phrase", "https://livijewelry.kz/shop.html"),
            ("украшения ручной работы астана", "Phrase", "https://livijewelry.kz/shop.html"),
            ("украшения ручной работы астана", "Exact", "https://livijewelry.kz/shop.html"),
            ("украшения на кыз узату алматы", "Phrase", "https://livijewelry.kz/product/prod_01.html"),
            ("украшения невесты из жемчуга", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("авторская бижутерия купить алматы", "Exact", "https://livijewelry.kz/shop.html"),
            ("подарок женщине ювелирные украшения", "Phrase", "https://livijewelry.kz/product/prod_02.html")
        ],
        "headlines": [
            "Подарок девушке — Украшения", "Авторские украшения Livi", "Ювелирная бижутерия Алматы",
            "Идеальный подарок со вкусом", "Натуральный жемчуг и камни", "Доставка СДЭК по Казахстану",
            "Подарочная упаковка в комплекте", "Счёт в приложении Kaspi.kz", "В наличии с быстрой доставкой",
            "Подарок на день рождения", "Индивидуальная подгонка", "Заказ и видео в WhatsApp",
            "Эксклюзив ручной работы", "Бутик Livi Jewelry", "Каталог подарков 2026"
        ],
        "descriptions": [
            "Ищете изысканный подарок? Авторские украшения из натурального жемчуга и камней.",
            "Премиальная подарочная коробка к каждому заказу. Доставка СДЭК в любой город Казахстана.",
            "Счёт на оплату в Kaspi.kz. 100% совпадение с фото. Консультация мастера онлайн.",
            "Напишите нам в WhatsApp: снимем видео изделия и поможем сделать незабываемый подарок!"
        ]
    }
]

# Write 1_google_ads_keywords.csv
all_kws_count = 0
with open("1_google_ads_keywords.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Campaign", "Ad Group", "Keyword", "Criterion Type", "Final URL"])
    for group in ad_groups_data:
        for item in group["keywords"]:
            kw = item[0]
            c_type = item[1]
            final_url = item[2] if len(item) > 2 else group["url"]
            writer.writerow([CAMPAIGN_NAME, group["name"], kw, c_type, final_url])
            all_kws_count += 1

print(f"[OK] 1_google_ads_keywords.csv: {all_kws_count} keywords across {len(ad_groups_data)} ad groups")

# Write google_ads_campaign_import.csv
headers = [
    "Action", "Campaign", "Campaign Daily Budget", "Campaign Type", "Networks", 
    "Bid Strategy Type", "Ad Group", "Keyword", "Criterion Type",
    "Headline 1", "Headline 2", "Headline 3", "Headline 4", "Headline 5",
    "Headline 6", "Headline 7", "Headline 8", "Headline 9", "Headline 10",
    "Headline 11", "Headline 12", "Headline 13", "Headline 14", "Headline 15",
    "Description 1", "Description 2", "Description 3", "Description 4", "Final URL"
]

rows = []
# 1. Campaign definition
camp_row = ["Add", CAMPAIGN_NAME, "3000", "Search", "Google search", "Maximize Clicks"] + [""] * 23
rows.append(camp_row)

for group in ad_groups_data:
    # 2. Ad Group definition
    ag_row = ["Add", CAMPAIGN_NAME, "", "Search", "", "Maximize Clicks", group["name"]] + [""] * 22
    rows.append(ag_row)

    # 3. Keywords in this group with keyword-level Final URLs
    for item in group["keywords"]:
        kw = item[0]
        c_type = item[1]
        kw_url = item[2] if len(item) > 2 else group["url"]
        kw_row = ["Add", CAMPAIGN_NAME, "", "Search", "", "Maximize Clicks", group["name"], kw, c_type] + [""] * 19 + [kw_url]
        rows.append(kw_row)

    # 4. Responsive Search Ad in this group
    ad_row = ["Add", CAMPAIGN_NAME, "", "Search", "", "Maximize Clicks", group["name"], "", "Responsive search ad"]
    ad_row.extend(group["headlines"])
    ad_row.extend(group["descriptions"])
    ad_row.append(group["url"])
    rows.append(ad_row)

with open("google_ads_campaign_import.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"[OK] google_ads_campaign_import.csv: {len(rows)} rows generated successfully")

# Write import_all_negative_keywords.js
js_content = f"""/**
 * Google Ads Script: Автоматическое создание списка минус-слов и прикрепление к кампаниям
 * Livi Jewelry (Аккаунт: 167-939-74126)
 *
 * Всего минус-слов: {len(negatives)} шт. (Полная защита от слива бюджета)
 *
 * КАК ЗАПУСТИТЬ ЗА 10 СЕКУНД:
 * 1. В Google Ads нажмите: Инструменты и настройки (Tools & Settings) -> Скрипты (Scripts).
 * 2. Нажмите синюю кнопку "+" (Новый скрипт).
 * 3. Удалите весь текст в окне, вставьте этот скрипт и нажмите "Авторизовать" (Authorize), затем "Выполнить" (Run).
 */

function main() {{
  var LIST_NAME = "Livi Jewelry - Мастер Минус-слова";
  
  var NEGATIVES = {json.dumps(negatives, ensure_ascii=False, indent=4)};

  Logger.log("==================================================");
  Logger.log("LIVI JEWELRY: АВТОМАТИЧЕСКАЯ УСТАНОВКА " + NEGATIVES.length + " МИНУС-СЛОВ");
  Logger.log("==================================================");

  // 1. Поиск или создание списка минус-слов
  var listIterator = AdsApp.negativeKeywordLists().withCondition("Name = '" + LIST_NAME + "'").get();
  var negativeList;

  if (listIterator.hasNext()) {{
    negativeList = listIterator.next();
    Logger.log("Список уже найден: " + LIST_NAME);
  }} else {{
    var builder = AdsApp.newNegativeKeywordListBuilder().withName(LIST_NAME).build();
    negativeList = builder.getResult();
    Logger.log("Создан новый мастер-список: " + LIST_NAME);
  }}

  // 2. Добавление минус-слов
  var addedCount = 0;
  for (var i = 0; i < NEGATIVES.length; i++) {{
    try {{
      negativeList.addNegativeKeyword(NEGATIVES[i]);
      addedCount++;
    }} catch (e) {{
      // Игнорируем дубликаты
    }}
  }}
  Logger.log("Успешно добавлено минус-слов в список: " + addedCount);

  // 3. Привязка списка ко всем активным кампаниям
  var campaignIterator = AdsApp.campaigns().get();
  var attachedCampaigns = 0;
  while (campaignIterator.hasNext()) {{
    var campaign = campaignIterator.next();
    try {{
      campaign.addNegativeKeywordList(negativeList);
      attachedCampaigns++;
      Logger.log("Прикреплено к кампании: " + campaign.getName());
    }} catch (err) {{
      Logger.log("Кампания " + campaign.getName() + " уже привязана или ошибка: " + err);
    }}
  }}

  Logger.log("==================================================");
  Logger.log("ГОТОВО! " + NEGATIVES.length + " минус-слов активны и защищают бюджет.");
  Logger.log("==================================================");
}}
"""

with open("import_all_negative_keywords.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"[OK] import_all_negative_keywords.js: generated with {len(negatives)} negative keywords")
