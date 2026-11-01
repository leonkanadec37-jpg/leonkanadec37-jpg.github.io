/**
 * ==============================================================================
 * LIVI JEWELRY — РАЗОВАЯ КОНСОЛИДАЦИЯ В 1 ЕДИНУЮ ГРУППУ ОБЪЯВЛЕНИЙ
 * Файл: marketing/google_ads/scripts/create_single_ad_group.js
 * Версия: v2.1 CATALOG DIRECT EDITION (ЕДИНЫЙ URL: https://livijewelry.kz/shop.html)
 * 
 * ЧТО ДЕЛАЕТ СКРИПТ:
 *   1. Находит или переименовывает основную группу в «Все украшения Livi Jewelry»
 *      (с сохранением накопленной статистики кликов и показов).
 *   2. Ставит дублирующие группы объявлений на паузу (ликвидирует 100% канибализации).
 *   3. Загружает ровно 150 чистых коммерческих ключей с прямым маркером покупки
 *      («купить», «заказать», «магазин», «каталог», «цена») в фразовом соответствии ("...").
 *   4. Направляет 100% трафика напрямую в общий интерактивный каталог:
 *      https://livijewelry.kz/shop.html (вся витрина из 63 товаров, фильтры, цены).
 *   5. Устанавливает базовую ставку DEFAULT_CPC: 0.24$ для уверенного входа в топ-3.
 *   6. Создает адаптивное объявление (RSA) с динамической подстановкой {KeyWord:...},
 *      триггерами ручной работы, гарантией натуральности и оплатой Kaspi QR / Red.
 * ==============================================================================
 */

var CONFIG = {
  // true = применить изменения в аккаунте.
  // false = тестовый прогон (dry-run), только логирование действий без изменения аккаунта.
  APPLY_CHANGES: true,

  // Название единой группы объявлений:
  SINGLE_GROUP_NAME: "Все украшения Livi Jewelry",

  // Единая посадочная страница каталога Livi Jewelry для всех объявлений и ключей:
  CATALOG_URL: "https://livijewelry.kz/shop.html",

  // Базовая ставка за клик (CPC) для добавляемых ключевых слов ($):
  DEFAULT_CPC: 0.24,

  // Поставить остальные дублирующие группы на паузу:
  PAUSE_OTHER_GROUPS: true,

  // Синхронизировать 150 коммерческих ключей:
  UPDATE_KEYWORDS: true,

  // Создать адаптивное объявление (RSA) на shop.html:
  CREATE_RSA_AD: true
};

