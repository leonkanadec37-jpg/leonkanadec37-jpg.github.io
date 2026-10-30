#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import json
import os
import pathlib

DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"
REPORTS_DIR = pathlib.Path(__file__).resolve().parent.parent.parent / "reports" / "GOOGLE ADS ОТЧЕТЫ"
path = REPORTS_DIR / '25.10.26' / 'Отчет о поисковых запросах (2).csv'
if not path.exists():
    path = pathlib.Path('Отчет о поисковых запросах (2).csv')

with open(path, 'r', encoding='utf-16', errors='replace') as f:
    reader = csv.reader(f, delimiter='\t')
    rows = list(reader)

print(f"Total rows in CSV: {len(rows)}")
headers = rows[2]
data = rows[3:]

terms = []
for r in data:
    if len(r) < 11:
        continue
    term = r[0].strip()
    if term.startswith('Итого') or term.startswith('Total') or not term:
        continue
    try:
        clicks = int(r[5].replace('\xa0', '').replace(' ', '').replace(',', '') or 0)
    except:
        clicks = 0
    try:
        impr = int(r[6].replace('\xa0', '').replace(' ', '').replace(',', '') or 0)
    except:
        impr = 0
    cost_str = r[10].replace(',', '.').replace('\xa0', '').replace(' ', '').replace('$', '').strip()
    try:
        cost = float(cost_str or 0)
    except:
        cost = 0.0
    status = r[2].strip()
    campaign = r[3].strip()
    adgroup = r[4].strip()
    match_type = r[1].strip()

    terms.append({
        'term': term,
        'clicks': clicks,
        'impr': impr,
        'cost': cost,
        'status': status,
        'campaign': campaign,
        'adgroup': adgroup,
        'match_type': match_type
    })

print(f"Extracted valid search terms: {len(terms)}")
with_clicks = [t for t in terms if t['clicks'] > 0]
total_clicks = sum(t['clicks'] for t in terms)
total_spend = sum(t['cost'] for t in terms)
print(f"Terms with clicks: {len(with_clicks)}, Total clicks: {total_clicks}, Total spend: ${total_spend:.2f}")

with open(DATA_DIR / 'big_report_terms.json', 'w', encoding='utf-8') as out:
    json.dump(terms, out, ensure_ascii=False, indent=2)

print(f"Saved clean data to {DATA_DIR / 'big_report_terms.json'}")
