import os
from pathlib import Path
from PIL import Image

# Directory containing assets
ASSETS_DIR = Path(__file__).parent / "assets"

# Supported image extensions
EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg"}

# Quality settings (0‑100) – lower => smaller size
WEBP_QUALITY = 70  # adjust as needed
JPEG_QUALITY = 70
PNG_OPTIMIZE = True

def compress_image(image_path: Path):
    try:
        with Image.open(image_path) as im:
            # Preserve original format
            fmt = im.format
            if fmt == "WEBP":
                im.save(image_path, "WEBP", quality=WEBP_QUALITY, method=6)
            elif fmt in {"JPEG", "JPG"}:
                im.save(image_path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
            elif fmt == "PNG":
                im.save(image_path, "PNG", optimize=PNG_OPTIMIZE)
            else:
                print(f"Skipping unsupported format: {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def main():
    if not ASSETS_DIR.is_dir():
        print(f"Assets directory not found: {ASSETS_DIR}")
        return
    for root, _, files in os.walk(ASSETS_DIR):
        for name in files:
            p = Path(root) / name
            if p.suffix.lower() in EXTENSIONS:
                print(f"Compressing {p.relative_to(ASSETS_DIR.parent)}")
                compress_image(p)

if __name__ == "__main__":
    main()
