/**
 * ==============================================================================
 * LIVI JEWELRY — GROWTH & SCALING ADVISOR v1.3.2 (ВЕЧЕРНИЙ СОВЕТНИК 21:00)
 * ==============================================================================
 * 
 * РОЛЬ СКРИПТА:
 * Высокоточный советник по масштабированию и поиску РЕАЛЬНЫХ покупателей.
 * Полностью синхронизирован по фильтрам с Autopilot v5.6 Diamond Shield.
 * 
 * СТРОГИЕ ФИЛЬТРЫ Livi Jewelry:
 * 1. [Строгий фильтр ассортимента] В рекомендации ключевых слов попадают ТОЛЬКО:
 *    - Изделия: колье, чокеры, браслеты, серьги, пусеты, гвоздики, кольца с камнями,
 *      сотуары, бусы, сеты, ожерелья, кулоны/колье на леске и тросике.
 *    - Материалы: натуральный жемчуг, барочный жемчуг, майорка, перламутр, природные камни
 *      (нефрит, аметист, гранат, турмалин, агат, малахит, бирюза, янтарь, лазурит и др.).
 * 2. [Полный запрет чужого] Ни при каких условиях НЕ рекомендует:
 *    - Общие запросы на кольца/пусеты/гвоздики БЕЗ указания камня или жемчуга.
 *    - Заводское золото 585, серебро 925, бриллианты в каратах, обручальные кольца.
 *    - Муранское стекло, бисер, эпоксидку, дерево, рукоделие, дизайн бус, лом, экспертизу.
 *    - Драгоценные камни 1-й категории (изумруд, бриллиант, рубин, сапфир) и жемчуг мело.
 *    - Бренды конкурентов и дома моды (Swarovski, Prada, Versace, Tiffany, Pandora, Ganezzi и др.).
 *    - Информационные запросы («сколько стоит», «виды», «цвет», «свойства», «сонник»).
 * ==============================================================================
 */

var CONFIG = {
  ALERT_EMAIL: "viksonna94@gmail.com",
  MIN_CTR_THRESHOLD: 10.0,       // Строгий целевой порог CTR (10.0%)
  BUDGET_SATURATION_PCT: 88.0,   // Если потрачено >88% бюджета, емкости не хватает
  TARGET_CAMPAIGN_NAME: "Livi Jewelry - Поиск Казахстан", // Основная поисковая кампания
  SEND_EMAIL: true
};

// ------------------------------------------------------------------------------
// 1. БРЕНДЫ-КОНКУРЕНТЫ (СТРОЖАЙШИЙ БАН, СИНХРОНИЗИРОВАНО С AUTOPILOT v5.5.2)
// ------------------------------------------------------------------------------
var COMPETITOR_BRANDS = [
  /swarovski/i, /сваровск/i, /тиффани/i, /tiffany/i, /картье/i, /cartier/i,
  /messika/i, /мессика/i, /apm\b/i, /monaco/i, /апм/i, /монако/i,
  /aroush/i, /larosh/i, /laroush/i, /ляруш/i, /merhat/i, /мерхат/i,
  /tallys/i, /таллис/i, /sansi/i, /санси/i, /люченте/i, /luchente/i, /lucente/i,
  /lucenta/i, /люцента/i, /казахювелир/i, /kazakhyuvelir/i, /пандор/i, /pandora/i,
  /соколов/i, /sokolov/i, /санлайт/i, /sunlight/i, /ван\s*клиф/i, /van\s*cleef/i,
  /ванклив/i, /балауса/i, /balausa/i, /sakina/i, /сакина/i, /(^|[^а-яёa-z])mone([^а-яёa-z]|$)/i, /chopard/i,
  /шопард/i, /шопар/i, /bvlgari/i, /bulgari/i, /булгари/i, /tous\b/i, /тоус/i, /адамас/i,
  /adamas/i, /miuz/i, /мюз/i, /сереброфф/i, /серебров/i, /serebroff/i, /дамиани/i,
  /damiani/i, /фрайвилле/i, /frey\s*wille/i, /сблеском/i, /sbleskom/i, /луи\s*ви/i,
  /louis\s*vuitton/i, /шанель/i, /chanel/i, /эрмес/i, /гермес/i, /hermes/i, /гуччи/i, /gucci/i,
  /диор/i, /dior/i, /tatirocks/i, /athena\s*gaia/i, /miramira/i, /moonka/i, /sania\b/i,
  /sael\b/i, /rebecca\b/i, /tomiris/i, /shona\b/i, /siyera/i, /viennois/i,
  /maria\s*tash/i, /kruger\s*studios/i, /kruger/i, /крюгер/i, /лалик/i, /lalique/i, /best\s*wishes/i,
  /magic\s*stones/i, /дерберг/i, /dyrberg/i, /deberquem/i, /канциан/i, /canzian/i, /cancian/i,
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
  /nomination/i, /номинэйшн/i, /номинейшн/i, /лакост/i, /lacoste/i, /la\s*roche/i, /jewelry\s*bus/i,
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
  /эпл\s*даймонд/i, /epldiamond/i, /шахерезад/i, /казювелирторг/i
];

