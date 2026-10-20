#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматическая проверка статуса индексации всех 126 страниц Livi Jewelry через Google Search Console URL Inspection API.

Требования:
1. pip install google-api-python-client google-auth
2. Создать сервисный аккаунт в Google Cloud Console и скачать ключ credentials.json в корень проекта.
3. В Google Search Console (Настройки -> Пользователи и разрешения) добавить email сервисного аккаунта с правами «Полный доступ» (или Владелец).

Использование:
    python check_gsc_indexing.py [--credentials path/to/credentials.json] [--site https://livijewelry.kz/]
"""

import argparse
import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SITEMAP_FILE = "sitemap.xml"
DEFAULT_SITE_URL = "https://livijewelry.kz/"
DEFAULT_CREDS_FILE = "credentials.json"
REPORT_OUTPUT_FILE = "gsc_indexing_report.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def get_sitemap_urls(sitemap_path: str) -> list:
    if not os.path.exists(sitemap_path):
        print(f"[FAIL] Файл {sitemap_path} не найден.")
        return []
    tree = ET.parse(sitemap_path)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text.strip() for loc in tree.getroot().findall("sm:url/sm:loc", ns)]


def inspect_url(service, inspection_url: str, site_url: str):
    try:
        request = service.urlInspection().index().inspect(
            body={
                "inspectionUrl": inspection_url,
                "siteUrl": site_url,
                "languageCode": "ru-KZ"
            }
        )
        return request.execute()
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="GSC Indexing Auditor for Livi Jewelry")
    parser.add_argument("--credentials", default=DEFAULT_CREDS_FILE, help="Путь к service account credentials.json")
    parser.add_argument("--site", default=DEFAULT_SITE_URL, help="URL ресурса в GSC (например, https://livijewelry.kz/ или sc-domain:livijewelry.kz)")
    parser.add_argument("--limit", type=int, default=0, help="Ограничить количество проверяемых URL для теста (0 = все 126)")
    args = parser.parse_args()

    urls = get_sitemap_urls(SITEMAP_FILE)
    print(f"Загружено {len(urls)} URL из {SITEMAP_FILE}")

    if not os.path.exists(args.credentials):
        print("\n" + "=" * 70)
        print(f"[ИНФОРМАЦИЯ] Файл сервисного аккаунта '{args.credentials}' пока не найден.")
        print("Для запуска прямого автоматического аудита индексации:")
        print("1. Перейдите в Google Cloud Console -> Создайте Service Account")
        print("2. Включите Google Search Console API")
        print("3. Создайте JSON-ключ и сохраните его в корень как credentials.json")
        print("4. В Google Search Console добавьте email сервисного аккаунта в Настройки -> Пользователи")
        print("5. Запустите этот скрипт снова: python check_gsc_indexing.py")
        print("=" * 70 + "\n")
        return

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds = service_account.Credentials.from_service_account_file(
            args.credentials, scopes=SCOPES
        )
        service = build("searchconsole", "v1", credentials=creds)
    except Exception as e:
        print(f"[FAIL] Ошибка инициализации клиента Google Search Console: {e}")
        return

    check_list = urls[:args.limit] if args.limit > 0 else urls
    print(f"Начинаю опрос Google Search Console URL Inspection API для {len(check_list)} URL...")

    results = []
    stats = {
        "INDEXED": 0,
        "CRAWLED_NOT_INDEXED": 0,
        "DISCOVERED_NOT_INDEXED": 0,
        "NOT_INDEXED_OTHER": 0,
        "ERRORS": 0
    }

    for i, u in enumerate(check_list, 1):
        print(f"[{i}/{len(check_list)}] Проверка: {u} ...", end=" ", flush=True)
        resp = inspect_url(service, u, args.site)
        
        if "error" in resp:
            print(f"ОШИБКА: {resp['error']}")
            stats["ERRORS"] += 1
            results.append({"url": u, "status": "ERROR", "details": resp["error"]})
        else:
            inspection_result = resp.get("inspectionResult", {})
            index_status = inspection_result.get("indexStatusResult", {})
            verdict = index_status.get("verdict", "NEUTRAL")
            coverage = index_status.get("coverageState", "UNKNOWN")
            last_crawl = index_status.get("lastCrawlTime", "never")
            robot_state = index_status.get("robotsTxtState", "UNKNOWN")
            indexing_state = index_status.get("indexingState", "UNKNOWN")

            if verdict == "PASS":
                stats["INDEXED"] += 1
                short_status = "INDEXED"
            elif "Crawled" in coverage:
                stats["CRAWLED_NOT_INDEXED"] += 1
                short_status = "CRAWLED_NOT_INDEXED"
            elif "Discovered" in coverage:
                stats["DISCOVERED_NOT_INDEXED"] += 1
                short_status = "DISCOVERED_NOT_INDEXED"
            else:
                stats["NOT_INDEXED_OTHER"] += 1
                short_status = coverage

            print(f"{verdict} ({coverage}, послед обход: {last_crawl})")
            results.append({
                "url": u,
                "status": short_status,
                "coverage": coverage,
                "verdict": verdict,
                "last_crawl": last_crawl,
                "robots_txt": robot_state,
                "indexing_state": indexing_state,
                "rich_results": inspection_result.get("richResultsResult", {})
            })

        # Пауза для соблюдения лимитов API (квота GSC API: 2 000 запросов/день, 600 запросов/мин)
        time.sleep(0.15)

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_checked": len(check_list),
        "stats": stats,
        "urls": results
    }

    with open(REPORT_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 50)
    print("ИТОГ АУДИТА ИНДЕКСАЦИИ GSC:")
    print(f"  Всего проверено: {len(check_list)}")
    print(f"  В индексе (PASS): {stats['INDEXED']}")
    print(f"  Просканирована, но не проиндексирована: {stats['CRAWLED_NOT_INDEXED']}")
    print(f"  Обнаружена, но не проиндексирована: {stats['DISCOVERED_NOT_INDEXED']}")
    print(f"  Прочие статусы: {stats['NOT_INDEXED_OTHER']}")
    print(f"  Ошибок запроса: {stats['ERRORS']}")
    print(f"Детальный отчет сохранен в: {REPORT_OUTPUT_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    main()
