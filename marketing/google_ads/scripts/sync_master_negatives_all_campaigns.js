/**
 * Google Ads Script: Сквозная привязка существующего мастер-списка минус-слов ко всем кампаниям
 * Мастерская украшений Livi Jewelry (Астана, livijewelry.kz)
 * Аккаунт Google Ads: 167-939-74126
 *
 * ЧТО ДЕЛАЕТ ЭТОТ СКРИПТ:
 * 1. НЕ ИЗМЕНЯЕТ, НЕ ДОБАВЛЯЕТ И НЕ УДАЛЯЕТ НИ ОДНОГО СЛОВА в ваших списках!
 *    (Всеми словами продолжает управлять ваш скрипт-автопилот).
 * 2. Находит ваш готовый, живой мастер-список "Livi Jewelry - Мастер Минус-слова".
 * 3. Проверяет привязку списка ко ВСЕМ кампаниям аккаунта:
 *    - Поисковые кампании (Search: "Livi Jewelry - Поиск Казахстан" и др.)
 *    - Торговые кампании (Google Shopping: "Sales-Shopping-1" и др.)
 * 4. Если кампания Shopping еще не была привязана к списку — скрипт мгновенно привязывает её.
 * 5. Выводит понятный и прозрачный отчет: какая кампания к какому списку подключена.
 *
 * ИНСТРУКЦИЯ ПО ЗАПУСКУ (30 секунд):
 * 1. В Google Ads откройте: Инструменты и настройки (Tools & Settings) -> Скрипты (Scripts).
 * 2. Нажмите синюю кнопку "+" (Новый скрипт).
 * 3. Назовите: "Привязка Мастер-списка к Shopping и Поиску".
 * 4. Вставьте этот код и нажмите "Авторизовать" (Authorize), затем "Выполнить" (Run).
 */

var CONFIG = {
  // Название вашего рабочего мастер-списка, который ведет автопилот:
  MASTER_LIST_NAME: "Livi Jewelry - Мастер Минус-слова",

  // Применять изменения в аккаунте (true = связать кампании)
  APPLY_CHANGES: true
};

