/**
 * ==============================================================================
 * LIVI JEWELRY — GOOGLE ADS AUTOPILOT v5.2 DIAMOND SHIELD (СИНХРОНИЗАЦИЯ СПИСКОВ)
 * ==============================================================================
 * 
 * ЧТО ДЕЛАЕТ ЭТОТ СКРИПТ АВТОМАТИЧЕСКИ:
 * 1. [Auto-Convert "X камень" to Exact] Сам находит в мастер-списке старые фразовые
 *    записи вида "аметист камень" / "нефрит камень", удаляет фразовый вариант и
 *    переводит их в ТОЧНОЕ соответствие [аметист камень], чтобы не резать покупки.
 * 2. [Pre-Emptive Brand Shield] Загружает 175+ корней всех брендов-конкурентов
 *    (включая 12 брендов, которые раньше были только в Exact), мастерских и стоп-слов
 *    во ФРАЗОВОМ соответствии до первого клика.
 * 3. [Strict Silver & Gold 585 Ban (Вариант А)] Полная блокировка любого серебра и
 *    заводского золота 585 пробы (разрешена только «позолота» в связке с нашим камнем).
 * 4. [Full Stone & Kazakh Ethno WhiteList] Защищает все природные камни мастерской
 *    и казахские национальные запросы (әшекей, маржан, меруерт, алқа, білезік, сырға).
 * 5. [No External OAuth] Работает без внешних сетевых запросов — 100% стабильный запуск.
 * ==============================================================================
 */

var CONFIG = {
  ALERT_EMAIL: "viksonna94@gmail.com",
  DAILY_BUDGET_CAP: 10.0,
  MAX_CPC_CAP: 0.20,
  MIN_CPC_FLOOR: 0.05,
  CONVERSION_BID_BOOST: 0.10,
  SAVER_BID_DISCOUNT: 0.05,
  NEGATIVE_LIST_NAME: "Livi Jewelry - Мастер Минус-слова",
  APPLY_CHANGES: true,
  SEND_DAILY_SUMMARY: true
};

