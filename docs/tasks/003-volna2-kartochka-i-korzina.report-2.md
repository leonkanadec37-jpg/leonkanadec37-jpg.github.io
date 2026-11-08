# Отчёт по доработкам 003 · Волна 2 (R1, R3–R5)

**От:** Antigravity · **Кому:** Claude, Леонид · **Дата:** 08.11.2026  
**Коммит фикса:** `0005e16` (`fix(task-003): address review items R1, R3-R5 for product cards and mini-cart`)  
**Статус:** Исправлены R1, R3, R4, R5 на 100%. R2 не менялся в соответствии с указанием («R2 не трогай»).

---

## Что исправлено по пунктам ревью

### R1 (P0). Карточка товара на телефоне: фото и кнопка Instagram
1. **Перевод `.product-gallery` на мобильную вертикальную колонку:**
   - В `styles.css` для медиа-запроса `@media (max-width: 860px)` устранено свойство `display: flex` (со значением row по умолчанию).
   - Задано строгое колоночное позиционирование:
     ```css
     .product-gallery {
       position: static;
       width: 100%;
       height: auto;
       max-height: none;
       aspect-ratio: auto;
       margin: 0 auto;
       display: flex;
       flex-direction: column;
       align-items: stretch;
       justify-content: flex-start;
       background: transparent;
       overflow: visible;
     }
     ```
   - Фотография `.product-gallery img` теперь занимает 100% ширины экрана с пропорцией 3:4 (`aspect-ratio: 3/4; width: 100%; object-fit: contain;`).
2. **Кнопка Instagram под фото:**
   - Расположена непосредственно под фото на всю ширину колонки:
     ```css
     .product-ig-btn {
       width: 100%;
       min-height: 44px;
       height: 44px;
       margin-top: 10px;
       box-sizing: border-box;
       display: inline-flex;
       align-items: center;
       justify-content: center;
     }
     ```
   - Текст «Смотреть на модели в Instagram» больше не сжимается и не обрезается справа.
3. **Десктопная версия:**
   - В `.storefront-product .product-gallery` заданы `overflow: visible; display: flex; flex-direction: column;`, что обеспечивает идеальное отображение на компьютере (кнопка ровно под фото на ширину колонки) с сохранением sticky-позиционирования.

---

### R3. Мини-корзина: шапка, кнопки и мобильный Bottom Sheet
1. **Z-index и видимость поверх шапки:**
   - Классы `.mini-cart-backdrop` и `.mini-cart-modal` переведены на `position: fixed; inset: 0; z-index: 10000;`.
   - Шапка окна («Добавлено в корзину» и крестик ✕) больше ни при каких условиях не подлезает под липкую шапку сайта (у `header` `z-index: 60`).
2. **Мобильный Bottom Sheet с safe-area:**
   - На экранах ≤ 768px модальное окно теперь выезжает снизу:
     ```css
     @media (max-width: 768px) {
       .mini-cart-backdrop,
       .mini-cart-modal {
         align-items: flex-end;
         justify-content: center;
         padding: 0;
       }
       .mini-cart-dialog {
         max-width: 100%;
         max-height: 85vh;
         border-radius: 16px 16px 0 0;
         border-bottom: none;
         padding: 20px 20px calc(20px + env(safe-area-inset-bottom, 0px));
         animation: slideUpSheet 0.28s cubic-bezier(0.2, 0.8, 0.2, 1);
       }
     }
     ```
   - На десктопе окно остаётся классическим центрированным модальным диалогом.
3. **Кнопка «Продолжить покупки»:**
   - Задан прозрачный фон с обводкой:
     ```css
     .mini-cart-actions .btn.outline,
     .mini-cart-actions .mini-cart-btn-continue,
     .mini-cart-continue {
       background: transparent !important;
       color: var(--fg) !important;
       border: 1px solid var(--line) !important;
       min-height: 44px;
     }
     .mini-cart-actions .btn.outline:hover {
       background: var(--bg-surface) !important;
       border-color: var(--fg) !important;
     }
     ```
   - Теперь на экране только одна главная кнопка с чёрной заливкой («Оформить заказ →»).
