# 900 · Отложено: реклама и трекинг

**От:** Claude · **Дата:** 08.11.2026 · **Статус:** НЕ ДЕЛАТЬ, пока Леонид не скажет

Решение Леонида 08.11: сейчас работаем только над дизайном и SEO (индексация и выдача Google). Скрипт AUTOPILOT не трогаем. Задачи ниже сохранены, чтобы не потерять, — к ним вернёмся отдельной задачей.

**A1. Честная конверсия WhatsApp (P0)** — `shop.html`, `index.html`, `cart.html` + генераторы (`scripts/generate_product_pages.py`, `scripts/generate_kz_pages.py`, `scripts/generate_uz_pages.py`), везде где есть кнопки WhatsApp.
- На **любом** клике WhatsApp (модалка товара, главная, корзина, плавающая кнопка): ровно **одна** отправка `gtag('event','conversion',{send_to:'AW-16793974126/dLz3CKyagbAdEO7q_sc-', value: <цена товара/корзины в KZT>, currency:'KZT'})` + GA4 `generate_lead` и `whatsapp_click` + Meta `Lead`/`Contact`.
- **Удалить** на кликах WhatsApp: GA4 `purchase`, Ads-вызовы с `MuJ_CObHup8bEO7q_sc-`, Meta `Purchase`. Это не покупки, а начало диалога.
- Ценность: передавать реальную сумму товара/корзины в KZT, а не `1.0 USD`. Ads сам пересчитает в валюту аккаунта.
- Защита от дублей: один клик = одна отправка (debounce, флаг на элементе). Проверить, что на главной и в корзине не висят двойные обработчики.

**A2. Корзина (P0).** В `cart.html` при отправке формы заказа: GA4 `purchase` с `transaction_id: orderId` + `gtag('event','conversion',{send_to:'AW-16793974126/Xk1CCKDnu7QdEO7q_sc-', value: total, currency:'KZT', transaction_id: orderId})` + `user_data` (enhanced conversions уже есть, оставить). Старый `MuJ_…` убрать. Ярлык вынести в одну константу, чтобы KZ/UZ подхватывали через генераторы.

**A3. Код заказа в сообщении WhatsApp → связь с реальной оплатой (P0, главное для продаж).**
Сейчас gclid при заказе через WhatsApp теряется, и Ads никогда не узнает, кто реально купил.
- При клике на WhatsApp генерировать короткий код `LV-XXXX` (4–5 символов) и вставлять его в предзаполненный текст: «…Мой код заказа: LV-7K3P».
- Одновременно отправлять на webhook (Apps Script, `navigator.sendBeacon`) строку: дата/время, код, товар, сумма, `gclid`/`gbraid`/`wbraid`, UTM, страница. Атрибуция уже собирается в `scripts/cart-core.js` (`livi_attribution`).
- В `scripts/google_apps_script_order_backend.js`: лист `WA_Leads` (код, время, товар, сумма, gclid, gbraid, wbraid, utm, статус). Статус («Оплачен» / «Не купил») и фактическую сумму вручную ставит менеджер, когда клиент оплатил в WhatsApp/Kaspi (ищет по коду из сообщения).
- Функция `buildOfflineConversions()` + ежедневный триггер: строки со статусом «Оплачен» и непустым gclid/gbraid/wbraid → лист `GoogleAds_Offline` в формате импорта Google Ads: `Google Click ID | Conversion Name = "Оплаченный заказ" | Conversion Time (yyyy-MM-dd HH:mm:ss+05:00) | Conversion Value | Conversion Currency = KZT`, без дублей. То же для заказов из корзины (лист заказов уже есть).
- `ORDER_WEBHOOK_URL` в `cart.html` сейчас `''` (и на проде тоже). Вынести в одну константу для RU/KZ/UZ. URL даст Леонид после развёртывания Apps Script как веб-приложения.
- Когда лист `GoogleAds_Offline` заработает, я подключу в Ads действие «Оплаченный заказ» (импорт из Google Таблиц по расписанию). После 15–30 оплат переведём кампании на «Максимум конверсий» с упором на оплаты.

**A6. Проверки перед фиксацией.** `python build_all.py` и `python scripts/verify_audit.py` (45/45). Плюс Tag Assistant на RU/KZ/UZ с `?gclid=TEST123`:
- клик WA → одна `dLz3…` с ценностью в KZT, `generate_lead`, никакого `purchase`; в листе `WA_Leads` появилась строка с кодом и gclid; код есть в тексте WhatsApp;
- оформление в корзине → `purchase` + `Xk1C…` с `orderId`; строка в листе заказов с gclid.

**A5. Структура Поиска KZ (P1)** — скрипт `marketing/google_ads/scripts/create_themed_ad_groups.js` по образцу `create_single_ad_group.js`: 6 тематических групп, каждая со своим хабом и своим RSA (15 заголовков ≤30 симв., 4 описания ≤90 симв.). Старую группу ставить на паузу после запуска (флаг `APPLY_CHANGES`). Ключи и ставки Леонид правит сам — скрипт только создаёт каркас.

| Группа | Конечный URL |
|---|---|
| Жемчуг: колье, бусы, сотуары | `/kolye-iz-zhemchuga.html` |
| Серьги с жемчугом | `/sergi-iz-zhemchuga.html` |
| Чокеры и колье из камней | `/chokery-iz-naturalnyh-kamney.html` |
| Украшения по камню | `/ukrasheniya-iz-<камень>.html` |
| Комплекты и подарки | `/komplekty-ukrasheniy.html` |
| Магазин / гео / казахские | `/shop.html` |
