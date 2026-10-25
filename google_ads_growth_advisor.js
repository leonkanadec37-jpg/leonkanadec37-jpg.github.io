/**
 * ==============================================================================
 * LIVI JEWELRY — GROWTH & KEYWORD ADVISOR v2.0 (СОВЕТНИК НА БАЗЕ АВТОПИЛОТА)
 * ==============================================================================
 *
 * РОЛЬ СКРИПТА (Вариант А — Умный Советник):
 * 1. Анализирует реальные поисковые запросы за последние 7 дней (Search + Shopping).
 * 2. Использует СТРОГИЕ ФИЛЬТРЫ автопилота v5.8.1 Diamond Shield:
 *    - Моментально бракует бренды-конкуренты (aroush, swarovski, pandora, tiffany и др.).
 *    - Моментально бракует инфо-запросы («сколько стоит», «с чем носить», «виды», «свойства»).
 *    - Моментально бракует чужие материалы (муранское стекло, бисер, дерево, смола).
 *    - Запрещает одиночные браслеты, кольца, кулоны/подвески с буквами (нет в ассортименте Livi).
 * 3. Находит ТОЛЬКО настоящие целевые самородки и раскладывает их по 8 группам:
 *    - Группа 1: Комплекты и сеты (Sets)
 *    - Группа 2: Колье из натурального жемчуга (Pearl Necklaces)
 *    - Группа 3: Колье и бусы из натуральных камней (Stone Necklaces)
 *    - Группа 4: Серьги с натуральными камнями и жемчугом (Earrings)
 *    - Группа 5: Чокеры из жемчуга и камней (Chokers)
 *    - Группа 6: Сотуары и лариаты (Sotuars & Lariats)
 *    - Группа 7: Барочный жемчуг и цепи (Baroque Pearl)
 *    - Группа 8: Жемчуг Майорка (Mallorca Pearl)
 * 4. Формирует чистый и понятный отчет (в лог и на почту) с разделением:
 *    - 💎 САМОРОДКИ ДЛЯ ДОБАВЛЕНИЯ (с указанием конкретной группы объявлений)
 *    - 🚫 ОТФИЛЬТРОВАННЫЙ МУСОР (заблокирован автопилотом)
 *    - 📊 СВОДКА БЮДЖЕТА И CTR
 * ==============================================================================
 */

var CONFIG = {
  ALERT_EMAIL: "viksonna94@gmail.com",
  MIN_CTR_THRESHOLD: 10.0,
  BUDGET_SATURATION_PCT: 88.0,
  TARGET_CAMPAIGN_NAME: "Livi Jewelry - Поиск Казахстан",
  SEND_EMAIL: true
};

// ------------------------------------------------------------------------------
// 1. БРЕНДЫ-КОНКУРЕНТЫ (ПОЛНАЯ БАЗА АВТОПИЛОТА v5.8.1)
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
  /damiani/i, /фрай\s*вилл/i, /frey\s*wille/i, /сблеском/i, /sbleskom/i, /луи\s*ви/i,
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
  /moon\s*almaty/i, /moon\s*(украшения|бижутерия)/i, /roberto\s*bravo/i, /роберто\s*браво/i,
  /(^|[^а-яёa-z])алтын([^а-яёa-z]|$)/i, /altyn\b/i, /talisman\s*kz/i, /микимото/i,
  /mikimoto/i, /gotto\s*jewelry/i, /pure\s*jewelry/i, /soroka\s*jewelry/i, /сорока\s*jewelry/i,
  /nomination/i, /номинэйшн/i, /лакост/i, /lacoste/i, /la\s*roche/i, /jewelry\s*bus/i,
  /minimal\s*silver/i, /браслет\s*minimal/i, /muraa/i, /yelai/i, /jewelfinger/i,
  /darry\s*ring/i, /favory/i, /farro/i, /via\s*jewelry/i, /astra\s*jewelry/i,
  /le\s*carat/i, /mimi\s*jewelry/i, /assos/i, /два\s*жираф/i, /ganezzi/i,
  /larimar\s*jewelry/i,

  // Мировые дома высокой моды, премиальные бренды и обновление v5.8.1:
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
  /sophie\s*buhai/i, /софи\s*бухай/i, /hugo\s*kreit/i, /vida\s*kush/i,
  /kalliope/i, /каллиоп/i, /сара\s*кавентри/i, /sarah\s*coventry/i,
  /aimaq/i, /аймак/i, /kirks\s*folly/i, /жемчуг\s*dame/i, /\bdame\b/i,
  /скиапарелли/i, /schiaparelli/i, /стайл\s*авеню/i, /style\s*avenue/i,
  /offbeat/i, /coeur\s*de\s*lion/i, /emily\s*lux/i, /viled/i, /вилед/i,
  /lhasa/i, /лхаса/i, /charlotte\s*chesnais/i, /tina\s*pearl/i,
  /саботини/i, /sabotini/i, /leari/i, /\bzara\b/i, /(^|[^а-яёa-z])зара([^а-яёa-z]|$)/i,
  /тадж\s*махал/i, /камнемани/i, /la\s*voie\s*nomade/i,
  /uno\s*de\s*50/i, /selro/i, /selini/i, /tory\s*burch/i, /леонардо/i
];

