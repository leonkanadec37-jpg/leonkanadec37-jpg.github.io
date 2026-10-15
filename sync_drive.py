#!/usr/bin/env python3
"""
Livi Jewelry - Автоматическая синхронизация товаров из Google Drive или локальной папки.
Включает автоматическое обнаружение дубликатов по фото (perceptual diff) и названию.

Использование:
    python sync_drive.py "https://drive.google.com/drive/folders/ID" [--commit] [--push]
    python sync_drive.py --local-folder "path/to/folder" [--commit] [--push]
"""

import os
import sys
import re
import json
import shutil
import argparse
import subprocess
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

TRANSLIT_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'і': 'i', 'ң': 'n', 'ғ': 'g', 'ү': 'u', 'ұ': 'u', 'қ': 'k', 'ө': 'o', 'һ': 'h'
}

def slugify(text):
    text = text.lower().strip()
    result = []
    for char in text:
        if char in TRANSLIT_MAP:
            result.append(TRANSLIT_MAP[char])
        elif char.isalnum():
            result.append(char)
        elif char in (' ', '-', '_'):
            result.append('-')
    slug = ''.join(result)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug or 'tovar'

def get_image_fingerprint(image_path):
    """32x32 grayscale fingerprint для быстрого сравнения схожести изображений"""
    try:
        with Image.open(image_path) as im:
            im = ImageOps.exif_transpose(im).convert('L').resize((32, 32), Image.Resampling.LANCZOS)
            # Избегаем getdata deprecation warning в новых Pillow
            return list(getattr(im, 'get_flattened_data', im.getdata)())
    except Exception as e:
        return None

def compute_diff(fp1, fp2):
    if not fp1 or not fp2 or len(fp1) != len(fp2):
        return 999.0
    return sum(abs(a - b) for a, b in zip(fp1, fp2)) / len(fp1)

def normalize_title(title):
    return re.sub(r'[\s\W_]+', '', title.lower())

def optimize_image(src_path, dst_path, max_w=1440, max_h=1920, quality=82):
    with Image.open(src_path) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            im = im.convert('RGBA')
        else:
            im = im.convert('RGB')
        
        w, h = im.size
        if w > max_w or h > max_h:
            im.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        im.save(dst_path, "WEBP", quality=quality, method=6)

def detect_category(title):
    t = title.lower()
    if 'браслет' in t:
        return 'Bracelets'
    elif 'комплект' in t or 'гарнитур' in t:
        return 'Sets'
    elif 'сотуар' in t:
        return 'Lariats'
    elif 'цепь' in t:
        return 'Chains'
    else:
        return 'Necklaces'

def extract_price(raw_title):
    # Ищем цены вида "25.000 тг", "34000 тенге", "40.000"
    matches = re.findall(r'(\d+[\.\s]?\d{3})', raw_title)
    if matches:
        # Берем наибольшую или первую
        clean = re.sub(r'\D', '', matches[0])
        return int(clean)
    return 30000

def detect_materials(title, description=""):
    text = (title + " " + description).lower()
    mats = []
    if 'жемчуг' in text: mats.append('Натуральный жемчуг')
    if 'малахит' in text: mats.append('Натуральный малахит')
    if 'агат' in text: mats.append('Натуральный агат')
    if 'гранат' in text: mats.append('Натуральный гранат')
    if 'аметист' in text: mats.append('Натуральный аметист')
    if 'кварц' in text: mats.append('Розовый кварц')
    if 'жадеит' in text: mats.append('Натуральный жадеит')
    if 'тигров' in text: mats.append('Тигровый глаз')
    if 'бирюз' in text: mats.append('Натуральная бирюза')
    if 'коралл' in text: mats.append('Натуральный коралл')
    if 'яшм' in text: mats.append('Яшма')
    if 'авантюрин' in text: mats.append('Натуральный авантюрин')
    if 'позолот' in text or 'золот' in text: mats.append('Позолота')
    
    mats.append('Ювелирный сплав')
    # Убираем дубли сохраняя порядок
    return list(dict.fromkeys(mats))