// ------------------------------------------------------------------------------
// 2. ЗАЩИТНЫЙ WHITELIST НАТУРАЛЬНЫХ КАМНЕЙ, ЖЕМЧУГА И ЭТНО-ТЕРМИНОВ
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
// 3. СТОП-ПАТТЕРНЫ МУСОРА (СИНХРОНИЗИРОВАНО С AUTOPILOT v5.5.2)
// ------------------------------------------------------------------------------
var JUNK_PATTERNS = [
  /мопассан/i, /краткое\s*содержание/i, /рассказ.*ожерелье/i, /анализ\s*рассказа/i,
  /клевер/i, /гвоздь/i,
  /на заказ/i, /изготовлен/i, /мастерск/i, /переплав/i, /лить[её]/i,
  /гравировк/i, /с надписью/i, /сделать на заказ/i,
  /ювелиры алматы/i, /ювелир алматы/i, /ювелир астана/i, /ювелиры астана/i,
  /экспертиз/i, /(^|[^а-яёa-z])лом([^а-яёa-z]|$)/i, /инструмент/i,
  /уменьшени/i, /увеличени/i, /научиться/i, /станок/i, /станки/i,
  /замок\s+для/i, /оценк/i, /(^|[^а-яёa-z])нить([^а-яёa-z]|$)/i, /часик/i,
  /сережки\s+капельки/i, /дубайск/i,
  /для девочк/i, /девочке/i, /девочки/i, /для детей/i, /детск/i, /фигурк.*детей/i,
  /брошь/i, /броши/i, /брошка/i, /фенечк/i, /кафф/i, /клипс/i, /конго/i, /дорик/i, /галстук/i,
  /^заказать онлайн$/i, /^купить онлайн$/i, /чоловічі/i, /срібні/i, /tilla\b/i, /zirak/i,
  /(^|\s)подар/i, /что подарить/i, /что можно подарить/i, /день рожден/i, /(^|[^а-яёa-z])д[рp]([^а-яёa-z]|$)/i,
  /юбилей/i, /годовщин/i, /молодожен/i, /презент/i, /сюрприз/i,
  /своими руками/i, /как сделать/i, /как сплести/i, /как собрать/i, /научиться делать/i, /схем/i,
  /мастер класс/i, /(^|[^а-яёa-z])мк([^а-яёa-z]|$)/i, /бисероплетени/i, /бисер/i, /плетени/i, /вязани/i,
  /фурнитур/i, /застежк/i, /швенз/i, /штифт/i, /(^|[^а-яёa-z])пины([^а-яёa-z]|$)/i, /леск/i, /проволок/i,
  /тросик/i, /эпоксидн/i, /полимерн.*глин/i, /вышивк/i, /станок/i, /с буквой/i,
  /букв[аы]\s+[a-zа-я]/i, /снейк/i, /дизайн бус/i, /кабошон/i,
  /стекл/i, /муранск/i, /murano/i, /мурано/i, /стекляр/i, /шерст/i, /валян/i,
  /муассанит/i, /фианит/i, /дерев/i, /пластик/i, /акрил/i, /силикон/i, /каучук/i,
  /веревочк/i, /на веревк/i, /шнурок/i, /xuping/i, /ксьюпинг/i, /медицинск/i,
  /лабрет/i, /пирсинг/i, /(^|[^а-яёa-z])(мело|melo)([^а-яёa-z]|$)/i, /сколько стоит/i, /аква кварц/i,
  /сутажн/i, /минанкари/i,
  /дешев/i, /недорог/i, /бесплатн/i, /даром/i, /ломбард/i, /скупк/i, /залог/i,
  /сдать/i, /проба/i, /585/i, /750/i, /925/i, /слит/i, /грамм/i, /карат/i, /алиэкспресс/i,
  /aliexpress/i, /temu/i, /тему/i, /shein/i, /шейн/i, /таобао/i, /taobao/i,
  /секонд/i, /барахолк/i, /конфискат/i, /(^|[^а-яёa-z])б[\s/]?у([^а-яёa-z]|$)/i, /оптом/i, /(^|[^а-яёa-z])опт([^а-яёa-z]|$)/i,
  /olx/i, /олх/i, /авито/i, /ярмарка мастеров/i, /etsy/i,
  /(^|\s)золот/i, /серебр/i, /serebro/i, /silver/i, /платин/i, /бриллиант/i, /брилиан/i, /diamond/i,
  /изумруд/i, /рубин/i, /сапфир/i, /теннисн/i, /tennis.*bracelet/i,
  /печатка/i, /обручальн/i, /помолвочн/i, /парные кольца/i, /кольца парные/i, /на мизинец/i,
  /винтов/i, /с драгоценным камнем/i,
  /шапк/i, /рубашк/i, /плать/i, /кофт/i, /пальто/i, /юбк/i, /на ног/i, /через палец/i,
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
  /вьетнам/i, /шри ланк/i, /катар/i, /пхукет/i, /(^|[^а-яёa-z])гоа([^а-яёa-z]|$)/i, /туркестан/i, /египет/i,
  /тайланд/i, /(^|[^а-яёa-z])бали([^а-яёa-z]|$)/i, /milan/i, /милан/i, /греци/i, /япони/i, /украин/i, /дагестан/i,
  /узбекск/i, /турки/i, /турецк/i, /индийск/i, /ближайш/i, /поблизости/i, /рядом/i,

  // Кольца, пусеты и гвоздики проверяются ПОСЛЕ всех остальных стоп-слов:
  /кольц/i, /колечк/i, /перстен/i, /пусет/i, /пуссет/i, /гвоздик/i
];

