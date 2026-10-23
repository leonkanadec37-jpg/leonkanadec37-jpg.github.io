/**
 * ==============================================================================
 * LIVI JEWELRY — GROWTH & SCALING ADVISOR v1.0 (ВЕЧЕРНИЙ СОВЕТНИК 21:00)
 * ==============================================================================
 * 
 * РОЛЬ СКРИПТА:
 * Это аналитический «Советник по масштабированию» (Growth Advisor).
 * Он НЕ меняет ставки и НЕ списывает деньги — твои финансы под твоим контролем.
 * 
 * ЧТО ОН ДЕЛАЕТ КАЖДЫЙ ВЕЧЕР В 21:00:
 * 1. [Емкость рынка] Проверяет расход бюджета за сегодня: хватило ли его на весь
 *    день или реклама остановилась в обед. Выдает ровно 2 строки: Факт + Совет.
 * 2. [Самородки] Находит реальные поисковые запросы покупателей, которые содержат
 *    слово «КУПИТЬ» / «САТЫП АЛУ» в связке с нашими камнями и выдает ГОТОВЫЙ
 *    список в квадратных скобках [...] для вставки в Google Ads в 1 клик.
 * 3. [Светофор масштабирования] Строгий порог CTR >= 10.0%. Зажигает 🟢 ЗЕЛЕНЫЙ
 *    или 🟡 ЖЕЛТЫЙ свет, подсказывая точный момент перехода на бюджет $6–$8.
 * ==============================================================================
 */

var CONFIG = {
  ALERT_EMAIL: "viksonna94@gmail.com",
  MIN_CTR_THRESHOLD: 10.0,       // Строгий порог CTR для зеленого света (10.0%)
  BUDGET_SATURATION_PCT: 88.0,   // Если потрачено >88% бюджета, емкости не хватает
  TARGET_CAMPAIGN_NAME: "Livi Jewelry - Поиск Казахстан", // Основная поисковая кампания
  SEND_EMAIL: true
};

// Белый список камней и украшений мастерской Livi Jewelry
var SAFE_TERMS = [
  "жемчуг", "меруерт", "маржан", "аметист", "гранат", "турмалин", "агат", "малахит",
  "бирюза", "нефрит", "жадеит", "лазурит", "флюорит", "аквамарин", "циркон", "шпинель",
  "гематит", "янтарь", "яшма", "сердолик", "халцедон", "варисцит", "хризолит", "хризопраз",
  "коралл", "родонит", "амазонит", "апатит", "ларимар", "тигровый глаз", "кошачий глаз",
  "лунный камень", "солнечный камень", "әшекей", "алқа", "білезік", "сырға", "шашбау",
  "колье", "чокер", "браслет", "серьги", "сотуар", "бусы", "ожерелье", "подвеска", "кулон"
];

function main() {
  Logger.log("=====================================================");
  Logger.log("💎 LIVI JEWELRY — GROWTH ADVISOR v1.0 (АНАЛИЗ В 21:00)");
  Logger.log("=====================================================");

  var reportDate = Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy HH:mm");
  
  // 1. Сбор существующих активных ключевых слов в аккаунте
  var existingKeywords = {};
  try {
    var kwIter = AdsApp.keywords().withCondition("Status = ENABLED").get();
    while (kwIter.hasNext()) {
      var kw = kwIter.next();
      var cleanKw = kw.getText().toLowerCase().replace(/^["\[]|["\]]$/g, "").trim();
      existingKeywords[cleanKw] = true;
    }
  } catch (kwErr) {
    Logger.log("Ошибка чтения ключевых слов: " + kwErr);
  }

  // 2. Анализ бюджета и емкости рынка за СЕГОДНЯ
  var todayBudgetInfo = analyzeTodayBudget();

  // 3. Анализ качества за последние 3 ДНЯ (CTR и клики)
  var threeDayStats = analyzeThreeDayPerformance();

  // 4. Поиск запросов-самородков со словом "КУПИТЬ"
  var goldenQueries = findGoldenBuyQueries(existingKeywords);

  // 5. Определение статуса светофора
  var trafficLight = evaluateTrafficLight(todayBudgetInfo, threeDayStats);

  // 6. Формирование компактного отчета (без воды)
  var emailBody = buildCleanReport(reportDate, todayBudgetInfo, threeDayStats, goldenQueries, trafficLight);

  Logger.log("\n" + emailBody);

  // 7. Отправка на почту
  if (CONFIG.SEND_EMAIL && CONFIG.ALERT_EMAIL) {
    var subject = trafficLight.icon + " Livi Growth Advisor: " + trafficLight.title + " [" + reportDate + "]";
    try {
      MailApp.sendEmail({
        to: CONFIG.ALERT_EMAIL,
        subject: subject,
        body: emailBody
      });
      Logger.log("📧 Вечерний отчет успешно отправлен на: " + CONFIG.ALERT_EMAIL);
    } catch (mailErr) {
      Logger.log("Ошибка отправки email: " + mailErr);
    }
  }
}

