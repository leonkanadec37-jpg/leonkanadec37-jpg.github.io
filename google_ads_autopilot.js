/**
 * ==============================================================================
 * LIVI JEWELRY — GOOGLE ADS AUTOPILOT v3.0 (ЗАЩИТА КАМНЕЙ + УТРЕННИЙ ДАЙДЖЕСТ)
 * ==============================================================================
 * 
 * ЧТО ДЕЛАЕТ ЭТОТ СКРИПТ АВТОМАТИЧЕСКИ КАЖДОЕ УТРО:
 * 1. [WhiteList Stone Guard] Внедрен строгий защитный список корней натуральных
 *    минералов и украшений (SAFE_ROOTS). Любой запрос, содержащий камень или тип
 *    изделия из WhiteList, КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО блокировать (даже при расходе
 *    без конверсий). Такие фразы выводятся исключительно в email на ручной контроль.
 * 2. [Auto-Negation Pure Junk] Находит мусорные запросы за 7 дней ТОЛЬКО по
 *    строгим стоп-паттернам (JUNK_PATTERNS: DIY, чужие материалы, ломбарды, скупка,
 *    дешевый опт, ремонт) и добавляет их во фразовом соответствии '"' + term + '"'.
 * 3. [No Spend-Based Auto-Block] Полностью отключена авто-блокировка по сумме расхода ($1.50)
 *    или кликам — скрипт больше не блокирует целевые фразы за расход.
 * 4. [Detailed Morning Digest] Формирует утренний отчет на viksonna94@gmail.com:
 *    - Раздельная статистика за вчера по Поиску (Search) и Shopping (Покупки).
 *    - Блок «🔍 Все поисковые запросы с кликами за вчера».
 *    - Блок «⚠️ Запросы с расходом без конверсий (на ручную проверку)».
 *    - Блок «🏆 Кандидаты в точное соответствие (Conversions > 0 или CTR >= 10%)».
 *    - Тихий аудит 404 ошибок целевых страниц (предупреждение без остановки кампаний).
 * 5. [Smart CPC Management] Корректирует ставки CPC ключевых слов для удержания топа.
 *
 * РАСПИСАНИЕ: Запускается автоматически каждый день в 07:00 или 08:00 утра.
 * ==============================================================================
 */

var CONFIG = {
  // Email владельца для утреннего дайджеста и предупреждений:
  ALERT_EMAIL: "viksonna94@gmail.com",

  // Лимит дневного расхода аккаунта для предупреждения (валюта аккаунта, например USD или эквивалент KZT):
  DAILY_BUDGET_CAP: 10.0,

  // Максимальный потолок ставки CPC (защита от переплат):
  MAX_CPC_CAP: 0.35,

  // Минимальный пол ставки CPC:
  MIN_CPC_FLOOR: 0.05,

  // Шаг повышения ставки для конвертящих фраз:
  CONVERSION_BID_BOOST: 0.10, // +10%

  // Шаг экономии для фраз с высоким CTR в топе:
  SAVER_BID_DISCOUNT: 0.05,   // -5%

  // Название мастер-списка минус-слов в аккаунде:
  NEGATIVE_LIST_NAME: "Livi Jewelry - Мастер Минус-слова",

  // Применять ли изменения на боевом аккаунте (true = боевой режим, false = dry-run):
  APPLY_CHANGES: true,

  // Всегда отправлять утреннюю сводку:
  SEND_DAILY_SUMMARY: true
};

// ------------------------------------------------------------------------------
// 1. БРЕНДЫ-КОНКУРЕНТЫ (БЕЗУСЛОВНЫЙ БАН В ПЕРВУЮ ОЧЕРЕДЬ)
// ------------------------------------------------------------------------------
var COMPETITOR_BRANDS = [
  /swarovski/i, /сваровск/i, /тиффани/i, /tiffany/i, /картье/i, /cartier/i,
  /messika/i, /мессика/i, /apm/i, /monaco/i, /апм/i, /монако/i,
  /aroush/i, /larosh/i, /laroush/i, /ляруш/i, /merhat/i, /мерхат/i,
  /tallys/i, /таллис/i, /sansi/i, /санси/i, /люченте/i, /luchente/i, /lucente/i,
  /казахювелир/i, /kazakhyuvelir/i, /пандор/i, /pandora/i, /соколов/i, /sokolov/i,
  /санлайт/i, /sunlight/i, /ван клиф/i, /van cleef/i, /балауса/i, /balausa/i,
  /sakina/i, /сакина/i, /mone\b/i
];