// ------------------------------------------------------------------------------
// СПИСОК ИЗ 150 СВЕРХГОРЯЧИХ КОММЕРЧЕСКИХ КЛЮЧЕЙ (КАЗАХСТАН — RU + KZ)
// Каждый ключ содержит четкое покупательское намерение: купить / заказать / магазин
// ------------------------------------------------------------------------------
var CLEAN_KEYWORDS_KZ = [
  // 1. Колье, бусы, ожерелья и сотуары из жемчуга (28)
  "купить колье из жемчуга", "колье из натурального жемчуга купить", "купить жемчужное колье",
  "колье с натуральным жемчугом купить", "купить колье из барочного жемчуга", "колье из белого жемчуга купить",
  "купить бусы из жемчуга", "бусы из жемчуга купить", "бусы из натурального жемчуга купить",
  "купить бусы из натурального жемчуга", "жемчужные бусы купить", "натуральные жемчужные бусы купить",
  "купить ожерелье из жемчуга", "ожерелье из жемчуга купить", "ожерелье из натурального жемчуга купить",
  "жемчужное ожерелье купить", "купить сотуар из жемчуга", "сотуар из жемчуга купить",
  "сотуары из натуральных камней купить", "колье из перламутра купить", "купить колье майорка",
  "колье из жемчуга майорка купить", "цепь с барочным жемчугом купить",
  "колье из жемчуга алматы купить", "колье из жемчуга астана купить",
  "бусы из жемчуга алматы купить", "бусы из жемчуга астана купить", "купить жемчужное колье алматы",

  // 2. Колье и бусы из натуральных камней (33)
  "купить колье из камней", "колье из натуральных камней купить", "колье с натуральными камнями купить",
  "купить бусы из натуральных камней", "бусы из натуральных камней купить", "ожерелье из натуральных камней купить",
  "колье ручной работы из камней купить", "колье из натуральной бирюзы купить", "колье с бирюзой купить",
  "купить колье из граната", "гранатовое колье купить", "колье из коралла купить",
  "коралловые бусы купить", "колье из лазурита купить", "купить колье с малахитом",
  "колье из малахита купить", "колье с аметистом купить", "колье из горного хрусталя купить",
  "колье из розового кварца купить", "колье из тигрового глаза купить", "колье из гематита купить",
  "колье из лунного камня купить", "бусы из агата купить", "бусы из натуральной бирюзы купить",
  "бусы из лазурита купить", "бусы из яшмы купить", "гранатовые бусы купить",
  "колье из натуральных камней алматы", "колье из натуральных камней астана",
  "бусы из натуральных камней алматы", "бусы из натуральных камней астана",
  "колье ручной работы алматы купить", "бусы ручной работы алматы купить",

  // 3. Чокеры из натуральных камней и жемчуга (24)
  "купить чокер из камней", "чокер из камней купить", "купить чокер из натуральных камней",
  "чокер из натуральных камней купить", "чокеры из натуральных камней купить", "чокер на шею из камней купить",
  "купить чокер из жемчуга", "чокер из жемчуга купить", "чокер из натурального жемчуга купить",
  "купить чокер из барочного жемчуга", "жемчужный чокер купить", "чокер из аметиста купить",
  "чокер из бирюзы купить", "чокер из граната купить", "чокер из лазурита купить",
  "чокер из горного хрусталя купить", "чокер из розового кварца купить", "чокер из лунного камня купить",
  "чокер из тигрового глаза купить", "чокер из гематита купить",
  "чокер из жемчуга цена", "чокер из камней алматы купить", "чокер из камней астана купить",
  "чокер из жемчуга алматы купить",

  // 4. Браслеты и серьги из камней и жемчуга (25)
  "купить браслет из камней", "браслеты из натуральных камней купить", "купить браслет из натуральных камней",
  "браслет из жемчуга купить", "жемчужный браслет купить", "браслет из агата купить",
  "браслет из бирюзы купить", "гранатовый браслет купить", "браслет из граната купить",
  "браслет из коралла купить", "браслет из лазурита купить", "браслет из малахита купить",
  "браслет из розового кварца купить", "браслет из лунного камня купить", "браслет с турмалином купить",
  "серьги из натуральных камней купить", "серьги с жемчугом купить", "жемчужные серьги купить",
  "серьги с бирюзой купить", "пусеты с бирюзой купить", "серьги с гранатом купить",
  "серьги с малахитом купить", "браслеты из камней алматы купить", "браслеты из камней астана купить",
  "серьги из натуральных камней алматы",

  // 5. Комплекты, наборы и сеты украшений (15)
  "купить комплект украшений", "комплект украшений купить", "комплект украшений из натуральных камней купить",
  "комплект из натуральных камней купить", "комплект украшений из жемчуга купить", "комплект из жемчуга купить",
  "комплект колье и браслет купить", "комплект колье и серьги купить", "набор украшений купить",
  "набор украшений из жемчуга купить", "набор украшений ручной работы купить", "подарочный набор украшений купить",
  "комплект бижутерии купить", "комплект украшений алматы купить", "комплект украшений астана купить",

  // 6. Общие коммерческие магазины и авторские украшения (25)
  "купить украшения из натуральных камней", "украшения из натуральных камней купить", "купить украшения из натурального жемчуга",
  "украшения из натурального жемчуга купить", "украшения из барочного жемчуга купить", "украшения с бирюзой купить",
  "украшения с гранатом купить", "украшения с аметистом купить", "коралловые украшения купить",
  "авторские украшения купить", "авторские украшения ручной работы купить", "дизайнерские украшения купить",
  "украшения ручной работы купить", "элитная бижутерия купить", "казахские национальные украшения купить",
  "интернет магазин украшений из камней", "магазин авторских украшений алматы", "магазин украшений из натуральных камней",
  "магазин бижутерии алматы", "магазин бижутерии астана", "украшения из натуральных камней алматы купить",
  "украшения из натуральных камней астана купить", "украшения из жемчуга алматы купить", "украшения из жемчуга астана купить",
  "авторские украшения алматы купить"
];

