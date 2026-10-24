#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовая AI-генерация кадров на моделях для 3 товаров Livi Jewelry:
- prod_20: Колье из флюорита и цирконов
- prod_24: Колье из жемчуга и лазурита
- prod_11: Комплект (колье из аметиста и розового кварца + серьги из аметиста)
"""

import io
import pathlib
import sys
import time
from PIL import Image
from google import genai

import os
API_KEY = os.environ.get("GEMINI_API_KEY", "")

TEST_ITEMS = [
    {
        "id": "prod_20",
        "title": "Колье из флюорита и цирконов",
        "ref": "assets/kole-iz-flyuorita-i-tsirkonov-35000.webp",
        "out": "test_preview_prod_20.webp",
        "prompt": (
            "Professional commercial luxury jewelry photography in the refined aesthetic of Cartier and Tiffany & Co. "
            "An elegant 24-year-old Kazakh fashion model with glowing warm porcelain skin, graceful neck, and delicate collarbones. "
            "She is wearing a sophisticated off-shoulder light silk top. "
            "Focus and medium close-up on the model's neck and collarbones showcasing this exact necklace from the reference photo. "
            "CRITICAL REQUIREMENT: 100% preserve the exact shape, translucent mint-green and lavender fluorite gemstone beads, "
            "and sparkling cubic zirconia crystal accents of the necklace exactly as shown in the reference image. "
            "The choker necklace must rest naturally and flawlessly on her neck. "
            "Soft diffused natural daylight, high-end editorial lighting, ultra-sharp jewelry details, 8k resolution, photorealistic."
        )
    },
    {
        "id": "prod_24",
        "title": "Колье из жемчуга и лазурита",
        "ref": "assets/kole-iz-zhemchuga-i-lazurita-40000.webp",
        "out": "test_preview_prod_24.webp",
        "prompt": (
            "Professional commercial luxury jewelry photography in the refined aesthetic of Cartier and Tiffany & Co. "
            "An elegant 24-year-old Kazakh fashion model with flawless warm porcelain skin, graceful neck, and delicate collarbones. "
            "She is wearing a minimal chic off-shoulder ivory silk top. "
            "Focus and close-up on the model's neck and collarbones showcasing this exact necklace from the reference photo. "
            "CRITICAL REQUIREMENT: 100% preserve the exact alternating arrangement of natural lustrous white pearls and "
            "royal ultramarine blue lapis lazuli beads with natural golden pyrite specks exactly as shown in the reference image. "
            "The necklace sits naturally and gracefully along her collarbone. "
            "Soft diffused natural daylight, high-end editorial lighting, ultra-sharp jewelry details, 8k resolution, photorealistic."
        )
    },
    {
        "id": "prod_11",
        "title": "Комплект (колье из аметиста и розового кварца + серьги из аметиста)",
        "ref": "assets/kole-iz-ametista-i-rozovogo-kvartsa-s-sergami-45000.webp",
        "out": "test_preview_prod_11.webp",
        "prompt": (
            "Professional commercial luxury jewelry photography in the refined aesthetic of Cartier and Tiffany & Co. "
            "An elegant 24-year-old Kazakh fashion model with hair swept up in an elegant soft updo, showing her earlobes, graceful neck, and collarbones. "
            "CRITICAL REQUIREMENT: She is wearing the COMPLETE MATCHING JEWELRY SET from the reference image simultaneously: "
            "1. The matching amethyst earrings from the reference image are worn in her earlobes, with delicate lavender amethyst drop stones and silver/rhodium ear wires. "
            "2. The necklace from the reference image is gracefully worn around her neck, featuring the exact arrangement of soft pastel pink rose quartz and translucent lavender amethyst beads. "
            "She is wearing a soft blush off-shoulder silk dress. "
            "The composition is a three-quarter portrait clearly displaying BOTH the earrings in her ear and the necklace on her neck and collarbones. "
            "Soft diffused natural daylight, high-end luxury editorial lighting, ultra-sharp jewelry details, 8k resolution, photorealistic."
        )
    }
]

def generate_item(client, item, root_dir):
    ref_path = root_dir / item["ref"]
    out_path = root_dir / item["out"]

    if not ref_path.exists():
        print(f"[{item['id']}] Ошибка: файл референса не найден: {ref_path}")
        return False

    print(f"\n--- [{item['id']}] {item['title']} ---")
    print(f"Загрузка референса: {ref_path.name}")
    ref_img = Image.open(ref_path)

    print("Отправка запроса в Gemini API...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[item["prompt"], ref_img]
        )
    except Exception as e:
        print(f"[{item['id']}] Ошибка при вызове Gemini API: {e}")
        return False

    image_bytes = None
    for candidate in response.candidates:
        if not candidate.content or not candidate.content.parts:
            continue
        for part in candidate.content.parts:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                image_bytes = part.inline_data.data
                break
            elif getattr(part, "data", None):
                image_bytes = part.data
                break

    if not image_bytes:
        print(f"[{item['id']}] В ответе модели не найдено изображение.")
        return False

    img = Image.open(io.BytesIO(image_bytes))
    img.save(out_path, "WEBP", quality=90, method=6)
    print(f"[{item['id']}] Готово! Сохранено: {out_path.name} ({img.size[0]}x{img.size[1]} px)")
    return True

def main():
    root_dir = pathlib.Path(__file__).parent
    client = genai.Client(api_key=API_KEY)

    print("Запуск генерации для 3 товаров...")
    success_count = 0
    for idx, item in enumerate(TEST_ITEMS, start=1):
        ok = generate_item(client, item, root_dir)
        if ok:
            success_count += 1
        if idx < len(TEST_ITEMS):
            print("Пауза 3 сек между запросами...")
            time.sleep(3)

    print(f"\n==========================================")
    print(f"Итог: успешно сгенерировано {success_count} из {len(TEST_ITEMS)} фото!")

if __name__ == "__main__":
    main()
