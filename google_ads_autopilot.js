/**
 * ==============================================================================
 * LIVI JEWELRY — GOOGLE ADS AUTOPILOT v3.2 PRO (МАКСИМАЛЬНАЯ ЗАЩИТА БЮДЖЕТА)
 * ==============================================================================
 * 
 * ЧТО ДЕЛАЕТ ЭТОТ СКРИПТ АВТОМАТИЧЕСКИ КАЖДОЕ УТРО:
 * 1. [Pre-Emptive Brand Shield] Превентивно добавляет чистые корни брендов-конкурентов
 *    (merhat, tallys, aroush, messika, апм, монако, сваровский, пандора и др.)
 *    в мастер-список минус-слов, чтобы блокировать запросы ДО первого клика.
 * 2. [Full Stone WhiteList] Защищает ВСЕ природные минералы и жемчуг (SAFE_ROOTS),
 *    включая топаз, аквамарин, берилл, янтарь, опал и новинки из мастерской жены.
 * 3. [Smart Metal Filter] Разрешает запросы с позолотой и серебряными замками/фурнитурой
 *    для наших камней, но беспощадно блокирует искателей заводского золота 585 пробы,
 *    колец и ломбардов.
 * 4. [TikTok & Encyclopedia Shield] Отсекает информационный мусор по камням (фото,
 *    картинки, как отличить, кому подходит, значение, свойства, «жемчуг мело» из TikTok).
 * 5. [Safe CPC Bidding] Корректирует ставки CPC для ручных групп и безопасно работает
 *    в связке со стратегией «Максимальное количество кликов».
 * 6. [Morning Executive Digest] Каждое утро в 07:00–08:00 шлет полный подробный отчет
 *    по Поиску и Shopping на viksonna94@gmail.com.
 *
 * РАСПИСАНИЕ В GOOGLE ADS: Ежедневно в 07:00 или 08:00 утра (Asia/Almaty).
 * ==============================================================================
 */

var CONFIG = {
  // Email владельца для утреннего дайджеста и предупреждений:
  ALERT_EMAIL: "viksonna94@gmail.com",

  // Лимит дневного расхода аккаунта для предупреждения (валюта USD, бюджет $4.14):
  DAILY_BUDGET_CAP: 6.0,

  // Максимальный потолок ставки CPC (защита от переплат, лимит кампании $0.20):
  MAX_CPC_CAP: 0.20,

  // Минимальный пол ставки CPC:
  MIN_CPC_FLOOR: 0.05,

  // Шаг повышения ставки для конвертящих фраз:
  CONVERSION_BID_BOOST: 0.10, // +10%

  // Шаг экономии для фраз с высоким CTR в топе:
  SAVER_BID_DISCOUNT: 0.05,   // -5%

  // Название мастер-списка минус-слов в аккаунте:
  NEGATIVE_LIST_NAME: "Livi Jewelry - Мастер Минус-слова",

  // Применять ли изменения на боевом аккаунте (true = боевой режим, false = dry-run):
  APPLY_CHANGES: true,

  // Всегда отправлять утреннюю сводку:
  SEND_DAILY_SUMMARY: true
};