// ------------------------------------------------------------------------------
// 0. БАЗОВЫЕ КОРНИ БРЕНДОВ И МУСОРА (ДОБАВЛЯЮТСЯ ВО ФРАЗОВОМ СООТВЕТСТВИИ "...")
// ------------------------------------------------------------------------------
var SEED_ROOT_NEGATIVES = [
  // Все мировые и локальные бренды (включая бывшие Exact из списка 879 слов):
  "swarovski", "сваровски", "сваровский", "тиффани", "tiffany", "картье", "cartier",
  "messika", "мессика", "apm", "monaco", "апм", "монако", "aroush", "larosh",
  "laroush", "ляруш", "merhat", "мерхат", "tallys", "таллис", "sansi", "санси",
  "люченте", "luchente", "lucente", "lucenta", "люцента", "казахювелир", "kazakhyuvelir",
  "пандора", "pandora", "соколов", "sokolov", "санлайт", "sunlight", "ван клиф", "van cleef",
  "ванклив", "балауса", "balausa", "sakina", "сакина", "mone", "chopard", "шопард",
  "булгари", "bulgari", "bvlgari", "tous", "тоус", "адамас", "adamas", "мюз", "miuz",
  "московский ювелирный завод", "серебров", "сереброфф", "serebroff", "дамиани", "damiani",
  "фрайвилле", "frey wille", "сблеском", "sbleskom", "луи витон", "louis vuitton",
  "шанель", "chanel", "эрмес", "hermes", "гуччи", "gucci", "диор", "dior",
  "tatirocks", "athena gaia", "miramira", "moonka", "sania", "sael", "rebecca",
  "tomiris", "shona", "siyera", "viennois", "maria tash", "kruger studios",
  "рене лалик", "lalique", "best wishes", "magic stones", "дерберг керн", "dyrberg",
  "деберкем", "deberquem", "канциан", "graziella", "грациелла", "оксизян", "instyle",
  "сенсатори", "sensatori", "дионис", "dionis", "keklik", "дэвид юрман", "david yurman",
  "кубачи", "каратов", "karatov", "nature bijoux", "ouro", "ластория", "lastoria",
  "вива ла вика", "viva la vika", "tesoro", "meraly", "армат", "armat", "lurea",
  "луара", "luara", "kurshuni", "hefang", "серик рысбек", "serik rysbek", "ларентия",
  "laurentia", "гальяно", "galliano", "леди коллекшн", "lady collection", "anka jewelry",
  "roberto bravo", "роберто браво", "алтын", "altyn", "talisman kz", "микимото",
  "mikimoto", "gotto jewelry", "pure jewelry", "soroka jewelry", "nomination", "номинэйшн",
  "лакоста", "la roche", "jewelry bus", "minimal silver",
  "muraa", "yelai", "jewelfinger", "darry ring", "favory", "farro", "via jewelry",
  "astra jewelry", "le carat", "mimi jewelry", "assos",

  // Изготовление на заказ, ювелирные мастерские, переплавка, гравировка:
  "на заказ", "изготовление на заказ", "изготовление ювелирных", "ювелирная мастерская",
  "ювелирные мастерские", "ювелиры алматы", "ювелир алматы", "ювелир астана", "ювелиры астана",
  "переплавка", "литье золота", "с гравировкой", "гравировка", "сделать подвеску",
  "сделать кольцо", "сделать на заказ", "цепочки на заказ", "кулон на заказ",

  // Школьная литература, фейки клевер/гвоздь:
  "мопассан", "браслет клевер", "колье клевер", "кулон гвоздь", "браслет гвоздь",

  // Общие подарки без указания камня:
  "что подарить", "что можно подарить", "подарить девушке", "подарок девушке",
  "подарок маме", "подарок женщине", "подарки для женщин", "подарок подруге",
  "беспроигрышный подарок",

  // Дети и непрофильные категории изделий:
  "для девочки", "для девочек", "для детей", "брошь", "броши", "брошка",
  "фенечка", "фенечки", "каффы", "пусеты",

  // Нецелевые материалы, подделки, стекло, бисер, серебро, оценка сырья:
  "серебро", "серебряный", "серебряные", "серебряное", "серебряная",
  "муассанит", "xuping", "ксьюпинг", "медицинское золото", "медицинские серьги",
  "муранское стекло", "murano", "мурано", "бисер", "стеклярус", "лабрет", "пирсинг",
  "теннисный браслет", "фигурки детей", "каучук", "шнурок", "снейк", "жемчуг мело",
  "сколько стоит жемчуг", "с буквой", "бусы из шерсти", "ломбард", "скупка",
  "своими руками", "бисероплетение", "алиэкспресс", "aliexpress", "temu", "тему",
  "shein", "шейн", "таобао", "taobao", "секонд хенд", "барахолка", "конфискат",
  "оптом", "авито", "olx", "ярмарка мастеров", "etsy",

  // Оффлайн-поиск и чужое гео:
  "ближайший ювелирный магазин", "ювелирный магазин поблизости", "ювелирный магазин рядом",
  "вьетнам", "шри ланка", "катар", "пхукет", "гоа", "египет", "тайланд",
  "tilla", "ziraklar", "чоловічі"
];