4. **Кнопка «+ Добавить» в рекомендациях:**
   - Селекторы `.mini-rec-add` и `.btn-rec-add` согласованы с разметкой.
   - Задана тонкая рамка `1px solid var(--fg)`, Montserrat 11px uppercase, высота 44px, белая заливка (при добавлении — мягкий зелёный фон `#2E7D32`). Дефолтный серый `border: outset` полностью устранён.

---

### R4. Рекомендации: дополнять, а не повторять
1. **Интеллектуальный подбор камня без влияния металла:**
   - Базовые металлы (`ювелирный сплав`, `позолота`, `родированная фурнитура`, `серебро`) исключены из подсчёта совпадения камней.
   - Введён семантический анализатор корней минералов (`жемчуг`, `перламутр`, `малахит`, `агат`, `гранат`, `кварц`, `аметист` и др.).
2. **Приоритет комплементарных категорий:**
   - Для колье алгоритм в первую очередь выбирает изделия **другой категории** с тем же камнем (серьги, браслеты, кольца или сеты с ними).
   - Только если изделий другой категории с совпадающим минералом меньше 2, алгоритм добирает изделия той же категории.
3. **Поддержка поля `pairs_with` в `products.json`:**
   - Реализована высшая приоритетность ручных связок: если у товара задан массив ID в `pairs_with`, они первыми попадают в блок «С этим носят» и мини-корзину.
   - Для флагманского товара `prod_01` (Колье с барочным жемчугом) прописаны гармонирующие связки:
     - `prod_04` — Позолоченная цепь и браслет с барочным жемчугом (браслет к колье)
     - `prod_73` — Серьги с натуральным жемчугом
     - `prod_40` — Серьги пусеты
4. **Фильтрация товаров, уже лежащих в корзине:**
   - В клиентской функции `openMiniCart()` через `readCart()` анализируются текущие товары в корзине клиента.
   - Если товар из блока рекомендаций уже лежит в корзине, его мини-карточка автоматически скрывается, а покупателю показываются до 2 других актуальных рекомендаций.

---

### R5. Заголовки в стиле H2 сайта (Cormorant Garamond)
1. **Блок «С этим носят»:**
   - Тег заменен на `<h2 class="product-pairs-title">`.
   - В `styles.css` задан шрифт `var(--font-serif)`:
     ```css
     .product-pairs-title,
     .product-pairs-with h2,
     .product-pairs-with h3,
     .pairs-with-title {
       font-family: var(--font-serif) !important;
       font-size: clamp(22px, 2.6vw, 28px);
       font-weight: 400 !important;
       letter-spacing: 0.02em;
       color: var(--fg);
       margin: 0 0 14px;
       text-align: left;
     }
     ```
   - Заголовок синхронизирован на всех трёх языках:
     - RU: *«С этим носят»*
     - KZ: *«Осымен бірге тағады»*
     - UZ: *«Buning bilan taqishadi»*
2. **Блок в мини-корзине «С этим украшением рекомендуем:»:**
   - Оформлен серифом `var(--font-serif)` 18px (RU: *«С этим украшением рекомендуем:»*, KZ: *«Осы әшекеймен бірге ұсынамыз:»*, UZ: *«Ushbu taqinchoq bilan tavsiya qilamiz:»*).

---

### Статус пункта R2 («Бесплатно» в доставке)
- В точном соответствии с указанием пользователя («R2 не трогай»), блок стоимости доставки и итоговых сумм в `cart.html` не модифицировался.
- Заметка `003-volna2-kartochka-i-korzina.note-r2.md` принята к сведению; ожидается отмашка на синхронизацию текстов после согласования условий и цифр для фидов.

---

## Результаты верификации и тестов

1. **`python build_all.py`**:
   - Все 10 этапов конвейера сборки отработали чисто за 16.00с.
   - Перегенерированы страницы RU, KZ, UZ, фиды и карты сайта.
2. **`python scripts/verify_audit.py`**:
   - **45 из 45 инвариантов PASS (0 ошибок)**.
3. **Проверка DOM**:
   - На мобильном вьюпорте `.product-gallery` отображается вертикальной колонкой, фото — 100% ширины, кнопка Instagram — под фото с высотой 44px.
   - Модальное окно мини-корзины имеет `z-index: 10000` и выезжает снизу на экранах ≤ 768px.
   - Кнопка «Продолжить покупки» оформлена обводкой.
   - Для `prod_01` предлагаются браслет и серьги с жемчугом вместо конкурирующих колье.
