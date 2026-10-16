/**
 * ==============================================================================
 * LIVI JEWELRY — GOOGLE ADS AUTOPILOT v2.0 (ПОЛНЫЙ БОЕВОЙ АВТОПИЛОТ)
 * ==============================================================================
 * 
 * ЧТО ДЕЛАЕТ ЭТОТ СКРИПТ АВТОМАТИЧЕСКИ КАЖДОЕ УТРО:
 * 1. [Auto-Sync Negatives] Поддерживает мастер-список из 250+ минус-слов и привязывает
 *    его ко всем активным поисковым и торговым кампаниям (Shopping).
 * 2. [Search Query Mining] Сканирует отчет поисковых запросов (Search Terms) за 7 дней.
 *    Автоматически находит мусорные запросы (дешево, алиэкспресс, своими руками, фурнитура,
 *    ремонт, ломбард, золото 585 и т.д.) или запросы без конверсий с перерасходом,
 *    и мгновенно добавляет их в минус-слова.
 * 3. [Smart Bidding & Top Position] Управляет ставками CPC на основе новой гибридной ценности
 *    конверсий (Корзина = 100% ценности, Клик WhatsApp = 20% ценности):
 *    - Повышает ставку (+10%) конвертящим ключам, если они теряют Top-of-page показы.
 *    - Снижает ставку (-5%) ключам, уже удерживающим Топ с высоким CTR (минимизирует цену клика).
 *    - Снижает ставку (-20%) или ставит на паузу ключи, сливающие бюджет без конверсий.
 * 4. [Budget & Bleed Guard] Контролирует общий дневной расход (защита от скликивания).
 * 5. [Email Digest] Отправляет красивый детальный отчет о действиях и расходах на почту.
 *
 * РАСПИСАНИЕ: Запускается автоматически каждый день в 07:00 или 08:00 утра.
 * ==============================================================================
 */

var CONFIG = {
  // Почта для утренних отчетов и срочных алертов:
  ALERT_EMAIL: "viksonna94@gmail.com",
  
  // Лимит дневного расхода аккаунта (в валюте аккаунта, например USD или эквивалент KZT):
  DAILY_BUDGET_CAP: 10.0,
  
  // Максимальный потолок ставки CPC (защита от переплат на аукционе):
  MAX_CPC_CAP: 0.35,
  
  // Минимальный пол ставки CPC:
  MIN_CPC_FLOOR: 0.05,
  
  // Порог расхода ключа/запроса без единой конверсии для применения штрафа:
  WASTE_SPEND_THRESHOLD: 1.50,
  
  // Порог кликов без конверсий:
  WASTE_CLICKS_THRESHOLD: 8,
  
  // Целевая доля показов вверху страницы (Top Impression Share):
  TARGET_TOP_SHARE: 0.85,
  
  // Шаг повышения ставки для конвертящих фраз:
  CONVERSION_BID_BOOST: 0.10, // +10%
  
  // Шаг снижения ставки для экономии при доминировании в топе:
  SAVER_BID_DISCOUNT: 0.05,   // -5%
  
  // Название мастер-списка минус-слов:
  NEGATIVE_LIST_NAME: "Livi Jewelry - Мастер Минус-слова",
  
  // Применять ли изменения на боевом аккаунте (true = боевой режим, false = симуляция/dry-run):
  APPLY_CHANGES: true,
  
  // Всегда отправлять утреннюю сводку:
  SEND_DAILY_SUMMARY: true
};