// ------------------------------------------------------------------------------
// 0. БАЗОВЫЕ КОРНИ ДЛЯ ПРЕВЕНТИВНОЙ БЛОКИРОВКИ ДО ПЕРВОГО КЛИКА (ФРАЗОВОЕ СООТВЕТСТВИЕ)
// ------------------------------------------------------------------------------
var SEED_ROOT_NEGATIVES = [
  // Бренды-конкуренты (блокируют "брэнд алматы", "брэнд кольцо", "брэнд серьги" превентивно):
  "swarovski", "сваровски", "сваровский", "тиффани", "tiffany", "картье", "cartier",
  "messika", "мессика", "apm", "monaco", "апм", "монако", "aroush", "larosh",
  "laroush", "ляруш", "merhat", "мерхат", "tallys", "таллис", "sansi", "санси",
  "люченте", "luchente", "lucente", "казахювелир", "kazakhyuvelir", "пандора",
  "pandora", "соколов", "sokolov", "санлайт", "sunlight", "ван клиф", "van cleef",
  "балауса", "balausa", "sakina", "сакина", "mone", "chopard", "шопард", "булгари",
  "bulgari", "bvlgari", "tous", "тоус", "адамас", "adamas", "мюз", "miuz",
  "серебров", "сереброфф", "serebroff", "дамиани", "damiani", "фрайвилле", "frey wille",
  "сблеском", "sbleskom", "луи витон", "louis vuitton", "шанель", "chanel",
  "эрмес", "hermes", "гуччи", "gucci", "диор", "dior", "tatirocks", "athena gaia",
  "miramira", "moonka", "sania", "sael", "rebecca", "tomiris", "shona", "siyera",
  "viennois", "maria tash", "kruger studios", "рене лалик", "lalique", "best wishes",
  "magic stones", "дерберг керн", "dyrberg", "деберкем", "deberquem", "канциан",

  // Строгий бан общих подарков (женщины выбирают украшения под себя):
  "подарок", "подарки", "что подарить", "подарить девушке", "подарок девушке",
  "подарок маме", "подарок женщине", "подарок подруге", "день рождения", "юбилей",

  // Нецелевые материалы, подделки, стекло и бисер:
  "муассанит", "xuping", "ксьюпинг", "медицинское золото", "медицинские серьги",
  "муранское стекло", "стекло", "murano", "бисер", "стеклярус", "лабрет",
  "с буквой", "бусы из шерсти", "ломбард", "скупка", "своими руками", "бисероплетение",
  "алиэкспресс", "aliexpress", "temu", "тему", "shein", "шейн", "таобао", "taobao",
  "секонд хенд", "барахолка", "конфискат", "оптом", "авито", "olx",

  // Географический туризм (Google Shopping показывает отпускникам):
  "вьетнам", "шри ланка", "катар", "пхукет", "гоа", "туркестан", "египет", "тайланд"
];

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
  /sakina/i, /сакина/i, /mone\b/i, /chopard/i, /шопард/i, /bvlgari/i, /bulgari/i, /булгари/i,
  /tous\b/i, /тоус/i, /адамас/i, /adamas/i, /miuz/i, /мюз/i,
  /сереброфф/i, /серебров/i, /serebroff/i, /дамиани/i, /damiani/i,
  /фрайвилле/i, /frey wille/i, /сблеском/i, /sbleskom/i, /луи витон/i, /louis vuitton/i,
  /шанель/i, /chanel/i, /эрмес/i, /hermes/i, /гуччи/i, /gucci/i, /диор/i, /dior/i,
  /tatirocks/i, /athena gaia/i, /miramira/i, /moonka/i, /sania\b/i, /sael\b/i,
  /rebecca\b/i, /tomiris/i, /shona\b/i, /siyera/i, /viennois/i, /maria tash/i,
  /kruger studios/i, /лалик/i, /lalique/i, /best wishes/i, /magic stones/i,
  /дерберг керн/i, /dyrberg/i, /deberquem/i, /канциан/i, /canzian/i
];

// ------------------------------------------------------------------------------
// 2. ЗАЩИТНЫЙ WHITELIST ВСЕХ НАТУРАЛЬНЫХ КАМНЕЙ, КАЗАХСКИХ ТЕРМИНОВ И ИЗДЕЛИЙ МАСТЕРСКОЙ
// Включает как текущий каталог, так и минералы в работе у мастера (КАТЕГОРИЧЕСКИ НЕ БЛОКИРОВАТЬ)
// ------------------------------------------------------------------------------
var SAFE_ROOTS = [
  // Жемчуг:
  /жемчуг/i, /барочн/i, /майорк/i,

  // Нефрит и жадеит:
  /нефрит/i, /жадеит/i, /джедаит/i,

  // Классические минералы каталога:
  /аметист/i, /малахит/i, /агат/i, /гранат/i, /кварц/i, /бирюз/i, /гематит/i, /хрустал/i,
  /лунн.*камен/i, /лунн/i, /тигров.*глаз/i, /тигров/i, /лазурит/i, /коралл/i, /яшм/i,
  /сердолик/i, /амазонит/i, /турмалин/i, /цитрин/i, /авантюрин/i, /флюорит/i, /перламутр/i,
  /оникс/i, /шпинел/i, /лабрадор/i, /чароит/i, /хризопраз/i, /змеевик/i,

  // Расширенный список минералов мастерской (топаз, аквамарин, янтарь, кунцит и др.):
  /топаз/i, /аквамарин/i, /берилл/i, /опал/i, /янтарь/i, /родонит/i, /пирит/i, /содалит/i,
  /морганит/i, /родохрозит/i, /кунцит/i, /халцедон/i, /ларимар/i, /празиолит/i,

  // Казахские термины украшений и камней (100% защита):
  /әшекей/i, /бұйым/i, /маржан/i, /меруерт/i, /алқа/i, /білезік/i, /сырға/i, /сырга/i, /тас\b/i, /тасы\b/i,

  // Типы авторских изделий и бренд:
  /сотуар/i, /чокер/i, /натуральн.*камн/i, /авторск.*украшен/i, /livi/i
];

