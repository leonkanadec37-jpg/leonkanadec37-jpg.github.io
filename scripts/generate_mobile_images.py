#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор мобильных WebP-изображений (750w) для Livi Jewelry.
Создает оптимизированные копии фотографий (ширина 750px, quality 82, method 6)
для поддержки srcset и ускорения мобильного LCP на 3G/4G.
"""

import os
import json
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_FILE = os.path.join(ROOT_DIR, "products.json")


def generate_mobile_images():
    if not os.path.exists(PRODUCTS_FILE):
        print(f"Error: {PRODUCTS_FILE} not found.")
        return

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    generated = 0
    skipped = 0

    for p in products:
        rel_path = (p.get("image") or "").lstrip("/")
        full_path = os.path.join(ROOT_DIR, rel_path)
        if not os.path.exists(full_path):
            continue

        base, ext = os.path.splitext(full_path)
        out_path = f"{base}-750w.webp"

        # Check if out_path exists and is newer than source
        if os.path.exists(out_path) and os.path.getmtime(out_path) >= os.path.getmtime(full_path):
            skipped += 1
            continue

        try:
            with Image.open(full_path) as im:
                w, h = im.size
                if w > 750:
                    new_w = 750
                    new_h = int(h * (750 / w))
                    im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    im_resized.save(out_path, "WEBP", quality=82, method=6)
                else:
                    im.save(out_path, "WEBP", quality=82, method=6)
                generated += 1
        except Exception as e:
            print(f"Error resizing {full_path}: {e}")

    print(f"[Mobile Images] Done: {generated} generated, {skipped} up-to-date.")


if __name__ == "__main__":
    generate_mobile_images()