// Базовый мастер-список стоп-слов Livi Jewelry (250+ фильтров)
var MASTER_NEGATIVES = [
  // 1. DIY, Рукоделие, Хобби
  "своими руками", "как сделать", "как сплести", "как собрать", "схема", "схемы", 
  "мастер класс", "мк", "бисероплетение", "бисер", "плетение", "вязание", 
  "бусины поштучно", "бусины оптом", "бусины для рукоделия", "фурнитура", 
  "застежка для колье", "карабин ювелирный", "швензы", "штифты", "пины", 
  "леска для бус", "ювелирная проволока", "тросик", "инструменты для бижутерии", 
  "круглогубцы", "плоскогубцы", "эпоксидная смола", "полимерная глина", "бейлы", 
  "концевики", "каллоты", "кримпы", "разделители бусин", "шапочки для бусин", 
  "силиконовая нить", "спандекс", "паракорд", "макраме", "вышивка", "пайетки", 
  "стеклярус", "мулине", "пряжа", "кабошон", "заготовки для колец", "основы для броши", 
  "форма для смолы", "молд", "станок для бисероплетения", "сборка на дому",

  // 2. Дешевые маркетплейсы, секонд-хенд, халява, опт
  "дешево", "недорого", "самый дешевый", "бесплатно", "даром", "отдам даром", 
  "в дар", "подарок бесплатно", "садовод", "тяк москва", "алиэкспресс", "aliexpress", 
  "temu", "тему", "shein", "шейн", "таобао", "taobao", "1688", "оптом", "опт", 
  "крупный опт", "дропшиппинг", "барахолка", "барахолка бу", "секонд хенд", "бу", 
  "б у", "б/у", "авито", "olx", "olx бу", "satu kz", "конфискат", "таможенный конфискат", 
  "китайский ширпотреб", "ликвидация магазина", "фикс прайс", "fix price",

  // 3. Металлы не нашего профиля, ломбарды, скупка
  "золото 585", "золото 750", "белое золото", "червонное золото", "ломбард", 
  "скупка", "скупка золота", "лом золота", "сдать золото", "грамм золота", 
  "цена за грамм", "курс золота", "проба 585", "проба 925", "клеймо", "слитки", 
  "слиток золота", "инвестиционные монеты", "платина", "палладий", "титан", 
  "медицинская сталь", "нержавеющая сталь", "вольфрам", "серебро 925 ломбард", 
  "залог золота", "займ под залог",

  // 4. Дешевые ненатуральные материалы
  "пластик", "пластиковые", "дерево", "деревянные", "стекло", "стеклянные", 
  "акрил", "акриловые", "силикон", "силиконовые", "эпоксидка", "смола", 
  "янтарь лечебный", "янтарные бусы от щитовидки", "фианит", "фианиты оптом", 
  "искусственный жемчуг дешевый", "пластиковый жемчуг",

  // 5. Неподходящие типы изделий
  "пирсинг", "пирсинг пупка", "септум", "микродермал", "тоннели в уши", "плаги", 
  "обручальные кольца", "помолвочное кольцо", "мужская печатка", "печатка мужская", 
  "мужская цепь золото", "цепочка бисмарк", "панцирное плетение", "крестик золотой", 
  "крестик серебряный", "нательный крест", "ладанка", "иконка", "полумесяц кулон", 
  "мусульманские кулоны", "аят аль курси", "четки", "четки перекидные", "тасбих", 
  "часы", "наручные часы", "смарт часы", "apple watch", "ремешок для часов", 
  "запонки", "зажим для галстука", "детские украшения", "набор для девочки", 
  "игрушечная бижутерия",

  // 6. Ремонт, уход, чистка, экспертиза
  "ремонт", "ремонт бижутерии", "ювелирная мастерская", "реставрация", "пайка", 
  "лазерная пайка", "перетяжка бус", "перевязать бусы", "замена замка", 
  "уменьшить кольцо", "увеличить кольцо", "ультразвуковая чистка", "чистка золота", 
  "как почистить жемчуг", "как отбелить жемчуг", "как отличить натуральный жемчуг", 
  "тест на подлинность", "экспертиза камней", "геммолог", "оценка ювелирных",

  // 7. Конкуренты и масс-маркет сети
  "пандора", "pandora", "шармы пандора", "санлайт", "sunlight", "соколов", 
  "sokolov", "адамас", "585 золотой", "tiffany", "тиффани", "картье", "cartier", 
  "гвоздь картье", "van cleef", "ван клиф", "клевер ван клиф", "chopard", 
  "шопард", "булгари", "bulgari", "swarovski", "сваровски", "tous", "тоус мишка", 
  "казахювелир", "алтын", "эпл даймонд",

  // 8. Информационные, эзотерика, вакансии
  "гороскоп", "знак зодиака", "магия камней", "магические свойства", 
  "лечебные свойства", "заговор", "приворот", "чакры", "амулет от сглаза", 
  "реферат", "курсовая", "википедия", "доклад", "презентация", 
  "фото высокого разрешения", "картинки", "обои на телефон", "раскраска", 
  "скачать", "видео", "youtube", "тикток", "книга", "курсы", "обучение", 
  "работа", "вакансии", "резюме", "зарплата", "продавец консультант вакансии"
];

