#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Единый оркестратор сборки и проверки сайта Livi Jewelry (livijewelry.kz):
Последовательно запускает все генераторы кодовой базы и тестовый сьют:
  1) generate_product_pages.py (28 RU страниц товаров + пререндеринг витрин)
  2) generate_seo_hubs.py (21 кластерный SEO-хаб)
  3) generate_kz_pages.py (витрина KZ + 28 казахских страниц товаров)
  4) generate_feed.py (Google Merchant Center feed.xml)
  5) generate_sitemap.py (XML карта сайта sitemap.xml)
  6) build_campaign_assets.py (Google Ads кампании, ключевые слова и минус-слова)
  7) verify_audit.py (автотесты всех 35 SEO/технических инвариантов)

При любой ошибке процесс немедленно прерывается с кодом выхода != 0.
"""

import sys
import subprocess
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STEPS = [
    ("generate_product_pages.py", "1/7 Генерация 28 RU страниц товаров и пререндеринг витрин"),
    ("generate_seo_hubs.py", "2/7 Генерация 21 кластерного SEO-хаба"),
    ("generate_kz_pages.py", "3/7 Генерация казахской витрины и 28 KZ страниц товаров"),
    ("generate_feed.py", "4/7 Генерация товарного фида Google Shopping"),
    ("generate_sitemap.py", "5/7 Генерация карты сайта sitemap.xml"),
    ("build_campaign_assets.py", "6/7 Генерация рекламных кампаний и ассетов Google Ads"),
    ("verify_audit.py", "7/7 Запуск валидации технического аудита и 35 тестов инвариантов"),
]


def run_step(script_name: str, desc: str):
    print(f"\n========================================================")
    print(f">> [{desc}]")
    print(f"   Выполняется: python {script_name}...")
    print(f"========================================================")

    start_time = time.time()
    cmd = [sys.executable, script_name]
    res = subprocess.run(cmd)
    elapsed = time.time() - start_time

    if res.returncode != 0:
        print(f"\n[FAIL] Шаг {script_name} завершился с ошибкой (код {res.returncode}) за {elapsed:.2f}с")
        sys.exit(res.returncode)

    print(f"[OK] Шаг {script_name} успешно выполнен за {elapsed:.2f}с")


def main():
    print("========================================================")
    print("НАЧАЛО ПОЛНОЙ СБОРКИ И ВЕРИФИКАЦИИ LIVI JEWELRY")
    print("========================================================")

    total_start = time.time()
    for script, desc in STEPS:
        run_step(script, desc)

    total_elapsed = time.time() - total_start
    print("\n========================================================")
    print(f"ВСЕ ЭТАПЫ СБОРКИ И ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ ({total_elapsed:.2f}с)!")
    print("========================================================\n")


if __name__ == "__main__":
    main()
