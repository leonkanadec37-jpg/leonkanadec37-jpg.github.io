/**
 * ==============================================================================
 * LIVI JEWELRY — ЕЖЕДНЕВНЫЙ ОТЧЕТ ПО ВСЕМ КАМПАНИЯМ (ПОИСК + SHOPPING) v2.1
 * ==============================================================================
 * 
 * Назначение:
 * Каждое утро робот собирает статистику за ВЧЕРА по ВСЕМ кампаниям аккаунта:
 * 1. Поисковые кампании (Search: "Новая кампания 24.09" / "Livi Jewelry - Поиск")
 * 2. Торговые товарные кампании (Google Shopping: "Sales-Shopping-1")
 * 
 * И отправляет красивую понятную сводку на почту: viksonna94@gmail.com
 * ==============================================================================
 */

var CONFIG = {
  ALERT_EMAIL: "viksonna94@gmail.com",
  DAILY_BUDGET_CAP: 10.0, // Лимит для алерта при перерасходе
  SEND_DAILY_SUMMARY: true
};

function main() {
  Logger.log("LIVI JEWELRY: Запуск формирования утреннего отчета...");
  var account = AdsApp.currentAccount();
  var currency = account.getCurrencyCode();

  var reportLines = [
    "💎 Отчет робота Livi Jewelry по Google Рекламе",
    "Аккаунт: " + (account.getName() || "Livi Jewelry") + " (" + account.getCustomerId() + ")",
    "Дата: " + Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy"),
    "--------------------------------------------------"
  ];

  var totalCost = 0;
  var totalClicks = 0;
  var totalImps = 0;
  var totalConv = 0;
  var foundCampaignsCount = 0;

  // ------------------------------------------------------------------
  // 1. ПОИСКОВЫЕ КАМПАНИИ (Search)
  // ------------------------------------------------------------------
  var searchIter = AdsApp.campaigns().get();
  while (searchIter.hasNext()) {
    var camp = searchIter.next();
    foundCampaignsCount++;
    var stats = camp.getStatsFor("YESTERDAY");
    var cost = stats.getCost();
    var clicks = stats.getClicks();
    var imps = stats.getImpressions();
    var conv = stats.getConversions();

    totalCost += cost;
    totalClicks += clicks;
    totalImps += imps;
    totalConv += conv;

    var statusText = camp.isEnabled() ? "АКТИВНА" : "ПАУЗА";
    reportLines.push("Кампания: " + camp.getName() + " [ПОИСК] [" + statusText + "]");
    reportLines.push("  - Показы: " + imps + " | Клики: " + clicks + " | Расход: " + cost.toFixed(2) + " " + currency);
    if (conv > 0) {
      reportLines.push("  - Конверсии: " + conv);
    }
    reportLines.push("");
  }

  // ------------------------------------------------------------------
  // 2. ТОРГОВЫЕ КАМПАНИИ (Google Shopping)
  // ------------------------------------------------------------------
  var shopIter = AdsApp.shoppingCampaigns().get();
  while (shopIter.hasNext()) {
    var sCamp = shopIter.next();
    foundCampaignsCount++;
    var sStats = sCamp.getStatsFor("YESTERDAY");
    var sCost = sStats.getCost();
    var sClicks = sStats.getClicks();
    var sImps = sStats.getImpressions();
    var sConv = sStats.getConversions();

    totalCost += sCost;
    totalClicks += sClicks;
    totalImps += sImps;
    totalConv += sConv;

    var sStatusText = sCamp.isEnabled() ? "АКТИВНА" : "ПАУЗА";
    reportLines.push("Кампания: " + sCamp.getName() + " [ПОКУПКИ] [" + sStatusText + "]");
    reportLines.push("  - Показы: " + sImps + " | Клики: " + sClicks + " | Расход: " + sCost.toFixed(2) + " " + currency);
    if (sConv > 0) {
      reportLines.push("  - Конверсии: " + sConv);
    }
    reportLines.push("");
  }

  // ------------------------------------------------------------------
  // 3. ИТОГОВАЯ СВОДКА ЗА ВЧЕРА
  // ------------------------------------------------------------------
  reportLines.push("--------------------------------------------------");
  reportLines.push("ИТОГО ЗА ВЧЕРА (ВСЕ КАМПАНИИ):");
  reportLines.push("• Показов в Google: " + totalImps);
  reportLines.push("• Переходов на сайт: " + totalClicks);
  reportLines.push("• Заказов / конверсий: " + totalConv);
  reportLines.push("• Потрачено: " + totalCost.toFixed(2) + " " + currency);
  reportLines.push("--------------------------------------------------");

  if (totalImps === 0) {
    reportLines.push("ℹ️ Показов за вчера не зафиксировано. Проверьте статус модерации объявлений и баланс.");
  } else if (totalClicks === 0) {
    reportLines.push("ℹ️ Показы идут (" + totalImps + "), объявления участвуют в аукционе Google.");
  }

  var text = reportLines.join("\n");
  Logger.log(text);

  var subject = "💎 Livi Jewelry: Сводка рекламы (" + totalClicks + " кликов, " + totalCost.toFixed(2) + " " + currency + ")";

  try {
    MailApp.sendEmail(CONFIG.ALERT_EMAIL, subject, text);
    Logger.log("[OK] Отчет успешно отправлен на: " + CONFIG.ALERT_EMAIL);
  } catch (e) {
    Logger.log("[!] Ошибка отправки email: " + e.message);
  }
}
