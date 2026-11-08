# 001 · Волна 0: риски и поломки

**От:** Claude · **Кому:** Antigravity · **Срок:** сегодня, до 07:00 09.11 · **Утверждено:** Леонид, 08.11.2026

> Протокол: см. `docs/tasks/README.md`. Отчёт по этой задаче — **новым файлом** `docs/tasks/001-volna0-riski-i-polomki.report.md` (этот файл не редактировать). Контекст при необходимости: `docs/agent-handoff.md` (архив), но всё нужное для задачи — ниже.

Самое срочное для дизайна и SEO: то, что может привести к санкциям Google, ломает разметку для роботов Google или мешает покупке на телефоне.

> A4 (скрипт AUTOPILOT) отменён: скрипт не трогаем. Рекламу и трекинг сейчас не делаем — см. `900-otlozheno-reklama-i-trekking.md`.

## D1. Сгенерированные отзывы
**D1. Убрать сгенерированные отзывы.** `scripts/generate_product_pages.py`: `REVIEWS_POOL`, `get_deterministic_reviews()` подставляют каждому товару 2 отзыва из общего пула и «5–24 оценки» с пометкой «✓ Проверенный покупатель»; имена повторяются между товарами, текст заканчивается шаблоном «Модель «…» превзошла все ожидания». Это же уходит в JSON-LD `Review` + `aggregateRating` (на `kolye-iz-zhemchuga.html` 6 aggregateRating и 12 Review). Риск: ручные меры Google за спам в структурированных данных, блокировка Merchant Center за искажение информации.
- Удалить аккордеон «Отзывы покупателей», `reviews_cards_html`, `aggregateRating` и `review` из карточек и хабов (`generate_seo_hubs.py`), KZ/UZ генераторов.
- Оставить механизм под **реальные** отзывы: `reviews.json` (автор, город, дата, текст, источник: google/2gis/whatsapp, `product_id` или общий). Пусто → блок не выводится, разметки нет.
- Добавить в `verify_audit.py` инвариант: в собранных HTML нет строки «Проверенный покупатель» и нет `aggregateRating`, если `reviews.json` пуст.

## D2. Строка категорий на мобильном
**D2. Строка категорий на мобильном.** В `shop.html` (и `/kz/`, `/uz/`) `.filters` центрируется, при 375 px кнопки «Все» и «Колье» получают left −85 и −42 px и недоступны для прокрутки. На мобильном `justify-content: flex-start` (или `safe center`), `padding-inline` 16 px, при загрузке `scrollIntoView({inline:'center'})` для активной кнопки.

## T-P0.1. Невалидный ItemList / Product
В `ItemList` свойства `offers`, `sku`, `mpn` сейчас висят на `ListItem`. Перенести во вложенный `item: {"@type": "Product", name, image, offers}`. Файлы: `shop.html`, `kz/shop.html`, хабы и их генераторы.

## T-P0.2. /kz/cart.html на русском
`<title>` и `<h1>` «Корзина» → «Себет» (`scripts/generate_kz_pages.py`).

## T-P0.4. Прокрутка фона под меню и модалками
`body.drawer-open`, `body.modal-open` → блокировать прокрутку документа (`overflow: hidden` на `html` + сохранение позиции, `overscroll-behavior: contain` у панели). `styles.css`, `scripts/storefront-menu.js`.

## Готово, когда
- `python build_all.py` и `python scripts/verify_audit.py` проходят без ошибок.
- Изменения задеплоены (коммит + push), в отчёте — хэш коммита.
- В отчёте: что сделано по каждому пункту, что не получилось и почему, вопросы к Леониду или Claude.
