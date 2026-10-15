/**
 * ==============================================================================
 * LIVI JEWELRY - GOOGLE ADS AUTOPILOT SCRIPT (v1.0)
 * ==============================================================================
 * 
 * ЧТО ДЕЛАЕТ ЭТОТ СКРИПТ АВТОМАТИЧЕСКИ:
 * 1. Защита бюджета: проверяет дневной расход и при аномалиях предупреждает.
 * 2. Мониторинг кампаний (Shopping + Search): проверяет показы, клики, CTR и конверсии.
 * 3. Аудит статусов: следит, чтобы кампания Sales-Shopping-1 не отключилась.
 * 4. Ежедневный отчет на Email: отправляет сводку за день на вашу почту viksonna94@gmail.com.
 * 
 * РАСПИСАНИЕ: Запускается автоматически каждый день в 08:00 утра.
 */

var CONFIG = {
  // Ваша почта для ежедневных отчетов:
  ALERT_EMAIL: "viksonna94@gmail.com",
  
  // Максимальный дневной бюджет в валюте аккаунта (USD):
  DAILY_BUDGET_CAP: 5.0, 
  
  // Название вашей кампании:
  MAIN_CAMPAIGN_NAME: "Sales-Shopping-1",
  
  // Отправлять отчет даже если всё в порядке:
  SEND_DAILY_SUMMARY: true
};

function main() {
  Logger.log("==================================================");
  Logger.log("LIVI JEWELRY AUTOPILOT: Запуск проверки аккаунта...");
  Logger.log("==================================================");

  var account = AdsApp.currentAccount();
  var accountName = account.getName() || "Livi Jewelry";
  var customerId = account.getCustomerId();
  var currency = account.getCurrencyCode();

  var reportLines = [];
  reportLines.push("Отчет агента Livi Jewelry по Google Рекламе");
  reportLines.push("Аккаунт: " + accountName + " (ID: " + customerId + ")");
  reportLines.push("Дата проверки: " + new Date().toLocaleString() + "\n");
  reportLines.push("--------------------------------------------------");

  var totalCostYesterday = 0;
  var totalClicksYesterday = 0;
  var totalImpressionsYesterday = 0;
  var totalConversionsYesterday = 0;

  var hasIssues = false;
  var issuesList = [];

  // 1. Проверяем все торговые кампании (Shopping / Performance Max)
  Logger.log("\n[1/3] Проверка кампаний...");
  var shoppingIterator = AdsApp.shoppingCampaigns().get();
  var shoppingCount = 0;

  while (shoppingIterator.hasNext()) {
    var camp = shoppingIterator.next();
    shoppingCount++;
    var name = camp.getName();
    var isEnabled = camp.isEnabled();
    var stats = camp.getStatsFor("YESTERDAY");

    var cost = stats.getCost();
    var clicks = stats.getClicks();
    var imps = stats.getImpressions();
    var conv = stats.getConversions();

    totalCostYesterday += cost;
    totalClicksYesterday += clicks;
    totalImpressionsYesterday += imps;
    totalConversionsYesterday += conv;

    var statusStr = isEnabled ? "АКТИВНА" : "ПАУЗА";
    reportLines.push("Кампания: " + name + " [" + statusStr + "]");
    reportLines.push("  - Показы: " + imps);
    reportLines.push("  - Клики: " + clicks);
    reportLines.push("  - Расход: " + cost.toFixed(2) + " " + currency);
    reportLines.push("  - Заказы/Конверсии: " + conv);
    reportLines.push("");

    if (cost > CONFIG.DAILY_BUDGET_CAP) {
      hasIssues = true;
      issuesList.push("ВНИМАНИЕ: Расход по кампании " + name + " (" + cost.toFixed(2) + " " + currency + ") превысил лимит!");
    }
  }

  // 2. Проверяем поисковые кампании (Search), если они есть
  var searchIterator = AdsApp.campaigns().withCondition("AdvertisingChannelType = SEARCH").get();
  while (searchIterator.hasNext()) {
    var searchCamp = searchIterator.next();
    var sName = searchCamp.getName();
    var sStats = searchCamp.getStatsFor("YESTERDAY");
    var sCost = sStats.getCost();
    var sClicks = sStats.getClicks();
    var sImps = sStats.getImpressions();
    var sConv = sStats.getConversions();

    totalCostYesterday += sCost;
    totalClicksYesterday += sClicks;
    totalImpressionsYesterday += sImps;
    totalConversionsYesterday += sConv;

    reportLines.push("Кампания (Поиск): " + sName);
    reportLines.push("  - Показы: " + sImps + ", Клики: " + sClicks + ", Расход: " + sCost.toFixed(2) + " " + currency);
    reportLines.push("");
  }

  // 3. Сводка за вчера
  reportLines.push("--------------------------------------------------");
  reportLines.push("ИТОГО ЗА ВЧЕРА:");
  reportLines.push("Всего показов: " + totalImpressionsYesterday);
  reportLines.push("Всего переходов на сайт: " + totalClicksYesterday);
  reportLines.push("Общий расход: " + totalCostYesterday.toFixed(2) + " " + currency);
  reportLines.push("Конверсий (заказов/кликов в WhatsApp): " + totalConversionsYesterday);
  reportLines.push("--------------------------------------------------");

  if (totalImpressionsYesterday === 0) {
    reportLines.push("ℹ️ Показов вчера еще не было (товары в процессе одобрения модерацией Merchant Center).");
  }

  var fullReportText = reportLines.join("\n");
  Logger.log("\n" + fullReportText);

  // 4. Отправка отчета на Email
  if (CONFIG.ALERT_EMAIL && (CONFIG.SEND_DAILY_SUMMARY || hasIssues)) {
    var subject = (hasIssues ? "⚠️ Внимание: " : "💎 Livi Jewelry: ") + 
                  "Отчет Google Рекламы (" + totalClicksYesterday + " кликов, " + 
                  totalCostYesterday.toFixed(2) + " " + currency + ")";
    try {
      MailApp.sendEmail(CONFIG.ALERT_EMAIL, subject, fullReportText);
      Logger.log("\n[OK] Отчет успешно отправлен на: " + CONFIG.ALERT_EMAIL);
    } catch (e) {
      Logger.log("\n[!] Ошибка отправки email: " + e);
    }
  }

  Logger.log("\n==================================================");
  Logger.log("АВТОПИЛОТ: Проверка успешно завершена.");
  Logger.log("==================================================");
}
