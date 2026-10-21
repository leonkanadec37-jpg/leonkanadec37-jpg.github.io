import csv
import json

# ==============================================================================
# LIVI JEWELRY - CAMPAIGN ASSETS GENERATOR v3.0
# Generates:
#  1. master_negative_keywords_kz.csv (250+ targeted negatives)
#  2. 1_google_ads_keywords.csv (Keywords with product-level and SEO-hub Final URLs)
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
# 2. КЛЮЧЕВЫЕ СЛОВА С ТОЧЕЧНОЙ ПРИВЯЗКОЙ К НОВЫМ SEO-ХАБАМ v3.0
# ==============================================================================
CAMPAIGN_NAME = "Livi Jewelry - Поиск Казахстан"

ad_groups_data = [
    # 1. Комплекты украшений -> https://livijewelry.kz/komplekty-ukrasheniy.html
    {
        "name": "Комплекты украшений",
        "url": "https://livijewelry.kz/komplekty-ukrasheniy.html",
        "keywords": [
            ("комплект украшений из жемчуга", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("комплект украшений из жемчуга", "Exact", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("набор украшений ручной работы", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("набор украшений ручной работы", "Exact", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("ювелирный комплект алматы", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("ювелирный комплект алматы", "Exact", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("комплект из натуральных камней", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("комплект из натуральных камней", "Exact", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("комплект колье и серьги из жемчуга", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("набор украшений с натуральными камнями", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("комплект украшений алматы купить", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("комплект украшений алматы купить", "Exact", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("комплект из жемчуга астана", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("сет украшений ручной работы", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("комплект колье и браслет", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("комплект из коралла и яшмы", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html"),
            ("комплект из бирюзы купить", "Phrase", "https://livijewelry.kz/komplekty-ukrasheniy.html")
        ],
        "headlines": [
            "Комплекты украшений", "Сеты из жемчуга и камней", "Ювелирные комплекты",
            "Livi Jewelry — Сеты", "Колье + Серьги + Браслет", "100% натуральные камни",
            "Доставка СДЭК по РК", "Подарочная упаковка 0 ₸", "Счёт в Kaspi Pay",
            "В наличии в Астане", "Подбор сета под образ", "Примерка в WhatsApp",
            "Готовый женский образ", "Бутик сетов Livi", "Каталог сетов 2026"
        ],
        "descriptions": [
            "Авторские комплекты из жемчуга и минералов. Скидка на полный сет. Доставка СДЭК.",
            "Роскошные ювелирные комплекты ручной работы. Подарочная упаковка включена в заказ.",
            "Экспресс-доставка СДЭК по Астане и всему Казахстану. Удобная оплата через Kaspi Pay.",
            "Консультация мастера и видео посадки комплекта в WhatsApp. Подбор размера под вас."
        ]
    },

    # 2. Чокеры -> https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html
    {
        "name": "Чокеры из камней",
        "url": "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html",
        "keywords": [
            ("чокер из натуральных камней", "Phrase", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("чокер из натуральных камней", "Exact", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("чокер из жемчуга алматы", "Phrase", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("чокер из жемчуга алматы", "Exact", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("чокер из жемчуга астана", "Phrase", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("чокер из жемчуга купить", "Phrase", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("чокер из жемчуга купить", "Exact", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("чокер на шею из камней", "Phrase", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("авторский чокер ручной работы", "Phrase", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("короткое колье чокер", "Phrase", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("чокер из барочного жемчуга", "Phrase", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"),
            ("жемчужный чокер казахстан", "Phrase", "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html")
        ],
        "headlines": [
            "Чокеры из камней и жемчуга", "Чокер из жемчуга Алматы", "Чокеры ручной работы",
            "Livi Jewelry — Чокеры", "Идеальная посадка по шее", "Натуральный жемчуг и камни",
            "Доставка СДЭК по РК", "Подарочная упаковка 0 ₸", "Счёт в Kaspi Pay",
            "Размеры: 38 см и 40 см", "В наличии в Астане", "Видео чокеров в WhatsApp",
            "Трендовые чокеры 2026", "Бутик Livi Jewelry", "Каталог чокеров"
        ],
        "descriptions": [
            "Стильные чокеры из натурального жемчуга и камней. Идеальная посадка по вашей шее.",
            "Быстрая доставка курьером СДЭК по Астане, Алматы и Казахстану. Оплата в Kaspi Pay.",
            "Фирменная подарочная упаковка к каждому чокеру. Гипоаллергенный родий и позолота.",
            "Напишите в WhatsApp: поможем подобрать точную длину чокера и пришлем живое видео."
        ]
    },

    # 3. Сотуары -> https://livijewelry.kz/sotuary-iz-zhemchuga.html
    {
        "name": "Сотуары и галстуки",
        "url": "https://livijewelry.kz/sotuary-iz-zhemchuga.html",
        "keywords": [
            ("сотуар из жемчуга купить", "Phrase", "https://livijewelry.kz/sotuary-iz-zhemchuga.html"),
            ("сотуар из жемчуга купить", "Exact", "https://livijewelry.kz/sotuary-iz-zhemchuga.html"),
            ("длинное колье сотуар", "Phrase", "https://livijewelry.kz/sotuary-iz-zhemchuga.html"),
            ("колье галстук из жемчуга", "Phrase", "https://livijewelry.kz/sotuary-iz-zhemchuga.html"),
            ("колье галстук из жемчуга", "Exact", "https://livijewelry.kz/sotuary-iz-zhemchuga.html"),
            ("сотуар из натуральных камней", "Phrase", "https://livijewelry.kz/sotuary-iz-zhemchuga.html"),
            ("сотуар из камней алматы", "Phrase", "https://livijewelry.kz/sotuary-iz-zhemchuga.html"),
            ("колье трансформер сотуар", "Phrase", "https://livijewelry.kz/sotuary-iz-zhemchuga.html"),
            ("украшение сотуар купить казахстан", "Phrase", "https://livijewelry.kz/sotuary-iz-zhemchuga.html"),
            ("украшение сотуар из агата", "Phrase", "https://livijewelry.kz/sotuary-iz-zhemchuga.html")
        ],
        "headlines": [
            "Сотуары из жемчуга", "Колье-галстуки ручной сборки", "Длинные колье сотуары",
            "Livi Jewelry — Сотуары", "Жемчуг и натуральные камни", "Элегантное колье-галстук",
            "Доставка СДЭК по РК", "Подарочный футляр 0 ₸", "Счёт в Kaspi Pay",
            "Украшение для выреза и спины", "В наличии в Астане", "Видео сотуаров в WhatsApp",
            "Авторский дизайн Livi", "Эксклюзивные сотуары", "Каталог сотуаров 2026"
        ],
        "descriptions": [
            "Роскошные сотуары и колье-галстуки из натурального жемчуга и агата. Ручная работа.",
            "Элегантная длина визуально вытягивает силуэт. Идеально под вечерний или деловой образ.",
            "Быстрая доставка СДЭК до двери по Казахстану. Фирменная упаковка в подарок.",
            "Консультация мастера и живое видео изделий в WhatsApp. Оплата удаленно в Kaspi."
        ]
    },

    # 4. Барочный жемчуг -> https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html
    {
        "name": "Барочный жемчуг",
        "url": "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html",
        "keywords": [
            ("украшения из барочного жемчуга", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html"),
            ("украшения из барочного жемчуга", "Exact", "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html"),
            ("барочный жемчуг купить алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html"),
            ("барочный жемчуг колье", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html"),
            ("барочный жемчуг колье", "Exact", "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html"),
            ("колье с барочным жемчугом", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html"),
            ("браслет с барочным жемчугом", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html"),
            ("серьги с барочным жемчугом", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html"),
            ("барочный жемчуг украшения казахстан", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html"),
            ("крупный барочный жемчуг", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-barochnogo-zhemchuga.html")
        ],
        "headlines": [
            "Барочный жемчуг — Колье", "Украшения из барочного жемчуга", "Отборный барочный жемчуг",
            "Livi Jewelry — Жемчуг", "Неповторимая форма жемчужин", "100% натуральный жемчуг",
            "Доставка СДЭК по РК", "Подарочная коробка 0 ₸", "Счёт в Kaspi Pay",
            "Колье, браслеты, серьги", "В наличии в Астане", "Видео перелива в WhatsApp",
            "Эксклюзив ручной работы", "Премиум коллекция жемчуга", "Каталог жемчуга 2026"
        ],
        "descriptions": [
            "Авторские украшения с крупным барочным жемчугом отборной селекции. Ручная работа.",
            "Каждая барочная жемчужина уникальна по форме и сиянию. Стойкая гипоаллергенная фурнитура.",
            "Экспресс-доставка СДЭК по Астане, Алматы и всему Казахстану. Оплата через Kaspi Pay.",
            "Напишите в WhatsApp: снимем видео конкретного колье перед заказом и поможем с выбором."
        ]
    },

    # 5. Гематит -> https://livijewelry.kz/ukrasheniya-iz-gematita.html
    {
        "name": "Украшения из гематита",
        "url": "https://livijewelry.kz/ukrasheniya-iz-gematita.html",
        "keywords": [
            ("украшения из гематита купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gematita.html"),
            ("украшения из гематита купить", "Exact", "https://livijewelry.kz/ukrasheniya-iz-gematita.html"),
            ("колье из гематита", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gematita.html"),
            ("колье из гематита", "Exact", "https://livijewelry.kz/ukrasheniya-iz-gematita.html"),
            ("браслет из гематита алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gematita.html"),
            ("бусы из гематита купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gematita.html"),
            ("колье из тигрового глаза и гематита", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gematita.html"),
            ("чокер из гематита", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gematita.html"),
            ("натуральный гематит украшения", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gematita.html")
        ],
        "headlines": [
            "Украшения из гематита", "Колье из гематита Алматы", "Браслеты из гематита",
            "Livi Jewelry — Гематит", "Графитовый зеркальный блеск", "Натуральный камень гематит",
            "Доставка СДЭК по РК", "Подарочный футляр 0 ₸", "Счёт в Kaspi Pay",
            "Гематит + Тигровый глаз", "В наличии в Астане", "Видео украшений в WhatsApp",
            "Стильная геометрия камня", "Бутик Livi Jewelry", "Каталог гематита 2026"
        ],
        "descriptions": [
            "Стильные украшения из натурального гематита с зеркальным металлическим блеском.",
            "Колье и браслеты ручной сборки. Сочетания с тигровым глазом и нефритом.",
            "Быстрая доставка СДЭК по Казахстану. Фирменная подарочная упаковка включена.",
            "Заказ и консультация мастера в WhatsApp. Быстрый счет в приложении Kaspi Pay."
        ]
    },

    # 6. Малахит -> https://livijewelry.kz/ukrasheniya-iz-malahita.html
    {
        "name": "Украшения из малахита",
        "url": "https://livijewelry.kz/ukrasheniya-iz-malahita.html",
        "keywords": [
            ("украшения из малахита алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-malahita.html"),
            ("украшения из малахита алматы", "Exact", "https://livijewelry.kz/ukrasheniya-iz-malahita.html"),
            ("браслет из малахита алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-malahita.html"),
            ("браслет из малахита алматы", "Exact", "https://livijewelry.kz/ukrasheniya-iz-malahita.html"),
            ("браслет из натурального малахита", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-malahita.html"),
            ("колье из малахита купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-malahita.html"),
            ("бусы из малахита астана", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-malahita.html"),
            ("натуральный малахит украшения", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-malahita.html"),
            ("украшения с малахитом казахстан", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-malahita.html")
        ],
        "headlines": [
            "Украшения из малахита", "Браслет из малахита Алматы", "Натуральный малахит купить",
            "Livi Jewelry — Малахит", "Изумрудный узор малахита", "100% природный малахит",
            "Доставка СДЭК по РК", "Подарочная упаковка 0 ₸", "Счёт в Kaspi Pay",
            "Малахит ручной сборки", "В наличии в Астане", "Видео минерала в WhatsApp",
            "Глубокий изумрудный цвет", "Бутик камней Livi", "Каталог малахита 2026"
        ],
        "descriptions": [
            "Авторские браслеты и колье из натурального малахита с неповторимым шелковым узором.",
            "Отборные природные камни ручной сборки. Гипоаллергенная родированная фурнитура.",
            "Экспресс-доставка СДЭК по Астане, Алматы и всему Казахстану. Оплата в Kaspi Pay.",
            "Напишите в WhatsApp: пришлем макро-видео перелива малахита и подберем размер."
        ]
    },

    # 7. Аметист -> https://livijewelry.kz/ukrasheniya-iz-ametista.html
    {
        "name": "Украшения из аметиста",
        "url": "https://livijewelry.kz/ukrasheniya-iz-ametista.html",
        "keywords": [
            ("украшения из аметиста алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-ametista.html"),
            ("украшения из аметиста алматы", "Exact", "https://livijewelry.kz/ukrasheniya-iz-ametista.html"),
            ("колье из аметиста купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-ametista.html"),
            ("колье из аметиста купить", "Exact", "https://livijewelry.kz/ukrasheniya-iz-ametista.html"),
            ("браслет из аметиста астана", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-ametista.html"),
            ("комплект из аметиста", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-ametista.html"),
            ("бусы из натурального аметиста", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-ametista.html"),
            ("серьги с аметистом ручной работы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-ametista.html"),
            ("колье из аметиста и розового кварца", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-ametista.html")
        ],
        "headlines": [
            "Украшения из аметиста", "Колье из аметиста Алматы", "Аметист ручной работы",
            "Livi Jewelry — Аметист", "Благородный фиолетовый цвет", "100% природный аметист",
            "Доставка СДЭК по РК", "Подарочный футляр 0 ₸", "Счёт в Kaspi Pay",
            "Аметист + Розовый кварц", "В наличии в Астане", "Видео аметиста в WhatsApp",
            "Нежный лавандовый блеск", "Бутик аметиста Livi", "Каталог аметиста 2026"
        ],
        "descriptions": [
            "Изысканные колье, браслеты и сеты из природного аметиста. Глубокий лавандовый оттенок.",
            "Ручная сборка в ателье Livi Jewelry. Премиальная подарочная упаковка включена.",
            "Быстрая доставка курьером СДЭК до двери по Казахстану. Оплата в приложении Kaspi.",
            "Свяжитесь с мастером в WhatsApp: снимем видео украшения при дневном свете."
        ]
    },

    # 8. Гранат -> https://livijewelry.kz/ukrasheniya-iz-granata.html
    {
        "name": "Украшения из граната",
        "url": "https://livijewelry.kz/ukrasheniya-iz-granata.html",
        "keywords": [
            ("украшения из граната алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-granata.html"),
            ("украшения из граната алматы", "Exact", "https://livijewelry.kz/ukrasheniya-iz-granata.html"),
            ("колье из граната купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-granata.html"),
            ("колье из натурального граната", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-granata.html"),
            ("колье из натурального граната", "Exact", "https://livijewelry.kz/ukrasheniya-iz-granata.html"),
            ("бусы из граната астана", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-granata.html"),
            ("браслет из граната купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-granata.html"),
            ("колье из граната и жемчуга", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-granata.html"),
            ("натуральный гранат украшения", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-granata.html")
        ],
        "headlines": [
            "Украшения из граната", "Колье из граната купить", "Натуральный гранат Алматы",
            "Livi Jewelry — Гранат", "Глубокий винный оттенок", "100% природный гранат",
            "Доставка СДЭК по РК", "Подарочная упаковка 0 ₸", "Счёт в Kaspi Pay",
            "Гранат + Натуральный жемчуг", "В наличии в Астане", "Видео граната в WhatsApp",
            "Изысканный бардовый блеск", "Бутик граната Livi", "Каталог граната 2026"
        ],
        "descriptions": [
            "Роскошные колье и браслеты из граненого природного граната. Благородный винный цвет.",
            "Ручная сборка мастера. Сочетания граната с белым жемчугом и черным агатом.",
            "Экспресс-доставка СДЭК до двери по всему Казахстану. Фирменная коробка в подарок.",
            "Консультация мастера и живое видео изделий в WhatsApp. Оплата через Kaspi Pay."
        ]
    },

    # 9. Розовый кварц -> https://livijewelry.kz/ukrasheniya-iz-rozovogo-kvarca.html
    {
        "name": "Украшения из розового кварца",
        "url": "https://livijewelry.kz/ukrasheniya-iz-rozovogo-kvarca.html",
        "keywords": [
            ("украшения из розового кварца алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-rozovogo-kvarca.html"),
            ("украшения из розового кварца алматы", "Exact", "https://livijewelry.kz/ukrasheniya-iz-rozovogo-kvarca.html"),
            ("колье из розового кварца", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-rozovogo-kvarca.html"),
            ("чокер из розового кварца", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-rozovogo-kvarca.html"),
            ("браслет из розового кварца", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-rozovogo-kvarca.html"),
            ("бусы из розового кварца купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-rozovogo-kvarca.html"),
            ("сет колье с розовым кварцем", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-rozovogo-kvarca.html"),
            ("розовый кварц украшения казахстан", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-rozovogo-kvarca.html")
        ],
        "headlines": [
            "Розовый кварц — Украшения", "Колье из розового кварца", "Розовый кварц в Алматы",
            "Livi Jewelry — Кварц", "Нежнейший пастельный оттенок", "100% природный кварц",
            "Доставка СДЭК по РК", "Подарочный футляр 0 ₸", "Счёт в Kaspi Pay",
            "Розовый кварц + Жемчуг", "В наличии в Астане", "Видео перелива в WhatsApp",
            "Символ нежности и любви", "Бутик кварца Livi", "Каталог кварца 2026"
        ],
        "descriptions": [
            "Нежные авторские колье, чокеры и сеты из природного розового кварца и жемчуга.",
            "Ручная работа. Камни отборной чистоты и мягкого пастельного свечения. Стойкий родий.",
            "Быстрая доставка курьером СДЭК по Астане, Алматы и Казахстану. Оплата в Kaspi Pay.",
            "Напишите нам в WhatsApp: снимем видео посадки украшения и поможем с выбором."
        ]
    },

    # 10. Бирюза -> https://livijewelry.kz/ukrasheniya-iz-biryuzy.html
    {
        "name": "Украшения из бирюзы",
        "url": "https://livijewelry.kz/ukrasheniya-iz-biryuzy.html",
        "keywords": [
            ("украшения из натуральной бирюзы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-biryuzy.html"),
            ("украшения из натуральной бирюзы", "Exact", "https://livijewelry.kz/ukrasheniya-iz-biryuzy.html"),
            ("браслет из бирюзы алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-biryuzy.html"),
            ("комплект из бирюзы купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-biryuzy.html"),
            ("комплект из бирюзы купить", "Exact", "https://livijewelry.kz/ukrasheniya-iz-biryuzy.html"),
            ("колье из бирюзы астана", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-biryuzy.html"),
            ("бусы из бирюзы натуральной", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-biryuzy.html"),
            ("натуральная бирюза украшения казахстан", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-biryuzy.html"),
            ("серьги с бирюзой купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-biryuzy.html")
        ],
        "headlines": [
            "Украшения из бирюзы", "Комплект из бирюзы Алматы", "Натуральная бирюза купить",
            "Livi Jewelry — Бирюза", "Яркий лазурный цвет", "100% природная бирюза",
            "Доставка СДЭК по РК", "Подарочная упаковка 0 ₸", "Счёт в Kaspi Pay",
            "Колье, браслет, серьги", "В наличии в Астане", "Видео бирюзы в WhatsApp",
            "Восточная эстетика камня", "Бутик бирюзы Livi", "Каталог бирюзы 2026"
        ],
        "descriptions": [
            "Эффектные колье, браслеты и полные комплекты из природной бирюзы ручной работы.",
            "Насыщенный небесно-голубой цвет. Надежная гипоаллергенная фурнитура с позолотой.",
            "Экспресс-доставка СДЭК по Астане, Алматы и всему Казахстану. Оплата в Kaspi Pay.",
            "Напишите мастеру в WhatsApp: пришлем видео сета из бирюзы и уточним параметры."
        ]
    },

    # 11. Горный хрусталь -> https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html
    {
        "name": "Украшения из хрусталя",
        "url": "https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html",
        "keywords": [
            ("украшения из горного хрусталя", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html"),
            ("украшения из горного хрусталя", "Exact", "https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html"),
            ("колье из горного хрусталя", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html"),
            ("бусы из горного хрусталя алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html"),
            ("колье из жемчуга и горного хрусталя", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html"),
            ("колье из жемчуга и горного хрусталя", "Exact", "https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html"),
            ("чокер из горного хрусталя", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html"),
            ("браслет из горного хрусталя", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html"),
            ("натуральный горный хрусталь", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-gornogo-hrustalya.html")
        ],
        "headlines": [
            "Горный хрусталь — Колье", "Украшения из хрусталя", "Горный хрусталь в Алматы",
            "Livi Jewelry — Хрусталь", "Кристальная прозрачность", "Природный горный хрусталь",
            "Доставка СДЭК по РК", "Подарочный футляр 0 ₸", "Счёт в Kaspi Pay",
            "Хрусталь + Барочный жемчуг", "В наличии в Астане", "Видео сверкания в WhatsApp",
            "Алмазный блеск граней", "Бутик хрусталя Livi", "Каталог хрусталя 2026"
        ],
        "descriptions": [
            "Сверкающие колье и браслеты из граненого природного горного хрусталя и жемчуга.",
            "Идеальная игра граней на свету. Премиальная селекция минералов и ручная сборка.",
            "Быстрая доставка курьером СДЭК до двери по Казахстану. Оплата в приложении Kaspi.",
            "Свяжитесь с мастером в WhatsApp: покажем сверкание хрусталя на живом видео."
        ]
    },

    # 12. Лунный камень и перламутр -> https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html
    {
        "name": "Лунный камень и перламутр",
        "url": "https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html",
        "keywords": [
            ("украшения из лунного камня", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html"),
            ("украшения из лунного камня", "Exact", "https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html"),
            ("колье из лунного камня", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html"),
            ("чокер из лунного камня", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html"),
            ("бусы из лунного камня алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html"),
            ("украшения из перламутра купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html"),
            ("колье из перламутра астана", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html"),
            ("колье из жемчуга майорка", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html"),
            ("украшения с лунным камнем казахстан", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lunnogo-kamnya.html")
        ],
        "headlines": [
            "Лунный камень — Украшения", "Украшения из лунного камня", "Колье из перламутра",
            "Livi Jewelry — Перламутр", "Мягкое шелковое сияние", "100% природный минерал",
            "Доставка СДЭК по РК", "Подарочная упаковка 0 ₸", "Счёт в Kaspi Pay",
            "Лунный камень + Майорка", "В наличии в Астане", "Видео сияния в WhatsApp",
            "Загадочный перелив камня", "Бутик перламутра Livi", "Каталог камней 2026"
        ],
        "descriptions": [
            "Утонченные украшения из натурального лунного камня, жемчуга Майорка и перламутра.",
            "Таинственное внутреннее свечение минерала. Ручная работа мастера ателье Livi.",
            "Экспресс-доставка СДЭК по Астане, Алматы и всему Казахстану. Оплата в Kaspi Pay.",
            "Напишите в WhatsApp: покажем мягкое свечение лунного камня на видео и поможем с заказом."
        ]
    },

    # 13. Колье из жемчуга (основная категория) -> https://livijewelry.kz/kolye-iz-zhemchuga.html
    {
        "name": "Колье из жемчуга",
        "url": "https://livijewelry.kz/kolye-iz-zhemchuga.html",
        "keywords": [
            ("колье из натурального жемчуга", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("колье из натурального жемчуга", "Exact", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("купить колье из жемчуга", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("купить жемчужное колье", "Exact", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("бусы из натурального жемчуга алматы", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("авторское колье из жемчуга", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("многорядное колье из жемчуга", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("жемчужные бусы астана купить", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html")
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

    # 14. Браслеты из жемчуга и камней -> https://livijewelry.kz/braslety-iz-zhemchuga.html
    {
        "name": "Браслеты из жемчуга",
        "url": "https://livijewelry.kz/braslety-iz-zhemchuga.html",
        "keywords": [
            ("браслет из натуральных камней купить", "Phrase", "https://livijewelry.kz/braslety-iz-zhemchuga.html"),
            ("браслет из натуральных камней купить", "Exact", "https://livijewelry.kz/braslety-iz-zhemchuga.html"),
            ("браслет из жемчуга алматы", "Phrase", "https://livijewelry.kz/braslety-iz-zhemchuga.html"),
            ("браслет из жемчуга алматы", "Exact", "https://livijewelry.kz/braslety-iz-zhemchuga.html"),
            ("браслет из натурального жемчуга", "Phrase", "https://livijewelry.kz/braslety-iz-zhemchuga.html"),
            ("браслет из барочного жемчуга", "Phrase", "https://livijewelry.kz/braslety-iz-zhemchuga.html"),
            ("браслет из натуральных минералов казахстан", "Phrase", "https://livijewelry.kz/braslety-iz-zhemchuga.html")
        ],
        "headlines": [
            "Браслеты из жемчуга и камней", "Браслет из жемчуга Алматы", "Украшения на запястье",
            "Livi Jewelry — Браслеты", "100% натуральные минералы", "Доставка СДЭК по Казахстану",
            "Браслеты ручной работы", "Удаленный счёт Kaspi Pay", "Подарочная шкатулка к заказу",
            "В наличии с быстрой доставкой", "Подбор размера на запястье", "Заказ и примерка в WhatsApp",
            "Видео перелива минералов в чат", "Бутик украшений Livi", "Каталог браслетов 2026"
        ],
        "descriptions": [
            "Браслеты ручной работы из натурального жемчуга и природных минералов. Отборные камни.",
            "Экспресс-доставка СДЭК до двери или в ПВЗ. Удобная оплата через счёт Kaspi Pay.",
            "Изысканные браслеты с натуральными камнями. Подарочная шкатулка к каждому заказу.",
            "Свяжитесь с мастером в WhatsApp: пришлем видео перелива камней и поможем с выбором."
        ]
    },

    # 15. Серьги из жемчуга и камней -> https://livijewelry.kz/sergi-iz-zhemchuga.html
    {
        "name": "Серьги из жемчуга",
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
            ("длинные серьги с жемчугом", "Phrase", "https://livijewelry.kz/sergi-iz-zhemchuga.html"),
            ("серьги с натуральными камнями купить", "Phrase", "https://livijewelry.kz/sergi-iz-zhemchuga.html")
        ],
        "headlines": [
            "Серьги из жемчуга в Алматы", "Серьги с барочным жемчугом", "Livi Jewelry — Серьги",
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

    # 16. Подарки и авторские украшения -> https://livijewelry.kz/shop.html
    {
        "name": "Подарки и авторские украшения",
        "url": "https://livijewelry.kz/shop.html",
        "keywords": [
            ("подарок девушке украшения алматы", "Phrase", "https://livijewelry.kz/shop.html"),
            ("подарок девушке украшения алматы", "Exact", "https://livijewelry.kz/shop.html"),
            ("подарок жене на день рождения украшения", "Phrase", "https://livijewelry.kz/shop.html"),
            ("подарок маме украшения алматы", "Phrase", "https://livijewelry.kz/shop.html"),
            ("авторские украшения ручной работы", "Phrase", "https://livijewelry.kz/shop.html"),
            ("авторские украшения ручной работы", "Exact", "https://livijewelry.kz/shop.html"),
            ("ювелирная бижутерия алматы", "Phrase", "https://livijewelry.kz/shop.html"),
            ("дизайнерские украшения ручной работы казахстан", "Phrase", "https://livijewelry.kz/shop.html"),
            ("украшения ручной работы астана", "Phrase", "https://livijewelry.kz/shop.html"),
            ("украшения ручной работы астана", "Exact", "https://livijewelry.kz/shop.html"),
            ("украшения на кыз узату алматы", "Phrase", "https://livijewelry.kz/shop.html"),
            ("украшения невесты из жемчуга", "Phrase", "https://livijewelry.kz/kolye-iz-zhemchuga.html"),
            ("авторская бижутерия купить алматы", "Exact", "https://livijewelry.kz/shop.html"),
            ("подарок женщине ювелирные украшения", "Phrase", "https://livijewelry.kz/shop.html")
        ],
        "headlines": [
            "Подарок девушке — Украшения", "Авторские украшения Livi", "Ювелирная бижутерия Алматы",
            "Идеальный подарок со вкусом", "Натуральный жемчуг и камни", "Доставка СДЭК по Казахстану",
            "Фирменная упаковка в подарок", "Счёт в приложении Kaspi.kz", "В наличии с быстрой доставкой",
            "Подарок на день рождения", "Индивидуальная подгонка", "Заказ и видео в WhatsApp",
            "Эксклюзив ручной работы", "Бутик Livi Jewelry", "Каталог подарков 2026"
        ],
        "descriptions": [
            "Ищете изысканный подарок? Авторские украшения из натурального жемчуга и камней.",
            "Премиальная подарочная коробка к каждому заказу. Доставка СДЭК в любой город Казахстана.",
            "Счёт на оплату в Kaspi.kz. 100% совпадение с фото. Консультация мастера онлайн.",
            "Напишите нам в WhatsApp: снимем видео изделия и поможем сделать незабываемый подарок!"
        ]
    },

    # 17. Жемчуг Майорка -> https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html
    {
        "name": "Жемчуг Майорка",
        "url": "https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html",
        "keywords": [
            ("украшения из жемчуга майорка", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html"),
            ("украшения из жемчуга майорка", "Exact", "https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html"),
            ("колье жемчуг майорка купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html"),
            ("бусы майорка алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html"),
            ("испанский жемчуг майорка", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html"),
            ("колье из майорки астана", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html"),
            ("серьги майорка купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html"),
            ("браслет из майорки казахстан", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html"),
            ("украшения майорка ручной работы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-zhemchuga-mayorka.html")
        ],
        "headlines": [
            "Жемчуг Майорка — Колье", "Украшения жемчуг Майорка", "Испанский жемчуг Майорка",
            "Livi Jewelry — Майорка", "Идеальный глянец и гладь", "Органический жемчуг Майорка",
            "Доставка СДЭК по РК", "Подарочная упаковка 0 ₸", "Счёт в Kaspi Pay",
            "Колье, браслеты, серьги", "В наличии в Астане", "Видео украшений в WhatsApp",
            "Премиум качество Майорка", "Бутик Livi Jewelry", "Каталог Майорка 2026"
        ],
        "descriptions": [
            "Авторские колье и браслеты из жемчуга Майорка. Идеальный зеркальный глянец и прочность.",
            "Экспресс-доставка СДЭК по Астане, Алматы и Казахстану. Удобная оплата через Kaspi Pay.",
            "Стильные украшения из жемчуга Майорка ручной работы. Подарочная упаковка в комплекте.",
            "Напишите мастеру в WhatsApp: снимем видео сияния жемчуга Майорка и подберем размер."
        ]
    },

    # 18. Украшения из тигрового глаза -> https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html
    {
        "name": "Украшения из тигрового глаза",
        "url": "https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html",
        "keywords": [
            ("украшения из тигрового глаза", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html"),
            ("украшения из тигрового глаза", "Exact", "https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html"),
            ("колье из тигрового глаза купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html"),
            ("браслет тигровый глаз алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html"),
            ("браслет тигровый глаз алматы", "Exact", "https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html"),
            ("бусы из тигрового глаза астана", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html"),
            ("тигровый глаз украшения казахстан", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html"),
            ("чокер из тигрового глаза", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html"),
            ("натуральный тигровый глаз купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-tigrovogo-glaza.html")
        ],
        "headlines": [
            "Тигровый глаз — Украшения", "Колье из тигрового глаза", "Браслет тигровый глаз",
            "Livi Jewelry — Минералы", "Шелковистый перелив камня", "100% природный минерал",
            "Доставка СДЭК по РК", "Подарочная упаковка 0 ₸", "Счёт в Kaspi Pay",
            "Тигровый глаз + Гематит", "В наличии в Астане", "Видео камней в WhatsApp",
            "Мощная энергетика камня", "Бутик минералов Livi", "Каталог тигровый глаз 2026"
        ],
        "descriptions": [
            "Эффектные колье и браслеты из природного тигрового глаза. Золотисто-коричневый перелив.",
            "Авторская ручная сборка. Сочетания тигрового глаза с гематитом и натуральным жемчугом.",
            "Быстрая доставка курьером СДЭК до двери по Казахстану. Оплата в приложении Kaspi Pay.",
            "Напишите мастеру в WhatsApp: пришлем живое видео перелива камня и поможем с заказом."
        ]
    },

    # 19. Коралл и яшма -> https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html
    {
        "name": "Коралл и яшма",
        "url": "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html",
        "keywords": [
            ("украшения из коралла и яшмы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html"),
            ("украшения из коралла и яшмы", "Exact", "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html"),
            ("колье из коралла купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html"),
            ("колье из коралла купить", "Exact", "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html"),
            ("бусы из натурального коралла", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html"),
            ("браслет из яшмы алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html"),
            ("украшения из красного коралла", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html"),
            ("колье из яшмы астана", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html"),
            ("комплект из коралла казахстан", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html"),
            ("сет из коралла и жемчуга", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-koralla-i-yashmy.html")
        ],
        "headlines": [
            "Коралл и яшма — Украшения", "Колье из коралла купить", "Украшения из яшмы Алматы",
            "Livi Jewelry — Коралл", "Яркий терракотовый цвет", "100% природные минералы",
            "Доставка СДЭК по РК", "Подарочная коробка 0 ₸", "Счёт в Kaspi Pay",
            "Коралл + Натуральный жемчуг", "В наличии в Астане", "Видео минералов в WhatsApp",
            "Этнический шик и классика", "Бутик украшений Livi", "Каталог коралл 2026"
        ],
        "descriptions": [
            "Колье, браслеты и сеты из натурального коралла и пейзажной яшмы. Яркие природные цвета.",
            "Ручная сборка с отборным жемчугом. Надежная гипоаллергенная фурнитура с позолотой.",
            "Экспресс-доставка СДЭК по Астане, Алматы и Казахстану. Удобная оплата через Kaspi Pay.",
            "Консультация мастера в WhatsApp: пришлем видео примерки колье и подберем размер."
        ]
    },

    # 20. Украшения из лазурита -> https://livijewelry.kz/ukrasheniya-iz-lazurita.html
    {
        "name": "Украшения из лазурита",
        "url": "https://livijewelry.kz/ukrasheniya-iz-lazurita.html",
        "keywords": [
            ("украшения из лазурита", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lazurita.html"),
            ("украшения из лазурита", "Exact", "https://livijewelry.kz/ukrasheniya-iz-lazurita.html"),
            ("колье из лазурита купить", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lazurita.html"),
            ("колье из лазурита купить", "Exact", "https://livijewelry.kz/ukrasheniya-iz-lazurita.html"),
            ("браслет из лазурита алматы", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lazurita.html"),
            ("бусы из натурального лазурита", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lazurita.html"),
            ("чокер из лазурита астана", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lazurita.html"),
            ("лазурит украшения казахстан", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lazurita.html"),
            ("колье из лазурита и жемчуга", "Phrase", "https://livijewelry.kz/ukrasheniya-iz-lazurita.html")
        ],
        "headlines": [
            "Украшения из лазурита", "Колье из лазурита купить", "Браслет из лазурита Алматы",
            "Livi Jewelry — Лазурит", "Королевский ультрамарин", "Природный лазурит с пиритом",
            "Доставка СДЭК по РК", "Подарочная коробка 0 ₸", "Счёт в Kaspi Pay",
            "Лазурит + Барочный жемчуг", "В наличии в Астане", "Видео лазурита в WhatsApp",
            "Глубокий синий оттенок", "Бутик лазурита Livi", "Каталог лазурита 2026"
        ],
        "descriptions": [
            "Благородные колье и браслеты из природного лазурита глубокого ультрамаринового цвета.",
            "Золотистые искры пирита и натуральный жемчуг. Ручная работа мастера ателье Livi.",
            "Быстрая доставка СДЭК до двери по всему Казахстану. Оплата в приложении Kaspi Pay.",
            "Свяжитесь с мастером в WhatsApp: снимем видео сияния лазурита и поможем с выбором."
        ]
    },

    # 21. Цепи с барочным жемчугом -> https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html
    {
        "name": "Цепи с барочным жемчугом",
        "url": "https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html",
        "keywords": [
            ("цепь с барочным жемчугом", "Phrase", "https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html"),
            ("цепь с барочным жемчугом", "Exact", "https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html"),
            ("колье цепь с жемчужиной", "Phrase", "https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html"),
            ("колье цепь с жемчужиной", "Exact", "https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html"),
            ("массивная цепь с жемчугом алматы", "Phrase", "https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html"),
            ("крупная цепь с подвеской жемчуг", "Phrase", "https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html"),
            ("колье цепочка с барочным жемчугом", "Phrase", "https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html"),
            ("цепь с жемчугом астана купить", "Phrase", "https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html"),
            ("трендовая цепь с жемчугом казахстан", "Phrase", "https://livijewelry.kz/tsepi-s-barochnym-zhemchugom.html")
        ],
        "headlines": [
            "Цепи с барочным жемчугом", "Колье-цепь с жемчужиной", "Массивные цепи с жемчугом",
            "Livi Jewelry — Цепи", "Барочная жемчужина подвес", "Стойкая позолота и родий",
            "Доставка СДЭК по РК", "Подарочная шкатулка 0 ₸", "Счёт в Kaspi Pay",
            "Трендовое колье 2026", "В наличии в Астане", "Видео примерки в WhatsApp",
            "Городской шик и акцент", "Бутик цепей Livi", "Каталог цепей 2026"
        ],
        "descriptions": [
            "Трендовые колье-цепи со съемными кулонами из крупного барочного жемчуга. Ручная сборка.",
            "Стойкое гипоаллергенное покрытие золотом 18К и родием. Идеальный акцент под любой образ.",
            "Экспресс-доставка СДЭК по Астане, Алматы и Казахстану. Удобная оплата через Kaspi Pay.",
            "Напишите мастеру в WhatsApp: покажем варианты плетения цепей и посадку на видео."
        ]
    },

    # 22. Кольца и комплекты из камней -> https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html
    {
        "name": "Кольца и комплекты из камней",
        "url": "https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html",
        "keywords": [
            ("кольца с натуральными камнями", "Phrase", "https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html"),
            ("кольца с натуральными камнями", "Exact", "https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html"),
            ("кольцо с жемчугом купить алматы", "Phrase", "https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html"),
            ("кольцо с жемчугом купить алматы", "Exact", "https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html"),
            ("комплект кольцо и серьги жемчуг", "Phrase", "https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html"),
            ("авторские кольца из камней астана", "Phrase", "https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html"),
            ("кольцо с барочным жемчугом казахстан", "Phrase", "https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html"),
            ("ювелирный комплект с кольцом", "Phrase", "https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html"),
            ("широкое кольцо с натуральным камнем", "Phrase", "https://livijewelry.kz/koltsa-i-garnitury-iz-kamney.html")
        ],
        "headlines": [
            "Кольца с натуральными камнями", "Кольцо с жемчугом Алматы", "Комплекты кольцо + серьги",
            "Livi Jewelry — Кольца", "Барочный жемчуг и камни", "Регулируемый размер кольца",
            "Доставка СДЭК по РК", "Подарочный футляр 0 ₸", "Счёт в Kaspi Pay",
            "Полный комплект со скидкой", "В наличии в Астане", "Видео колец в WhatsApp",
            "Удобная посадка на палец", "Бутик колец Livi", "Каталог колец 2026"
        ],
        "descriptions": [
            "Авторские кольца и полные комплекты с барочным жемчугом и натуральными самоцветами.",
            "Удобные безразмерные основы или точная подгонка. Стойкое родирование и позолота.",
            "Быстрая доставка СДЭК до двери по Казахстану. Фирменная подарочная упаковка к заказу.",
            "Свяжитесь с нами в WhatsApp: пришлем видео примерки кольца и комплекта на руке."
        ]
    }
]

# ==============================================================================
# 2.1 ИНТЕГРАЦИЯ SEARCH_KEYWORDS ИЗ PRODUCTS.JSON С ПРИВЯЗКОЙ К СТРАНИЦАМ ТОВАРОВ
# ==============================================================================
def map_product_to_ad_group(p):
    title = (p.get("title") or "").lower()
    materials = " ".join(p.get("materials") or []).lower()
    category = p.get("category") or ""
    full_text = f"{title} {materials}"

    if "майорк" in full_text:
        return "Жемчуг Майорка"
    if "тигров" in full_text:
        return "Украшения из тигрового глаза"
    if "коралл" in full_text or "яшм" in full_text:
        return "Коралл и яшма"
    if "лазурит" in full_text:
        return "Украшения из лазурита"
    if "цеп" in full_text and ("бароч" in full_text or "жемчуг" in full_text):
        return "Цепи с барочным жемчугом"
    if category == "Rings" or "кольц" in full_text:
        return "Кольца и комплекты из камней"
    if category == "Sets" or "комплект" in full_text or "комплект" in full_text:
        return "Комплекты украшений"
    if "чокер" in full_text:
        return "Чокеры из камней"
    if "сотуар" in full_text or "галстук" in full_text:
        return "Сотуары и галстуки"
    if "гематит" in full_text:
        return "Украшения из гематита"
    if "малахит" in full_text:
        return "Украшения из малахита"
    if "аметист" in full_text:
        return "Украшения из аметиста"
    if "гранат" in full_text:
        return "Украшения из граната"
    if "розов" in full_text and "кварц" in full_text:
        return "Украшения из розового кварца"
    if "бирюз" in full_text:
        return "Украшения из бирюзы"
    if "хрустал" in full_text:
        return "Украшения из хрусталя"
    if "лунн" in full_text or "перламутр" in full_text:
        return "Лунный камень и перламутр"
    if "бароч" in full_text:
        return "Барочный жемчуг"
    if category == "Earrings" or "серьг" in full_text:
        return "Серьги из жемчуга"
    if category == "Bracelets" or "браслет" in full_text:
        return "Браслеты из жемчуга"
    if category == "Necklaces" or "колье" in full_text:
        return "Колье из жемчуга"
    return "Подарки и авторские украшения"

try:
    with open("products.json", "r", encoding="utf-8") as pf:
        products_catalog = json.load(pf)
    
    group_by_name = {g["name"]: g for g in ad_groups_data}
    added_product_kws = 0

    for p in products_catalog:
        target_group_name = map_product_to_ad_group(p)
        target_group = group_by_name.get(target_group_name, group_by_name["Подарки и авторские украшения"])
        prod_url = f"https://livijewelry.kz/product/{p['id']}.html"
        existing_kws_in_group = {item[0].lower() for item in target_group["keywords"]}

        for kw in p.get("search_keywords", []):
            kw_clean = kw.strip()
            if not kw_clean:
                continue
            kw_lower = kw_clean.lower()
            if kw_lower not in existing_kws_in_group:
                target_group["keywords"].append((kw_clean, "Phrase", prod_url))
                target_group["keywords"].append((kw_clean, "Exact", prod_url))
                existing_kws_in_group.add(kw_lower)
                added_product_kws += 2

    print(f"[OK] Added {added_product_kws} keywords from products.json into ad groups with product Final URLs")
except Exception as e:
    print(f"[WARN] Failed to load search_keywords from products.json: {e}")

# Валидация длины заголовков (<= 30) и описаний (<= 90) для Google Ads
for group in ad_groups_data:
    for h in group["headlines"]:
        if len(h) > 30:
            raise ValueError(f"Headline too long ({len(h)} > 30) in {group['name']}: '{h}'")
    for d in group["descriptions"]:
        if len(d) > 90:
            raise ValueError(f"Description too long ({len(d)} > 90) in {group['name']}: '{d}'")

# Write 1_google_ads_keywords.csv
try:
    import generate_ads_keywords_csv
    generate_ads_keywords_csv.main()
    print("[OK] 1_google_ads_keywords.csv: synced via generate_ads_keywords_csv.py")
except Exception as e:
    print(f"[WARN] Failed to run generate_ads_keywords_csv: {e}")

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

print(f"[OK] google_ads_campaign_import.csv: {len(rows)} rows generated successfully across {len(ad_groups_data)} ad groups")

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