// ------------------------------------------------------------------------------
// 1. БРЕНДЫ-КОНКУРЕНТЫ (БЕЗУСЛОВНЫЙ БАН В ПЕРВУЮ ОЧЕРЕДЬ ВО ФРАЗОВОМ СООТВЕТСТВИИ)
// ------------------------------------------------------------------------------
var COMPETITOR_BRANDS = [
  /swarovski/i, /сваровск/i, /тиффани/i, /tiffany/i, /картье/i, /cartier/i,
  /messika/i, /мессика/i, /apm/i, /monaco/i, /апм/i, /монако/i,
  /aroush/i, /larosh/i, /laroush/i, /ляруш/i, /merhat/i, /мерхат/i,
  /tallys/i, /таллис/i, /sansi/i, /санси/i, /люченте/i, /luchente/i, /lucente/i,
  /lucenta/i, /люцента/i, /казахювелир/i, /kazakhyuvelir/i, /пандор/i, /pandora/i,
  /соколов/i, /sokolov/i, /санлайт/i, /sunlight/i, /ван\s*клиф/i, /van\s*cleef/i,
  /ванклив/i, /балауса/i, /balausa/i, /sakina/i, /сакина/i, /mone\b/i, /chopard/i,
  /шопард/i, /bvlgari/i, /bulgari/i, /булгари/i, /tous\b/i, /тоус/i, /адамас/i,
  /adamas/i, /miuz/i, /мюз/i, /сереброфф/i, /серебров/i, /serebroff/i, /дамиани/i,
  /damiani/i, /фрайвилле/i, /frey wille/i, /сблеском/i, /sbleskom/i, /луи витон/i,
  /louis vuitton/i, /шанель/i, /chanel/i, /эрмес/i, /hermes/i, /гуччи/i, /gucci/i,
  /диор/i, /dior/i, /tatirocks/i, /athena gaia/i, /miramira/i, /moonka/i, /sania\b/i,
  /sael\b/i, /rebecca\b/i, /tomiris/i, /shona\b/i, /siyera/i, /viennois/i,
  /maria tash/i, /kruger studios/i, /лалик/i, /lalique/i, /best wishes/i,
  /magic stones/i, /дерберг керн/i, /dyrberg/i, /deberquem/i, /канциан/i, /canzian/i,
  /грациелла/i, /graziella/i, /оксизян/i, /instyle/i, /сенсатори/i, /sensatori/i,
  /дионис/i, /dionis/i, /keklik/i, /дэвид юрман/i, /david yurman/i, /кубачи/i,
  /каратов/i, /karatov/i, /nature bijoux/i, /ouro/i, /ластория/i, /lastoria/i,
  /вива ла вика/i, /viva la vika/i, /tesoro/i, /meraly/i, /армат/i, /armat\b/i,
  /lurea/i, /луара/i, /luara/i, /kurshuni/i, /hefang/i, /серик рысбек/i,
  /serik rysbek/i, /ларентия/i, /laurentia/i, /гальяно/i, /galliano/i,
  /lady\s*collection/i, /леди коллекшн/i, /anka jewelry/i, /moon\s*(украшения|бижутерия)/i,
  /roberto bravo/i, /роберто браво/i, /алтын\b/i, /altyn\b/i, /talisman\s*kz/i,
  /микимото/i, /mikimoto/i, /gotto jewelry/i, /pure jewelry/i, /soroka jewelry/i,
  /сорока\s*jewelry/i, /nomination/i, /номинэйшн/i, /лакост/i, /lacoste/i,
  /la roche/i, /jewelry bus/i, /minimal\s*silver/i, /браслет minimal/i,
  /muraa/i, /yelai/i, /jewelfinger/i, /darry\s*ring/i, /favory/i, /farro/i,
  /via\s*jewelry/i, /astra\s*jewelry/i, /le\s*carat/i, /mimi\s*jewelry/i, /assos/i
];

