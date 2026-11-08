# Отчёт по доработке 001 (T-P0.4: мобильное меню)

**От:** Antigravity · **Кому:** Claude, Леонид · **Дата:** 08.11.2026  
**Коммит фикса:** `265909e` (`fix(menu): lock scroll on html only and fix mobile storefront-menu to viewport`)  
**Статус:** Исправлено и проверено в реальном браузере на 375×812 при `scrollY = 900`  

---

## Что исправлено

1. **Снято правило `overflow: hidden` с `body`**:
   - В `styles.css` правило изоляции скролла изменено с `html.drawer-open, body.drawer-open...` на:
     ```css
     html.drawer-open,
     html.modal-open {
       overflow: hidden !important;
       touch-action: none;
     }
     ```
   - За счёт этого `body` больше не становится локальным скролл-контейнером с нулевым смещением и не срывает `position: sticky; top: 0` у шапки `header.storefront-header`.

2. **Зафиксировано мобильное меню в viewport**:
   - Для `.storefront-menu` на экранах ≤ 768 px явно задано:
     ```css
     .storefront-menu {
       position: fixed;
       top: var(--storefront-header-height); /* 57px на мобильном */
       left: 0;
       bottom: 0;
       width: min(88vw, 370px);
       height: calc(100dvh - var(--storefront-header-height));
       overflow-y: auto;
       overscroll-behavior: contain;
       border-right: 1px solid var(--line);
       z-index: 1;
     }
     ```
   - Теперь меню жестко привязано к видимой области экрана непосредственно под шапкой (`top: 57px`) и не зависит от позиции родительских элементов.

---

## Проверка в реальном headless Chrome (375×812)

Скрипт проверки через Chrome DevTools Protocol протестировал сценарий:
1. Загрузка `shop.html` с мобильным вьюпортом 375×812.
2. Прокрутка вниз до `scrollY = 900`.
3. Клик по кнопке «Меню»:
   - `headerRect`: `top = 0, bottom = 58, height = 58` (шапка на месте вверху экрана).
   - `menuRect`: `top = 57, bottom = 812, left = 0, width = 330, height = 755` (меню открыто прямо под шапкой и занимает экран до низа).
   - `backdropRect`: `top = 57, bottom = 812, height = 755` (затемнение активно под шапкой).
   - Фон страницы заблокирован (`html.drawer-open`).
4. Закрытие меню (как по клику на бэкдроп, так и по кнопке «Меню»):
   - Меню закрывается (`menu.hidden = true`).
   - `scrollY` остаётся строго на `900`.

---

## Сборка и деплой
- `python build_all.py` — 10/10 шагов успешно пройдены за 19.9с.
- `python scripts/verify_audit.py` — **45/45 PASS**.
- Коммит `265909e` запушен в `origin/main`.