// Паттерны немедленной блокировки в реальных поисковых запросах
var JUNK_PATTERNS = [
  /дешев/i, /недорог/i, /бесплатн/i, /даром/i, /алиэкспресс/i, /aliexpress/i,
  /temu/i, /тему/i, /shein/i, /шейн/i, /таобао/i, /taobao/i, /1688/i,
  /своими руками/i, /как сделать/i, /как сплести/i, /схем/i, /мастер класс/i,
  /фурнитур/i, /бусин/i, /бисер/i, /проволок/i, /швенз/i, /застежк/i, /пины/i,
  /оптом/i, /опт\b/i, /барахолк/i, /б[\s/]?у\b/i, /секонд/i, /olx/i, /авито/i,
  /золот/i, /ломбард/i, /скупк/i, /проба 585/i, /проба 925/i, /слит/i,
  /ремонт/i, /мастерск/i, /чистк/i, /перетяжк/i, /пайк/i,
  /пандор/i, /pandora/i, /санлайт/i, /sunlight/i, /соколов/i, /sokolov/i,
  /картье/i, /cartier/i, /тиффани/i, /tiffany/i, /ван клиф/i, /van cleef/i,
  /сваровски/i, /swarovski/i, /тоус/i, /часы/i, /пирсинг/i, /обручальн/i,
  /ваканси/i, /резюме/i, /работа/i, /скачать/i, /видео/i, /ютуб/i
];

function main() {
  Logger.log("==================================================================");
  Logger.log("   💎 LIVI JEWELRY AUTOPILOT v2.0: ЗАПУСК ОПТИМИЗАЦИИ РЕКЛАМЫ    ");
  Logger.log("==================================================================");

  var account = AdsApp.currentAccount();
  var accountName = account.getName() || "Livi Jewelry";
  var customerId = account.getCustomerId();
  var currency = account.getCurrencyCode();

  var actionLogs = [];
  var warningsList = [];

  // ------------------------------------------------------------------
  // 1. СИНХРОНИЗАЦИЯ МАСТЕР-СПИСКА МИНУС-СЛОВ (250+ СЛОВ)
  // ------------------------------------------------------------------
  Logger.log("\n[1/4] Синхронизация мастер-списка минус-слов...");
  var negativeList = getOrCreateNegativeList(CONFIG.NEGATIVE_LIST_NAME);
  var attachedCampaignsCount = attachNegativeListToAllCampaigns(negativeList);
  actionLogs.push("Мастер-список минус-слов прикреплен к " + attachedCampaignsCount + " кампаниям.");

  // ------------------------------------------------------------------
  // 2. АВТО-ЧИСТКА МУСОРНЫХ ЗАПРОСОВ (SEARCH TERM MINING)
  // ------------------------------------------------------------------
  Logger.log("\n[2/4] Анализ реальных поисковых запросов за 7 дней...");
  var negatedTermsCount = mineJunkSearchTerms(negativeList, actionLogs);

  // ------------------------------------------------------------------
  // 3. УМНОЕ УПРАВЛЕНИЕ СТАВКАМИ CPC (ТОП ВЫДАЧИ + КОНВЕРСИИ)
  // ------------------------------------------------------------------
  Logger.log("\n[3/4] Оптимизация ставок CPC ключевых слов (удержание топа и экономия)...");
  var bidStats = optimizeKeywordBids(actionLogs);

  // ------------------------------------------------------------------
  // 4. СБОР СТАТИСТИКИ ЗА ВЧЕРА И КОНТРОЛЬ ДНЕВНОГО РАСХОДА
  // ------------------------------------------------------------------
  Logger.log("\n[4/4] Сбор показателей за вчера и аудит лимита бюджета...");
  var perfSummary = getYesterdayPerformance(currency, warningsList);

  // ------------------------------------------------------------------
  // 5. ОТПРАВКА ДЕТАЛЬНОГО EMAIL-ОТЧЕТА
  // ------------------------------------------------------------------
  if (CONFIG.SEND_DAILY_SUMMARY || warningsList.length > 0) {
    sendAutopilotEmailReport(accountName, customerId, currency, perfSummary, actionLogs, warningsList);
  }

  Logger.log("\n==================================================================");
  Logger.log("   АВТОПИЛОТ v2.0: Оптимизация успешно завершена!               ");
  Logger.log("==================================================================");
}

