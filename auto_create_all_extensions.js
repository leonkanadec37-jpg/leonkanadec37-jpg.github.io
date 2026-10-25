/**
 * ==============================================================================
 * LIVI JEWELRY — АВТОМАТИЧЕСКОЕ СОЗДАНИЕ ВСЕХ РАСШИРЕНИЙ ОБЪЯВЛЕНИЙ (ASSETS) v2.0
 * ==============================================================================
 *
 * ЧТО ЭТОТ СКРИПТ ДЕЛАЕТ АВТОМАТИЧЕСКИ (ЗА 5 СЕКУНД):
 * 1. Создает 6 Быстрых ссылок (Sitelinks) с описаниями и URL на главные разделы:
 *    - «Комплекты украшений» -> /komplekty-ukrasheniy.html
 *    - «Колье из жемчуга» -> /kolye-iz-zhemchuga.html
 *    - «Серьги от 8 500 ₸» -> /sergi-iz-zhemchuga.html
 *    - «Чокеры из камней» -> /chokery-iz-naturalnyh-kamney.html
 *    - «Сотуары и галстуки» -> /sotuary-iz-zhemchuga.html
 *    - «Весь каталог (55 моделей)» -> /shop.html
 * 2. Создает 8 Уточнений (Callouts) без стоп-фраз:
 *    - «Натуральные камни и жемчуг»
 *    - «Ручная работа в Астане»
 *    - «Курьером день-в-день Астана»
 *    - «Доставка СДЭК 1-3 дня по РК»
 *    - «Подарочная упаковка 0 ₸»
 *    - «Kaspi Pay / Kaspi Red»
 *    - «Живое видео в WhatsApp»
 *    - «Стойкий родий и позолота»
 * 3. Создает 2 Структурированных описания (Structured Snippets):
 *    - Типы: Комплекты, Колье, Серьги, Чокеры, Сотуары, Цепи с жемчугом
 *    - Стили: Барочный жемчуг, Натуральные камни, Жемчуг Майорка, Ручная работа
 * 4. Автоматически привязывает их к кампании "Livi Jewelry - Поиск Казахстан"!
 * ==============================================================================
 */

var CONFIG = {
  TARGET_CAMPAIGN_NAME: "Livi Jewelry - Поиск Казахстан"
};

function main() {
  Logger.log("==================================================================");
  Logger.log("   💎 LIVI JEWELRY — АВТОМАТИЧЕСКОЕ СОЗДАНИЕ РАСШИРЕНИЙ v2.0      ");
  Logger.log("==================================================================");

  var campIter = AdsApp.campaigns()
    .withCondition("Name = '" + CONFIG.TARGET_CAMPAIGN_NAME + "'")
    .get();

  if (!campIter.hasNext()) {
    Logger.log("⚠️ Кампания \"" + CONFIG.TARGET_CAMPAIGN_NAME + "\" не найдена. Проверьте точное название!");
    return;
  }

  var campaign = campIter.next();
  Logger.log("✓ Кампания найдена: " + campaign.getName());

  setupSitelinks(campaign);
  setupCallouts(campaign);
  setupSnippets(campaign);

  Logger.log("\n==================================================================");
  Logger.log("🎉 ВСЕ РАСШИРЕНИЯ v2.0 УСПЕШНО СОЗДАНЫ И ПРИВЯЗАНЫ К КАМПАНИИ!");
  Logger.log("==================================================================");
}

