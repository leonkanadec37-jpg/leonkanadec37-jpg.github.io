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

def format_num(n):
    return f"{n:,}".replace(',', ' ')

def log_warning(msg):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [WARN] {msg}\n"
    print(f"[WARN] {msg}")
    try:
        with open("sync_warnings.log", "a", encoding="utf-8") as f:
            f.write(formatted)
    except Exception as e:
        print(f"[ERROR] Не удалось записать в sync_warnings.log: {e}")

def parse_item_info(raw_title):
    raw = raw_title.strip()
    
    # Игнорируем видео и не-товары
    if 'не товар' in raw.lower() or raw.lower().endswith('.mp4') or 'video' in raw.lower():
        return None

    note = ""
    if "под заказ" in raw.lower():
        note = " (под заказ)"
    
    clean_raw = re.sub(r'\s*\(\s*под заказ\s*\)\s*', '', raw, flags=re.IGNORECASE).strip()

    # Заменяем точки-разделители между элементами: "36000 тенге. Серьги" -> "36000 тенге, Серьги"
    s = re.sub(r'(\d+[\.\s]?\d{3})\.\s*(тг|тенге)', r'\1 \2', clean_raw, flags=re.IGNORECASE)
    s = re.sub(r'(\d+[\.\s]?\d{3}\s*(?:тг|тенге)?)\.\s+([А-ЯA-Z])', r'\1, \2', s)

    # Разбиваем по запятым
    chunks = [c.strip() for c in re.split(r'[,;]', s) if c.strip()]
    
    elements = []
    for ch in chunks:
        p_match = re.search(r'(\d+[\.\s]?\d{3})\s*(?:тг|тенге|\.)?', ch, flags=re.IGNORECASE)
        if p_match:
            price_num = int(re.sub(r'\D', '', p_match.group(1)))
            if price_num > 0:
                name = ch[:p_match.start()] + ch[p_match.end():]
                name = re.sub(r'(?:тг|тенге|\.|\-|–|—)', ' ', name, flags=re.IGNORECASE).strip()
                name = re.sub(r'^(?:и|\+)\s+', '', name, flags=re.IGNORECASE).strip()
                if name:
                    elements.append((name, price_num))

    if not elements:
        p_match = re.search(r'(\d+[\.\s]?\d{3})', raw)
        if not p_match:
            log_warning(f"Файл '{raw_title}' пропущен: отсутствует цена в названии или опечатка (не найдены цифры стоимости).")
            return None
        price_num = int(re.sub(r'\D', '', p_match.group(1)))
        if price_num <= 0:
            log_warning(f"Файл '{raw_title}' пропущен: невалидная цена {price_num} KZT.")
            return None
        clean_name = re.sub(r'\s*\.?\s*\d+[\.\s]?\d*\s*(?:тг|тенге|\.)?.*$', '', raw, flags=re.IGNORECASE).strip()
        elements.append((clean_name or raw, price_num))

    if not elements or any(p <= 0 for _, p in elements):
        log_warning(f"Файл '{raw_title}' пропущен: элементы содержат некорректную цену.")
        return None

    if len(elements) == 1:
        elem_name, elem_price = elements[0]
        if elem_name.lower().startswith('коле '):
            elem_name = 'Колье ' + elem_name[5:]
        elem_name = elem_name[0].upper() + elem_name[1:] if elem_name else ""
        elem_name = re.sub(r'\s+', ' ', elem_name).strip(' .')
        title = elem_name + note
        if title.lower().startswith('коле '):
            title = 'Колье ' + title[5:]
        display_price = elem_price
        
        t_low = title.lower()
        if 'браслет' in t_low:
            category = 'Bracelets'
        elif 'комплект' in t_low or 'гарнитур' in t_low:
            category = 'Sets'
        elif 'сотуар' in t_low or 'украшение из' in t_low:
            category = 'Lariats'
        elif 'цепь' in t_low:
            category = 'Chains'
        else:
            category = 'Necklaces'
            
        description = f"{elem_name} — {format_num(elem_price)} тг{note}."
    else:
        total_price = sum(p for _, p in elements)
        category = 'Sets'
        
        elem_names_lower = [e[0].lower() for e in elements]
        if 'булавка' in elem_names_lower[0]:
            parts = [e[0].lower() for e in elements]
            title = f"Гарнитур: {', '.join(parts)}" + note
        elif any('клубничк' in n for n in elem_names_lower):
            title = "Сет колье: «Клубнички» и розовый кварц с жемчугом" + note
        elif any('колье' in n for n in elem_names_lower):
            base = [n[0] for n in elements if 'колье' in n[0].lower()][0]
            other = [e[0].lower() for e in elements if 'колье' not in e[0].lower()]
            if other:
                title = f"Комплект: {base}, {', '.join(other)}" + note
            else:
                title = f"Сет: {', '.join(e[0] for e in elements)}" + note
        else:
            title = f"Комплект: {', '.join(e[0] for e in elements)}" + note
            
        title = title[0].upper() + title[1:]
        title = re.sub(r'\s+', ' ', title).strip(' .')
        
        desc_parts = []
        for name, p in elements:
            n_clean = name[0].upper() + name[1:] if name else ""
            n_clean = re.sub(r'\s+', ' ', n_clean).strip(' .')
            desc_parts.append(f"{n_clean} — {format_num(p)} тг")
        
        items_str = ", ".join(desc_parts)
        description = f"В комплекте: {items_str}. Полная стоимость комплекта — {format_num(total_price)} тг{note}. Каждое изделие можно приобрести по отдельности или полным сетом."
        display_price = total_price

    mats = detect_materials(title, description)
    return {
        'title': title,
        'category': category,
        'display_price': display_price,
        'description': description,
        'materials': mats,
        'elements': elements
    }

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
    if 'флюорит' in text: mats.append('Натуральный флюорит')
    if 'циркон' in text: mats.append('Цирконы')
    if 'гематит' in text: mats.append('Гематит')
    if 'авантюрин' in text: mats.append('Натуральный авантюрин')
    if 'позолот' in text or 'золот' in text: mats.append('Позолота')
    
    mats.append('Ювелирный сплав')
    return list(dict.fromkeys(mats))