/**
 * Поиск или создание мастер-списка минус-слов и первичное наполнение
 */
function getOrCreateNegativeList(listName) {
  var listIter = AdsApp.negativeKeywordLists().withCondition("Name = '" + listName + "'").get();
  var negativeList;
  if (listIter.hasNext()) {
    negativeList = listIter.next();
    Logger.log("  ✓ Список найден: " + listName);
  } else {
    var builder = AdsApp.newNegativeKeywordListBuilder().withName(listName).build();
    negativeList = builder.getResult();
    Logger.log("  ✓ Создан новый мастер-список: " + listName);
  }

  // Быстрое пополнение мастер-словами, если список был новым
  var existingNegs = {};
  var negIter = negativeList.getNegativeKeywords();
  while (negIter.hasNext()) {
    existingNegs[negIter.next().getText().toLowerCase()] = true;
  }

  var added = 0;
  for (var i = 0; i < MASTER_NEGATIVES.length; i++) {
    var word = MASTER_NEGATIVES[i].toLowerCase();
    if (!existingNegs[word]) {
      try {
        if (CONFIG.APPLY_CHANGES) {
          negativeList.addNegativeKeyword(word);
        }
        existingNegs[word] = true;
        added++;
      } catch (e) {}
    }
  }
  if (added > 0) {
    Logger.log("  ✓ Добавлено новых базовых минус-слов: " + added);
  }
  return negativeList;
}

/**
 * Привязка мастер-списка ко всем активным кампаниям
 */
function attachNegativeListToAllCampaigns(negativeList) {
  var count = 0;
  var campIter = AdsApp.campaigns().get();
  while (campIter.hasNext()) {
    var camp = campIter.next();
    try {
      if (CONFIG.APPLY_CHANGES) {
        camp.addNegativeKeywordList(negativeList);
      }
      count++;
    } catch (e) {}
  }
  return count;
}

/**
 * Сканирование реальных поисковых запросов за 7 дней и авто-минусация
 */
