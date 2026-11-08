# Отчёт по задаче 001 · Волна 0: риски и поломки

**От:** Antigravity · **Кому:** Claude, Леонид · **Дата:** 08.11.2026  
**Статус:** Готово к приёмке (все инварианты соблюдены, тесты 45/45 PASS, билд 10/10 OK)  
**Коммит:** `3b4e6e2` (`feat(task-001): resolve wave 0 critical risks (reviews, ItemList, kz-cart, scroll lock, filters)`)

---

## 1. Выполненные работы по пунктам

### A4. Скрипт AUTOPILOT
- **Статус:** Отменён Леонидом и Claude (зафиксировано в `docs/tasks/900-otlozheno-reklama-i-trekking.md` и `docs/tasks/001-volna0-riski-i-polomki.note-a4.md`).
- Файлы в папке `marketing/google_ads/` сохранены в оригинальном боевом виде без изменений.

---

### D1. Сгенерированные отзывы
- **Что сделано:**
  1. Полностью удалены генераторы фиктивных отзывов `REVIEWS_POOL`, `REVIEWS_POOL_KZ`, `REVIEWS_POOL_UZ` и функции детерминированной подстановки `get_deterministic_reviews()` из всех генераторов кодовой базы:
     - `scripts/generate_product_pages.py` (RU карточки товаров)
     - `scripts/generate_seo_hubs.py` (21 кластерный SEO-хаб)
     - `scripts/generate_kz_pages.py` (KZ карточки товаров и витрина)
     - `scripts/generate_uz_pages.py` (UZ карточки товаров и витрина)
  2. Удалены визуальные блоки аккордеонов «Отзывы покупателей», фиктивные бейджи «✓ Проверенный покупатель», «✓ Расталған сатып алушы», «✓ Tasdiqlangan xaridor» и шаблонная фраза «Модель «…» превзошла все ожидания».
  3. Из микроразметки Schema.org (`Product` JSON-LD) полностью удалены сгенерированные свойства `aggregateRating` и `review`.
  4. Создан файл `reviews.json` в корне проекта (массив реальных отзывов: `author`, `city`, `date`, `text`, `source`, `product_id`).
  5. Реализован механизм: если `reviews.json` пуст (`[]`) или для товара нет записей — аккордеон с отзывами в HTML не выводится, разметка `aggregateRating` и `review` в JSON-LD отсутствует. Если в `reviews.json` появятся реальные отзывы, они автоматически отрендерится с корректным подсчетом рейтинга.
  6. В `scripts/verify_audit.py` инвариант 20 переработан: проверяет отсутствие строки «Проверенный покупатель», отсутствие `aggregateRating` и отсутствие `review` при пустом `reviews.json`.

---

### D2. Строка категорий на мобильном
- **Что сделано:**
  1. В `styles.css`:
     - В блоке `.filters` заменено `justify-content: center` на `justify-content: flex-start;`.
     - В блоке `/* Catalog Filter Tabs (Single-line horizontal scroll) */` `.filters` установлены свойства `justify-content: flex-start;`, `padding: 6px 16px; padding-inline: 16px;`.
     - Теперь на экранах смартфонов (≤ 375 px) кнопки «Все» и «Колье» не смещаются за левую границу в отрицательные координаты flex-контейнера и остаются полностью доступными для горизонтальной прокрутки.
  2. В `shop.html` в функцию `renderFilters()` добавлено автоцентрирование активной кнопки:
     ```javascript
     const activeBtn = filters.querySelector('.tag.active');
     if (activeBtn) {
       try { activeBtn.scrollIntoView({ inline: 'center', block: 'nearest' }); } catch(e) {}
     }
     ```

---

### T-P0.1. Невалидный ItemList / Product
- **Что сделано:**
  1. В структуре Schema.org `ItemList` исправлено несоответствие спецификации Google Rich Results: свойства `offers`, `sku`, `mpn`, `brand`, `image`, `description` перенесены со `ListItem` во вложенный объект `item: {"@type": "Product", ...}`.
  2. Исправление применено во всех каталогах и генераторах:
     - `shop.html` (в статическом скрипте `#shopItemListLd` и генераторе `sync_static_catalogs`)
     - `kz/shop.html` (`scripts/generate_kz_pages.py`)
     - `uz/shop.html` (`scripts/generate_uz_pages.py`)
     - Все 21 кластерный SEO-хаб (`scripts/generate_seo_hubs.py` -> `build_product_schema_for_itemlist`)
  3. Теперь каждый элемент списка имеет валидный вид:
     ```json
     {
       "@type": "ListItem",
       "position": 1,
       "url": "https://livijewelry.kz/product/prod_01.html",
       "item": {
         "@type": "Product",
         "name": "...",
         "image": "...",
         "description": "...",
         "sku": "prod_01",
         "mpn": "prod_01",
         "brand": { "@type": "Brand", "name": "Livi Jewelry" },
         "offers": { ... }
       }
     }
     ```

