#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Единый оркестратор сборки и проверки сайта Livi Jewelry (livijewelry.kz):
Последовательно запускает все генераторы кодовой базы и тестовый сьют:
  1) generate_product_pages.py (RU страницы товаров + пререндеринг витрин)
  2) generate_seo_hubs.py (21 кластерный SEO-хаб на RU, KZ, UZ)
  3) generate_kz_pages.py (витрина KZ + казахские страницы товаров)
  4) generate_uz_pages.py (витрина UZ + узбекские страницы товаров)
  5) generate_feed.py (Google Merchant Center feed.xml)
  6) generate_kaspi_feed.py (товарный фид и каталог Kaspi.kz)
  7) generate_2gis_catalog.py (товарный фид и каталог 2ГИС)
  8) generate_pinterest_assets.py (каталог и пины Pinterest)
  9) generate_sitemap.py (XML карта сайта sitemap.xml)
  10) verify_audit.py (автотесты всех 45 SEO/технических инвариантов)

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
    ("generate_product_pages.py", "1/10 Генерация RU страниц товаров и пререндеринг витрин"),
    ("generate_seo_hubs.py", "2/10 Генерация 21 кластерного SEO-хаба (RU, KZ, UZ)"),
    ("generate_kz_pages.py", "3/10 Генерация казахской витрины и KZ страниц товаров"),
    ("generate_uz_pages.py", "4/10 Генерация узбекской витрины и UZ страниц товаров"),
    ("generate_feed.py", "5/10 Генерация товарного фида Google Shopping"),
    ("generate_kaspi_feed.py", "6/10 Генерация товарного фида и каталога Kaspi.kz"),
    ("generate_2gis_catalog.py", "7/10 Генерация товарного фида и каталога 2ГИС"),
    ("generate_pinterest_assets.py", "8/10 Генерация каталога и пинов Pinterest"),
    ("generate_sitemap.py", "9/10 Генерация карты сайта sitemap.xml"),
    ("verify_audit.py", "10/10 Запуск валидации технического аудита и 45 тестов инвариантов"),
]


def run_step(script_name: str, desc: str):
    print(f"\n========================================================")
    print(f">> [{desc}]")
    print(f"   Выполняется: python {script_name}...")
    print(f"========================================================")

    start_time = time.time()
    cmd = [sys.executable, script_name]
    res = subprocess.run(cmd)
    time.sleep(0.15)
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