function main() {
  Logger.log("==================================================================");
  Logger.log("💎 LIVI JEWELRY: ПРИВЯЗКА МАСТЕР-СПИСКА МИНУС-СЛОВ КО ВСЕМ КАМПАНИЯМ");
  Logger.log("   (Только связка списков. Слова внутри списков НЕ затрагиваются)");
  Logger.log("==================================================================");

  // 1. Поиск всех списков минус-слов в аккаунте
  Logger.log("\n[1] Поиск списков минус-слов в аккаунте...");
  var allListsIter = AdsApp.negativeKeywordLists().get();
  var foundLists = [];
  var targetMasterList = null;

  while (allListsIter.hasNext()) {
    var list = allListsIter.next();
    var name = list.getName();
    foundLists.push(name);
    if (name.toLowerCase() === CONFIG.MASTER_LIST_NAME.toLowerCase()) {
      targetMasterList = list;
    }
  }

  Logger.log("  Всего найдено списков в аккаунте: " + foundLists.length);
  for (var i = 0; i < foundLists.length; i++) {
    Logger.log("  • Список #" + (i + 1) + ": \"" + foundLists[i] + "\"");
  }

  if (!targetMasterList) {
    Logger.log("\n❌ ОШИБКА: Список с именем \"" + CONFIG.MASTER_LIST_NAME + "\" не найден!");
    Logger.log("Проверьте точное название списка в разделе «Инструменты и настройки -> Списки минус-слов».");
    return;
  }

  Logger.log("\n✓ Целевой мастер-список найден: \"" + targetMasterList.getName() + "\"");

  // 2. Обработка поисковых кампаний (Search)
  Logger.log("\n[2] Проверка ПОИСКОВЫХ кампаний (Search)...");
  var searchIter = AdsApp.campaigns().get();
  var searchTotal = 0;
  var searchAlreadyLinked = 0;
  var searchNewlyLinked = 0;

  while (searchIter.hasNext()) {
    var camp = searchIter.next();
    var campName = camp.getName();
    searchTotal++;

    var isAttached = checkCampaignHasList(camp, targetMasterList.getName());
    if (isAttached) {
      searchAlreadyLinked++;
      Logger.log("  [Search] ✓ " + campName + " -> Уже защищен мастер-списком");
    } else {
      if (CONFIG.APPLY_CHANGES) {
        try {
          camp.addNegativeKeywordList(targetMasterList);
          searchNewlyLinked++;
          Logger.log("  [Search] 🔗 " + campName + " -> УСПЕШНО ПРИВЯЗАН к мастер-списку!");
        } catch (errSearch) {
          Logger.log("  [Search] ⚠️ " + campName + " -> Ошибка привязки: " + errSearch);
        }
      } else {
        Logger.log("  [Search] [Preview] " + campName + " -> Требуется привязка");
      }
    }
  }

  // 3. Обработка торговых кампаний (Google Shopping)
  Logger.log("\n[3] Проверка ТОРГОВЫХ кампаний (Google Shopping)...");
  var shoppingTotal = 0;
  var shoppingAlreadyLinked = 0;
  var shoppingNewlyLinked = 0;

  try {
    var shopIter = AdsApp.shoppingCampaigns().get();
    while (shopIter.hasNext()) {
      var sCamp = shopIter.next();
      var sCampName = sCamp.getName();
      shoppingTotal++;

      var sIsAttached = checkCampaignHasList(sCamp, targetMasterList.getName());
      if (sIsAttached) {
        shoppingAlreadyLinked++;
        Logger.log("  [Shopping] ✓ " + sCampName + " -> Уже защищен мастер-списком");
      } else {
        if (CONFIG.APPLY_CHANGES) {
          try {
            sCamp.addNegativeKeywordList(targetMasterList);
            shoppingNewlyLinked++;
            Logger.log("  [Shopping] 🔗 " + sCampName + " -> УСПЕШНО ПРИВЯЗАН к мастер-списку!");
          } catch (errShop) {
            Logger.log("  [Shopping] ⚠️ " + sCampName + " -> Ошибка привязки: " + errShop);
          }
        } else {
          Logger.log("  [Shopping] [Preview] " + sCampName + " -> Требуется привязка");
        }
      }
    }
  } catch (eShop) {
    Logger.log("  [Shopping] Исключение при чтении торговых кампаний: " + eShop);
  }

  // 4. Итоговый отчет
  Logger.log("\n==================================================================");
  Logger.log("🎉 ИТОГИ СИНХРОНИЗАЦИИ КАМПАНИЙ:");
  Logger.log("   • Мастер-список: \"" + targetMasterList.getName() + "\"");
  Logger.log("   • Поисковых кампаний всего: " + searchTotal);
  Logger.log("     - Были привязаны ранее: " + searchAlreadyLinked);
  Logger.log("     - Вновь привязано: " + searchNewlyLinked);
  Logger.log("   • Shopping кампаний всего: " + shoppingTotal);
  Logger.log("     - Были привязаны ранее: " + shoppingAlreadyLinked);
  Logger.log("     - Вновь привязано: " + shoppingNewlyLinked);
  Logger.log("   • Изменения в словах списка: 0 (список остался нетронутым)");
  Logger.log("==================================================================");
}

/**
 * Проверяет, привязан ли уже указанный список минус-слов к кампании
 */
function checkCampaignHasList(campaign, targetListName) {
  try {
    if (typeof campaign.negativeKeywordLists === "function") {
      var listsIter = campaign.negativeKeywordLists().get();
      while (listsIter.hasNext()) {
        var existingList = listsIter.next();
        if (existingList.getName().toLowerCase() === targetListName.toLowerCase()) {
          return true;
        }
      }
    }
  } catch (e) {
    // В случае ограничений API возвращаем false для попытки привязки
  }
  return false;
}
