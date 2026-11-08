#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор мобильных WebP-изображений (400w, 750w, 1080w) для Livi Jewelry.
Создает оптимизированные копии фотографий:
- 400w (quality 78, method 6) для 2-колоночной мобильной сетки (50vw)
- 750w (quality 82, method 6) для экранов 1-2x и планшетов
- 1080w (quality 82, method 6) для Hero-обложки на экранах высокой плотности
"""

import os
import json
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_FILE = os.path.join(ROOT_DIR, "products.json")

# Standalone hero/cover images and required widths
STANDALONE_CONFIG = {
    "assets/hero-kole-iz-naturalnogo-zhemchuga-80000.webp": [
        (750, 82, "-750w.webp"),
        (1080, 82, "-1080w.webp"),
    ]
}


def resize_image(full_path, target_width, quality, out_path):
    # Check if out_path exists and is newer than source
    if os.path.exists(out_path) and os.path.getmtime(out_path) >= os.path.getmtime(full_path):
        return False

    with Image.open(full_path) as im:
        w, h = im.size
        if w > target_width:
            new_w = target_width
            new_h = int(h * (target_width / w))
            im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
            im_resized.save(out_path, "WEBP", quality=quality, method=6)
        else:
            im.save(out_path, "WEBP", quality=quality, method=6)
    return True


def generate_mobile_images():
    if not os.path.exists(PRODUCTS_FILE):
        print(f"Error: {PRODUCTS_FILE} not found.")
        return

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    generated = 0
    skipped = 0

    # 1. Product images: 400w and 750w
    for p in products:
        rel_path = (p.get("image") or "").lstrip("/")
        if not rel_path:
            continue
        full_path = os.path.join(ROOT_DIR, rel_path)
        if not os.path.exists(full_path):
            continue

        base, _ = os.path.splitext(full_path)
        
        # 400w
        try:
            if resize_image(full_path, 400, 78, f"{base}-400w.webp"):
                generated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"Error generating 400w for {full_path}: {e}")

        # 750w
        try:
            if resize_image(full_path, 750, 82, f"{base}-750w.webp"):
                generated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"Error generating 750w for {full_path}: {e}")

    # 2. Standalone hero images
    for rel_path, configs in STANDALONE_CONFIG.items():
        full_path = os.path.join(ROOT_DIR, rel_path)
        if not os.path.exists(full_path):
            continue
        base, _ = os.path.splitext(full_path)
        for w, q, suffix in configs:
            out_path = f"{base}{suffix}"
            try:
                if resize_image(full_path, w, q, out_path):
                    generated += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"Error generating {suffix} for {full_path}: {e}")

    print(f"[Mobile Images] Done: {generated} generated, {skipped} up-to-date.")


if __name__ == "__main__":
    generate_mobile_images()