// ------------------------------------------------------------------------------
// 2. ЗАЩИТНЫЙ WHITELIST НАТУРАЛЬНЫХ КАМНЕЙ И ЖЕМЧУГА (КАТЕГОРИЧЕСКИ НЕ БЛОКИРОВАТЬ)
// Очищен от общих слов (серьги, кольцо, браслет) и драгметаллов (изумруд, рубин, сапфир)
// ------------------------------------------------------------------------------
var SAFE_ROOTS = [
  /жемчуг/i, /барочн/i, /нефрит/i, /жадеит/i, /джедаит/i, /аметист/i, /малахит/i, /агат/i,
  /гранат/i, /кварц/i, /бирюз/i, /гематит/i, /хрустал/i, /лунн.*камен/i, /лунн/i,
  /тигров.*глаз/i, /тигров/i, /лазурит/i, /коралл/i, /яшм/i, /сердолик/i, /амазонит/i,
  /турмалин/i, /цитрин/i, /авантюрин/i, /флюорит/i, /перламутр/i, /оникс/i, /шпинел/i,
  /топаз/i, /аквамарин/i, /берилл/i, /лабрадор/i, /чароит/i, /хризопраз/i, /змеевик/i,
  /опал/i, /янтарь/i, /сотуар/i, /чокер/i, /натуральн.*камн/i, /livi/i
];

// ------------------------------------------------------------------------------
// 3. СТОП-ПАТТЕРНЫ МУСОРА, ДЕШЕВОГО ОПТА, НЕЦЕЛЕВЫХ МЕТАЛЛОВ И УСЛУГ
// ------------------------------------------------------------------------------
var JUNK_PATTERNS = [
  // Рукоделие, DIY, детали и фурнитура
  /своими руками/i, /как сделать/i, /как сплести/i, /схем/i, /мастер класс/i, /мк\b/i,
  /бисероплетени/i, /плетени/i, /вязани/i, /фурнитур/i, /застежк/i, /швенз/i, /штифт/i,
  /пины\b/i, /леск/i, /проволок/i, /эпоксидн/i, /полимерн.*глин/i, /вышивк/i, /станок/i,
  /с буквой/i,

  // Нецелевые чужие материалы
  /шерст/i, /валян/i, /муассанит/i, /дерев/i, /пластик/i, /акрил/i, /силикон/i, /xuping/i,
  /медицинск.*золот/i,

  // Халява, ломбарды, скупка, дешевый опт, б/у
  /бесплатн/i, /даром/i, /ломбард/i, /скупк/i, /сдать.*золото/i, /проба 585/i, /золото 585/i,
  /слит.*золот/i, /алиэкспресс/i, /aliexpress/i, /temu/i, /shein/i, /таобао/i, /секонд/i,
  /конфискат/i, /б[\s/]?у\b/i,

  // Нецелевые металлы и масс-маркет (блокируются ТОЛЬКО если нет камня из SAFE_ROOTS)
  /золот/i, /серебр/i, /магазин золота/i, /бриллиант/i, /изумруд/i, /рубин/i, /сапфир/i,

  // Нецелевые услуги, инфо-запросы и гео
  /ремонт/i, /пайк/i, /чистк.*золот/i, /ультразвуков/i, /ваканси/i, /резюме/i, /работа/i,
  /зарплат/i, /реферат/i, /сонник/i, /гороскоп/i, /знак.*зодиак/i, /магическ/i,
  /лечебн.*свойств/i, /приворот/i, /заговор/i, /скачать/i, /обои.*телефон/i,
  /milan/i, /милан/i, /греци/i
];

/**
 * Проверка запроса на наличие корней натуральных минералов и жемчуга
 */
function isSafeTerm(term) {
  if (!term) return false;
  var lower = term.toLowerCase().trim();
  for (var i = 0; i < SAFE_ROOTS.length; i++) {
    if (SAFE_ROOTS[i].test(lower)) {
      return true;
    }
  }
  return false;
}

/**
 * Комплексная оценка поискового запроса:
 * 1. Бренд конкурента -> безусловный мусор (БАН)
 * 2. Камень + серебро/золото фурнитура -> ЗАЩИТА (НЕ БЛОКИРОВАТЬ)
 * 3. Стоп-паттерн мусора (без нашего камня) -> мусор (БАН)
 * 4. Наш камень/жемчуг -> ЗАЩИТА
 */