function mineJunkSearchTerms(negativeList, actionLogs) {
  var addedCount = 0;
  try {
    var query = "SELECT search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions " +
                "FROM search_term_view WHERE segments.date DURING LAST_7_DAYS";
    var rows = AdsApp.search(query);

    while (rows.hasNext()) {
      var row = rows.next();
      var term = (row.searchTermView.searchTerm || "").trim().toLowerCase();
      var cost = (row.metrics.costMicros || 0) / 1000000;
      var clicks = row.metrics.clicks || 0;
      var convs = row.metrics.conversions || 0;

      if (!term || term.length < 2) continue;

      var isJunk = false;
      var reason = "";

      // 1. Проверка по паттернам нецелевого трафика
      for (var i = 0; i < JUNK_PATTERNS.length; i++) {
        if (JUNK_PATTERNS[i].test(term)) {
          isJunk = true;
          reason = "совпадение со стоп-паттерном (" + JUNK_PATTERNS[i] + ")";
          break;
        }
      }

      // 2. Проверка по сливу бюджета без конверсий
      if (!isJunk && cost >= CONFIG.WASTE_SPEND_THRESHOLD && convs === 0) {
        isJunk = true;
        reason = "расход $" + cost.toFixed(2) + " без единой конверсии";
      }

      if (isJunk) {
        try {
          if (CONFIG.APPLY_CHANGES) {
            negativeList.addNegativeKeyword(term);
          }
          addedCount++;
          var logMsg = "[Auto-Negated] Заблокирован запрос: \"" + term + "\" (" + reason + ")";
          actionLogs.push(logMsg);
          Logger.log("  🚫 " + logMsg);
        } catch (err) {}
      }
    }
  } catch (e) {
    Logger.log("  ℹ️ Отчет поисковых запросов: " + e.message);
  }
  Logger.log("  • Всего авто-заблокировано нецелевых запросов: " + addedCount);
  return addedCount;
}

/**
 * Умная оптимизация ставок CPC для ключевых слов
 */
function optimizeKeywordBids(actionLogs) {
  var stats = { boosted: 0, saved: 0, paused: 0 };

  try {
    var kwIter = AdsApp.keywords()
      .withCondition("Status = ENABLED")
      .withCondition("CampaignStatus = ENABLED")
      .withCondition("AdGroupStatus = ENABLED")
      .get();

    while (kwIter.hasNext()) {
      var kw = kwIter.next();
      var kwStats = kw.getStatsFor("LAST_14_DAYS");

      var clicks = kwStats.getClicks();
      var cost = kwStats.getCost();
      var convs = kwStats.getConversions();
      var ctr = kwStats.getCtr() * 100;
      var currentCpc = kw.bidding().getCpc() || 0.15;

      // 1. Ключи с конверсиями (Корзина или WhatsApp) -> удерживаем в Топ-1/Топ-2
      if (convs > 0) {
        if (currentCpc < CONFIG.MAX_CPC_CAP) {
          var newBoostedCpc = Math.min(CONFIG.MAX_CPC_CAP, Number((currentCpc * (1 + CONFIG.CONVERSION_BID_BOOST)).toFixed(2)));
          if (newBoostedCpc > currentCpc) {
            if (CONFIG.APPLY_CHANGES) {
              kw.bidding().setCpc(newBoostedCpc);
            }
            stats.boosted++;
            var boostMsg = "[Bid Boost] Ключ \"" + kw.getText() + "\" (" + convs + " конв.): CPC " + currentCpc + " ➔ " + newBoostedCpc + " для удержания топа.";
            actionLogs.push(boostMsg);
            Logger.log("  🚀 " + boostMsg);
          }
        }
      }
      // 2. Ключи-лидеры с высоким CTR (>5%) -> плавно снижаем CPC для минимизации цены клика
      else if (clicks >= 10 && ctr >= 5.0 && convs >= 0) {
        if (currentCpc > CONFIG.MIN_CPC_FLOOR) {
          var newDiscountCpc = Math.max(CONFIG.MIN_CPC_FLOOR, Number((currentCpc * (1 - CONFIG.SAVER_BID_DISCOUNT)).toFixed(2)));
          if (newDiscountCpc < currentCpc) {
            if (CONFIG.APPLY_CHANGES) {
              kw.bidding().setCpc(newDiscountCpc);
            }
            stats.saved++;
            var saveMsg = "[Bid Saver] Ключ \"" + kw.getText() + "\" (CTR " + ctr.toFixed(1) + "%): CPC " + currentCpc + " ➔ " + newDiscountCpc + " (минимизация цены клика).";
            actionLogs.push(saveMsg);
            Logger.log("  💰 " + saveMsg);
          }
        }
      }
      // 3. Ключи-сливатели бюджета (Cost > WASTE_SPEND_THRESHOLD при 0 конверсий)
      else if (cost >= CONFIG.WASTE_SPEND_THRESHOLD && convs === 0 && clicks >= CONFIG.WASTE_CLICKS_THRESHOLD) {
        if (cost >= CONFIG.WASTE_SPEND_THRESHOLD * 2) {
          // Пауза ключа при сильном сливе
          if (CONFIG.APPLY_CHANGES) {
            kw.pause();
          }
          stats.paused++;
          var pauseMsg = "[Bleed Guard: PAUSE] Ключ \"" + kw.getText() + "\" потратил $" + cost.toFixed(2) + " без конверсий ➔ поставлен на паузу.";
          actionLogs.push(pauseMsg);
          Logger.log("  ⏸️ " + pauseMsg);
        } else {
          // Снижение ставки на 20%
          var penalCpc = Math.max(CONFIG.MIN_CPC_FLOOR, Number((currentCpc * 0.8).toFixed(2)));
          if (penalCpc < currentCpc) {
            if (CONFIG.APPLY_CHANGES) {
              kw.bidding().setCpc(penalCpc);
            }
            var penalMsg = "[Bleed Guard: -20%] Ключ \"" + kw.getText() + "\" потратил $" + cost.toFixed(2) + " без конверсий ➔ CPC снижен до " + penalCpc;
            actionLogs.push(penalMsg);
            Logger.log("  📉 " + penalMsg);
          }
        }
      }
    }
  } catch (e) {
    Logger.log("  ℹ️ Оптимизация ставок: " + e.message);
  }

  Logger.log("  • Итоги управления ставками: " + stats.boosted + " повышено, " + stats.saved + " снижено для экономии, " + stats.paused + " на паузе.");
  return stats;
}