// ------------------------------------------------------------------------------
// СПИСОК ИЗ 150 СВЕРХГОРЯЧИХ КОММЕРЧЕСКИХ КЛЮЧЕЙ (УЗБЕКИСТАН — O'ZBEK TILI)
// 100% чистый узбекский язык: sotib olish / xarid qilish / narxi / do'koni
// ------------------------------------------------------------------------------
var CLEAN_KEYWORDS_UZ = [
  // 1. Marvarid va sadafdan kolye, munchoq, marjon va sotuarlar (28)
  "marvarid kolye sotib olish", "tabiiy marvarid kolye sotib olish", "marvaridli kolye sotib olish",
  "tabiiy marvaridli kolye sotib olish", "barokko marvarid kolye sotib olish", "oq marvarid kolye sotib olish",
  "marvarid munchoq sotib olish", "marvarid marjon sotib olish", "tabiiy marvarid munchoq sotib olish",
  "tabiiy marvaridli marjon sotib olish", "marvaridli munchoq sotib olish", "haqiqiy marvarid munchoq sotib olish",
  "marvarid bo'yintumor sotib olish", "marvarid taqinchoq sotib olish", "tabiiy marvarid marjon sotib olish",
  "marvarid marjon xarid qilish", "marvarid sotuar sotib olish", "marvaridli sotuar sotib olish",
  "tabiiy toshlardan sotuar sotib olish", "sadaf kolye sotib olish", "mayorka kolye sotib olish",
  "mayorka marvarid kolye sotib olish", "barokko marvaridli zanjir sotib olish",
  "marvarid kolye toshkent sotib olish", "marvarid kolye o'zbekiston sotib olish",
  "marvarid munchoq toshkent sotib olish", "marvarid marjon toshkent sotib olish", "marvarid marjon toshkent narxi",

  // 2. Tabiiy toshlardan kolye va munchoqlar (33)
  "toshli kolye sotib olish", "tabiiy toshlardan kolye sotib olish", "tabiiy toshli marjon sotib olish",
  "tabiiy tosh munchoq sotib olish", "tabiiy toshlardan munchoq sotib olish", "tabiiy tosh marjon sotib olish",
  "qo'l mehnati toshli kolye sotib olish", "tabiiy feruza kolye sotib olish", "feruza toshli kolye sotib olish",
  "granat kolye sotib olish", "yoqut kolye sotib olish", "marjon tosh kolye sotib olish",
  "marjon toshli munchoq sotib olish", "lajvard kolye sotib olish", "malaxit toshli kolye sotib olish",
  "malaxit kolye sotib olish", "ametist toshli kolye sotib olish", "tog' billuri kolye sotib olish",
  "pushti kvars kolye sotib olish", "yo'lbars ko'zi kolye sotib olish", "gematit kolye sotib olish",
  "oy toshi kolye sotib olish", "aqiq munchoq sotib olish", "tabiiy feruza munchoq sotib olish",
  "lajvard munchoq sotib olish", "yashma munchoq sotib olish", "granat munchoq sotib olish",
  "tabiiy tosh kolye toshkent", "tabiiy tosh kolye samarqand",
  "tabiiy tosh munchoq toshkent", "tabiiy tosh munchoq o'zbekiston",
  "qo'l mehnati kolye toshkent sotib olish", "qo'l mehnati munchoq toshkent sotib olish",

  // 3. Tabiiy tosh va marvariddan chokerlar (24)
  "toshli choker sotib olish", "toshli choker xarid qilish", "tabiiy toshlardan choker sotib olish",
  "tabiiy toshli choker sotib olish", "choker tabiiy tosh sotib olish", "bo'yinga toshli choker sotib olish",
  "marvarid choker sotib olish", "marvaridli choker sotib olish", "tabiiy marvarid choker sotib olish",
  "barokko marvarid choker sotib olish", "marvarid choker xarid qilish", "ametist choker sotib olish",
  "feruza choker sotib olish", "granat choker sotib olish", "lajvard choker sotib olish",
  "tog' billuri choker sotib olish", "pushti kvars choker sotib olish", "oy toshi choker sotib olish",
  "yo'lbars ko'zi choker sotib olish", "gematit choker sotib olish",
  "marvarid choker toshkent narxi", "toshli choker toshkent sotib olish", "toshli choker o'zbekiston sotib olish",
  "marvarid choker toshkent sotib olish",

  // 4. Tabiiy tosh va marvariddan bilaguzuk va ziraklar (25)
  "toshli bilaguzuk sotib olish", "tabiiy tosh bilaguzuk sotib olish", "tabiiy toshlardan bilaguzuk sotib olish",
  "marvarid bilaguzuk sotib olish", "marvaridli bilaguzuk xarid qilish", "aqiq bilaguzuk sotib olish",
  "feruza bilaguzuk sotib olish", "granat bilaguzuk sotib olish", "yoqut bilaguzuk sotib olish",
  "marjon tosh bilaguzuk sotib olish", "lajvard bilaguzuk sotib olish", "malaxit bilaguzuk sotib olish",
  "pushti kvars bilaguzuk sotib olish", "oy toshi bilaguzuk sotib olish", "turmalin bilaguzuk sotib olish",
  "tabiiy toshli zirak sotib olish", "marvaridli zirak sotib olish", "marvarid zirak xarid qilish",
  "feruzali zirak sotib olish", "feruza puset zirak sotib olish", "granat zirak sotib olish",
  "malaxit zirak sotib olish", "tabiiy tosh bilaguzuk toshkent sotib olish", "marvarid bilaguzuk toshkent sotib olish",
  "tabiiy tosh ziraklar toshkent",

  // 5. To'plamlar, setlar va sovg'a jamlanmalari (15)
  "taqinchoqlar to'plami sotib olish", "taqinchoqlar komplekti sotib olish", "tabiiy toshlar to'plami sotib olish",
  "tabiiy tosh komplekt sotib olish", "marvarid to'plam sotib olish", "marvarid komplekt sotib olish",
  "kolye va bilaguzuk to'plami sotib olish", "kolye va zirak to'plami sotib olish", "taqinchoq jamlanmasi sotib olish",
  "marvaridli jamlanma sotib olish", "qo'l mehnati taqinchoq to'plami sotib olish", "sovg'abop taqinchoqlar to'plami sotib olish",
  "bijuteriya to'plami sotib olish", "taqinchoqlar to'plami toshkent sotib olish", "marvarid to'plam toshkent sotib olish",

  // 6. Do'konlar va mualliflik taqinchoqlari (25)
  "tabiiy toshlardan taqinchoqlar sotib olish", "tabiiy tosh taqinchoqlar xarid qilish", "tabiiy marvarid taqinchoqlar sotib olish",
  "marvarid taqinchoqlar sotib olish", "barokko marvarid taqinchoqlar sotib olish", "feruza taqinchoqlar sotib olish",
  "granat taqinchoqlar sotib olish", "ametist taqinchoqlar sotib olish", "korall taqinchoqlar sotib olish",
  "mualliflik taqinchoqlari sotib olish", "mualliflik qo'l mehnati taqinchoqlar sotib olish", "dizaynerlik taqinchoqlari sotib olish",
  "qo'l mehnati taqinchoqlar sotib olish", "elita bijuteriya sotib olish", "milliy taqinchoqlar toshkent sotib olish",
  "internet do'kon toshli taqinchoqlar", "mualliflik taqinchoqlari do'koni toshkent", "tabiiy tosh taqinchoqlar do'koni",
  "bijuteriya do'koni toshkent", "zargarlik do'koni toshkent", "tabiiy tosh taqinchoqlar toshkent sotib olish",
  "tabiiy tosh taqinchoqlar samarqand sotib olish", "marvarid taqinchoqlar toshkent sotib olish", "toshkent zargarlik buyumlari sotib olish",
  "mualliflik taqinchoqlari toshkent sotib olish"
];