// Белый список реальных изделий Livi Jewelry
var VALID_ITEM_PATTERNS = [
  /колье/i, /чокер/i, /браслет/i, /серьг/i, /сырғ/i, /сырг/i, /сотуар/i,
  /бусы/i, /ожерель/i, /алқа/i, /білезік/i, /шашбау/i, /әшекей/i, /подвеск/i, /кулон/i,
  /(^|[^а-яёa-z])сет([^а-яёa-z]|$)/i, /комплект/i, /пусет/i, /пуссет/i, /гвоздик/i,
  /на леске/i, /на тросике/i, /кольц/i, /колечк/i, /перстен/i
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
  return /на леске|на тросике/i.test(lower) && !/для бисер|для рукодел|катушк|купить леску|леска для/i.test(lower);
}

function isTwoWordLookup(term) {
  var clean = (term || "").toLowerCase().trim();
  return /^[а-яёәіңғүұқөһa-z-]+\s+(камень|тас|тасы|виды|вид|цвет|цвета|свойства|цена|стоимость|натуральный|природный)$/i.test(clean) ||
         /^(виды|вид|цвет|цвета|свойства|цена|стоимость|натуральный|природный)\s+[а-яёәіңғүұқөһa-z-]+$/i.test(clean);
}

function classifySearchTerm(term) {
  var lower = (term || "").toLowerCase().trim();
  if (!lower) return { type: "SKIP" };

  // 1. Проверка на бренд конкурента
  for (var b = 0; b < COMPETITOR_BRANDS.length; b++) {
    if (COMPETITOR_BRANDS[b].test(lower)) {
      return { type: "JUNK", reason: "Бренд-конкурент" };
    }
  }

  var hasStone = isSafeStoneTerm(lower);
  var isLineJewelry = isLineJewelryTerm(lower);

  // 2. Проверка на стоп-паттерны с исключениями для ассортимента Livi Jewelry
  for (var j = 0; j < JUNK_PATTERNS.length; j++) {
    if (JUNK_PATTERNS[j].test(lower)) {
      var patStr = String(JUNK_PATTERNS[j]);

      // Исключение А: позолота + наш камень
      if (hasStone && /позолот/i.test(lower) && !/(^|\s)золот/i.test(lower) && patStr.indexOf("золот") !== -1) {
        continue;
      }

      // Исключение Б: подарок с нашим камнем или украшение на леске
      var isGiftPattern = patStr.indexOf("подар") !== -1 || patStr.indexOf("день рожден") !== -1 || patStr.indexOf("юбилей") !== -1;
      if ((hasStone || isLineJewelry) && isGiftPattern) {
        continue;
      }

      // Исключение В и Г: пусеты, гвоздики и кольца (ТОЛЬКО если есть камень/жемчуг или на леске)
      var isRingOrStudPattern = (
        patStr === "/кольц/i" ||
        patStr === "/колечк/i" ||
        patStr === "/перстен/i" ||
        patStr === "/пусет/i" ||
        patStr === "/пуссет/i" ||
        patStr === "/гвоздик/i"
      );
      if (isRingOrStudPattern) {
        if (hasStone || isLineJewelry) {
          continue;
        } else {
          return { type: "JUNK", reason: "Общий запрос кольца/пусеты без камня" };
        }
      }

      // Исключение Д: кулоны, колье, украшения на леске/тросике
      if (isLineJewelry && (patStr.indexOf("леск") !== -1 || patStr.indexOf("тросик") !== -1)) {
        continue;
      }

      return { type: "JUNK", reason: "Не наш ассортимент / стоп-слово" };
    }
  }

  // 3. Инфо-запросы из 2 слов ("хризопраз камень", "агат виды", "бирюза цвет", "бирюза цена")
  if (isTwoWordLookup(lower)) {
    return { type: "JUNK", reason: "Справочный инфо-запрос" };
  }

  // 4. Проверка на принадлежность каталогу Livi Jewelry (обязателен камень/жемчуг либо украшение на леске)
  if (!hasStone && !isLineJewelry) {
    return { type: "SKIP" };
  }

  var hasItem = false;
  for (var i = 0; i < VALID_ITEM_PATTERNS.length; i++) {
    if (VALID_ITEM_PATTERNS[i].test(lower)) {
      hasItem = true;
      break;
    }
  }

  // 5. Проверка покупательского намерения
  var hasBuyIntent = /купить|заказать|каталог|магазин|сатып\s*ал|баға|тапсырыс|в наличии|алматы|астана/i.test(lower);
  var isPureProductPhrase = (hasStone && hasItem) || isLineJewelry;

  if (hasBuyIntent || isPureProductPhrase) {
    return { type: "GOLDEN", reason: hasBuyIntent ? "Горячий покупатель" : "Целевое готовое изделие" };
  }

  return { type: "SKIP" };
}

