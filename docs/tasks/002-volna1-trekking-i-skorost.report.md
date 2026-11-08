# Отчёт по задаче 002 · Волна 1: скорость первого экрана

**Автор:** Antigravity  
**Дата:** 08.11.2026  
**Хэш коммита реализации:** `146cbae`  
**Статус:** Выполнено (100%)

---

## 1. Что сделано по каждому пункту

### T-P0.3. Hero без srcset и preload
1. **Генерация мобильной версии 750w**:
   - Обновлен генератор `scripts/generate_mobile_images.py`: добавлен список `EXTRA_IMAGES` для автономных медиа-ассетов (обложек витрин и баннеров).
   - Сгенерирована оптимизированная версия `/assets/hero-kole-iz-naturalnogo-zhemchuga-80000-750w.webp` (750×1000 px, WebP quality 82, method 6). Вес файла уменьшен в 2 раза: с 94 КБ до 47 КБ.
2. **Preload и адаптивная доставка в `index.html`**:
   - В секцию `<head>` добавлен тег предварительной загрузки мобильного LCP:
     ```html
     <link rel="preload" as="image" href="/assets/hero-kole-iz-naturalnogo-zhemchuga-80000-750w.webp" imagesrcset="/assets/hero-kole-iz-naturalnogo-zhemchuga-80000-750w.webp 750w, /assets/hero-kole-iz-naturalnogo-zhemchuga-80000.webp 1440w" imagesizes="(max-width: 768px) 100vw, 1440px" fetchpriority="high">
     ```
   - Тег `img.storefront-cover-photo` оснащен адаптивным набором `srcset`, `sizes`, `fetchpriority="high"`, `loading="eager"`, `decoding="async"` и расширенным атрибутом `alt="Колье с барочной подвеской — Livi Jewelry"`.
   - В блоке меню (`storefront-menu-feature`) десктопное изображение переведено на версию 750w с валидным alt-текстом `alt="Барочный жемчуг"`.
3. **Preload для LCP на страницах каталога и языковых версиях**:
   - В `shop.html`, `kz/shop.html`, `uz/shop.html`, `kz/index.html`, `uz/index.html` в `<head>` добавлен тег `<link rel="preload" as="image">` для первого отображаемого товара каталога (`/assets/kole-iz-naturalnogo-zhemchuga-80000-750w.webp`), являющегося фактическим LCP-элементом на этих витринах.
   - Генераторы `scripts/generate_kz_pages.py` и `scripts/generate_uz_pages.py` обновлены — теги preload и адаптивные srcset встроены в шаблоны витрин.

---

### D10. Fade-in и задержки у первых карточек (серые плашки)
1. **Отключение анимаций и переходов в CSS**:
   - В `styles.css` для первых 8 карточек сетки каталога и витрин добавлены жесткие правила:
     ```css
     /* D10: Disable fade-in and transition delay for first 8 cards above the fold (prevents gray placeholder lag) */
     .grid > .card:nth-child(-n+8),
     .storefront-featured .card:nth-child(-n+8) {
       opacity: 1 !important;
       animation: none !important;
       transition: none !important;
     }

     .grid > .card:nth-child(-n+8) .card-img-wrap,
     .storefront-featured .card:nth-child(-n+8) .card-img-wrap {
       animation: none !important;
     }

     .grid > .card:nth-child(-n+8) img,
     .storefront-featured .card:nth-child(-n+8) img {
       animation: none !important;
     }

     .grid > .card:nth-child(-n+8):hover img,
     .storefront-featured .card:nth-child(-n+8):hover img {
       transition: transform 0.75s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
     }
     ```
     Это полностью устраняет 0.3s переход прозрачности и любые анимационные лаги при первичном рендеринге карточек первого и второго экранов смартфона.
2. **Eager loading для первых 8 карточек**:
   - Ранее только первые 4 карточки (`idx < 4`) загружались с `loading="eager"`, а карточки 5–8 имели `loading="lazy"`, что вызывало показ фоновых серых плашек (`#F3EFE9`) при быстрой прокрутке на смартфонах.
   - Порог увеличен до 8 карточек (`idx < 8`):
     - Карточки 1–2 (первый ряд смартфона / LCP): `loading="eager" fetchpriority="high"`
     - Карточки 3–8 (ряды 2–4 смартфона): `loading="eager"` (без блокировки приоритета браузера)
     - Карточки 9+ (ниже 4-го экрана): `loading="lazy"`
   - Обновление синхронизировано во всех генераторах и страницах:
     - `shop.html` (статическая сетка и динамический JavaScript `renderGrid()`)
     - `scripts/generate_product_pages.py` (`build_static_card_html`)
     - `scripts/generate_kz_pages.py` (`build_kz_card_html`)
     - `scripts/generate_uz_pages.py` (`build_uz_card_html`)
     - `scripts/generate_seo_hubs.py` (21 SEO-кластер)
     - Топ-3 статических хаба (`kolye-iz-zhemchuga.html`, `braslety-iz-zhemchuga.html`, `sergi-iz-zhemchuga.html`)

---

### Аналитика и трекинг (уточнение)
- Скрипты аналитики (gtag Google Ads `AW-16793974126`, GA4 `G-YFF2TR0N36`, Meta Pixel) оставлены в неизменном виде в `<head>`.
- Логика событий не менялась, перенос за `load` не производился per `900-otlozheno-reklama-i-trekking.md`.

---

## 2. Что не получилось и почему
- Все запланированные пункты выполнены в полном объеме, блокеров не возникло.

---

## 3. Результаты тестов и верификации
1. **`python scripts/verify_audit.py`**:
   - **45 из 45 инвариантов PASS** (0 ошибок).
2. **`python build_all.py`**:
   - Все 10 шагов конвейера сборки успешно пройдены (20.18 с).
3. **Проверка DOM**:
   - В `index.html` и `shop.html` теги `<link rel="preload">` и `srcset` корректно подключены.
   - Первые 8 карточек отдаются с `loading="eager"` и `opacity: 1 !important`.

---

## 4. Вопросы к Леониду или Claude
- Вопросов нет. Скорость отображения первого экрана и карточек на мобильных устройствах оптимизирована. Готов переходить к следующей задаче согласно `docs/tasks/README.md` (003 · Волна 2: карточка, мини-корзина, корзина, удобство на телефоне) по готовности ТЗ.