// ------------------------------------------------------------------------------
// АНАЛИЗ ЕМКОСТИ РЫНКА ЗА СЕГОДНЯ
// ------------------------------------------------------------------------------
function analyzeTodayBudget() {
  var totalSpend = 0.0;
  var totalDailyBudget = 0.0;
  var searchSpend = 0.0;
  var searchBudget = 0.0;
  var shoppingSpend = 0.0;
  var shoppingBudget = 0.0;

  var campIter = AdsApp.campaigns().withCondition("Status = ENABLED").get();
  while (campIter.hasNext()) {
    var camp = campIter.next();
    var stats = camp.getStatsFor("TODAY");
    var spend = stats.getCost();
    var bAmount = 0.0;
    try { bAmount = camp.getBudget().getAmount(); } catch (e) {}

    totalSpend += spend;
    totalDailyBudget += bAmount;

    if (camp.getName().indexOf("Shopping") === -1) {
      searchSpend += spend;
      searchBudget += bAmount;
    }
  }

  var shopIter = AdsApp.shoppingCampaigns().withCondition("Status = ENABLED").get();
  while (shopIter.hasNext()) {
    var sCamp = shopIter.next();
    var sStats = sCamp.getStatsFor("TODAY");
    var sSpend = sStats.getCost();
    var sBAmount = 0.0;
    try { sBAmount = sCamp.getBudget().getAmount(); } catch (e) {}

    totalSpend += sSpend;
    totalDailyBudget += sBAmount;
    shoppingSpend += sSpend;
    shoppingBudget += sBAmount;
  }

  var usagePct = totalDailyBudget > 0 ? (totalSpend / totalDailyBudget) * 100 : 0;
  var isSaturated = usagePct >= CONFIG.BUDGET_SATURATION_PCT;

  return {
    totalSpend: totalSpend,
    totalDailyBudget: totalDailyBudget,
    searchSpend: searchSpend,
    searchBudget: searchBudget,
    shoppingSpend: shoppingSpend,
    shoppingBudget: shoppingBudget,
    usagePct: usagePct,
    isSaturated: isSaturated
  };
}

// ------------------------------------------------------------------------------
// АНАЛИЗ ПОКАЗАТЕЛЕЙ ЗА 3 ДНЯ (CTR И КАЧЕСТВО)
// ------------------------------------------------------------------------------
function analyzeThreeDayPerformance() {
  var totalClicks = 0;
  var totalImps = 0;
  var totalCost = 0.0;
  var searchClicks = 0;
  var searchImps = 0;

  var campIter = AdsApp.campaigns().withCondition("Status = ENABLED").get();
  while (campIter.hasNext()) {
    var camp = campIter.next();
    var stats = camp.getStatsFor("LAST_3_DAYS");
    totalClicks += stats.getClicks();
    totalImps += stats.getImpressions();
    totalCost += stats.getCost();

    if (camp.getName().indexOf("Shopping") === -1) {
      searchClicks += stats.getClicks();
      searchImps += stats.getImpressions();
    }
  }

  var shopIter = AdsApp.shoppingCampaigns().withCondition("Status = ENABLED").get();
  while (shopIter.hasNext()) {
    var sCamp = shopIter.next();
    var sStats = sCamp.getStatsFor("LAST_3_DAYS");
    totalClicks += sStats.getClicks();
    totalImps += sStats.getImpressions();
    totalCost += sStats.getCost();
  }

  var overallCtr = totalImps > 0 ? (totalClicks / totalImps) * 100 : 0.0;
  var searchCtr = searchImps > 0 ? (searchClicks / searchImps) * 100 : 0.0;

  return {
    totalClicks: totalClicks,
    totalImps: totalImps,
    totalCost: totalCost,
    overallCtr: overallCtr,
    searchClicks: searchClicks,
    searchImps: searchImps,
    searchCtr: searchCtr
  };
}