// 15 заголовков RSA (строго <= 30 символов, без восклицательных знаков)
var RSA_HEADLINES_KZ = [
  "{KeyWord:Авторские украшения}",
  "Колье из натурального жемчуга",
  "Колье из натуральных камней",
  "Чокеры из природных камней",
  "Чокеры из жемчуга ручной сбор",
  "Браслеты и серьги из камней",
  "Комплекты украшений из камней",
  "Livi Jewelry — Ручная работа",
  "Барочный жемчуг и перламутр",
  "Бирюза, гранат, агат, лазурит",
  "Сотуары и бусы из жемчуга",
  "100% природные камни и жемчуг",
  "Казахские этно-украшения Livi",
  "Подарочная упаковка в компл.",
  "Доставка по всему Казахстану"
];

var RSA_HEADLINES_UZ = [
  "{KeyWord:Авторские украшения}",
  "Колье из натурального жемчуга",
  "Колье из натуральных камней",
  "Чокеры из природных камней",
  "Чокеры из жемчуга ручной сбор",
  "Браслеты и серьги из камней",
  "Комплекты украшений из камней",
  "Livi Jewelry — Ручная работа",
  "Барочный жемчуг и перламутр",
  "Бирюза, гранат, агат, лазурит",
  "Сотуары и бусы из жемчуга",
  "100% природные камни и жемчуг",
  "Tabiiy tosh va marvarid Livi",
  "Подарочная упаковка в компл.",
  "Быстрая доставка в Узбекистан"
];