// ------------------------------------------------------------------------------
// 2. ЗАЩИТНЫЙ WHITELIST ВСЕХ НАТУРАЛЬНЫХ КАМНЕЙ, КАЗАХСКИХ ТЕРМИНОВ И ИЗДЕЛИЙ МАСТЕРСКОЙ
// ------------------------------------------------------------------------------
var SAFE_ROOTS = [
  /жемчу[гж]/i, /барочн/i, /майорк/i, /majorica/i, /pearl/i,
  /нефрит/i, /жадеит/i, /джедаит/i,
  /аметист/i, /малахит/i, /агат/i, /гранат/i, /кварц/i, /бирюз/i, /гематит/i, /хрустал/i,
  /лунн.*камен/i, /лунн/i, /тигров.*глаз/i, /тигров/i, /лазурит/i, /коралл/i, /яшм/i,
  /сердолик/i, /амазонит/i, /турмалин/i, /цитрин/i, /авантюрин/i, /флюорит/i, /перламутр/i,
  /оникс/i, /шпинел/i, /лабрадор/i, /чароит/i, /хризопраз/i, /змеевик/i,
  /топаз/i, /аквамарин/i, /берилл/i, /опал/i, /янтар/i, /родонит/i, /пирит/i, /содалит/i,
  /морганит/i, /родохрозит/i, /кунцит/i, /халцедон/i, /ларимар/i, /larimar/i, /празиолит/i,
  /хризолит/i, /хризоколл/i, /апатит/i, /танзанит/i, /варисцит/i, /александрит/i,
  /диоптаз/i, /арагонит/i, /aragonite/i, /обсидиан/i, /кошачий.*глаз/i,

  // Казахские термины украшений и этно-стиль:
  /әшекей/i, /бұйым/i, /маржан/i, /меруерт/i, /алқа/i, /білезік/i, /сырға/i, /сырга/i,
  /шашбау/i, /асыл тас/i, /табиғи тас/i,
  /этно/i, /этническ/i, /национальн.*украшен/i, /kazakh jewelry/i,

  // Типы авторских изделий и бренд:
  /сотуар/i, /сатуар/i, /чокер/i, /натуральн.*камн/i, /натуральн.*камен/i,
  /издели.*из.*камн/i, /бусы.*из.*камн/i, /браслет.*из.*камн/i, /колье.*из.*камн/i,
  /авторск.*украшен/i, /livi/i
];