---

### T-P0.2. /kz/cart.html на русском
- **Что сделано:**
  1. В `scripts/generate_kz_pages.py` исправлена процедура сборки страницы `kz/cart.html`.
  2. Замена `<title>` и `<h1>` переведена на надёжные регулярные выражения:
     - `<title data-i18n="meta.title">Livi Jewelry — Себет</title>`
     - `<h1 data-i18n="page.title">Себет</h1>`
  3. В собранном файле `kz/cart.html` теги `<title>` и `<h1>` отображаются на казахском языке («Себет»).

---

### T-P0.4. Прокрутка фона под меню и модалками
- **Что сделано:**
  1. В `styles.css` добавлены строгие правила изоляции скролла:
     ```css
     html.drawer-open,
     body.drawer-open,
     html.modal-open,
     body.modal-open {
       overflow: hidden !important;
       touch-action: none;
     }

     .storefront-menu,
     .drawer-panel,
     .drawer,
     .modal-card,
     .modal-content,
     .modal-inner {
       overscroll-behavior: contain;
     }
     ```
  2. В `scripts/storefront-menu.js`:
     - Добавлено сохранение позиции `savedScrollY = window.scrollY || window.pageYOffset || 0` перед открытием шторки.
     - Класс `drawer-open` добавляется одновременно на `document.documentElement` и `document.body`.
     - При закрытии меню класс удаляется и позиция скролла восстанавливается `window.scrollTo(0, savedScrollY)`.
     - Предотвращено случайное прокручивание страницы под открытым меню на iOS Safari и Android Chrome.

---

## 2. Результаты верификации и сборки

1. **Оркестратор сборки `python build_all.py`**:
   - Шаг 0/10: WebP 750w (85 изображений актуальны)
   - Шаг 1/10: RU карточки товаров и витрины пререндерены
   - Шаг 2/10: 21 SEO-хаб (RU, KZ, UZ) собраны
   - Шаг 3/10: KZ витрина и карточки собраны
   - Шаг 4/10: UZ витрина и карточки собраны
   - Шаг 5/10: Google Shopping feed.xml (85 товаров)
   - Шаг 6/10: Kaspi XML и CSV (85 товаров)
   - Шаг 7/10: 2ГИС XML и CSV (85 товаров)
   - Шаг 8/10: Pinterest CSV и XML (74 товара)
   - Шаг 9/10: sitemap.xml (297 URL)
   - Шаг 10/10: `verify_audit.py` (45 инвариантов) — **PASS**
   - Время полного прогона: 15.36с, код выхода: 0.

2. **Тестовый комплекс `python scripts/verify_audit.py`**:
   - `45/45 PASS`, 0 Errors.
   - Инвариант 20 успешно подтвердил отсутствие фейковых отзывов и отсутствие `aggregateRating` при пустом `reviews.json`.

3. **Специальный скрипт валидации Wave 0**:
   - Подтверждено отсутствие «Проверенный покупатель», `aggregateRating` и `review` во всех карточках и хабах.
   - Подтверждена вложенность `item: Product` в `ItemList` на главной витрине, KZ, UZ и хабах.
   - Подтвержден заголовок «Себет» в `kz/cart.html`.
   - Подтверждено правило блокировки скролла и `justify-content: flex-start` в `styles.css`.

---

## 3. Что не получилось и почему
- Все задачи в рамках скоупа 001 выполнены на 100%, блокеров нет.

---

## 4. Вопросы и информация для Леонида и Claude

1. **Реальные отзывы (`reviews.json`)**:
   Механизм полностью готов. Как только появятся реальные отзывы (из WhatsApp, 2ГИС, Google Карт), их можно добавить в `reviews.json` в формате:
   ```json
   [
     {
       "author": "Мадина С.",
       "city": "Алматы",
       "date": "2026-03-20",
       "text": "Прекрасное колье, качество жемчуга превосходное!",
       "rating": 5,
       "source": "2gis",
       "product_id": "prod_01"
     }
   ]
   ```
   После этого при очередной сборке отзывы автоматически появятся на карточках соответствующих товаров в виде аккордеона и попадут в микроразметку Schema.org.

2. **Готовность к Волне 1**:
   Готовы приступать к следующей задаче: `002-volna1-trekking-i-skorost.md` (скорость первого экрана, hero `srcset`/`preload`, удаление задержек fade-in).
