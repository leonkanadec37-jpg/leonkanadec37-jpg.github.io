/**
 * ==============================================================================
 * LIVI JEWELRY — АВТОМАТИЧЕСКОЕ СОЗДАНИЕ ВСЕХ РАСШИРЕНИЙ ОБЪЯВЛЕНИЙ (ASSETS) v1.0
 * ==============================================================================
 * 
 * ЧТО ЭТОТ СКРИПТ ДЕЛАЕТ АВТОМАТИЧЕСКИ (ЗА 5 СЕКУНД):
 * 1. Создает 4 богатые Быстрые ссылки (Sitelinks) с описаниями и URL на SEO-хабы:
 *    - «Колье из жемчуга» -> /kolye-iz-zhemchuga.html
 *    - «Комплекты украшений» -> /komplekty-ukrasheniy.html
 *    - «Серьги с жемчугом» -> /sergi-iz-zhemchuga.html
 *    - «Браслеты из камней» -> /braslety-iz-zhemchuga.html
 * 2. Создает 6 Уточнений (Callouts):
 *    - «100% натуральные камни»
 *    - «Барочный жемчуг»
 *    - «Ручная работа Livi»
 *    - «Доставка 1-3 дня по РК»
 *    - «Подарочная упаковка»
 *    - «Kaspi Red / Рассрочка»
 * 3. Создает 2 Структурированных описания (Structured Snippets):
 *    - Материалы: Барочный жемчуг, Аметист, Малахит, Бирюза, Гранат, Кварц
 *    - Типы: Колье, Чокеры, Серьги, Браслеты, Авторские сеты, Сотуары
 * 4. Автоматически привязывает их к кампании "Livi Jewelry - Поиск Казахстан"!
 * 
 * КАК ЗАПУСТИТЬ:
 * 1. Откройте Google Ads -> Инструменты и настройки -> Скрипты (Scripts).
 * 2. Нажмите "+", вставьте этот код, нажмите "Авторизовать" и "Выполнить".
 * 3. Все расширения будут мгновенно созданы в вашем аккаунте без ручной рутины!
 * ==============================================================================
 */

var CONFIG = {
  TARGET_CAMPAIGN_NAME: "Livi Jewelry - Поиск Казахстан"
};

function main() {
  Logger.log("==================================================================");
  Logger.log("   💎 LIVI JEWELRY — АВТОМАТИЧЕСКОЕ СОЗДАНИЕ РАСШИРЕНИЙ (ASSETS)   ");
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

  // 1. Быстрые ссылки (Sitelinks)
  setupSitelinks(campaign);

  // 2. Уточнения (Callouts)
  setupCallouts(campaign);

  // 3. Структурированные описания (Snippets)
  setupSnippets(campaign);

  Logger.log("\n==================================================================");
  Logger.log("🎉 ВСЕ РАСШИРЕНИЯ УСПЕШНО СОЗДАНЫ И ПРИВЯЗАНЫ К КАМПАНИИ!");
  Logger.log("==================================================================");
}

function setupSitelinks(campaign) {
  Logger.log("\n[1] Настройка Быстрых ссылок (Sitelinks)...");
  
  var existing = {};
  var it = campaign.extensions().sitelinks().get();
  while (it.hasNext()) {
    existing[it.next().getLinkText().toLowerCase().trim()] = true;
  }

  var sitelinksData = [
    {
      text: "Колье из жемчуга",
      desc1: "Натуральный барочный жемчуг",
      desc2: "Ручная работа и премиум фурнитура",
      url: "https://livijewelry.kz/kolye-iz-zhemchuga.html"
    },
    {
      text: "Комплекты украшений",
      desc1: "Авторские сеты колье и серьги",
      desc2: "Идеальный подарок со вкусом",
      url: "https://livijewelry.kz/komplekty-ukrasheniy.html"
    },
    {
      text: "Серьги с жемчугом",
      desc1: "Барокко и майорка ручной работы",
      desc2: "Гипоаллергенный сплав и позолота",
      url: "https://livijewelry.kz/sergi-iz-zhemchuga.html"
    },
    {
      text: "Браслеты из камней",
      desc1: "Малахит, аметист, бирюза и гранат",
      desc2: "Быстрая доставка по всему Казахстану",
      url: "https://livijewelry.kz/braslety-iz-zhemchuga.html"
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
    existing[it.next().getText().toLowerCase().trim()] = true;
  }

  var calloutsList = [
    "100% натуральные камни",
    "Барочный жемчуг",
    "Ручная работа Livi",
    "Доставка 1-3 дня по РК",
    "Подарочная упаковка",
    "Kaspi Red / Рассрочка"
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
      values: ["Колье", "Чокеры", "Серьги", "Браслеты", "Авторские сеты", "Сотуары"]
    },
    {
      header: "Материалы",
      values: ["Барочный жемчуг", "Аметист", "Малахит", "Бирюза", "Гранат", "Кварц"]
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
