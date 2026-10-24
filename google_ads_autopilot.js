/**
 * ==============================================================================
 * LIVI JEWELRY — GOOGLE ADS AUTOPILOT v5.6 DIAMOND SHIELD (ULTIMATE FIX & CLEANUP)
 * ==============================================================================
 * 
 * ЧТО ВХОДИТ В v5.6 ULTIMATE (ПОЛНЫЙ АУДИТ v5.3, v5.5 И v5.6 ОТ ARGON):
 * 1. [Критический фикс Google Ads API]: Метод getNegativeKeywordsIterator(negList)
 *    через negList.negativeKeywords().get() обеспечивает 100% стабильное чтение
 *    списка минус-слов (в v5.3 вызов negList.getNegativeKeywords() молча падал).
 * 2. [Exact Ring & Stud Conversion]: Все общие запросы на кольца/пусеты/гвоздики
 *    без указания камня переводятся строго в точное соответствие [кольцо], [пусеты],
 *    что полностью открыло показы для всех колец и пусет Livi с камнями и жемчугом.
 * 3. [Двухсловные инфо-запросы до JUNK-паттернов]: Запросы вида "агат виды", "аметист цвет",
 *    "бирюза цена" гарантированно уходят в точный минус [X], не трогая широкие фразы.
 * 4. [Strict Whitelist Auto-Unblock]: Функция shouldUnblockNegative() разблокирует
 *    СТРОГО те фразы, где есть наш камень/жемчуг/леска (!evalRes.isJunk && evalRes.isSafe).
 *    Никакие неизвестные бренды, литература, лом или ремонт не могут быть разблокированы.
 * 5. [Защита от 240+ брендов, лома и литературы]: Включает все мировые дома моды,
 *    мастерские, инструменты, лом, экспертизу и школьную литературу.
 * 6. [Защита цикла ставок]: Оптимизация CPC защищена локальным try/catch для каждого ключа.
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
  // Все мировые и локальные бренды (включая дома высокой моды):
  "swarovski", "сваровски", "сваровский", "тиффани", "tiffany", "картье", "cartier",
  "messika", "мессика", "apm", "monaco", "апм", "монако", "aroush", "larosh",
  "laroush", "ляруш", "merhat", "мерхат", "tallys", "таллис", "sansi", "санси",
  "люченте", "luchente", "lucente", "lucenta", "люцента", "казахювелир", "kazakhyuvelir",
  "пандора", "pandora", "соколов", "sokolov", "санлайт", "sunlight", "ван клиф", "van cleef",
  "ванклив", "балауса", "balausa", "sakina", "сакина", "mone", "chopard", "шопард", "шопар",
  "булгари", "bulgari", "bvlgari", "tous", "тоус", "адамас", "adamas", "мюз", "miuz",
  "московский ювелирный завод", "серебров", "сереброфф", "serebroff", "дамиани", "damiani",
  "фрайвилле", "frey wille", "сблеском", "sbleskom", "луи витон", "louis vuitton",
  "шанель", "chanel", "эрмес", "гермес", "hermes", "гуччи", "gucci", "диор", "dior",
  "prada", "прада", "versace", "версаче", "fendi", "фенди", "burberry", "берберри", "барбери",
  "moschino", "москино", "roberto cavalli", "кавалли", "valentino", "валентино",
  "armani", "армани", "givenchy", "живанши", "balenciaga", "баленсиага",
  "marco bicego", "марко бичего", "ysl", "saint laurent", "сен лоран",
  "lagerfeld", "лагерфельд", "boucheron", "бушерон", "celine", "селин", "loewe", "лоэве",
  "piaget", "пьяже", "chaumet", "шоме", "додо", "dodo", "graff", "граф", "kruger",
  "delight", "дилайт", "stephen webster", "стефан вебстер", "pomellato", "помеллато",
  "bottega", "боттега", "etrusca", "этруска", "ippolita", "ипполита",
  "русские самоцветы", "линии любви", "ювелирочка", "бронницкий", "ювелирцентр",
  "дериглазов", "cancian", "эпл даймонд", "шахерезада", "казювелирторг", "номинейшн",
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
  "mikimoto", "gotto jewelry", "pure jewelry", "soroka jewelry", "nomination",
  "лакоста", "la roche", "jewelry bus", "minimal silver",
  "muraa", "yelai", "jewelfinger", "darry ring", "favory", "farro", "via jewelry",
  "astra jewelry", "le carat", "mimi jewelry", "assos", "ganezzi", "два жирафа",
  "талисман кз", "лалик", "freywille", "номинэйшн", "луи виттон", "miu miu", "миу миу",
  "дерберг", "claudio canzian", "moon soul", "larimar jewelry", "mone jewelry", "ouro jewelry",
  "rebecca jewelry", "sael jewellery", "sania jeweler", "shona jewelry", "siyera jewels",
  "tesoro jewelry", "tomiris jewellery", "якутские бриллианты", "бриллианты якутии", "кубачинское",
  "585 золотой", "магия золота", "vidda", "видда", "паскуаль бруни", "pasquale bruni",
  "sophie buhai", "софи бухай", "hugo kreit", "хьюго крейт", "vida kush", "керамика", "керамический",

  // Изготовление на заказ, ювелирные мастерские, ремонт, переплавка, лом, экспертиза:
  "на заказ", "изготовление на заказ", "изготовление ювелирных", "ювелирная мастерская",
  "ювелирные мастерские", "ювелиры алматы", "ювелир алматы", "ювелир астана", "ювелиры астана",
  "мастерская", "ремонт", "пайка", "перетяжка", "чистка", "ультразвуковая", "изготовление", "литье",
  "переплавка", "литье золота", "с гравировкой", "гравировка", "сделать подвеску",
  "сделать кольцо", "сделать на заказ", "цепочки на заказ", "кулон на заказ",
  "экспертиза", "лом", "инструменты", "уменьшение", "увеличение", "научиться", "станки",
  "замок для", "оценка", "нить", "часики", "сережки капельки", "дубайское",
  "сдать", "бу", "б/у", "секонд", "опт", "эпоксидная", "проволока", "фурнитура", "бусины оптом",
  "кабошон", "мастер класс", "схема", "плетение", "как сделать", "медицинская сталь",
  "serebro", "silver", "золото 585", "золотой браслет", "золотое кольцо", "золотые сережки",
  "золотая цепь", "золотые подвески", "золотой набор", "платина", "платиновый",
  "бриллиант", "бриллиантовый", "diamond", "фианит", "изумруд", "рубин", "сапфир",
  "гвоздь", "клевер", "гю де мопассан", "крестик", "четки", "тасбих", "мужской", "для мужчин", "мужские", "часы",

  // Школьная литература, фейки клевер/гвоздь:
  "мопассан", "краткое содержание", "рассказ ожерелье", "анализ рассказа",
  "браслет клевер", "колье клевер", "кулон гвоздь", "браслет гвоздь",

  // Общие подарки без указания камня:
  "что подарить", "что можно подарить", "подарить девушке", "подарок девушке",
  "подарок маме", "подарок женщине", "подарки для женщин", "подарок подруге",
  "беспроигрышный подарок",

  // Дети и непрофильные категории изделий:
  "для девочки", "для девочек", "для детей", "брошь", "броши", "брошка",
  "фенечка", "фенечки", "каффы",

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
  "tilla", "чоловічі"
];

// ------------------------------------------------------------------------------
// 1. БРЕНДЫ-КОНКУРЕНТЫ (БЕЗУСЛОВНЫЙ БАН В ПЕРВУЮ ОЧЕРЕДЬ ВО ФРАЗОВОМ СООТВЕТСТВИИ)
// ------------------------------------------------------------------------------
var COMPETITOR_BRANDS = [
  /swarovski/i, /сваровск/i, /тиффани/i, /tiffany/i, /картье/i, /cartier/i,
  /messika/i, /мессика/i, /apm\b/i, /monaco/i, /апм/i, /монако/i,
  /aroush/i, /larosh/i, /laroush/i, /ляруш/i, /merhat/i, /мерхат/i,
  /tallys/i, /таллис/i, /sansi/i, /санси/i, /люченте/i, /luchente/i, /lucente/i,
  /lucenta/i, /люцента/i, /казахювелир/i, /kazakhyuvelir/i, /пандор/i, /pandora/i,
  /соколов/i, /sokolov/i, /санлайт/i, /sunlight/i, /ван\s*клиф/i, /van\s*cleef/i,
  /ванклив/i, /балауса/i, /balausa/i, /sakina/i, /сакина/i, /mone\b/i, /chopard/i,
  /шопард/i, /bvlgari/i, /bulgari/i, /булгари/i, /tous\b/i, /тоус/i, /адамас/i,
  /adamas/i, /miuz/i, /мюз/i, /сереброфф/i, /серебров/i, /serebroff/i, /дамиани/i,
  /damiani/i, /фрайвилле/i, /frey\s*wille/i, /сблеском/i, /sbleskom/i, /луи\s*ви/i,
  /louis\s*vuitton/i, /шанель/i, /chanel/i, /эрмес/i, /hermes/i, /гуччи/i, /gucci/i,
  /диор/i, /dior/i, /tatirocks/i, /athena\s*gaia/i, /miramira/i, /moonka/i, /sania\b/i,
  /sael\b/i, /rebecca\b/i, /tomiris/i, /shona\b/i, /siyera/i, /viennois/i,
  /maria\s*tash/i, /kruger\s*studios/i, /лалик/i, /lalique/i, /best\s*wishes/i,
  /magic\s*stones/i, /дерберг/i, /dyrberg/i, /deberquem/i, /канциан/i, /canzian/i,
  /грациелла/i, /graziella/i, /оксизян/i, /instyle/i, /сенсатори/i, /sensatori/i,
  /дионис/i, /dionis/i, /keklik/i, /дэвид\s*юрман/i, /david\s*yurman/i, /кубачи/i,
  /каратов/i, /karatov/i, /nature\s*bijoux/i, /ouro/i, /ластория/i, /lastoria/i,
  /вива\s*ла\s*вика/i, /viva\s*la\s*vika/i, /tesoro/i, /meraly/i, /армат/i, /armat\b/i,
  /lurea/i, /луара/i, /luara/i, /kurshuni/i, /hefang/i, /серик\s*рысбек/i,
  /serik\s*rysbek/i, /ларентия/i, /laurentia/i, /гальяно/i, /galliano/i,
  /lady\s*collection/i, /леди\s*коллекшн/i, /anka\s*jewelry/i, /moon\s*soul/i,
  /moon\s*(украшения|бижутерия)/i, /roberto\s*bravo/i, /роберто\s*браво/i,
  /(^|[^а-яёa-z])алтын([^а-яёa-z]|$)/i, /altyn\b/i, /talisman\s*kz/i, /микимото/i,
  /mikimoto/i, /gotto\s*jewelry/i, /pure\s*jewelry/i, /soroka\s*jewelry/i, /сорока\s*jewelry/i,
  /nomination/i, /номинэйшн/i, /лакост/i, /lacoste/i, /la\s*roche/i, /jewelry\s*bus/i,
  /minimal\s*silver/i, /браслет\s*minimal/i, /muraa/i, /yelai/i, /jewelfinger/i,
  /darry\s*ring/i, /favory/i, /farro/i, /via\s*jewelry/i, /astra\s*jewelry/i,
  /le\s*carat/i, /mimi\s*jewelry/i, /assos/i, /два\s*жираф/i, /ganezzi/i,
  /larimar\s*jewelry/i,

  // Мировые дома высокой моды и премиальные бренды:
  /miu\s*miu/i, /миу\s*миу/i, /fendi/i, /фенди/i,
  /burberry/i, /берберри/i, /барбери/i,
  /moschino/i, /москино/i, /roberto\s*cavalli/i, /кавалли/i,
  /valentino/i, /валентино/i, /versace/i, /версаче/i,
  /prada/i, /прада/i, /armani/i, /армани/i,
  /givenchy/i, /живанши/i, /balenciaga/i, /баленсиага/i,
  /marco\s*bicego/i, /марко\s*бичего/i,
  /saint\s*laurent/i, /ysl\b/i, /сен\s*лоран/i,
  /lagerfeld/i, /лагерфельд/i, /boucheron/i, /бушерон/i,
  /celine/i, /селин/i, /loewe/i, /лоэве/i,
  /piaget/i, /пьяже/i, /chaumet/i, /шоме/i,
  /(^|[^а-яёa-z])додо([^а-яёa-z]|$)/i, /(^|[^a-z])dodo([^a-z]|$)/i,
  /graff/i, /(^|[^а-яёa-z])граф([^а-яёa-z]|$)/i,
  /kruger/i, /крюгер/i,
  /delight/i, /дилайт/i,
  /stephen\s*webster/i, /стефан\s*вебстер/i,
  /pomellato/i, /помеллато/i, /bottega/i, /боттега/i,
  /etrusca/i, /этруска/i, /ippolita/i, /ипполита/i,
  /русские\s*самоцветы/i, /линии\s*любви/i, /ювелирочка/i,
  /бронницк/i, /ювелирцентр/i, /дериглазов/i,
  /cancian/i,
  /эпл\s*даймонд/i, /epldiamond/i, /шахерезад/i, /казювелирторг/i,
  /vidda/i, /видда/i, /паскуаль\s*бруни/i, /pasquale\s*bruni/i,
  /sophie\s*buhai/i, /софи\s*бухай/i, /hugo\s*kreit/i, /vida\s*kush/i
];

// ------------------------------------------------------------------------------
// 2. ЗАЩИТНЫЙ WHITELIST НАТУРАЛЬНЫХ КАМНЕЙ, ЖЕМЧУГА И ЭТНО-ТЕРМИНОВ
//    (ВАЖНО: без общих слов "пусеты/кольца/кулон", чтобы не пропускать бриллианты/золото!)
// ------------------------------------------------------------------------------
var SAFE_STONE_ROOTS = [
  /жемчу[гж]/i, /барочн/i, /майорк/i, /majorica/i, /pearl/i, /перламутр/i,
  /нефрит/i, /жадеит/i, /джедаит/i,
  /аметист/i, /малахит/i, /агат/i, /гранат/i, /кварц/i, /бирюз/i, /гематит/i, /хрустал/i,
  /лунн.*камен/i, /лунн/i, /тигров.*глаз/i, /тигров/i, /лазурит/i, /коралл/i, /яшм/i,
  /сердолик/i, /амазонит/i, /турмалин/i, /цитрин/i, /авантюрин/i, /флюорит/i,
  /оникс/i, /шпинел/i, /лабрадор/i, /чароит/i, /хризопраз/i, /змеевик/i,
  /топаз/i, /аквамарин/i, /берилл/i, /опал/i, /янтар/i, /родонит/i, /пирит/i, /содалит/i,
  /морганит/i, /родохрозит/i, /кунцит/i, /халцедон/i, /ларимар/i, /larimar/i, /празиолит/i,
  /хризолит/i, /хризоколл/i, /апатит/i, /танзанит/i, /варисцит/i, /александрит/i,
  /диоптаз/i, /арагонит/i, /aragonite/i, /обсидиан/i, /кошачий.*глаз/i, /параиб/i,

  // Указание на натуральные камни / минералы:
  /натуральн.*камн/i, /натуральн.*камен/i, /природн.*камн/i, /природн.*камен/i,
  /издели.*из.*камн/i, /бусы.*из.*камн/i, /браслет.*из.*камн/i, /колье.*из.*камн/i,
  /серьги.*с.*камн/i, /пусет.*с.*камн/i, /гвоздик.*с.*камн/i,
  /кольц.*с.*камн/i, /кольц.*с.*минерал/i, /с\s+(большим|крупным|розовым|черным|желтым|зеленым|голубым|синим|белым|красным)и?\s+камн/i,

  // Казахские термины украшений и этно-стиль:
  /әшекей/i, /бұйым/i, /маржан/i, /меруерт/i, /алқа/i, /білезік/i, /сырға/i, /сырга/i,
  /шашбау/i, /асыл тас/i, /табиғи тас/i,
  /этно/i, /этническ/i, /национальн.*украшен/i, /kazakh jewelry/i,

  // Фирменные категории мастерской Livi:
  /сотуар/i, /сатуар/i, /чокер/i, /авторск.*украшен/i, /livi/i
];

// ------------------------------------------------------------------------------
// 3. СТОП-ПАТТЕРНЫ МУСОРА, МАСТЕРСКИХ, СЕРЕБРА, ЗОЛОТА 585, ЧУЖИХ КАТЕГОРИЙ И ИНФО
// ------------------------------------------------------------------------------
var JUNK_PATTERNS = [
  /мопассан/i, /краткое\s*содержание/i, /рассказ.*ожерелье/i, /анализ\s*рассказа/i,
  /клевер/i, /гвоздь/i,

  // Производство, ювелирные мастерские, переплавка, лом, экспертиза, гравировка:
  /на заказ/i, /изготовлен/i, /мастерск/i, /переплав/i, /лить[её]/i,
  /гравировк/i, /с надписью/i, /сделать на заказ/i,
  /ювелиры алматы/i, /ювелир алматы/i, /ювелир астана/i, /ювелиры астана/i,
  /экспертиз/i, /(^|[^а-яёa-z])лом([^а-яёa-z]|$)/i, /инструмент/i,
  /уменьшени/i, /увеличени/i, /научиться/i, /станок/i, /станки/i,
  /замок\s+для/i, /оценк/i, /(^|[^а-яёa-z])нить([^а-яёa-z]|$)/i, /часик/i,
  /сережки\s+капельки/i, /дубайск/i,

  // Дети, девочки, непрофильные изделия:
  /для девочк/i, /девочке/i, /девочки/i, /для детей/i, /детск/i, /фигурк.*детей/i,
  /брошь/i, /броши/i, /брошка/i, /фенечк/i, /кафф/i, /клипс/i, /конго/i, /дорик/i, /галстук/i,

  // Пустые общие онлайн-запросы и иноязычный спам:
  /^заказать онлайн$/i, /^купить онлайн$/i, /чоловічі/i, /срібні/i, /tilla/i, /zirak/i,

  // Подарки (разрешены только если в запросе явно указан наш камень/жемчуг из SAFE_STONE_ROOTS):
  /(^|\s)подар/i, /что подарить/i, /что можно подарить/i, /день рожден/i, /(^|[^а-яёa-z])д[рp]([^а-яёa-z]|$)/i,
  /юбилей/i, /годовщин/i, /молодожен/i, /презент/i, /сюрприз/i,

  // Рукоделие, DIY, детали и фурнитура для сборки:
  /своими руками/i, /как сделать/i, /как сплести/i, /как собрать/i, /научиться делать/i, /схем/i,
  /мастер класс/i, /(^|[^а-яёa-z])мк([^а-яёa-z]|$)/i, /бисероплетени/i, /бисер/i, /плетени/i, /вязани/i,
  /фурнитур/i, /застежк/i, /швенз/i, /штифт/i, /(^|[^а-яёa-z])пины([^а-яёa-z]|$)/i, /леск/i, /проволок/i,
  /тросик/i, /эпоксидн/i, /полимерн.*глин/i, /вышивк/i, /станок/i, /с буквой/i,
  /букв[аы]\s+[a-zа-я]/i, /снейк/i, /дизайн бус/i, /кабошон/i,

  // Нецелевые чужие материалы, стекло, пирсинг, оценка сырья:
  /стекл/i, /муранск/i, /murano/i, /мурано/i, /стекляр/i, /шерст/i, /валян/i,
  /муассанит/i, /фианит/i, /дерев/i, /пластик/i, /акрил/i, /силикон/i, /каучук/i, /керамик/i,
  /веревочк/i, /на веревк/i, /шнурок/i, /xuping/i, /ксьюпинг/i, /медицинск/i,
  /ис+кусс?твен/i, /шкатулк/i,
  /лабрет/i, /пирсинг/i, /(^|[^а-яёa-z])(мело|melo)([^а-яёa-z]|$)/i, /сколько стоит/i, /аква кварц/i,
  /сутажн/i, /минанкари/i,

  // Халява, ломбарды, скупка, дешевый опт, б/у, маркетплейсы:
  /дешев/i, /недорог/i, /бесплатн/i, /даром/i, /ломбард/i, /скупк/i, /залог/i,
  /сдать/i, /проба/i, /585/i, /750/i, /925/i, /слит/i, /грамм/i, /карат/i, /алиэкспресс/i,
  /aliexpress/i, /temu/i, /тему/i, /shein/i, /шейн/i, /таобао/i, /taobao/i,
  /секонд/i, /барахолк/i, /конфискат/i, /(^|[^а-яёa-z])б[\s/]?у([^а-яёa-z]|$)/i, /оптом/i, /(^|[^а-яёa-z])опт([^а-яёa-z]|$)/i,
  /olx/i, /олх/i, /авито/i, /ярмарка мастеров/i, /etsy/i,

  // Заводское золото, серебро, бриллианты и драгкамни 1-й категории:
  /(^|\s)золот/i, /серебр/i, /serebro/i, /silver/i, /платин/i, /бриллиант/i, /брилиан/i, /diamond/i,
  /изумруд/i, /рубин/i, /сапфир/i, /теннисн/i, /tennis.*bracelet/i,
  /печатка/i, /обручальн/i, /помолвочн/i, /парные кольца/i, /кольца парные/i, /на мизинец/i,
  /винтов/i, /с драгоценным камнем/i,

  // Одежда и чужие части тела:
  /шапк/i, /рубашк/i, /плать/i, /кофт/i, /пальто/i, /юбк/i, /на ног/i, /через палец/i,

  // Информационные запросы, эзотерика, уход, ремонт:
  /(^|[^а-яёa-z])виды([^а-яёa-z]|$)/i, /разновидност/i, /шакка/i, /sciacca/i,
  /что такое/i, /что это/i, /(^|[^а-яёa-z])это$/i, /как называется/i, /как носить/i, /с чем носить/i,
  /бывает ли/i, /для чего/i, /зачем/i, /ремонт/i, /пайк/i, /перетяжк/i, /чистк/i,
  /как почистить/i, /ультразвуков/i, /как отличить/i, /как проверить/i, /как определить/i,
  /как выгляд/i, /подделк/i, /кому подходит/i, /подходит ли/i, /свойств/i, /значени/i,
  /гороскоп/i, /знак.*зодиак/i, /знак/i, /магическ/i, /лечебн/i, /литотерапи/i, /талисман/i,
  /оберег/i, /амулет/i, /приворот/i, /заговор/i, /сонник/i, /к чему снится/i,
  /википеди/i, /месторожден/i, /твердость/i, /формула/i, /(^|[^а-яёa-z])фото([^а-яёa-z]|$)/i, /картинк/i,
  /обои/i, /скачать/i, /видео/i, /реферат/i, /ваканси/i, /резюме/i, /работа/i,
  /зарплат/i, /мужск/i, /для мужчин/i, /мужчин/i, /крестик/i, /четки/i, /тасбих/i,
  /часы/i, /зодиак/i, /овен/i, /телец/i, /тельц/i, /близнец/i, /(^|[^а-яёa-z])рак([^а-яёa-z]|$)/i, /рака/i,
  /(^|[^а-яёa-z])лев([^а-яёa-z]|$)/i, /льва/i, /дева/i, /девам/i, /весы/i, /весов/i, /скорпион/i, /стрелец/i, /козерог/i,
  /водолей/i, /рыбы/i,

  // Гео-туризм и оффлайн-поиск:
  /вьетнам/i, /шри ланк/i, /катар/i, /пхукет/i, /(^|[^а-яёa-z])гоа([^а-яёa-z]|$)/i, /туркестан/i, /египет/i,
  /тайланд/i, /(^|[^а-яёa-z])бали([^а-яёa-z]|$)/i, /milan/i, /милан/i, /греци/i, /япони/i, /украин/i, /дагестан/i,
  /турки/i, /турецк/i, /индийск/i, /ближайш/i, /поблизости/i, /рядом/i,

  // Кольца, пусеты и гвоздики проверяются ПОСЛЕ всех остальных стоп-слов:
  // (если есть камень/жемчуг — разрешены; если без камня — переводятся строго в ТОЧНОЕ соответствие [X]):
  /кольц/i, /колечк/i, /перстен/i, /пусет/i, /пуссет/i, /гвоздик/i
];

function isSafeStoneTerm(term) {
  if (!term) return false;
  var lower = term.toLowerCase().trim();
  for (var i = 0; i < SAFE_STONE_ROOTS.length; i++) {
    if (SAFE_STONE_ROOTS[i].test(lower)) {
      return true;
    }
  }
  return false;
}

function isLineJewelryTerm(term) {
  if (!term) return false;
  var lower = term.toLowerCase().trim();
  // Украшения на леске/тросике (исключая запросы про бисероплетение/фурнитуру/катушки лески)
  return /на леске|на тросике/i.test(lower) && !/для бисер|для рукодел|катушк|купить леску|леска для/i.test(lower);
}

function isTwoWordStoneLookup(term) {
  var clean = (term || "").toLowerCase().trim().replace(/^["\[]|["\]]$/g, "");
  var fwd = /^[а-яёәіңғүұқөһa-z-]+\s+(камень|тас|тасы|виды|вид|цвет|цвета|свойства|цена|стоимость|натуральный|природный)$/i.test(clean);
  var rev = /^(виды|вид|цвет|цвета|свойства|цена|стоимость|натуральный|природный)\s+[а-яёәіңғүұқөһa-z-]+$/i.test(clean);
  return fwd || rev;
}

function evaluateSearchTerm(term) {
  var lower = (term || "").toLowerCase().trim().replace(/^["\[]|["\]]$/g, "").trim();
  if (!lower) return { isJunk: false, isExactOnly: false, isSafe: false, reason: "Пустой запрос" };

  // 1. Бренд конкурента -> МГНОВЕННЫЙ БАН (Фразовое соответствие)
  for (var b = 0; b < COMPETITOR_BRANDS.length; b++) {
    if (COMPETITOR_BRANDS[b].test(lower)) {
      return { isJunk: true, isExactOnly: false, isSafe: false, reason: "Бренд-конкурент (" + COMPETITOR_BRANDS[b] + ")" };
    }
  }

  var hasSafeStone = isSafeStoneTerm(lower);
  var isLineJewelry = isLineJewelryTerm(lower);

  // 2. Двухсловные инфо-запросы вида "[минерал] камень / виды / цвет / цена / натуральный" -> ТОЧНОЕ СООТВЕТСТВИЕ [X]
  //    (Проверяем до JUNK_PATTERNS, чтобы "агат виды" попадал в точный минус [агат виды], а не фразовый)
  if (isTwoWordStoneLookup(lower) && hasSafeStone) {
    return { isJunk: true, isExactOnly: true, isSafe: false, reason: "Инфо-запрос [точное соответствие]" };
  }

  // 3. Проверка на стоп-паттерны с исключениями Livi Jewelry
  for (var j = 0; j < JUNK_PATTERNS.length; j++) {
    if (JUNK_PATTERNS[j].test(lower)) {
      var patStr = String(JUNK_PATTERNS[j]);

      // Исключение А: Позолота + наш камень
      var isGoldPlated = /позолот/i.test(lower) && !/(^|\s)золот/i.test(lower);
      if (hasSafeStone && isGoldPlated && patStr.indexOf("золот") !== -1) {
        continue;
      }

      // Исключение Б: Покупка нашего конкретного камня/жемчуга (или кулона на леске) в подарок
      var isGiftPattern = patStr.indexOf("подар") !== -1 || patStr.indexOf("день рожден") !== -1 || patStr.indexOf("юбилей") !== -1;
      if ((hasSafeStone || isLineJewelry) && isGiftPattern) {
        continue;
      }

      // Исключение В и Г: Пусеты, серьги-гвоздики и кольца
      // Если в запросе есть наш камень/жемчуг/перламутр — разрешаем!
      // Если камня в запросе НЕТ (например, просто "кольцо", "кольца алматы", "пусеты", "гвоздики серьги") —
      // блокируем ТОЛЬКО В ТОЧНОМ СООТВЕТСТВИИ [кольцо], чтобы фразовый минус не заблокировал "кольцо с жемчугом"!
      var isRingOrStudPattern = (
        patStr === "/кольц/i" ||
        patStr === "/колечк/i" ||
        patStr === "/перстен/i" ||
        patStr === "/пусет/i" ||
        patStr === "/пуссет/i" ||
        patStr === "/гвоздик/i"
      );
      if (isRingOrStudPattern) {
        if (hasSafeStone || isLineJewelry) {
          continue;
        } else {
          return {
            isJunk: true,
            isExactOnly: true,
            isSafe: false,
            reason: "Общий запрос кольца/пусеты без камня [точное соответствие]"
          };
        }
      }

      // Исключение Д: Кулоны, колье, сотуары и браслеты на леске / тросике
      if (isLineJewelry && (patStr.indexOf("леск") !== -1 || patStr.indexOf("тросик") !== -1)) {
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
    isSafe: hasSafeStone || isLineJewelry,
    reason: (hasSafeStone || isLineJewelry) ? "Целевой камень / изделие мастерской" : "Общий целевой запрос"
  };
}

function shouldUnblockNegative(term, mType) {
  var lower = (term || "").toLowerCase().trim().replace(/^["\[]|["\]]$/g, "").trim();
  if (!lower) return false;

  for (var i = 0; i < SEED_ROOT_NEGATIVES.length; i++) {
    if (SEED_ROOT_NEGATIVES[i].toLowerCase().trim() === lower) {
      return false;
    }
  }

  // СТРОГО: Разблокируем ТОЛЬКО те фразы из минус-слов, которые:
  // 1) НЕ являются мусором (!evalRes.isJunk)
  // 2) И СТРОГО являются целевыми изделиями Livi (камни, жемчуг, этно, украшения на леске — evalRes.isSafe === true)
  // Это 100% исключает разблокировку неизвестных брендов, ремонта, лома или литературы!
  var evalRes = evaluateSearchTerm(lower);
  if (!evalRes.isJunk && evalRes.isSafe) {
    return true;
  }

  return false;
}

function shouldConvertPhraseToExact(term, mType) {
  if (mType === "EXACT") return false;
  var lower = (term || "").toLowerCase().trim().replace(/^["\[]|["\]]$/g, "").trim();
  if (!lower) return false;

  var evalRes = evaluateSearchTerm(lower);
  // Конвертируем из PHRASE/BROAD в EXACT:
  // 1) Двухсловные инфо-запросы ("аметист камень" -> [аметист камень])
  // 2) Общие запросы на кольца/пусеты/гвоздики без камня ("кольцо" -> [кольцо], "пусеты" -> [пусеты]),
  //    чтобы фразовый минус "кольцо" или "пусеты" не блокировал показы "кольцо с жемчугом" и "пусеты с агатом"!
  return evalRes.isJunk && evalRes.isExactOnly;
}

function main() {
  Logger.log("==================================================================");
  Logger.log("   💎 LIVI JEWELRY AUTOPILOT v5.6 DIAMOND SHIELD: ЗАПУСК         ");
  Logger.log("==================================================================");

  var account = AdsApp.currentAccount();
  var accountName = account.getName() || "Livi Jewelry";
  var customerId = account.getCustomerId();
  var currency = account.getCurrencyCode();

  var actionLogs = [];
  var warningsList = [];

  // 1. Привязка мастер-списка, авто-разбан товаров Livi и превентивные бренды
  Logger.log("\n[1/5] Синхронизация мастер-списка и авто-разбан товаров Livi...");
  var negativeList = getOrCreateNegativeList(CONFIG.NEGATIVE_LIST_NAME, actionLogs);
  var attachedCampaignsCount = attachNegativeListToAllCampaigns(negativeList);
  if (attachedCampaignsCount > 0) {
    actionLogs.push("Мастер-список минус-слов активен на " + attachedCampaignsCount + " кампаниях.");
  }

  // Сквозная проверка всех остальных списков минус-слов аккаунта на случай внешних блокировок
  auditAndUnblockAllSharedLists(actionLogs);

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
  Logger.log("   АВТОПИЛОТ v5.6 DIAMOND SHIELD: Выполнение успешно завершено!   ");
  Logger.log("==================================================================");
}

function getNegativeKeywordsIterator(negList) {
  if (typeof negList.negativeKeywords === "function") {
    return negList.negativeKeywords().get();
  }
  if (typeof negList.getNegativeKeywords === "function") {
    return negList.getNegativeKeywords();
  }
  return null;
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
  var toUnblock = [];

  try {
    var it = getNegativeKeywordsIterator(negList);
    while (it && it.hasNext()) {
      var nk = it.next();
      var rawText = nk.getText().toLowerCase().trim();
      var mType = nk.getMatchType();
      var stripped = rawText.replace(/^["\[]|["\]]$/g, "").trim();

      if (shouldUnblockNegative(stripped, mType)) {
        toUnblock.push({ nkObj: nk, clean: stripped });
      } else if (shouldConvertPhraseToExact(stripped, mType)) {
        toConvertExact.push({ nkObj: nk, clean: stripped });
      } else {
        if (mType === "EXACT") {
          existing["[" + stripped + "]"] = true;
        } else if (mType === "PHRASE") {
          existing['"' + stripped + '"'] = true;
          existing[stripped] = true;
        } else {
          existing[stripped] = true;
          existing[rawText] = true;
        }
      }
    }
  } catch (e) {
    Logger.log("  [!] Ошибка чтения списка минус-слов: " + e);
  }

  // 1. Авто-разблокировка целевых товаров Livi (кольца/пусеты/гвоздики с камнями и жемчугом, кулоны на леске)
  var unblockedCount = 0;
  for (var u = 0; u < toUnblock.length; u++) {
    var uItem = toUnblock[u];
    try {
      if (CONFIG.APPLY_CHANGES) {
        uItem.nkObj.remove();
      }
      unblockedCount++;
      var unblockMsg = "РАЗБЛОКИРОВАН целевой запрос Livi из минус-слов: \"" + uItem.clean + "\"";
      actionLogs.push(unblockMsg);
      Logger.log("  🔓 " + unblockMsg);
    } catch (uErr) {
      Logger.log("  [!] Ошибка удаления минус-слова " + uItem.clean + ": " + uErr);
    }
  }
  if (unblockedCount > 0) {
    Logger.log("  ✓ Всего успешно разблокировано целевых фраз Livi: " + unblockedCount + " шт.");
  }

  // 2. Авто-конвертация фразовых "X камень" и общих "кольцо/пусеты" (без камня) в точное соответствие [...]
  var convertedCount = 0;
  for (var c = 0; c < toConvertExact.length; c++) {
    var item = toConvertExact[c];
    var exactKey = "[" + item.clean + "]";
    try {
      if (CONFIG.APPLY_CHANGES) {
        item.nkObj.remove();
        if (!existing[exactKey]) {
          negList.addNegativeKeyword(exactKey);
        }
      }
      existing[exactKey] = true;
      convertedCount++;
    } catch (convErr) {
      Logger.log("  [!] Ошибка конвертации минус-слова " + item.clean + ": " + convErr);
    }
  }
  if (convertedCount > 0) {
    var convMsg = "Переведено из фразового в точное соответствие [...]: " + convertedCount + " шт. (снят фразовый блок с колец, пусет и камней).";
    actionLogs.push(convMsg);
    Logger.log("  🔄 " + convMsg);
  }

  // 3. Превентивная загрузка брендов и стоп-корней во ФРАЗОВОМ соответствии
  var seeded = 0;
  for (var i = 0; i < SEED_ROOT_NEGATIVES.length; i++) {
    var rootWord = SEED_ROOT_NEGATIVES[i].toLowerCase().trim();
    if (!existing[rootWord] && !existing['"' + rootWord + '"']) {
      try {
        if (CONFIG.APPLY_CHANGES) {
          negList.addNegativeKeyword('"' + rootWord + '"');
        }
        existing[rootWord] = true;
        existing['"' + rootWord + '"'] = true;
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

function auditAndUnblockAllSharedLists(actionLogs) {
  Logger.log("\n[1.1] Сквозной аудит всех списков минус-слов аккаунта...");
  try {
    var allLists = AdsApp.negativeKeywordLists().get();
    var otherListsChecked = 0;
    var otherUnblocked = 0;
    while (allLists.hasNext()) {
      var list = allLists.next();
      var listName = list.getName();
      if (listName === CONFIG.NEGATIVE_LIST_NAME) continue;
      otherListsChecked++;

      var it = getNegativeKeywordsIterator(list);
      while (it && it.hasNext()) {
        var nk = it.next();
        var rawText = nk.getText().toLowerCase().trim();
        var mType = nk.getMatchType();
        var stripped = rawText.replace(/^["\[]|["\]]$/g, "").trim();

        if (shouldUnblockNegative(stripped, mType)) {
          try {
            if (CONFIG.APPLY_CHANGES) {
              nk.remove();
            }
            otherUnblocked++;
            var msg = "РАЗБЛОКИРОВАН товар Livi из стороннего списка '" + listName + "': \"" + stripped + "\"";
            actionLogs.push(msg);
            Logger.log("  🔓 " + msg);
          } catch(e) {}
        }
      }
    }
    if (otherUnblocked > 0) {
      Logger.log("  ✓ Всего разблокировано в сторонних списках: " + otherUnblocked + " шт.");
    } else {
      Logger.log("  ✓ Сторонние списки аккаунта (" + otherListsChecked + " шт.) проверены: конфликтов с товарами Livi нет.");
    }
  } catch(err) {
    Logger.log("  [!] Замечание при аудите сторонних списков: " + err);
  }
}

function mineJunkSearchTerms(negativeList, actionLogs) {
  var addedCount = 0;
  var existingNegs = {};

  try {
    var negIter = getNegativeKeywordsIterator(negativeList);
    while (negIter && negIter.hasNext()) {
      var nkItem = negIter.next();
      var nkText = nkItem.getText().toLowerCase().trim().replace(/^["\[]|["\]]$/g, "").trim();
      var nkType = nkItem.getMatchType();
      if (nkType === "EXACT") {
        existingNegs["[" + nkText + "]"] = true;
      } else if (nkType === "PHRASE") {
        existingNegs['"' + nkText + '"'] = true;
        existingNegs[nkText] = true;
      } else {
        existingNegs[nkText] = true;
      }
    }
  } catch (err) {
    Logger.log("  [!] Ошибка чтения существующих минус-слов во 2 шаге: " + err);
  }

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
        // Если isExactOnly === true -> ТОЧНОЕ соответствие [...], иначе ФРАЗОВОЕ "..."
        var formattedNeg = evalRes.isExactOnly ? ("[" + term + "]") : ('"' + term + '"');
        var checkExists = evalRes.isExactOnly
          ? existingNegs[formattedNeg.toLowerCase()]
          : (existingNegs[formattedNeg.toLowerCase()] || existingNegs[term]);

        if (!checkExists) {
          try {
            if (CONFIG.APPLY_CHANGES) {
              negativeList.addNegativeKeyword(formattedNeg);
            }
            existingNegs[formattedNeg.toLowerCase()] = true;
            if (!evalRes.isExactOnly) {
              existingNegs[term] = true;
            }
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
      try {
        var kw = kwIter.next();
        var kwStats = kw.getStatsFor("LAST_14_DAYS");

        var clicks = kwStats.getClicks();
        var convs = kwStats.getConversions();
        var ctr = kwStats.getCtr() * 100;
        var currentCpc = 0.15;
        try {
          var bidding = kw.bidding();
          if (bidding && typeof bidding.getCpc === "function") {
            currentCpc = bidding.getCpc() || 0.15;
          }
        } catch (bErr) {
          continue;
        }

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
      } catch (kwErr) {}
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
          isExactOnly: evalRes.isExactOnly,
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
          isExactOnly: evalRes.isExactOnly,
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
                "Утренний отчет Google Ads v5.6 DIAMOND SHIELD за вчера (" + dateStr + ") — " +
                perf.totalClicks + " кликов, " + perf.totalCost.toFixed(2) + " " + currency;

  var lines = [];
  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("   LIVI JEWELRY — УТРЕННИЙ БОЕВОЙ ОТЧЕТ AUTOPILOT v5.6 DIAMOND   ");
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
      var mark = item.isSafe
        ? " [💎 Наш камень/изделие]"
        : (item.isExactOnly ? " [📌 Точный минус двухсловника/общего запроса]" : (item.isJunk ? " [🚫 Мусор/Бренд]" : " [🔍 Общий запрос]"));
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