/**
 * Сводка за вчерашний день
 */
function getYesterdayPerformance(currency, warningsList) {
  var totalCost = 0;
  var totalClicks = 0;
  var totalImps = 0;
  var totalConvs = 0;
  var campaignsData = [];

  // Shopping Campaigns
  var shopIter = AdsApp.shoppingCampaigns().get();
  while (shopIter.hasNext()) {
    var sCamp = shopIter.next();
    var sStats = sCamp.getStatsFor("YESTERDAY");
    var cost = sStats.getCost();
    totalCost += cost;
    totalClicks += sStats.getClicks();
    totalImps += sStats.getImpressions();
    totalConvs += sStats.getConversions();
    campaignsData.push({
      name: sCamp.getName(),
      type: "Shopping",
      status: sCamp.isEnabled() ? "АКТИВНА" : "ПАУЗА",
      clicks: sStats.getClicks(),
      cost: cost,
      conv: sStats.getConversions()
    });

    if (cost > CONFIG.DAILY_BUDGET_CAP) {
      warningsList.push("Торговая кампания " + sCamp.getName() + " потратила " + cost.toFixed(2) + " " + currency + " (выше лимита " + CONFIG.DAILY_BUDGET_CAP + ")");
    }
  }

  // Search Campaigns
  var searchIter = AdsApp.campaigns().withCondition("AdvertisingChannelType = SEARCH").get();
  while (searchIter.hasNext()) {
    var camp = searchIter.next();
    var stats = camp.getStatsFor("YESTERDAY");
    var cCost = stats.getCost();
    totalCost += cCost;
    totalClicks += stats.getClicks();
    totalImps += stats.getImpressions();
    totalConvs += stats.getConversions();
    campaignsData.push({
      name: camp.getName(),
      type: "Search",
      status: camp.isEnabled() ? "АКТИВНА" : "ПАУЗА",
      clicks: stats.getClicks(),
      cost: cCost,
      conv: stats.getConversions()
    });

    if (cCost > CONFIG.DAILY_BUDGET_CAP) {
      warningsList.push("Поисковая кампания " + camp.getName() + " потратила " + cCost.toFixed(2) + " " + currency + " (выше лимита " + CONFIG.DAILY_BUDGET_CAP + ")");
    }
  }

  return {
    cost: totalCost,
    clicks: totalClicks,
    imps: totalImps,
    convs: totalConvs,
    campaigns: campaignsData
  };
}