// ------------------------------------------------------------------------------
// ПОИСК САМОРОДКОВ СО СЛОВОМ "КУПИТЬ" / "САТЫП АЛУ"
// ------------------------------------------------------------------------------
function findGoldenBuyQueries(existingKeywords) {
  var goldenList = [];
  var seen = {};

  try {
    var query = "SELECT search_term_view.search_term, metrics.clicks, metrics.impressions, metrics.ctr, metrics.conversions, metrics.cost_micros " +
                "FROM search_term_view WHERE segments.date DURING LAST_7_DAYS AND metrics.clicks > 0";
    var rows = AdsApp.search(query);

    while (rows.hasNext()) {
      var row = rows.next();
      var rawTerm = (row.searchTermView.search_term || row.searchTermView.searchTerm || "").trim();
      var term = rawTerm.toLowerCase();
      if (!term || term.length < 4) continue;

      // Условие 1: СТРОГО содержит "купить" или казахское "сатып ал"
      var hasBuyIntent = /купить/i.test(term) || /сатып\s*ал/i.test(term);
      if (!hasBuyIntent) continue;

      // Условие 2: Содержит камень или изделие из нашего каталога
      var hasOurProduct = false;
      for (var s = 0; s < SAFE_TERMS.length; s++) {
        if (term.indexOf(SAFE_TERMS[s]) !== -1) {
          hasOurProduct = true;
          break;
        }
      }
      if (!hasOurProduct) continue;

      // Условие 3: Не является уже существующим активным ключевиком
      if (existingKeywords[term]) continue;
      if (seen[term]) continue;

      seen[term] = true;
      var clicks = row.metrics.clicks || 0;
      var ctr = (row.metrics.ctr || 0) * 100;
      var conv = row.metrics.conversions || 0;

      goldenList.push({
        raw: rawTerm,
        exactTag: "[" + rawTerm + "]",
        clicks: clicks,
        ctr: ctr.toFixed(1),
        conv: conv
      });
    }
  } catch (searchErr) {
    Logger.log("Ошибка анализа поисковых запросов: " + searchErr);
  }

  // Сортировка по кликам и CTR
  goldenList.sort(function(a, b) {
    return b.clicks - a.clicks;
  });

  return goldenList;
}

// ------------------------------------------------------------------------------
// СВЕТОФОР МАСШТАБИРОВАНИЯ
// ------------------------------------------------------------------------------
function evaluateTrafficLight(budgetInfo, stats3Day) {
  var isCtrHigh = stats3Day.searchCtr >= CONFIG.MIN_CTR_THRESHOLD;
  var isBudgetCapped = budgetInfo.isSaturated;

  // 🟢 ЗЕЛЕНЫЙ СВЕТ: CTR >= 10.0% И Бюджет полностью вырабатывается
  if (isCtrHigh && isBudgetCapped) {
    return {
      status: "GREEN",
      icon: "🟢",
      title: "ЗЕЛЕНЫЙ СВЕТ — ПОРА МАСШТАБИРОВАТЬСЯ!",
      recommendation: "Подними дневной бюджет кампании с $" + budgetInfo.totalDailyBudget.toFixed(2) + " до $" + (budgetInfo.totalDailyBudget * 1.5).toFixed(2) + " (спрос высокий, CTR " + stats3Day.searchCtr.toFixed(1) + "% > " + CONFIG.MIN_CTR_THRESHOLD + "%)."
    };
  }

  // 🟡 ЖЕЛТЫЙ СВЕТ: Наблюдаем (держим текущий бюджет)
  var reason = "";
  if (!isCtrHigh && isBudgetCapped) {
    reason = "Бюджет выработан, но Search CTR (" + stats3Day.searchCtr.toFixed(1) + "%) пока ниже строгого порога " + CONFIG.MIN_CTR_THRESHOLD + "%. Ждем роста качества.";
  } else if (isCtrHigh && !isBudgetCapped) {
    reason = "Search CTR отличный (" + stats3Day.searchCtr.toFixed(1) + "% >= " + CONFIG.MIN_CTR_THRESHOLD + "%), но дневной бюджет еще не исчерпан (потрачено " + budgetInfo.usagePct.toFixed(0) + "%). Текущего бюджета пока хватает на весь день.";
  } else {
    reason = "Идет плановый сбор данных. Дневного бюджета хватает, перегрузки по спросу нет. Держим $" + budgetInfo.totalDailyBudget.toFixed(2) + ".";
  }

  return {
    status: "YELLOW",
    icon: "🟡",
    title: "ЖЕЛТЫЙ СВЕТ — ДЕРЖИМ ТЕКУЩИЙ БЮДЖЕТ",
    recommendation: reason
  };
}

