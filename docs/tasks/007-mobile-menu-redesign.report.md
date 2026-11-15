# Отчёт по задаче 007 — Новое мобильное меню

**Статус:** Выполнено · **Дата:** 12.11.2026  
**Исполнитель:** Antigravity  
**Файл задачи:** [007-mobile-menu-redesign.md](file:///d:/Livi_jewelry%20(Antigravity)/docs/tasks/007-mobile-menu-redesign.md)  
**Макет Claude:** https://claude.ai/artifact/KX9oHaotCiDhVDnYtA6huY (390 px)

---

## 1. Что сделано

1. **Единый генератор мобильного меню (`scripts/generate_mobile_menu.py`)**:
   - Реализована строгая структура меню в точном соответствии с макетом Claude:
     1. **Шапка 58 px:** кнопка закрытия (×, 44×44, `aria-label="Закрыть меню"` / localized), логотип `LIVI JEWELRY`, поиск (44×44, `aria-label="Поиск по каталогу"`), корзина (44×44, `aria-label="Корзина"`) с живым синхронизируемым бейджем `.cart-badge`. Нижняя граница 1 px `#E8E2D8`.
     2. **Подпись «УКРАШЕНИЯ»:** 11 px, font-weight 600, `letter-spacing: .2em`, цвет `--gold-text` (`#85693F`).
     3. **5 категорий:** Колье, Серьги, Браслеты, Комплекты, Кольца и сеты. Высота строки 56 px, Cormorant Garamond 27 px font-weight 500, шеврон 18 px (`#9A9389`), разделитель 1 px `#E8E2D8`.
     4. **Кнопка «ВЕСЬ КАТАЛОГ →»:** 48 px, рамка 1 px `#1F1D1A`, без заливки, 12 px 600 `.16em`, отступ сверху 20 px.
     5. **«ЕЩЁ КАТЕГОРИИ»:** горизонтальный ряд pill-кнопок (44 px, r22, border `#DCD5C9`, bg `#FFF`, 14 px, `overflow-x: auto`, скроллбар скрыт, отступы по краям 24 px, эффект обрезки края экрана).
     6. **«ПО КАМНЮ»:** горизонтальный ряд pill-кнопок со всеми 13 минералами каталога. Каждая таблетка содержит цветную точку 16 px:
        - Жемчуг: `#EDE6DA` + border `#D8CFC0`
        - Гематит: `#4A4A4F`
        - Малахит: `#2F7A55`
        - Аметист: `#8A6BA8`
        - Гранат: `#7A1F2B`
        - Розовый кварц: `#E9C3C6`
        - Бирюза: `#5FB3AE`
        - Горный хрусталь: `#E4E9EE` + border `#D8CFC0`
        - Лунный камень: `#DCE6EC` + border `#C5D2DB`
        - Жемчуг Майорка: `#EDE6DA` + border `#D8CFC0`
        - Тигровый глаз: `#9E6738`
        - Коралл и Яшма: `#C2553F`
        - Лазурит: `#2A4B8D`
     7. **Разделитель:** 1 px `#E8E2D8`, отступ сверху 32 px.
     8. **Служебные ссылки (48 px, 15 px, иконки 20 px `--gold-text`):**
        - «Доставка и оплата» (иконка грузовика)
        - «Магазин в Астане» (иконка пина, ссылка `https://maps.app.goo.gl/yrLFpFFKjz9kE1GHA`, `target="_blank" rel="noopener"`)
     9. **2 кнопки соцсетей (сетка 2 колонки, 48 px):**
        - WhatsApp (bg `#2B2620`, цвет `#FFF`, иконка WhatsApp, сохранена аналитика и предзаполненный текст)
        - Instagram (bg `#FFF`, border `#DCD5C9`, иконка Instagram)
     10. **Переключатель языка:** полноширинный сегмент 44 px, r22, border `#DCD5C9`. 3 равные части: RU / KZ / UZ. Активный язык выделен `#1F1D1A`, белый текст, `aria-current="true"`. Ссылки ведут строго на эквивалентные страницы текущего раздела/товара.
     11. **Контакты в футере (12 px, `#6B665F`):** «Астана, пр. Кабанбай Батыра, 43» и кликабельный телефон `+7 705 451 05 84` (`tel:+77054510584`).

2. **Адаптивность и изоляция (`styles.css`)**:
   - Десктопная шапка (`min-width: 769px`): меню полностью скрыто (`display: none !important`), поведение и выпадающие меню десктопа не затронуты.
   - Мобильная версия (`max-width: 768px`): меню занимает 100% ширины экрана (`width: 100vw; max-width: 100vw; inset: 0; position: fixed; background: #F9F7F3;`), полоска hero-фото справа полностью отсутствует.
   - Скроллбар на горизонтальных рядах скрыт кроссбраузерно (`scrollbar-width: none; -ms-overflow-style: none; &::-webkit-scrollbar { display: none }`).
   - Учтены безопасные зоны iPhone с вырезом (`env(safe-area-inset-top)`, `env(safe-area-inset-bottom)`).
   - Все кликабельные элементы ≥ 44 px.

3. **Интерактивность и доступность (`scripts/storefront-menu.js`)**:
   - Сохранены все фиксы задачи 006:
     * Блокировка фонового скролла при открытии меню (`drawer-open` на `html` и `body`).
     * Корректный возврат фокуса на кнопку открытия после закрытия меню.
     * Закрытие меню по клавише `Escape` и по клику на крестик.
     * Атрибут `aria-expanded` синхронизируется на кнопке открытия.
   - Автоматическая синхронизация бейджа корзины (`.cart-badge` и `.smm-cart-badge`) при загрузке и событии `storage`.

4. **Охват страниц и генераторы**:
   - `scripts/patch_static_pages.py`: обновлены корневые страницы `index.html`, `shop.html`, `delivery.html`, `cart.html`, `privacy.html`, `terms.html`, `404.html`.
   - `scripts/generate_product_pages.py`: протестированы и обновлены все 91 RU карточки товаров `/product/prod_XX.html`.
   - `scripts/generate_seo_hubs.py`: интегрирован новый хедер на всех 21 хабах RU, 21 хабах KZ и 21 хабах UZ.
   - `scripts/generate_kz_pages.py`: переведён с устаревшего drawer на единый `render_full_storefront_header("kk", ...)` для `kz/index.html`, `kz/shop.html`, 91 карточки в `kz/product/`, `kz/delivery.html`, `kz/terms.html`, `kz/privacy.html`, `kz/cart.html`.
   - `scripts/generate_uz_pages.py`: переведён с устаревшего drawer на единый `render_full_storefront_header("uz", ...)` для `uz/index.html`, `uz/shop.html`, 91 карточки в `uz/product/`, `uz/delivery.html`, `uz/terms.html`, `uz/privacy.html`, `uz/cart.html`.

5. **Тестирование и валидация**:
   - Скрипт полного цикла `python build_all.py` завершился успешно за 24.15с.
   - `scripts/verify_audit.py`: все 48 из 48 тестов инвариантов пройдены (PASS).
   - `tests/test_mobile_menu_visual.py`: успешно выполнены сквозные тесты в движке Safari (WebKit) на iPhone 13 (390 px) и iPhone SE (375 px). Проверены отсутствие горизонтального переполнения (`scrollWidth <= 375`), блокировка скролла, скрытие/показ, и чистота локализации KZ и UZ (0 русских строк).

---

## 2. Итоговые переводы новых строк

| RU | KZ (Қазақша) | UZ (O‘zbekcha) |
|---|---|---|
| **УКРАШЕНИЯ** | **ӘШЕКЕЙЛЕР** | **TAQINCHOQLAR** |
| Колье | Алқалар | Marjonlar |
| Серьги | Сырғалар | Ziraklar |
| Браслеты | Білезіктер | Bilaguzuklar |
| Комплекты | Жиынтықтар | To‘plamlar |
| Кольца и сеты | Сақиналар мен сеттер | Uzuklar va to‘plamlar |
| **ВЕСЬ КАТАЛОГ →** | **БАРЛЫҚ КАТАЛОГ →** | **BARCHA KATALOG →** |
| **ЕЩЁ КАТЕГОРИИ** | **БАСҚА САНАТТАР** | **BOSHQA TOIFALAR** |
| Чокеры из камней | Тастардан жасалған чокерлер | Toshli chokerlar |
| Сотуары | Сотуарлар | Sotuarlar |
| Цепи с жемчугом | Інжуі бар шынжырлар | Marvaridli zanjirlar |
| **ПО КАМНЮ** | **ТАС БОЙЫНША** | **TOSH BO‘YICHA** |
| Доставка и оплата | Жеткізу және төлем | Yetkazib berish va to‘lov |
| Магазин в Астане | Астанадағы дүкен | Ostonadagi do‘kon |
| Астана, пр. Кабанбай Батыра, 43 | Астана қ., Қабанбай батыр даңғ., 43 | Ostona sh., Qabanbay botir shoh ko‘ch., 43 |

---

## 3. Скриншоты проверки (Safari WebKit)

Скриншоты сгенерированы в тестовом сьюте `tests/test_mobile_menu_visual.py` через Safari (Playwright WebKit) с реальным рендерингом стилей и шрифтов:

1. **RU меню (375 px, iPhone SE)**:  
   `C:/Users/user/.gemini/antigravity/brain/52d6a95c-9271-4d9b-8ac3-cca6d0eba04c/menu_ru_375px.png`
2. **RU меню с прокрученным рядом камней (375 px)**:  
   `C:/Users/user/.gemini/antigravity/brain/52d6a95c-9271-4d9b-8ac3-cca6d0eba04c/menu_ru_stones_scrolled_375px.png`
3. **RU меню на 390 px (iPhone 13)**:  
   `C:/Users/user/.gemini/antigravity/brain/52d6a95c-9271-4d9b-8ac3-cca6d0eba04c/menu_ru_390px.png`
4. **KZ меню (375 px)**:  
   `C:/Users/user/.gemini/antigravity/brain/52d6a95c-9271-4d9b-8ac3-cca6d0eba04c/menu_kz_375px.png`
5. **UZ меню (375 px)**:  
   `C:/Users/user/.gemini/antigravity/brain/52d6a95c-9271-4d9b-8ac3-cca6d0eba04c/menu_uz_375px.png`

---

## 4. Список изменённых и созданных файлов

### Новые файлы
- `scripts/generate_mobile_menu.py` — единый генератор HTML-компонентов меню и шапки для 3 языков.
- `scripts/patch_static_pages.py` — утилита внедрения единого хедера в корневые статические файлы.
- `tests/test_mobile_menu_visual.py` — автотест визуального отображения, скролла и локализации на Safari WebKit (375px / 390px).
- `docs/tasks/007-mobile-menu-redesign.report.md` — настоящий отчёт.

### Изменённые шаблоны и генераторы
- `styles.css` — добавлены стили для `.storefront-mobile-menu`, скрытие на десктопе (`display: none !important`), стили горизонтальных скролл-рядов, цветных точек камней, кнопок и переключателя языков.
- `scripts/storefront-menu.js` — поддержка кнопки закрытия `.smm-close-btn`, синхронизация `.smm-cart-badge`, обработка клавиатуры и блокировка скролла через класс `drawer-open`.
- `scripts/generate_seo_hubs.py` — импорт `render_full_storefront_header` и подключение нового мобильного меню ко всем 63 страницам кластеров (21 RU, 21 KZ, 21 UZ).
- `scripts/generate_kz_pages.py` — замена устаревшего drawer на `render_full_storefront_header("kk", ...)`, подключение `storefront-menu.js` во все разделы KZ.
- `scripts/generate_uz_pages.py` — замена устаревшего drawer на `render_full_storefront_header("uz", ...)`, подключение `storefront-menu.js` во все разделы UZ.
- `scripts/verify_audit.py` — актуализирован regex SKU под артикулы до 3 цифр (`LIVI-\d{2,3}`).
- `.gitignore` — добавлена маска `tests/fixtures/*.png`.

### Сгенерированные HTML-страницы (обновлены через `build_all.py`)
- Корневые RU страницы: `index.html`, `shop.html`, `delivery.html`, `cart.html`, `privacy.html`, `terms.html`, `404.html`.
- Все 21 кластерный SEO-хаб на RU, KZ, UZ.
- Все 91 карточки товаров RU (`product/prod_XX.html`), 91 карточки KZ (`kz/product/prod_XX.html`), 91 карточки UZ (`uz/product/prod_XX.html`).
- Сервисные страницы и корзины KZ и UZ (`kz/cart.html`, `uz/cart.html`, `kz/delivery.html`, `uz/delivery.html`, etc.).

---

## 5. Чек-лист критериев приёмки

- [x] На 375 и 390 px меню выглядит как макет: 3 уровня текста, одинаковые строки категорий, ряды таблеток листаются вбок.
- [x] Ни один элемент не выходит за левый край (`scrollWidth <= 375` подтверждено тестом).
- [x] Меню перекрывает весь экран на 100vw, фон под ним не прокручивается (класс `drawer-open`).
- [x] Все ссылки ведут на правильные страницы; языковой переключатель переводит на ту же страницу в другом языке.
- [x] Трекинг WhatsApp и Instagram сохранён без изменений (`whatsapp_click`, `contact`, `generate_lead` с сохранением URL-параметров и текстов).
- [x] RU, KZ, UZ проверены; на KZ и UZ отсутствуют русские строки (подтверждено тестом).
- [x] Проверено в Safari на iPhone (Playwright WebKit, iPhone 13 и iPhone SE).
- [x] Все 48 тестов технического аудита и SEO-инвариантов (`verify_audit.py`) пройдены успешно (48/48 PASS).

---

## 6. Вопросы к Леониду

1. Проверить перевод названия магазина в узбекской версии: **«Ostonadagi do‘kon»** (г. Астана по-узбекски традиционно пишется как *Ostona*). Если предпочтительнее форма *«Astanadagi do‘kon»*, заменим в одном месте словаря `scripts/generate_mobile_menu.py`.