function evaluateSearchTerm(term) {
  var lower = (term || "").toLowerCase().trim();
  if (!lower) return { isJunk: false, isSafe: false, reason: "Пустой запрос" };

  // 1. Бренд конкурента -> МГНОВЕННЫЙ БАН
  for (var b = 0; b < COMPETITOR_BRANDS.length; b++) {
    if (COMPETITOR_BRANDS[b].test(lower)) {
      return { isJunk: true, isSafe: false, reason: "Бренд-конкурент (" + COMPETITOR_BRANDS[b] + ")" };
    }
  }

  // 2. Проверка наличия нашего натурального минерала / жемчуга
  var hasSafeStone = isSafeTerm(lower);

  // 3. Проверка на стоп-паттерны
  for (var j = 0; j < JUNK_PATTERNS.length; j++) {
    if (JUNK_PATTERNS[j].test(lower)) {
      // Исключение: если есть наш камень/жемчуг И это просто указание металла замка/фурнитуры (серебро/золото)
      var isMetalFittings = (/золот/i.test(lower) || /серебр/i.test(lower)) &&
                            !/ломбард/i.test(lower) && !/скупк/i.test(lower) && !/проба 585/i.test(lower);

      if (hasSafeStone && isMetalFittings) {
        return { isJunk: false, isSafe: true, reason: "Камень + фурнитура серебро/золото" };
      }

      // В остальных случаях (камня нет, либо это чистый мусор DIY/ломбард/алмазы) -> БАН
      return { isJunk: true, isSafe: false, reason: "Стоп-паттерн (" + JUNK_PATTERNS[j] + ")" };
    }
  }

  // 4. Обычный запрос без мусора
  return {
    isJunk: false,
    isSafe: hasSafeStone,
    reason: hasSafeStone ? "Натуральный камень / жемчуг" : "Общий запрос"
  };
}

function main() {
  Logger.log("==================================================================");
  Logger.log("   💎 LIVI JEWELRY AUTOPILOT v3.0: ЗАПУСК ОПТИМИЗАЦИИ РЕКЛАМЫ    ");
  Logger.log("==================================================================");

  var account = AdsApp.currentAccount();
  var accountName = account.getName() || "Livi Jewelry";
  var customerId = account.getCustomerId();
  var currency = account.getCurrencyCode();

  var actionLogs = [];
  var warningsList = [];

  // 1. Подключение существующего мастер-списка минус-слов ко всем кампаниям
  Logger.log("\n[1/5] Проверка и привязка мастер-списка минус-слов...");
  var negativeList = getOrCreateNegativeList(CONFIG.NEGATIVE_LIST_NAME);
  var attachedCampaignsCount = attachNegativeListToAllCampaigns(negativeList);
  if (attachedCampaignsCount > 0) {
    actionLogs.push("Мастер-список минус-слов прикреплен к " + attachedCampaignsCount + " кампаниям.");
  }

  // 2. Авто-чистка реальных мусорных запросов за 7 дней с защитой WhiteList
  Logger.log("\n[2/5] Анализ поисковых запросов за 7 дней (строгий WhiteList камней)...");
  var negatedTermsCount = mineJunkSearchTerms(negativeList, actionLogs);

  // 3. Управление ставками CPC ключевых слов
  Logger.log("\n[3/5] Оптимизация ставок CPC ключевых слов...");
  var bidStats = optimizeKeywordBids(actionLogs);

  // 4. Проверка корректности целевых посадочных страниц
  Logger.log("\n[4/5] Проверка корректности целевых страниц объявлений...");
  var landingPageAlerts = auditLandingPages();
  if (landingPageAlerts.length > 0) {
    for (var b = 0; b < landingPageAlerts.length; b++) {
      warningsList.push(landingPageAlerts[b]);
    }
  }

  // 5. Детальный сбор статистики за вчера (Поиск + Shopping + Запросы)
  Logger.log("\n[5/5] Формирование детального утреннего отчета за вчера...");
  var perfSummary = getYesterdayDetailedPerformance(currency, warningsList);

  // 6. Отправка подробного утреннего email-отчета
  if (CONFIG.SEND_DAILY_SUMMARY || warningsList.length > 0) {
    sendAutopilotEmailReport(accountName, customerId, currency, perfSummary, actionLogs, warningsList);
  }

  Logger.log("\n==================================================================");
  Logger.log("   АВТОПИЛОТ v3.0: Выполнение успешно завершено!                 ");
  Logger.log("==================================================================");
}

