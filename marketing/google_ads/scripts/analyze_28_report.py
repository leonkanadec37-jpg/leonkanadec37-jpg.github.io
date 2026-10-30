#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import os
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

REPORT_FILE = pathlib.Path('marketing/reports/GOOGLE ADS ОТЧЕТЫ/28.10.26/Поисковые_запросы(Поиск_2026.10.28).csv')

with open(REPORT_FILE, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    headers = next(reader)
    rows = list(reader)

COMPETITORS = [
    r'pandora', r'пандор', r'avgust', r'larouche', r'ларош', r'lyarush', r'северная чернь', 
    r'магазин бижутерии', r'магазин украшений', r'ювелирный магазин.*каталог'
]

FOREIGN_GEO = [
    r'мальдив', r'вьетнам', r'турецк'
]

ASTRO_INFO = [
    r'по дате рождения', r'зодиака', r'для льва', r'у скорпиона', r'для дева', 
    r'какой камень подходит', r'какой камень', r'от чего помогают', r'к белому платью',
    r'в тренде у молодежи', r'самый дорогой камень', r'вещи из'
]

IRRELEVANT_MATERIALS = [
    r'янтар', r'янтарь', r'изумруд', r'шерст', r'мельхиор', r'казачьи'
]

VINTAGE = [
    r'винтаж', r'80 х годов', r'старинный'
]

categories = {
    'ЦЕЛЕВЫЕ (КЛИКИ ИЛИ ВЫСОКИЙ ПОТЕНЦИАЛ)': [],
    'КОНКУРЕНТЫ И ЧУЖИЕ МАГАЗИНЫ': [],
    'ЧУЖАЯ ГЕОГРАФИЯ И КУРОРТЫ': [],
    'АСТРОЛОГИЯ И ИНФО-МУСОР': [],
    'ЧУЖИЕ МАТЕРИАЛЫ (ВНЕ КАТАЛОГА LIVI)': [],
    'ВИНТАЖ И РЕТРО': [],
    'ОБЩИЕ / СМЕЖНЫЕ': []
}

total_impr = 0
total_clicks = 0
total_cost = 0.0

for r in rows:
    query = r[0].strip()
    cost_str = r[1].replace('\xa0', '').replace('$', '').replace(',', '.').strip()
    cost = float(cost_str or 0)
    clicks = int(r[2].replace('\xa0', '').strip())
    impr = int(r[3].replace('\xa0', '').strip())
    conv = float(r[4].replace('\xa0', '').replace(',', '.').strip())
    
    total_impr += impr
    total_clicks += clicks
    total_cost += cost

    q_low = query.lower()
    
    item = {
        'query': query,
        'impr': impr,
        'clicks': clicks,
        'cost': cost,
        'conv': conv
    }

    if any(re.search(p, q_low) for p in COMPETITORS):
        categories['КОНКУРЕНТЫ И ЧУЖИЕ МАГАЗИНЫ'].append(item)
    elif any(re.search(p, q_low) for p in FOREIGN_GEO):
        categories['ЧУЖАЯ ГЕОГРАФИЯ И КУРОРТЫ'].append(item)
    elif any(re.search(p, q_low) for p in ASTRO_INFO):
        categories['АСТРОЛОГИЯ И ИНФО-МУСОР'].append(item)
    elif any(re.search(p, q_low) for p in IRRELEVANT_MATERIALS):
        categories['ЧУЖИЕ МАТЕРИАЛЫ (ВНЕ КАТАЛОГА LIVI)'].append(item)
    elif any(re.search(p, q_low) for p in VINTAGE):
        categories['ВИНТАЖ И РЕТРО'].append(item)
    elif clicks > 0 or any(k in q_low for k in ['жемчуг', 'чокер', 'колье', 'сотуар', 'серьги', 'браслет', 'бусы', 'комплект', 'аметист', 'гранат', 'гематит', 'бирюз', 'кварц', 'малахит']):
        categories['ЦЕЛЕВЫЕ (КЛИКИ ИЛИ ВЫСОКИЙ ПОТЕНЦИАЛ)'].append(item)
    else:
        categories['ОБЩИЕ / СМЕЖНЫЕ'].append(item)

print(f"=== ИТОГИ АНАЛИЗА 100 ЗАПРОСОВ (28.10.2026) ===")
print(f"Всего показов: {total_impr}, Кликов: {total_clicks}, Расход: ${total_cost:.2f}\n")

for cat_name, items in categories.items():
    cat_impr = sum(x['impr'] for x in items)
    cat_clicks = sum(x['clicks'] for x in items)
    cat_cost = sum(x['cost'] for x in items)
    pct_impr = (cat_impr / total_impr * 100) if total_impr else 0
    print(f"■ {cat_name} ({len(items)} шт, {cat_impr} пок [{pct_impr:.1f}%], {cat_clicks} кл, ${cat_cost:.2f}):")
    for it in sorted(items, key=lambda x: (x['clicks'], x['impr']), reverse=True):
        print(f"    - [{it['impr']:2d} пок, {it['clicks']} кл, ${it['cost']:.2f}] \"{it['query']}\"")
    print()
