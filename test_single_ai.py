#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовая AI-генерация кадра на модели для колье Livi Jewelry
с использованием модели gemini-2.5-flash-image через библиотеку google.genai.
"""

import io
import pathlib
import sys
from PIL import Image
from google import genai

import os
API_KEY = os.environ.get("GEMINI_API_KEY", "")

def main():
    root_dir = pathlib.Path(__file__).parent
    ref_image_path = root_dir / "assets" / "kole-iz-naturalnogo-zhemchuga-80000.webp"
    output_path = root_dir / "test_model_preview.webp"

    if not ref_image_path.exists():
        print(f"Ошибка: референс не найден: {ref_image_path}")
        sys.exit(1)

    print(f"Загрузка референса: {ref_image_path.name}...")
    ref_image = Image.open(ref_image_path)

    client = genai.Client(api_key=API_KEY)

    prompt = (
        "Professional commercial luxury jewelry photography in the refined aesthetic of Cartier and Tiffany & Co. "
        "A stunning, elegant 24-year-old Kazakh fashion model with flawless warm porcelain skin, graceful neck, and delicate collarbones. "
        "She is wearing an off-shoulder beige silk dress. "
        "Focus and close-up on the model's neck and collarbones showcasing this exact necklace from the reference photo. "
        "CRITICAL REQUIREMENT: 100% preserve the exact shape, natural luster, organic baroque irregularities, size, and pearl arrangement "
        "of the necklace and its distinctive baroque pearl pendant exactly as seen in the reference image. "
        "The necklace must be naturally and elegantly resting on her neck and collarbones. "
        "Soft, diffused natural daylight, high-end editorial lighting, ultra-sharp jewelry details, 8k resolution, photorealistic."
    )

    print("Отправка запроса в Gemini API (gemini-2.5-flash-image)...")
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt, ref_image]
    )

    generated_image_bytes = None
    for candidate in response.candidates:
        if not candidate.content or not candidate.content.parts:
            continue
        for part in candidate.content.parts:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                generated_image_bytes = part.inline_data.data
                break
            elif getattr(part, "data", None):
                generated_image_bytes = part.data
                break

    if not generated_image_bytes:
        print("В ответе модели не найдено изображение.")
        sys.exit(1)

    print("Обработка и сохранение изображения в формате WebP...")
    img = Image.open(io.BytesIO(generated_image_bytes))
    img.save(output_path, "WEBP", quality=90, method=6)

    print(f"УСПЕХ! Изображение сгенерировано и сохранено: {output_path.resolve()}")
    print(f"Разрешение: {img.size[0]}x{img.size[1]} px")

if __name__ == "__main__":
    main()