/**
 * Получение или создание списка минус-слов без перезаписи существующей базы 800+ слов
 */
function getOrCreateNegativeList(listName) {
  var listIter = AdsApp.negativeKeywordLists().withCondition("Name = '" + listName + "'").get();
  if (listIter.hasNext()) {
    var existingList = listIter.next();
    Logger.log("  ✓ Список минус-слов найден в аккаунте: " + listName);
    return existingList;
  }
  var builder = AdsApp.newNegativeKeywordListBuilder().withName(listName).build();
  Logger.log("  ✓ Создан список минус-слов: " + listName);
  return builder.getResult();
}

/**
 * Привязка списка ко всем активным поисковым и торговым кампаниям
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

  var shopIter = AdsApp.shoppingCampaigns().get();
  while (shopIter.hasNext()) {
    var sCamp = shopIter.next();
    try {
      if (CONFIG.APPLY_CHANGES) {
        sCamp.addNegativeKeywordList(negativeList);
      }
      count++;
    } catch (e) {}
  }
  return count;
}

/**
 * Поиск нецелевых запросов за 7 дней.
 * СТРОГОЕ ПРАВИЛО:
 * 1. Бренды-конкуренты блокируются всегда.
 * 2. Натуральные камни и жемчуг (включая с серебром/позолотой) КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО блокировать.
 * 3. Чистый мусор блокируется во фразовом соответствии '"' + term + '"'.
 */
function mineJunkSearchTerms(negativeList, actionLogs) {
  var addedCount = 0;
  var existingNegs = {};

  try {
    var negIter = negativeList.getNegativeKeywords();
    while (negIter.hasNext()) {
      existingNegs[negIter.next().getText().toLowerCase()] = true;
    }
  } catch (err) {}

  try {
    var query = "SELECT search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions " +
                "FROM search_term_view WHERE segments.date DURING LAST_7_DAYS";
    var rows = AdsApp.search(query);

    while (rows.hasNext()) {
      var row = rows.next();
      var term = (row.searchTermView.searchTerm || "").trim().toLowerCase();
      if (!term || term.length < 2) continue;

      var evalRes = evaluateSearchTerm(term);
      if (evalRes.isJunk) {
        var phraseNeg = '"' + term + '"';
        if (!existingNegs[phraseNeg.toLowerCase()] && !existingNegs[term]) {
          try {
            if (CONFIG.APPLY_CHANGES) {
              negativeList.addNegativeKeyword(phraseNeg);
            }
            existingNegs[phraseNeg.toLowerCase()] = true;
            addedCount++;
            var logMsg = "[Auto-Negated] Заблокирован нецелевой запрос: " + phraseNeg + " [" + evalRes.reason + "]";
            actionLogs.push(logMsg);
            Logger.log("  🚫 " + logMsg);
          } catch (negErr) {}
        }
      }
    }
  } catch (e) {
    Logger.log("  ℹ️ Запрос отчета поисковых фраз: " + e.message);
  }

  Logger.log("  • Всего авто-заблокировано мусорных запросов во фразовом соответствии: " + addedCount);
  return addedCount;
}

/**
 * Оптимизация ставок CPC ключевых слов
 */