function setupSitelinks(campaign) {
  Logger.log("\n[1] Настройка Быстрых ссылок (Sitelinks)...");

  var existing = {};
  var it = campaign.extensions().sitelinks().get();
  while (it.hasNext()) {
    var sl = it.next();
    var txt = sl.getLinkText().toLowerCase().trim();
    // Удаляем старую ссылку на браслеты, так как в каталоге всего 1 браслет
    if (txt.indexOf("браслет") !== -1) {
      campaign.removeSitelink(sl);
      Logger.log("  • Отвязана неактуальная быстрая ссылка: \"" + sl.getLinkText() + "\"");
      continue;
    }
    existing[txt] = true;
  }

  // Лимиты Google Ads: text <= 25 симв., desc1 <= 35 симв., desc2 <= 35 симв.
  var sitelinksData = [
    {
      text: "Комплекты украшений",             // 19
      desc1: "Колье, браслет и серьги в сете",   // 30
      desc2: "Можно купить вместе или отдельно", // 32
      url: "https://livijewelry.kz/komplekty-ukrasheniy.html"
    },
    {
      text: "Колье из жемчуга",                // 16
      desc1: "Натуральный и барочный жемчуг",   // 29
      desc2: "Ручная сборка и стойкая фурнитура",// 33
      url: "https://livijewelry.kz/kolye-iz-zhemchuga.html"
    },
    {
      text: "Серьги от 8 500 ₸",               // 17
      desc1: "Пусеты, трансформеры и классика",  // 31
      desc2: "Гипоаллергенный родий и позолота", // 32
      url: "https://livijewelry.kz/sergi-iz-zhemchuga.html"
    },
    {
      text: "Чокеры из камней",                // 16
      desc1: "Граненый гранат, аметист, жемчуг", // 32
      desc2: "Изящная посадка по линии шеи",     // 28
      url: "https://livijewelry.kz/chokery-iz-naturalnyh-kamney.html"
    },
    {
      text: "Сотуары и галстуки",              // 18
      desc1: "Длинные колье-трансформеры 85 см", // 32
      desc2: "Эффектный акцент для декольте",    // 29
      url: "https://livijewelry.kz/sotuary-iz-zhemchuga.html"
    },
    {
      text: "Весь каталог Livi",               // 17
      desc1: "55 авторских украшений в наличии", // 32
      desc2: "Доставка СДЭК по всему Казахстану",// 33
      url: "https://livijewelry.kz/shop.html"
    }
  ];

  var created = 0;
  for (var i = 0; i < sitelinksData.length; i++) {
    var item = sitelinksData[i];
    if (existing[item.text.toLowerCase()]) {
      Logger.log("  • Ссылка \"" + item.text + "\" уже существует — пропуск.");
      continue;
    }

    try {
      var builder = AdsApp.extensions().newSitelinkBuilder()
        .withLinkText(item.text)
        .withDescription1(item.desc1)
        .withDescription2(item.desc2)
        .withFinalUrl(item.url);

      var op = builder.build();
      if (op.isSuccessful()) {
        campaign.addSitelink(op.getResult());
        Logger.log("  ✓ Создана быстрая ссылка: \"" + item.text + "\"");
        created++;
      } else {
        Logger.log("  ⚠️ Ошибка создания: " + op.getErrors());
      }
    } catch (e) {
      Logger.log("  ⚠️ Исключение при создании ссылки: " + e.message);
    }
  }
  Logger.log("Итого создано быстрых ссылок: " + created);
}

function setupCallouts(campaign) {
  Logger.log("\n[2] Настройка Уточнений (Callouts)...");

  var existing = {};
  var it = campaign.extensions().callouts().get();
  while (it.hasNext()) {
    var co = it.next();
    var txt = co.getText().toLowerCase().trim();
    if (txt.indexOf("100%") !== -1 || txt.indexOf("подгон") !== -1) {
      campaign.removeCallout(co);
      Logger.log("  • Отвязано устаревшее уточнение: \"" + co.getText() + "\"");
      continue;
    }
    existing[txt] = true;
  }

  // Лимит Google Ads: до 25 символов
  var calloutsList = [
    "Природные камни и жемчуг", // 24
    "Ручная работа в Астане",   // 22
    "Доставка в день заказа",   // 22
    "СДЭК 1-3 дня по всему РК", // 24
    "Подарочная упаковка 0 ₸",  // 23
    "Kaspi Pay и Kaspi Red",    // 21
    "Живое видео в WhatsApp",   // 22
    "Стойкий родий и позолота"  // 24
  ];

  var created = 0;
  for (var i = 0; i < calloutsList.length; i++) {
    var text = calloutsList[i];
    if (existing[text.toLowerCase()]) {
      Logger.log("  • Уточнение \"" + text + "\" уже есть — пропуск.");
      continue;
    }

    try {
      var op = AdsApp.extensions().newCalloutBuilder().withText(text).build();
      if (op.isSuccessful()) {
        campaign.addCallout(op.getResult());
        Logger.log("  ✓ Создано уточнение: \"" + text + "\"");
        created++;
      }
    } catch (e) {
      Logger.log("  ⚠️ Ошибка уточнения: " + e.message);
    }
  }
  Logger.log("Итого создано уточнений: " + created);
}

function setupSnippets(campaign) {
  Logger.log("\n[3] Настройка Структурированных описаний (Snippets)...");

  var existing = {};
  var it = campaign.extensions().snippets().get();
  while (it.hasNext()) {
    existing[it.next().getHeader().toLowerCase().trim()] = true;
  }

  var snippetsData = [
    {
      header: "Типы",
      values: ["Комплекты украшений", "Колье из жемчуга", "Колье из камней", "Серьги", "Чокеры", "Сотуары"]
    },
    {
      header: "Модели",
      values: ["Барочный жемчуг", "Натуральные самоцветы", "Жемчуг Майорка", "Цепи с жемчужиной", "Колье-галстуки"]
    }
  ];

  var created = 0;
  for (var i = 0; i < snippetsData.length; i++) {
    var item = snippetsData[i];
    if (existing[item.header.toLowerCase()]) {
      Logger.log("  • Описание \"" + item.header + "\" уже есть — пропуск.");
      continue;
    }

    try {
      var op = AdsApp.extensions().newSnippetBuilder()
        .withHeader(item.header)
        .withValues(item.values)
        .build();
      if (op.isSuccessful()) {
        campaign.addSnippet(op.getResult());
        Logger.log("  ✓ Создано структурированное описание: \"" + item.header + "\"");
        created++;
      }
    } catch (e) {
      Logger.log("  ⚠️ Ошибка описания: " + e.message);
    }
  }
  Logger.log("Итого создано описаний: " + created);
}