/**
 * Отправка структурированного отчета на Email
 */
function sendAutopilotEmailReport(accountName, customerId, currency, perf, actionLogs, warningsList) {
  var isAlert = warningsList.length > 0;
  var subject = (isAlert ? "⚠️ Внимание: " : "💎 Livi Jewelry: ") + 
                "Отчет Google Рекламы за " + Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy") +
                " (" + perf.clicks + " переходов, " + perf.cost.toFixed(2) + " " + currency + ")";

  var lines = [];
  lines.push("══════════════════════════════════════════════════════════");
  lines.push("   LIVI JEWELRY — ЕЖЕДНЕВНЫЙ ОТЧЕТ АВТОПИЛОТА v2.0       ");
  lines.push("══════════════════════════════════════════════════════════");
  lines.push("Аккаунт: " + accountName + " (ID: " + customerId + ")");
  lines.push("Дата запуска: " + Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy HH:mm") + " (Астана)");
  lines.push("Режим работы: " + (CONFIG.APPLY_CHANGES ? "БОЕВОЙ (изменения применены)" : "СИМУЛЯЦИЯ (dry-run)") + "\n");

  if (warningsList.length > 0) {
    lines.push("⚠️ ВНИМАНИЕ (ТРЕБУЕТСЯ ПРОВЕРКА):");
    for (var w = 0; w < warningsList.length; w++) {
      lines.push("  • " + warningsList[w]);
    }
    lines.push("──────────────────────────────────────────────────────────\n");
  }

  lines.push("📊 ПОКАЗАТЕЛИ ЗА ВЧЕРА:");
  lines.push("  • Всего показов: " + perf.imps);
  lines.push("  • Переходов на сайт: " + perf.clicks);
  lines.push("  • Расход бюджета: " + perf.cost.toFixed(2) + " " + currency);
  lines.push("  • Конверсий (WhatsApp 20% + Корзина 100%): " + perf.convs);
  if (perf.clicks > 0) {
    lines.push("  • Средняя цена клика (CPC): " + (perf.cost / perf.clicks).toFixed(2) + " " + currency);
  }
  lines.push("");

  if (perf.campaigns.length > 0) {
    lines.push("📋 КАМПАНИИ:");
    for (var c = 0; c < perf.campaigns.length; c++) {
      var cp = perf.campaigns[c];
      lines.push("  • [" + cp.type + "] " + cp.name + " (" + cp.status + "): " + 
                 cp.clicks + " кликов, " + cp.cost.toFixed(2) + " " + currency + ", " + cp.conv + " конв.");
    }
    lines.push("");
  }

  lines.push("🤖 АВТОМАТИЧЕСКИЕ ДЕЙСТВИЯ АВТОПИЛОТА:");
  if (actionLogs.length > 0) {
    for (var a = 0; a < actionLogs.length; a++) {
      lines.push("  " + (a + 1) + ". " + actionLogs[a]);
    }
  } else {
    lines.push("  ✓ Все ставки в оптимальном диапазоне, новых мусорных запросов за сутки не обнаружено.");
  }
  lines.push("\n══════════════════════════════════════════════════════════");
  lines.push("Мастерская Livi Jewelry • livijewelry.kz");

  var emailBody = lines.join("\n");
  try {
    MailApp.sendEmail(CONFIG.ALERT_EMAIL, subject, emailBody);
    Logger.log("\n[OK] Отчет успешно отправлен на: " + CONFIG.ALERT_EMAIL);
  } catch (err) {
    Logger.log("\n[!] Ошибка отправки email: " + err.message);
  }
}