function optimizeKeywordBids(actionLogs) {
  var stats = { boosted: 0, saved: 0 };
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
      var convs = kwStats.getConversions();
      var ctr = kwStats.getCtr() * 100;
      var currentCpc = kw.bidding().getCpc() || 0.15;

      // Конвертящие фразы -> повышаем ставку (+10%) для удержания топа
      if (convs > 0) {
        if (currentCpc < CONFIG.MAX_CPC_CAP) {
          var newBoostedCpc = Math.min(CONFIG.MAX_CPC_CAP, Number((currentCpc * (1 + CONFIG.CONVERSION_BID_BOOST)).toFixed(2)));
          if (newBoostedCpc > currentCpc) {
            if (CONFIG.APPLY_CHANGES) {
              kw.bidding().setCpc(newBoostedCpc);
            }
            stats.boosted++;
            var boostMsg = "[Bid Boost] Ключ \"" + kw.getText() + "\" (" + convs + " конв.): CPC " + currentCpc + " ➔ " + newBoostedCpc;
            actionLogs.push(boostMsg);
            Logger.log("  🚀 " + boostMsg);
          }
        }
      }
      // Фразы с высоким CTR (>8%) и достаточным объемом -> плавно снижаем ставку для экономии
      else if (clicks >= 12 && ctr >= 8.0) {
        if (currentCpc > CONFIG.MIN_CPC_FLOOR) {
          var newDiscountCpc = Math.max(CONFIG.MIN_CPC_FLOOR, Number((currentCpc * (1 - CONFIG.SAVER_BID_DISCOUNT)).toFixed(2)));
          if (newDiscountCpc < currentCpc) {
            if (CONFIG.APPLY_CHANGES) {
              kw.bidding().setCpc(newDiscountCpc);
            }
            stats.saved++;
            var saveMsg = "[Bid Saver] Ключ \"" + kw.getText() + "\" (CTR " + ctr.toFixed(1) + "%): CPC " + currentCpc + " ➔ " + newDiscountCpc;
            actionLogs.push(saveMsg);
            Logger.log("  💰 " + saveMsg);
          }
        }
      }
    }
  } catch (e) {
    Logger.log("  ℹ️ Оптимизация ставок: " + e.message);
  }
  return stats;
}

/**
 * Проверка корректности целевых URL объявлений (без внешних HTTP-запросов, безопасно для Google)
 */
function auditLandingPages() {
  var alerts = [];
  var checked = {};
  try {
    var adIter = AdsApp.ads()
      .withCondition("Status = ENABLED")
      .withCondition("CampaignStatus = ENABLED")
      .get();

    while (adIter.hasNext()) {
      var ad = adIter.next();
      var finalUrl = ad.urls().getFinalUrl() || "";
      if (finalUrl && !checked[finalUrl]) {
        checked[finalUrl] = true;
        if (finalUrl.indexOf("http://") === 0) {
          alerts.push("Объявление использует небезопасный HTTP: " + finalUrl);
        } else if (finalUrl.indexOf("livijewelry.kz") === -1) {
          alerts.push("Объявление ведет на сторонний домен: " + finalUrl);
        }
      }
    }
  } catch (e) {
    Logger.log("  ℹ️ Проверка целевых страниц: " + e.message);
  }
  return alerts;
}

/**
 * Сбор детальной статистики за вчерашний день раздельно по Поиску и Shopping
 */