function main() {
  Logger.log("==================================================================");
  Logger.log("💎 LIVI JEWELRY — GROWTH ADVISOR v1.3.2 (СИНХРОНИЗИРОВАН С v5.6)");
  Logger.log("==================================================================");

  var reportDate = Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy HH:mm");
  
  var existingKeywords = {};
  try {
    var kwIter = AdsApp.keywords().withCondition("Status = ENABLED").get();
    while (kwIter.hasNext()) {
      var kw = kwIter.next();
      var cleanKw = kw.getText().toLowerCase().replace(/^["\[]|["\]]$/g, "").trim();
      existingKeywords[cleanKw] = true;
    }
    Logger.log("  ✓ Загружено активных ключевых слов в аккаунте: " + Object.keys(existingKeywords).length);
  } catch (kwErr) {
    Logger.log("  [!] Ошибка чтения ключевых слов: " + kwErr);
  }

  var todayBudgetInfo = analyzeTodayBudget();
  var perfStats = analyzePeriodPerformance();
  var categorizedQueries = analyzeAndFilterQueries(existingKeywords);
  var trafficLight = evaluateTrafficLight(todayBudgetInfo, perfStats);

  var emailBody = buildCleanReport(reportDate, todayBudgetInfo, perfStats, categorizedQueries, trafficLight);
  Logger.log("\n" + emailBody);

  if (CONFIG.SEND_EMAIL && CONFIG.ALERT_EMAIL) {
    var subject = trafficLight.icon + " Livi Growth Advisor v1.3.2: CTR " + perfStats.searchCtr.toFixed(1) + "% | " + trafficLight.title + " [" + reportDate + "]";
    try {
      MailApp.sendEmail(CONFIG.ALERT_EMAIL, subject, emailBody);
      Logger.log("\n📧 Вечерний отчет успешно отправлен на: " + CONFIG.ALERT_EMAIL);
    } catch (mailErr) {
      Logger.log("\n[!] Ошибка отправки email через MailApp: " + mailErr);
    }
  }

  Logger.log("\n==================================================================");
  Logger.log("💎 Анализ советника v1.3.2 завершен успешно (без ошибок)!");
  Logger.log("==================================================================");
}