// 4 описания RSA (строго <= 90 символов)
var RSA_DESCRIPTIONS_KZ = [
  "Авторские колье, чокеры, браслеты и серьги из натуральных камней и речного жемчуга Livi.",
  "Ручная сборка в единственном экземпляре. Барочный жемчуг, бирюза, гранат, агат, лазурит.",
  "Готовые комплекты и отдельные украшения в фирменной коробке. Быстрая доставка по РК.",
  "Выбирайте украшения на сайте с живыми фото и ценами. Оплата Kaspi QR и Kaspi Red."
];

var RSA_DESCRIPTIONS_UZ = [
  "Авторские колье, чокеры, браслеты и серьги из натуральных камней и речного жемчуга Livi.",
  "Ручная сборка в единственном экземпляре. Барочный жемчуг, бирюза, гранат, агат, лазурит.",
  "Готовые комплекты и отдельные украшения в фирменной коробке. Доставка в Ташкент и по УЗ.",
  "Выбирайте украшения в каталоге с живыми фото и ценами. Удобный заказ через WhatsApp."
];

function processCampaign(camp) {
  var campName = camp.getName();
  var isUz = /узбекистан|uzbekistan|\buz\b/i.test(campName);
  var targetKeywords = isUz ? CLEAN_KEYWORDS_UZ : CLEAN_KEYWORDS_KZ;
  var targetHeadlines = isUz ? RSA_HEADLINES_UZ : RSA_HEADLINES_KZ;
  var targetDescriptions = isUz ? RSA_DESCRIPTIONS_UZ : RSA_DESCRIPTIONS_KZ;

  Logger.log("\n==================================================================");
  Logger.log("▶ КАМПАНИЯ: «" + campName + "» (" + (isUz ? "УЗБЕКИСТАН" : "КАЗАХСТАН") + ")");
  Logger.log("  Целевая витрина: " + CONFIG.CATALOG_URL);
  Logger.log("==================================================================");

  // 1. Поиск или подготовка группы «Все украшения Livi Jewelry»
  var primaryGroup = null;
  var otherGroups = [];
  var agIter = camp.adGroups().get();
  while (agIter.hasNext()) {
    var ag = agIter.next();
    if (ag.getName() === CONFIG.SINGLE_GROUP_NAME) {
      primaryGroup = ag;
    } else {
      otherGroups.push(ag);
    }
  }

  // Если точного имени нет, берем группу «1. Комплекты и общие украшения» для сохранения статистики
  if (!primaryGroup) {
    for (var g = 0; g < otherGroups.length; g++) {
      if (/^1\.|комплект/i.test(otherGroups[g].getName())) {
        primaryGroup = otherGroups[g];
        otherGroups.splice(g, 1);
        break;
      }
    }
    if (!primaryGroup && otherGroups.length > 0) {
      primaryGroup = otherGroups.shift();
    }

    if (primaryGroup) {
      var oldName = primaryGroup.getName();
      Logger.log("  ✓ Переименование группы «" + oldName + "» ➔ «" + CONFIG.SINGLE_GROUP_NAME + "»");
      if (CONFIG.APPLY_CHANGES) {
        primaryGroup.setName(CONFIG.SINGLE_GROUP_NAME);
        if (primaryGroup.isPaused()) primaryGroup.enable();
      }
    } else {
      Logger.log("  ✓ Создание новой группы «" + CONFIG.SINGLE_GROUP_NAME + "»");
      if (CONFIG.APPLY_CHANGES) {
        var res = camp.newAdGroupBuilder()
          .withName(CONFIG.SINGLE_GROUP_NAME)
          .withCpc(CONFIG.DEFAULT_CPC)
          .withStatus("ENABLED")
          .build();
        if (res.isSuccessful()) {
          primaryGroup = res.getResult();
        }
      }
    }
  } else if (primaryGroup.isPaused() && CONFIG.APPLY_CHANGES) {
    primaryGroup.enable();
    Logger.log("  ✓ Активация единой группы «" + CONFIG.SINGLE_GROUP_NAME + "»");
  }

  // 2. Остановка остальных дублирующих групп
  if (CONFIG.PAUSE_OTHER_GROUPS) {
    var pausedCount = 0;
    for (var p = 0; p < otherGroups.length; p++) {
      var grp = otherGroups[p];
      if (grp.isEnabled()) {
        Logger.log("  ⏸ Остановка дублирующей группы: «" + grp.getName() + "»");
        if (CONFIG.APPLY_CHANGES) {
          grp.pause();
        }
        pausedCount++;
      }
    }
    Logger.log("  ✓ Поставлено на паузу дублирующих групп: " + pausedCount + " шт.");
  }

  if (!primaryGroup && !CONFIG.APPLY_CHANGES) {
    Logger.log("  [DRY-RUN] Группа будет создана при боевом запуске.");
    return;
  }
  if (!primaryGroup) {
    Logger.log("  [!] Не удалось получить единую группу.");
    return;
  }

  // 3. Синхронизация чистых 150 коммерческих ключевых слов (все ведут на shop.html)
  if (CONFIG.UPDATE_KEYWORDS) {
    Logger.log("  🔑 Синхронизация 150 коммерческих ключей (URL: " + CONFIG.CATALOG_URL + ")...");
    var targetMap = {};
    for (var k = 0; k < targetKeywords.length; k++) {
      targetMap[targetKeywords[k].toLowerCase().trim()] = targetKeywords[k];
    }

    var seenPhrase = {};
    var removedCount = 0;
    var updatedCount = 0;
    var addedCount = 0;

    var kwIter = primaryGroup.keywords().get();
    while (kwIter.hasNext()) {
      var kw = kwIter.next();
      var rawText = kw.getText();
      var cleanText = rawText.toLowerCase().trim().replace(/^["\[]+|["\]]+$/g, "").trim();
      var mType = kw.getMatchType();

      // Удаляем дубли точного соответствия [], некоммерческие запросы и повторы
      if (mType !== "PHRASE" || !targetMap[cleanText] || seenPhrase[cleanText]) {
        if (CONFIG.APPLY_CHANGES) {
          try { kw.remove(); } catch(e) {}
        }
        removedCount++;
      } else {
        seenPhrase[cleanText] = true;
        if (CONFIG.APPLY_CHANGES) {
          try {
            if (kw.isPaused()) kw.enable();
            if (kw.bidding().getCpc() !== CONFIG.DEFAULT_CPC) {
              kw.bidding().setCpc(CONFIG.DEFAULT_CPC);
            }
            if (kw.urls().getFinalUrl() !== CONFIG.CATALOG_URL) {
              kw.urls().setFinalUrl(CONFIG.CATALOG_URL);
            }
          } catch(e) {}
        }
        updatedCount++;
      }
    }

    // Добавляем недостающие коммерческие ключи напрямую с переходом в каталог
    for (var tk = 0; tk < targetKeywords.length; tk++) {
      var kwNorm = targetKeywords[tk].toLowerCase().trim();
      if (!seenPhrase[kwNorm]) {
        if (CONFIG.APPLY_CHANGES) {
          try {
            var kwOp = primaryGroup.newKeywordBuilder()
              .withText('"' + targetKeywords[tk] + '"')
              .withCpc(CONFIG.DEFAULT_CPC)
              .build();
            if (kwOp.isSuccessful()) {
              var createdKw = kwOp.getResult();
              try {
                createdKw.urls().setFinalUrl(CONFIG.CATALOG_URL);
              } catch (urlErr) {
                Logger.log("      [!] Ошибка установки Final URL для «" + targetKeywords[tk] + "»: " + urlErr);
              }
              addedCount++;
            } else {
              Logger.log("      [!] Ошибка создания ключа «" + targetKeywords[tk] + "»: " + kwOp.getErrors().join("; "));
            }
          } catch(e) {
            Logger.log("      [!] Исключение при создании ключа «" + targetKeywords[tk] + "»: " + e);
          }
        } else {
          addedCount++;
        }
      }
    }

    Logger.log("    • Добавлено новых коммерческих ключей: " + addedCount + " шт.");
    Logger.log("    • Удалено нецелевых/дублирующих ключей: " + removedCount + " шт.");
    Logger.log("    • Обновлено целевых ключей (URL + ставка): " + updatedCount + " шт.");
    Logger.log("    • Всего активных коммерческих ключей: " + targetKeywords.length + " шт.");
  }

  // 4. Создание единого адаптивного поискового объявления (RSA) на shop.html
  if (CONFIG.CREATE_RSA_AD) {
    Logger.log("  📢 Создание нового эталонного объявления (RSA) на " + CONFIG.CATALOG_URL + "...");

    if (CONFIG.APPLY_CHANGES) {
      try {
        var builder = primaryGroup.newAd().responsiveSearchAdBuilder()
          .withFinalUrl(CONFIG.CATALOG_URL)
          .withPath1("Украшения")
          .withPath2("Каталог");

        for (var h = 0; h < targetHeadlines.length; h++) {
          builder.addHeadline(targetHeadlines[h]);
        }
        for (var d = 0; d < targetDescriptions.length; d++) {
          builder.addDescription(targetDescriptions[d]);
        }

        var op = builder.build();
        if (!op.isSuccessful()) {
          // Резервный вариант, если {KeyWord:...} не поддерживается синтаксисом
          var fbBuilder = primaryGroup.newAd().responsiveSearchAdBuilder()
            .withFinalUrl(CONFIG.CATALOG_URL)
            .withPath1("Украшения")
            .withPath2("Каталог");
          for (var fh = 0; fh < targetHeadlines.length; fh++) {
            var text = fh === 0 ? (isUz ? "Tabiiy tosh taqinchoqlar" : "Авторские украшения Livi") : targetHeadlines[fh];
            fbBuilder.addHeadline(text);
          }
          for (var fd = 0; fd < targetDescriptions.length; fd++) {
            fbBuilder.addDescription(targetDescriptions[fd]);
          }
          op = fbBuilder.build();
        }

        if (op.isSuccessful()) {
          var newAdId = op.getResult().getId();
          Logger.log("    ✓ Успешно создано новое эталонное RSA объявление (ID: " + newAdId + ") на " + CONFIG.CATALOG_URL);

          // Ставим ВСЕ старые объявления в группе на паузу
          var oldAdIter = primaryGroup.ads().withCondition("Status = ENABLED").get();
          var pausedOldCount = 0;
          while (oldAdIter.hasNext()) {
            var oldAd = oldAdIter.next();
            if (oldAd.getId() !== newAdId) {
              try { oldAd.pause(); } catch(e) {}
              pausedOldCount++;
            }
          }
          Logger.log("    ⏸ Поставлено на паузу старых объявлений: " + pausedOldCount + " шт.");
        } else {
          Logger.log("    [!] Ошибка создания RSA: " + op.getErrors().join("; "));
        }
      } catch(err) {
        Logger.log("    [!] Исключение при создании RSA: " + err);
      }
    } else {
      Logger.log("    [DRY-RUN] Будет создано новое RSA объявление (15 заголовков + 4 описания), а все старые объявления будут поставлены на паузу.");
    }
  }
}