// ------------------------------------------------------------------------------
// 3. СТОП-ПАТТЕРНЫ МУСОРА, МАСТЕРСКИХ, СЕРЕБРА, ЗОЛОТА 585, КОЛЕЦ И ИНФО
// ------------------------------------------------------------------------------
var JUNK_PATTERNS = [
  /мопассан/i, /клевер/i, /гвоздь/i,

  // Производство, ювелирные мастерские, переплавка, гравировка:
  /на заказ/i, /изготовлен/i, /мастерск/i, /переплав/i, /лить[её]/i,
  /гравировк/i, /с надписью/i, /сделать на заказ/i,
  /ювелиры алматы/i, /ювелир алматы/i, /ювелир астана/i, /ювелиры астана/i,

  // Дети, девочки, непрофильные изделия:
  /для девочк/i, /девочке/i, /девочки/i, /для детей/i, /детск/i, /фигурк.*детей/i,
  /брошь/i, /броши/i, /брошка/i, /фенечк/i, /кафф/i, /пусет/i, /галстук/i,

  // Пустые общие онлайн-запросы и иноязычный спам:
  /^заказать онлайн$/i, /^купить онлайн$/i, /чоловічі/i, /срібні/i, /tilla\b/i, /zirak/i,

  // Подарки (разрешены только если в запросе явно указан наш камень из SAFE_ROOTS):
  /(^|\s)подар/i, /что подарить/i, /что можно подарить/i, /день рожден/i, /\bд[рp]\b/i,
  /юбилей/i, /годовщин/i, /молодожен/i, /презент/i, /сюрприз/i,

  // Рукоделие, DIY, детали и фурнитура для сборки:
  /своими руками/i, /как сделать/i, /как сплести/i, /как собрать/i, /научиться делать/i, /схем/i,
  /мастер класс/i, /мк\b/i, /бисероплетени/i, /бисер/i, /плетени/i, /вязани/i,
  /фурнитур/i, /застежк/i, /швенз/i, /штифт/i, /пины\b/i, /леск/i, /проволок/i,
  /тросик/i, /эпоксидн/i, /полимерн.*глин/i, /вышивк/i, /станок/i, /с буквой/i,
  /буква\s+[a-zа-я]/i, /снейк/i,

  // Нецелевые чужие материалы, стекло, пирсинг, оценка сырья:
  /стекл/i, /муранск/i, /murano/i, /мурано/i, /стекляр/i, /шерст/i, /валян/i,
  /муассанит/i, /фианит/i, /дерев/i, /пластик/i, /акрил/i, /силикон/i, /каучук/i,
  /веревочк/i, /на веревк/i, /шнурок/i, /xuping/i, /ксьюпинг/i, /медицинск/i,
  /лабрет/i, /пирсинг/i, /мело\b/i, /melo\b/i, /сколько стоит/i, /аква кварц/i,
  /сутажные/i, /минанкари/i,

  // Халява, ломбарды, скупка, дешевый опт, б/у, маркетплейсы:
  /дешев/i, /недорог/i, /бесплатн/i, /даром/i, /ломбард/i, /скупк/i, /залог/i,
  /сдать/i, /проба/i, /585/i, /750/i, /925/i, /слит/i, /грамм/i, /алиэкспресс/i,
  /aliexpress/i, /temu/i, /тему/i, /shein/i, /шейн/i, /таобао/i, /taobao/i,
  /секонд/i, /барахолк/i, /конфискат/i, /б[\s/]?у\b/i, /оптом/i, /опт\b/i,
  /olx/i, /олх/i, /авито/i, /ярмарка мастеров/i, /etsy/i,

  // Заводское золото, серебро (Вариант А — полный бан), кольца и драгкамни 1-й категории:
  /(^|\s)золот/i, /серебр/i, /serebro/i, /платин/i, /бриллиант/i, /брилиан/i, /diamond/i,
  /изумруд/i, /рубин/i, /сапфир/i, /теннисн/i, /tennis.*bracelet/i,
  /кольц/i, /колечк/i, /перстен/i, /печатка/i, /обручальн/i, /помолвочн/i,
  /парные кольца/i, /на мизинец/i,

  // Одежда и чужие части тела:
  /шапк/i, /рубашк/i, /плать/i, /кофт/i, /пальто/i, /юбк/i, /на ног/i, /через палец/i,

  // Информационные запросы, эзотерика, уход, ремонт:
  /\bвиды\b/i, /разновидност/i, /шакка/i, /sciacca/i,
  /что такое/i, /что это/i, /\bэто$/i, /как называется/i, /как носить/i, /с чем носить/i,
  /бывает ли/i, /для чего/i, /зачем/i, /ремонт/i, /пайк/i, /перетяжк/i, /чистк/i,
  /как почистить/i, /ультразвуков/i, /как отличить/i, /как проверить/i, /как определить/i,
  /как выгляд/i, /подделк/i, /кому подходит/i, /подходит ли/i, /свойств/i, /значени/i,
  /гороскоп/i, /знак.*зодиак/i, /магическ/i, /лечебн/i, /литотерапи/i, /талисман/i,
  /оберег/i, /амулет/i, /приворот/i, /заговор/i, /сонник/i, /к чему снится/i,
  /википеди/i, /месторожден/i, /твердость/i, /формула/i, /фото\b/i, /картинк/i,
  /обои/i, /скачать/i, /видео/i, /реферат/i, /ваканси/i, /резюме/i, /работа/i,
  /зарплат/i, /мужск/i, /для мужчин/i, /мужчин/i, /крестик/i, /четки/i, /тасбих/i,
  /часы/i, /зодиак/i, /овен/i, /телец/i, /тельц/i, /близнец/i, /рак\b/i, /рака/i,
  /лев\b/i, /льва/i, /дева/i, /весы/i, /весов/i, /скорпион/i, /стрелец/i, /козерог/i,
  /водолей/i, /рыбы/i,

  // Гео-туризм и оффлайн-поиск:
  /вьетнам/i, /шри ланк/i, /катар/i, /пхукет/i, /гоа\b/i, /туркестан/i, /египет/i,
  /тайланд/i, /бали\b/i, /milan/i, /милан/i, /греци/i, /япони/i, /украин/i, /дагестан/i,
  /узбекск/i, /турки/i, /турецк/i, /индийск/i, /ближайш/i, /поблизости/i, /рядом/i
];

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

function isTwoWordStoneLookup(term) {
  var clean = (term || "").toLowerCase().trim().replace(/^["\[]|["\]]$/g, "");
  var fwd = /^[а-яёәіңғүұқөһa-z-]+\s+(камень|тас|тасы|виды|вид|цвет|цвета|свойства|цена|стоимость|натуральный|природный)$/i.test(clean);
  var rev = /^(виды|вид|цвет|цвета|свойства|цена|стоимость|натуральный|природный)\s+[а-яёәіңғүұқөһa-z-]+$/i.test(clean);
  return fwd || rev;
}