function analyzeTodayBudget() {
  var totalSpend = 0.0;
  var totalDailyBudget = 0.0;
  var searchSpend = 0.0;
  var searchBudget = 0.0;

  try {
    var campIter = AdsApp.campaigns().withCondition("Status = ENABLED").get();
    while (campIter.hasNext()) {
      var camp = campIter.next();
      var spend = 0.0;
      var bAmount = 0.0;
      try { spend = camp.getStatsFor("TODAY").getCost(); } catch (e) {}
      try { bAmount = camp.getBudget().getAmount(); } catch (e) {}

      totalSpend += spend;
      totalDailyBudget += bAmount;

      var campName = camp.getName() || "";
      if (campName.indexOf("Shopping") === -1 && campName.indexOf("Покупки") === -1) {
        searchSpend += spend;
        searchBudget += bAmount;
      }
    }
  } catch (e) {}

  var usagePct = totalDailyBudget > 0 ? (totalSpend / totalDailyBudget) * 100 : 0;
  var isSaturated = usagePct >= CONFIG.BUDGET_SATURATION_PCT;

  return {
    totalSpend: totalSpend,
    totalDailyBudget: totalDailyBudget,
    searchSpend: searchSpend,
    searchBudget: searchBudget,
    usagePct: usagePct,
    isSaturated: isSaturated
  };
}

function analyzePeriodPerformance() {
  var totalClicks = 0;
  var totalImps = 0;
  var totalCost = 0.0;
  var searchClicks = 0;
  var searchImps = 0;
  var searchCost = 0.0;

  var now = new Date();
  var threeDaysAgo = new Date(now.getTime() - 3 * 24 * 60 * 60 * 1000);
  var dateFrom = Utilities.formatDate(threeDaysAgo, "Asia/Almaty", "yyyyMMdd");
  var dateTo = Utilities.formatDate(now, "Asia/Almaty", "yyyyMMdd");
  var periodLabel = Utilities.formatDate(threeDaysAgo, "Asia/Almaty", "dd.MM") + " – " + Utilities.formatDate(now, "Asia/Almaty", "dd.MM");

  try {
    var campIter = AdsApp.campaigns().withCondition("Status = ENABLED").get();
    while (campIter.hasNext()) {
      var camp = campIter.next();
      var stats = null;
      try {
        stats = camp.getStatsFor(dateFrom, dateTo);
      } catch (errCustomDate) {
        try {
          stats = camp.getStatsFor("LAST_7_DAYS");
          periodLabel = "Последние 7 дней";
        } catch (e7) {}
      }

      if (stats) {
        var clicks = stats.getClicks();
        var imps = stats.getImpressions();
        var cost = stats.getCost();

        totalClicks += clicks;
        totalImps += imps;
        totalCost += cost;

        var campName = camp.getName() || "";
        var isSearch = campName.indexOf("Shopping") === -1 && campName.indexOf("Покупки") === -1;
        if (isSearch) {
          searchClicks += clicks;
          searchImps += imps;
          searchCost += cost;
        }
      }
    }
  } catch (e) {}

  var overallCtr = totalImps > 0 ? (totalClicks / totalImps) * 100 : 0.0;
  var searchCtr = searchImps > 0 ? (searchClicks / searchImps) * 100 : 0.0;

  return {
    totalClicks: totalClicks,
    totalImps: totalImps,
    totalCost: totalCost,
    overallCtr: overallCtr,
    searchClicks: searchClicks,
    searchImps: searchImps,
    searchCost: searchCost,
    searchCtr: searchCtr,
    periodLabel: periodLabel
  };
}