def update_shop_schema(products):
    """Обновляет микроразметку schema.org/ItemList и статическую сетку товаров в shop.html и index.html"""
    try:
        from generate_product_pages import sync_static_catalogs
        sync_static_catalogs(products)
    except Exception as e:
        print(f"[WARN] Ошибка синхронизации статических каталогов: {e}")

def download_drive_file(fid, dst_path):
    """Скачивает файл с Google Drive по fid напрямую через drive.usercontent"""
    url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&authuser=0"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url, headers=headers, timeout=30, stream=True)
        if r.status_code == 200:
            with open(dst_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=65536):
                    f.write(chunk)
            if os.path.exists(dst_path) and os.path.getsize(dst_path) > 1000:
                return True
    except Exception as e:
        print(f"[WARN] Прямое скачивание {fid} не удалось: {e}")
    return False

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
        print(f"[INFO] Считываем каталог из Google Drive: {drive_url}")
        
        # Парсим оригинальные названия файлов и ID из HTML страницы папки Google Диска
        current_drive_ids = set()
        drive_items = []
        try:
            r = requests.get(drive_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            soup = BeautifulSoup(r.content.decode('utf-8', errors='replace'), 'html.parser')
            for tr in soup.find_all('tr', attrs={'data-id': True}):
                fid = tr.get('data-id')
                if not fid:
                    continue
                current_drive_ids.add(fid)
                label = tr.get('aria-label') or ''
                if not label:
                    for el in tr.find_all(True):
                        al = el.get('aria-label') or ''
                        if 'Image' in al or 'Shared' in al or 'Video' in al:
                            label = al
                            break
                clean_title = label.replace(' Image Shared', '').replace(' Shared', '').strip()
                if clean_title:
                    drive_items.append((fid, clean_title))
        except Exception as e:
            print(f"[WARN] Не удалось извлечь метаданные через web: {e}")

        # Собираем кандидатов для проверки
        existing_by_drive_id = {p['drive_id']: p for p in products if p.get('drive_id')}

        for fid, raw_title in drive_items:
            # Игнорируем служебные файлы (видео, баннеры, файлы с пометкой "не товар")
            if any(term in raw_title.lower() for term in ['не товар', 'видео', 'баннер', 'логотип']):
                print(f"[SKIP] Пропущен служебный файл: {raw_title}")
                continue

            # Если товар уже в каталоге, используем его локальное фото для сверки
            if fid in existing_by_drive_id:
                local_img = existing_by_drive_id[fid].get('image')
                if local_img and os.path.exists(local_img):
                    candidates.append({
                        'source_path': local_img,
                        'raw_title': raw_title,
                        'drive_id': fid
                    })
                    continue

            # Новый товар: скачиваем напрямую без ограничений
            dl_path = os.path.join(temp_dir, f"{fid}.jpg")
            print(f"[DOWNLOAD] Скачиваем новый товар с Google Диска: {raw_title} (ID: {fid})...")
            if download_drive_file(fid, dl_path):
                candidates.append({
                    'source_path': dl_path,
                    'raw_title': raw_title,
                    'drive_id': fid
                })
            else:
                print(f"[ERROR] Не удалось скачать файл {raw_title} (ID: {fid})")

    elif local_folder and os.path.exists(local_folder):
        for fn in os.listdir(local_folder):
            fp = os.path.join(local_folder, fn)
            if os.path.isfile(fp) and fn.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.mpo', '.heic')):
                candidates.append({'source_path': fp, 'raw_title': os.path.splitext(fn)[0]})

    print(f"[INFO] Найдено {len(candidates)} файлов для проверки.")

    existing_ids = [int(re.sub(r'\D', '', p.get("id", "0")) or 0) for p in products]
    next_num = max(existing_ids, default=0) + 1
    added_count = 0
    updated_count = 0

    for cand in candidates:
        src = cand['source_path']
        raw_t = cand['raw_title']

        parsed_info = parse_item_info(raw_t)
        if not parsed_info:
            print(f"[IGNORE] Пропущен не-товар: {raw_t}")
            continue

        cand_fp = get_image_fingerprint(src)

        # 1. Проверка на дубликат по изображению
        is_duplicate = False
        duplicate_reason = ""
        matched_prod = None

        if cand_fp:
            for pid, (efp, ep) in existing_fps.items():
                diff = compute_diff(cand_fp, efp)
                if diff < 12.0:  # порог различия менее 5%
                    is_duplicate = True
                    matched_prod = ep
                    duplicate_reason = f"визуально совпадает с {pid} (\"{ep.get('title')}\", diff={diff:.2f})"
                    break

        # 2. Проверка по нормализованному названию
        if not is_duplicate:
            norm_cand = normalize_title(parsed_info['title'])
            for p in products:
                if normalize_title(p.get('title', '')) == norm_cand:
                    is_duplicate = True
                    matched_prod = p
                    duplicate_reason = f"название совпадает с {p['id']} (\"{p.get('title')}\")"
                    break

        # 3. Проверка по drive_id
        if not is_duplicate and cand.get('drive_id'):
            for p in products:
                if p.get('drive_id') == cand.get('drive_id'):
                    is_duplicate = True
                    matched_prod = p
                    duplicate_reason = f"drive_id совпадает с {p['id']} (\"{p.get('title')}\")"
                    break

        if is_duplicate and matched_prod:
            if cand.get('drive_id') and not matched_prod.get('drive_id'):
                matched_prod['drive_id'] = cand['drive_id']
            
            # Актуализируем описание, цены комплекта и заголовок
            changed = False
            is_set = len(parsed_info.get('elements', [])) > 1 or parsed_info.get('category') == 'Sets'
            
            # Для сетов - всегда применяем полное название, категорию Sets, полную цену и развернутое описание
            if is_set:
                if matched_prod.get('title') != parsed_info['title']:
                    matched_prod['title'] = parsed_info['title']
                    changed = True
                if matched_prod.get('price') != parsed_info['display_price']:
                    matched_prod['price'] = parsed_info['display_price']
                    changed = True
                if matched_prod.get('category') != 'Sets':
                    matched_prod['category'] = 'Sets'
                    changed = True
                if matched_prod.get('description') != parsed_info['description']:
                    matched_prod['description'] = parsed_info['description']
                    changed = True
                if not matched_prod.get('materials') or matched_prod.get('materials') == ['Ювелирный сплав']:
                    matched_prod['materials'] = parsed_info['materials']
                    changed = True
            else:
                # Одиночный товар: актуализируем цену и категорию
                if matched_prod.get('price') != parsed_info['display_price']:
                    matched_prod['price'] = parsed_info['display_price']
                    changed = True
                # Если название в каталоге содержало опечатку (например "Коле" -> "Колье")
                if matched_prod.get('title', '').startswith('Коле '):
                    matched_prod['title'] = parsed_info['title']
                    changed = True
                # Если описание было шаблоном ("— авторское украшение ручной работы...")
                if 'авторское украшение ручной работы из натуральных камней' in matched_prod.get('description', ''):
                    matched_prod['description'] = parsed_info['description']
                    changed = True
                if not matched_prod.get('materials') or matched_prod.get('materials') == ['Ювелирный сплав']:
                    matched_prod['materials'] = parsed_info['materials']
                    changed = True
            
            if changed:
                updated_count += 1
                print(f"[SYNC/UPDATE] Обновлен товар {matched_prod['id']}: {matched_prod['title']} ({matched_prod['price']} тг)")
            else:
                print(f"[SKIP] Товар уже есть в каталоге: {raw_t} -> {duplicate_reason}")
            continue

        # Создаем новый товар
        title = parsed_info['title']
        price = parsed_info['display_price']
        cat = parsed_info['category']
        mats = parsed_info['materials']
        desc = parsed_info['description']

        new_id = f"prod_{next_num:02d}"
        next_num += 1

        slug = slugify(title)
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
            "title": title,
            "category": cat,
            "price": price,
            "image": f"assets/{filename}",
            "materials": mats,
            "description": desc,
            "inStock": True,
            "featured": True
        }
        if cand.get('drive_id'):
            new_prod['drive_id'] = cand['drive_id']

        products.append(new_prod)
        existing_fps[new_id] = (cand_fp, new_prod)
        added_count += 1
        print(f"[ADD] Добавлен товар {new_id}: {title} ({price} тг) -> assets/{filename}")

    # Двусторонняя синхронизация: мягкая архивация (Soft Archive 14 дней) товаров, удаленных с Google Диска
    archived_count = 0
    purged_count = 0
    from datetime import datetime

    if drive_url and len(current_drive_ids) > 0:
        remaining_products = []
        now = datetime.now()
        for p in products:
            p_drive_id = p.get('drive_id')
            if p_drive_id and p_drive_id not in current_drive_ids:
                # Товар отсутствует на Google Диске
                if not p.get('archived'):
                    # Первый раз: переводим в Soft Archive на 14 дней
                    p['archived'] = True
                    p['archived_at'] = now.strftime('%Y-%m-%d')
                    p['inStock'] = False
                    p['featured'] = False
                    archived_count += 1
                    print(f"[ARCHIVE] Товар {p['id']} (\"{p.get('title')}\") переведен в статус 'Продано' (soft archive на 14 дней, out_of_stock)")
                    remaining_products.append(p)
                else:
                    # Товар уже в архиве - проверяем срок 14 дней
                    arch_date_str = p.get('archived_at')
                    days_in_archive = 0
                    if arch_date_str:
                        try:
                            arch_date = datetime.strptime(arch_date_str[:10], '%Y-%m-%d')
                            days_in_archive = (now - arch_date).days
                        except Exception:
                            days_in_archive = 0

                    if days_in_archive >= 14:
                        print(f"[PURGE] Товар {p['id']} (\"{p.get('title')}\") удален окончательно (в архиве {days_in_archive} дн. >= 14).")
                        img_path = p.get('image')
                        if img_path and os.path.exists(img_path):
                            try:
                                os.remove(img_path)
                            except Exception:
                                pass
                        html_path = os.path.join("product", f"{p['id']}.html")
                        if os.path.exists(html_path):
                            try:
                                os.remove(html_path)
                            except Exception:
                                pass
                        purged_count += 1
                    else:
                        remaining_products.append(p)
            else:
                # Товар присутствует на Google Диске
                if p.get('archived'):
                    # Если товар снова загрузили на Диск - восстанавливаем из архива
                    p['archived'] = False
                    p['inStock'] = True
                    p.pop('archived_at', None)
                    print(f"[RESTORE] Товар {p['id']} (\"{p.get('title')}\") восстановлен из архива в активный каталог.")
                    updated_count += 1
                remaining_products.append(p)
        products = remaining_products

    # Сохраняем products.json при наличии любых изменений (добавления, обновления, архивации или удаления)
    if added_count > 0 or updated_count > 0 or archived_count > 0 or purged_count > 0:
        with open(products_file, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        update_shop_schema(products)
        try:
            from generate_product_pages import generate_product_pages
            generate_product_pages()
        except Exception as e:
            print(f"[WARN] Ошибка генерации статических страниц товаров: {e}")

        try:
            from generate_feed import generate_feed
            generate_feed()
        except Exception as e:
            print(f"[WARN] Ошибка обновления XML-фида: {e}")

        try:
            from generate_sitemap import generate_sitemap
            generate_sitemap()
        except Exception as e:
            print(f"[WARN] Ошибка обновления sitemap.xml: {e}")

        actions = []
        if added_count > 0:
            actions.append(f"добавлено: {added_count}")
        if updated_count > 0:
            actions.append(f"обновлено: {updated_count}")
        if archived_count > 0:
            actions.append(f"в архиве (out_of_stock): {archived_count}")
        if purged_count > 0:
            actions.append(f"удалено (>14 дней): {purged_count}")
        summary_str = ", ".join(actions)
        print(f"\n[SUCCESS] Синхронизация завершена ({summary_str}). Всего товаров: {len(products)}")

        if auto_commit or auto_push:
            try:
                subprocess.run(["git", "add", "-A", products_file, "shop.html", "index.html", "feed.xml", "google_merchant_feed.xml", "sitemap.xml", "assets/", "product/", "kolye-iz-zhemchuga.html", "braslety-iz-zhemchuga.html", "sergi-iz-zhemchuga.html"], check=True)
                msg = f"Автосинхронизация каталога: {summary_str}"
                subprocess.run(["git", "commit", "-m", msg], check=True)
                print(f"[OK] Git commit: {msg}")
                if auto_push:
                    subprocess.run(["git", "push"], check=True)
                    print("[OK] Git push выполнен успешно!")
            except Exception as e:
                print(f"[WARN] Ошибка git: {e}")
    else:
        print("\n[OK] Изменений нет — каталог полностью соответствует Google Диску!")

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