// ------------------------------------------------------------------------------
// 2. БЕЛЫЙ СПИСОК НАТУРАЛЬНЫХ КАМНЕЙ И ЖЕМЧУГА (LIVI JEWELRY)
// ------------------------------------------------------------------------------
var SAFE_STONE_ROOTS = [
  // Русские корни натуральных камней и жемчуга (включая майкаинскую бирюзу и картографическую яшму):
  /жемчу[гж]/i, /барочн/i, /майорк/i, /майорик/i, /majorica/i, /pearl/i, /перламутр/i,
  /нефрит/i, /жадеит/i, /джедаит/i,
  /аметист/i, /малахит/i, /агат/i, /гранат/i, /кварц/i, /бирюз/i, /гематит/i, /хрустал/i,
  /лунн.*камен/i, /лунн/i, /адуляр/i, /тигров.*глаз/i, /тигров/i, /лазурит/i, /коралл/i, /яшм/i,
  /сердолик/i, /карнеол/i, /амазонит/i, /турмалин/i, /цитрин/i, /авантюрин/i, /флюорит/i,
  /оникс/i, /шпинел/i, /лабрадор/i, /чароит/i, /хризопраз/i, /змеевик/i,
  /топаз/i, /аквамарин/i, /берилл/i, /опал/i, /янтар/i, /родонит/i, /пирит/i, /содалит/i,
  /морганит/i, /родохрозит/i, /кунцит/i, /халцедон/i, /ларимар/i, /larimar/i, /празиолит/i,
  /хризолит/i, /хризоколл/i, /апатит/i, /танзанит/i, /варисцит/i, /александрит/i,
  /диоптаз/i, /арагонит/i, /aragonite/i, /обсидиан/i, /кошачий.*глаз/i, /параиб/i, /азурмалахит/i,
  /майкаинск.*бирюз/i, /картографическ.*яшм/i, /пейзажн.*яшм/i,

  // Указание на натуральные камни / минералы / дизайнерские изделия (RU):
  /натуральн.*камн/i, /натуральн.*камен/i, /природн.*камн/i, /природн.*камен/i,
  /издели.*из.*камн/i, /бусы.*из.*камн/i, /браслет.*из.*камн/i, /колье.*из.*камн/i,
  /серьги.*с.*камн/i, /пусет.*с.*камн/i, /гвоздик.*с.*камн/i,
  /кольц.*с.*камн/i, /кольц.*с.*минерал/i,
  /с\s+(большим|крупным|розовым|черным|желтым|зеленым|голубым|синим|белым|красным)и?\s+камн/i,
  /дизайнерск.*(украшен|серьг|сережк|серёжк|колье|браслет|чокер|бусы|ожерель|сотуар|кольц)/i,
  /украшен.*ручной\s*работы/i, /авторск.*(украшен|серьг|сережк|серёжк|колье|браслет|чокер|бусы|сотуар|кольц)/i,

  // Белый список для бижутерии Livi (v5.8.1):
  /бижутери.*(алматы|астана|казахстан|кз|kz)/i,
  /(алматы|астана|казахстан|кз|kz).*бижутери/i,
  /(авторск|дизайнерск|элитн|качествен|стильн|женск|ручной\s*работы).*бижутери/i,
  /бижутери.*(авторск|дизайнерск|элитн|качествен|стильн|женск|ручной\s*работы)/i,
  /бижутери.*из.*камн/i,

  // Казахские термины украшений и камней (KZ) + полная защита казахских национальных украшений:
  /әшекей/i, /бұйым/i, /маржан/i, /меруерт/i, /інжу/i, /алқа/i, /білезік/i, /сырға/i, /сырга/i,
  /шашбау/i, /асыл\s*тас/i, /табиғи\s*тас/i, /ақық/i, /перуза/i, /кәріптас/i, /ай\s*тас/i,
  /этно/i, /этническ/i, /национальн.*украшен/i, /современн.*казахск.*украшен/i,
  /казахск.*(украшен|серьг|сережк|серёжк|колье|браслет|чокер|бусы|ожерель|сотуар|кольц|кулон|подвеск|комплект|набор|бижутери|стил)/i,
  /(украшен|серьг|сережк|серёжк|колье|браслет|чокер|бусы|ожерель|сотуар|кольц|кулон|подвеск|комплект|набор|бижутери).*казахск/i,
  /национальн.*(украшен|серьг|сережк|серёжк|колье|браслет|чокер|бусы|ожерель|сотуар|кольц|кулон|подвеск|комплект|набор|бижутери|стил)/i,
  /(украшен|серьг|сережк|серёжк|колье|браслет|чокер|бусы|ожерель|сотуар|кольц|кулон|подвеск|комплект|набор|бижутери).*национальн/i,
  /kazakh.*jewel/i, /labrador/i, /carnelian/i,

  // Узбекские термины натуральных камней, жемчуга и авторских украшений (UZ Латиница + Кириллица):
  /marvarid/i, /марварид/i, /\bdur\b/i, /\bsadaf\b/i, /садаф/i,
  /feruza/i, /феруза/i, /\baqiq\b/i, /ақиқ/i, /anor\s*tosh/i, /анор\s*тош/i,
  /nefrit/i, /malaxit/i, /ametist/i, /kvars/i, /gematit/i,
  /tog['’ʻ]?\s*billur/i, /\bbillur\b/i, /биллур/i, /oy\s*tosh/i, /ой\s*тош/i,
  /yo['’ʻ]?lbars\s*ko['’ʻ]?z/i, /йўлбарс\s*кўз/i, /lazurit/i, /lojuvard/i, /ложувард/i,
  /marjon\s*tosh/i, /yashma/i, /kahrabo/i, /каҳрабо/i, /serdolik/i, /turmalin/i,
  /avanturin/i, /flyuorit/i, /oniks/i, /shpinel/i, /topaz/i, /akvamarin/i, /berill/i,
  /tabiiy\s*tosh/i, /табиий\s*тош/i, /qimmatbaho\s*tosh/i,
  /qo['’ʻ]?l\s*mehnat/i, /қўл\s*меҳнат/i, /mualliflik\s*taqinchoq/i,

  // Фирменные категории мастерской Livi:
  /сотуар/i, /сатуар/i, /sotuar/i, /чокер/i, /choker/i, /livi/i
];

// ------------------------------------------------------------------------------
// 3. СТОП-ПАТТЕРНЫ МУСОРА, МАТЕРИАЛОВ И ИНФО-ЗАПРОСОВ (АВТОПИЛОТ v5.8.1)
// ------------------------------------------------------------------------------
var JUNK_PATTERNS = [
  // Литература и фейки клевер/гвоздь:
  /мопассан/i, /краткое\s*содержание/i, /рассказ.*ожерелье/i, /анализ\s*рассказа/i,
  /клевер/i, /гвоздь/i,

  // Производство, ювелирные мастерские, переплавка, лом, экспертиза, гравировка (RU + KZ + UZ):
  /на заказ/i, /изготовлен/i, /мастерск/i, /переплав/i, /лить[её]/i,
  /гравировк/i, /с надписью/i, /сделать на заказ/i,
  /ювелиры алматы/i, /ювелир алматы/i, /ювелир астана/i, /ювелиры астана/i,
  /экспертиз/i, /(^|[^а-яёa-z])лом([^а-яёa-z]|$)/i, /инструмент/i,
  /уменьшени/i, /увеличени/i, /научиться/i, /станок/i, /станки/i,
  /замок\s+для/i, /оценк/i, /(^|[^а-яёa-z])нить([^а-яёa-z]|$)/i, /часик/i,
  /сережки\s+капельки/i, /дубай/i,
  // UZ мастерские / ремонт / изготовление:
  /ustaxon/i, /устахон/i, /ta['’ʻ]?mirlash/i, /tamirlash/i, /таъмирлаш/i,
  /yasash/i, /ясаш/i, /kavsharlash/i, /qayta\s*eritish/i, /gravirovka/i,

  // Дети, девочки, возраст и непрофильные изделия (RU + UZ):
  /для девочк/i, /девочке/i, /девочки/i, /для детей/i, /детск/i, /фигурк.*детей/i,
  /для\s+\d+\s+лет/i, /для\s+самых\s+маленьких/i, /qizlar\s*uchun/i, /bolalar\s*uchun/i,
  /брошь/i, /броши/i, /брошка/i, /to['’ʻ]?g['’ʻ]?nog['’ʻ]?ich/i,
  /фенечк/i, /кафф/i, /клипс/i, /конго/i, /дорик/i, /галстук/i,
  /гердан/i, /шахмаран/i, /шаркия/i, /с\s*кольцами/i, /шибирма/i, /shibirma/i,
  /хеликс/i, /мэрилин\s*монро/i, /аксессуар/i, /спорт\s*шик/i, /(^|\s)(вишн|клубник|ягод|фрукт)/i,

  // Пустые общие онлайн-запросы и иноязычный спам (турецкий без флага i на ı, грузинский, арабский, польский):
  /^заказать онлайн$/i, /^купить онлайн$/i, /чоловічі/i, /срібні/i,
  /[şğŞĞı]/, /[\u0600-\u06FF]/, /(^|[^a-zşğıçöü])taşı([^a-zşğıçöü]|$)/i, /(^|[^a-zşğıçöü])tasi([^a-zşğıçöü]|$)/i, /\bakik\b/i, /\bsedef\b/i,
  /faydalar/i, /kazakistandan/i, /margalitis/i, /yelsabami/i, /bizuteria/i,
  /\bkamen\b/i, /persian/i, /\bmaori\b/i, /\bindian\b/i, /\balpaca\b/i,

  // Годовщины свадеб и подарки (БЕЗ блокировки обычных свадебных украшений невесты!):
  /(агатов|бирюзов|лавандов|ситцев|деревянн|розов|серебрян|золот).*свадьб/i,
  /на\s+[а-яё]+\s+свадьбу/i, /что\s+дарить/i, /что\s+дарят/i, /что\s+привезти/i, /женский\s+день/i,
  /(^|\s)подар/i, /что подарить/i, /что можно подарить/i, /день рожден/i, /(^|[^а-яёa-z])д[рp]([^а-яёa-z]|$)/i,
  /юбилей/i, /годовщин/i, /молодожен/i, /презент/i, /сюрприз/i,
  /\bsovg['’ʻ]?a\b/i, /совға/i, /tug['’ʻ]?ilgan\s*kun/i,

  // Рукоделие, DIY, детали, бусины, шармы и фурнитура для сборки (RU + UZ):
  /своими руками/i, /o['’ʻ]?z\s*qo['’ʻ]?li\s*bilan/i, /ўз\s*қўли\s*билан/i,
  /как сделать/i, /qanday\s*yasaladi/i, /как сплести/i, /как собрать/i, /научиться делать/i, /схем/i,
  /мастер класс/i, /(^|[^а-яёa-z])мк([^а-яёa-z]|$)/i, /бисероплетени/i, /бисер/i, /\bbiser\b/i,
  /плетени/i, /to['’ʻ]?qish/i, /вязани/i, /вязан/i, /крючком/i,
  /фурнитур/i, /furnitur/i, /застежк/i, /швенз/i, /штифт/i, /(^|[^а-яёa-z])пины([^а-яёa-z]|$)/i,
  /леск/i, /проволок/i, /тросик/i, /бусин/i, /ракуш/i, /шарм/i, /из\s*ткани/i, /глин/i,
  /пинтерест/i, /pinterest/i, /из\s*монет/i, /(^|[^а-яёa-z])дзи([^а-яёa-z]|$)/i,
  /cabouchon/i, /магнитн/i, /эпоксидн/i, /полимерн.*глин/i, /вышивк/i, /с буквой/i,
  /букв[аы]\s+[a-zа-я]/i, /снейк/i, /дизайн бус/i, /кабошон/i,

  // Редкие минералы вне ассортимента Livi и нецелевые материалы (v5.8.1):
  /андалузит/i, /стихтит/i, /уникит/i, /унакит/i, /голубой\s*янтар/i, /варисции/i,
  /стекл/i, /shisha/i, /муранск/i, /murano/i, /мурано/i, /стекляр/i, /шерст/i, /валян/i,
  /муассанит/i, /фианит/i, /fianit/i, /дерев/i, /yog['’ʻ]?och/i, /пластик/i, /plastik/i,
  /акрил/i, /силикон/i, /каучук/i, /керами[кч]/i, /keramik/i,
  /веревочк/i, /на веревк/i, /шнурок/i, /xuping/i, /ксьюпинг/i, /медицинск/i,
  /ис+кусс?твен/i, /sun['’ʻ]?iy/i, /сунъий/i, /шкатулк/i, /quti/i,
  /лабрет/i, /пирсинг/i, /pirsing/i, /(^|[^а-яёa-z])(мело|melo)([^а-яёa-z]|$)/i,
  /сколько\s+стоит/i, /сколько\s+стоят/i, /аква кварц/i, /сутажн/i, /минанкари/i,

  // Халява, ломбарды, скупка, дешевый опт, б/у, маркетплейсы, соцсети (RU + UZ):
  /инстаграм/i, /instagram/i,
  /дешев/i, /недорог/i, /arzon/i, /арзон/i, /бесплатн/i, /bepul/i, /даром/i,
  /ломбард/i, /lombard/i, /скупк/i, /залог/i, /кредит/i, /kredit/i, /qarzga/i,
  /сдать/i, /проба/i, /proba/i, /585/i, /750/i, /925/i, /слит/i, /quym/i,
  /грамм/i, /gramm/i, /карат/i, /karat/i, /алиэкспресс/i, /aliexpress/i, /temu/i, /тему/i,
  /shein/i, /шейн/i, /таобао/i, /taobao/i, /секонд/i, /барахолк/i, /конфискат/i,
  /(^|[^а-яёa-z])б[\s/]?у([^а-яёa-z]|$)/i, /ishlatilgan/i,
  /оптом/i, /(^|[^а-яёa-z])опт([^а-яёa-z]|$)/i, /ulgurji/i, /улгуржи/i, /optom/i,
  /olx/i, /олх/i, /авито/i, /ярмарка мастеров/i, /etsy/i,

  // Заводское золото, серебро, бриллианты и драгкамни 1-й категории (RU + KZ + UZ):
  /(^|\s)золот/i, /белого\s+золота/i, /tilla/i, /тилла/i, /\boltin\b/i, /олтин/i,
  /серебр/i, /serebro/i, /silver/i, /kumush/i, /кумуш/i, /күміс/i,
  /платин/i, /бриллиант/i, /брилиан/i, /diamond/i, /olmos/i, /олмос/i,
  /изумруд/i, /zumrad/i, /зумрад/i, /рубин/i, /сапфир/i, /yoqut/i, /ёқут/i,
  /теннисн/i, /tennis.*bracelet/i, /печатка/i, /обручальн/i, /помолвочн/i, /nikoh\s*uzuk/i,
  /парные кольца/i, /кольца парные/i, /на мизинец/i, /винтов/i, /с драгоценным камнем/i,

  // Мебель, кухонные гарнитуры, наушники:
  /кухон/i, /мебел/i, /гарнитур/i, /наушник/i, /блютуз/i, /bluetooth/i, /диван/i, /шкаф/i, /стол/i,

  // Одежда и чужие части тела:
  /шапк/i, /рубашк/i, /плать/i, /ko['’ʻ]?ylak/i, /кофт/i, /пальто/i, /юбк/i, /на ног/i, /oyoqqa/i, /через палец/i,

  // Информационный щит v5.8.1, эзотерика, гороскопы, сонники, уход, ремонт (RU + KZ + UZ):
  /подойд/i, /какие\s+подойдут/i, /(^|\s)это(\s|$)/i, /деген\s*не/i,
  /тренд/i, /2024/i,
  /(^|[^а-яёa-z])виды([^а-яёa-z]|$)/i, /разновидност/i, /шакка/i, /sciacca/i,
  /что такое/i, /что это/i, /nima\s*degani/i, /nima\s*bu/i,
  /что\s+за\s/i, /как называется/i, /названи/i, /nomlari/i,
  /как носить/i, /с чем носить/i, /qanday\s*taqiladi/i, /кому\s+нельзя/i, /можно\s+ли\s+дарить/i,
  /бывает\s+ли/i, /в\s+природе/i, /какого\s+цвета/i,
  /камень\s+(черного|зеленого|зелёного|голубого|красного|синего|белого|розового|желтого)\s+цвета/i,
  /цвета\s+непрозрачн/i, /это\s+агат/i, /это\s+драгоценный/i, /это\s+натуральный/i, /дорогой\s+камень/i,
  /сочетание/i, /для чего/i, /зачем/i, /ремонт/i, /пайк/i, /перетяжк/i, /чистк/i,
  /как почистить/i, /qanday\s*tozalanadi/i, /ультразвуков/i,
  /как отличить/i, /как проверить/i, /как определить/i, /как понять/i, /qanday\s*farqlash/i, /haqiqiymi/i,
  /как выгляд/i, /подделк/i, /qalbaki/i, /кому подходит/i, /подходит ли/i, /kimga\s*mos/i,
  /свойств/i, /xususiyat/i, /хусусият/i, /foydasi/i, /фойдаси/i, /значени/i, /ma['’ʻ]?nosi/i, /маъноси/i,
  /гороскоп/i, /munajjim/i, /знак.*зодиак/i, /знак/i, /\bburj/i, /бурж/i,
  /магическ/i, /лечебн/i, /shifobaxsh/i, /литотерапи/i, /талисман/i, /talisman/i,
  /оберег/i, /амулет/i, /tumor/i, /тумор/i, /приворот/i, /заговор/i,
  /сонник/i, /к чему снится/i, /tushda/i, /tush\s*tabiri/i, /тушда/i,
  /википеди/i, /месторожден/i, /твердость/i, /формула/i, /(^|[^а-яёa-z])фото([^а-яёa-z]|$)/i, /картинк/i, /rasm/i,
  /обои/i, /скачать/i, /видео/i, /реферат/i, /ваканси/i, /резюме/i, /работа/i, /ish\s*o['’ʻ]?rni/i,
  /зарплат/i, /мужск/i, /для мужчин/i, /мужчин/i, /erkaklar/i, /крестик/i, /четки/i, /тасбих/i, /tasbeh/i,
  /часы/i, /\bsoat\b/i, /зодиак/i, /лучший\s+камень/i,
  /овен/i, /телец/i, /тельц/i, /близнец/i, /(^|[^а-яёa-z])рак([^а-яёa-z]|$)/i, /рака/i, /раков/i,
  /(^|[^а-яёa-z])лев([^а-яёa-z]|$)/i, /льва/i, /львов/i, /дева/i, /девы/i, /девам/i,
  /весы/i, /весов/i, /скорпион/i, /стрелец/i, /козерог/i, /водолей/i, /рыбы/i, /у\s+рыб([^а-яёa-z]|$)/i, /рыбам/i,
  /қазақша/i,

  // Полный фильтр курортных стран и чужого импорта (ТОП-15 v5.8.1 — БЕЗ казахск и национальн!) и оффлайн-поиск:
  /та[йи]ланд/i, /тайск/i, /вьетнам/i, /шри ланк/i, /катар/i, /пхукет/i, /(^|[^а-яёa-z])гоа([^а-яёa-z]|$)/i,
  /туркестан/i, /египет/i, /(^|[^а-яёa-z])бали([^а-яёa-z]|$)/i, /milan/i, /милан/i, /греци/i, /япони/i,
  /украин/i, /дагестан/i, /турки/i, /турецк/i, /турци/i, /корейск/i, /корея/i, /индийск/i, /индия/i,
  /грузинск/i, /чешск/i, /чехи/i, /испанск/i, /французск/i, /итальянск/i, /итали/i,
  /китая/i, /(^|[^а-яёa-z])китай([^а-яёa-z]|$)/i, /китайск/i, /ссср/i, /ближайш/i, /поблизости/i, /рядом/i, /yaqinidagi/i,

  // Кольца, пусеты, гвоздики (RU + KZ + UZ) проверяются ПОСЛЕ всех остальных стоп-слов:
  // (если есть камень/жемчуг — разрешены; если без камня — переводятся строго в ТОЧНОЕ соответствие [X]):
  /кольц/i, /колечк/i, /перстен/i, /пусет/i, /пуссет/i, /гвоздик/i,
  /\buzuk\b/i, /\buzuklar\b/i, /узук/i, /\bzirak\b/i, /\bziraklar\b/i, /зирак/i
];

/**
 * Оценка поискового запроса по строгой матрице ассортимента Livi
 */
function evaluateSearchTermForAdvisor(term) {
  var lower = (term || "").toLowerCase().trim().replace(/^["\[]|["\]]$/g, "").trim();
  if (!lower || lower.length < 3) {
    return { isGold: false, reason: "Слишком короткий запрос" };
  }

  // 1. Проверка на бренды-конкуренты (автоматический бан)
  for (var b = 0; b < COMPETITOR_BRANDS.length; b++) {
    if (COMPETITOR_BRANDS[b].test(lower)) {
      return { isGold: false, isJunk: true, reason: "Бренд-конкурент (" + COMPETITOR_BRANDS[b].source + ")" };
    }
  }

  // 2. Проверка на стоп-паттерны автопилота (муранское стекло, сколько стоит, с чем носить, золото 585 и т.д.)
  for (var j = 0; j < JUNK_PATTERNS.length; j++) {
    if (JUNK_PATTERNS[j].test(lower)) {
      return { isGold: false, isJunk: true, reason: "Мусор / Стоп-паттерн (" + JUNK_PATTERNS[j].source + ")" };
    }
  }

  // 3. ЖЕСТКИЙ ЗАПРЕТ позиций, которых нет в каталоге Livi:
  // А) Одиночные браслеты (Livi НЕ продает браслеты отдельно)
  if (/браслет/i.test(lower) && !/(комплект|набор|сет)/i.test(lower)) {
    return { isGold: false, isJunk: true, reason: "Одиночный браслет (нет в каталоге Livi)" };
  }
  // Б) Одиночные кольца (Livi НЕ продает кольца отдельно)
  if (/кольц/i.test(lower) && !/(комплект|набор|сет)/i.test(lower)) {
    return { isGold: false, isJunk: true, reason: "Кольцо (нет в каталоге Livi)" };
  }
  // В) Кулоны / подвески / буквы / крестики
  if (/(кулон|подвеск|букв|крестик|четки|тасбих)/i.test(lower)) {
    return { isGold: false, isJunk: true, reason: "Кулон / подвеска / чужой тип изделия" };
  }

  // 4. Определение конкретной целевой группы Livi Jewelry (1 из 8):
  var targetGroup = null;
  var groupNum = 0;

  if (/(комплект|набор|сет)/i.test(lower)) {
    targetGroup = "1. Комплекты и сеты (Sets)";
    groupNum = 1;
  } else if (/майорк|майорик|majorica/i.test(lower)) {
    targetGroup = "8. Жемчуг Майорка (Mallorca Pearl)";
    groupNum = 8;
  } else if (/барочн|барокко/i.test(lower)) {
    targetGroup = "7. Барочный жемчуг и цепи (Baroque Pearl)";
    groupNum = 7;
  } else if (/чокер|choker/i.test(lower)) {
    targetGroup = "5. Чокеры из натуральных камней и жемчуга";
    groupNum = 5;
  } else if (/сотуар|сатуар|лариат|sotuar/i.test(lower)) {
    targetGroup = "6. Сотуары и лариаты (Sotuars & Lariats)";
    groupNum = 6;
  } else if (/(серьг|сережк|серёжк)/i.test(lower)) {
    targetGroup = "4. Серьги с натуральными камнями и жемчугом";
    groupNum = 4;
  } else if (/(колье|бусы|ожерель)/i.test(lower)) {
    if (/жемчу[гж]|перламутр/i.test(lower)) {
      targetGroup = "2. Колье из натурального жемчуга (Pearl Necklaces)";
      groupNum = 2;
    } else {
      targetGroup = "3. Колье и бусы из натуральных камней (Stone Necklaces)";
      groupNum = 3;
    }
  }

  if (!targetGroup) {
    return { isGold: false, isJunk: true, reason: "Сырьевой запрос без готового изделия (нет колье/серег/чокера)" };
  }

  // 5. Обязательное наличие камня или жемчуга из каталога Livi
  var hasStone = false;
  for (var s = 0; s < SAFE_STONE_ROOTS.length; s++) {
    if (SAFE_STONE_ROOTS[s].test(lower)) {
      hasStone = true;
      break;
    }
  }

  if (!hasStone) {
    return { isGold: false, isJunk: true, reason: "Нет камня или жемчуга из каталога Livi" };
  }

  return {
    isGold: true,
    isJunk: false,
    group: targetGroup,
    groupNum: groupNum,
    reason: "Целевое готовое изделие Livi Jewelry"
  };
}

function main() {
  Logger.log("==================================================================");
  Logger.log("💎 LIVI JEWELRY — СОВЕТНИК ПО МАСШТАБИРОВАНИЮ v2.0 (DIAMOND SHIELD)");
  Logger.log("   (Анализ реальных запросов на базе фильтров автопилота)");
  Logger.log("==================================================================");

  var reportDate = Utilities.formatDate(new Date(), "Asia/Almaty", "dd.MM.yyyy HH:mm");

  // 1. Загрузка активных ключевых слов в аккаунте
  var existingKeywords = {};
  try {
    var kwIter = AdsApp.keywords().withCondition("Status = ENABLED").get();
    while (kwIter.hasNext()) {
      var kw = kwIter.next();
      var cleanKw = kw.getText().toLowerCase().replace(/^["\[]|["\]]$/g, "").trim();
      existingKeywords[cleanKw] = true;
    }
    Logger.log("✓ Загружено активных ключевых слов в аккаунте: " + Object.keys(existingKeywords).length);
  } catch (kwErr) {
    Logger.log("[!] Ошибка чтения ключевых слов: " + kwErr);
  }

  // 2. Сбор статистики бюджета и эффективности
  var todayBudgetInfo = analyzeTodayBudget();
  var perfStats = analyzePeriodPerformance();
  var categorizedQueries = analyzeAndFilterQueries(existingKeywords);
  var trafficLight = evaluateTrafficLight(todayBudgetInfo, perfStats);

  // 3. Формирование чистого отчета
  var emailBody = buildCleanReport(reportDate, todayBudgetInfo, perfStats, categorizedQueries, trafficLight);
  Logger.log("\n" + emailBody);

  // 4. Отправка отчета на email
  if (CONFIG.SEND_EMAIL && CONFIG.ALERT_EMAIL) {
    var subject = trafficLight.icon + " Livi Advisor v2.0: " + trafficLight.title + " (Найдено самородков: " + categorizedQueries.totalGold + ") [" + reportDate + "]";
    try {
      MailApp.sendEmail(CONFIG.ALERT_EMAIL, subject, emailBody);
      Logger.log("\n📧 Отчет успешно отправлен на: " + CONFIG.ALERT_EMAIL);
    } catch (mailErr) {
      Logger.log("\n[!] Ошибка отправки email: " + mailErr);
    }
  }

  Logger.log("\n==================================================================");
  Logger.log("💎 Анализ советника v2.0 завершен успешно!");
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
  var groupsGold = {
    1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []
  };
  var junkList = [];
  var seen = {};
  var totalGold = 0;

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

      var evalRes = evaluateSearchTermForAdvisor(term);

      if (evalRes.isGold) {
        if (!existingKeywords[term]) {
          groupsGold[evalRes.groupNum].push({
            raw: rawTerm,
            exactTag: "[" + rawTerm + "]",
            clicks: clicks,
            ctr: ctr.toFixed(1),
            conv: conv,
            group: evalRes.group
          });
          totalGold++;
        }
      } else if (evalRes.isJunk) {
        junkList.push({
          raw: rawTerm,
          clicks: clicks,
          ctr: ctr.toFixed(1),
          reason: evalRes.reason
        });
      }
    }
  } catch (e) {
    Logger.log("[!] Ошибка анализа поисковых запросов: " + e);
  }

  // Сортировка мусора по кликам
  junkList.sort(function(a, b) {
    return b.clicks - a.clicks;
  });

  return {
    groupsGold: groupsGold,
    totalGold: totalGold,
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
  lines.push("  💎 LIVI JEWELRY — СОВЕТНИК ПО МАСШТАБИРОВАНИЮ v2.0 (DIAMOND SHIELD)");
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

  lines.push("💎 3. САМОРОДКИ РЕАЛЬНЫХ ПОКУПАТЕЛЕЙ (РАСПРЕДЕЛЕНЫ ПО 8 ГРУППАМ):");
  if (queries.totalGold === 0) {
    lines.push("   • За последние 7 дней новых целевых коммерческих запросов не появилось.");
    lines.push("   • Все целевые поисковые фразы уже присутствуют в ваших группах объявлений.");
  } else {
    lines.push("   Ниже представлены проверенные запросы реальных покупателей.");
    lines.push("   Скопируйте нужную строчку в соответствующую группу объявлений:");
    lines.push("   -------------------------------------------------");

    var groupNames = {
      1: "📁 ГРУППА 1: Комплекты и сеты (Sets)",
      2: "📁 ГРУППА 2: Колье из натурального жемчуга",
      3: "📁 ГРУППА 3: Колье и бусы из натуральных камней",
      4: "📁 ГРУППА 4: Серьги с натуральными камнями и жемчугом",
      5: "📁 ГРУППА 5: Чокеры из натуральных камней и жемчуга",
      6: "📁 ГРУППА 6: Сотуары и лариаты",
      7: "📁 ГРУППА 7: Барочный жемчуг и цепи",
      8: "📁 ГРУППА 8: Жемчуг Майорка"
    };

    for (var gNum = 1; gNum <= 8; gNum++) {
      var items = queries.groupsGold[gNum];
      if (items && items.length > 0) {
        lines.push("\n   " + groupNames[gNum] + ":");
        for (var k = 0; k < items.length; k++) {
          var it = items[k];
          var convText = it.conv > 0 ? ("🔥 ЗАКАЗОВ: " + it.conv + " | ") : "";
          lines.push("      " + it.exactTag + "  /* " + convText + it.clicks + " кл., CTR " + it.ctr + "% */");
        }
      }
    }
    lines.push("   -------------------------------------------------");
  }
  lines.push("");

  if (queries.junk.length > 0) {
    lines.push("🚫 4. ОТФИЛЬТРОВАННЫЙ МУСОР ЗА 7 ДНЕЙ (БЛОКИРУЕТСЯ АВТОПИЛОТОМ):");
    lines.push("   (Эти нецелевые запросы отсечены фильтрами автопилота и НЕ попали в рекомендации):");
    for (var j = 0; j < Math.min(queries.junk.length, 15); j++) {
      var junk = queries.junk[j];
      lines.push("   • «" + junk.raw + "» — " + junk.clicks + " кл. [" + junk.reason + "]");
    }
    lines.push("");
  }

  lines.push("══════════════════════════════════════════════════════════════════");
  lines.push("Советник работает строго в режиме рекомендаций (без авто-добавлений).");

  return lines.join("\n");
}