// ------------------------------------------------------------------------------
// 3. СТОП-ПАТТЕРНЫ МУСОРА, ДЕШЕВОГО ОПТА, ЧУЖИХ МЕТАЛЛОВ, ИНФО-ЗАПРОСОВ И КОЛЕЦ
// ------------------------------------------------------------------------------
var JUNK_PATTERNS = [
  // Строгий бан общих подарков (женщины выбирают авторские украшения под себя):
  /(^|\s)подар/i, /что подарить/i, /что можно подарить/i, /день рожден/i, /юбилей/i, /годовщин/i,

  // Рукоделие, DIY, детали и фурнитура для сборки
  /своими руками/i, /как сделать/i, /как сплести/i, /как собрать/i, /научиться делать/i, /схем/i,
  /мастер класс/i, /мк\b/i, /бисероплетени/i, /бисер/i, /плетени/i, /вязани/i,
  /фурнитур/i, /застежк/i, /швенз/i, /штифт/i, /пины\b/i, /леск/i, /проволок/i,
  /тросик/i, /эпоксидн/i, /полимерн.*глин/i, /вышивк/i, /станок/i, /с буквой/i,

  // Нецелевые чужие материалы, стекло, бисер и пирсинг:
  /стекл/i, /муранск/i, /murano/i, /стекляр/i, /шерст/i, /валян/i, /муассанит/i, /фианит/i,
  /дерев/i, /пластик/i, /акрил/i, /силикон/i, /xuping/i, /ксьюпинг/i, /медицинск.*золот/i,
  /медицинск.*серьг/i, /лабрет/i, /пирсинг/i, /мело\b/i, /melo\b/i,

  // Халява, ломбарды, скупка, дешевый опт, б/у, маркетплейсы
  /дешев/i, /недорог/i, /бесплатн/i, /даром/i, /ломбард/i, /скупк/i, /залог/i,
  /сдать/i, /проба/i, /585/i, /750/i, /слит/i, /грамм/i, /алиэкспресс/i,
  /aliexpress/i, /temu/i, /тему/i, /shein/i, /шейн/i, /таобао/i, /taobao/i,
  /секонд/i, /барахолк/i, /конфискат/i, /б[\s/]?у\b/i, /оптом/i, /опт\b/i,
  /olx/i, /олх/i, /авито/i,

  // Заводское золото, кольца и драгкамни 1-й категории (позолота разрешена отдельно)
  /(^|\s)золот/i, /серебр/i, /платин/i, /бриллиант/i, /брилиан/i, /изумруд/i, /рубин/i, /сапфир/i,
  /кольц/i, /колечк/i, /перстен/i, /печатка/i, /обручальн/i, /помолвочн/i,

  // Одежда и ложные цвета одежды:
  /шапк/i, /рубашк/i, /плать/i, /кофт/i, /пальто/i, /юбк/i,

  // Информационные запросы, определения ("что такое бусы"), эзотерика, гео-туризм:
  /что такое/i, /\bэто$/i, /\bэто\s/i,
  /ремонт/i, /пайк/i, /перетяжк/i, /чистк/i, /как почистить/i, /ультразвуков/i,
  /как отличить/i, /как проверить/i, /подделк/i, /кому подходит/i, /свойств/i,
  /значени/i, /гороскоп/i, /знак.*зодиак/i, /магическ/i, /лечебн/i, /литотерапи/i,
  /талисман/i, /оберег/i, /амулет/i, /приворот/i, /заговор/i, /сонник/i, /к чему снится/i,
  /википеди/i, /месторожден/i, /твердость/i, /формула/i, /фото\b/i,
  /картинк/i, /обои/i, /скачать/i, /видео/i, /реферат/i, /ваканси/i, /резюме/i,
  /работа/i, /зарплат/i, /мужск/i, /для мужчин/i, /крестик/i,
  /четки/i, /тасбих/i, /часы/i,
  /вьетнам/i, /шри ланк/i, /катар/i, /пхукет/i, /гоа\b/i, /туркестан/i, /египет/i, /тайланд/i, /бали\b/i,
  /milan/i, /милан/i, /греци/i
];

