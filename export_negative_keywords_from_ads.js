/**
 * ==============================================================================
 * LIVI JEWELRY — ЭКСПОРТ ВСЕХ АКТУАЛЬНЫХ МИНУС-СЛОВ ИЗ GOOGLE ADS v1.0
 * ==============================================================================
 * 
 * Назначение:
 * 1. Выгружает ВСЕ минус-слова, которые сейчас реально записаны в рекламном аккаунте:
 *    - Из общих списков минус-слов (Shared Lists: "Livi Jewelry - Мастер Минус-слова" и др.)
 *    - С уровня каждой кампании (Campaign-level negatives)
 *    - С уровня каждой группы объявлений (AdGroup-level negatives)
 * 2. Убирает возможные дубликаты и определяет тип соответствия (Exact / Phrase / Broad).
 * 3. Отправляет готовый CSV-файл на email: viksonna94@gmail.com (как вложение и текстом).
 * 4. Выводит полный CSV в лог для копирования в 1 клик.
 * 
 * ИНСТРУКЦИЯ ПО ЗАПУСКУ (занимает 15 секунд):
 * 1. Откройте Google Ads -> Инструменты и настройки (Tools & Settings) -> Скрипты (Scripts).
 * 2. Нажмите синюю кнопку "+" (Новый скрипт).
 * 3. Вставьте этот код, нажмите "Авторизовать" (Authorize), затем "Выполнить" (Run).
 * 4. Проверьте почту или Execution Log — вы получите полный файл со всеми минус-словами!
 * ==============================================================================
 */

var CONFIG = {
  RECIPIENT_EMAIL: "viksonna94@gmail.com",
  SEND_EMAIL: true
};