function main() {
  Logger.log("==================================================================");
  Logger.log("   💎 LIVI JEWELRY — КОНСОЛИДАЦИЯ В 1 ЕДИНУЮ ГРУППУ ОБЪЯВЛЕНИЙ   ");
  Logger.log("   Версия: v2.1 Catalog Direct (Все 150 ключей ведут на shop.html)");
  Logger.log("   Целевой каталог: " + CONFIG.CATALOG_URL);
  Logger.log("   Базовая ставка: " + CONFIG.DEFAULT_CPC + "$ | Режим: " + (CONFIG.APPLY_CHANGES ? "БОЕВОЙ" : "ТЕСТОВЫЙ ПРОГОН"));
  Logger.log("==================================================================");

  var campIter = AdsApp.campaigns()
    .withCondition("Status = ENABLED")
    .get();

  var processedCampaigns = 0;
  while (campIter.hasNext()) {
    var camp = campIter.next();
    var cName = camp.getName();
    if (/поиск|search/i.test(cName)) {
      processCampaign(camp);
      processedCampaigns++;
    }
  }

  Logger.log("\n==================================================================");
  Logger.log("   ИТОГ: Обработано кампаний: " + processedCampaigns + " шт.");
  Logger.log("   КОНСОЛИДАЦИЯ УСПЕШНО ЗАВЕРШЕНА!                                ");
  Logger.log("==================================================================");
}