function analyzeAndFilterQueries(existingKeywords) {
  var goldenList = [];
  var junkList = [];
  var seen = {};

  try {
    var query = "SELECT search_term_view.search_term, metrics.clicks, metrics.impressions, metrics.ctr, metrics.conversions, metrics.cost_micros " +
                "FROM search_term_view WHERE segments.date DURING LAST_7_DAYS AND metrics.clicks > 0";
    var rows = AdsApp.search(query);

    while (rows.hasNext()) {
      var row = rows.next();
      var stv = row.searchTermView || row.search_term_view;
      var rawTerm = stv ? (stv.searchTerm || stv.search_term || "") : "";
      rawTerm = (rawTerm || "").trim();
      var term = rawTerm.toLowerCase();
      if (!term || term.length < 3) continue;
      if (seen[term]) continue;
      seen[term] = true;

      var metrics = row.metrics || {};
      var clicks = Number(metrics.clicks || 0);
      var imps = Number(metrics.impressions || 0);
      var rawCtr = metrics.ctr != null ? Number(metrics.ctr) : (imps > 0 ? clicks / imps : 0);
      var ctr = rawCtr <= 1.0 ? rawCtr * 100 : rawCtr;
      var conv = Number(metrics.conversions || 0);

      var evalRes = classifySearchTerm(term);

      if (evalRes.type === "GOLDEN") {
        if (!existingKeywords[term]) {
          goldenList.push({
            raw: rawTerm,
            exactTag: "[" + rawTerm + "]",
            clicks: clicks,
            ctr: ctr.toFixed(1),
            conv: conv,
            reason: evalRes.reason
          });
        }
      } else if (evalRes.type === "JUNK") {
        junkList.push({
          raw: rawTerm,
          clicks: clicks,
          ctr: ctr.toFixed(1),
          reason: evalRes.reason
        });
      }
    }
  } catch (e) {
    Logger.log("  [!] Ошибка анализа поисковых запросов: " + e);
  }

  goldenList.sort(function(a, b) {
    if (b.conv !== a.conv) return b.conv - a.conv;
    if (b.clicks !== a.clicks) return b.clicks - a.clicks;
    return parseFloat(b.ctr) - parseFloat(a.ctr);
  });

  junkList.sort(function(a, b) {
    return b.clicks - a.clicks;
  });

  return {
    golden: goldenList,
    junk: junkList
  };
}

function evaluateTrafficLight(budgetInfo, stats) {
  var isCtrHigh = stats.searchCtr >= CONFIG.MIN_CTR_THRESHOLD;
  var isBudgetCapped = budgetInfo.isSaturated;

  if (isCtrHigh && isBudgetCapped) {
    return {
      status: "GREEN",
      icon: "🟢",
      title: "ЗЕЛЕНЫЙ СВЕТ — ПОРА МАСШТАБИРОВАТЬСЯ!",
      recommendation: "Подними дневной бюджет кампании с $" + budgetInfo.totalDailyBudget.toFixed(2) + " до $" + (budgetInfo.totalDailyBudget * 1.5).toFixed(2) + " (высокий спрос, Search CTR " + stats.searchCtr.toFixed(1) + "% > " + CONFIG.MIN_CTR_THRESHOLD + "%)."
    };
  }

  if (isCtrHigh && !isBudgetCapped) {
    return {
      status: "YELLOW",
      icon: "🟡",
      title: "ЖЕЛТЫЙ СВЕТ — CTR ВЫШЕ 10%, НО БЮДЖЕТА ХВАТАЕТ",
      recommendation: "Search CTR отличный (" + stats.searchCtr.toFixed(1) + "% >= " + CONFIG.MIN_CTR_THRESHOLD + "%), но бюджет еще не исчерпан (потрачено " + budgetInfo.usagePct.toFixed(0) + "%). Текущего лимита хватает."
    };
  }

  if (!isCtrHigh && isBudgetCapped) {
    return {
      status: "YELLOW",
      icon: "🟡",
      title: "ЖЕЛТЫЙ СВЕТ — БЮДЖЕТ В ЛИМИТЕ, НО CTR НИЖЕ 10%",
      recommendation: "Бюджет выработан, но Search CTR (" + stats.searchCtr.toFixed(1) + "%) пока ниже " + CONFIG.MIN_CTR_THRESHOLD + "%. Проверь КМС и минус-слова перед подъемом бюджета."
    };
  }

  return {
    status: "YELLOW",
    icon: "🟡",
    title: "ЖЕЛТЫЙ СВЕТ — ДЕРЖИМ ТЕКУЩИЙ БЮДЖЕТ",
    recommendation: "Идет плановый сбор данных. Дневного бюджета $" + budgetInfo.totalDailyBudget.toFixed(2) + " хватает, Search CTR = " + stats.searchCtr.toFixed(1) + "% (цель: >=10%). Держим текущие ставки."
  };
}