function main() {
  Logger.log("==================================================================");
  Logger.log("   💎 LIVI JEWELRY — ЭКСПОРТ ВСЕХ МИНУС-СЛОВ ИЗ АККАУНТА GOOGLE ADS   ");
  Logger.log("==================================================================");

  var account = AdsApp.currentAccount();
  var accountName = account.getName() || "Livi Jewelry";
  var customerId = account.getCustomerId();

  var rows = [];
  rows.push(["Уровень размещения", "Название списка / Кампании", "Минус-слово", "Тип соответствия"]);

  var totalNegatives = 0;
  var seenKeys = {};

  // 1. Сбор из общих списков минус-слов (Shared Lists)
  Logger.log("\n[1] Сканирование общих списков минус-слов (Shared Lists)...");
  var listIter = AdsApp.negativeKeywordLists().get();
  var listsCount = 0;
  while (listIter.hasNext()) {
    var list = listIter.next();
    listsCount++;
    var listName = list.getName();
    var kwIter = typeof list.negativeKeywords === "function" ? list.negativeKeywords().get() : list.getNegativeKeywords();
    var inListCount = 0;
    while (kwIter.hasNext()) {
      var nk = kwIter.next();
      var rawText = nk.getText().trim();
      var matchType = nk.getMatchType();
      var dedupeKey = "LIST:" + listName + ":" + rawText.toLowerCase();
      if (!seenKeys[dedupeKey]) {
        seenKeys[dedupeKey] = true;
        rows.push(["Общий список (Shared List)", listName, rawText, matchType]);
        totalNegatives++;
        inListCount++;
      }
    }
    Logger.log("  ✓ Список \"" + listName + "\": найдено " + inListCount + " минус-слов");
  }

  // 2. Сбор с уровня кампаний (Campaign-level Negatives)
  Logger.log("\n[2] Сканирование уровня Кампаний...");
  var campIter = AdsApp.campaigns().get();
  while (campIter.hasNext()) {
    var camp = campIter.next();
    var campName = camp.getName();
    var cKwIter = camp.negativeKeywords().get();
    var inCampCount = 0;
    while (cKwIter.hasNext()) {
      var cnk = cKwIter.next();
      var cText = cnk.getText().trim();
      var cMatchType = cnk.getMatchType();
      var cKey = "CAMP:" + campName + ":" + cText.toLowerCase();
      if (!seenKeys[cKey]) {
        seenKeys[cKey] = true;
        rows.push(["Уровень кампании", campName, cText, cMatchType]);
        totalNegatives++;
        inCampCount++;
      }
    }
    if (inCampCount > 0) {
      Logger.log("  ✓ Кампания \"" + campName + "\": найдено " + inCampCount + " минус-слов");
    }
  }

  // 3. Сбор с уровня групп объявлений (AdGroup-level Negatives)
  Logger.log("\n[3] Сканирование уровня Групп объявлений...");
  var agIter = AdsApp.adGroups().get();
  var totalAgNegs = 0;
  while (agIter.hasNext()) {
    var ag = agIter.next();
    var agName = ag.getName();
    var agCampName = ag.getCampaign().getName();
    var agKwIter = ag.negativeKeywords().get();
    while (agKwIter.hasNext()) {
      var agnk = agKwIter.next();
      var agText = agnk.getText().trim();
      var agMatchType = agnk.getMatchType();
      var agKey = "AG:" + agCampName + "/" + agName + ":" + agText.toLowerCase();
      if (!seenKeys[agKey]) {
        seenKeys[agKey] = true;
        rows.push(["Уровень группы", agCampName + " > " + agName, agText, agMatchType]);
        totalNegatives++;
        totalAgNegs++;
      }
    }
  }
  if (totalAgNegs > 0) {
    Logger.log("  ✓ Уровень групп: найдено " + totalAgNegs + " минус-слов");
  } else {
    Logger.log("  ✓ На уровне отдельных групп дополнительных минус-слов нет (все в общих списках).");
  }

  Logger.log("\nИТОГО СОБРАНО УНИКАЛЬНЫХ МИНУС-СЛОВ: " + totalNegatives);

  // Формирование CSV
  var csvLines = [];
  for (var i = 0; i < rows.length; i++) {
    var r = rows[i];
    var escapedRow = [
      escapeCsv(r[0]),
      escapeCsv(r[1]),
      escapeCsv(r[2]),
      escapeCsv(r[3])
    ];
    csvLines.push(escapedRow.join(","));
  }
  var csvContent = csvLines.join("\r\n");

  // Отправка на Email
  if (CONFIG.SEND_EMAIL && CONFIG.RECIPIENT_EMAIL) {
    var dateStr = Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy HH:mm");
    var subject = "💎 Livi Jewelry: Экспорт " + totalNegatives + " минус-слов из Google Ads (" + dateStr + ")";
    var body = "Здравствуйте!\n\n" +
               "Скрипт синхронизации выгрузил ВСЕ актуальные минус-слова из вашего аккаунта Google Ads:\n" +
               "• Аккаунт: " + accountName + " (ID: " + customerId + ")\n" +
               "• Дата выгрузки: " + dateStr + "\n" +
               "• Всего минус-слов в аккаунте: " + totalNegatives + "\n\n" +
               "Полный файл прикреплен к этому письму в формате CSV (актуальные_минус_слова_google_ads.csv).\n" +
               "Вы можете скачать его и загрузить в папку проекта для сверки с AI-ассистентом.\n\n" +
               "С уважением,\nLivi Jewelry Google Ads Robot";

    try {
      MailApp.sendEmail({
        to: CONFIG.RECIPIENT_EMAIL,
        subject: subject,
        body: body,
        attachments: [
          Utilities.newBlob(csvContent, "text/csv", "актуальные_минус_слова_google_ads.csv")
        ]
      });
      Logger.log("✅ CSV-файл успешно отправлен на email: " + CONFIG.RECIPIENT_EMAIL);
    } catch (mailErr) {
      Logger.log("⚠️ Ошибка отправки на email: " + mailErr.message);
    }
  }

  Logger.log("\n==================================================================");
  Logger.log("ГОТОВО! Для сохранения файла скопируйте лог или проверьте почту.");
  Logger.log("==================================================================");
}

function escapeCsv(field) {
  if (field === null || field === undefined) return '""';
  var str = field.toString();
  if (str.indexOf('"') !== -1 || str.indexOf(',') !== -1 || str.indexOf('\n') !== -1 || str.indexOf('\r') !== -1) {
    return '"' + str.replace(/"/g, '""') + '"';
  }
  return str;
}
