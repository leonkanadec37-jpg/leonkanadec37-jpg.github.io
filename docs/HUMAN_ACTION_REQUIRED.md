# Чек-лист для владельца Livi Jewelry (3 минуты после пробуждения)

Все технические исправления в коде, микроразметке `Schema.org`, страницах товаров `/product/prod_01.html`..`prod_28.html`, XML-фиде (`google_merchant_feed.xml` и `feed.xml`), `sitemap.xml`, `robots.txt` и тегах отслеживания Google Ads / GA4 уже **проверены автотестами (0 ошибок) и выгружены на рабочий сайт `https://livijewelry.kz/`**.

Ниже — 3 быстрых действия в личных кабинетах Google, которые требуют вашей авторизации в браузере (займут ~3 минуты):

---

## 1. Google Search Console (GSC) — Ускорить индексацию 28 страниц товаров (~1 минута)
1. Откройте [Google Search Console](https://search.google.com/search-console) для ресурса `https://livijewelry.kz/`.
2. Перейдите в раздел **Файлы Sitemap** (`Sitemaps`) в левом меню.
3. Введите `sitemap.xml` (полный адрес: `https://livijewelry.kz/sitemap.xml`) и нажмите **Отправить** (`Submit`), чтобы Googlebot мгновенно перечитал обновлённую карту сайта из 36 канонических страниц.
4. В верхней строке поиска GSC (**Проверка URL** / `URL Inspection`) вставьте 1–2 основные страницы:
   - `https://livijewelry.kz/shop.html`
   - `https://livijewelry.kz/product/prod_08.html`
   и нажмите **Запросить индексирование** (`Request Indexing`). Так как теперь в исходном HTML `shop.html` и `index.html` встроены прямые статические ссылки `<a href="/product/prod_XX.html">` на все 28 товаров, робот Google автоматически обойдёт весь каталог.

---

## 2. Google Merchant Center (GMC) — Обновить фид товаров (~1 минута)
1. Откройте [Google Merchant Center](https://merchants.google.com/).
2. Перейдите в **Товары → Источники данных** (`Products → Data sources` / `Feeds`).
3. Убедитесь, что URL вашего основного фида указывает на:
   `https://livijewelry.kz/google_merchant_feed.xml` (также на сайте теперь создана зеркальная копия по адресу `https://livijewelry.kz/feed.xml`).
4. Нажмите кнопку **Обновить сейчас** (`Fetch now` / `Update`).
   * **Что исправлено:** Все 28 товаров теперь имеют 100% совпадение названий (`<g:title>` = `<h1>` = JSON-LD `name`), цен в формате `XXXX.00 KZT` (`<g:price>` = JSON-LD `offers.price`), обязательный для ручной работы тег `<g:identifier_exists>no</g:identifier_exists>`, категорию `188` (Украшения) и единую политику возврата `ReturnShippingFees`.

---

## 3. Google Ads & Google Analytics 4 — Проверить статус основных целей «Покупка» и «Контакт» (~1 минута)
1. Откройте [Google Ads](https://ads.google.com/) → **Цели → Сводка** (`Goals → Summary`).
2. Проверьте, что:
   - Конверсия с ярлыком `AW-16793974126/MuJ_CObHup8bEO7q_sc-` (и/или импортированные из GA4 `G-YFF2TR0N36` события **`purchase`** и **`generate_lead`**) имеет статус **«Основная» (`Primary`)** для оптимизации ставок в кампаниях.
   - Если вы импортируете конверсии из GA4 (`G-YFF2TR0N36`) и одновременно используете прямую конверсию Google Ads (`AW-16793974126/MuJ_CObHup8bEO7q_sc-`), оставьте **Основной (`Primary`)** прямую конверсию Google Ads (она теперь срабатывает и при оформлении заказа с полной суммой чека `LIVI-<timestamp>`, и при клике на WhatsApp), а дублирующую импортированную из GA4 переведите в **Второстепенную (`Secondary` / Наблюдение)**, чтобы избежать двойного подсчёта.

---

## Мгновенный откат (если когда-либо потребуется)
Перед началом аудита была сохранена полная резервная ветка исходного состояния сайта: `backup/pre-audit-snapshot`.
Для мгновенного возврата к состоянию до аудита достаточно выполнить:
```bash
git checkout main
git reset --hard origin/backup/pre-audit-snapshot
git push --force origin main
```