def update_shop_schema(products):
    if not os.path.exists('shop.html'):
        return
    item_list = []
    for p in products:
        item_list.append({
            "@type": "Product",
            "name": p["title"],
            "image": f"https://livijewelry.kz/{p['image']}",
            "description": p.get("description", ""),
            "offers": {
                "@type": "Offer",
                "price": str(p["price"]),
                "priceCurrency": "KZT"
            }
        })
    schema_obj = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": item_list
    }
    schema_json = json.dumps(schema_obj, ensure_ascii=False, indent=2)
    with open('shop.html', 'r', encoding='utf-8') as f:
        html = f.read()
    pattern = r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema.org",\s*"@type":\s*"ItemList".*?</script>'
    replacement = f'<script type="application/ld+json">\n{schema_json}\n</script>'
    new_html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)
    if count > 0:
        with open('shop.html', 'w', encoding='utf-8') as f:
            f.write(new_html)

def sync_products(drive_url=None, local_folder=None, auto_commit=False, auto_push=False):
    products_file = "products.json"
    if os.path.exists(products_file):
        with open(products_file, "r", encoding="utf-8") as f:
            products = json.load(f)
    else:
        products = []

    print(f"[INFO] Текущих товаров в каталоге: {len(products)}")

    # Собираем отпечатки всех существующих изображений в каталоге
    existing_fps = {}
    for p in products:
        img_p = p.get('image')
        if img_p and os.path.exists(img_p):
            fp = get_image_fingerprint(img_p)
            if fp:
                existing_fps[p['id']] = (fp, p)

    # Скачивание / чтение кандидатов
    temp_dir = "temp_sync"
    os.makedirs(temp_dir, exist_ok=True)

    candidates = []

    if drive_url:
        print(f"[INFO] Скачиваем файлы из Google Drive: {drive_url}")
        subprocess.run([sys.executable, "-m", "gdown", "--folder", drive_url, "-O", temp_dir], check=False)
        
        # Парсим оригинальные названия файлов из HTML страницы диска
        try:
            r = requests.get(drive_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            soup = BeautifulSoup(r.content.decode('utf-8', errors='replace'), 'html.parser')
            for tr in soup.find_all('tr', attrs={'data-id': True}):
                label = tr.get('aria-label') or ''
                if not label:
                    for el in tr.find_all(True):
                        al = el.get('aria-label') or ''
                        if 'Image' in al or 'Shared' in al:
                            label = al
                            break
                clean_title = label.replace(' Image Shared', '').replace(' Shared', '').strip()
                fid = tr.get('data-id')
                # сопоставляем с файлами в папке
                for fn in os.listdir(temp_dir):
                    fp = os.path.join(temp_dir, fn)
                    if os.path.isfile(fp):
                        candidates.append({
                            'source_path': fp,
                            'raw_title': clean_title or fn
                        })
                        break
        except Exception as e:
            print(f"[WARN] Не удалось извлечь метаданные через web: {e}")

        if not candidates:
            for fn in os.listdir(temp_dir):
                fp = os.path.join(temp_dir, fn)
                if os.path.isfile(fp) and fn.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.mpo', '.heic')):
                    candidates.append({'source_path': fp, 'raw_title': fn})

    elif local_folder and os.path.exists(local_folder):
        for fn in os.listdir(local_folder):
            fp = os.path.join(local_folder, fn)
            if os.path.isfile(fp) and fn.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.mpo', '.heic')):
                candidates.append({'source_path': fp, 'raw_title': os.path.splitext(fn)[0]})

    print(f"[INFO] Найдено {len(candidates)} файлов для проверки.")

    existing_ids = [int(re.sub(r'\D', '', p.get("id", "0")) or 0) for p in products]
    next_num = max(existing_ids, default=0) + 1
    added_count = 0

    for cand in candidates:
        src = cand['source_path']
        raw_t = cand['raw_title']
        cand_fp = get_image_fingerprint(src)

        # 1. Проверка на дубликат по изображению
        is_duplicate = False
        duplicate_reason = ""

        if cand_fp:
            for pid, (efp, ep) in existing_fps.items():
                diff = compute_diff(cand_fp, efp)
                if diff < 12.0:  # порог различия менее 5%
                    is_duplicate = True
                    duplicate_reason = f"визуально совпадает с {pid} (\"{ep.get('title')}\", diff={diff:.2f})"
                    break

        # 2. Проверка по нормализованному названию
        if not is_duplicate:
            norm_cand = normalize_title(raw_t)
            for p in products:
                if normalize_title(p.get('title', '')) == norm_cand:
                    is_duplicate = True
                    duplicate_reason = f"название совпадает с {p['id']} (\"{p.get('title')}\")"
                    break

        if is_duplicate:
            print(f"[SKIP] Товар пропущен (дубликат): {raw_t} -> {duplicate_reason}")
            continue

        # Создаем новый товар
        price = extract_price(raw_t)
        # Очищаем название от цены в конце
        clean_name = re.sub(r'\s*\.?\s*\d+[\.\s]?\d*\s*(?:тг|тенге|\.)?.*$', '', raw_t, flags=re.IGNORECASE).strip()
        if not clean_name:
            clean_name = raw_t

        cat = detect_category(clean_name)
        mats = detect_materials(clean_name)
        new_id = f"prod_{next_num:02d}"
        next_num += 1

        slug = slugify(clean_name)
        filename = f"{slug}-{price}.webp"
        dst_path = os.path.join("assets", filename)
        c = 1
        while os.path.exists(dst_path):
            filename = f"{slug}-{price}-{c}.webp"
            dst_path = os.path.join("assets", filename)
            c += 1

        optimize_image(src, dst_path)
        new_prod = {
            "id": new_id,
            "title": clean_name,
            "category": cat,
            "price": price,
            "image": f"assets/{filename}",
            "materials": mats,
            "description": f"{clean_name} — авторское украшение ручной работы из натуральных камней.",
            "inStock": True,
            "featured": True
        }
        products.append(new_prod)
        existing_fps[new_id] = (cand_fp, new_prod)
        added_count += 1
        print(f"[ADD] Добавлен товар {new_id}: {clean_name} ({price} тг) -> assets/{filename}")

    # Сохраняем products.json
    if added_count > 0:
        with open(products_file, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        update_shop_schema(products)
        print(f"\n[SUCCESS] Добавлено новых товаров: {added_count}. Всего товаров: {len(products)}")

        if auto_commit or auto_push:
            try:
                subprocess.run(["git", "add", products_file, "shop.html", "assets/"], check=True)
                msg = f"Автосинхронизация каталога: добавлено {added_count} новых товаров"
                subprocess.run(["git", "commit", "-m", msg], check=True)
                print(f"[OK] Git commit: {msg}")
                if auto_push:
                    subprocess.run(["git", "push"], check=True)
                    print("[OK] Git push выполнен успешно!")
            except Exception as e:
                print(f"[WARN] Ошибка git: {e}")
    else:
        print("\n[OK] Новых товаров не найдено — все товары уже есть в каталоге!")

    # Удаляем временные файлы
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Синхронизация каталога Livi Jewelry с защитой от дубликатов")
    parser.add_argument("drive_url", nargs="?", default=None, help="Ссылка на папку Google Drive")
    parser.add_argument("--local-folder", default=None, help="Путь к локальной папке с фотографиями")
    parser.add_argument("--commit", action="store_true", help="Автоматически создать git commit")
    parser.add_argument("--push", action="store_true", help="Автоматически отправить в git push")

    args = parser.parse_args()
    if not args.drive_url and not args.local_folder:
        print("Использование: python sync_drive.py <URL_диска> [--commit] [--push]")
        sys.exit(1)

    sync_products(drive_url=args.drive_url, local_folder=args.local_folder, auto_commit=args.commit, auto_push=args.push)
