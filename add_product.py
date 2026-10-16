#!/usr/bin/env python3
"""
Livi Jewelry - Скрипт мгновенного добавления/выгрузки нового товара
Использование:
    python add_product.py \
      --image path/to/photo.jpg \
      --title "Колье с барочным жемчугом" \
      --category "Necklaces" \
      --price 25000 \
      --materials "Натуральный жемчуг, Позолота" \
      --description "Колье ручной работы с крупным барочным жемчугом" \
      [--featured] \
      [--commit]

Категории: Necklaces, Sets, Bracelets, Lariats, Chains
"""

import os
import sys
import json
import argparse
import subprocess
import re
from PIL import Image, ImageOps

# Таблица транслитерации для чистых URL и имен файлов
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
    try:
        with Image.open(image_path) as im:
            im = ImageOps.exif_transpose(im).convert('L').resize((32, 32), Image.Resampling.LANCZOS)
            return list(getattr(im, 'get_flattened_data', im.getdata)())
    except Exception:
        return None

def compute_diff(fp1, fp2):
    if not fp1 or not fp2 or len(fp1) != len(fp2):
        return 999.0
    return sum(abs(a - b) for a, b in zip(fp1, fp2)) / len(fp1)

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
    
    old_size = os.path.getsize(src_path) / 1024
    new_size = os.path.getsize(dst_path) / 1024
    print(f"[OK] Фото оптимизировано: {old_size:.1f} KB -> {new_size:.1f} KB WebP ({dst_path})")

def main():
    parser = argparse.ArgumentParser(description="Добавление товара в каталог Livi Jewelry")
    parser.add_argument("--image", required=True, help="Путь к исходной фотографии (jpg, png, webp)")
    parser.add_argument("--title", required=True, help="Название товара")
    parser.add_argument("--category", required=True, choices=["Necklaces", "Sets", "Bracelets", "Lariats", "Chains"], help="Категория")
    parser.add_argument("--price", type=int, required=True, help="Цена в тенге (число)")
    parser.add_argument("--materials", default="", help="Материалы через запятую")
    parser.add_argument("--description", default="", help="Описание товара")
    parser.add_argument("--featured", action="store_true", help="Поместить в избранное на главной")
    parser.add_argument("--out-of-stock", action="store_true", help="Пометить как отсутствующий")
    parser.add_argument("--force", action="store_true", help="Добавить принудительно, игнорируя защиту от дубликатов")
    parser.add_argument("--commit", action="store_true", help="Сформировать git commit после выгрузки")
    parser.add_argument("--push", action="store_true", help="Сделать git push в репозиторий")

    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"[ERROR] Файл изображения не найден: {args.image}")
        sys.exit(1)

    products_file = "products.json"
    if os.path.exists(products_file):
        with open(products_file, "r", encoding="utf-8") as f:
            products = json.load(f)
    else:
        products = []

    # Защита от дубликатов (по фото и названию)
    if not args.force:
        cand_fp = get_image_fingerprint(args.image)
        norm_title = re.sub(r'[\s\W_]+', '', args.title.lower())
        for p in products:
            if cand_fp and p.get("image") and os.path.exists(p["image"]):
                efp = get_image_fingerprint(p["image"])
                if efp and compute_diff(cand_fp, efp) < 12.0:
                    print(f"[SKIP] Товар уже есть в каталоге! Фото совпадает с {p['id']} (\"{p.get('title')}\").")
                    print("       Используйте флаг --force, если действительно хотите добавить повторно.")
                    sys.exit(0)
            norm_existing = re.sub(r'[\s\W_]+', '', p.get("title", "").lower())
            if norm_title == norm_existing and p.get("price") == args.price:
                print(f"[SKIP] Товар уже есть в каталоге! Название и цена совпадают с {p['id']} (\"{p.get('title')}\").")
                print("       Используйте флаг --force, если действительно хотите добавить повторно.")
                sys.exit(0)

    # Генерация ID
    existing_ids = [int(re.sub(r'\D', '', p.get("id", "0")) or 0) for p in products]
    next_num = max(existing_ids, default=0) + 1
    new_id = f"prod_{next_num:02d}"

    # Имя файла картинки
    slug = slugify(args.title)
    img_filename = f"{slug}-{args.price}.webp"
    assets_dir = "assets"
    dst_img_path = os.path.join(assets_dir, img_filename)

    # Проверка на коллизию имени
    counter = 1
    while os.path.exists(dst_img_path):
        img_filename = f"{slug}-{args.price}-{counter}.webp"
        dst_img_path = os.path.join(assets_dir, img_filename)
        counter += 1

    # Калибровка и сжатие в WebP
    optimize_image(args.image, dst_img_path)

    # Обработка материалов
    if args.materials:
        materials_list = [m.strip() for m in args.materials.split(",") if m.strip()]
    else:
        materials_list = ["Натуральный жемчуг", "Ювелирный сплав"]

    desc = args.description or f"{args.title} — украшение ручной работы из натуральных материалов."

    new_product = {
        "id": new_id,
        "title": args.title,
        "category": args.category,
        "price": args.price,
        "image": f"assets/{img_filename}",
        "materials": materials_list,
        "description": desc,
        "inStock": not args.out_of_stock,
        "featured": bool(args.featured)
    }

    products.append(new_product)

    with open(products_file, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"[OK] Товар {new_id} ({args.title}) добавлен в {products_file}.")
    print(f"     Категория: {args.category} | Цена: {args.price} тг | Фото: assets/{img_filename}")

    try:
        from generate_product_pages import generate_product_pages
        generate_product_pages()
    except Exception:
        pass

    try:
        from generate_feed import generate_feed
        generate_feed()
    except Exception:
        pass

    try:
        from generate_sitemap import generate_sitemap
        generate_sitemap()
    except Exception:
        pass

    if args.commit or args.push:
        try:
            subprocess.run(["git", "add", "products.json", dst_img_path, "product/", "google_merchant_feed.xml", "sitemap.xml"], check=True)
            commit_msg = f"Добавлен товар: {args.title} ({args.price} тг)"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            print(f"[OK] Git commit создан: \"{commit_msg}\"")
            if args.push:
                subprocess.run(["git", "push"], check=True)
                print("[OK] Изменения успешно отправлены на GitHub!")
        except Exception as e:
            print(f"[WARN] Ошибка git: {e}")

if __name__ == "__main__":
    main()