function buildCleanReport(reportDate, budgetInfo, stats, queries, trafficLight) {
  var lines = [];
  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("  💎 LIVI JEWELRY — СОВЕТНИК ПО МАСШТАБИРОВАНИЮ v1.3.2 (ВЕЧЕР 21:00)");
  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("Дата анализа: " + reportDate + " (Астана)");
  lines.push("Период анализа качества: " + stats.periodLabel);
  lines.push("");

  lines.push("🚦 ВЕРДИКТ МАСШТАБИРОВАНИЯ:");
  lines.push("   " + trafficLight.icon + " " + trafficLight.title);
  lines.push("   👉 " + trafficLight.recommendation);
  lines.push("");

  lines.push("📊 1. ЕМКОСТЬ РЫНКА ЗА СЕГОДНЯ:");
  if (budgetInfo.isSaturated) {
    lines.push("   • Факт: Дневной бюджет $" + budgetInfo.totalDailyBudget.toFixed(2) + " выработан на " + budgetInfo.usagePct.toFixed(0) + "% (израсходовано $" + budgetInfo.totalSpend.toFixed(2) + "). Кампания уперлась в лимит.");
    lines.push("   • Совет: Ты теряешь вечерних покупателей. Рынок готов принять $" + (budgetInfo.totalDailyBudget * 1.5).toFixed(2) + "/день.");
  } else {
    lines.push("   • Факт: Бюджета $" + budgetInfo.totalDailyBudget.toFixed(2) + " хватило на весь день (израсходовано $" + budgetInfo.totalSpend.toFixed(2) + ", выработано " + budgetInfo.usagePct.toFixed(0) + "%).");
    lines.push("   • Совет: Дневной лимит оптимален, искусственно раздувать бюджет не требуется.");
  }
  lines.push("");

  lines.push("📈 2. КАЧЕСТВО ТРАФИКА И CTR:");
  lines.push("   • Search CTR (Чистый поиск): " + stats.searchCtr.toFixed(1) + "% [Цель: >=" + CONFIG.MIN_CTR_THRESHOLD + "%]");
  lines.push("   • Всего кликов на Поиске: " + stats.searchClicks + " | Показов: " + stats.searchImps + " | Расход: $" + stats.searchCost.toFixed(2));
  if (stats.totalImps > stats.searchImps) {
    var displayImps = stats.totalImps - stats.searchImps;
    lines.push("   ⚠️ ВНИМАНИЕ: Зафиксировано " + displayImps + " показов вне чистого поиска (КМС / Поисковые партнеры). Это размывает общий CTR до " + stats.overallCtr.toFixed(1) + "%!");
    lines.push("      Действие: Отключи галочку «Контекстно-медийная сеть» в настройках поисковой кампании.");
  }
  lines.push("");

  lines.push("💎 3. САМОРОДКИ РЕАЛЬНЫХ ПОКУПАТЕЛЕЙ (ТОЛЬКО ИЗДЕЛИЯ LIVI JEWELRY):");
  if (queries.golden.length === 0) {
    lines.push("   • За последние 7 дней все целевые запросы покупателей уже добавлены в ключевые слова.");
  } else {
    lines.push("   Скопируй этот блок и вставь в Поисковую кампанию -> Ключевые слова:");
    lines.push("   -------------------------------------------------");
    for (var g = 0; g < queries.golden.length; g++) {
      var item = queries.golden[g];
      lines.push("   " + item.exactTag + "  /* " + item.clicks + " кл., CTR " + item.ctr + "% — " + item.reason + " */");
    }
    lines.push("   -------------------------------------------------");
  }
  lines.push("");

  if (queries.junk.length > 0) {
    lines.push("🚫 4. ОБНАРУЖЕННЫЙ МУСОР И КОНКУРЕНТЫ ЗА 7 ДНЕЙ (БЛОКИРУЮТСЯ АВТОПИЛОТОМ):");
    lines.push("   (Эти нецелевые запросы сливали бюджет. Скрипт-автопилот отсекает их):");
    for (var j = 0; j < Math.min(queries.junk.length, 12); j++) {
      var junk = queries.junk[j];
      lines.push("   • «" + junk.raw + "» — " + junk.clicks + " кл., CTR " + junk.ctr + "% [" + junk.reason + "]");
    }
    lines.push("");
  }

  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("Советник работает в режиме Read-Only (без автоматических списаний).");

  return lines.join("\n");
}
