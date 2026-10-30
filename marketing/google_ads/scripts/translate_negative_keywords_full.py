# translate_negative_keywords_full.py
"""
Перевод полного списка минус‑слов из CSV (UTF‑16 LE) в узбекский язык.

Исходный файл:  "GOOGLE ADS ОТЧЕТЫ/полный список минус слов.csv"
Результат:      "GOOGLE ADS ОТЧЕТЫ/полный список минус слов_uz.csv"

Требования:
  - Python 3.10+
  - pip пакеты: pandas, googletrans==4.0.0rc1

Запуск:
  python translate_negative_keywords_full.py
"""

import pathlib, sys
import pandas as pd
from googletrans import Translator

# ---------- Конфигурация ----------
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent / "reports"
SRC_FILE = BASE_DIR / "GOOGLE ADS ОТЧЕТЫ" / "полный список минус слов.csv"
DST_FILE = BASE_DIR / "GOOGLE ADS ОТЧЕТЫ" / "полный список минус слов_uz.csv"
SRC_LANG = "ru"
DST_LANG = "uz"
# ----------------------------------

def main() -> None:
    if not SRC_FILE.exists():
        sys.exit(f"[❌] Не найден файл: {SRC_FILE}")
    print("[▶️] Читаем CSV (utf‑16)…")
    df = pd.read_csv(SRC_FILE, encoding="utf-16", dtype=str)
    # Определяем колонку с ключевыми словами (обычно 'Keyword')
    keyword_col = next((c for c in df.columns if "keyword" in c.lower()), None)
    if not keyword_col:
        sys.exit(f"[❌] В файле нет колонки Keyword. Есть: {list(df.columns)}")
    translator = Translator()
    translated = []
    print("[⚙️] Переводим… (может занять несколько минут)")
    for i, txt in enumerate(df[keyword_col]):
        txt = str(txt) if pd.notna(txt) else ""
        if txt:
            try:
                translated.append(translator.translate(txt, src=SRC_LANG, dest=DST_LANG).text)
            except Exception as e:  # pragma: no cover
                print(f"[⚠️] Ошибка перевода строки {i+2}: {e}")
                translated.append(txt)
        else:
            translated.append(txt)
        if (i + 1) % 500 == 0:
            print(f"   …{i + 1}/{len(df)}")
    df[keyword_col] = translated
    print("[💾] Записываем результат в UTF‑8 (BOM)…")
    df.to_csv(DST_FILE, index=False, encoding="utf-8-sig")
    print(f"[✅] Готово: {DST_FILE}")

if __name__ == "__main__":
    main()
