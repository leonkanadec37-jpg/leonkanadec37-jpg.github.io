#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Livi Jewelry — Programmatic SEO Hub Generator (generate_seo_hubs.py)
Generates static indexable HTML landing pages for stone clusters and jewelry categories,
and injects internal linking blocks across existing category/catalog pages.
"""

import os
import re
import json

BASE_URL = "https://livijewelry.kz"
PRODUCTS_FILE = "products.json"

ALL_HUBS = [
    {
        "slug": "komplekty-ukrasheniy.html",
        "chip_label": "Комплекты украшений",
        "h1": "Комплекты украшений из натуральных камней и жемчуга ручной работы",
        "title_cluster": "комплекты украшений из натуральных камней и жемчуга",
        "breadcrumb": "Комплекты украшений",
        "eyebrow": "Haute Joaillerie • Ювелирные сеты",
        "lead": "Авторские гарнитуры и сеты из натурального жемчуга, аметиста, малахита, бирюзы и розового кварца. Каждое изделие из комплекта можно приобрести полным сетом или по отдельности с индивидуальной подгонкой длины.",
        "filter_type": "category",
        "filter_val": "Sets",
        "stone_name_gen": "натуральных камней и жемчуга",
        "stone_name_prep": "комплектах украшений",
        "seo_title": "Эксклюзивные комплекты украшений ручной сборки в ателье Livi Jewelry",
        "seo_p1": "Ювелирный гарнитур из натуральных минералов и культивированного жемчуга — это безупречно выверенный ансамбль, в котором колье, браслет, серьги и кольцо гармонируют по оттенку, калибру камней и стилю фурнитуры. В мастерской Livi Jewelry (Астана, Казахстан) мы собираем комплекты вручную, тщательно отбирая каждый минерал по чистоте рисунка и глубине природного блеска. Вы можете приобрести как готовый сет целиком, так и отдельные его элементы.",
        "seo_p2": "Каждое украшение создается на ювелирном тросике высокой прочности с использованием гипоаллергенной фурнитуры премиум-класса (стойкое родирование или позолота 18K). Перед отправкой мастер бесплатно адаптирует длину колье и обхват браслета под ваши индивидуальные мерки, чтобы посадка была идеальной. Все комплекты упаковываются в фирменную подарочную шкатулку и доставляются курьером день в день по Астане или экспресс-службой СДЭК в Алматы и любой город Казахстана за 1–3 рабочих дня."
    },
    {
        "slug": "chokery-iz-naturalnyh-kamney.html",
        "chip_label": "Чокеры из камней",
        "h1": "Чокеры из натуральных камней и жемчуга",
        "title_cluster": "чокеры из натуральных камней и жемчуга",
        "breadcrumb": "Чокеры из натуральных камней",
        "eyebrow": "Haute Joaillerie • Изящный акцент на ключицах",
        "lead": "Утонченные чокеры и короткие колье из природного граната, флюорита, жемчуга, лазурита и гематита. Бесплатная комплектация удлинительной цепочкой 5 см для комфортной регулировки посадки.",
        "filter_type": "choker",
        "filter_val": ["чокер", "колье из"],
        "stone_name_gen": "натуральных самоцветов и жемчуга",
        "stone_name_prep": "чокерах из камней",
        "seo_title": "Чокеры из натуральных камней и речного жемчуга — эстетика и ручная работа",
        "seo_p1": "Чокер из натуральных камней — главный ювелирный тренд, который деликатно подчеркивает линию шеи и ключицы. В коллекции Livi Jewelry представлены чокеры и прилегающие колье (38–42 см) из граненого граната, благородного лазурита, полупрозрачного флюорита, тигрового глаза и барочного жемчуга. Природная огранка минералов создает живое мерцание при каждом движении и легко сочетается как с деловым жакетом, так и с вечерним платьем.",
        "seo_p2": "В ателье Livi Jewelry каждое изделие собирается вручную в единственном экземпляре или малой серией. Мы комплектуем чокеры удобной удлинительной цепочкой (+5 см) и надежными карабинами с родиевым или позолоченным покрытием, которое не темнеет и не вызывает аллергии. Доступна индивидуальная коррекция длины точно по обхвату вашей шеи и быстрая доставка СДЭК по всему Казахстану."
    },
    {
        "slug": "sotuary-iz-zhemchuga.html",
        "chip_label": "Сотуары",
        "h1": "Сотуары и колье-галстуки из жемчуга и камней",
        "title_cluster": "сотуары и колье-галстуки из жемчуга и камней",
        "breadcrumb": "Сотуары из жемчуга и камней",
        "eyebrow": "Haute Joaillerie • Удлиненный силуэт",
        "lead": "Аристократичные длинные сотуары и колье-галстуки из натурального жемчуга, агата, граната и горного хрусталя. Визуально вытягивают силуэт и добавляют образу утонченный французский шик.",
        "filter_type": "lariat",
        "filter_val": ["Lariats", "сотуар"],
        "stone_name_gen": "натурального жемчуга, агата и граната",
        "stone_name_prep": "сотуарах и колье-галстуках",
        "seo_title": "Длинные сотуары из натурального жемчуга и самоцветов от мастерской Livi Jewelry",
        "seo_p1": "Сотуар — культовое удлиненное украшение эпохи ар-деко, которое триумфально вернулось в современную моду Haute Joaillerie. Длинные нити из натурального жемчуга, черного агата и винного граната с изящными подвесками или шелковыми кистями визуально стройнят фигуру, акцентируют декольте и великолепно смотрятся поверх однотонного трикотажа, шелковых блуз и вечерних нарядов.",
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
        "seo_title": "Натуральный гематит в авторских колье и гарнитурах Livi Jewelry",
        "seo_p1": "Природный гематит ценится в высоком ювелирном искусстве за свой неповторимый зеркально-стальной отлив, приятную прохладу и благородную тяжесть. Граненые бусины и разделители из гематита создают выразительный контраст в сочетании с теплым тигровым глазом, изумрудным нефритом и перламутровым жемчугом, придавая украшению современный графичный характер.",
        "seo_p2": "В мастерской Livi Jewelry гематит проходит деликатную полировку, сохраняя стойкий металлический блеск на долгие годы. Мы используем гипоаллергенную фурнитуру с родированием и позолотой, бесплатно подгоняем длину колье или браслета под ваши мерки и бережно отправляем заказы курьером по Астане и службой СДЭК в Алматы и все регионы Казахстана."
    },
    {
        "slug": "ukrasheniya-iz-malahita.html",
        "chip_label": "Малахит",
        "h1": "Украшения из натурального малахита ручной работы",
        "title_cluster": "украшения из малахита",
        "breadcrumb": "Украшения из малахита",
        "eyebrow": "Изумрудная классика • Природный узор",
        "lead": "Изысканные браслеты, колье и комплекты из натурального малахита с уникальным ленточным рисунком и позолоченной фурнитурой. Ручная селекция камней в ателье Livi Jewelry.",
        "filter_type": "stone",
        "filter_val": ["малахит", "нефрит", "жадеит"],
        "stone_name_gen": "натурального малахита и зеленых самоцветов",
        "stone_name_prep": "украшениях из малахита",
        "seo_title": "Украшения из природного малахита — благородный изумрудный акцент",
        "seo_p1": "Натуральный малахит — один из самых узнаваемых и статусных самоцветов, прославленный своими концентрическими узорами от нежно-бирюзового до глубокого хвойно-изумрудного оттенка. В палитре Livi Jewelry малахит, а также родственные зеленые минералы (нефрит и жадеит) сочетаются с теплым сиянием позолоченной фурнитуры и натуральным жемчугом, создавая роскошный образ в стиле высоких ювелирных домов.",
        "seo_p2": "Каждая бусина малахита отбирается мастером вручную, чтобы рисунок камня раскрывался максимально выразительно. Мы бесплатно адаптируем размер браслета или колье под ваше запястье и шею, упаковываем изделие в подарочный футляр Livi Jewelry и обеспечиваем быструю доставку по Астане, Алматы и всему Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-ametista.html",
        "chip_label": "Аметист",
        "h1": "Украшения из натурального аметиста ручной работы",
        "title_cluster": "украшения из аметиста",
        "breadcrumb": "Украшения из аметиста",
        "eyebrow": "Королевский фиолетовый • Природный кварц",
        "lead": "Гарнитуры, колье, серьги и браслеты из натурального лавандового и глубокого фиолетового аметиста в дуэте с жемчугом и розовым кварцем.",
        "filter_type": "stone",
        "filter_val": ["аметист", "флюорит"],
        "stone_name_gen": "натурального аметиста",
        "stone_name_prep": "украшениях из аметиста",
        "seo_title": "Авторские украшения из натурального аметиста в ателье Livi Jewelry",
        "seo_p1": "Натуральный аметист — благородная фиолетовая разновидность кварца, которая с древности считается символом гармонии, утонченного вкуса и внутренней силы. Прозрачные и полупрозрачные грани аметиста великолепно преломляют дневной и вечерний свет, особенно в авторских сочетаниях с нежным розовым кварцем и классическим речным жемчугом.",
        "seo_p2": "В ателье Livi Jewelry вы можете купить комплекты, колье, серьги и броши-булавки из подлинного природного аметиста ручной сборки. По вашему выбору мы установим родированную или позолоченную гипоаллергенную фурнитуру, подгоним длину изделия по вашим меркам и доставим заказ в фирменной подарочной упаковке курьером по Астане или СДЭК по Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-granata.html",
        "chip_label": "Гранат",
        "h1": "Украшения из натурального граната ручной работы",
        "title_cluster": "украшения из граната",
        "breadcrumb": "Украшения из граната",
        "eyebrow": "Винный бархат • Граненый пироп и альмандин",
        "lead": "Колье, сотуары и комплекты из натурального граненого граната насыщенного бордово-винного оттенка в сочетании с черным агатом и перламутровым жемчугом.",
        "filter_type": "stone",
        "filter_val": ["гранат"],
        "stone_name_gen": "натурального граната",
        "stone_name_prep": "украшениях из граната",
        "seo_title": "Колье, сотуары и сеты из натурального граната — ручная сборка Livi Jewelry",
        "seo_p1": "Природный гранат завораживает глубоким винно-рубиновым цветом, который вспыхивает яркими искрами при попадании света на ювелирные грани. В коллекции Livi Jewelry гранат представлен как в сольных моно-колье, так и в драматичных контрастных композициях с бархатным черным агатом и белоснежным натуральным жемчугом.",
        "seo_p2": "Мы используем только натуральный граненый гранат высокой чистоты и собираем каждое украшение вручную на прочном ювелирном тросике с надежными замками из гипоаллергенного сплава (родий или позолота). Бесплатная регулировка длины, фирменная подарочная коробка и экспресс-доставка СДЭК в Алматы, Астану и по всему Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-rozovogo-kvarca.html",
        "chip_label": "Розовый кварц",
        "h1": "Украшения из розового кварца ручной работы",
        "title_cluster": "украшения из розового кварца",
        "breadcrumb": "Украшения из розового кварца",
        "eyebrow": "Пудровая нежность • Натуральный минерал",
        "lead": "Нежные колье, сеты и серьги из натурального розового кварца, речного жемчуга и аметиста. Освежают тон кожи и создают романтичный женственный образ.",
        "filter_type": "stone",
        "filter_val": ["розового кварца", "розовый кварц", "клубнич"],
        "stone_name_gen": "натурального розового кварца",
        "stone_name_prep": "украшениях из розового кварца",
        "seo_title": "Украшения из натурального розового кварца и жемчуга в Livi Jewelry",
        "seo_p1": "Натуральный розовый кварц — воплощение нежности и утонченной женственности. Его мягкий полупрозрачный пудровый оттенок обладает удивительным свойством освежать цвет лица и смягчать черты. В комбинации с натуральным речным жемчугом и лавандовым аметистом розовый кварц образует изысканную пастельную палитру, идеальную для свадебных, дневных и романтичных вечерних выходов.",
        "seo_p2": "Мастера Livi Jewelry вручную отбирают бусины розового кварца без грубых трещин и помутнений, дополняя их стойкой позолоченной или родированной фурнитурой. Каждое колье и комплект можно адаптировать под индивидуальную длину и приобрести как полным сетом, так и по отдельности с доставкой по Астане и Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-biryuzy.html",
        "chip_label": "Бирюза",
        "h1": "Украшения из натуральной бирюзы ручной работы",
        "title_cluster": "украшения из натуральной бирюзы",
        "breadcrumb": "Украшения из бирюзы",
        "eyebrow": "Небесная лазурь • Природная бирюза",
        "lead": "Полные ювелирные комплекты, колье, браслеты и серьги из натуральной бирюзы с благородной природной фактурой. Яркий статусный акцент в любое время года.",
        "filter_type": "stone",
        "filter_val": ["бирюз"],
        "stone_name_gen": "натуральной бирюзы",
        "stone_name_prep": "украшениях из бирюзы",
        "seo_title": "Комплекты и колье из натуральной бирюзы ручной работы — Livi Jewelry",
        "seo_p1": "Натуральная бирюза — камень с тысячелетней историей, который на Востоке и в мировом ювелирном искусстве почитается как талисман удачи, благополучия и королевского достоинства. Выразительный небесно-голубой и морской оттенок природной бирюзы мгновенно притягивает взгляды и великолепно оттеняет любой цветотип внешности.",
        "seo_p2": "В каталоге Livi Jewelry представлены роскошные гарнитуры из натуральной бирюзы (колье, браслет, серьги, кольцо), которые можно купить полным комплектом или выбрать отдельные изделия. Мы гарантируем ручную сборку, гипоаллергенную фурнитуру, бесплатную подгонку размера и быструю доставку в фирменной упаковке по Астане, Алматы и всему Казахстану."
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
        "seo_p1": "Горный хрусталь — кристально чистая прозрачная разновидность природного кварца. Его ледяной блеск и высокая светопреломляющая способность создают вокруг шеи и лица эффект легкого сияющего ореола. В сочетании с натуральным перламутровым жемчугом горный хрусталь придает многослойным колье воздушность и торжественную утонченность.",
        "seo_p2": "Каждое украшение с горным хрусталем и кварцем в ателье Livi Jewelry собирается вручную с использованием надежной гипоаллергенной фурнитуры (родий или позолота). Мы бесплатно скорректируем длину изделия под ваши пожелания и доставим заказ в подарочной шкатулке день в день по Астане или за 1–3 дня СДЭК по Казахстану."
    },
    {
        "slug": "ukrasheniya-iz-lunnogo-kamnya.html",
        "chip_label": "Лунный камень и перламутр",
        "h1": "Украшения из лунного камня и перламутра ручной работы",
        "title_cluster": "украшения из лунного камня и перламутра",
        "breadcrumb": "Лунный камень и перламутр",
        "eyebrow": "Шелковое сияние • Перламутр и адуляр",
        "lead": "Утонченные авторские колье, чокеры и гарнитуры с переливчатым натуральным перламутром, речным жемчугом и полупрозрачными минералами.",
        "filter_type": "stone",
        "filter_val": ["лунн", "перламутр", "майорка"],
        "stone_name_gen": "лунного камня, перламутра и жемчуга",
        "stone_name_prep": "украшениях из лунного камня и перламутра",
        "seo_title": "Украшения с перламутром и лунным сиянием от мастерской Livi Jewelry",
        "seo_p1": "Украшения с натуральным перламутром, лунным камнем и органическим жемчугом славятся мягким иризирующим свечением — эффектом внутреннего голубовато-жемчужного перелива. Такие изделия универсальны: они не перегружают дневной образ и одновременно выглядят благородно и статусно в вечернем освещении.",
        "seo_p2": "В мастерской Livi Jewelry каждое колье и гарнитур собираются вручную с вниманием к малейшим нюансам оттенка и формы бусин. Вы можете выбрать желаемую длину украшения и покрытие фурнитуры (серебристый родий или теплая позолота), а мы позаботимся о фирменной подарочной упаковке и быстрой доставке СДЭК по всему Казахстану."
    }
]

EXISTING_HUBS = [
    ("kolye-iz-zhemchuga.html", "Колье из жемчуга"),
    ("braslety-iz-zhemchuga.html", "Браслеты из жемчуга"),
    ("sergi-iz-zhemchuga.html", "Серьги из жемчуга"),
]


def clean_attr(text):
    if not text:
        return ""
    return str(text).replace("&", "&amp;").replace('"', "&quot;").replace("\n", " ").strip()


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
    if len(matched) < 3:
        # Дополняем подборку 3–4 комплементарными изделиями из барочного/натурального жемчуга
        matched_ids = {p["id"] for p in matched}
        baroque_candidates = [
            p for p in active
            if p["id"] not in matched_ids
            and (
                "барочн" in (" ".join(p.get("materials", [])) + " " + p.get("title", "")).lower()
                or "жемчуг" in (" ".join(p.get("materials", [])) + " " + p.get("title", "")).lower()
            )
        ]
        for comp in baroque_candidates[:4]:
            matched.append(comp)
            recommended_ids.add(comp["id"])

    return matched, recommended_ids


def build_interlink_block_html(current_slug="", prefix=""):
    chips = []
    for slug, label in EXISTING_HUBS:
        active_cls = " active" if slug == current_slug else ""
        chips.append(f'      <a class="chip-link{active_cls}" href="{prefix}/{slug}">{label}</a>')
    for h in ALL_HUBS:
        slug = h["slug"]
        label = h["chip_label"]
        active_cls = " active" if slug == current_slug else ""
        chips.append(f'      <a class="chip-link{active_cls}" href="{prefix}/{slug}">{label}</a>')
    chips_str = "\n".join(chips)
    return f"""    <!-- Навигационный блок: Подборки по камням и стилям -->
    <section class="hub-interlink-section" aria-label="Подборки по камням и стилям">
      <h2 class="hub-interlink-title">Подборки украшений по натуральным камням и стилям</h2>
      <nav class="stone-chips" style="margin-bottom:0;">
{chips_str}
      </nav>
    </section>"""


def generate_hub_page(hub, products):
    slug = hub["slug"]
    canonical_url = f"{BASE_URL}/{slug}"
    matched_products, recommended_ids = match_products_for_hub(hub, products)

    prices = [int(p.get("price", 0)) for p in matched_products if int(p.get("price", 0)) > 0]
    min_price = min(prices) if prices else 25000
    max_price = max(prices) if prices else 91000
    min_fmt = f"{min_price:,}".replace(",", " ")
    max_fmt = f"{max_price:,}".replace(",", " ")

    page_title = f"Купить {hub['title_cluster']} ручной работы в Астане, Алматы и Казахстане — цена в тенге | Livi Jewelry"
    meta_desc = (
        f"Купить {hub['title_cluster']} ручной работы в Livi Jewelry. "
        f"Цены от {min_fmt} до {max_fmt} ₸. 100% натуральные камни и жемчуг, "
        f"бесплатная индивидуальная подгонка размера, подарочная упаковка и быстрая доставка СДЭК по Казахстану."
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
        pdesc = p.get("description") or ptitle
        pprice = int(p.get("price", 0))
        pprice_fmt = f"{pprice:,}".replace(",", " ")
        pprice_dec = f"{pprice:.2f}"
        pimg_rel = p["image"].lstrip("/")
        pimg_abs = f"{BASE_URL}/{pimg_rel}"
        p_instock = p.get("inStock", True) and not p.get("archived", False)
        p_url = f"{BASE_URL}/product/{pid}.html"
        pmats = ", ".join(p.get("materials", []))

        item_list_elements.append({
            "@type": "Product",
            "position": idx,
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
                    "priceRange": "15000 KZT - 85000 KZT",
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": "Астана",
                        "addressCountry": "KZ"
                    }
                }
            }
        })

        rec_badge = ""
        if pid in recommended_ids:
            rec_badge = '<div style="font-size:10px;text-transform:uppercase;letter-spacing:0.12em;color:var(--gold);margin-bottom:4px;">Рекомендуемые изделия из коллекции</div>'

        alt_str = clean_attr(f"{ptitle} — ручная работа Livi Jewelry ({pprice_fmt} ₸)")
        cards_html.append(f"""        <article class="card" data-id="{pid}" data-name="{clean_attr(ptitle)}" data-price="{pprice}" data-category="{clean_attr(p.get('category', 'Necklaces'))}" onclick="if(!event.target.closest('a'))location.href='/product/{pid}.html'">
          <div class="card-img-wrap">
            <img src="{pimg_rel}" alt="{alt_str}" loading="lazy" decoding="async" width="600" height="800">
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

    # 3. FAQPage Schema (3 commercial questions specific to this stone/category)
    q1 = f"Как проверяется подлинность {hub['stone_name_gen']} в украшениях Livi Jewelry?"
    a1 = f"В ателье Livi Jewelry мы используем исключительно натуральные минералы и отборный культивированный жемчуг. Каждая партия {hub['stone_name_gen']} проходит ручную проверку мастером на природную плотность, характерную прохладу камня, естественные включения и глубину оттенка."
    q2 = f"Можно ли бесплатно изменить длину или размер в {hub['stone_name_prep']}?"
    a2 = "Да, перед отправкой мастер бесплатно адаптирует длину колье, чокера или обхват браслета точно под ваши индивидуальные мерки, а также добавит удобную удлинительную цепочку 5 см и установит родированную или позолоченную гипоаллергенную фурнитуру на ваш выбор."
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

    interlink_html = build_interlink_block_html(current_slug=slug, prefix="")
    cards_grid_str = "\n".join(cards_html)

    html = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />

  <title>{clean_attr(page_title)}</title>
  <meta name="description" content="{clean_attr(meta_desc)}">
  <link rel="canonical" href="{canonical_url}">
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
  <link rel="stylesheet" href="styles.css">

  <!-- Icons & Manifest -->
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#141312">
  <meta name="msapplication-TileColor" content="#141312">

  <!-- Google tag (GA4 + Ads) with Google Consent Mode v2 -->
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

  <!-- Meta Pixel Code (Dual Pixel: Primary 199604456030882 + Secondary 4185620171718327) -->
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
      content_category: {json.dumps(hub['breadcrumb'], ensure_ascii=False)},
      content_name: {json.dumps(hub['h1'], ensure_ascii=False)}
    }});
  </script>
  <noscript><img height="1" width="1" style="display:none"
    src="https://www.facebook.com/tr?id=199604456030882&ev=PageView&noscript=1"
  /></noscript>

  <!-- Structured Data: BreadcrumbList -->
  <script type="application/ld+json">
{json.dumps(schema_breadcrumbs, ensure_ascii=False, indent=2)}
  </script>

  <!-- Structured Data: ItemList -->
  <script type="application/ld+json">
{json.dumps(schema_itemlist, ensure_ascii=False, indent=2)}
  </script>

  <!-- Structured Data: FAQPage -->
  <script type="application/ld+json">
{json.dumps(schema_faq, ensure_ascii=False, indent=2)}
  </script>

  <style>
    .landing-hero {{
      text-align: center;
      padding: 48px 20px 32px;
      max-width: 920px;
      margin: 0 auto;
    }}
    .landing-eyebrow {{
      font-size: 11px;
      letter-spacing: 0.24em;
      text-transform: uppercase;
      color: var(--gold);
      font-weight: 500;
      display: inline-block;
      margin-bottom: 12px;
    }}
    .landing-title {{
      font-family: var(--font-serif);
      font-size: clamp(32px, 4.8vw, 52px);
      font-weight: 300;
      line-height: 1.15;
      letter-spacing: 0.02em;
      color: var(--fg);
      margin-bottom: 18px;
    }}
    .landing-lead {{
      font-size: 15px;
      line-height: 1.8;
      color: var(--fg-soft);
      font-weight: 300;
      max-width: 740px;
      margin: 0 auto 28px;
    }}
    .landing-cta-row {{
      display: flex;
      gap: 14px;
      justify-content: center;
      flex-wrap: wrap;
      margin-bottom: 32px;
    }}
    .editorial-content {{
      max-width: 880px;
      margin: 56px auto;
      padding: 40px 32px;
      background: #FFFFFF;
      border: 1px solid var(--line);
    }}
    .editorial-content h2 {{
      font-family: var(--font-serif);
      font-size: clamp(24px, 3.2vw, 32px);
      font-weight: 400;
      color: var(--fg);
      margin: 0 0 16px;
      letter-spacing: 0.02em;
    }}
    .editorial-content p {{
      color: var(--fg-soft);
      font-size: 14.5px;
      line-height: 1.8;
      margin-bottom: 16px;
      font-weight: 300;
    }}
  </style>