/**
 * Проверка запроса на наличие корней натуральных минералов и изделий
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
 * 1. Бренд конкурента -> безусловный мгновенный БАН
 * 2. Проверка стоп-паттернов:
 *    - Позолота + наш камень -> ЗАЩИТА (позолоченные замки/фурнитура разрешены)
 *    - Серебряный замок/фурнитура + наш камень -> ЗАЩИТА (серебряные элементы разрешены, кроме колец и лома)
 *    - Чистое золото, кольца, ломбард, DIY, инфо-запросы -> БАН
 * 3. Наш камень/изделие -> ЗАЩИТА
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

  var hasSafeStone = isSafeTerm(lower);

  // 2. Проверка на стоп-паттерны с тонкими исключениями для фурнитуры
  for (var j = 0; j < JUNK_PATTERNS.length; j++) {
    if (JUNK_PATTERNS[j].test(lower)) {
      // Исключение А: Позолота + наш камень (разрешаем позолоченные колье/чокеры, отсекая чистое золото)
      var isGoldPlated = /позолот/i.test(lower) && !/(^|\s)золот/i.test(lower);
      if (hasSafeStone && isGoldPlated && String(JUNK_PATTERNS[j]).indexOf("золот") !== -1) {
        continue;
      }

      // Исключение Б: Серебряный замок/фурнитура/элементы + наш камень (кроме колец, 925 пробы и ломбардов)
      var isSilverFittings = /серебр/i.test(lower) && !/кольц/i.test(lower) && !/проба/i.test(lower) && !/ломбард/i.test(lower);
      if (hasSafeStone && isSilverFittings && String(JUNK_PATTERNS[j]).indexOf("серебр") !== -1) {
        continue;
      }

      // В остальных случаях (камня нет, либо это кольцо/заводское золото/ломбард/инфо-мусор) -> БАН
      return { isJunk: true, isSafe: false, reason: "Стоп-паттерн (" + JUNK_PATTERNS[j] + ")" };
    }
  }

  // 3. Запрос вида "[минерал] камень" без коммерческого намерения (например: "аметист камень")
  if (/^[а-яёa-z]+\s+камень$/i.test(lower)) {
    return { isJunk: true, isSafe: false, reason: "Инфо-запрос о минерале (X камень)" };
  }

  return {
    isJunk: false,
    isSafe: hasSafeStone,
    reason: hasSafeStone ? "Целевой камень / изделие мастерской" : "Общий целевой запрос"
  };
}

function main() {
  Logger.log("==================================================================");
  Logger.log("   💎 LIVI JEWELRY AUTOPILOT v3.2 PRO: ЗАПУСК ОПТИМИЗАЦИИ        ");
  Logger.log("==================================================================");

  var account = AdsApp.currentAccount();
  var accountName = account.getName() || "Livi Jewelry";
  var customerId = account.getCustomerId();
  var currency = account.getCurrencyCode();

  var actionLogs = [];
  var warningsList = [];

  // 1. Привязка мастер-списка и превентивная загрузка базовых корней брендов
  Logger.log("\n[1/5] Проверка мастер-списка и превентивных стоп-корней...");
  var negativeList = getOrCreateNegativeList(CONFIG.NEGATIVE_LIST_NAME, actionLogs);
  var attachedCampaignsCount = attachNegativeListToAllCampaigns(negativeList);
  if (attachedCampaignsCount > 0) {
    actionLogs.push("Мастер-список минус-слов активен на " + attachedCampaignsCount + " кампаниях.");
  }

  // 2. Авто-чистка реальных мусорных запросов за 7 дней с защитой WhiteList
  Logger.log("\n[2/5] Анализ поисковых запросов за 7 дней...");
  mineJunkSearchTerms(negativeList, actionLogs);

  // 3. Управление ставками CPC ключевых слов
  Logger.log("\n[3/5] Оптимизация ставок CPC ключевых слов...");
  optimizeKeywordBids(actionLogs);

  // 4. Проверка корректности целевых посадочных страниц
  Logger.log("\n[4/5] Проверка корректности целевых страниц объявлений...");
  var landingPageAlerts = auditLandingPages();
  for (var b = 0; b < landingPageAlerts.length; b++) {
    warningsList.push(landingPageAlerts[b]);
  }

  // 5. Детальный сбор статистики за вчера (Поиск + Shopping + Запросы)
  Logger.log("\n[5/5] Формирование детального утреннего отчета за вчера...");
  var perfSummary = getYesterdayDetailedPerformance(currency, warningsList);

  // 6. Отправка подробного утреннего email-отчета
  if (CONFIG.SEND_DAILY_SUMMARY || warningsList.length > 0) {
    sendAutopilotEmailReport(accountName, customerId, currency, perfSummary, actionLogs, warningsList);
  }

  Logger.log("\n==================================================================");
  Logger.log("   АВТОПИЛОТ v3.2 PRO: Выполнение успешно завершено!             ");
  Logger.log("==================================================================");
}

/**
 * Получение списка минус-слов и превентивное наполнение корнями брендов/мусора
 */
