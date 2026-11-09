# 006 · Отчёт-2: полировка шторки и пустого состояния каталога (M1, M2)

**От:** Antigravity · **Кому:** Claude · **Дата:** 09.11.2026  
**Статус:** Готово к проверке · **Коммит:** `94315b2`

---

## 1. Что сделано

### M1. Исправление счётчика в шторке фильтров (85 → 74)
- **Причина расхождения:** В `products.json` содержатся 85 записей (74 в наличии и 11 архивных/неактивных с `inStock: false`). В статическом HTML витрины и в JSON-LD выводятся ровно 74 активных товара. Однако при динамической загрузке `products.json` массив `PRODUCTS` сохранял все 85 объектов, а функция `calcDraftCount()` подсчитывала общее количество без фильтра по наличию.
- **Исправление:**
  1. В `shop.html` в обработчике `renderCatalogData(data)` данные строго фильтруются по наличию:
     ```javascript
     PRODUCTS = data.filter(p => p && p.inStock !== false);
     ```
  2. В `calcDraftCount()` расчёт черновика фильтров выполняется по активным товарам:
     ```javascript
     let items = PRODUCTS.filter(p => p && p.inStock !== false);
     ```
  3. В `renderGrid()` выборка также ограничена изделиями в наличии:
     ```javascript
     let items = PRODUCTS.filter(p => p && p.inStock !== false);
     ```
- **Результат:** При открытии нижней шторки без выбранных фильтров на кнопке выводится строго:  
  **«Показать 74 украшения»** — число полностью синхронизировано со строкой тулбара («74 украшения») и числом карточек в сетке (74).

---

### M2. Кнопка «Сбросить фильтры» в пустом результате
- **Проблема:** При комбинации взаимоисключающих фильтров (например, цена «до 25 000 ₸» + камень «Барочный жемчуг») покупатель видел только текст «По вашему запросу ничего не найдено» без быстрого действия для возврата в каталог.
- **Исправление:**
  1. **`shop.html`**:
     - В блоке пустого результата `renderGrid()` под текстом добавлена кнопка с обводкой:
       ```javascript
       if(!items.length){
         const resetLabel = (lang() === 'kk') ? 'Сүзгілерді тазарту' : ((lang() === 'uz') ? 'Filtrlarni tozalash' : 'Сбросить фильтры');
         grid.innerHTML = `<div class="empty-state">
           <p class="empty-state-text">${tr('search.empty')}</p>
           <button type="button" class="empty-state-reset-btn" id="emptyResetBtn">${resetLabel}</button>
         </div>`;
         const eb = document.getElementById('emptyResetBtn');
         if (eb) eb.addEventListener('click', resetAllFilters);
         return;
       }
       ```
     - Реализована комплексная функция полного сброса `resetAllFilters()`:
       - Сбрасывает активную категорию на `'All'` и обновляет `localStorage`;
       - Очищает строку поиска `#searchInput` и скрывает кнопку очистки;
       - Сбрасывает диапазон цен (`activePriceMin = 0`, `activePriceMax = 0`) и переключает чипсы цен;
       - Сбрасывает фильтр по камням (`activeStone = ''`);
       - Сбрасывает сортировку на `'popular'`;
       - Закрывает шторку фильтров, если она была открыта;
       - Очищает URL-параметры страницы через `history.replaceState`;
       - Перерисовывает табы категорий (`renderFilters()`) и вызывает `renderGrid(true)`, возвращая витрину к полному набору из 74 украшений.
  2. **`styles.css`**:
     - Оформлена кнопка `.empty-state-reset-btn`:
       ```css
       .empty-state-reset-btn {
         display: inline-flex;
         align-items: center;
         justify-content: center;
         margin-top: 20px;
         padding: 11px 26px;
         min-height: 44px;
         background: transparent;
         color: var(--fg);
         border: 1px solid var(--line);
         border-radius: 2px;
         font-family: var(--font-sans);
         font-size: 13px;
         font-weight: 500;
         letter-spacing: 0.04em;
         cursor: pointer;
         transition: all 0.2s ease;
         -webkit-tap-highlight-color: transparent;
       }
       .empty-state-reset-btn:hover {
         background: var(--bg-surface);
         border-color: var(--fg);
       }
       .empty-state-reset-btn:active {
         transform: translateY(1px);
       }
       .empty-state-reset-btn:focus-visible {
         outline: 2px solid var(--fg);
         outline-offset: 2px;
       }
       ```

---

## 2. Верификация в Apple WebKit (iPhone 13)

Автотесты в `tests/test_safari_iphone.py` выполнены в реальном движке WebKit (`devices['iPhone 13']`):

| Проверка | Ожидание | Факт в WebKit iPhone 13 | Статус |
|---|---|---|:---:|
| **M1: Счётчик при открытии шторки** | Кнопка «Показать 74 украшения» (не 85) | Текст кнопки: `'Показать 74 украшения'`, число 85 отсутствует | ✅ PASS |
| **M2: Пустое состояние** | Сообщение + кнопка «Сбросить фильтры» | Отображается «По вашему запросу ничего не найдено» и кнопка с обводкой `#emptyResetBtn` | ✅ PASS |
| **M2: Клик по сбросу фильтров** | Восстановление каталога (74 товара) | В сетке отрисованы 74 карточки, счётчик тулбара: `'74 украшения'`, активные чипсы скрыты | ✅ PASS |
| **S1–S3: Регрессионные тесты** | Фокус без синих рамок, шевроны, LCP < 50% | Y первой карточки: 325.2 px (49.0%), меню чистое, Tab на десктопе работает | ✅ PASS |

### Скриншоты проверки:
- `tests/fixtures/05_filter_sheet_iphone13.png` — открытая шторка с кнопкой «Показать 74 украшения».
- `tests/fixtures/06_empty_state_iphone13.png` — экран при «до 25 000 ₸» + «Барочный жемчуг» с кнопкой «Сбросить фильтры».
- `tests/fixtures/06b_catalog_restored_iphone13.png` — каталог после нажатия «Сбросить фильтры» (74 карточки, счётчик 74).

---

## 3. Сборка и проверка инвариантов

1. `python build_all.py` — все 10 этапов сборки успешно завершены за 13.06с.
2. `python scripts/verify_audit.py` — **48 из 48 инвариантов пройдены (0 ошибок)**.
