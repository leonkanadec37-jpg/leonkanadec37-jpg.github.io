# 004 · Заметка: часы работы

**От:** Claude · **Кому:** Antigravity · **Дата:** 09.11.2026 · Подтвердил Леонид.

Дополнение к `004-…note-kontakty-dostavka.md`, пункт «Часы»: **ежедневно с 11:00 до 17:00.**

- Подвал (RU/KZ/UZ): «Ежедневно 11:00–17:00» вместо «Часы работы — уточняйте в WhatsApp». KZ: «Күн сайын 11:00–17:00». UZ: «Har kuni 11:00–17:00».
- JSON-LD `JewelryStore`: добавить
```json
"openingHoursSpecification": [{
  "@type": "OpeningHoursSpecification",
  "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
  "opens": "11:00",
  "closes": "17:00"
}]
```
- Текст «Курьер сегодня при заказе до 16:00» остаётся как есть — он согласован с закрытием в 17:00.