function evaluateSearchTerm(term) {
  var lower = (term || "").toLowerCase().trim();
  if (!lower) return { isJunk: false, isExactOnly: false, isSafe: false, reason: "Пустой запрос" };

  // 1. Бренд конкурента -> МГНОВЕННЫЙ БАН (Фразовое соответствие)
  for (var b = 0; b < COMPETITOR_BRANDS.length; b++) {
    if (COMPETITOR_BRANDS[b].test(lower)) {
      return { isJunk: true, isExactOnly: false, isSafe: false, reason: "Бренд-конкурент (" + COMPETITOR_BRANDS[b] + ")" };
    }
  }

  var hasSafeStone = isSafeTerm(lower);

  // 2. Проверка на стоп-паттерны
  for (var j = 0; j < JUNK_PATTERNS.length; j++) {
    if (JUNK_PATTERNS[j].test(lower)) {
      var patStr = String(JUNK_PATTERNS[j]);

      // Исключение А: Позолота + наш камень
      var isGoldPlated = /позолот/i.test(lower) && !/(^|\s)золот/i.test(lower);
      if (hasSafeStone && isGoldPlated && patStr.indexOf("золот") !== -1) {
        continue;
      }

      // Исключение Б: Покупка нашего конкретного камня/жемчуга в подарок
      var isGiftPattern = patStr.indexOf("подар") !== -1 || patStr.indexOf("день рожден") !== -1 || patStr.indexOf("юбилей") !== -1;
      if (hasSafeStone && isGiftPattern) {
        continue;
      }

      return { isJunk: true, isExactOnly: false, isSafe: false, reason: "Стоп-паттерн (" + JUNK_PATTERNS[j] + ")" };
    }
  }

  // 3. Инфо-запрос из 2 слов вида "[минерал] камень / тас / тасы" -> ТОЛЬКО ТОЧНОЕ СООТВЕТСТВИЕ [X камень]
  if (isTwoWordStoneLookup(lower)) {
    return { isJunk: true, isExactOnly: true, isSafe: false, reason: "Инфо-запрос [точное соответствие]" };
  }

  return {
    isJunk: false,
    isExactOnly: false,
    isSafe: hasSafeStone,
    reason: hasSafeStone ? "Целевой камень / изделие мастерской" : "Общий целевой запрос"
  };
}

