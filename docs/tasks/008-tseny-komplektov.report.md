# Отчёт по задаче 008: цены комплектов и выбор варианта на странице товара

Дата: 2026-11-15  
Задача: [008-tseny-komplektov.md](008-tseny-komplektov.md)  
План: [PLAN.md](PLAN.md)

---

## 0. Проверка и восстановление папки `docs/tasks/`

Перед началом работы проверено состояние `docs/tasks/` (`git status`, `git log --stat -- docs/tasks` и корзина `D:\$RECYCLE.BIN`):

- Коммитом `84ed5de` ранее были штатно удалены архивы завершённых задач `001–004`, `006` и `agent-handoff.md`.
- Файлы `005-volna4-kz-ads-polirovka.md`, `900-otlozheno-reklama-i-trekking.md`, `README.md` (отслеживаемые в Git), а также неотслеживаемые `007-mobile-menu-redesign.md` и `007-mobile-menu-redesign.report.md` **не переносились** — они были случайно удалены в корзину Windows `15.11.2026 12:05`.
- Все 5 файлов восстановлены в `docs/tasks/`:
  - `005-volna4-kz-ads-polirovka.md`, `900-otlozheno-reklama-i-trekking.md`, `README.md` — через `git checkout -- ...`;
  - `007-mobile-menu-redesign.md` и `007-mobile-menu-redesign.report.md` — скопированы обратно из `D:\$RECYCLE.BIN`.

---

## 1. Что сделано и в каких файлах

1. **Единая логика ценообразования (без дублирования по генераторам)**
   - [scripts/catalog_pricing.py](../../scripts/catalog_pricing.py): функции `PLACEHOLDER_OPTION_NAMES`, `real_bundle_options`, `has_from_price`, `main_bundle_option`, `catalog_price`, `ordered_bundle_options`, `full_option_index`, `variant_param`, `format_price_num`, `format_from_price`, `price_html`. Заглушки 70/30 (`"Основное украшение комплекта"`, `"Дополнительный элемент сета"`) отсеиваются; при равных ценах выбирается вариант с меньшим исходным индексом; полный комплект (`is_full=True`) выносится в конец списка.
   - [scripts/catalog-pricing.js](../../scripts/catalog-pricing.js): зеркальный клиентский модуль `window.LiviPricing` для витрин и фильтров.

2. **Стили**
   - [styles.css](../../styles.css): добавлены `.price-from` (без наложения курсивного сдвига, `font-weight: 400; font-size: 0.85em`), `.bundle-options[role="radiogroup"]`, `.bundle-option[role="radio"]` (клик-зона `min-height: 44px`, выделение активного варианта `aria-checked="true"` рамкой `--gold-text`, состояние `:focus-visible`).

3. **Страницы товаров, витрины и `ItemList` (RU / KZ / UZ)**
   - [scripts/generate_product_pages.py](../../scripts/generate_product_pages.py), [scripts/generate_kz_pages.py](../../scripts/generate_kz_pages.py), [scripts/generate_uz_pages.py](../../scripts/generate_uz_pages.py):
     - на карточках витрин (`shop.html`, `index.html`, `kz/shop.html`, `kz/index.html`, `uz/shop.html`, `uz/index.html`) и в `ItemList` комплекты отображаются с ценой главного предмета (`catalog_price`) и пометкой `от` / `бастап` / `dan` (`price_html`);
     - на страницах комплектов `<select id="customBundle">` заменён на `role="radiogroup"` с сортировкой по убыванию цены и полным комплектом в конце; по умолчанию выбран главный предмет (`aria-checked="true"`), цена в шапке и CTA соответствует ему;
     - удалён блок `bundle-breakdown-badge`;
     - добавлена поддержка `?v=full` и `?v=<orig_idx>` при загрузке и переключении (`history.replaceState` с сохранением UTM/gclid), неизвестное значение `?v=` безопасно откатывается на главный предмет; добавлена навигация стрелками / `Home` / `End` и roving `tabindex`;
     - в JSON-LD `Product.offers` для комплектов формируется массив вариантов со ссылками `?v=...`; `<meta property="product:price:amount">` сохранён равным полной цене `products.json.price`;
     - быстрое добавление в корзину (карточки «С этим носят» / мини-корзина / витрины) и добавление выбранного варианта на странице товара используют уникальный ключ `pid-<orig_idx>` и корректный `customBundle`/`unitPrice`, чтобы в корзину не попадал полный сет по цене одного предмета.
   - [shop.html](../../shop.html) и [index.html](../../index.html): подключён `/scripts/catalog-pricing.js` (без `defer` перед inline-скриптами); фильтрация по цене, сортировка (`price_asc`/`price_desc`), модальное окно, `calcDraftCount`, `initStaticCards` и `addToCart` переведены на `window.LiviPricing`.

4. **SEO-хабы (21 RU + 21 KZ + 21 UZ)**
   - [scripts/generate_seo_hubs.py](../../scripts/generate_seo_hubs.py): переведены на `catalog_price(p)` и `price_html(p, lang)` (`ItemList`, диапазон цен в `meta_desc`, карточки хабов и `sergi-iz-zhemchuga.html`).

