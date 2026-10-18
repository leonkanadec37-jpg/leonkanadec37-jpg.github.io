import os
import json
from datetime import datetime
from xml.sax.saxutils import escape

SITE_URL = "https://livijewelry.kz"

STATIC_PAGES = [
    ("", "1.0", "daily"),
    ("shop.html", "0.9", "daily"),
    ("kolye-iz-zhemchuga.html", "0.85", "weekly"),
    ("braslety-iz-zhemchuga.html", "0.85", "weekly"),
    ("sergi-iz-zhemchuga.html", "0.85", "weekly"),
    # 12 коммерческих SEO-хабов (Этап 1)
    ("komplekty-ukrasheniy.html", "0.85", "weekly"),
    ("chokery-iz-naturalnyh-kamney.html", "0.85", "weekly"),
    ("sotuary-iz-zhemchuga.html", "0.85", "weekly"),
    ("ukrasheniya-iz-barochnogo-zhemchuga.html", "0.85", "weekly"),
    ("ukrasheniya-iz-gematita.html", "0.85", "weekly"),
    ("ukrasheniya-iz-malahita.html", "0.85", "weekly"),
    ("ukrasheniya-iz-ametista.html", "0.85", "weekly"),
    ("ukrasheniya-iz-granata.html", "0.85", "weekly"),
    ("ukrasheniya-iz-rozovogo-kvarca.html", "0.85", "weekly"),
    ("ukrasheniya-iz-biryuzy.html", "0.85", "weekly"),
    ("ukrasheniya-iz-gornogo-hrustalya.html", "0.85", "weekly"),
    ("ukrasheniya-iz-lunnogo-kamnya.html", "0.85", "weekly"),
    # Статическая казахскоязычная витрина (Этап 5)
    ("kz/", "0.85", "weekly"),
    ("kz/shop.html", "0.85", "weekly"),
    # Сервисные и информационные страницы
    ("delivery.html", "0.6", "monthly"),
    ("privacy.html", "0.3", "yearly"),
    ("terms.html", "0.3", "yearly"),
]


def generate_sitemap():
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    for page, prio, freq in STATIC_PAGES:
        url = f"{SITE_URL}/{page}" if page else f"{SITE_URL}/"
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")

    # Все карточки товаров: чистые статические URL /product/prod_XX.html + <image:image>
    if os.path.exists("products.json"):
        with open("products.json", "r", encoding="utf-8") as f:
            products = json.load(f)
        for p in products:
            if not p.get("inStock", True):
                continue
            pid = p["id"]
            url = f"{SITE_URL}/product/{pid}.html"
            img_rel = p.get("image", "").lstrip("/")
            img_loc = escape(f"{SITE_URL}/{img_rel}")
            title = escape(f"{p.get('title', '').strip()} — ручная работа Livi Jewelry")
            materials = ", ".join(p.get("materials") or ["натуральный жемчуг"])
            caption = escape(
                f"{p.get('title', '').strip()}. {p.get('description', '').strip()} Материалы: {materials}. Купить в Астане и Алматы с доставкой по Казахстану."
            )
            lines.append("  <url>")
            lines.append(f"    <loc>{url}</loc>")
            lines.append(f"    <lastmod>{today}</lastmod>")
            lines.append("    <changefreq>weekly</changefreq>")
            lines.append("    <priority>0.8</priority>")
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{img_loc}</image:loc>")
            lines.append(f"      <image:title>{title}</image:title>")
            lines.append(f"      <image:caption>{caption}</image:caption>")
            lines.append("    </image:image>")
            lines.append("  </url>")

    lines.append("</urlset>")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[OK] Sitemap обновлен ({len(STATIC_PAGES)} статических страниц/хабов + товары с <image:image>)")


if __name__ == "__main__":
    generate_sitemap()