function getOrCreateNegativeList(listName, actionLogs) {
  var listIter = AdsApp.negativeKeywordLists().withCondition("Name = '" + listName + "'").get();
  var negList;
  if (listIter.hasNext()) {
    negList = listIter.next();
    Logger.log("  ✓ Список минус-слов найден в аккаунте: " + listName);
  } else {
    var builder = AdsApp.newNegativeKeywordListBuilder().withName(listName).build();
    negList = builder.getResult();
    Logger.log("  ✓ Создан новый список минус-слов: " + listName);
  }

  // Считываем уже добавленные минус-слова, чтобы избежать повторов
  var existing = {};
  try {
    var it = negList.getNegativeKeywords();
    while (it.hasNext()) {
      existing[it.next().getText().toLowerCase().replace(/^"|"$/g, "")] = true;
    }
  } catch (e) {}

  // Превентивно загружаем корневые слова брендов и стоп-паттернов
  var seeded = 0;
  for (var i = 0; i < SEED_ROOT_NEGATIVES.length; i++) {
    var rootWord = SEED_ROOT_NEGATIVES[i].toLowerCase();
    if (!existing[rootWord]) {
      try {
        if (CONFIG.APPLY_CHANGES) {
          negList.addNegativeKeyword('"' + rootWord + '"');
        }
        existing[rootWord] = true;
        seeded++;
      } catch (err) {}
    }
  }
  if (seeded > 0) {
    var seedMsg = "Превентивно добавлено " + seeded + " базовых корней минус-слов (бренды конкурентов и стоп-корни).";
    actionLogs.push(seedMsg);
    Logger.log("  🛡️ " + seedMsg);
  }
  return negList;
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
 * Анализ поисковых запросов за 7 дней и авто-минусация чистого мусора
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
      var term = (row.searchTermView.search_term || row.searchTermView.searchTerm || "").trim().toLowerCase();
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

  return addedCount;
}