5. **Товарные фиды (Google, 2ГИС, Pinterest) и Kaspi**
   - [scripts/generate_feed.py](../../scripts/generate_feed.py): в `google_merchant_feed.xml` и `feed.xml` ссылка комплектов ведёт на `?v=full`, в `build_rich_description()` варианты теперь берутся через `real_bundle_options(p)`, полная цена не изменилась.
   - [scripts/generate_2gis_catalog.py](../../scripts/generate_2gis_catalog.py): в `2gis_feed.xml` и `feeds/2gis_catalog.csv` ссылка комплектов ведёт на `?v=full`, цена полная.
   - [scripts/generate_pinterest_assets.py](../../scripts/generate_pinterest_assets.py): ссылка комплектов содержит `?v=full&utm_source=...` (один `?`), цена полная.
   - `products.json`, `sync_drive.py`, `scripts/add_product.py` и `scripts/generate_kaspi_feed.py` не изменялись.
   - Проверка Kaspi: `git diff --stat kaspi_feed.xml` → `kaspi_feed.xml | 2 +-` (изменилась только строка с датой генерации `date="..."`, ни одна цена или позиция не изменилась).

6. **Служебное и автотесты**
   - [.gitignore](../../.gitignore): добавлено `.ai-collab/`.
   - [scripts/verify_audit.py](../../scripts/verify_audit.py): обновлены проверки 4, 15, 17, 24, 39 под `offers[]` и `radiogroup`; добавлены проверки 49–54 (логика `catalog_pricing` на 5 эталонных товарах + заглушках, витрины и `ItemList` RU/KZ/UZ, `radiogroup` и кнопка заказа RU/KZ/UZ, `Product.offers` с проверкой всех `?v=`, фиды Google/2ГИС/Pinterest и неизменность цен `kaspi_feed.xml`), задан фиксированный счётчик `EXPECTED_TESTS = 54`.

---

## 2. Результат `build_all.py` и тестов

Финальный прогон `python build_all.py` после всех правок:
- Все шаги `0/10` – `10/10` завершились без ошибок за **26.47с** (`[OK] Sitemap обновлен: 303 URLs`).
- `scripts/verify_audit.py`: **54/54 PASS, 0 Errors** (подтверждены эталоны `prod_11`: 61000→45000, `prod_21`: 74000→40000, `prod_18`: 74000→30000, `prod_04`: 40000→25000, `prod_73`: 93000→75000).

### Локальная валидация JSON-LD и браузерная проверка (Playwright / Edge)

Проверено локальным скриптом поверх HTTP-сервера на ширинах **375×812** (mobile) и **1366×900** (desktop):
- **JSON-LD `/product/prod_11.html`**: корректные блоки `Product`, `BreadcrumbList`, `FAQPage`; `Product.offers` — массив из 3 объектов `Offer` (`45000`, `16000`, `61000` KZT, `InStock`, `hasMerchantReturnPolicy` 14 дней, `shippingDetails` 4000 KZT, ссылки содержат `?v=1`, `?v=2`, `?v=full`).
- **`?v=full` и `?v=999` на `/product/prod_11.html`**: `?v=full` открывает полный комплект (`61 000 ₸`, `aria-checked="true"`), `?v=999` откатывается на главный предмет (`45 000 ₸`).
- **Корзина (`livi_cart_v3`)**: добавление двух вариантов `prod_11` создаёт две раздельные записи с разными ID (`prod_11-1` и `prod_11-0`).
- **Сортировка и фильтр витрины (`shop.html`)**: при `price_asc` товар `prod_18` (главный предмет 30 000 ₸, полный 74 000 ₸) располагается раньше `prod_73` (75 000 ₸); по URL `shop.html?max_price=50000` товар `prod_11` (45 000 ₸) присутствует в выдаче, `prod_73` (75 000 ₸) исключён.
- **Клавиатура**: `ArrowDown`, `End`, `Home` корректно переключают выбранный вариант, цену и параметр `?v=` в адресной строке.
- **Отсутствие ошибок и переполнения (`375px` и `1366px`)**: проверены `/shop.html`, `/index.html`, `/komplekty-ukrasheniy.html`, `/product/prod_11.html`, `/kz/product/prod_11.html`, `/uz/product/prod_11.html` — `overflow: false` на всех страницах, ошибок консоли и JS (`errors: []`) нет.

---

## 3. Отклонения от текста задачи и почему они сделаны

1. **Формат SKU в тесте 2 `verify_audit.py`**: регулярное выражение расширено с `\d{2}` до `\d{2,3}`, так как в `products.json` уже присутствуют активные товары `prod_100` и `prod_101` (артикулы `LIVI-100`, `LIVI-101`).
2. **Данные событий аналитики в `shop.html` и `kz/shop.html`**: значения `price` и `item_name`/`content_name` в `view_item_list`, `add_to_cart` и `AddToCart` приведены к главному предмету комплекта, чтобы аналитика соответствовала фактической цене витрины и составу корзины. Сами вызовы `gtag`/`fbq` и теги конверсий не менялись.
3. **Заглушки 70/30 в `sync_drive.py`**: согласно условию не изменять `sync_drive.py`, его код не тронут; возможные заглушки отсекаются в `catalog_pricing.py`, `catalog-pricing.js` и `generate_feed.py` (в тесте 4 для них добавлено предупреждение `WARN`).

---

## Вопрос пользователю

`sync_drive.py` (и `scripts/add_product.py`) всё ещё умеют автоматически создавать заглушки 70/30 (`"Основное украшение комплекта"`, `"Дополнительный элемент сета"`), если не передана реальная разбивка. На сайте и в фиде Google такие заглушки теперь игнорируются. Нужно ли отдельной задачей убрать этот автогенератор 70/30 из `sync_drive.py` и `scripts/add_product.py`?