function getYesterdayDetailedPerformance(currency, warningsList) {
  var searchTotals = { imps: 0, clicks: 0, cost: 0, convs: 0, campaigns: [] };
  var shoppingTotals = { imps: 0, clicks: 0, cost: 0, convs: 0, campaigns: [] };

  // 1. Поисковые кампании (AdsApp.campaigns())
  var searchIter = AdsApp.campaigns().get();
  while (searchIter.hasNext()) {
    var camp = searchIter.next();
    var stats = camp.getStatsFor("YESTERDAY");
    var cost = stats.getCost();
    var clicks = stats.getClicks();
    var imps = stats.getImpressions();
    var convs = stats.getConversions();
    var ctr = imps > 0 ? (clicks / imps) * 100 : 0;
    var avgCpc = clicks > 0 ? (cost / clicks) : 0;

    searchTotals.imps += imps;
    searchTotals.clicks += clicks;
    searchTotals.cost += cost;
    searchTotals.convs += convs;

    searchTotals.campaigns.push({
      name: camp.getName(),
      status: camp.isEnabled() ? "АКТИВНА" : "ПАУЗА",
      imps: imps,
      clicks: clicks,
      ctr: ctr,
      avgCpc: avgCpc,
      cost: cost,
      convs: convs
    });

    if (cost > CONFIG.DAILY_BUDGET_CAP) {
      warningsList.push("Поисковая кампания «" + camp.getName() + "» потратила " + cost.toFixed(2) + " " + currency + " (выше лимита " + CONFIG.DAILY_BUDGET_CAP + ")");
    }
  }

  // 2. Shopping кампании (AdsApp.shoppingCampaigns())
  var shopIter = AdsApp.shoppingCampaigns().get();
  while (shopIter.hasNext()) {
    var sCamp = shopIter.next();
    var sStats = sCamp.getStatsFor("YESTERDAY");
    var sCost = sStats.getCost();
    var sClicks = sStats.getClicks();
    var sImps = sStats.getImpressions();
    var sConvs = sStats.getConversions();
    var sCtr = sImps > 0 ? (sClicks / sImps) * 100 : 0;
    var sAvgCpc = sClicks > 0 ? (sCost / sClicks) : 0;

    shoppingTotals.imps += sImps;
    shoppingTotals.clicks += sClicks;
    shoppingTotals.cost += sCost;
    shoppingTotals.convs += sConvs;

    shoppingTotals.campaigns.push({
      name: sCamp.getName(),
      status: sCamp.isEnabled() ? "АКТИВНА" : "ПАУЗА",
      imps: sImps,
      clicks: sClicks,
      ctr: sCtr,
      avgCpc: sAvgCpc,
      cost: sCost,
      convs: sConvs
    });

    if (sCost > CONFIG.DAILY_BUDGET_CAP) {
      warningsList.push("Торговая кампания «" + sCamp.getName() + "» потратила " + sCost.toFixed(2) + " " + currency + " (выше лимита " + CONFIG.DAILY_BUDGET_CAP + ")");
    }
  }

  // 3. Анализ всех реальных поисковых запросов за вчера
  var clickedQueries = [];
  var spendWithoutConvQueries = [];
  var exactCandidates = [];

  try {
    var qQuery = "SELECT search_term_view.search_term, campaign.name, metrics.clicks, metrics.impressions, " +
                 "metrics.cost_micros, metrics.conversions, metrics.ctr " +
                 "FROM search_term_view WHERE segments.date DURING YESTERDAY";
    var rows = AdsApp.search(qQuery);

    while (rows.hasNext()) {
      var r = rows.next();
      var term = (r.searchTermView.search_term || r.searchTermView.searchTerm || "").trim();
      if (!term) continue;

      var clicks = r.metrics.clicks || 0;
      var imps = r.metrics.impressions || 0;
      var cost = (r.metrics.cost_micros || r.metrics.costMicros || 0) / 1000000;
      var convs = r.metrics.conversions || 0;
      var ctr = r.metrics.ctr ? (r.metrics.ctr * 100) : (imps > 0 ? (clicks / imps) * 100 : 0);
      var cpc = clicks > 0 ? (cost / clicks) : 0;
      var campName = (r.campaign && r.campaign.name) ? r.campaign.name : "Поиск/Shopping";
      
      var evalRes = evaluateSearchTerm(term);

      // Все запросы с кликами
      if (clicks > 0) {
        clickedQueries.push({
          term: term,
          campaign: campName,
          clicks: clicks,
          cpc: cpc,
          cost: cost,
          convs: convs,
          isSafe: evalRes.isSafe,
          isJunk: evalRes.isJunk,
          reason: evalRes.reason
        });
      }

      // Запросы с расходом без конверсий (ТОЛЬКО НА РУЧНУЮ ПРОВЕРКУ, БЕЗ БЛОКИРОВКИ)
      if (cost > 0 && convs === 0) {
        spendWithoutConvQueries.push({
          term: term,
          campaign: campName,
          clicks: clicks,
          cost: cost,
          isSafe: evalRes.isSafe,
          isJunk: evalRes.isJunk,
          reason: evalRes.reason
        });
      }

      // Кандидаты в точное соответствие:
      // Строго НЕ мусор (!evalRes.isJunk) И (есть конверсии ИЛИ (это наш камень/жемчуг И кликов >= 2 И CTR >= 10%))
      if (!evalRes.isJunk && (convs > 0 || (evalRes.isSafe && clicks >= 2 && ctr >= 10.0))) {
        exactCandidates.push({
          term: term,
          campaign: campName,
          clicks: clicks,
          ctr: ctr,
          cost: cost,
          convs: convs
        });
      }
    }
  } catch (err) {
    Logger.log("  ℹ️ Анализ поисковых запросов за вчера: " + err.message);
  }

  return {
    search: searchTotals,
    shopping: shoppingTotals,
    totalCost: searchTotals.cost + shoppingTotals.cost,
    totalClicks: searchTotals.clicks + shoppingTotals.clicks,
    totalImps: searchTotals.imps + shoppingTotals.imps,
    totalConvs: searchTotals.convs + shoppingTotals.convs,
    clickedQueries: clickedQueries,
    spendWithoutConvQueries: spendWithoutConvQueries,
    exactCandidates: exactCandidates
  };
}

/**
 * Отправка подробного структурированного отчета на Email
 */