/**
 * Корректировка ставок CPC ключевых слов (безопасно для Smart Bidding / Maximize Clicks)
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

      if (convs > 0) {
        if (currentCpc < CONFIG.MAX_CPC_CAP) {
          var newBoostedCpc = Math.min(CONFIG.MAX_CPC_CAP, Number((currentCpc * (1 + CONFIG.CONVERSION_BID_BOOST)).toFixed(2)));
          if (newBoostedCpc > currentCpc) {
            var applied = false;
            if (CONFIG.APPLY_CHANGES) {
              try {
                kw.bidding().setCpc(newBoostedCpc);
                applied = true;
              } catch (bidErr) {
                // Если стратегия автоматическая («Максимум кликов»), ручная ставка не поддерживается
              }
            }
            if (applied || !CONFIG.APPLY_CHANGES) {
              stats.boosted++;
              var boostMsg = "[Bid Boost] Ключ \"" + kw.getText() + "\" (" + convs + " конв.): CPC " + currentCpc + " ➔ " + newBoostedCpc;
              actionLogs.push(boostMsg);
            }
          }
        }
      } else if (clicks >= 12 && ctr >= 8.0) {
        if (currentCpc > CONFIG.MIN_CPC_FLOOR) {
          var newDiscountCpc = Math.max(CONFIG.MIN_CPC_FLOOR, Number((currentCpc * (1 - CONFIG.SAVER_BID_DISCOUNT)).toFixed(2)));
          if (newDiscountCpc < currentCpc) {
            var appliedSave = false;
            if (CONFIG.APPLY_CHANGES) {
              try {
                kw.bidding().setCpc(newDiscountCpc);
                appliedSave = true;
              } catch (bidErr) {}
            }
            if (appliedSave || !CONFIG.APPLY_CHANGES) {
              stats.saved++;
              var saveMsg = "[Bid Saver] Ключ \"" + kw.getText() + "\" (CTR " + ctr.toFixed(1) + "%): CPC " + currentCpc + " ➔ " + newDiscountCpc;
              actionLogs.push(saveMsg);
            }
          }
        }
      }
    }
  } catch (e) {}
  return stats;
}

/**
 * Проверка конечных URL объявлений
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
  } catch (e) {}
  return alerts;
}

/**
 * Сбор вчерашней статистики по Поиску, Shopping и запросам
 */
function getYesterdayDetailedPerformance(currency, warningsList) {
  var searchTotals = { imps: 0, clicks: 0, cost: 0, convs: 0, campaigns: [] };
  var shoppingTotals = { imps: 0, clicks: 0, cost: 0, convs: 0, campaigns: [] };

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
  } catch (err) {}

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
 * Отправка подробного утреннего email-отчета
 */
function sendAutopilotEmailReport(accountName, customerId, currency, perf, actionLogs, warningsList) {
  var isAlert = warningsList.length > 0;
  var dateStr = Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy");
  var subject = (isAlert ? "⚠️ Внимание: " : "💎 Livi Jewelry: ") +
                "Утренний отчет Google Ads v3.2 PRO за вчера (" + dateStr + ") — " +
                perf.totalClicks + " кликов, " + perf.totalCost.toFixed(2) + " " + currency;

  var lines = [];
  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("   LIVI JEWELRY — УТРЕННИЙ БОЕВОЙ ОТЧЕТ AUTOPILOT v3.2 PRO       ");
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

  lines.push("📊 ОБЩИЕ ПОКАЗАТЕЛИ ЗА ВЧЕРА:");
  lines.push("  • Всего показов: " + perf.totalImps);
  lines.push("  • Всего кликов: " + perf.totalClicks);
  lines.push("  • Общий расход: " + perf.totalCost.toFixed(2) + " " + currency);
  lines.push("  • Конверсий: " + perf.totalConvs);
  var overallCtr = perf.totalImps > 0 ? (perf.totalClicks / perf.totalImps) * 100 : 0;
  var overallCpc = perf.totalClicks > 0 ? (perf.totalCost / perf.totalClicks) : 0;
  lines.push("  • Общий CTR: " + overallCtr.toFixed(2) + "%");
  lines.push("  • Средний CPC: " + overallCpc.toFixed(2) + " " + currency + "\n");

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

  lines.push("⚠️ ЗАПРОСЫ С РАСХОДОМ БЕЗ КОНВЕРСИЙ (НА РУЧНУЮ ПРОВЕРКУ):");
  if (perf.spendWithoutConvQueries.length > 0) {
    for (var sw = 0; sw < perf.spendWithoutConvQueries.length; sw++) {
      var swItem = perf.spendWithoutConvQueries[sw];
      var statusTag = swItem.isSafe
        ? " [🛡️ В WhiteList натуральных камней — защита от блокировки]"
        : (swItem.isJunk ? " [🚫 Заблокировано автопилотом: " + swItem.reason + "]" : " [🔍 Общий запрос — на решение владельца]");
      lines.push("  • «" + swItem.term + "»" + statusTag +
                 ": расход " + swItem.cost.toFixed(2) + " " + currency +
                 ", кликов: " + swItem.clicks + " (" + swItem.campaign + ")");
    }
  } else {
    lines.push("  ✓ Все запросы с расходом либо сконвертировались, либо расход равен нулю.");
  }
  lines.push("");

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