// ------------------------------------------------------------------------------
// ФОРМИРОВАНИЕ КОМПАКТНОГО ОТЧЕТА (БЕЗ ВОДЫ)
// ------------------------------------------------------------------------------
function buildCleanReport(reportDate, budgetInfo, stats3Day, goldenQueries, trafficLight) {
  var lines = [];
  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("  LIVI JEWELRY — СОВЕТНИК ПО МАСШТАБИРОВАНИЮ (ВЕЧЕР 21:00)");
  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("Дата и время: " + reportDate + " (Астана)");
  lines.push("");

  // 1. Светофор масштабирования
  lines.push("🚦 ВЕРДИКТ МАСШТАБИРОВАНИЯ:");
  lines.push("   " + trafficLight.icon + " " + trafficLight.title);
  lines.push("   👉 " + trafficLight.recommendation);
  lines.push("");

  // 2. Емкость рынка (ровно 2 строки: Факт + Совет)
  lines.push("📊 1. ЕМКОСТЬ РЫНКА ЗА СЕГОДНЯ:");
  if (budgetInfo.isSaturated) {
    lines.push("   • Факт: Дневной бюджет $" + budgetInfo.totalDailyBudget.toFixed(2) + " выработан на " + budgetInfo.usagePct.toFixed(0) + "% (израсходовано $" + budgetInfo.totalSpend.toFixed(2) + "). Кампания уперлась в лимит.");
    lines.push("   • Совет: Ты теряешь вечерних покупателей. Рынок готов принять $" + (budgetInfo.totalDailyBudget * 1.5).toFixed(2) + "/день.");
  } else {
    lines.push("   • Факт: Бюджета $" + budgetInfo.totalDailyBudget.toFixed(2) + " хватило на весь день (израсходовано $" + budgetInfo.totalSpend.toFixed(2) + " из $" + budgetInfo.totalDailyBudget.toFixed(2) + ", остаток " + (100 - budgetInfo.usagePct).toFixed(0) + "%).");
    lines.push("   • Совет: Бюджет оптимален, искусственно раздувать его не требуется.");
  }
  lines.push("");

  // 3. Качество за 3 дня
  lines.push("📈 2. КАЧЕСТВО ТРАФИКА ЗА 3 ДНЯ:");
  lines.push("   • Search CTR (Поиск): " + stats3Day.searchCtr.toFixed(1) + "% (Целевой порог: >=" + CONFIG.MIN_CTR_THRESHOLD + "%)");
  lines.push("   • Всего кликов за 3 дня: " + stats3Day.totalClicks + " | Показов: " + stats3Day.totalImps + " | Расход: $" + stats3Day.totalCost.toFixed(2));
  lines.push("");

  // 4. Запросы-самородки строго со словом "КУПИТЬ"
  lines.push("💎 3. САМОРОДКИ СО СЛОВОМ «КУПИТЬ» (ГОТОВЫ К ДОБАВЛЕНИЮ В 1 КЛИК):");
  if (goldenQueries.length === 0) {
    lines.push("   • За последние дни новых поисковых запросов со словом «купить» пока не зафиксировано.");
    lines.push("     (Все целевые фразы уже добавлены, либо показы шли по текущему списку).");
  } else {
    lines.push("   Скопируй этот готовый блок и вставь в Поисковую кампанию -> Ключевые слова:");
    lines.push("   -------------------------------------------------");
    for (var g = 0; g < goldenQueries.length; g++) {
      var item = goldenQueries[g];
      lines.push("   " + item.exactTag + "  /* " + item.clicks + " кл., CTR " + item.ctr + "% */");
    }
    lines.push("   -------------------------------------------------");
  }
  lines.push("");
  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("Скрипт-советник работает в режиме только чтения (Read-Only).");

  return lines.join("\n");
}