function main() {
  Logger.log("==================================================================");
  Logger.log("   💎 LIVI JEWELRY AUTOPILOT v5.2 DIAMOND SHIELD: ЗАПУСК         ");
  Logger.log("==================================================================");

  var account = AdsApp.currentAccount();
  var accountName = account.getName() || "Livi Jewelry";
  var customerId = account.getCustomerId();
  var currency = account.getCurrencyCode();

  var actionLogs = [];
  var warningsList = [];

  // 1. Привязка мастер-списка, конвертация "X камень" в [X камень] и превентивные бренды
  Logger.log("\n[1/5] Синхронизация мастер-списка и перевод 'X камень' в точное соответствие...");
  var negativeList = getOrCreateNegativeList(CONFIG.NEGATIVE_LIST_NAME, actionLogs);
  var attachedCampaignsCount = attachNegativeListToAllCampaigns(negativeList);
  if (attachedCampaignsCount > 0) {
    actionLogs.push("Мастер-список минус-слов активен на " + attachedCampaignsCount + " кампаниях.");
  }

  // 2. Авто-чистка реальных мусорных запросов за 7 дней
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

  // 5. Детальный сбор статистики за вчера
  Logger.log("\n[5/5] Формирование детального утреннего отчета за вчера...");
  var perfSummary = getYesterdayDetailedPerformance(currency, warningsList);

  // 6. Отправка подробного утреннего email-отчета
  if (CONFIG.SEND_DAILY_SUMMARY || warningsList.length > 0) {
    sendAutopilotEmailReport(accountName, customerId, currency, perfSummary, actionLogs, warningsList);
  }

  Logger.log("\n==================================================================");
  Logger.log("   АВТОПИЛОТ v5.2 DIAMOND SHIELD: Выполнение успешно завершено!   ");
  Logger.log("==================================================================");
}

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

  var existing = {};
  var toConvertExact = [];

  try {
    var it = negList.getNegativeKeywords();
    while (it.hasNext()) {
      var nk = it.next();
      var rawText = nk.getText().toLowerCase().trim();
      var mType = nk.getMatchType();
      var stripped = rawText.replace(/^["\[]|["\]]$/g, "").trim();

      // Если "X камень" записано во фразовом или широком соответствии -> переводим в ТОЧНОЕ [X камень]
      if (isTwoWordStoneLookup(stripped) && mType !== "EXACT") {
        toConvertExact.push({ nkObj: nk, clean: stripped });
      } else {
        existing[stripped] = true;
        existing[rawText] = true;
      }
    }
  } catch (e) {}

  // Авто-конвертация старых фразовых "X камень" в точное соответствие [X камень]
  var convertedCount = 0;
  for (var c = 0; c < toConvertExact.length; c++) {
    var item = toConvertExact[c];
    try {
      if (CONFIG.APPLY_CHANGES) {
        item.nkObj.remove();
        negList.addNegativeKeyword("[" + item.clean + "]");
      }
      existing["[" + item.clean + "]"] = true;
      existing[item.clean] = true;
      convertedCount++;
    } catch (convErr) {}
  }
  if (convertedCount > 0) {
    var convMsg = "Переведено из фразового в точное соответствие [X камень]: " + convertedCount + " шт. (защита покупок с камнями).";
    actionLogs.push(convMsg);
    Logger.log("  🔄 " + convMsg);
  }

  // Превентивная загрузка брендов и стоп-корней во ФРАЗОВОМ соответствии
  var seeded = 0;
  for (var i = 0; i < SEED_ROOT_NEGATIVES.length; i++) {
    var rootWord = SEED_ROOT_NEGATIVES[i].toLowerCase().trim();
    if (!existing[rootWord] && !existing['"' + rootWord + '"']) {
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
    var seedMsg = "Превентивно добавлено во фразовом соответствии: " + seeded + " брендов и стоп-корней.";
    actionLogs.push(seedMsg);
    Logger.log("  🛡️ " + seedMsg);
  }
  return negList;
}

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

function mineJunkSearchTerms(negativeList, actionLogs) {
  var addedCount = 0;
  var existingNegs = {};

  try {
    var negIter = negativeList.getNegativeKeywords();
    while (negIter.hasNext()) {
      existingNegs[negIter.next().getText().toLowerCase().trim()] = true;
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
        // Для "X камень" ставим ТОЧНОЕ соответствие [...], для брендов и мусора — ФРАЗОВОЕ "..."
        var formattedNeg = evalRes.isExactOnly ? ("[" + term + "]") : ('"' + term + '"');
        if (!existingNegs[formattedNeg.toLowerCase()] && !existingNegs[term]) {
          try {
            if (CONFIG.APPLY_CHANGES) {
              negativeList.addNegativeKeyword(formattedNeg);
            }
            existingNegs[formattedNeg.toLowerCase()] = true;
            addedCount++;
            var logMsg = "[Auto-Negated] Заблокирован запрос: " + formattedNeg + " [" + evalRes.reason + "]";
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
              } catch (bidErr) {}
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

function sendAutopilotEmailReport(accountName, customerId, currency, perf, actionLogs, warningsList) {
  var isAlert = warningsList.length > 0;
  var dateStr = Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy");
  var subject = (isAlert ? "⚠️ Внимание: " : "💎 Livi Jewelry: ") +
                "Утренний отчет Google Ads v5.2 DIAMOND SHIELD за вчера (" + dateStr + ") — " +
                perf.totalClicks + " кликов, " + perf.totalCost.toFixed(2) + " " + currency;

  var lines = [];
  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("   LIVI JEWELRY — УТРЕННИЙ БОЕВОЙ ОТЧЕТ AUTOPILOT v5.2 DIAMOND   ");
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
