#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
from collections import Counter

with open('big_report_terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

# Competitor brands currently in google_ads_autopilot.js v4.0
COMPETITOR_BRANDS = [
    re.compile(r'swarovski', re.I), re.compile(r'сваровск', re.I), re.compile(r'тиффани', re.I),
    re.compile(r'tiffany', re.I), re.compile(r'картье', re.I), re.compile(r'cartier', re.I),
    re.compile(r'messika', re.I), re.compile(r'мессика', re.I), re.compile(r'apm', re.I),
    re.compile(r'monaco', re.I), re.compile(r'апм', re.I), re.compile(r'монако', re.I),
    re.compile(r'aroush', re.I), re.compile(r'larosh', re.I), re.compile(r'laroush', re.I),
    re.compile(r'ляруш', re.I), re.compile(r'merhat', re.I), re.compile(r'мерхат', re.I),
    re.compile(r'tallys', re.I), re.compile(r'таллис', re.I), re.compile(r'sansi', re.I),
    re.compile(r'санси', re.I), re.compile(r'люченте', re.I), re.compile(r'luchente', re.I),
    re.compile(r'lucente', re.I), re.compile(r'казахювелир', re.I), re.compile(r'kazakhyuvelir', re.I),
    re.compile(r'казах\s*ювелир', re.I), re.compile(r'kazakh\s*yuvelir', re.I),
    re.compile(r'пандор', re.I), re.compile(r'pandora', re.I), re.compile(r'соколов', re.I),
    re.compile(r'sokolov', re.I), re.compile(r'санлайт', re.I), re.compile(r'sunlight', re.I),
    re.compile(r'ван\s*клиф', re.I), re.compile(r'van\s*cleef', re.I), re.compile(r'ванклив', re.I),
    re.compile(r'балауса', re.I), re.compile(r'balausa', re.I), re.compile(r'sakina', re.I),
    re.compile(r'сакина', re.I), re.compile(r'mone\b', re.I), re.compile(r'chopard', re.I),
    re.compile(r'шопард', re.I), re.compile(r'bvlgari', re.I), re.compile(r'bulgari', re.I),
    re.compile(r'булгари', re.I), re.compile(r'tous\b', re.I), re.compile(r'тоус', re.I),
    re.compile(r'адамас', re.I), re.compile(r'adamas', re.I), re.compile(r'miuz', re.I),
    re.compile(r'мюз', re.I), re.compile(r'сереброфф', re.I), re.compile(r'серебров', re.I),
    re.compile(r'serebroff', re.I), re.compile(r'дамиани', re.I), re.compile(r'damiani', re.I),
    re.compile(r'фрайвилле', re.I), re.compile(r'frey wille', re.I), re.compile(r'сблеском', re.I),
    re.compile(r'sbleskom', re.I), re.compile(r'луи витон', re.I), re.compile(r'louis vuitton', re.I),
    re.compile(r'шанель', re.I), re.compile(r'chanel', re.I), re.compile(r'эрмес', re.I),
    re.compile(r'hermes', re.I), re.compile(r'гуччи', re.I), re.compile(r'gucci', re.I),
    re.compile(r'диор', re.I), re.compile(r'dior', re.I), re.compile(r'tatirocks', re.I),
    re.compile(r'athena gaia', re.I), re.compile(r'miramira', re.I), re.compile(r'moonka', re.I),
    re.compile(r'sania\b', re.I), re.compile(r'sael\b', re.I), re.compile(r'rebecca\b', re.I),
    re.compile(r'tomiris', re.I), re.compile(r'shona\b', re.I), re.compile(r'siyera', re.I),
    re.compile(r'viennois', re.I), re.compile(r'maria tash', re.I), re.compile(r'kruger studios', re.I),
    re.compile(r'лалик', re.I), re.compile(r'lalique', re.I), re.compile(r'best wishes', re.I),
    re.compile(r'magic stones', re.I), re.compile(r'дерберг керн', re.I), re.compile(r'dyrberg', re.I),
    re.compile(r'deberquem', re.I), re.compile(r'канциан', re.I), re.compile(r'canzian', re.I),
    re.compile(r'грациелла', re.I), re.compile(r'graziella', re.I), re.compile(r'оксизян', re.I),
    re.compile(r'instyle', re.I), re.compile(r'сенсатори', re.I), re.compile(r'sensatori', re.I),
    re.compile(r'дионис', re.I), re.compile(r'dionis', re.I), re.compile(r'keklik', re.I),
    re.compile(r'дэвид юрман', re.I), re.compile(r'david yurman', re.I), re.compile(r'кубачи', re.I),
    re.compile(r'каратов', re.I), re.compile(r'karatov', re.I), re.compile(r'nature bijoux', re.I),
    re.compile(r'ouro', re.I), re.compile(r'ластория', re.I), re.compile(r'lastoria', re.I),
    re.compile(r'вива ла вика', re.I), re.compile(r'viva la vika', re.I), re.compile(r'tesoro', re.I),
    re.compile(r'meraly', re.I), re.compile(r'армат', re.I), re.compile(r'armat\b', re.I),
    re.compile(r'lurea', re.I), re.compile(r'луара', re.I), re.compile(r'luara', re.I),
    re.compile(r'kurshuni', re.I), re.compile(r'hefang', re.I), re.compile(r'серик рысбек', re.I),
    re.compile(r'serik rysbek', re.I), re.compile(r'ларентия', re.I), re.compile(r'laurentia', re.I),
    re.compile(r'гальяно', re.I), re.compile(r'galliano', re.I), re.compile(r'lady\s*collection', re.I),
    re.compile(r'леди коллекшн', re.I), re.compile(r'anka jewelry', re.I), re.compile(r'moon\s*(украшения|бижутерия)', re.I),
    re.compile(r'lucenta', re.I), re.compile(r'люцента', re.I), re.compile(r'roberto bravo', re.I),
    re.compile(r'роберто браво', re.I), re.compile(r'алтын\b', re.I), re.compile(r'altyn\b', re.I),
    re.compile(r'talisman\s*kz', re.I), re.compile(r'микимото', re.I), re.compile(r'mikimoto', re.I),
    re.compile(r'gotto jewelry', re.I), re.compile(r'pure jewelry', re.I), re.compile(r'soroka jewelry', re.I),
    re.compile(r'сорока\s*jewelry', re.I), re.compile(r'nomination', re.I), re.compile(r'номинэйшн', re.I),
    re.compile(r'лакост', re.I), re.compile(r'lacoste', re.I), re.compile(r'la roche', re.I),
    re.compile(r'jewelry bus', re.I), re.compile(r'minimal\s*silver', re.I), re.compile(r'браслет minimal', re.I)
]

SAFE_ROOTS = [
    re.compile(r'жемчу[гж]', re.I), re.compile(r'барочн', re.I), re.compile(r'майорк', re.I),
    re.compile(r'majorica', re.I), re.compile(r'pearl', re.I),
    re.compile(r'нефрит', re.I), re.compile(r'жадеит', re.I), re.compile(r'джедаит', re.I),
    re.compile(r'аметист', re.I), re.compile(r'малахит', re.I), re.compile(r'агат', re.I),
    re.compile(r'гранат', re.I), re.compile(r'кварц', re.I), re.compile(r'бирюз', re.I),
    re.compile(r'гематит', re.I), re.compile(r'хрустал', re.I), re.compile(r'лунн.*камен', re.I),
    re.compile(r'лунн', re.I), re.compile(r'тигров.*глаз', re.I), re.compile(r'тигров', re.I),
    re.compile(r'лазурит', re.I), re.compile(r'коралл', re.I), re.compile(r'яшм', re.I),
    re.compile(r'сердолик', re.I), re.compile(r'амазонит', re.I), re.compile(r'турмалин', re.I),
    re.compile(r'цитрин', re.I), re.compile(r'авантюрин', re.I), re.compile(r'флюорит', re.I),
    re.compile(r'перламутр', re.I), re.compile(r'оникс', re.I), re.compile(r'шпинел', re.I),
    re.compile(r'лабрадор', re.I), re.compile(r'чароит', re.I), re.compile(r'хризопраз', re.I),
    re.compile(r'змеевик', re.I), re.compile(r'топаз', re.I), re.compile(r'аквамарин', re.I),
    re.compile(r'берилл', re.I), re.compile(r'опал', re.I), re.compile(r'янтар', re.I),
    re.compile(r'родонит', re.I), re.compile(r'пирит', re.I), re.compile(r'содалит', re.I),
    re.compile(r'морганит', re.I), re.compile(r'родохрозит', re.I), re.compile(r'кунцит', re.I),
    re.compile(r'халцедон', re.I), re.compile(r'ларимар', re.I), re.compile(r'larimar', re.I),
    re.compile(r'празиолит', re.I), re.compile(r'хризолит', re.I), re.compile(r'хризоколл', re.I),
    re.compile(r'апатит', re.I), re.compile(r'танзанит', re.I), re.compile(r'варисцит', re.I),
    re.compile(r'александрит', re.I), re.compile(r'диоптаз', re.I), re.compile(r'арагонит', re.I),
    re.compile(r'aragonite', re.I), re.compile(r'обсидиан', re.I), re.compile(r'кошачий.*глаз', re.I),
    # Казахские термины и этно-стиль:
    re.compile(r'әшекей', re.I), re.compile(r'бұйым', re.I), re.compile(r'маржан', re.I),
    re.compile(r'меруерт', re.I), re.compile(r'алқа', re.I), re.compile(r'білезік', re.I),
    re.compile(r'сырға', re.I), re.compile(r'сырга', re.I), re.compile(r'тас\b', re.I),
    re.compile(r'тасы\b', re.I), re.compile(r'шашбау', re.I), re.compile(r'асыл тас', re.I),
    re.compile(r'этно', re.I), re.compile(r'этническ', re.I), re.compile(r'национальн.*украшен', re.I),
    re.compile(r'kazakh jewelry', re.I),
    # Авторские изделия и натуральные камни:
    re.compile(r'сотуар', re.I), re.compile(r'сатуар', re.I), re.compile(r'чокер', re.I),
    re.compile(r'камн', re.I), re.compile(r'камен', re.I), re.compile(r'бусин', re.I),
    re.compile(r'авторск.*украшен', re.I), re.compile(r'livi', re.I)
]

JUNK_PATTERNS = [
    # Литература, школьная программа, фейки клевер/гвоздь:
    re.compile(r'мопассан', re.I), re.compile(r'клевер', re.I), re.compile(r'гвоздь', re.I),
    # Производство, ювелирные мастерские, переплавка, гравировка (Livi продает готовые изделия):
    re.compile(r'на заказ', re.I), re.compile(r'изготовлен', re.I), re.compile(r'мастерск', re.I),
    re.compile(r'переплав', re.I), re.compile(r'лить[её]', re.I), re.compile(r'гравировк', re.I),
    re.compile(r'с надписью', re.I), re.compile(r'сделать на заказ', re.I),
    re.compile(r'ювелиры алматы', re.I), re.compile(r'ювелир алматы', re.I),
    re.compile(r'ювелир астана', re.I), re.compile(r'ювелиры астана', re.I),
    # Дети, девочки, мама:
    re.compile(r'для девочк', re.I), re.compile(r'девочке', re.I), re.compile(r'девочки', re.I),
    re.compile(r'для детей', re.I), re.compile(r'для мамы', re.I),
    # Другие типы украшений, которых нет у Livi:
    re.compile(r'брошь', re.I), re.compile(r'броши', re.I), re.compile(r'брошка', re.I),
    re.compile(r'фенечк', re.I), re.compile(r'кафф', re.I), re.compile(r'пусет', re.I),
    re.compile(r'свадебн', re.I), re.compile(r'галстук', re.I),
    # Строгий бан подарков:
    re.compile(r'(^|\s)подар', re.I), re.compile(r'что подарить', re.I), re.compile(r'что можно подарить', re.I),
    re.compile(r'день рожден', re.I), re.compile(r'\bд[рp]\b', re.I), re.compile(r'юбилей', re.I),
    re.compile(r'годовщин', re.I), re.compile(r'свадьб', re.I), re.compile(r'молодожен', re.I),
    re.compile(r'презент', re.I), re.compile(r'сюрприз', re.I), re.compile(r'8 марта', re.I),
    re.compile(r'новый год', re.I),
    # DIY, рукоделие, детали:
    re.compile(r'своими руками', re.I), re.compile(r'как сделать', re.I), re.compile(r'как сплести', re.I),
    re.compile(r'как собрать', re.I), re.compile(r'научиться делать', re.I), re.compile(r'схем', re.I),
    re.compile(r'как собрать', re.I), re.compile(r'научиться делать', re.I), re.compile(r'схем', re.I),
    re.compile(r'мастер класс', re.I), re.compile(r'мк\b', re.I), re.compile(r'бисероплетени', re.I),
    re.compile(r'бисер', re.I), re.compile(r'плетени', re.I), re.compile(r'вязани', re.I),
    re.compile(r'фурнитур', re.I), re.compile(r'застежк', re.I), re.compile(r'швенз', re.I),
    re.compile(r'штифт', re.I), re.compile(r'пины\b', re.I), re.compile(r'леск', re.I),
    re.compile(r'проволок', re.I), re.compile(r'тросик', re.I), re.compile(r'эпоксидн', re.I),
    re.compile(r'полимерн.*глин', re.I), re.compile(r'вышивк', re.I), re.compile(r'станок', re.I),
    re.compile(r'с буквой', re.I), re.compile(r'буква\s+[a-zа-я]', re.I), re.compile(r'снейк', re.I),
    # Чужие материалы и бижутерия:
    re.compile(r'стекл', re.I), re.compile(r'муранск', re.I), re.compile(r'murano', re.I),
    re.compile(r'стекляр', re.I), re.compile(r'шерст', re.I), re.compile(r'валян', re.I),
    re.compile(r'муассанит', re.I), re.compile(r'фианит', re.I), re.compile(r'циркон', re.I),
    re.compile(r'дерев', re.I), re.compile(r'пластик', re.I), re.compile(r'акрил', re.I),
    re.compile(r'силикон', re.I), re.compile(r'каучук', re.I), re.compile(r'веревочк', re.I),
    re.compile(r'на веревк', re.I), re.compile(r'шнурок', re.I), re.compile(r'xuping', re.I),
    re.compile(r'ксьюпинг', re.I), re.compile(r'медицинск', re.I), re.compile(r'лабрет', re.I),
    re.compile(r'пирсинг', re.I), re.compile(r'мело\b', re.I), re.compile(r'melo\b', re.I),
    re.compile(r'аква кварц', re.I), re.compile(r'сутажные', re.I), re.compile(r'минанкари', re.I),
    # Ломбарды, пробы, дешевый опт:
    re.compile(r'дешев', re.I), re.compile(r'недорог', re.I), re.compile(r'бесплатн', re.I),
    re.compile(r'даром', re.I), re.compile(r'ломбард', re.I), re.compile(r'скупк', re.I),
    re.compile(r'залог', re.I), re.compile(r'сдать', re.I), re.compile(r'проба', re.I),
    re.compile(r'585', re.I), re.compile(r'750', re.I), re.compile(r'925', re.I),
    re.compile(r'слит', re.I), re.compile(r'грамм', re.I), re.compile(r'алиэкспресс', re.I),
    re.compile(r'aliexpress', re.I), re.compile(r'temu', re.I), re.compile(r'тему', re.I),
    re.compile(r'shein', re.I), re.compile(r'шейн', re.I), re.compile(r'таобао', re.I),
    re.compile(r'taobao', re.I), re.compile(r'секонд', re.I), re.compile(r'барахолк', re.I),
    re.compile(r'конфискат', re.I), re.compile(r'б[\s/]?у\b', re.I), re.compile(r'оптом', re.I),
    re.compile(r'опт\b', re.I), re.compile(r'olx', re.I), re.compile(r'олх', re.I),
    re.compile(r'авито', re.I), re.compile(r'ярмарка мастеров', re.I), re.compile(r'etsy', re.I),
    # Заводское золото, кольца и драгкамни 1-й категории:
    re.compile(r'(^|\s)золот', re.I), re.compile(r'серебр', re.I), re.compile(r'платин', re.I),
    re.compile(r'бриллиант', re.I), re.compile(r'брилиан', re.I), re.compile(r'diamond', re.I),
    re.compile(r'изумруд', re.I), re.compile(r'рубин', re.I), re.compile(r'сапфир', re.I),
    re.compile(r'теннисн', re.I), re.compile(r'tennis.*bracelet', re.I),
    re.compile(r'кольц', re.I), re.compile(r'колечк', re.I), re.compile(r'перстен', re.I),
    re.compile(r'печатка', re.I), re.compile(r'обручальн', re.I), re.compile(r'помолвочн', re.I),
    re.compile(r'парные кольца', re.I), re.compile(r'на мизинец', re.I),
    # Одежда и части тела:
    re.compile(r'шапк', re.I), re.compile(r'рубашк', re.I), re.compile(r'плать', re.I),
    re.compile(r'кофт', re.I), re.compile(r'пальто', re.I), re.compile(r'юбк', re.I),
    re.compile(r'на ног', re.I), re.compile(r'через палец', re.I),
    # Инфо-мусор, определения, эзотерика, гороскопы:
    re.compile(r'что такое', re.I), re.compile(r'\bэто$', re.I), re.compile(r'\bэто\s', re.I),
    re.compile(r'как называется', re.I), re.compile(r'как носить', re.I), re.compile(r'с чем носить', re.I),
    re.compile(r'бывает ли', re.I), re.compile(r'отзывы', re.I), re.compile(r'бизнес', re.I),
    re.compile(r'для чего', re.I), re.compile(r'зачем', re.I),
    re.compile(r'ремонт', re.I), re.compile(r'пайк', re.I), re.compile(r'перетяжк', re.I),
    re.compile(r'чистк', re.I), re.compile(r'как почистить', re.I), re.compile(r'ультразвуков', re.I),
    re.compile(r'как отличить', re.I), re.compile(r'как проверить', re.I), re.compile(r'как определить', re.I),
    re.compile(r'как выгляд', re.I), re.compile(r'подделк', re.I), re.compile(r'кому подходит', re.I),
    re.compile(r'подходит ли', re.I), re.compile(r'свойств', re.I), re.compile(r'значени', re.I),
    re.compile(r'гороскоп', re.I), re.compile(r'знак.*зодиак', re.I), re.compile(r'магическ', re.I),
    re.compile(r'лечебн', re.I), re.compile(r'литотерапи', re.I), re.compile(r'талисман', re.I),
    re.compile(r'оберег', re.I), re.compile(r'амулет', re.I), re.compile(r'приворот', re.I),
    re.compile(r'заговор', re.I), re.compile(r'сонник', re.I), re.compile(r'к чему снится', re.I),
    re.compile(r'википеди', re.I), re.compile(r'месторожден', re.I), re.compile(r'твердость', re.I),
    re.compile(r'формула', re.I), re.compile(r'фото\b', re.I), re.compile(r'картинк', re.I),
    re.compile(r'обои', re.I), re.compile(r'скачать', re.I), re.compile(r'видео', re.I),
    re.compile(r'реферат', re.I), re.compile(r'ваканси', re.I), re.compile(r'резюме', re.I),
    re.compile(r'работа', re.I), re.compile(r'зарплат', re.I), re.compile(r'мужск', re.I),
    re.compile(r'для мужчин', re.I), re.compile(r'мужчин', re.I), re.compile(r'крестик', re.I),
    re.compile(r'четки', re.I), re.compile(r'тасбих', re.I), re.compile(r'часы', re.I),
    re.compile(r'зодиак', re.I), re.compile(r'овен', re.I), re.compile(r'телец', re.I),
    re.compile(r'тельц', re.I), re.compile(r'близнец', re.I), re.compile(r'рак\b', re.I),
    re.compile(r'рака', re.I), re.compile(r'лев\b', re.I), re.compile(r'льва', re.I),
    re.compile(r'дева', re.I), re.compile(r'весы', re.I), re.compile(r'весов', re.I),
    re.compile(r'скорпион', re.I), re.compile(r'стрелец', re.I), re.compile(r'козерог', re.I),
    re.compile(r'водолей', re.I), re.compile(r'рыбы', re.I),
    # Гео-туризм и чужие страны:
    re.compile(r'вьетнам', re.I), re.compile(r'шри ланк', re.I), re.compile(r'катар', re.I),
    re.compile(r'пхукет', re.I), re.compile(r'гоа\b', re.I), re.compile(r'туркестан', re.I),
    re.compile(r'египет', re.I), re.compile(r'тайланд', re.I), re.compile(r'бали\b', re.I),
    re.compile(r'milan', re.I), re.compile(r'милан', re.I), re.compile(r'греци', re.I),
    re.compile(r'япони', re.I), re.compile(r'украин', re.I), re.compile(r'дагестан', re.I),
    re.compile(r'узбекск', re.I), re.compile(r'турки', re.I), re.compile(r'турецк', re.I),
    re.compile(r'индийск', re.I),
    # Оффлайн-магазины:
    re.compile(r'ближайш', re.I), re.compile(r'поблизости', re.I), re.compile(r'рядом', re.I),
    # Чужие языковые термины:
    re.compile(r'tilla\b', re.I), re.compile(r'zirak', re.I), re.compile(r'детск', re.I),
    re.compile(r'фигурк.*детей', re.I)
]

def eval_term(term):
    lower = term.lower().strip()
    for b in COMPETITOR_BRANDS:
        if b.search(lower):
            return "COMPETITOR_BAN", b.pattern
    has_stone = any(s.search(lower) for s in SAFE_ROOTS)
    for j in JUNK_PATTERNS:
        if j.search(lower):
            is_fittings = (re.search(r'золот|серебр', lower)) and not re.search(r'ломбард|скупк|проба|585|750|925|кольц', lower)
            if has_stone and is_fittings:
                return "SAFE_FITTINGS", "Камень + фурнитура"
            return "JUNK_BAN", j.pattern
    if has_stone:
        return "SAFE_STONE", "Натуральный камень / жемчуг"
    return "UNKNOWN_GENERAL", "Общий запрос"

results = {
    "COMPETITOR_BAN": [],
    "JUNK_BAN": [],
    "SAFE_FITTINGS": [],
    "SAFE_STONE": [],
    "UNKNOWN_GENERAL": []
}

for t in terms:
    cat, reason = eval_term(t['term'])
    results[cat].append((t, reason))

# Print high-level overview
print("=== СВОДНЫЙ АУДИТ 5 955 ЗАПРОСОВ ===")
for k, v in results.items():
    clicks = sum(t[0]['clicks'] for t in v)
    cost = sum(t[0]['cost'] for t in v)
    impr = sum(t[0]['impr'] for t in v)
    print(f"{k}: {len(v)} запросов | {clicks} кликов | {impr} показов | расход: ${cost:.2f}")

# N-gram analysis of UNKNOWN_GENERAL
words_counter = Counter()
for item in results["UNKNOWN_GENERAL"]:
    t = item[0]
    words = re.findall(r'[а-яёa-z0-9]+', t['term'].lower())
    for w in words:
        if len(w) >= 3:
            words_counter[w] += t['clicks'] * 10 + t['impr']

# Save detailed report
with open('detailed_5955_audit.txt', 'w', encoding='utf-8') as out:
    out.write("=== ПОЛНЫЙ ДЕТАЛЬНЫЙ АУДИТ 5 955 ПОИСКОВЫХ ЗАПРОСОВ ===\n\n")
    for k, v in results.items():
        clicks = sum(t[0]['clicks'] for t in v)
        cost = sum(t[0]['cost'] for t in v)
        impr = sum(t[0]['impr'] for t in v)
        out.write(f"{k}: {len(v)} запросов | {clicks} кликов | {impr} показов | расход: ${cost:.2f}\n")

    out.write("\n======================================================\n")
    out.write("1. БРЕНДЫ-КОНКУРЕНТЫ (ТОП ПО РАСХОДУ И КЛИКАМ)\n")
    out.write("======================================================\n")
    for t, r in sorted(results["COMPETITOR_BAN"], key=lambda x: (x[0]['clicks'], x[0]['cost']), reverse=True)[:50]:
        out.write(f"[{t['clicks']} кл, {t['impr']} пок, ${t['cost']:.2f}, {t['campaign']}] \"{t['term']}\" (паттерн: {r})\n")

    out.write("\n======================================================\n")
    out.write("2. ЧИСТЫЙ МУСОР И ПОДАРКИ (ТОП ПО РАСХОДУ И КЛИКАМ)\n")
    out.write("======================================================\n")
    for t, r in sorted(results["JUNK_BAN"], key=lambda x: (x[0]['clicks'], x[0]['cost']), reverse=True)[:50]:
        out.write(f"[{t['clicks']} кл, {t['impr']} пок, ${t['cost']:.2f}, {t['campaign']}] \"{t['term']}\" (паттерн: {r})\n")

    out.write("\n======================================================\n")
    out.write("3. НАШИ ЦЕЛЕВЫЕ КАМНИ И ЖЕМЧУГ (САМЫЕ ПРИБЫЛЬНЫЕ ФРАЗЫ)\n")
    out.write("======================================================\n")
    for t, r in sorted(results["SAFE_STONE"], key=lambda x: (x[0]['clicks'], x[0]['cost']), reverse=True)[:50]:
        out.write(f"[{t['clicks']} кл, {t['impr']} пок, ${t['cost']:.2f}, {t['campaign']}] \"{t['term']}\"\n")

    out.write("\n======================================================\n")
    out.write("4. ЧАСТОТНЫЙ АНАЛИЗ СЛОВ В UNKNOWN_GENERAL (ПОИСК СКРЫТОГО МУСОРА)\n")
    out.write("======================================================\n")
    for w, score in words_counter.most_common(60):
        out.write(f"  Слово: '{w}' (скор: {score})\n")

    out.write("\n======================================================\n")
    out.write("5. ВСЕ ЗАПРОСЫ ИЗ UNKNOWN_GENERAL С КЛИКАМИ ИЛИ ПОКАЗАМИ >= 10\n")
    out.write("======================================================\n")
    for t, r in sorted(results["UNKNOWN_GENERAL"], key=lambda x: (x[0]['clicks'], x[0]['impr']), reverse=True):
        if t['clicks'] > 0 or t['impr'] >= 10:
            out.write(f"[{t['clicks']} кл, {t['impr']} пок, ${t['cost']:.2f}, {t['campaign']}] \"{t['term']}\"\n")

print("Audit written to detailed_5955_audit.txt successfully!")