</head>
<body>
  <!-- Drawer -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back"></div>
    <div class="drawer-panel" role="menu" aria-label="Меню">
      <a href="/">Главная</a>
      <a href="shop.html">Каталог</a>
      <a href="kolye-iz-zhemchuga.html">Колье из жемчуга</a>
      <a href="braslety-iz-zhemchuga.html">Браслеты из жемчуга</a>
      <a href="sergi-iz-zhemchuga.html">Серьги из жемчуга</a>
      <a href="komplekty-ukrasheniy.html">Комплекты украшений</a>
      <a href="delivery.html">Доставка и оплата</a>
      <a href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
      <a href="https://wa.me/77054510584?text=Здравствуйте!%20Хочу%20получить%20консультацию%20по%20украшениям%20Livi%20Jewelry." target="_blank" rel="noopener">WhatsApp Мастера</a>
      <div class="lang">
        <a href="/" id="ruBtn" class="active" style="text-align:center;font-family:var(--font-sans);font-size:12px;">RU</a>
        <a href="/kz/" id="kkBtn" style="text-align:center;font-family:var(--font-sans);font-size:12px;">KZ</a>
      </div>
    </div>
  </div>

  <!-- Header -->
  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Меню"><span></span></button>
      <a class="brand" href="/" aria-label="Livi Jewelry">
        <span>LIVI JEWELRY</span>
      </a>
      <div class="nav-actions">
        <div class="header-lang-links">
          <a href="/" class="active">RU</a>
          <a href="/kz/">KZ</a>
        </div>
        <a class="cart-link" href="shop.html">Каталог</a>
        <a class="cart-link" href="cart.html">Корзина <span id="cartBadge" class="cart-badge" style="display:none"></span></a>
      </div>
    </div>
  </header>

  <main>
    <!-- Breadcrumbs -->
    <div class="wrap" style="padding-bottom: 0; padding-top: 24px;">
      <nav class="breadcrumbs" aria-label="Навигационная цепочка" style="margin-bottom:0;">
        <a href="/">Главная</a>
        <span class="sep">/</span>
        <a href="shop.html">Каталог</a>
        <span class="sep">/</span>
        <span class="current" aria-current="page">{hub['breadcrumb']}</span>
      </nav>
    </div>

    <!-- Hero Editorial Header -->
    <section class="landing-hero">
      <span class="landing-eyebrow">{hub['eyebrow']}</span>
      <h1 class="landing-title">{hub['h1']}</h1>
      <p class="landing-lead">{hub['lead']}</p>
      <div class="landing-cta-row">
        <a class="btn" href="shop.html">Смотреть весь каталог</a>
        <a class="btn btn-secondary" href="https://wa.me/77054510584?text=Здравствуйте!%20Помогите%20подобрать%20украшение%20({urllib.parse.quote(hub['breadcrumb'])})." target="_blank" rel="noopener">Консультация мастера в WhatsApp</a>
      </div>
    </section>

    <!-- Product Showcase Grid -->
    <section class="wrap" style="padding-top: 0;">
      <h2 style="font-family: var(--font-serif); font-size: clamp(24px, 3.5vw, 36px); font-weight: 300; text-align: center; margin-bottom: 8px;">Изделия в наличии и под индивидуальный заказ ({min_fmt} — {max_fmt} ₸)</h2>
      <div class="rule"></div>

      <div class="grid" id="hubGrid">
{cards_grid_str}
      </div>
    </section>

    <!-- Expert Commercial SEO Block (150-250 words) -->
    <article class="editorial-content">
      <h2>{hub['seo_title']}</h2>
      <p>{hub['seo_p1']}</p>
      <p>{hub['seo_p2']}</p>
    </article>

    <!-- FAQ Section -->
    <section class="faq-section">
      <h2>Частые вопросы о коллекции «{hub['breadcrumb']}»</h2>
      <div class="rule"></div>
      <div class="faq-list">
        <details class="faq-item" open>
          <summary>{q1}</summary>
          <div class="faq-answer">{a1}</div>
        </details>
        <details class="faq-item">
          <summary>{q2}</summary>
          <div class="faq-answer">{a2}</div>
        </details>
        <details class="faq-item">
          <summary>{q3}</summary>
          <div class="faq-answer">{a3}</div>
        </details>
      </div>
    </section>