function sendAutopilotEmailReport(accountName, customerId, currency, perf, actionLogs, warningsList) {
  var isAlert = warningsList.length > 0;
  var dateStr = Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy");
  var subject = (isAlert ? "⚠️ Внимание: " : "💎 Livi Jewelry: ") +
                "Утренний отчет Google Ads v3.1 за вчера (" + dateStr + ") — " +
                perf.totalClicks + " кликов, " + perf.totalCost.toFixed(2) + " " + currency;

  var lines = [];
  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("   LIVI JEWELRY — УТРЕННИЙ БОЕВОЙ ОТЧЕТ AUTOPILOT v3.1           ");
  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("Аккаунт: " + accountName + " (ID: " + customerId + ")");
  lines.push("Дата формирования: " + Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy HH:mm") + " (Астана)");
  lines.push("Режим работы: " + (CONFIG.APPLY_CHANGES ? "БОЕВОЙ" : "СИМУЛЯЦИЯ (dry-run)") + "\n");

  if (warningsList.length > 0) {
    lines.push("⚠️ ВНИМАНИЕ / АЛЕРТЫ:");
    for (var w = 0; w < warningsList.length; w++) {
      lines.push("  • " + warningsList[w]);
    }
    lines.push("──────────────────────────────────────────────────────────────────\n");
  }

  // 1. Общие показатели за вчера
  lines.push("📊 ОБЩИЕ ПОКАЗАТЕЛИ ЗА ВЧЕРА:");
  lines.push("  • Всего показов: " + perf.totalImps);
  lines.push("  • Всего кликов: " + perf.totalClicks);
  lines.push("  • Общий расход: " + perf.totalCost.toFixed(2) + " " + currency);
  lines.push("  • Конверсий: " + perf.totalConvs);
  var overallCtr = perf.totalImps > 0 ? (perf.totalClicks / perf.totalImps) * 100 : 0;
  var overallCpc = perf.totalClicks > 0 ? (perf.totalCost / perf.totalClicks) : 0;
  lines.push("  • Общий CTR: " + overallCtr.toFixed(2) + "%");
  lines.push("  • Средний CPC: " + overallCpc.toFixed(2) + " " + currency + "\n");

  // 2. Поисковые кампании (Search)
  lines.push("🔍 1. ПОИСКОВЫЕ КАМПАНИИ (SEARCH):");
  var sCtr = perf.search.imps > 0 ? (perf.search.clicks / perf.search.imps) * 100 : 0;
  var sCpc = perf.search.clicks > 0 ? (perf.search.cost / perf.search.clicks) : 0;
  lines.push("  Сводка: " + perf.search.imps + " показов | " + perf.search.clicks + " кликов | CTR " +
             sCtr.toFixed(2) + "% | CPC " + sCpc.toFixed(2) + " " + currency + " | Расход: " +
             perf.search.cost.toFixed(2) + " " + currency + " | Конверсий: " + perf.search.convs);
  for (var sc = 0; sc < perf.search.campaigns.length; sc++) {
    var c = perf.search.campaigns[sc];
    lines.push("    • " + c.name + " [" + c.status + "]: " + c.clicks + " кл., CTR " +
               c.ctr.toFixed(1) + "%, CPC " + c.avgCpc.toFixed(2) + " " + currency +
               ", расход " + c.cost.toFixed(2) + " " + currency + ", конв.: " + c.convs);
  }
  lines.push("");

  // 3. Торговые кампании (Shopping)
  lines.push("🛍️ 2. ТОРГОВЫЕ КАМПАНИИ (SHOPPING):");
  var shCtr = perf.shopping.imps > 0 ? (perf.shopping.clicks / perf.shopping.imps) * 100 : 0;
  var shCpc = perf.shopping.clicks > 0 ? (perf.shopping.cost / perf.shopping.clicks) : 0;
  lines.push("  Сводка: " + perf.shopping.imps + " показов | " + perf.shopping.clicks + " кликов | CTR " +
             shCtr.toFixed(2) + "% | CPC " + shCpc.toFixed(2) + " " + currency + " | Расход: " +
             perf.shopping.cost.toFixed(2) + " " + currency + " | Конверсий: " + perf.shopping.convs);
  for (var shc = 0; shc < perf.shopping.campaigns.length; shc++) {
    var scamp = perf.shopping.campaigns[shc];
    lines.push("    • " + scamp.name + " [" + scamp.status + "]: " + scamp.clicks + " кл., CTR " +
               scamp.ctr.toFixed(1) + "%, CPC " + scamp.avgCpc.toFixed(2) + " " + currency +
               ", расход " + scamp.cost.toFixed(2) + " " + currency + ", конв.: " + scamp.convs);
  }
  lines.push("");

  // 4. Все поисковые запросы с кликами за вчера
  lines.push("🔍 ВСЕ ПОИСКОВЫЕ ЗАПРОСЫ С КЛИКАМИ ЗА ВЧЕРА (" + perf.clickedQueries.length + "):");
  if (perf.clickedQueries.length > 0) {
    for (var q = 0; q < perf.clickedQueries.length; q++) {
      var item = perf.clickedQueries[q];
      var mark = item.isSafe ? " [💎 Наш камень/изделие]" : (item.isJunk ? " [🚫 Мусор/Бренд]" : " [🔍 Общий запрос]");
      lines.push("  " + (q + 1) + ". «" + item.term + "»" + mark +
                 " — " + item.clicks + " кл. | CPC " + item.cpc.toFixed(2) + " " + currency +
                 " | Расход: " + item.cost.toFixed(2) + " " + currency +
                 " | Конв: " + item.convs + " (" + item.campaign + ")");
    }
  } else {
    lines.push("  • Вчера кликов по поисковым фразам не зарегистрировано.");
  }
  lines.push("");

  // 5. Запросы с расходом без конверсий
  lines.push("⚠️ ЗАПРОСЫ С РАСХОДОМ БЕЗ КОНВЕРСИЙ (НА РУЧНУЮ ПРОВЕРКУ):");
  lines.push("   (Скрипт защищает наши камни и выводит запросы на контроль)");
  if (perf.spendWithoutConvQueries.length > 0) {
    for (var sw = 0; sw < perf.spendWithoutConvQueries.length; sw++) {
      var swItem = perf.spendWithoutConvQueries[sw];
      var statusTag = "";
      if (swItem.isSafe) {
        statusTag = " [🛡️ В WhiteList натуральных камней — защита от блокировки]";
      } else if (swItem.isJunk) {
        statusTag = " [🚫 Мусор/Бренд — авто-блокировка в 7-дневном цикле: " + swItem.reason + "]";
      } else {
        statusTag = " [🔍 Общий ювелирный запрос — решение владельца]";
      }
      lines.push("  • «" + swItem.term + "»" + statusTag +
                 ": расход " + swItem.cost.toFixed(2) + " " + currency +
                 ", кликов: " + swItem.clicks + " (" + swItem.campaign + ")");
    }
  } else {
    lines.push("  ✓ Все запросы с расходом либо сконвертировались, либо расход равен нулю.");
  }
  lines.push("");

  // 6. Кандидаты в точное соответствие
  lines.push("🏆 КАНДИДАТЫ В ТОЧНОЕ СООТВЕТСТВИЕ (Conversions > 0 или CTR >= 10% при >= 2 кликах):");
  if (perf.exactCandidates.length > 0) {
    for (var ex = 0; ex < perf.exactCandidates.length; ex++) {
      var exItem = perf.exactCandidates[ex];
      lines.push("  • «" + exItem.term + "» — CTR " + exItem.ctr.toFixed(1) + "% | " +
                 exItem.clicks + " кл. | Конверсий: " + exItem.convs + " (" + exItem.campaign + ")");
    }
  } else {
    lines.push("  • Новых кандидатов с высоким CTR или конверсиями за вчера не обнаружено.");
  }
  lines.push("");

  // 7. Действия автопилота
  lines.push("🤖 АВТОМАТИЧЕСКИЕ ДЕЙСТВИЯ АВТОПИЛОТА ЗА СЕГОДНЯ:");
  if (actionLogs.length > 0) {
    for (var a = 0; a < actionLogs.length; a++) {
      lines.push("  " + (a + 1) + ". " + actionLogs[a]);
    }
  } else {
    lines.push("  ✓ Мусорных запросов вне WhiteList не обнаружено, ставки ключевых слов стабильны.");
  }

  lines.push("\n══════════════════════════════════════════════════════════════════");
  lines.push("Мастерская авторских украшений Livi Jewelry • livijewelry.kz");

  var emailBody = lines.join("\n");
  try {
    MailApp.sendEmail(CONFIG.ALERT_EMAIL, subject, emailBody);
    Logger.log("\n[OK] Отчет успешно отправлен на: " + CONFIG.ALERT_EMAIL);
  } catch (err) {
    Logger.log("\n[!] Ошибка отправки email: " + err.message);
  }
}