{interlink_html}
  </main>

  <!-- Footer -->
  <footer id="contact">
    <div class="foot">
      <div class="links">
        <a href="delivery.html">Доставка, оплата и возврат</a>
        <a href="privacy.html">Политика конфиденциальности</a>
        <a href="terms.html">Условия использования (Оферта)</a>
        <a href="shop.html">Каталог</a>
        <a href="kolye-iz-zhemchuga.html">Колье</a>
        <a href="braslety-iz-zhemchuga.html">Браслеты</a>
        <a href="sergi-iz-zhemchuga.html">Серьги</a>
        <a href="komplekty-ukrasheniy.html">Комплекты</a>
      </div>
      <div class="copy">© <span id="year">2026</span> Livi Jewelry — Авторские украшения ручной работы из натурального жемчуга и камней. Все права защищены.</div>
      <div class="links">
        <a class="tag" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram @livi_jwl</a>
        <a class="tag" href="https://wa.me/77054510584" target="_blank" rel="noopener">WhatsApp +7 (705) 451-05-84</a>
      </div>
    </div>
  </footer>

  <!-- Floating WhatsApp Widget -->
  <a class="floating-wa" href="https://wa.me/77054510584?text=Здравствуйте!%20Хочу%20получить%20консультацию%20по%20украшениям%20Livi%20Jewelry." target="_blank" rel="noopener" aria-label="Консультация мастера в WhatsApp">
    <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
      <path fill="currentColor" d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
      <path fill="currentColor" d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
    </svg>
    <span class="floating-wa-text">Консультация мастера</span>
  </a>

  <script>
    // Attribution Tracker (livi_attribution)
    (function() {{
      try {{
        const params = new URLSearchParams(window.location.search);
        const keys = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
        let existing = {{}};
        try {{ existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}') || {{}}; }} catch(e){{}}
        let updated = false;
        keys.forEach(k => {{
          const v = params.get(k);
          if (v) {{ existing[k] = v; updated = true; }}
        }});
        if (!existing.landing_page) {{
          existing.landing_page = window.location.pathname + window.location.search;
          existing.referrer = document.referrer || 'direct';
          existing.first_visit = new Date().toISOString();
          updated = true;
        }}
        if (updated) {{
          localStorage.setItem('livi_attribution', JSON.stringify(existing));
        }}
      }} catch(e) {{}}
    }})();

    const drawer = document.getElementById('drawer');
    const burger = document.getElementById('burger');
    if (burger && drawer) {{
      burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false'); }};
      drawer.querySelector('.drawer-back').onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden', 'true'); }};
    }}
    document.getElementById('year').textContent = new Date().getFullYear();

    function updateBadge() {{
      try {{
        const raw3 = localStorage.getItem('livi_cart_v3');
        const items = raw3 ? JSON.parse(raw3) : [];
        const count = (Array.isArray(items) ? items : []).reduce((s, i) => s + (parseInt(i.qty, 10) || 0), 0);
        const b = document.getElementById('cartBadge');
        if (b) {{
          b.textContent = count > 0 ? String(count) : '';
          b.style.display = count > 0 ? 'inline-block' : 'none';
        }}
      }} catch (e) {{}}
    }}
    updateBadge();

    // GA4 view_item_list & select_item
    const HUB_ITEMS = {json.dumps(ga4_items, ensure_ascii=False)};
    if (typeof gtag === 'function') {{
      gtag('event', 'view_item_list', {{
        item_list_id: {json.dumps(slug.replace('.html', ''))},
        item_list_name: {json.dumps(hub['h1'], ensure_ascii=False)},
        items: HUB_ITEMS
      }});
    }}

    document.querySelectorAll('#hubGrid .card').forEach((card, idx) => {{
      card.addEventListener('click', function() {{
        try {{
          if (typeof gtag === 'function') {{
            const itemObj = HUB_ITEMS[idx] || {{
              item_id: card.getAttribute('data-id'),
              item_name: card.getAttribute('data-name'),
              price: Number(card.getAttribute('data-price')) || 0,
              item_category: card.getAttribute('data-category') || 'Necklaces'
            }};
            gtag('event', 'select_item', {{
              item_list_id: {json.dumps(slug.replace('.html', ''))},
              item_list_name: {json.dumps(hub['h1'], ensure_ascii=False)},
              items: [itemObj]
            }});
          }}
        }} catch(e) {{}}
      }});
    }});

    // Contact Conversion Tracking (WhatsApp & Instagram)
    document.addEventListener('click', function(e) {{
      const a = e.target.closest('a[href]');
      if (!a) return;
      const href = a.getAttribute('href') || '';
      const isWa = href.includes('wa.me') || href.includes('whatsapp.com');
      const isIg = href.includes('instagram.com');
      if (!isWa && !isIg) return;

      const method = isWa ? 'WhatsApp' : 'Instagram';
      const val = 45000;
      try {{
        if (typeof gtag === 'function') {{
          gtag('event', 'generate_lead', {{
            currency: 'KZT',
            value: val,
            method: method,
            page_location: window.location.href,
            item_id: ''
          }});
          gtag('event', 'contact', {{
            currency: 'KZT',
            value: val,
            method: method,
            page_location: window.location.href,
            item_id: ''
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
        if (typeof fbq === 'function') fbq('track', 'Contact');
      }} catch(err) {{}}
    }});
  </script>
</body>
</html>
"""
    with open(slug, "w", encoding="utf-8") as f:
        f.write(html)
    return slug


def update_existing_pages_interlinking():
    """Updates kolye-iz-zhemchuga.html, braslety-iz-zhemchuga.html, sergi-iz-zhemchuga.html, shop.html, and index.html with SEO hub links."""
    for cat_page, _ in EXISTING_HUBS:
        if not os.path.exists(cat_page):
            continue
        with open(cat_page, "r", encoding="utf-8") as f:
            html = f.read()

        interlink_block = build_interlink_block_html(current_slug=cat_page, prefix="")
        if 'class="hub-interlink-section"' in html:
            html = re.sub(
                r'<!-- Навигационный блок: Подборки по камням и стилям -->\s*<section class="hub-interlink-section".*?</section>',
                interlink_block,
                html,
                flags=re.DOTALL,
            )
        else:
            html = html.replace("</main>", f"\n{interlink_block}\n  </main>")

        # Ensure select_item and livi_attribution are present in existing category pages
        if "livi_attribution" not in html:
            attr_And_Select_Script = """
    // Attribution Tracker & select_item
    (function() {
      try {
        const params = new URLSearchParams(window.location.search);
        const keys = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
        let existing = {};
        try { existing = JSON.parse(localStorage.getItem('livi_attribution') || '{}') || {}; } catch(e){}
        let updated = false;
        keys.forEach(k => { const v = params.get(k); if (v) { existing[k] = v; updated = true; } });
        if (!existing.landing_page) {
          existing.landing_page = window.location.pathname + window.location.search;
          existing.referrer = document.referrer || 'direct';
          updated = true;
        }
        if (updated) localStorage.setItem('livi_attribution', JSON.stringify(existing));
      } catch(e){}
    })();
    document.querySelectorAll('.grid .card').forEach((card, idx) => {
      card.addEventListener('click', function() {
        if (typeof gtag === 'function') {
          const titleEl = card.querySelector('.card-title-link');
          const href = titleEl ? titleEl.getAttribute('href') || '' : '';
          const m = href.match(/(prod_\\d+)/);
          gtag('event', 'select_item', {
            item_list_id: 'category_hub',
            item_list_name: document.title,
            items: [{ item_id: m ? m[1] : 'prod_01', item_name: titleEl ? titleEl.textContent.trim() : '', index: idx + 1 }]
          });
        }
      });
    });
"""
            html = html.replace("// Contact Conversion Tracking", attr_And_Select_Script + "\n    // Contact Conversion Tracking")

        with open(cat_page, "w", encoding="utf-8") as f:
            f.write(html)


def generate_seo_hubs():
    if not os.path.exists(PRODUCTS_FILE):
        print(f"Error: {PRODUCTS_FILE} not found!")
        return []

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    generated = []
    for hub in ALL_HUBS:
        out = generate_hub_page(hub, products)
        generated.append(out)

    update_existing_pages_interlinking()
    print(f"[OK] Generated {len(generated)} SEO hub landing pages and updated category interlinking.")
    return generated


if __name__ == "__main__":
    import urllib.parse
    generate_seo_hubs()
else:
    import urllib.parse
