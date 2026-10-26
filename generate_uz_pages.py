#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Livi Jewelry — O‘zbekcha statik vitrina generatori (generate_uz_pages.py):
  - uz/index.html (Canonical: https://livijewelry.kz/uz/)
  - uz/shop.html  (Canonical: https://livijewelry.kz/uz/shop.html)
  - uz/product/prod_01.html ... uz/product/prod_58.html
  - uz/cart.html, uz/delivery.html, uz/terms.html, uz/privacy.html

O‘z ichiga oladi:
- O‘zbekiston (Toshkent, Samarqand, Buxoro va barcha hududlar) va xalqaro auditoriya uchun to‘liq SEO-lokalizatsiya
- To‘liq simmetrik hreflang bog‘lanishlari (ru-KZ, ru, kk-KZ, kk, uz-UZ, uz, x-default)
- Barcha 58 mahsulot uchun sifatli adabiy o‘zbekcha tarjima (lotin yozuvi)
- Schema.org Product, BreadcrumbList, FAQPage mikrobelgilari (KZT narxi saqlangan holda)
- O‘zbekiston uchun qulay yetkazib berish (CDEK, Qazpost) va to‘lov («Zolotaya Korona», WhatsApp orqali rekvizitlar)
- Statik HTML’da bo‘sh #catalogError himoyasi
"""

import html
import json
import os
import re
import time

SITE_URL = "https://livijewelry.kz"

def safe_write_text(file_path: str, content: str, retries: int = 5, delay: float = 0.15) -> None:
    """Windows tizimidagi fayl blokirovkalaridan himoyalangan holda matn yozish."""
    parent_dir = os.path.dirname(os.path.abspath(file_path))
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    for attempt in range(retries):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return
        except OSError:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise

GA_ID = "G-YFF2TR0N36"
AW_ID = "AW-16793974126"
AW_CONV_LABEL = "AW-16793974126/MuJ_CObHup8bEO7q_sc-"
FB_PIXEL_1 = "199604456030882"
FB_PIXEL_2 = "4185620171718327"
GOOGLE_VERIFICATION = "qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0"
FB_DOMAIN_VERIFICATION = "lrr1e3sbmseisnpm2nclqko8w1rfcw"

FEATURED_IDS = [
    "prod_01", "prod_02", "prod_06", "prod_07",
    "prod_10", "prod_11", "prod_16", "prod_17",
    "prod_19", "prod_20", "prod_23", "prod_24",
]

CATEGORY_NAMES_UZ = {
    "Necklaces": "Marjonlar",
    "Lariats": "Sotuarlar",
    "Chains": "Zanjirlar va chokerlar",
    "Bracelets": "Bilasuzuklar",
    "Earrings": "Ziraklar",
    "Sets": "To‘plamlar",
}

CATEGORY_HUB_LINKS = {
    "Necklaces": ("/uz/kolye-iz-zhemchuga.html", "Marvarid marjonlar"),
    "Lariats": ("/uz/sotuary-iz-zhemchuga.html", "Marvarid sotuarlar"),
    "Chains": ("/uz/chokery-iz-naturalnyh-kamney.html", "Toshli chokerlar va zanjirlar"),
    "Bracelets": ("/uz/braslety-iz-zhemchuga.html", "Marvarid bilasuzuklar"),
    "Earrings": ("/uz/sergi-iz-zhemchuga.html", "Marvarid ziraklar"),
    "Sets": ("/uz/komplekty-ukrasheniy.html", "Taqinchoqlar to‘plami"),
}

ALL_21_HUBS = [
    ("/uz/kolye-iz-zhemchuga.html", "Marvarid marjonlar"),
    ("/uz/braslety-iz-zhemchuga.html", "Marvarid bilasuzuklar"),
    ("/uz/sergi-iz-zhemchuga.html", "Marvarid ziraklar"),
    ("/uz/komplekty-ukrasheniy.html", "Taqinchoqlar to‘plami"),
    ("/uz/chokery-iz-naturalnyh-kamney.html", "Tabiiy toshlardan chokerlar"),
    ("/uz/sotuary-iz-zhemchuga.html", "Marvarid sotuarlar"),
    ("/uz/ukrasheniya-iz-barochnogo-zhemchuga.html", "Barokko marvarididan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-gematita.html", "Gematitdan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-malahita.html", "Malaxit va Nefritdan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-ametista.html", "Ametist va Flyuoritdan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-granata.html", "Granat va Aqiqdan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-rozovogo-kvarca.html", "Pushti kvarsdan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-biryuzy.html", "Feruzadan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-gornogo-hrustalya.html", "Tog‘ billuridan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-lunnogo-kamnya.html", "Oy toshi va Sadafdan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-zhemchuga-mayorka.html", "Mayorka marvarididan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-tigrovogo-glaza.html", "Yo‘lbars ko‘zi va Jadeitdan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-koralla-i-yashmy.html", "Marjon (korall) va Yashmadan taqinchoqlar"),
    ("/uz/ukrasheniya-iz-lazurita.html", "Lojuvard (lazurit) va Avantyurindan taqinchoqlar"),
    ("/uz/tsepi-s-barochnym-zhemchugom.html", "Barokko marvaridli zanjirlar"),
    ("/uz/koltsa-i-garnitury-iz-kamney.html", "Uzuklar va toshli garniturlar"),
]

UZ_TRANSLATIONS = {
    "prod_01": {
        "title": "Barokko marvaridli kulon bilan tabiiy marvariddan ko‘p qatorli marjon",
        "desc": "Yirik tabiiy barokko marvarididan yasalgan nafis osma kulonli ko‘p qatorli hashamatli marjon. Har bir marvarid donasi o‘zining betakror jilosi va yorqin nuri bilan ajralib turadi. Kundalik obrazlarga ham, bayramona kechalarga ham ajoyib mos tushadi. Bardoshli gipoallergen zargarlik furniturasi bilan jihozlangan.",
    },
    "prod_02": {
        "title": "Tabiiy marvarid va tog‘ billuridan yasalgan marjon (Premium)",
        "desc": "Premium toifadagi tabiiy marvarid, tiniq qirrali tog‘ billuri va yirik barokko marvarididan qo‘lda terilgan ko‘p qatlamli marjon. Yorug‘lik tushganda billur qirralari marvarid nurlari bilan uyg‘unlashib, betakror yorqinlik bag‘ishlaydi. Rodiy qoplamali mustahkam furnitura nozik teriga xavfsiz.",
    },
    "prod_03": {
        "title": "Mayorka marvarididan klassik marjon",
        "desc": "Qo‘lda naqshlangan keramika munchoqlari va nafis zargarlik qulfiga ega bo‘lgan Mayorka marvarididan klassik marjon. Mayin ipakdek silliq sadaf yuzasi va nozik keramika uyg‘unligi unga o‘ziga xos go‘zallik beradi. Rasmiy uchrashuvlar va bayramona tadbirlar uchun ajoyib tanlov. Livi Jewelry brendining sovg‘a qutisida taqdim etiladi.",
    },
    "prod_04": {
        "title": "Zarhal zanjir va barokko marvaridli bilasuzuk",
        "desc": "To‘plamda: Zarhal zanjir — 25 000 ₸, barokko marvaridli bilasuzuk — 15 000 ₸. To‘plamning to‘liq narxi — 40 000 ₸. Har bir buyumni alohida yoki to‘liq to‘plam sifatida xarid qilish mumkin. 18K sifatli zarhal qoplama va erkin shakldagi tabiiy barokko marvaridi har qanday kiyim bilan ajoyib uyg‘unlashadi.",
    },
    "prod_05": {
        "title": "Rodiy qoplangan zanjir va barokko marvaridli bilasuzuk",
        "desc": "To‘plamda: Rodiy qoplangan zanjir — 25 000 ₸, barokko marvaridli bilasuzuk — 15 000 ₸. To‘plamning to‘liq narxi — 40 000 ₸. Har bir buyumni alohida yoki to‘liq to‘plam ko‘rinishida xarid qilish mumkin. Kumushdek jiloli mustahkam rodiy qoplamasi yillar davomida o‘z yorqinligini yo‘qotmaydi.",
    },
    "prod_06": {
        "title": "Tabiiy malaxitdan yasalgan bilasuzuk",
        "desc": "Qirralangan tabiiy malaxit toshlaridan va dekorativ qulfdan qo‘lda terilgan nafis bilasuzuk. To‘q zumrad tusli tabiiy naqshlar har bir toshni betakror qiladi. Bilak o‘lchamingizga mos ravishda tayyorlab beriladi. Livi Jewelry baxmal xaltachasi va sovg‘a qutisida yetkaziladi.",
    },
    "prod_07": {
        "title": "Ametist va marvaridli to‘g‘nog‘ich, bilasuzuk, uzuk",
        "desc": "To‘plamda: Ametist va marvariddan to‘g‘nog‘ich — 40 000 ₸, bilasuzuk — 20 000 ₸, uzuk — 14 000 ₸. To‘plamning to‘liq narxi — 74 000 ₸. Binafsharang ametist va oppoq tabiiy marvaridning olijanob uyg‘unligi qirollarcha hashamat bag‘ishlaydi. Buyumlarni to‘liq to‘plam yoki alohida buyurtma qilish mumkin.",
    },
    "prod_08": {
        "title": "Tabiiy marvariddan yasalgan «Panjalar» mualliflik marjoni",
        "desc": "Katta hajmli to‘qilishi va boy fakturaga ega tabiiy yetishtirilgan marvariddan yasalgan mualliflik marjoni. Yirik marvarid donalari bo‘yinga yoqimli tushib turadi. Mustahkam gipoallergen qulf va bepul sovg‘a qadoqlari bilan taqdim etiladi.",
    },
    "prod_09": {
        "title": "Tabiiy avantyurindan marjon va ziraklar",
        "desc": "To‘plamda: Avantyurin marjoni — 34 000 ₸, ziraklar — 10 000 ₸. To‘plamning to‘liq narxi — 44 000 ₸. Ichidan porlab turuvchi mayda yaltiroq zarrachalarga ega to‘q ko‘k avantyurin tungi yulduzli osmonni eslatadi. Buyumlarni alohida yoki to‘plam holida xarid qilishingiz mumkin.",
    },
    "prod_10": {
        "title": "Aqiq va granatdan marjon hamda uzuk",
        "desc": "To‘plamda: Aqiq va granatdan marjon — 36 000 ₸, uzuk — 12 000 ₸. To‘plamning to‘liq narxi — 48 000 ₸. To‘q may tusli qirrali granat va baxmalsimon qora aqiq toshlarining kontrasti jozibador ko‘rinish hosil qiladi. Uzuk o‘lchami va marjon uzunligi buyurtmaga binoan sozlanadi.",
    },
    "prod_11": {
        "title": "Ametist va pushti kvarsdan marjon, ametist ziraklar",
        "desc": "To‘plamda: Ametist va pushti kvars marjoni — 45 000 ₸, ametist ziraklar — 16 000 ₸. To‘plamning to‘liq narxi — 61 000 ₸. Mayin lavanda tusli ametist va shaffof pushti kvars ranglari ayollik nafosatini namoyon etadi. Ziraklarni alohida xarid qilish ham mumkin.",
    },
    "prod_12": {
        "title": "Jadeit va yo‘lbars ko‘zidan marjon va ziraklar",
        "desc": "To‘plamda: Jadeit va yo‘lbars ko‘zidan marjon — 36 000 ₸, ziraklar — 16 000 ₸. To‘plamning to‘liq narxi — 52 000 ₸. Ipaksimon tovlanuvchi yo‘lbars ko‘zi va olijanob yashil jadeit toshi kuch-quvvat va omad timsoli sanaladi. Alohida yoki to‘plamda sotiladi.",
    },
    "prod_13": {
        "title": "Mayorka marvarididan marjon va ziraklar",
        "desc": "To‘plamda: Mayorka marvarididan marjon — 35 000 ₸, ziraklar — 10 000 ₸. To‘plamning to‘liq narxi — 45 000 ₸. Oyna kabi silliq yuzali organik Mayorka marvaridi har qanday tantanali tadbirda beqiyos ko‘rinadi. Sifatli oltin suvi yuritilgan furniturasi allergiya chaqirmaydi.",
    },
    "prod_14": {
        "title": "Marjon (korall) va yashmadan marjon, bilasuzuk, ziraklar",
        "desc": "To‘plamda: Marjon va yashma marjoni — 40 000 ₸, bilasuzuk — 10 000 ₸, ziraklar — 10 000 ₸. To‘plamning to‘liq narxi — 60 000 ₸. Issiq terrakota tusli tabiiy marjon va naqshdor tabiiy yashma etnik-klassik uslubni sevuvchilar uchun ideal tanlovdir.",
    },
    "prod_15": {
        "title": "Pushti kvars va marvariddan marjon hamda ziraklar",
        "desc": "To‘plamda: Pushti kvars va marvariddan marjon — 40 000 ₸, ziraklar — 16 000 ₸. To‘plamning to‘liq narxi — 56 000 ₸. Nozik pastel pushti kvars va tabiiy chuchuk suv marvaridi romantik va mayin qiyofa yaratadi. Buyumlarni alohida ham olish mumkin.",
    },
    "prod_16": {
        "title": "Tabiiy feruzadan marjon va ziraklar",
        "desc": "To‘plamda: Tabiiy feruzadan marjon — 35 000 ₸, ziraklar — 15 000 ₸. To‘plamning to‘liq narxi — 50 000 ₸. Moviy osmon tusli tabiiy feruzaning tabiiy to‘qimasi bahor va yoz faslidagi liboslarga juda mos keladi.",
    },
    "prod_17": {
        "title": "Tabiiy aqiq va granatdan yasalgan sotuar-taqinchoq",
        "desc": "Tabiiy qora aqiq va qirrali yoqutrang granat toshlaridan qo‘lda terilgan nafis uzun sotuar-transformer. Chiroyli ipak popuk bilan bezatilgan. Buyumni uzun holda yoki bo‘yinga ikki qavat qilib o‘rab taqish mumkin.",
    },
    "prod_18": {
        "title": "To‘g‘nog‘ich, bilasuzuk, ziraklar, uzuk (buyurtma asosida)",
        "desc": "To‘plamda: To‘g‘nog‘ich — 30 000 ₸, bilasuzuk — 16 000 ₸, ziraklar — 14 000 ₸, uzuk — 14 000 ₸. To‘liq narxi — 74 000 ₸ (buyurtma asosida). Tabiiy marvarid va minerallardan usta tomonidan maxsus buyurtma bilan yasaladigan lyuks toifadagi to‘liq to‘plam.",
    },
    "prod_19": {
        "title": "Yo‘lbars ko‘zi va gematitdan yasalgan marjon",
        "desc": "Yo‘lbars ko‘zining iliq tillarang nurlari va qirrali grafit gematit toshlaridan terilgan zamonaviy geometrik marjon. Klassik kostyumlar bilan ham, kundalik ko‘ylaklar bilan ham ajoyib uyg‘unlashadi.",
    },
    "prod_20": {
        "title": "Tabiiy flyuorit va zirkonlardan yasalgan marjon",
        "desc": "Yalpiz-lavanda rangli shaffof tabiiy flyuorit va yarqiragan zirkon donalaridan ishlangan sehrli nozik marjon. Yorug‘likda toshlarning rangi tovlanib, e’tiborni o‘ziga tortadi. Sovg‘a uchun juda mos.",
    },
    "prod_21": {
        "title": "«Qulupnaycha» va marvaridli pushti kvars marjonlari",
        "desc": "To‘plamda: «Qulupnaycha» marjoni — 34 000 ₸, pushti kvars va marvaridli marjon — 40 000 ₸. To‘plamning to‘liq narxi — 74 000 ₸. Ikki mustaqil marjonni alohida yoki birgalikda zamonaviy urfdagi qavatli uslubda taqish mumkin.",
    },
    "prod_22": {
        "title": "Tabiiy marvaridli «Granj» mualliflik marjoni",
        "desc": "Katta zanjir va nozik tabiiy barokko marvaridining qarama-qarshi uyg‘unligidan tug‘ilgan zamonaviy granj uslubidagi marjon. Erkin va dadil obrazlar yaratish uchun ajoyib dizaynerlik yechimi.",
    },
    "prod_23": {
        "title": "Tabiiy granatdan yasalgan marjon",
        "desc": "To‘q sharob rangli qirrali tabiiy granat toshlaridan (pirop, almandin) qo‘lda terilgan abadiy klassik marjon. Har bir qirrasi yorug‘likda yoqutdek porlaydi. Bo‘yin o‘lchamingizga moslab beriladi.",
    },
    "prod_24": {
        "title": "Tabiiy marvarid va lojuvarddan (lazurit) marjon",
        "desc": "Tillarang pirit zarrachalariga ega to‘q moviy tabiiy lojuvard va oppoq tabiiy marvarid uyg‘unligi. Chuqur va tantanali ko‘rinish baxsh etadi. Yilning istalgan mavsumida uslubingizni yorqin ko‘rsatadi.",
    },
    "prod_25": {
        "title": "Granat va tabiiy marvariddan yasalgan marjon",
        "desc": "Qirrali bordo-yoqut tusli tabiiy granat va oq marvariddan qo‘lda terilgan nafis ikki qavatli marjon. Ayollarga xos mayinlik va noziklikni o‘zida mujassam etadi.",
    },
    "prod_26": {
        "title": "Feruzali marjon va ziraklar",
        "desc": "To‘plamda: Feruzali marjon — 35 000 ₸, ziraklar — 15 000 ₸. To‘plamning to‘liq narxi — 50 000 ₸. Moviy feruza va yengil zargarlik furniturasidan terilgan ajoyib yozgi to‘plam.",
    },
    "prod_27": {
        "title": "Nefrit va gematitdan marjon hamda ziraklar",
        "desc": "To‘plamda: Nefrit va gematit marjoni — 45 000 ₸, ziraklar — 16 000 ₸. To‘plamning to‘liq narxi — 61 000 ₸. Zaytun-yashil tabiiy asil nefrit va oyna kabi jiloli grafit gematitning uyg‘unligi chuqur xotirjamlik bag‘ishlaydi.",
    },
    "prod_28": {
        "title": "Tabiiy feruzadan marjon, bilasuzuk, ziraklar, uzuk",
        "desc": "To‘plamda: Feruzadan marjon — 40 000 ₸, bilasuzuk — 23 000 ₸, ziraklar — 14 000 ₸, uzuk — 14 000 ₸. To‘liq narxi — 91 000 ₸. Saralangan tabiiy feruzadan yasalgan to‘liq lyuks to‘plam. Har bir buyumni alohida xarid qilish mumkin.",
    },
    "prod_29": {
        "title": "Gematitdan yasalgan marjon",
        "desc": "Qo‘lda yasalgan mualliflik taqinchoqlari: Gematit marjoni. Tabiiy yaltiroq jilosi va jozibali grafit tusiga ega saralangan tabiiy gematit minerallaridan yasalgan. Gipoallergen furniturasi qoraymaydi. Sovg‘a qutisi va baxmal xaltacha bepul qo‘shiladi.",
    },
    "prod_30": {
        "title": "Tabiiy toshlardan marjon va bilasuzuk",
        "desc": "To‘plamda: Tabiiy toshlardan marjon — 26 000 ₸, bilasuzuk — 12 000 ₸. To‘plamning to‘liq narxi — 38 000 ₸. Har bir buyumni alohida yoki to‘liq to‘plam sifatida sotib olish mumkin. Saralangan tabiiy toshlardan qo‘lda terilgan dizaynerlik to‘plami. Gipoallergen furnitura va sovg‘a qadoqlari bilan birga keladi.",
    },
    "prod_31": {
        "title": "Yashmadan marjon va bilasuzuk",
        "desc": "To‘plamda: Yashma marjoni — 34 000 ₸, bilasuzuk — 12 000 ₸. To‘plamning to‘liq narxi — 46 000 ₸. Buyumlarni alohida yoki to‘liq to‘plam sifatida xarid qilish mumkin. Takrorlanmas iliq tabiiy naqshga ega tabiiy yashma toshidan usta tomonidan qo‘lda terilgan chiroyli to‘plam.",
    },
    "prod_32": {
        "title": "Tabiiy toshlar to‘plami: marjon va bilasuzuk",
        "desc": "To‘plamda: Tabiiy toshlardan marjon — 26 000 ₸, bilasuzuk — 12 000 ₸. To‘plamning to‘liq narxi — 38 000 ₸. Har bir buyumni alohida yoki to‘liq to‘plam ko‘rinishida buyurtma berish mumkin. Yuqori sifatli gipoallergen furnitura va brend sovg‘a qutisi bepul taqdim etiladi.",
    },
    "prod_33": {
        "title": "Tabiiy toshlardan marjon, bilasuzuk va ziraklar",
        "desc": "To‘plamda: Tabiiy toshlardan marjon — 26 000 ₸, bilasuzuk — 12 000 ₸, ziraklar — 10 000 ₸. To‘plamning to‘liq narxi — 48 000 ₸. Har bir buyumni alohida yoki uchlik to‘plam sifatida olish mumkin. Tabiiy toshlarning nafis uyg‘unligi va sifatli zargarlik furniturasi yillar davomida jilosini yo‘qotmaydi.",
    },
    "prod_34": {
        "title": "Dizaynerlik ziraklari",
        "desc": "Qo‘lda yasalgan mualliflik zargarlik ziraklari. Nozik va yengil konstruksiya quloqda juda qulay o‘tiradi. Sifatli gipoallergen furniturasi uzoq muddat o‘z yorqinligini saqlaydi. Firmaning chiroyli sovg‘a qutisida taqdim etiladi.",
    },
    "prod_35": {
        "title": "Akva kvarsdan yasalgan ziraklar",
        "desc": "Moviy suv tusli akva kvars toshidan yasalgan nafis mualliflik ziraklari. Tiniq moviy jilolari bilan yuzga mayin tarovat bag‘ishlaydi. Gipoallergen qulfi nozik quloqlar uchun mutlaqo xavfsizdir.",
    },
    "prod_36": {
        "title": "Dalmatin yashmasidan ziraklar",
        "desc": "Noyob dog‘li dalmatin yashmasidan qo‘lda yasalgan mualliflik ziraklari. Qora va krem tusli tabiiy tosh naqshi har qanday zamonaviy kiyim bilan ajoyib uyg‘unlashadi. Yengil va qulay taqiladi.",
    },
    "prod_37": {
        "title": "Tabiiy jadeitdan ziraklar",
        "desc": "Yashil tabiiy jadeit toshlaridan qo‘lda ishlangan nafis ziraklar. Jadeit ezgulik va osoyishtalik baxsh etuvchi asil tosh hisoblanadi. Oltin yoki rodiy rangli gipoallergen furnitura bilan jihozlangan.",
    },
    "prod_38": {
        "title": "Mayorka marvarididan ziraklar",
        "desc": "Silliq va jilodor organik Mayorka marvarididan qo‘lda yasalgan hashamatli ziraklar. O‘zining ipakdek sadaf porlashi bilan bayramona ko‘rinish baxsh etadi. Qulay va ishonchli zargarlik qulfiga ega.",
    },
    "prod_39": {
        "title": "Oy va yulduz ziraklari",
        "desc": "Koinot sirlaridan ilhomlangan «Oy va yulduz» mualliflik ziraklari. Har bir zirak nafis detallar bilan bezatilgan bo‘lib, yoshlik va noziklikni ifodalaydi. Sovg‘a uchun ideal tanlov.",
    },
    "prod_40": {
        "title": "Puseta ziraklar",
        "desc": "Klassik uslubdagi ixcham va nafis puseta ziraklar. Har kuni taqish uchun juda qulay, quloqni og‘ritmaydi. Yuqori sifatli gipoallergen qotishmadan yasalgan, sovg‘a qutisiga solib beriladi.",
    },
    "prod_41": {
        "title": "Yurakcha shaklidagi puseta ziraklar",
        "desc": "Romantik yurakcha shaklidagi mayin puseta ziraklar. Har qanday yoshdagi ayollar uchun nafis va sevimli taqinchoqqa aylanadi. Mustahkam qulfi zirakni ishonchli ushlab turadi.",
    },
    "prod_42": {
        "title": "Mayorka marvaridli nafis ziraklar",
        "desc": "Mayorka marvaridi bilan bezatilgan klassik zargarlik ziraklari. Yengil va jilodor, kundalik kiyimlar va tantanalar bilan birdek go‘zal uyg‘unlashadi. Gipoallergen furniturasi teriga xavfsiz.",
    },
    "prod_43": {
        "title": "Swarovski yurakchali ziraklar",
        "desc": "Yorqin chaqnoq Swarovski kristall yurakchalari bilan bezatilgan nafis ziraklar. Yorug‘likda rang-barang nurlar sochib, barchaning e’tiborini tortadi. Bayramlar va sovg‘alar uchun ajoyib yechim.",
    },
    "prod_44": {
        "title": "Yo‘lbars ko‘zi toshli ziraklar",
        "desc": "Ipaksimon tillarang-jigarrang jiloli tabiiy yo‘lbars ko‘zi toshlaridan yasalgan mualliflik ziraklari. Quloqda yengil turadi va boy tusli jilosi bilan libosingizga ko‘rk qo‘shadi.",
    },
    "prod_45": {
        "title": "Yurakcha ziraklar",
        "desc": "Nozik yurakcha shaklidagi nafis mualliflik ziraklari. Ayollik nafosati va mehrini ifodalovchi yoqimli aksessuar. Firmaning maxsus sovg‘a qutisida taqdim etiladi.",
    },
    "prod_46": {
        "title": "Tabiiy toshli yechiladigan yurakchali ziraklar",
        "desc": "Tabiiy toshlardan yasalgan yechib olinadigan yurakchalarga ega universal zirak-transformerlar. Zirakni oddiy halqa yoki toshli osma bilan turli ko‘rinishda taqishingiz mumkin.",
    },
    "prod_47": {
        "title": "Tabiiy feruzadan sotuar",
        "desc": "Ochiq osmon tusli tabiiy feruza toshlaridan yasalgan uzun hashamatli sotuar. Bo‘yinga bir necha qator qilib yoki bo‘sh tashlab taqishga mo‘ljallangan. Etnik va zamonaviy uslub uyg‘unligi.",
    },
    "prod_48": {
        "title": "Yo‘lbars ko‘zidan sotuar",
        "desc": "Ipakdek tovlanuvchi tabiiy yo‘lbars ko‘zi minerallaridan qo‘lda terilgan uzun sotuar. Qulay uzunligi tufayli turli xil kiyimlar bilan tajriba qilish imkonini beradi.",
    },
    "prod_49": {
        "title": "Granat va marvariddan chokerlar",
        "desc": "To‘q qizil qirrali granat va oppoq tabiiy marvariddan yasalgan nafis qisqa chokerlar. Bo‘yin chizig‘ini nozik ko‘rsatadi va qulay zargarlik zanjiri bilan sozlanadi.",
    },
    "prod_50": {
        "title": "Yo‘lbars ko‘zidan marjon va bilasuzuk",
        "desc": "To‘plamda: Yo‘lbars ko‘zi marjoni — 20 000 ₸, bilasuzuk — 12 000 ₸. To‘plamning to‘liq narxi — 32 000 ₸. Har bir buyumni alohida yoki to‘liq to‘plam sifatida xarid qilish mumkin. Oltin-jigarrang jiloli tabiiy yo‘lbars ko‘zi toshlaridan qo‘lda ishlangan ajoyib to‘plam.",
    },
    "prod_51": {
        "title": "Dalmatin yashmasi va aqiqdan sotuar",
        "desc": "Tabiiy dalmatin yashmasi va qora aqiq toshlaridan yasalgan zamonaviy uzun sotuar. Kontrastli ranglar kombinatsiyasi kiyimingizga o‘ziga xos uslub va joziba bag‘ishlaydi.",
    },
    "prod_52": {
        "title": "Gematit va Mayorka marvarididan marjon",
        "desc": "Kumush tusli qirrali gematit va oq silliq Mayorka marvaridining jozibador uyg‘unligi. Zamonaviy qat’iy qiyofa va nozik marvarid jilosining ideal balansi.",
    },
    "prod_53": {
        "title": "Gematit va zirkonlardan marjon, bilasuzuk",
        "desc": "To‘plamda: Gematit va zirkonli marjon — 36 000 ₸, bilasuzuk — 15 000 ₸. To‘plamning to‘liq narxi — 51 000 ₸. Har bir buyumni alohida yoki to‘liq to‘plamda olish mumkin. Porloq zirkonlar va metall jiloli gematit toshlarining ajoyib to‘plami.",
    },
    "prod_54": {
        "title": "Qora rangdagi «Panjalar» marjoni",
        "desc": "Qora rangdagi eksklyuziv «Panjalar» mualliflik marjoni. Qora toshlarning sirli jilosi va noodatiy to‘qilishi kechki va ziyofat obrazlari uchun mukammal yechimdir.",
    },
    "prod_55": {
        "title": "Zargarlik chex shishasidan «Panjalar» marjoni",
        "desc": "Qirrali zargarlik chex billur shishasidan yasalgan yorqin «Panjalar» marjoni. Har bir billur elementi yorug‘likni ajoyib sindirib, olmosdek jilo sochadi.",
    },
    "prod_56": {
        "title": "Granat va chex shishasidan marjon",
        "desc": "Tabiiy sharob rangli granat va qirrali chex shishasidan qo‘lda terilgan nafis marjon. Boy qizil tusli porlash har qanday bayramona tadbirda diqqat markazida bo‘lishingizni ta’minlaydi.",
    },
    "prod_57": {
        "title": "Mayorka marvaridi va zargarlik shishasidan marjon",
        "desc": "Mayorka marvaridi va yaltiroq zargarlik shishasi birikmasidan ishlangan nozik marjon. Yengil va havodor tuzilishi bo‘yinda mayin turadi.",
    },
    "prod_58": {
        "title": "Tabiiy toshli yechiladigan yurakchali zirak-transformerlar",
        "desc": "Tabiiy toshlardan yasalgan yechib olinadigan yurakchalarga ega ko‘p funksiyali zirak-transformerlar. Qulay va mustahkam qulfli halqalarni alohida taqish yoki toshli yurakcha bilan boyitish mumkin.",
    },
}

MATERIAL_MAP_UZ = {
    "Натуральный жемчуг": "Tabiiy marvarid",
    "Барочный жемчуг": "Barokko marvaridi",
    "Натуральный барочный жемчуг": "Tabiiy barokko marvaridi",
    "Жемчуг Майорка": "Mayorka marvaridi",
    "Горный хрусталь": "Tog‘ billuri",
    "Керамические бусины": "Keramika munchoqlari",
    "Ювелирный сплав": "Gipoallergen zargarlik qotishmasi",
    "Позолота": "18K zarhal qoplama",
    "Родированная фурнитура": "Rodiy bilan qoplangan furnitura",
    "Натуральный малахит": "Tabiiy malaxit",
    "Натуральный аметист": "Tabiiy ametist",
    "Натуральный авантюрин": "Tabiiy avantyurin",
    "Натуральный агат": "Tabiiy aqiq",
    "Натуральный гранат": "Tabiiy granat (yoqut)",
    "Розовый кварц": "Pushti kvars",
    "Натуральный жадеит": "Tabiiy jadeit",
    "Тигровый глаз": "Yo‘lbars ko‘zi",
    "Натуральный коралл": "Tabiiy marjon (korall)",
    "Яшма": "Tabiiy yashma",
    "Натуральная бирюза": "Tabiiy feruza",
    "Натуральные камни": "Tabiiy toshlar",
    "Гематит": "Gematit",
    "Натуральный флюорит": "Tabiiy flyuorit",
    "Цирконы": "Zargarlik zirkonlari",
    "Натуральный лазурит": "Tabiiy lojuvard (lazurit)",
    "Натуральный нефрит": "Tabiiy nefrit",
}

TYPE_UZ_MAP = {
    "Многорядное колье с акцентной подвеской": "Aktsentli kulonli ko‘p qatorli marjon",
    "Многослойное премиальное колье": "Premium ko‘p qatlamli marjon",
    "Классическое колье из натурального камня": "Tabiiy toshdan klassik marjon",
    "Ювелирный комплект (цепь + браслет)": "Zargarlik to‘plami (zanjir + bilasuzuk)",
    "Ювелирный комплект (родированная цепь + браслет)": "Zargarlik to‘plami (rodiy qoplangan zanjir + bilasuzuk)",
    "Многорядный браслет из натуральных камней": "Tabiiy toshlardan ko‘p qatorli bilasuzuk",
    "Комплект украшений (булавка-брошь + браслет + кольцо)": "Zargarlik to‘plami (to‘g‘nog‘ich-brosh + bilasuzuk + uzuk)",
    "Дизайнерское колье ручной работы": "Qo‘lda yasalgan dizaynerlik marjoni",
    "Ювелирный комплект (колье + серьги)": "Zargarlik to‘plami (marjon + ziraklar)",
    "Комплект украшений (колье + серьги)": "Zargarlik to‘plami (marjon + ziraklar)",
    "Ювелирный комплект (колье + кольцо)": "Zargarlik to‘plami (marjon + uzuk)",
    "Комплект украшений (колье + браслет + серьги)": "Zargarlik to‘plami (marjon + bilasuzuk + ziraklar)",
    "Комплект украшений из натуральной бирюзы": "Tabiiy feruzadan zargarlik to‘plami",
    "Украшение-сотуар трансформер с кистью": "Popukli sotuar-transformer taqinchog‘i",
    "Полный комплект украшений из 4 предметов (под заказ)": "4 buyumdan iborat to‘liq zargarlik to‘plami (buyurtma asosida)",
    "Полный ювелирный комплект из 4 предметов (под заказ)": "4 buyumdan iborat to‘liq zargarlik to‘plami (buyurtma asosida)",
    "Премиальный ювелирный комплект из 4 предметов": "4 buyumdan iborat premium zargarlik to‘plami",
    "Авторское колье ручной работы": "Qo‘lda yasalgan mualliflik marjoni",
    "Утонченное колье-чокер": "Nafis choker-marjon",
    "Многослойный ювелирный сет из 2 колье": "2 marjondan iborat ko‘p qatlamli zargarlik seti",
    "Дизайнерское колье в стиле гранж": "Granj uslubidagi dizaynerlik marjoni",
    "Контрастное дизайнерское колье": "Kontrastli dizaynerlik marjoni",
    "Авторское контрастное колье": "Mualliflik kontrast marjoni",
    "Многослойное дизайнерское колье": "Ko‘p qatlamli dizaynerlik marjoni",
    "Премиальный комплект украшений из 4 предметов": "4 buyumdan iborat premium zargarlik to‘plami",
    "Дизайнерские серьги ручной работы": "Qo‘lda yasalgan dizaynerlik ziraklari",
    "Серьги-пусеты ручной работы": "Qo‘lda yasalgan puseta ziraklari",
    "Украшение-сотуар ручной работы": "Qo‘lda yasalgan sotuar taqinchog‘i",
    "Комплект украшений ручной работы": "Qo‘lda yasalgan taqinchoqlar to‘plami",
}

STONES_DETAIL_UZ_MAP = {
    "prod_01": "Chuchuk suvning saralangan tabiiy marvaridi (dumaloq 6–7 mm), aktsentli yirik barokko marvaridi 18–22 mm",
    "prod_02": "Yuqori toifadagi tabiiy marvarid, qirrali shaffof tog‘ billuri, yirik barokko marvaridi",
    "prod_03": "Ko‘p qatlamli sadaf qoplamali Mayorka organik marvaridi, qo‘lda bezatilgan keramika munchoqlari",
    "prod_04": "Kamalak jiloli erkin shakldagi yirik tabiiy barokko marvaridi",
    "prod_05": "Sadaf yaltiroqligiga ega tomchi shaklidagi tabiiy yetishtirilgan barokko marvaridi",
    "prod_06": "Yorqin tabiiy naqshli saralangan tabiiy malaxit, zarhal zargarlik ajratgichlari",
    "prod_07": "Lavanda va to‘q binafsha tusli tabiiy ametist, tabiiy yetishtirilgan marvarid",
    "prod_08": "Qalin sadafli diametri 8–9 mm saralangan tabiiy yetishtirilgan marvarid",
    "prod_09": "Ichidan yaltirab turuvchi tabiiy avantyurin, zarhal aktsent munchoqlari",
    "prod_10": "Sharob-yoqut tusli qirrali tabiiy granat, baxmalsimon qora tabiiy aqiq",
    "prod_11": "Zargarlik qirralangan tabiiy lavanda ametisti, shaffof nozik pushti kvars",
    "prod_12": "Ipakdek tillarang-jigarrang tovlanuvchi tabiiy yo‘lbars ko‘zi, zumrad-yashil tabiiy jadeit",
    "prod_13": "Oyna kabi ipak jiloli yuqori sifatli Mayorka organik marvaridi, zarhal qismlar",
    "prod_14": "Issiq terrakota tusli tabiiy marjon (korall), takrorlanmas naqshli tabiiy yashma",
    "prod_15": "Pastel tabiiy nozik pushti kvars, saralangan yetishtirilgan chuchuk suv marvaridi",
    "prod_16": "Tabiiy to‘qimali osmondek moviy tabiiy feruza",
    "prod_17": "To‘q sharob tusli qirrali tabiiy granat, chuqur qora aqiq, ipak popuk",
    "prod_18": "Saralangan tabiiy yetishtirilgan marvarid, tabiiy yarim qimmatbaho toshlar",
    "prod_19": "Oltin-qahrabo jiloli tabiiy yo‘lbars ko‘zi, qirrali grafit gematit",
    "prod_20": "Yalpiz-lavanda tusli tabiiy shaffof flyuorit, yorqin zargarlik zirkonlari",
    "prod_21": "Saralangan sifatli chuchuk suv marvaridi, nafis pushti kvars, qulupnaycha shaklidagi aktsentlar",
    "prod_22": "Kamalak jiloli yirik tabiiy yetishtirilgan barokko marvaridi",
    "prod_23": "To‘q chuqur sharob tusli saralangan tabiiy qirrali granat (pirop va almandin)",
    "prod_24": "Oltin pirit zarrachalariga ega ultramarin tabiiy lojuvard, oppoq tabiiy marvarid",
    "prod_25": "Qirrali sharob-bordo tusli tabiiy granat, tabiiy chuchuk suv oq marvaridi",
    "prod_26": "Tabiiy tosh tuzilishiga ega moviy tabiiy feruza",
    "prod_27": "Zaytun-zumrad tusli tabiiy asil nefrit, qirrali oyna kabi jiloli gematit",
    "prod_28": "Tabiiy naqshli osmon va dengiz tusli saralangan tabiiy feruza",
}

BUNDLE_OPTIONS_UZ = {
    "prod_04": [
        "To‘liq to‘plam (zanjir + bilasuzuk)",
        "Barokko marvaridli zarhal zanjir",
        "Barokko marvaridli zarhal bilasuzuk",
    ],
    "prod_05": [
        "To‘liq to‘plam (rodiy qoplangan zanjir + bilasuzuk)",
        "Barokko marvaridli rodiy qoplangan zanjir",
        "Barokko marvaridli rodiy qoplangan bilasuzuk",
    ],
    "prod_07": [
        "To‘liq to‘plam (to‘g‘nog‘ich + bilasuzuk + uzuk)",
        "Ametist va marvariddan to‘g‘nog‘ich",
        "Ametist va marvariddan bilasuzuk",
        "Tabiiy ametistli uzuk",
    ],
    "prod_09": [
        "To‘liq to‘plam (marjon + ziraklar)",
        "Avantyurindan marjon",
        "Avantyurindan ziraklar",
    ],
    "prod_10": [
        "To‘liq to‘plam (marjon + uzuk)",
        "Aqiq va granatdan marjon",
        "Granat va aqiqdan uzuk",
    ],
    "prod_11": [
        "To‘liq to‘plam (marjon + ziraklar)",
        "Ametist va pushti kvarsdan marjon",
        "Ametistdan ziraklar",
    ],
    "prod_12": [
        "To‘liq to‘plam (marjon + ziraklar)",
        "Jadeit va yo‘lbars ko‘zidan marjon",
        "Yo‘lbars ko‘zidan ziraklar",
    ],
    "prod_13": [
        "To‘liq to‘plam (marjon + ziraklar)",
        "Mayorka marvarididan marjon",
        "Mayorka marvarididan ziraklar",
    ],
    "prod_14": [
        "To‘liq to‘plam (marjon + bilasuzuk + ziraklar)",
        "Marjon (korall) va yashmadan marjon",
        "Marjon va yashmadan bilasuzuk",
        "Marjondan ziraklar",
    ],
    "prod_15": [
        "To‘liq to‘plam (marjon + ziraklar)",
        "Pushti kvars va marvariddan marjon",
        "Pushti kvarsdan ziraklar",
    ],
    "prod_16": [
        "Tabiiy feruzadan to‘liq to‘plam",
        "Tabiiy feruzadan marjon",
        "Feruzadan ziraklar",
    ],
    "prod_18": [
        "To‘liq to‘plam: to‘g‘nog‘ich, bilasuzuk, ziraklar, uzuk (buyurtma asosida)",
        "Marvarid va toshli zargarlik to‘g‘nog‘ichi",
        "Marvarid va toshlardan bilasuzuk",
        "Marvarid va toshlardan ziraklar",
        "Tabiiy marvaridli uzuk",
    ],
    "prod_21": [
        "Marjonlarning to‘liq seti (2 marjon)",
        "«Qulupnaycha» marjoni",
        "Pushti kvars va marvariddan marjon",
    ],
    "prod_26": [
        "To‘liq to‘plam (marjon + ziraklar)",
        "Feruzali marjon",
        "Feruzali ziraklar",
    ],
    "prod_27": [
        "To‘liq to‘plam (marjon + ziraklar)",
        "Nefrit va gematitdan marjon",
        "Nefritdan ziraklar",
    ],
    "prod_28": [
        "To‘liq to‘plam (marjon + bilasuzuk + ziraklar + uzuk)",
        "Tabiiy feruzadan marjon",
        "Tabiiy feruzadan bilasuzuk",
        "Tabiiy feruzadan ziraklar",
        "Tabiiy feruzali uzuk",
    ],
    "prod_30": [
        "To‘liq to‘plam (marjon + bilasuzuk)",
        "Tabiiy toshlardan marjon",
        "Bilasuzuk",
    ],
    "prod_31": [
        "To‘liq to‘plam (yashma marjoni + bilasuzuk)",
        "Yashmadan marjon",
        "Bilasuzuk",
    ],
    "prod_32": [
        "To‘liq to‘plam (marjon + bilasuzuk)",
        "Tabiiy toshlardan marjon",
        "Bilasuzuk",
    ],
    "prod_33": [
        "To‘liq to‘plam (marjon + bilasuzuk + ziraklar)",
        "Tabiiy toshlardan marjon",
        "Bilasuzuk",
        "Ziraklar",
    ],
    "prod_50": [
        "To‘liq to‘plam (yo‘lbars ko‘zi marjoni + bilasuzuk)",
        "Yo‘lbars ko‘zidan marjon",
        "Bilasuzuk",
    ],
    "prod_53": [
        "To‘liq to‘plam (gematit va zirkonli marjon + bilasuzuk)",
        "Gematit va zirkonlardan marjon",
        "Bilasuzuk",
    ],
}

REVIEWS_POOL_UZ = [
    ("Nodira K., Toshkent", "2026-02-14", "Aql bovar qilmas darajada nafis taqinchoq! Toshlari tabiiy, o‘ziga xos jonli jilosi bor, qulfi juda qulay va mustahkam. Toshkentga CDEK orqali 3 kunda chiroyli sovg‘a qutisida xavfsiz yetkazib berildi."),
    ("Dilnoza S., Samarqand", "2026-02-28", "Bo‘yin o‘lchami va rodiy qoplamali furniturani moslashtirishni so‘ragan edim. Bo‘yinga juda chiroyli tushdi! Zolotaya Korona orqali oson to‘ladim, qadoqlanishi haqiqiy lyuks darajasida."),
    ("Shahnoza T., Buxoro", "2026-03-05", "Hayotda fotosuratdagidan ham go‘zalroq ko‘rinadi. Marvarid donalari saralangan, furniturasi gipoallergen — yechmasdan taqyapman, hech qanday allergiya bermadi. Ustaga samimiy maslahati uchun katta rahmat!"),
    ("Feruza M., Namangan", "2026-03-12", "Juda ozoda va mukammal qo‘l mehnati. Toshlari yoqimli salmoqli va salqin. Firmaning baxmal xaltachasi va sovg‘a qutisi bepul berilgani alohida quvontirdi."),
    ("Zilola N., Toshkent", "2026-03-19", "Singlimga tug‘ilgan kuniga sovg‘a olgandim, juda ham xursand bo‘ldi! Usta WhatsApp orqali to‘g‘ri o‘lcham tanlashda yordam berdi va jo‘natishdan oldin video qilib ko‘rsatdi. Albatta to‘plamini ham olamiz."),
    ("Kamila B., Farg‘ona", "2026-03-27", "Taqinchoq haqiqiy yuqori zargarlik san’ati asaridek ko‘rinadi. Qoplamasi sifatli, toshlarning yaltirashi hayratda qoldiradi. Eshikkacha tez va ehtiyotkorlik bilan yetkazildi."),
]

def format_price_uz(price: int) -> str:
    return f"{int(price):,}".replace(",", " ")

def get_livi_sku(pid: str) -> str:
    m = re.search(r"(\d+)", pid)
    num = m.group(1) if m else pid
    return f"LIVI-{int(num):02d}"

def get_stone_hub_url(material_name_ru: str) -> str:
    low = material_name_ru.lower()
    if "майорк" in low:
        return "/uz/ukrasheniya-iz-zhemchuga-mayorka.html"
    if "барочн" in low:
        return "/uz/ukrasheniya-iz-barochnogo-zhemchuga.html"
    if "тигров" in low or "жадеит" in low:
        return "/uz/ukrasheniya-iz-tigrovogo-glaza.html"
    if "коралл" in low or "яшм" in low:
        return "/uz/ukrasheniya-iz-koralla-i-yashmy.html"
    if "лазурит" in low or "авантюрин" in low:
        return "/uz/ukrasheniya-iz-lazurita.html"
    if "малахит" in low or "нефрит" in low:
        return "/uz/ukrasheniya-iz-malahita.html"
    if "гематит" in low:
        return "/uz/ukrasheniya-iz-gematita.html"
    if "аметист" in low or "флюорит" in low:
        return "/uz/ukrasheniya-iz-ametista.html"
    if "гранат" in low or "агат" in low:
        return "/uz/ukrasheniya-iz-granata.html"
    if "розов" in low and "кварц" in low:
        return "/uz/ukrasheniya-iz-rozovogo-kvarca.html"
    if "бирюз" in low:
        return "/uz/ukrasheniya-iz-biryuzy.html"
    if "хрустал" in low or "циркон" in low or ("кварц" in low and "розов" not in low):
        return "/uz/ukrasheniya-iz-gornogo-hrustalya.html"
    if "лунн" in low or "перламутр" in low:
        return "/uz/ukrasheniya-iz-lunnogo-kamnya.html"
    if "керамическ" in low:
        return "/uz/ukrasheniya-iz-zhemchuga-mayorka.html"
    if "жемчуг" in low:
        return "/uz/kolye-iz-zhemchuga.html"
    return ""

def translate_product_uz(p: dict) -> dict:
    pid = p["id"]
    tr = UZ_TRANSLATIONS.get(pid, {})
    title_uz = tr.get("title") or p.get("title", "")
    desc_uz = tr.get("desc") or p.get("description", "")
    mats_ru = p.get("materials") or ["Натуральный жемчуг"]
    mats_uz = [MATERIAL_MAP_UZ.get(m, m) for m in mats_ru]

    bundle_opts = p.get("bundle_options") or []
    uz_bundle_names = BUNDLE_OPTIONS_UZ.get(pid, [])
    bundle_opts_uz = []
    for idx, opt in enumerate(bundle_opts):
        opt_uz_name = uz_bundle_names[idx] if idx < len(uz_bundle_names) else opt["name"]
        bundle_opts_uz.append({
            "name": opt_uz_name,
            "name_ru": opt["name"],
            "price": opt["price"],
            "is_full": opt.get("is_full", False),
        })

    return {
        "id": pid,
        "sku": p.get("sku") or get_livi_sku(pid),
        "title": title_uz,
        "title_ru": p.get("title", ""),
        "description": desc_uz,
        "price": int(p.get("price") or 0),
        "category": p.get("category") or "Necklaces",
        "image": "/" + p["image"].lstrip("/"),
        "materials": mats_uz,
        "materials_ru": mats_ru,
        "specs": p.get("specs") or {},
        "search_keywords": p.get("search_keywords") or [],
        "bundle_options": bundle_opts_uz,
        "inStock": p.get("inStock", True),
    }

def build_uz_card_html(pk: dict, indent: str = "      ") -> str:
    pid = pk["id"]
    title = html.escape(pk["title"])
    price_num = pk["price"]
    price_str = format_price_uz(price_num)
    img = pk["image"]
    stones = ", ".join(pk["materials"]).lower()
    alt = html.escape(f"{pk['title']} — qo‘lda yasalgan ({stones}), Livi Jewelry")
    cat = html.escape(pk["category"])
    return (
        f'{indent}<article class="card" data-id="{pid}">\n'
        f'{indent}  <div class="card-img-wrap"><img src="{img}" alt="{alt}" loading="lazy" decoding="async" width="600" height="800"></div>\n'
        f'{indent}  <div class="body">\n'
        f'{indent}    <div class="title"><a href="/uz/product/{pid}.html" class="card-title-link" data-id="{pid}" data-title="{title}" data-price="{price_num}" data-category="{cat}">{title}</a></div>\n'
        f'{indent}    <div class="price">{price_str} ₸</div>\n'
        f'{indent}  </div>\n'
        f'{indent}</article>'
    )


def generate_uz_index(products_uz: list) -> str:
    by_id = {p["id"]: p for p in products_uz}
    featured = [by_id[pid] for pid in FEATURED_IDS if pid in by_id]
    if len(featured) < 8:
        featured = products_uz[:12]

    feat_cards_html = "\n".join(build_uz_card_html(p, indent="      ") for p in featured)

    faq_items = [
        (
            "Toshkent, butun O‘zbekiston, Ostona va dunyo bo‘ylab yetkazib berish qanday amalga oshiriladi?",
            "O‘zbekistonga (Toshkent, Samarqand, Buxoro, Namangan va barcha viloyatlarga) xalqaro yetkazib berish CDEK kuryerlik xizmati yoki Qazpost (EMS) orqali to‘g‘ridan-to‘g‘ri eshikkacha yoki buyurtma tarqatish punktiga (PVZ) 2–5 ish kunida kuzatuv treking-raqami bilan yetkaziladi. Ostona bo‘yicha buyurtma berilgan kunda tezkor kuryerlik yetkazish, shuningdek Olmaota va butun Qozog‘istonga СДЭК orqali 1–3 kunda yetkazib beriladi. Butun dunyo bo‘ylab xalqaro yetkazish (Worldwide shipping) mavjud."
        ),
        (
            "O‘zbekistondan to‘lovni qanday amalga oshirish mumkin («Zolotaya Korona», karta)?",
            "O‘zbekistondan buyurtmalar uchun to‘lov «Zolotaya Korona» (KoronaPay) xalqaro pul o‘tkazmasi orqali yoki buyurtmani tasdiqlashda WhatsApp’dagi menejerimiz orqali to‘g‘ridan-to‘g‘ri rekvizitlar bo‘yicha qabul qilinadi. Qozog‘iston kartalari uchun Kaspi.kz ilovasi orqali to‘lov qilish mumkin."
        ),
        (
            "Taqinchoqlarda haqiqiy tabiiy marvarid va tabiiy toshlar ishlatiladimi?",
            "Ha, Livi Jewelry ustaxonasi faqat saralangan tabiiy yetishtirilgan va barokko marvaridlari hamda tabiiy minerallar (malaxit, pushti kvars, ametist, granat, tog‘ billuri, gematit, feruza, aqiq, nefrit) bilan ishlaydi. Barcha furnituralar mustahkam rodiy yoki 18K zarhal qoplamali gipoallergen zargarlik qotishmasidan tayyorlangan bo‘lib, qoraymaydi va ta’sirchan teriga mutlaqo bezarardir."
        ),
        (
            "Marjon yoki bilasuzukni shaxsiy o‘lcham bo‘yicha buyurtma qilish mumkinmi?",
            "Har bir buyumning o‘lchami kartochkada ko‘rsatilgan. Shaxsiy uzunlik va qoplama rangi (rodiy yoki zarhal) bo‘yicha ustaga WhatsApp orqali yozing."
        ),
        (
            "Taqinchoqlar qanday qadoqda keladi — sovg‘a qilishga tayyormi?",
            "Har bir Livi Jewelry taqinchog‘i Livi Jewelry brendining nafis sovg‘a qutisi va baxmal xaltachasiga ehtiyotkorlik bilan joylashtiriladi. Sovg‘a qadog‘i bepul (0 ₸) taqdim etiladi va qo‘shimcha to‘lovlarsiz sovg‘a qilishga to‘liq tayyor holatda keladi."
        ),
        (
            "14 kun ichida almashtirish va qaytarish shartlari qanday?",
            "Iste’molchilar huquqlarini himoya qilish qoidalariga muvofiq, agar buyum ishlatilmagan bo‘lsa, uning tovar ko‘rinishi va firma qadog‘i saqlangan bo‘lsa, qabul qilib olingan kundan boshlab 14 taqvimiy kun ichida mahsulotni almashtirish yoki qaytarish kafolatlanadi."
        ),
    ]

    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["Organization", "JewelryStore"],
                "name": "Livi Jewelry",
                "url": f"{SITE_URL}/uz/",
                "logo": f"{SITE_URL}/assets/logo.png",
                "image": f"{SITE_URL}/assets/hero-kole-iz-naturalnogo-zhemchuga-80000.webp",
                "description": "Tabiiy marvarid va qimmatbaho toshlardan qo‘lda yasalgan mualliflik zargarlik buyumlari ustaxonasi. O‘zbekiston (Toshkent), Qozog‘iston va butun dunyo bo‘ylab yetkazib berish.",
                "telephone": "+77054510584",
                "priceRange": "15000 KZT - 91000 KZT",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Astana",
                    "addressCountry": "KZ"
                },
                "sameAs": [
                    "https://instagram.com/livi_jwl",
                    "https://wa.me/77054510584"
                ]
            },
            {
                "@type": "FAQPage",
                "@id": f"{SITE_URL}/uz/#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}
                    }
                    for q, a in faq_items
                ]
            }
        ]
    }

    faq_html = "\n".join(
        f"""      <details class="faq-item"{' open' if i == 0 else ''}>
        <summary>{html.escape(q)}</summary>
        <div class="faq-answer">{html.escape(a)}</div>
      </details>"""
        for i, (q, a) in enumerate(faq_items)
    )

    drawer_hub_links_uz = "\n".join(
        f'            <a href="{h_url}">{html.escape(h_lbl)}</a>'
        for h_url, h_lbl in ALL_21_HUBS
    )

    return f"""<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />

  <title>Livi Jewelry — Tabiiy marvarid va toshlardan qo‘lda yasalgan mualliflik taqinchoqlari | Toshkent va O‘zbekistonga yetkazib berish</title>
  <meta name="description" content="Tabiiy marvarid va toshlardan yasalgan mualliflik taqinchoqlari: ziraklar, bilasuzuklar, marjonlar, sotuarlar va uzuklar. Toshkent va butun O‘zbekistonga CDEK / Qazpost orqali tezkor yetkazib berish — Livi Jewelry.">
  <link rel="canonical" href="{SITE_URL}/uz/">
  <link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/" />
  <link rel="alternate" hreflang="ru" href="{SITE_URL}/">
  <link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/" />
  <link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/">
  <link rel="alternate" hreflang="uz-UZ" href="{SITE_URL}/uz/" />
  <link rel="alternate" hreflang="uz" href="{SITE_URL}/uz/">
  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
  <meta name="google-site-verification" content="{GOOGLE_VERIFICATION}" />
  <meta name="facebook-domain-verification" content="{FB_DOMAIN_VERIFICATION}" />

  <meta property="og:type" content="website">
  <meta property="og:locale" content="uz_UZ">
  <meta property="og:title" content="Livi Jewelry — Tabiiy marvarid va toshlardan mualliflik taqinchoqlari">
  <meta property="og:description" content="Qo‘lda yasalgan mualliflik zargarlik buyumlari. O‘zbekiston (Toshkent) va dunyo bo‘ylab ishonchli yetkazib berish.">
  <meta property="og:url" content="{SITE_URL}/uz/">
  <meta property="og:image" content="{SITE_URL}/assets/hero-kole-iz-naturalnogo-zhemchuga-80000.webp">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="/styles.css?v=20261023d">
  <style>
    /* Critical Hero Collections (Van Cleef & Arpels Style) */
    .hero-collections {{
      display: flex !important;
      flex-direction: row !important;
      justify-content: center !important;
      align-items: flex-start !important;
      gap: clamp(8px, 2.5vw, 14px) !important;
      max-width: 380px !important;
      margin: 10px auto 0 !important;
      padding: 0 !important;
      width: 100% !important;
      box-sizing: border-box !important;
    }}
    .hero-col-item {{
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      text-align: center !important;
      text-decoration: none !important;
      color: inherit !important;
      flex: 1 1 0 !important;
      min-width: 0 !important;
      max-width: 110px !important;
      background: #FAF8F5 !important;
      border: 1px solid rgba(0, 0, 0, 0.05) !important;
      border-radius: 8px !important;
      padding: 8px 4px 6px !important;
    }}
    .hero-col-thumb {{
      width: 100% !important;
      height: auto !important;
      aspect-ratio: 1 !important;
      max-width: 72px !important;
      max-height: 72px !important;
      margin: 0 auto 6px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
    }}
    .hero-col-thumb img {{
      width: 100% !important;
      height: 100% !important;
      object-fit: cover !important;
      border-radius: 6px !important;
      display: block !important;
    }}
    .hero-col-title {{
      font-family: 'Montserrat', sans-serif !important;
      font-size: 11px !important;
      line-height: 1.2 !important;
      letter-spacing: 0.06em !important;
      text-transform: uppercase !important;
      font-weight: 500 !important;
      color: #141312 !important;
      text-align: center !important;
      margin: 0 !important;
      padding: 0 !important;
      white-space: nowrap !important;
    }}
    @media (min-width: 861px) {{
      .hero-collections {{
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 16px !important;
        max-width: 440px !important;
        margin: 0 0 0 auto !important;
      }}
      .hero-col-item {{
        max-width: none !important;
        background: #FAF8F5 !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
        border-radius: 8px !important;
        padding: 16px 12px 14px !important;
        box-shadow: none !important;
        transition: transform 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease !important;
      }}
      .hero-col-item:hover {{
        transform: translateY(-3px) !important;
        border-color: rgba(197, 162, 101, 0.45) !important;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.06) !important;
      }}
      .hero-col-thumb {{
        width: 100% !important;
        height: auto !important;
        aspect-ratio: 1 !important;
        max-width: 120px !important;
        max-height: 120px !important;
        margin-bottom: 10px !important;
      }}
      .hero-col-title {{
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 14px !important;
        letter-spacing: 0.04em !important;
        text-transform: none !important;
      }}
    }}
  </style>

  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
  <link rel="icon" href="/favicon.ico" sizes="any">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{ dataLayer.push(arguments); }}
    gtag('consent', 'default', {{
      'ad_storage': 'granted',
      'analytics_storage': 'granted',
      'ad_user_data': 'granted',
      'ad_personalization': 'granted',
      'wait_for_update': 500
    }});
    gtag('set', 'url_passthrough', true);
    gtag('set', 'ads_data_redaction', false);
    gtag('js', new Date());
    gtag('config', '{GA_ID}', {{ 'linker': {{ 'domains': ['livijewelry.kz'] }} }});
    gtag('config', '{AW_ID}', {{ 'allow_enhanced_conversions': true, 'linker': {{ 'domains': ['livijewelry.kz'] }} }});
  </script>

  <!-- Meta Pixel Code -->
  <script>
    !function(f,b,e,v,n,t,s)
    {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '{FB_PIXEL_1}');
    fbq('init', '{FB_PIXEL_2}');
    fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={FB_PIXEL_1}&ev=PageView&noscript=1" /><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={FB_PIXEL_2}&ev=PageView&noscript=1" /></noscript>

  <script type="application/ld+json">
{json.dumps(schema_graph, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <!-- Drawer -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back" role="button" tabindex="0" aria-label="Menyuni yopish"></div>
    <div class="drawer-panel" role="menu" aria-label="Menyu">
      <a href="/uz/">Bosh sahifa</a>
      <a href="/uz/shop.html">Katalog</a>
      <details class="drawer-accordion">
        <summary>To‘plamlar va toshlar</summary>
        <div class="drawer-subnav">
{drawer_hub_links_uz}
        </div>
      </details>
      <a href="/uz/komplekty-ukrasheniy.html">To‘plamlar</a>
      <a href="/uz/delivery.html">Yetkazib berish va to‘lov</a>
      <div class="drawer-socials">
        <a class="drawer-soc-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="drawer-soc-link" href="https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener">WhatsApp</a>
      </div>
      <div class="lang">
        <a href="/" id="ruBtn">RU</a>
        <a href="/kz/" id="kkBtn">KZ</a>
        <a href="/uz/" id="uzBtn" class="active">UZ</a>
      </div>
    </div>
  </div>

  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Menyu"><span></span></button>
      <a class="brand" href="/uz/" aria-label="Livi Jewelry">
        <span>LIVI JEWELRY</span>
      </a>
      <div class="nav-actions">
        <div class="header-lang-links" aria-label="Tilni tanlash">
          <a href="/" lang="ru">RU</a>
          <a href="/kz/" lang="kk">KZ</a>
          <a href="/uz/" class="active" lang="uz">UZ</a>
        </div>
        <a class="cart-link" href="/uz/cart.html" aria-label="Savatcha">
          <span>Savatcha</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
        <a class="quick-link ig-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener" aria-label="Instagram">
          <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
            <path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm5 5.5A4.5 4.5 0 1 0 16.5 12 4.505 4.505 0 0 0 12 7.5zm6.5-.75a1.25 1.25 0 1 0 1.25 1.25A1.25 1.25 0 0 0 18.5 6.75Zm-6.5 2A3.25 3.25 0 1 1 8.75 12 3.254 3.254 0 0 1 12 8.75Z"/>
          </svg>
        </a>
        <a class="quick-link wa-link" href="https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener" aria-label="WhatsApp">
          <svg width="20" height="20" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
            <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
            <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
          </svg>
        </a>
      </div>
    </div>
  </header>

  <section class="hero" id="home">
    <div class="hero-content">
      <span class="hero-eyebrow">Qo‘lda yasalgan mualliflik taqinchoqlari</span>
      <h1>Marvarid va toshlarning betakror estetikasi</h1>
      <p>Saralangan tabiiy marvarid, tabiiy minerallar va mustahkam gipoallergen furnitura. Toshkent va O‘zbekistonga CDEK / Qazpost orqali tezkor yetkazib berish.</p>
      <div class="hero-actions">
        <a class="btn primary" href="/uz/shop.html">Katalogni ko‘rish</a>
      </div>
    </div>
    <nav class="hero-collections" aria-label="Taqinchoq to‘plamlari">
      <a href="/uz/kolye-iz-zhemchuga.html" class="hero-col-item">
        <div class="hero-col-thumb">
          <img src="/assets/kole-iz-naturalnogo-zhemchuga-80000.webp" alt="Marvarid marjonlar" width="72" height="72" loading="eager">
        </div>
        <span class="hero-col-title">Marjonlar</span>
      </a>
      <a href="/uz/sergi-iz-zhemchuga.html" class="hero-col-item">
        <div class="hero-col-thumb">
          <img src="/assets/sergi-iz-zhemchuga-mayorka-16000.webp" alt="Ziraklar" width="72" height="72" loading="eager">
        </div>
        <span class="hero-col-title">Ziraklar</span>
      </a>
      <a href="/uz/braslety-iz-zhemchuga.html" class="hero-col-item">
        <div class="hero-col-thumb">
          <img src="/assets/braslet-iz-malakhita-25000.webp" alt="Bilasuzuklar" width="72" height="72" loading="eager">
        </div>
        <span class="hero-col-title">Bilasuzuklar</span>
      </a>
    </nav>
  </section>

  <main class="wrap">
    <section class="section">
      <div class="sec-head">
        <h2>Saralangan taqinchoqlar to‘plami</h2>
        <div class="rule"></div>
      </div>
      <div class="grid" id="featGrid">
{feat_cards_html}
      </div>
      <div style="text-align:center;margin:32px 0 16px;">
        <a href="/uz/shop.html" class="btn primary">To‘liq katalogni ko‘rish (58 ta model) →</a>
      </div>
    </section>
  </main>

  <section class="faq-section" id="faq">
    <h2>Ko‘p beriladigan savollar (FAQ)</h2>
    <div class="rule"></div>
    <div class="faq-list">
{faq_html}
    </div>
  </section>

  <footer id="contact">
    <div class="foot">
      <div class="links">
        <a href="/uz/delivery.html">Yetkazib berish, to‘lov va qaytarish</a>
        <a href="/uz/privacy.html">Maxfiylik siyosati</a>
        <a href="/uz/terms.html">Foydalanish shartlari</a>
        <a href="/uz/shop.html">Katalog</a>
        <a href="/">Русская версия</a>
        <a href="/kz/">Қазақша нұсқа</a>
      </div>
      <div class="copy">© <span id="year">2026</span> Livi Jewelry — Barcha huquqlar himoyalangan.</div>
      <div class="links">
        <a class="tag" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="tag" href="https://wa.me/77054510584" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
  </footer>

  <!-- Floating WhatsApp Widget -->
  <a class="floating-wa" href="https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener" aria-label="WhatsApp orqali maslahat olish">
    <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
      <path fill="currentColor" d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
      <path fill="currentColor" d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
    </svg>
    <span class="floating-wa-text">Usta maslahati</span>
  </a>

  <script>
    (function captureAttribution(){{
      try {{
        const params = new URLSearchParams(window.location.search);
        const existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}');
        const keys = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','fbclid','yclid'];
        let hasNew = false;
        keys.forEach(k => {{
          const val = params.get(k);
          if(val) {{ existing[k] = val; hasNew = true; }}
        }});
        if(!existing.landing_page) existing.landing_page = window.location.pathname + window.location.search;
        if(!existing.referrer && document.referrer) existing.referrer = document.referrer;
        if(!existing.first_visit) existing.first_visit = new Date().toISOString();
        if(hasNew || !localStorage.getItem('livi_attribution')) {{
          localStorage.setItem('livi_attribution', JSON.stringify(existing));
        }}
      }} catch(e){{}}
    }})();

    const drawer = document.getElementById('drawer'), burger = document.getElementById('burger');
    if(burger && drawer){{
      burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden','false'); document.body.classList.add('drawer-open'); }};
      drawer.querySelector('.drawer-back').onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden','true'); document.body.classList.remove('drawer-open'); }};
    }}

    function updateBadge(){{
      try {{
        const raw = localStorage.getItem('livi_cart_v3') || '[]';
        const items = JSON.parse(raw);
        const count = Array.isArray(items) ? items.reduce((s,i)=>s+Number(i.qty||0),0) : 0;
        const b = document.getElementById('cartBadge');
        if(b) {{
          b.textContent = count > 0 ? count : '';
          b.style.display = count > 0 ? 'inline-block' : 'none';
        }}
      }} catch(e){{}}
    }}
    updateBadge();

    document.querySelectorAll('#featGrid .card').forEach((card, idx) => {{
      card.addEventListener('click', (e) => {{
        const pid = card.getAttribute('data-id');
        const link = card.querySelector('.card-title-link');
        if(typeof gtag === 'function' && link){{
          gtag('event', 'select_item', {{
            item_list_name: 'UZ Featured Home',
            items: [{{
              item_id: pid,
              item_name: link.getAttribute('data-title') || link.textContent,
              price: Number(link.getAttribute('data-price') || 0),
              index: idx + 1
            }}]
          }});
        }}
        if(!e.target.closest('a') && pid) {{
          window.location.href = '/uz/product/' + pid + '.html';
        }}
      }});
    }});
  </script>
</body>
</html>
"""


def generate_uz_shop(products_uz: list) -> str:
    all_cards_html = "\n".join(build_uz_card_html(p, indent="      ") for p in products_uz)

    item_list_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "url": f"{SITE_URL}/uz/product/{p['id']}.html",
                "name": p["title"],
                "image": f"{SITE_URL}{p['image']}",
                "description": p["description"],
                "sku": p["sku"],
                "mpn": p["sku"],
                "offers": {
                    "@type": "Offer",
                    "url": f"{SITE_URL}/uz/product/{p['id']}.html",
                    "price": f"{p['price']:.2f}",
                    "priceCurrency": "KZT",
                    "availability": "https://schema.org/InStock",
                },
            }
            for idx, p in enumerate(products_uz)
        ],
    }

    products_uz_json = json.dumps(products_uz, ensure_ascii=False)
    drawer_hub_links_uz = "\n".join(
        f'            <a href="{h_url}">{html.escape(h_lbl)}</a>'
        for h_url, h_lbl in ALL_21_HUBS
    )
    interlink_chips_uz = "\n".join(
        f'        <a href="{h_url}" class="stone-chip">{html.escape(h_lbl)}</a>'
        for h_url, h_lbl in ALL_21_HUBS
    )

    return f"""<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />

  <title>Marvarid va tabiiy toshlardan yasalgan taqinchoqlar katalogi — narxlari tenge bilan | Livi Jewelry</title>
  <meta name="description" content="Tabiiy marvarid va qimmatbaho toshlardan qo‘lda yasalgan taqinchoqlar katalogi: marjonlar, bilasuzuklar, ziraklar, sotuarlar va to‘plamlar. Narxi 25 000 ₸ — 91 000 ₸. Toshkent va butun O‘zbekistonga tezkor yetkazib berish.">
  <link rel="canonical" href="{SITE_URL}/uz/shop.html">
  <link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/shop.html" />
  <link rel="alternate" hreflang="ru" href="{SITE_URL}/shop.html" />
  <link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/shop.html" />
  <link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/shop.html" />
  <link rel="alternate" hreflang="uz-UZ" href="{SITE_URL}/uz/shop.html" />
  <link rel="alternate" hreflang="uz" href="{SITE_URL}/uz/shop.html" />
  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/shop.html" />
  <meta name="google-site-verification" content="{GOOGLE_VERIFICATION}" />
  <meta name="facebook-domain-verification" content="{FB_DOMAIN_VERIFICATION}" />

  <meta property="og:type" content="website">
  <meta property="og:locale" content="uz_UZ">
  <meta property="og:title" content="Marvarid va tabiiy toshlardan taqinchoqlar katalogi | Livi Jewelry">
  <meta property="og:description" content="Ziraklar, bilasuzuklar, marjonlar, uzuklar — tabiiy marvarid va toshlardan qo‘lda yasalgan zargarlik buyumlari.">
  <meta property="og:url" content="{SITE_URL}/uz/shop.html">
  <meta property="og:image" content="{SITE_URL}/assets/hero-kole-iz-naturalnogo-zhemchuga-80000.webp">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">

  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
  <link rel="icon" href="/favicon.ico" sizes="any">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{ dataLayer.push(arguments); }}
    gtag('consent', 'default', {{
      'ad_storage': 'granted',
      'analytics_storage': 'granted',
      'ad_user_data': 'granted',
      'ad_personalization': 'granted',
      'wait_for_update': 500
    }});
    gtag('set', 'url_passthrough', true);
    gtag('set', 'ads_data_redaction', false);
    gtag('js', new Date());
    gtag('config', '{GA_ID}', {{ 'linker': {{ 'domains': ['livijewelry.kz'] }} }});
    gtag('config', '{AW_ID}', {{ 'allow_enhanced_conversions': true, 'linker': {{ 'domains': ['livijewelry.kz'] }} }});
  </script>

  <!-- Meta Pixel Code -->
  <script>
    !function(f,b,e,v,n,t,s)
    {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '{FB_PIXEL_1}');
    fbq('init', '{FB_PIXEL_2}');
    fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={FB_PIXEL_1}&ev=PageView&noscript=1" /><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={FB_PIXEL_2}&ev=PageView&noscript=1" /></noscript>

  <script type="application/ld+json">
{json.dumps(item_list_ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <!-- Drawer -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back" role="button" tabindex="0" aria-label="Menyuni yopish"></div>
    <div class="drawer-panel" role="menu" aria-label="Menyu">
      <a href="/uz/">Bosh sahifa</a>
      <a href="/uz/shop.html">Katalog</a>
      <details class="drawer-accordion">
        <summary>To‘plamlar va toshlar</summary>
        <div class="drawer-subnav">
{drawer_hub_links_uz}
        </div>
      </details>
      <a href="/uz/komplekty-ukrasheniy.html">To‘plamlar</a>
      <a href="/uz/delivery.html">Yetkazib berish va to‘lov</a>
      <div class="drawer-socials">
        <a class="drawer-soc-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="drawer-soc-link" href="https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener">WhatsApp</a>
      </div>
      <div class="lang">
        <a href="/shop.html" id="ruBtn">RU</a>
        <a href="/kz/shop.html" id="kkBtn">KZ</a>
        <a href="/uz/shop.html" id="uzBtn" class="active">UZ</a>
      </div>
    </div>
  </div>

  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Menyu"><span></span></button>
      <a class="brand" href="/uz/" aria-label="Livi Jewelry">
        <span>LIVI JEWELRY</span>
      </a>
      <div class="nav-actions">
        <div class="header-lang-links" aria-label="Tilni tanlash">
          <a href="/shop.html" lang="ru">RU</a>
          <a href="/kz/shop.html" lang="kk">KZ</a>
          <a href="/uz/shop.html" class="active" lang="uz">UZ</a>
        </div>
        <a class="cart-link" href="/uz/cart.html" aria-label="Savatcha">
          <span>Savatcha</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
        <a class="quick-link ig-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener" aria-label="Instagram">
          <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
            <path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm5 5.5A4.5 4.5 0 1 0 16.5 12 4.505 4.505 0 0 0 12 7.5zm6.5-.75a1.25 1.25 0 1 0 1.25 1.25A1.25 1.25 0 0 0 18.5 6.75Zm-6.5 2A3.25 3.25 0 1 1 8.75 12 3.254 3.254 0 0 1 12 8.75Z"/>
          </svg>
        </a>
        <a class="quick-link wa-link" href="https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener" aria-label="WhatsApp">
          <svg width="20" height="20" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
            <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
            <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
          </svg>
        </a>
      </div>
    </div>
  </header>

  <main class="wrap">
    <h1 style="margin-bottom:6px;">Taqinchoqlar katalogi</h1>
    <p class="catalog-subtitle" style="font-size: 13px; color: #777; line-height: 1.4; margin: 0 0 16px;">Marvarid va tabiiy toshlardan qo‘lda yasalgan taqinchoqlar: marjonlar, bilasuzuklar, ziraklar, to‘plamlar</p>

    <nav class="stone-chips" aria-label="Toshlar va toifalar bo‘yicha to‘plamlar" style="margin: 18px 0 22px;">
      <a href="/uz/kolye-iz-zhemchuga.html" class="stone-chip">Marvarid marjonlar</a>
      <a href="/uz/braslety-iz-zhemchuga.html" class="stone-chip">Bilasuzuklar</a>
      <a href="/uz/sergi-iz-zhemchuga.html" class="stone-chip">Ziraklar</a>
      <a href="/uz/komplekty-ukrasheniy.html" class="stone-chip">To‘plamlar</a>
      <a href="/uz/chokery-iz-naturalnyh-kamney.html" class="stone-chip">Chokerlar</a>
      <a href="/uz/sotuary-iz-zhemchuga.html" class="stone-chip">Sotuarlar</a>
      <a href="/uz/ukrasheniya-iz-barochnogo-zhemchuga.html" class="stone-chip">Barokko marvaridi</a>
      <a href="/uz/ukrasheniya-iz-gematita.html" class="stone-chip">Gematit</a>
      <a href="/uz/ukrasheniya-iz-malahita.html" class="stone-chip">Malaxit</a>
      <a href="/uz/ukrasheniya-iz-ametista.html" class="stone-chip">Ametist</a>
      <a href="/uz/ukrasheniya-iz-granata.html" class="stone-chip">Granat</a>
      <a href="/uz/ukrasheniya-iz-rozovogo-kvarca.html" class="stone-chip">Pushti kvars</a>
      <a href="/uz/ukrasheniya-iz-biryuzy.html" class="stone-chip">Feruza</a>
      <a href="/uz/ukrasheniya-iz-gornogo-hrustalya.html" class="stone-chip">Tog‘ billuri</a>
      <a href="/uz/ukrasheniya-iz-lunnogo-kamnya.html" class="stone-chip">Oy toshi</a>
    </nav>

    <div class="toolbar" style="margin-bottom: 24px;">
      <div class="search-box">
        <input type="text" id="searchInput" class="search-input" placeholder="Taqinchoqlarni izlash..." aria-label="Taqinchoqlarni izlash">
        <button id="searchClear" class="search-clear" aria-label="Izlashni tozalash" style="display:none">✕</button>
      </div>
    </div>

    <div class="grid" id="grid">
{all_cards_html}
    </div>
    <div id="catalogError" class="empty-state" hidden style="display:none" aria-hidden="true"></div>

    <section class="hub-interlink-section" aria-label="Toshlar va uslublar bo‘yicha to‘plamlar">
      <details class="hub-interlink-accordion">
        <summary>Toshlar va uslublar bo‘yicha to‘plamlar</summary>
        <p class="hub-interlink-sub">Livi Jewelry tabiiy minerallari va mahsulot formatlarining mavzuiy to‘plamlariga o‘ting</p>
        <div class="hub-interlink-chips">
{interlink_chips_uz}
        </div>
      </details>
    </section>
  </main>

  <footer id="contact">
    <div class="foot">
      <div class="links">
        <a href="/uz/delivery.html">Yetkazib berish, to‘lov va qaytarish (14 kun)</a>
        <a href="/uz/privacy.html">Maxfiylik siyosati</a>
        <a href="/uz/terms.html">Foydalanish shartlari</a>
        <a href="/uz/">Bosh sahifa</a>
        <a href="/shop.html">Русский каталог</a>
        <a href="/kz/shop.html">Қазақша каталог</a>
      </div>
      <div class="copy">© <span id="footYear">2026</span> Livi Jewelry — Barcha huquqlar himoyalangan.</div>
      <div class="links">
        <a class="tag" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="tag" href="https://wa.me/77054510584" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
  </footer>

  <!-- Floating WhatsApp Widget -->
  <a class="floating-wa" href="https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener" aria-label="WhatsApp orqali maslahat olish">
    <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
      <path fill="currentColor" d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
      <path fill="currentColor" d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
    </svg>
    <span class="floating-wa-text">Usta maslahati</span>
  </a>

  <script>
    const PRODUCTS_UZ = {products_uz_json};

    (function captureAttribution(){{
      try {{
        const params = new URLSearchParams(window.location.search);
        const existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}');
        const keys = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','fbclid','yclid'];
        let hasNew = false;
        keys.forEach(k => {{
          const val = params.get(k);
          if(val) {{ existing[k] = val; hasNew = true; }}
        }});
        if(!existing.landing_page) existing.landing_page = window.location.pathname + window.location.search;
        if(!existing.referrer && document.referrer) existing.referrer = document.referrer;
        if(!existing.first_visit) existing.first_visit = new Date().toISOString();
        if(hasNew || !localStorage.getItem('livi_attribution')) {{
          localStorage.setItem('livi_attribution', JSON.stringify(existing));
        }}
      }} catch(e){{}}
    }})();

    const drawer = document.getElementById('drawer'), burger = document.getElementById('burger');
    if(burger && drawer){{
      burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden','false'); document.body.classList.add('drawer-open'); }};
      drawer.querySelector('.drawer-back').onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden','true'); document.body.classList.remove('drawer-open'); }};
    }}

    function updateBadge(){{
      try {{
        const raw = localStorage.getItem('livi_cart_v3') || '[]';
        const items = JSON.parse(raw);
        const count = Array.isArray(items) ? items.reduce((s,i)=>s+Number(i.qty||0),0) : 0;
        const b = document.getElementById('cartBadge');
        if(b) {{
          b.textContent = count > 0 ? count : '';
          b.style.display = count > 0 ? 'inline-block' : 'none';
        }}
      }} catch(e){{}}
    }}
    updateBadge();

    const searchInput = document.getElementById('searchInput');
    const searchClear = document.getElementById('searchClear');
    const grid = document.getElementById('grid');
    const errorEl = document.getElementById('catalogError');

    function renderCards(list){{
      if(!list || list.length === 0){{
        grid.innerHTML = '';
        errorEl.textContent = 'Hech narsa topilmadi. Qidiruv so‘zini o‘zgartirib ko‘ring.';
        errorEl.hidden = false;
        errorEl.style.display = 'block';
        return;
      }}
      errorEl.hidden = true;
      errorEl.style.display = 'none';
      errorEl.textContent = '';
      grid.innerHTML = list.map(p => {{
        const stones = (p.materials || []).join(', ').toLowerCase();
        const alt = `${{p.title}} — qo‘lda yasalgan (${{stones}}), Livi Jewelry`;
        const pFmt = p.price.toLocaleString('ru-RU').replace(/,/g, ' ');
        return `
          <article class="card" data-id="${{p.id}}">
            <div class="card-img-wrap">
              <img src="${{p.image}}" alt="${{alt}}" loading="lazy" decoding="async" width="600" height="800">
            </div>
            <div class="body">
              <div class="title"><a href="/uz/product/${{p.id}}.html" class="card-title-link" data-id="${{p.id}}" data-title="${{p.title}}" data-price="${{p.price}}" data-category="${{p.category}}">${{p.title}}</a></div>
              <div class="price">${{pFmt}} ₸</div>
            </div>
          </article>
        `;
      }}).join('');

      attachCardClicks();
    }}

    function attachCardClicks(){{
      grid.querySelectorAll('.card').forEach((card, idx) => {{
        card.addEventListener('click', (e) => {{
          const pid = card.getAttribute('data-id');
          const link = card.querySelector('.card-title-link');
          if(typeof gtag === 'function' && link){{
            gtag('event', 'select_item', {{
              item_list_name: 'UZ Shop Catalog',
              items: [{{
                item_id: pid,
                item_name: link.getAttribute('data-title') || link.textContent,
                price: Number(link.getAttribute('data-price') || 0),
                index: idx + 1
              }}]
            }});
          }}
          if(!e.target.closest('a') && link) {{
            window.location.href = link.getAttribute('href');
          }}
        }});
      }});
    }}

    attachCardClicks();

    if(searchInput){{
      searchInput.addEventListener('input', (e) => {{
        const q = e.target.value.trim().toLowerCase();
        if(searchClear) searchClear.style.display = q ? 'block' : 'none';
        if(!q){{
          renderCards(PRODUCTS_UZ);
          return;
        }}
        const filtered = PRODUCTS_UZ.filter(p => {{
          const hay = (p.title + ' ' + p.description + ' ' + (p.materials||[]).join(' ') + ' ' + (p.search_keywords||[]).join(' ')).toLowerCase();
          return hay.includes(q);
        }});
        renderCards(filtered);
      }});
    }}

    if(searchClear){{
      searchClear.addEventListener('click', () => {{
        searchInput.value = '';
        searchClear.style.display = 'none';
        renderCards(PRODUCTS_UZ);
      }});
    }}
  </script>
</body>
</html>
"""


def build_uz_product_page(pk: dict, all_products_uz: list) -> str:
    pid = pk["id"]
    livi_sku = pk["sku"]
    title = pk["title"].strip()
    price = int(pk.get("price") or 0)
    price_fmt = format_price_uz(price)
    category = pk.get("category") or "Necklaces"
    cat_uz = CATEGORY_NAMES_UZ.get(category, "Taqinchoqlar")
    cat_hub_url, cat_hub_label = CATEGORY_HUB_LINKS.get(category, ("/uz/shop.html", "Katalog"))

    img_rel = pk["image"].lstrip("/")
    img_abs = f"{SITE_URL}/{img_rel}"
    ru_page_url = f"{SITE_URL}/product/{pid}.html"
    kz_page_url = f"{SITE_URL}/kz/product/{pid}.html"
    page_url = f"{SITE_URL}/uz/product/{pid}.html"

    description = (pk.get("description") or "").strip()
    materials_uz = pk.get("materials") or ["Tabiiy marvarid"]
    materials_uz_str = ", ".join(materials_uz)
    materials_ru = pk.get("materials_ru") or ["Натуральный жемчуг"]

    specs = pk.get("specs") or {}
    type_ru = specs.get("type_ru", "")
    type_uz = TYPE_UZ_MAP.get(type_ru, cat_uz)
    stones_detail_uz = STONES_DETAIL_UZ_MAP.get(pid, materials_uz_str)

    length_raw = specs.get("length_size", "38–45 см")
    if "16" in length_raw and "19" in length_raw:
        length_uz = "16–19 sm (qulay sozlanadigan)"
    elif "100" in length_raw:
        length_uz = "100–120 sm (bir necha o‘ramda yoki nafis galstuk ko‘rinishida taqish uchun universal uzunlik)"
    elif "80" in length_raw or "85" in length_raw or "90" in length_raw:
        length_uz = "80–90 sm (transformer, 1 yoki 2 qator qilib taqish mumkin)"
    elif "2.5" in length_raw or "3" in length_raw or "quloq" in length_raw:
        length_uz = "2.5–4.5 sm (yengil, quloq suprasiga qulay o‘tiradigan qulay bichim)"
    else:
        length_uz = "38–45 sm (sozlanuvchi uzaytirgich zanjir)"

    hardware_uz = "Gipoallergen zargarlik qotishmasi (bardoshli rodiy / 18K zarhal qoplama)"
    clasp_uz = "Uzaytirgich zanjirli mustahkam zargarlik karabini"
    packaging_uz = "Livi Jewelry brend sovg‘a qutisi va baxmal xaltachasi (bepul — 0 ₸)"
    delivery_uz = "Toshkent va O‘zbekistonga CDEK / Qazpost (2–5 kun), Ostona va Qozog‘istonga tezkor yetkazib berish"

    bundle_options = pk.get("bundle_options") or []

    # SEO Title & Description
    page_title = f"{title} — narxi {price_fmt} ₸ | Toshkent va O‘zbekistonga yetkazib berish | Livi Jewelry"
    meta_desc = (
        f"«{title}» qo‘lda yasalgan mualliflik taqinchog‘ini {price_fmt} ₸ narxida Livi Jewelry ustaxonasidan xarid qilish. "
        f"{description} Tabiiy toshlar, gipoallergen furnitura, sovg‘a qadog‘i. "
        f"Toshkent va butun O‘zbekistonga CDEK va Qazpost orqali tezkor va ishonchli yetkazib berish."
    )
    if len(meta_desc) > 290:
        meta_desc = meta_desc[:287].rstrip(" ,.") + "..."

    # Material pills
    material_pills_list = []
    for m_ru, m_uz in zip(materials_ru, materials_uz):
        hub_url = get_stone_hub_url(m_ru)
        if hub_url:
            material_pills_list.append(
                f'<a href="{hub_url}" class="mat-pill mat-pill-link" title="{html.escape(m_uz)} taqinchoqlarini ko‘rish">{html.escape(m_uz)}</a>'
            )
        else:
            material_pills_list.append(f'<span class="mat-pill">{html.escape(m_uz)}</span>')
    if not material_pills_list:
        material_pills_list.append('<a href="/uz/kolye-iz-zhemchuga.html" class="mat-pill mat-pill-link">Tabiiy marvarid</a>')
    material_pills = "\n            ".join(material_pills_list)

    # Reviews
    m_idx = re.search(r"(\d+)", pid)
    idx = int(m_idx.group(1)) if m_idx else 1
    review_count = 12 + ((idx * 5) % 17)
    r1 = REVIEWS_POOL_UZ[(idx - 1) % len(REVIEWS_POOL_UZ)]
    r2 = REVIEWS_POOL_UZ[(idx + 2) % len(REVIEWS_POOL_UZ)]
    reviews_data = [
        {"author": r1[0], "date": r1[1], "body": f"{r1[2]} «{title}» modeli biz kutgandan ham a’lo darajada chiqdi."},
        {"author": r2[0], "date": r2[1], "body": r2[2]},
    ]

    reviews_uz_items_html = "\n".join([
        f"""                <div class="product-review-item">
                  <div class="review-header">
                    <strong class="review-author">{html.escape(r['author'])}</strong>
                    <span class="review-date">{html.escape(r['date'])}</span>
                  </div>
                  <div class="review-stars-row">★★★★★ <span class="review-verified">✓ Tasdiqlangan xaridor</span></div>
                  <p class="review-text">{html.escape(r['body'])}</p>
                </div>"""
        for r in reviews_data
    ])

    # Schemas
    product_ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": title,
        "image": [img_abs],
        "description": description,
        "sku": livi_sku,
        "mpn": livi_sku,
        "brand": {
            "@type": "Brand",
            "name": "Livi Jewelry"
        },
        "manufacturer": {
            "@type": ["Organization", "JewelryStore"],
            "name": "Livi Jewelry",
            "url": f"{SITE_URL}/uz/",
            "logo": f"{SITE_URL}/assets/logo.png",
            "telephone": "+77054510584"
        },
        "material": materials_uz,
        "category": cat_uz,
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "5.0",
            "reviewCount": str(review_count),
            "bestRating": "5",
            "worstRating": "1"
        },
        "review": [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": r["author"]},
                "datePublished": r["date"],
                "reviewBody": r["body"],
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "5",
                    "bestRating": "5",
                    "worstRating": "1"
                }
            }
            for r in reviews_data
        ],
        "offers": {
            "@type": "Offer",
            "url": page_url,
            "priceCurrency": "KZT",
            "price": f"{price:.2f}",
            "priceValidUntil": "2027-12-31",
            "itemCondition": "https://schema.org/NewCondition",
            "availability": "https://schema.org/InStock",
            "seller": {
                "@type": "Organization",
                "name": "Livi Jewelry"
            },
            "hasMerchantReturnPolicy": {
                "@type": "MerchantReturnPolicy",
                "applicableCountry": "KZ",
                "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                "merchantReturnDays": 14,
                "returnMethod": "https://schema.org/ReturnByMail",
                "returnFees": "https://schema.org/FreeReturn"
            },
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {
                    "@type": "MonetaryAmount",
                    "value": "0",
                    "currency": "KZT"
                },
                "shippingDestination": {
                    "@type": "DefinedRegion",
                    "addressCountry": "KZ"
                },
                "deliveryTime": {
                    "@type": "ShippingDeliveryTime",
                    "handlingTime": {
                        "@type": "QuantitativeValue",
                        "minValue": 0,
                        "maxValue": 1,
                        "unitCode": "DAY"
                    },
                    "transitTime": {
                        "@type": "QuantitativeValue",
                        "minValue": 1,
                        "maxValue": 3,
                        "unitCode": "DAY"
                    }
                }
            }
        }
    }

    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Bosh sahifa", "item": f"{SITE_URL}/uz/"},
            {"@type": "ListItem", "position": 2, "name": "Katalog", "item": f"{SITE_URL}/uz/shop.html"},
            {"@type": "ListItem", "position": 3, "name": cat_hub_label, "item": f"{SITE_URL}{cat_hub_url}"},
            {"@type": "ListItem", "position": 4, "name": title, "item": page_url}
        ]
    }

    faq_q1 = f"«{title}» taqinchog‘ida tabiiy toshlar va marvarid qanday ishlatilgan?"
    faq_a1 = f"Ushbu model Livi Jewelry ustaxonasida saralangan tabiiy minerallar ({materials_uz_str}) va yuqori toifadagi marvariddan qo‘lda terilgan. Furniturasi mustahkam gipoallergen qotishmadan iborat."
    faq_q2 = f"«{title}» o‘lchamini o‘zgartirish mumkinmi?"
    faq_a2 = f"Buyum o‘lchami kartochkada ko‘rsatilgan. Uzunlikni o‘zgartirish imkoniyatini ustadan WhatsApp orqali aniqlang."
    faq_q3 = "Toshkentga va O‘zbekistonga yetkazib berish hamda to‘lov qanday bo‘ladi?"
    faq_a3 = "O‘zbekistonga jo‘natish CDEK yoki Qazpost orqali kuzatuv treking-kodi bilan amalga oshiriladi. To‘lov «Zolotaya Korona» (KoronaPay) yoki menejer bilan WhatsApp orqali tasdiqlanadi. Sovg‘a qadog‘i bepul qo‘shiladi."

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": faq_q1, "acceptedAnswer": {"@type": "Answer", "text": faq_a1}},
            {"@type": "Question", "name": faq_q2, "acceptedAnswer": {"@type": "Answer", "text": faq_a2}},
            {"@type": "Question", "name": faq_q3, "acceptedAnswer": {"@type": "Answer", "text": faq_a3}}
        ]
    }

    # Bundle block HTML
    bundle_block_html = ""
    if bundle_options:
        opts_html = "\n".join([
            f'              <option value="{html.escape(opt["name"])}" data-price="{opt["price"]}">{html.escape(opt["name"])} — {format_price_uz(opt["price"])} ₸</option>'
            for opt in bundle_options
        ])
        bundle_block_html = f"""
        <div class="product-customizer-group" style="margin-bottom:18px;">
          <label class="customizer-label" for="customBundle"><strong>To‘plam tarkibini tanlash:</strong></label>
          <div class="custom-select-wrap">
            <select id="customBundle" class="product-bundle-select" aria-label="To‘plam tarkibini tanlash">
{opts_html}
            </select>
          </div>
          <p class="customizer-hint" style="font-size:12px;color:var(--muted);margin-top:4px;">Har bir buyumni alohida yoki to‘liq to‘plam sifatida xarid qilishingiz mumkin.</p>
        </div>"""

    drawer_hub_links_uz = "\n".join(
        f'            <a href="{h_url}">{html.escape(h_lbl)}</a>'
        for h_url, h_lbl in ALL_21_HUBS
    )

    product_js_obj = json.dumps({
        "id": pid,
        "title": title,
        "price": price,
        "category": category,
        "image": pk["image"],
        "bundle_options": bundle_options
    }, ensure_ascii=False)

    return f"""<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />

  <title>{html.escape(page_title)}</title>
  <meta name="description" content="{html.escape(meta_desc)}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="canonical" href="{page_url}" />
  <link rel="alternate" hreflang="ru-KZ" href="{ru_page_url}" />
  <link rel="alternate" hreflang="ru" href="{ru_page_url}" />
  <link rel="alternate" hreflang="kk-KZ" href="{kz_page_url}" />
  <link rel="alternate" hreflang="kk" href="{kz_page_url}" />
  <link rel="alternate" hreflang="uz-UZ" href="{page_url}" />
  <link rel="alternate" hreflang="uz" href="{page_url}" />
  <link rel="alternate" hreflang="x-default" href="{ru_page_url}" />

  <meta name="google-site-verification" content="{GOOGLE_VERIFICATION}" />
  <meta name="facebook-domain-verification" content="{FB_DOMAIN_VERIFICATION}" />

  <!-- Open Graph -->
  <meta property="og:type" content="product" />
  <meta property="og:site_name" content="Livi Jewelry" />
  <meta property="og:locale" content="uz_UZ" />
  <meta property="og:title" content="{html.escape(page_title)}" />
  <meta property="og:description" content="{html.escape(meta_desc)}" />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:image" content="{img_abs}" />
  <meta property="product:price:amount" content="{price}" />
  <meta property="product:price:currency" content="KZT" />
  <meta property="product:availability" content="in stock" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(page_title)}" />
  <meta name="twitter:description" content="{html.escape(meta_desc)}" />
  <meta name="twitter:image" content="{img_abs}" />

  <link rel="icon" type="image/png" href="/assets/logo.png">
  <link rel="apple-touch-icon" href="/assets/logo.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">

  <!-- Schema.org JSON-LD: Product -->
  <script type="application/ld+json">
{json.dumps(product_ld, ensure_ascii=False, indent=2)}
  </script>

  <!-- Schema.org JSON-LD: BreadcrumbList -->
  <script type="application/ld+json">
{json.dumps(breadcrumb_ld, ensure_ascii=False, indent=2)}
  </script>

  <!-- Schema.org JSON-LD: FAQPage -->
  <script type="application/ld+json">
{json.dumps(faq_ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <!-- Drawer -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back" role="button" tabindex="0" aria-label="Menyuni yopish"></div>
    <div class="drawer-panel" role="menu" aria-label="Menyu">
      <a href="/uz/">Bosh sahifa</a>
      <a href="/uz/shop.html">Katalog</a>
      <details class="drawer-accordion">
        <summary>To‘plamlar va toshlar</summary>
        <div class="drawer-subnav">
{drawer_hub_links_uz}
        </div>
      </details>
      <a href="/uz/komplekty-ukrasheniy.html">To‘plamlar</a>
      <a href="/uz/delivery.html">Yetkazib berish va to‘lov</a>
      <div class="drawer-socials">
        <a class="drawer-soc-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="drawer-soc-link" href="https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener">WhatsApp</a>
      </div>
      <div class="lang">
        <a href="{ru_page_url}">RU</a>
        <a href="{kz_page_url}">KZ</a>
        <a href="{page_url}" class="active">UZ</a>
      </div>
    </div>
  </div>

  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Menyu"><span></span></button>
      <a class="brand" href="/uz/" aria-label="Livi Jewelry">
        <span>LIVI JEWELRY</span>
      </a>
      <div class="nav-actions">
        <div class="header-lang-links" aria-label="Tilni tanlash">
          <a href="{ru_page_url}" lang="ru">RU</a>
          <a href="{kz_page_url}" lang="kk">KZ</a>
          <a href="{page_url}" class="active" lang="uz">UZ</a>
        </div>
        <a class="cart-link" href="/uz/cart.html" aria-label="Savatcha">
          <span>Savatcha</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
        <a class="quick-link ig-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener" aria-label="Instagram">
          <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
            <path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm5 5.5A4.5 4.5 0 1 0 16.5 12 4.505 4.505 0 0 0 12 7.5zm6.5-.75a1.25 1.25 0 1 0 1.25 1.25A1.25 1.25 0 0 0 18.5 6.75Zm-6.5 2A3.25 3.25 0 1 1 8.75 12 3.254 3.254 0 0 1 12 8.75Z"/>
          </svg>
        </a>
        <a class="quick-link wa-link" href="https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener" aria-label="WhatsApp">
          <svg width="20" height="20" viewBox="0 0 32 32" aria-hidden="true" fill="currentColor">
            <path d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
            <path d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
          </svg>
        </a>
      </div>
    </div>
  </header>

  <main class="product-page">
    <!-- Non bo‘laklari -->
    <nav class="breadcrumbs" aria-label="Non bo‘laklari">
      <a href="/uz/">Bosh sahifa</a>
      <span class="sep">/</span>
      <a href="/uz/shop.html">Katalog</a>
      <span class="sep">/</span>
      <a href="{cat_hub_url}">{html.escape(cat_hub_label)}</a>
      <span class="sep">/</span>
      <span class="current" aria-current="page">{html.escape(title)}</span>
    </nav>

    <div class="product-layout">
      <!-- Rasm galereyasi -->
      <div class="product-gallery">
        <div class="product-main-img-wrap">
          <img src="{pk['image']}" alt="{html.escape(title)} — qo‘lda yasalgan ({materials_uz_str}), Livi Jewelry" class="product-main-img" id="mainProductImg" width="600" height="800" fetchpriority="high">
        </div>
      </div>

      <!-- Mahsulot ma’lumotlari -->
      <div class="product-info-col">
        <div class="product-header">
          <div class="product-sku-badge" style="font-size:12px;color:var(--muted);letter-spacing:0.05em;margin-bottom:4px;">Artikul: {livi_sku}</div>
          <h1 class="product-title">{html.escape(title)}</h1>
          <div class="product-price-row">
            <span class="product-current-price" id="activePriceDisplay">{price_fmt} ₸</span>
            <span class="product-stock-tag in-stock">✓ Sotuvda mavjud</span>
          </div>
        </div>

        <div class="product-materials-block">
          <div class="mat-label" style="font-size:12px;color:var(--muted);margin-bottom:6px;">Tabiiy materiallar va toshlar:</div>
          <div class="mat-pills-row">
            {material_pills}
          </div>
        </div>

        <!-- Komplektatsiyani tanlash -->
        {bundle_block_html}

        <!-- Buyurtma berish tugmalari -->
        <div class="product-actions-box">
          <button type="button" class="btn primary btn-buy-wa" id="buyWaBtn" style="width:100%;margin-bottom:10px;">
            WhatsApp orqali buyurtma berish ({price_fmt} ₸)
          </button>
          <button type="button" class="btn secondary btn-add-cart" id="addToCartBtn" style="width:100%;">
            Savatchaga qo‘shish
          </button>
        </div>

        <div id="addedToast" class="cart-toast" style="display:none;background:#2e7d32;color:#fff;padding:10px 14px;border-radius:6px;font-size:13px;margin-top:10px;text-align:center;">
          ✓ Mahsulot savatchaga muvaffaqiyatli qo‘shildi!
        </div>

        <!-- Tavsif -->
        <div class="product-desc-block" style="margin-top:24px;">
          <h2 style="font-size:18px;margin-bottom:8px;">Taqinchoq haqida ma’lumot</h2>
          <p class="product-desc-text" style="line-height:1.6;color:var(--text);">{html.escape(description)}</p>
        </div>

        <!-- 7 qatorli xususiyatlar jadvali -->
        <div class="product-specs-section" style="margin-top:28px;">
          <h2 style="font-size:18px;margin-bottom:12px;">Mahsulot xususiyatlari</h2>
          <dl class="product-specs-grid">
            <div class="spec-row">
              <dt>Buyum turi:</dt>
              <dd>{html.escape(type_uz)}</dd>
            </div>
            <div class="spec-row">
              <dt>Asosiy toshlar va marvarid:</dt>
              <dd>{html.escape(stones_detail_uz)}</dd>
            </div>
            <div class="spec-row">
              <dt>O‘lchami / Uzunligi:</dt>
              <dd>{html.escape(length_uz)}</dd>
            </div>
            <div class="spec-row">
              <dt>Metall va furnitura:</dt>
              <dd>{html.escape(hardware_uz)}</dd>
            </div>
            <div class="spec-row">
              <dt>Zargarlik qulfi:</dt>
              <dd>{html.escape(clasp_uz)}</dd>
            </div>
            <div class="spec-row">
              <dt>Sovg‘a qadog‘i:</dt>
              <dd>{html.escape(packaging_uz)}</dd>
            </div>
            <div class="spec-row">
              <dt>Yetkazib berish:</dt>
              <dd>{html.escape(delivery_uz)}</dd>
            </div>
          </dl>
        </div>

        <!-- Yetkazib berish va servis bloki -->
        <div class="product-delivery-card" style="margin-top:24px;background:#FAF8F5;border:1px solid rgba(0,0,0,0.06);border-radius:8px;padding:16px;">
          <h3 style="font-size:15px;margin-bottom:8px;">O‘zbekiston, Qozog‘iston va dunyo bo‘ylab servis</h3>
          <ul style="font-size:13px;line-height:1.5;color:#555;padding-left:18px;margin:0;">
            <li><strong>O‘zbekistonga yetkazib berish:</strong> Toshkent, Samarqand, Buxoro va barcha hududlarga CDEK yoki Qazpost orqali kuzatuv treking-raqami bilan 2–5 kunda yetkaziladi.</li>
            <li><strong>O‘zbekistondan to‘lov:</strong> «Zolotaya Korona» (KoronaPay) pul o‘tkazmasi orqali yoki WhatsApp menejeri orqali oson to‘lov.</li>
            <li><strong>Ostona va Qozog‘iston:</strong> Ostonada kun davomida kuryer, Olmaota va Qozog‘iston shaharlariga 1–3 ish kunida CDEK orqali.</li>
            <li><strong>14 kunlik kafolat:</strong> Tovar ko‘rinishi saqlangan holda mahsulotni 14 kun ichida almashtirish yoki qaytarish imkoniyati.</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Ko‘p beriladigan savollar (FAQ) -->
    <section class="product-faq-section" style="margin-top:40px;">
      <h2 style="font-size:22px;margin-bottom:16px;">«{html.escape(title)}» bo‘yicha ko‘p beriladigan savollar</h2>
      <div class="faq-list">
        <details class="faq-item" open>
          <summary>{html.escape(faq_q1)}</summary>
          <div class="faq-answer">{html.escape(faq_a1)}</div>
        </details>
        <details class="faq-item">
          <summary>{html.escape(faq_q2)}</summary>
          <div class="faq-answer">{html.escape(faq_a2)}</div>
        </details>
        <details class="faq-item">
          <summary>{html.escape(faq_q3)}</summary>
          <div class="faq-answer">{html.escape(faq_a3)}</div>
        </details>
      </div>
    </section>

    <!-- Xaridorlar fikrlari -->
    <section class="product-reviews-section" style="margin-top:40px;">
      <div class="reviews-head" style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
        <h2 style="font-size:22px;margin:0;">Xaridorlar baholari va fikrlari (5.0 ★)</h2>
        <span class="reviews-count-badge" style="font-size:13px;color:var(--muted);">{review_count} ta tasdiqlangan baho</span>
      </div>
      <div class="product-reviews-list">
        {reviews_uz_items_html}
      </div>
    </section>
  </main>

  <footer id="contact">
    <div class="foot">
      <div class="links">
        <a href="/uz/delivery.html">Yetkazib berish, to‘lov va qaytarish (14 kun)</a>
        <a href="/uz/privacy.html">Maxfiylik siyosati</a>
        <a href="/uz/terms.html">Foydalanish shartlari</a>
        <a href="/uz/shop.html">Katalog</a>
        <a href="{ru_page_url}">Русская версия</a>
        <a href="{kz_page_url}">Қазақша нұсқа</a>
      </div>
      <div class="copy">© <span id="year">2026</span> Livi Jewelry — Barcha huquqlar himoyalangan.</div>
      <div class="links">
        <a class="tag" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="tag" href="https://wa.me/77054510584" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
  </footer>

  <!-- Floating WhatsApp Widget -->
  <a class="floating-wa" href="https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20maslahat%20olmoqchiman." target="_blank" rel="noopener" aria-label="WhatsApp orqali maslahat olish">
    <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true">
      <path fill="currentColor" d="M16 2.9A13.1 13.1 0 0 0 2.9 16c0 2.3.6 4.5 1.8 6.5L2 30l7.8-2.5A13 13 0 0 0 16 29a13.1 13.1 0 0 0 0-26.2Zm0 23.8c-2.2 0-4.2-.6-6.1-1.8l-.4-.2-4.6 1.5 1.5-4.5-.3-.4a11.1 11.1 0 1 1 9.9 5.4Z"/>
      <path fill="currentColor" d="M12.3 10.7c-.2-.6-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-1 1-1 2.4s1.1 2.8 1.3 3 .2.4.3.5c.2.3 2 3.2 5 4.3.7.3 1.3.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.2.2-1.3-.1-.1-.2-.2-.5-.4-.2-.1-1.3-.6-1.5-.6s-.3 0-.5.3c-.2.3-.6.8-.7.9-.1.2-.3.2-.5.1-.2 0-.9-.3-1.7-.8-.6-.3-1.1-.9-1.3-1-.1-.2 0-.4.1-.5.1-.1.3-.3.4-.4.2-.2.3-.3.4-.5.1-.2.1-.3 0-.5-.1-.1-.5-1.1-.7-1.5-.2-.4-.3-.4-.5-.5h-.4Z"/>
    </svg>
    <span class="floating-wa-text">Usta maslahati</span>
  </a>

  <script>
    const PRODUCT = {product_js_obj};
    let currentActivePrice = PRODUCT.price;
    let currentActiveTitle = PRODUCT.title;

    (function captureAttribution(){{
      try {{
        const params = new URLSearchParams(window.location.search);
        const existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}');
        const keys = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','fbclid','yclid'];
        let hasNew = false;
        keys.forEach(k => {{
          const val = params.get(k);
          if(val) {{ existing[k] = val; hasNew = true; }}
        }});
        if(!existing.landing_page) existing.landing_page = window.location.pathname + window.location.search;
        if(!existing.referrer && document.referrer) existing.referrer = document.referrer;
        if(!existing.first_visit) existing.first_visit = new Date().toISOString();
        if(hasNew || !localStorage.getItem('livi_attribution')) {{
          localStorage.setItem('livi_attribution', JSON.stringify(existing));
        }}
      }} catch(e){{}}
    }})();

    const drawer = document.getElementById('drawer'), burger = document.getElementById('burger');
    if(burger && drawer){{
      burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden','false'); document.body.classList.add('drawer-open'); }};
      drawer.querySelector('.drawer-back').onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden','true'); document.body.classList.remove('drawer-open'); }};
    }}

    function updateBadge(){{
      try {{
        const raw = localStorage.getItem('livi_cart_v3') || '[]';
        const items = JSON.parse(raw);
        const count = Array.isArray(items) ? items.reduce((s,i)=>s+Number(i.qty||0),0) : 0;
        const b = document.getElementById('cartBadge');
        if(b) {{
          b.textContent = count > 0 ? count : '';
          b.style.display = count > 0 ? 'inline-block' : 'none';
        }}
      }} catch(e){{}}
    }}
    updateBadge();

    const bundleSelect = document.getElementById('customBundle');
    const priceDisplay = document.getElementById('activePriceDisplay');
    const buyWaBtn = document.getElementById('buyWaBtn');

    function updateWaLink(){{
      const bundleVal = bundleSelect ? bundleSelect.value : '';
      const text = `Salom, Livi Jewelry! Menga «${{currentActiveTitle}}» (artikul: ${{PRODUCT.id}}) taqinchog‘i yoqdi. Narxi: ${{currentActivePrice.toLocaleString('ru-RU').replace(/,/g, ' ')}} ₸. Buyurtma berishda yordam bera olasizmi?`;
      const url = 'https://wa.me/77054510584?text=' + encodeURIComponent(text);
      if(buyWaBtn) buyWaBtn.onclick = () => {{ window.open(url, '_blank'); }};
    }}

    if(bundleSelect){{
      bundleSelect.addEventListener('change', () => {{
        const opt = bundleSelect.options[bundleSelect.selectedIndex];
        const p = Number(opt.getAttribute('data-price') || PRODUCT.price);
        currentActivePrice = p;
        currentActiveTitle = opt.value;
        if(priceDisplay) priceDisplay.textContent = p.toLocaleString('ru-RU').replace(/,/g, ' ') + ' ₸';
        if(buyWaBtn) buyWaBtn.textContent = `WhatsApp orqali buyurtma berish (${{p.toLocaleString('ru-RU').replace(/,/g, ' ')}} ₸)`;
        updateWaLink();
      }});
    }}

    updateWaLink();

    const addBtn = document.getElementById('addToCartBtn');
    if(addBtn){{
      addBtn.onclick = () => {{
        let cart = [];
        try {{ cart = JSON.parse(localStorage.getItem('livi_cart_v3') || '[]'); }} catch(e){{}}
        const bundleOpt = bundleSelect ? bundleSelect.value : '';
        const itemIdx = cart.findIndex(i => i.id === PRODUCT.id && (i.customBundle || '') === bundleOpt);
        if(itemIdx > -1){{
          cart[itemIdx].qty = (cart[itemIdx].qty || 1) + 1;
        }} else {{
          cart.push({{
            id: PRODUCT.id,
            title: currentActiveTitle,
            price: currentActivePrice,
            image: PRODUCT.image,
            category: PRODUCT.category,
            qty: 1,
            customBundle: bundleOpt,
            bundleOption: bundleOpt,
            unitPrice: currentActivePrice
          }});
        }}
        try {{
          localStorage.setItem('livi_cart_v3', JSON.stringify(cart));
          updateBadge();
        }} catch(e){{}}

        const toast = document.getElementById('addedToast');
        if(toast){{
          toast.style.display = 'block';
          setTimeout(() => {{ toast.style.display = 'none'; }}, 5000);
        }}
      }};
    }}

    // WhatsApp Order Button and Global WhatsApp tracking
    const waOrderBtnEl = document.getElementById('waOrderBtn');
    if (waOrderBtnEl) {{
      waOrderBtnEl.addEventListener('click', function() {{
        try {{
          if (window.fbq) fbq('track', 'Contact');
          if (typeof gtag === 'function') {{
            gtag('event', 'whatsapp_click', {{
              currency: 'KZT',
              value: currentActivePrice,
              method: 'WhatsApp',
              page_location: window.location.href,
              lead_source: 'uz_product_' + PRODUCT.id
            }});
            gtag('event', 'contact', {{
              currency: 'KZT',
              value: currentActivePrice,
              method: 'WhatsApp',
              page_location: window.location.href,
              lead_source: 'uz_product_' + PRODUCT.id
            }});
            gtag('event', 'generate_lead', {{
              currency: 'KZT',
              value: currentActivePrice,
              method: 'WhatsApp',
              lead_source: 'uz_product_' + PRODUCT.id
            }});
          }}
        }} catch(e){{}}
      }});
    }}

    document.addEventListener('click', function(e) {{
      const a = e.target.closest('a[href*="wa.me"], a[href*="whatsapp.com"]');
      if (!a || a.id === 'waOrderBtn') return;
      try {{
        if (window.fbq) fbq('track', 'Contact');
        if (typeof gtag === 'function') {{
          gtag('event', 'whatsapp_click', {{
            currency: 'KZT',
            value: (typeof currentActivePrice !== 'undefined' ? currentActivePrice : 40000),
            method: 'WhatsApp',
            page_location: window.location.href,
            lead_source: 'uz_wa_link'
          }});
          gtag('event', 'contact', {{
            currency: 'KZT',
            value: (typeof currentActivePrice !== 'undefined' ? currentActivePrice : 40000),
            method: 'WhatsApp',
            page_location: window.location.href,
            lead_source: 'uz_wa_link'
          }});
          gtag('event', 'generate_lead', {{
            currency: 'KZT',
            value: (typeof currentActivePrice !== 'undefined' ? currentActivePrice : 40000),
            method: 'WhatsApp',
            page_location: window.location.href,
            lead_source: 'uz_wa_link'
          }});
        }}
      }} catch(err){{}}
    }});
  </script>
</body>
</html>
"""


def generate_uz_service_pages():
    os.makedirs("uz", exist_ok=True)

    # 1. uz/cart.html
    cart_html = f"""<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
  <title>Livi Jewelry — Savatcha</title>

  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="{SITE_URL}/uz/cart.html">
  <link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/cart.html" />
  <link rel="alternate" hreflang="ru" href="{SITE_URL}/cart.html" />
  <link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/cart.html" />
  <link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/cart.html" />
  <link rel="alternate" hreflang="uz-UZ" href="{SITE_URL}/uz/cart.html" />
  <link rel="alternate" hreflang="uz" href="{SITE_URL}/uz/cart.html" />
  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/cart.html" />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">

  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
  <link rel="icon" href="/favicon.ico" sizes="any">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{ dataLayer.push(arguments); }}
    gtag('consent', 'default', {{
      'ad_storage': 'granted',
      'analytics_storage': 'granted',
      'ad_user_data': 'granted',
      'ad_personalization': 'granted',
      'wait_for_update': 500
    }});
    gtag('set', 'url_passthrough', true);
    gtag('set', 'ads_data_redaction', false);
    gtag('js', new Date());
    gtag('config', '{GA_ID}', {{ 'linker': {{ 'domains': ['livijewelry.kz'] }} }});
    gtag('config', '{AW_ID}', {{ 'allow_enhanced_conversions': true, 'linker': {{ 'domains': ['livijewelry.kz'] }} }});
  </script>

  <!-- Meta Pixel Code -->
  <script>
    !function(f,b,e,v,n,t,s)
    {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '{FB_PIXEL_1}');
    fbq('init', '{FB_PIXEL_2}');
    fbq('track', 'PageView');
  </script>
</head>
<body>
  <!-- Drawer -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back" role="button" tabindex="0" aria-label="Menyuni yopish"></div>
    <div class="drawer-panel" role="menu" aria-label="Menyu">
      <a href="/uz/">Bosh sahifa</a>
      <a href="/uz/shop.html">Katalog</a>
      <a href="/uz/komplekty-ukrasheniy.html">To‘plamlar</a>
      <a href="/uz/delivery.html">Yetkazib berish va to‘lov</a>
      <div class="drawer-socials">
        <a class="drawer-soc-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="drawer-soc-link" href="https://wa.me/77054510584?text=Salom!%20Livi%20Jewelry%20taqinchoqlari%20bo‘yicha%20savatchadan%20yozmoqdaman." target="_blank" rel="noopener">WhatsApp</a>
      </div>
      <div class="lang">
        <a href="/cart.html" id="ruBtn">RU</a>
        <a href="/kz/cart.html" id="kkBtn">KZ</a>
        <a href="/uz/cart.html" id="uzBtn" class="active">UZ</a>
      </div>
    </div>
  </div>

  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Menyu"><span></span></button>
      <a class="brand" href="/uz/" aria-label="Livi Jewelry">
        <span>LIVI JEWELRY</span>
      </a>
      <div class="nav-actions">
        <div class="header-lang-links" aria-label="Tilni tanlash">
          <a href="/cart.html" lang="ru">RU</a>
          <a href="/kz/cart.html" lang="kk">KZ</a>
          <a href="/uz/cart.html" class="active" lang="uz">UZ</a>
        </div>
        <a class="cart-link" href="/uz/cart.html" aria-label="Savatcha">
          <span>Savatcha</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
      </div>
    </div>
  </header>

  <main class="wrap cart-wrap">
    <h1>Savatcha</h1>
    <div id="root"></div>
  </main>

  <!-- Success Modal -->
  <div id="successModal" class="modal-overlay" aria-hidden="true">
    <div class="modal-box" role="dialog" aria-modal="true">
      <div class="modal-badge">✓</div>
      <h2 class="modal-title">Buyurtma shakllantirildi!</h2>
      <div id="modalOrderNo" class="modal-order-no">Buyurtma № LV-2410-UZ</div>
      
      <div class="modal-steps">
        <ul>
          <li>
            <span class="step-num">1</span>
            <div><strong>WhatsApp orqali to‘g‘ridan-to‘g‘ri yuborish</strong><br>Hozir tayyor buyurtma ma’lumotlari bilan WhatsApp ochiladi — buyurtmani tasdiqlash uchun «Yuborish» tugmasini bosing.</div>
          </li>
          <li>
            <span class="step-num">2</span>
            <div><strong>To‘lov va rekvizitlar</strong><br>O‘zbekiston uchun to‘lov «Zolotaya Korona» (KoronaPay) yoki karta rekvizitlari orqali menejer bilan tasdiqlanadi. Qozog‘istondan esa Kaspi Pay orqali hisob yuboriladi.</div>
          </li>
          <li>
            <span class="step-num">3</span>
            <div><strong>CDEK / Qazpost orqali jo‘natish</strong><br>To‘lovdan so‘ng taqinchoq ehtiyotkorlik bilan qadoqlanib, kuryerlik xizmatiga topshiriladi va treking-raqami ushbu WhatsApp chatiga yuboriladi.</div>
          </li>
        </ul>
      </div>

      <div class="modal-actions">
        <button id="modalCloseBtn" class="btn-modal-close">Katalogga qaytish</button>
        <a id="modalWaBtn" class="btn-alt-wa" target="_blank" rel="noopener">WhatsApp orqali yuborish</a>
      </div>
    </div>
  </div>

  <script>
    (function captureAttribution(){{
      try {{
        const params = new URLSearchParams(window.location.search);
        const existing = JSON.parse(localStorage.getItem('livi_attribution') || '{{}}');
        const keys = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','fbclid','yclid'];
        let hasNew = false;
        keys.forEach(k => {{
          const val = params.get(k);
          if(val) {{ existing[k] = val; hasNew = true; }}
        }});
        if(!existing.landing_page) existing.landing_page = window.location.pathname + window.location.search;
        if(!existing.referrer && document.referrer) existing.referrer = document.referrer;
        if(!existing.first_visit) existing.first_visit = new Date().toISOString();
        if(hasNew || !localStorage.getItem('livi_attribution')) {{
          localStorage.setItem('livi_attribution', JSON.stringify(existing));
        }}
      }} catch(e){{}}
    }})();

    const WA_PHONE = '77054510584';

    function readCart(){{
      try {{ return JSON.parse(localStorage.getItem('livi_cart_v3') || '[]'); }} catch(e){{ return []; }}
    }}
    function writeCart(c){{
      try {{ localStorage.setItem('livi_cart_v3', JSON.stringify(c)); }} catch(e){{}}
    }}

    function renderCart(){{
      const root = document.getElementById('root');
      const cart = readCart();
      const badge = document.getElementById('cartBadge');
      const totalCount = cart.reduce((s, i) => s + Number(i.qty || 0), 0);
      if(badge){{
        badge.textContent = totalCount > 0 ? totalCount : '';
        badge.style.display = totalCount > 0 ? 'inline-block' : 'none';
      }}

      if(cart.length === 0){{
        root.innerHTML = `
          <div class="cart-empty-box" style="text-align:center;padding:48px 16px;">
            <p style="font-size:18px;color:#777;margin-bottom:20px;">Savatchangiz hozircha bo‘sh.</p>
            <a href="/uz/shop.html" class="btn primary">Katalogga o‘tish</a>
          </div>
        `;
        return;
      }}

      const totalSum = cart.reduce((s, i) => s + (Number(i.unitPrice || i.price || 0) * Number(i.qty || 1)), 0);
      const totalSumFmt = totalSum.toLocaleString('ru-RU').replace(/,/g, ' ');

      const itemsHtml = cart.map((item, idx) => {{
        const uPrice = Number(item.unitPrice || item.price || 0);
        const itemSum = uPrice * Number(item.qty || 1);
        const bundleInfo = item.customBundle ? `<div style="font-size:12px;color:var(--muted);margin-top:2px;">Komplektatsiya: <strong>${{html.escape(item.customBundle)}}</strong></div>` : '';
        return `
          <div class="cart-item" style="display:flex;gap:14px;align-items:center;padding:14px 0;border-bottom:1px solid rgba(0,0,0,0.06);">
            <img src="${{item.image}}" alt="${{html.escape(item.title)}}" style="width:64px;height:80px;object-fit:cover;border-radius:4px;">
            <div style="flex:1;min-width:0;">
              <h3 style="font-size:15px;margin:0 0 4px;"><a href="/uz/product/${{item.id}}.html">${{html.escape(item.title)}}</a></h3>
              ${{bundleInfo}}
              <div style="font-size:14px;color:var(--accent);font-weight:600;margin-top:4px;">${{uPrice.toLocaleString('ru-RU').replace(/,/g, ' ')}} ₸</div>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
              <button type="button" class="btn-qty" onclick="changeQty(${{idx}}, -1)" style="width:28px;height:28px;border:1px solid #ddd;background:#fff;border-radius:4px;cursor:pointer;">-</button>
              <span style="font-weight:600;min-width:20px;text-align:center;">${{item.qty}}</span>
              <button type="button" class="btn-qty" onclick="changeQty(${{idx}}, 1)" style="width:28px;height:28px;border:1px solid #ddd;background:#fff;border-radius:4px;cursor:pointer;">+</button>
            </div>
            <button type="button" onclick="removeItem(${{idx}})" style="background:none;border:none;color:#999;font-size:18px;cursor:pointer;padding:6px;" title="O‘chirish">✕</button>
          </div>
        `;
      }}).join('');

      root.innerHTML = `
        <div class="cart-layout" style="display:grid;grid-template-columns:1fr;gap:32px;">
          <div class="cart-items-col">
            ${{itemsHtml}}
            <div style="display:flex;justify-content:space-between;align-items:center;padding-top:16px;">
              <button type="button" onclick="clearCart()" style="background:none;border:none;color:#888;text-decoration:underline;cursor:pointer;">Savatchani tozalash</button>
              <div style="font-size:18px;font-weight:700;">Jami to‘lov: <span style="color:var(--accent);">${{totalSumFmt}} ₸</span></div>
            </div>
          </div>

          <div class="cart-checkout-card" style="background:#FAF8F5;border:1px solid rgba(0,0,0,0.06);border-radius:8px;padding:24px;">
            <h2 style="font-size:20px;margin-bottom:16px;">Buyurtmani rasmiylashtirish</h2>
            <form id="checkoutForm" onsubmit="handleCheckout(event)">
              <div style="margin-bottom:14px;">
                <label style="display:block;font-size:13px;font-weight:600;margin-bottom:4px;">Ism va familiyangiz *</label>
                <input type="text" id="custName" required placeholder="Masalan: Dilnoza Karimova" style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:6px;box-sizing:border-box;">
                <span style="font-size:11px;color:#777;">CDEK yoki pochtada qabul qilib olish uchun</span>
              </div>
              <div style="margin-bottom:14px;">
                <label style="display:block;font-size:13px;font-weight:600;margin-bottom:4px;">Telefon raqamingiz (WhatsApp) *</label>
                <input type="tel" id="custPhone" required placeholder="+998 90 123 45 67 yoki +7 ..." style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:6px;box-sizing:border-box;">
                <span style="font-size:11px;color:#777;">Buyurtmani tasdiqlash va treking-raqamni yuborish uchun</span>
              </div>
              <div style="margin-bottom:14px;">
                <label style="display:block;font-size:13px;font-weight:600;margin-bottom:4px;">Yetkazib berish shahri va hududi *</label>
                <input type="text" id="custCity" required placeholder="Masalan: Toshkent shahri / Samarqand / Ostona" style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:6px;box-sizing:border-box;">
              </div>
              <div style="margin-bottom:14px;">
                <label style="display:block;font-size:13px;font-weight:600;margin-bottom:4px;">Yetkazib berish usuli:</label>
                <select id="deliveryType" style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:6px;box-sizing:border-box;">
                  <option value="CDEK (O‘zbekiston / Toshkent / PVZ)">CDEK (Toshkent / O‘zbekiston / Tarqatish punkti)</option>
                  <option value="CDEK (Eshikkacha kuryer)">CDEK (Kuryer orqali eshikkacha)</option>
                  <option value="Qazpost / EMS (Xalqaro pochta)">Qazpost / EMS (Xalqaro pochta)</option>
                  <option value="Ostona kuryer (kun davomida)">Ostona bo‘yicha tezkor kuryer</option>
                </select>
              </div>
              <div style="margin-bottom:14px;">
                <label style="display:block;font-size:13px;font-weight:600;margin-bottom:4px;">Yetkazib berish manzili *</label>
                <input type="text" id="custAddr" required placeholder="Ko‘cha, uy, xonadon yoki CDEK PVZ manzili" style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:6px;box-sizing:border-box;">
              </div>
              <div style="margin-bottom:18px;">
                <label style="display:block;font-size:13px;font-weight:600;margin-bottom:4px;">Buyurtmaga izoh (ixtiyoriy)</label>
                <textarea id="custComment" rows="2" placeholder="Bo‘yin o‘lchami, sovg‘a qutisi bo‘yicha tilaklar..." style="width:100%;padding:10px 12px;border:1px solid #ccc;border-radius:6px;box-sizing:border-box;"></textarea>
              </div>

              <div style="background:#fff;border:1px solid rgba(0,0,0,0.06);border-radius:6px;padding:12px;margin-bottom:16px;">
                <strong style="font-size:13px;display:block;margin-bottom:4px;">To‘lov usuli:</strong>
                <p style="font-size:12px;color:#555;margin:0;">O‘zbekistondan: «Zolotaya Korona» (KoronaPay) yoki karta rekvizitlari orqali. Qozog‘istondan: Kaspi Pay orqali masofaviy hisob.</p>
              </div>

              <button type="submit" class="btn primary" style="width:100%;padding:14px;font-size:16px;">
                Buyurtmani WhatsApp orqali tasdiqlash
              </button>
            </form>
          </div>
        </div>
      `;
    }}

    window.changeQty = function(idx, delta){{
      const cart = readCart();
      if(cart[idx]){{
        cart[idx].qty = Math.max(1, (cart[idx].qty || 1) + delta);
        writeCart(cart);
        renderCart();
      }}
    }};

    window.removeItem = function(idx){{
      const cart = readCart();
      cart.splice(idx, 1);
      writeCart(cart);
      renderCart();
    }};

    window.clearCart = function(){{
      writeCart([]);
      renderCart();
    }};

    window.handleCheckout = function(e){{
      e.preventDefault();
      const cart = readCart();
      if(cart.length === 0) return;

      const name = document.getElementById('custName').value.trim();
      const phone = document.getElementById('custPhone').value.trim();
      const city = document.getElementById('custCity').value.trim();
      const delType = document.getElementById('deliveryType').value;
      const addr = document.getElementById('custAddr').value.trim();
      const comment = document.getElementById('custComment').value.trim();

      const orderNo = 'LV-' + Math.floor(1000 + Math.random() * 9000);
      const totalSum = cart.reduce((s, i) => s + (Number(i.unitPrice || i.price || 0) * Number(i.qty || 1)), 0);

      const itemsText = cart.map(i => `• ${{i.title}} ${{i.customBundle ? '('+i.customBundle+')' : ''}} — ${{i.qty}} dona x ${{Number(i.unitPrice||i.price||0).toLocaleString('ru-RU').replace(/,/g, ' ')}} ₸`).join('\n');

      const waMsg = `Salom, Livi Jewelry! Men buyurtma bermoqchiman:\n` +
        `• Buyurtma №: ${{orderNo}}\n` +
        `• Mahsulotlar:\n${{itemsText}}\n` +
        `• Jami to‘lov: ${{totalSum.toLocaleString('ru-RU').replace(/,/g, ' ')}} ₸\n` +
        `• Xaridor: ${{name}}\n` +
        `• Telefon: ${{phone}}\n` +
        `• Shahar: ${{city}}\n` +
        `• Yetkazib berish: ${{delType}}\n` +
        `• Manzil: ${{addr}}` +
        (comment ? `\n• Izoh: ${{comment}}` : '');

      const waUrl = 'https://wa.me/' + WA_PHONE + '?text=' + encodeURIComponent(waMsg);

      const modal = document.getElementById('successModal');
      const modalNo = document.getElementById('modalOrderNo');
      const modalWa = document.getElementById('modalWaBtn');
      if(modalNo) modalNo.textContent = `Buyurtma № ${{orderNo}}`;
      if(modalWa) modalWa.href = waUrl;
      if(modal){{
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
      }}

      // Clear cart
      writeCart([]);
      renderCart();

      const closeBtn = document.getElementById('modalCloseBtn');
      if(closeBtn){{
        closeBtn.onclick = () => {{ window.location.href = '/uz/shop.html'; }};
      }}
    }};

    renderCart();

    const drawer = document.getElementById('drawer'), burger = document.getElementById('burger');
    if(burger && drawer){{
      burger.onclick = () => {{ drawer.classList.add('open'); drawer.setAttribute('aria-hidden','false'); document.body.classList.add('drawer-open'); }};
      drawer.querySelector('.drawer-back').onclick = () => {{ drawer.classList.remove('open'); drawer.setAttribute('aria-hidden','true'); document.body.classList.remove('drawer-open'); }};
    }}
  </script>
</body>
</html>
"""
    safe_write_text(os.path.join("uz", "cart.html"), cart_html)

    # 2. uz/delivery.html
    delivery_html = f"""<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
  <meta name="google-site-verification" content="{GOOGLE_VERIFICATION}" />
  <title>Yetkazib berish, to‘lov va qaytarish | Livi Jewelry — Mualliflik taqinchoqlari</title>
  <meta name="description" content="O‘zbekistonga (Toshkent, Samarqand, Buxoro) va Qozog‘istonga yetkazib berish shartlari, «Zolotaya Korona» va Kaspi orqali to‘lov hamda Livi Jewelry taqinchoqlarini 14 kun ichida qaytarish kafolati.">
  <link rel="canonical" href="{SITE_URL}/uz/delivery.html">
  <link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/delivery.html" />
  <link rel="alternate" hreflang="ru" href="{SITE_URL}/delivery.html" />
  <link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/delivery.html" />
  <link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/delivery.html" />
  <link rel="alternate" hreflang="uz-UZ" href="{SITE_URL}/uz/delivery.html" />
  <link rel="alternate" hreflang="uz" href="{SITE_URL}/uz/delivery.html" />
  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/delivery.html" />
  <meta name="robots" content="index, follow">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="uz_UZ">
  <meta property="og:title" content="Yetkazib berish, to‘lov va qaytarish — Livi Jewelry">
  <meta property="og:description" content="O‘zbekistonga CDEK va Qazpost orqali jo‘natish, «Zolotaya Korona» orqali xavfsiz to‘lov, 14 kunlik qaytarish kafolati.">
  <meta property="og:url" content="{SITE_URL}/uz/delivery.html">
  <meta property="og:image" content="{SITE_URL}/icon-512.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">

  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="icon" href="/favicon.ico" sizes="any">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{ dataLayer.push(arguments); }}
    gtag('consent', 'default', {{
      'ad_storage': 'granted',
      'analytics_storage': 'granted',
      'ad_user_data': 'granted',
      'ad_personalization': 'granted',
      'wait_for_update': 500
    }});
    gtag('set', 'url_passthrough', true);
    gtag('set', 'ads_data_redaction', false);
    gtag('js', new Date());
    gtag('config', '{GA_ID}', {{ 'linker': {{ 'domains': ['livijewelry.kz'] }} }});
    gtag('config', '{AW_ID}', {{ 'allow_enhanced_conversions': true, 'linker': {{ 'domains': ['livijewelry.kz'] }} }});
  </script>

  <!-- Schema.org WebPage & MerchantReturnPolicy -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Yetkazib berish, to‘lov va qaytarish — Livi Jewelry",
    "description": "Livi Jewelry mualliflik taqinchoqlarini O‘zbekiston, Qozog‘iston va butun dunyoga yetkazib berish, to‘lov va qaytarish qoidalari.",
    "url": "{SITE_URL}/uz/delivery.html",
    "mainEntity": {{
      "@type": "MerchantReturnPolicy",
      "name": "Livi Jewelry qaytarish va almashtirish qoidalari",
      "applicableCountry": "KZ",
      "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays": 14,
      "returnMethod": "https://schema.org/ReturnByMail",
      "returnFees": "https://schema.org/FreeReturn",
      "returnShippingFeesAmount": {{
        "@type": "MonetaryAmount",
        "value": "0",
        "currency": "KZT"
      }}
    }}
  }}
  </script>
</head>
<body>
  <!-- Drawer -->
  <div id="drawer" class="drawer" aria-hidden="true">
    <div class="drawer-back" role="button" tabindex="0" aria-label="Menyuni yopish"></div>
    <div class="drawer-panel" role="menu" aria-label="Menyu">
      <a href="/uz/">Bosh sahifa</a>
      <a href="/uz/shop.html">Katalog</a>
      <a href="/uz/komplekty-ukrasheniy.html">To‘plamlar</a>
      <a href="/uz/delivery.html">Yetkazib berish va to‘lov</a>
      <div class="drawer-socials">
        <a class="drawer-soc-link" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="drawer-soc-link" href="https://wa.me/77054510584" target="_blank" rel="noopener">WhatsApp</a>
      </div>
      <div class="lang">
        <a href="/delivery.html" id="ruBtn">RU</a>
        <a href="/kz/delivery.html" id="kkBtn">KZ</a>
        <a href="/uz/delivery.html" id="uzBtn" class="active">UZ</a>
      </div>
    </div>
  </div>

  <header>
    <div class="nav">
      <button id="burger" class="hamburger" aria-label="Menyu"><span></span></button>
      <a class="brand" href="/uz/" aria-label="Livi Jewelry">
        <span>LIVI JEWELRY</span>
      </a>
      <div class="nav-actions">
        <div class="header-lang-links" aria-label="Tilni tanlash">
          <a href="/delivery.html" lang="ru">RU</a>
          <a href="/kz/delivery.html" lang="kk">KZ</a>
          <a href="/uz/delivery.html" class="active" lang="uz">UZ</a>
        </div>
        <a class="cart-link" href="/uz/cart.html" aria-label="Savatcha">
          <span>Savatcha</span> <span id="cartBadge" class="cart-badge" style="display:none"></span>
        </a>
      </div>
    </div>
  </header>

  <main class="wrap service-page" style="padding:32px 16px;max-width:860px;margin:0 auto;">
    <h1 style="font-size:28px;margin-bottom:12px;">Yetkazib berish, to‘lov va 14 kunlik qaytarish kafolati</h1>
    <p style="color:#666;line-height:1.6;margin-bottom:32px;">Livi Jewelry ustaxonasi o‘z mijozlarining xavfsizligi va qulayligini birinchi o‘ringa qo‘yadi. Biz O‘zbekiston, Qozog‘iston va butun dunyo bo‘ylab ishonchli xizmat ko‘rsatamiz.</p>

    <section style="margin-bottom:36px;">
      <h2 style="font-size:20px;border-bottom:2px solid var(--accent);padding-bottom:6px;margin-bottom:16px;">1. Yetkazib berish geografiyasi va muddatlari</h2>
      <ul style="line-height:1.8;color:#444;">
        <li><strong>O‘zbekistonga yetkazib berish:</strong> Toshkent shahri, Samarqand, Buxoro, Andijon, Farg‘ona, Namangan va barcha viloyat markazlariga xalqaro kuryerlik xizmati <strong>CDEK</strong> yoki <strong>Qazpost (EMS)</strong> orqali yetkaziladi. Yetkazib berish muddati: 2–5 ish kuni. Barcha posilkalar qabul qilingan vaqtdan boshlab onlayn treking-raqami (track-number) bilan ta’minlanadi.</li>
        <li><strong>Ostona bo‘yicha:</strong> Buyurtma berilgan kunda tezkor kuryer orqali eshikkacha (kun davomida) bepul yetkazib berish.</li>
        <li><strong>Qozog‘iston bo‘ylab:</strong> Olmaota, Shymkent, Qarag‘anda va boshqa shaharlarga CDEK orqali 1–3 ish kunida.</li>
        <li><strong>Xalqaro yetkazib berish (Worldwide shipping):</strong> Dunyoning istalgan nuqtasiga tezkor kuryerlik pochtasi orqali jo‘natiladi.</li>
      </ul>
    </section>

    <section style="margin-bottom:36px;">
      <h2 style="font-size:20px;border-bottom:2px solid var(--accent);padding-bottom:6px;margin-bottom:16px;">2. Xavfsiz to‘lov usullari</h2>
      <ul style="line-height:1.8;color:#444;">
        <li><strong>O‘zbekistondan to‘lov:</strong> Xalqaro <strong>«Zolotaya Korona» (KoronaPay)</strong> tizimi orqali to‘lov yoki buyurtmani rasmiylashtirishda WhatsApp menejeri orqali xavfsiz rekvizitlar asosida qabul qilinadi.</li>
        <li><strong>Qozog‘istondan to‘lov:</strong> Kaspi.kz mobil ilovasida «IP Livi Jewelry» nomidan masofaviy hisob (Kaspi Pay) orqali 1 daqiqada.</li>
        <li>Barcha to‘lovlar buyurtma tafsilotlari usta bilan WhatsApp’da kelishib olingandan so‘ng amalga oshiriladi.</li>
      </ul>
    </section>

    <section style="margin-bottom:36px;">
      <h2 style="font-size:20px;border-bottom:2px solid var(--accent);padding-bottom:6px;margin-bottom:16px;">3. 14 kunlik qaytarish va almashtirish siyosati</h2>
      <p style="line-height:1.6;color:#444;">Agar taqinchoq biron sababga ko‘ra sizga ma’qul kelmasa, qabul qilib olgan kundan boshlab <strong>14 taqvimiy kun</strong> ichida uni almashtirish yoki to‘lovni qaytarib olish huquqiga egasiz:</p>
      <ul style="line-height:1.8;color:#444;">
        <li>Mahsulot ishlatilmagan bo‘lishi, tovar ko‘rinishi va yorliqlari to‘liq saqlangan bo‘lishi lozim;</li>
        <li>Brendning asl sovg‘a qutisi va qadoqlari butun bo‘lishi kerak;</li>
        <li>Mablag‘ mahsulot ustaxonaga yetib kelib tekshirilgandan so‘ng 1–3 ish kuni ichida to‘liq qaytariladi.</li>
      </ul>
    </section>

    <section style="margin-bottom:36px;">
      <h2 style="font-size:20px;border-bottom:2px solid var(--accent);padding-bottom:6px;margin-bottom:16px;">4. Bepul sovg‘a qadog‘i</h2>
      <p style="line-height:1.6;color:#444;">Har bir buyum Livi Jewelry firmasining chiroyli qattiq qutichasiga va ipak lentalar bilan bezatilgan baxmal xaltachasiga joylashtiriladi. Siz qo‘shimcha to‘lov qilmasdan sovg‘a sifatida taqdim etishingiz mumkin.</p>
    </section>
  </main>

  <footer id="contact">
    <div class="foot">
      <div class="links">
        <a href="/uz/delivery.html">Yetkazib berish, to‘lov va qaytarish</a>
        <a href="/uz/privacy.html">Maxfiylik siyosati</a>
        <a href="/uz/terms.html">Foydalanish shartlari</a>
        <a href="/uz/shop.html">Katalog</a>
        <a href="/delivery.html">Русская версия</a>
        <a href="/kz/delivery.html">Қазақша нұсқа</a>
      </div>
      <div class="copy">© <span id="year">2026</span> Livi Jewelry — Barcha huquqlar himoyalangan.</div>
      <div class="links">
        <a class="tag" href="https://instagram.com/livi_jwl" target="_blank" rel="noopener">Instagram</a>
        <a class="tag" href="https://wa.me/77054510584" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
  </footer>
</body>
</html>
"""
    safe_write_text(os.path.join("uz", "delivery.html"), delivery_html)

    # 3. uz/terms.html
    terms_html = f"""<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
  <title>Foydalanish shartlari va ommaviy oferta | Livi Jewelry</title>
  <meta name="description" content="Livi Jewelry mualliflik zargarlik buyumlari internet-do‘konining foydalanish shartlari, xizmat ko‘rsatish qoidalari va ommaviy ofertasi.">
  <link rel="canonical" href="{SITE_URL}/uz/terms.html">
  <link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/terms.html" />
  <link rel="alternate" hreflang="ru" href="{SITE_URL}/terms.html" />
  <link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/terms.html" />
  <link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/terms.html" />
  <link rel="alternate" hreflang="uz-UZ" href="{SITE_URL}/uz/terms.html" />
  <link rel="alternate" hreflang="uz" href="{SITE_URL}/uz/terms.html" />
  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/terms.html" />
  <meta name="robots" content="index, follow">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
</head>
<body>
  <header>
    <div class="nav">
      <a class="brand" href="/uz/"><span>LIVI JEWELRY</span></a>
      <div class="nav-actions">
        <div class="header-lang-links">
          <a href="/terms.html" lang="ru">RU</a>
          <a href="/kz/terms.html" lang="kk">KZ</a>
          <a href="/uz/terms.html" class="active" lang="uz">UZ</a>
        </div>
      </div>
    </div>
  </header>

  <main class="wrap service-page" style="padding:32px 16px;max-width:860px;margin:0 auto;line-height:1.7;">
    <h1>Foydalanish shartlari va ommaviy oferta</h1>
    <p>Ushbu hujjat «Livi Jewelry» internet-do‘konidan (sayt: https://livijewelry.kz) foydalanish tartibi va mualliflik zargarlik buyumlarini xarid qilish shartlarini belgilaydi.</p>
    <h2>1. Umumiy qoidalar</h2>
    <p>Saytda buyurtma berish orqali xaridor ushbu oferta shartlariga to‘liq rozilik bildiradi. Barcha mahsulotlar saralangan tabiiy minerallar va marvaridlardan qo‘lda yasaladi.</p>
    <h2>2. Narxlar va to‘lov</h2>
    <p>Mahsulotlarning rasmiy narxlari Qozog‘iston tengesida (₸ / KZT) ko‘rsatilgan. O‘zbekiston va boshqa davlatlardan to‘lov xalqaro pul o‘tkazmalari («Zolotaya Korona») yoki kelishuv bo‘yicha amalga oshiriladi.</p>
    <h2>3. Yetkazib berish</h2>
    <p>Yetkazib berish kuryerlik xizmatlari (CDEK, Qazpost) orqali amalga oshiriladi. Jo‘natma treking-raqami xaridorga taqdim etiladi.</p>
    <h2>4. Kafolat va qaytarish</h2>
    <p>Xaridor tovar ko‘rinishi saqlangan holda buyumni qabul qilib olgan kundan boshlab 14 kun ichida almashtirish yoki qaytarish huquqiga ega.</p>
  </main>

  <footer id="contact">
    <div class="foot">
      <div class="links">
        <a href="/uz/delivery.html">Yetkazib berish va to‘lov</a>
        <a href="/uz/privacy.html">Maxfiylik siyosati</a>
        <a href="/uz/shop.html">Katalog</a>
        <a href="/terms.html">Русская версия</a>
      </div>
      <div class="copy">© 2026 Livi Jewelry — Barcha huquqlar himoyalangan.</div>
    </div>
  </footer>
</body>
</html>
"""
    safe_write_text(os.path.join("uz", "terms.html"), terms_html)

    # 4. uz/privacy.html
    privacy_html = f"""<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
  <title>Maxfiylik siyosati | Livi Jewelry</title>
  <meta name="description" content="Livi Jewelry internet-do‘koni mijozlarining shaxsiy ma’lumotlarini himoya qilish va maxfiylik siyosati.">
  <link rel="canonical" href="{SITE_URL}/uz/privacy.html">
  <link rel="alternate" hreflang="ru-KZ" href="{SITE_URL}/privacy.html" />
  <link rel="alternate" hreflang="ru" href="{SITE_URL}/privacy.html" />
  <link rel="alternate" hreflang="kk-KZ" href="{SITE_URL}/kz/privacy.html" />
  <link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/privacy.html" />
  <link rel="alternate" hreflang="uz-UZ" href="{SITE_URL}/uz/privacy.html" />
  <link rel="alternate" hreflang="uz" href="{SITE_URL}/uz/privacy.html" />
  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/privacy.html" />
  <meta name="robots" content="index, follow">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
</head>
<body>
  <header>
    <div class="nav">
      <a class="brand" href="/uz/"><span>LIVI JEWELRY</span></a>
      <div class="nav-actions">
        <div class="header-lang-links">
          <a href="/privacy.html" lang="ru">RU</a>
          <a href="/kz/privacy.html" lang="kk">KZ</a>
          <a href="/uz/privacy.html" class="active" lang="uz">UZ</a>
        </div>
      </div>
    </div>
  </header>

  <main class="wrap service-page" style="padding:32px 16px;max-width:860px;margin:0 auto;line-height:1.7;">
    <h1>Maxfiylik siyosati</h1>
    <p>«Livi Jewelry» mijozlarning shaxsiy daxlsizligi va konfidensialligini yuksak qadrlaydi. Ushbu siyosat siz saytimizdan foydalanganda va buyurtma berganda shaxsiy ma’lumotlaringiz qanday to‘planishi va himoyalanishini tushuntiradi.</p>
    <h2>1. To‘planadigan ma’lumotlar</h2>
    <p>Buyurtmani rasmiylashtirish va yetkazib berish maqsadida biz sizning ismingiz, telefon raqamingiz va yetkazib berish manzilingizni qabul qilamiz.</p>
    <h2>2. Ma’lumotlardan foydalanish maqsadi</h2>
    <p>Ma’lumotlar faqat buyurtmani qayta ishlash, to‘lovni tasdiqlash va kuryerlik xizmatiga (CDEK, pochta) topshirish uchun ishlatiladi. Shaxsiy ma’lumotlar hech qachon uchinchi shaxslarga tijoriy maqsadda sotilmaydi yoki berilmaydi.</p>
    <h2>3. Xavfsizlik</h2>
    <p>Biz barcha shaxsiy ma’lumotlarni ruxsatsiz kirish va tarqalishdan himoya qilish uchun zamonaviy xavfsizlik protokollarini qo‘llaymiz.</p>
  </main>

  <footer id="contact">
    <div class="foot">
      <div class="links">
        <a href="/uz/delivery.html">Yetkazib berish va to‘lov</a>
        <a href="/uz/terms.html">Foydalanish shartlari</a>
        <a href="/uz/shop.html">Katalog</a>
        <a href="/privacy.html">Русская версия</a>
      </div>
      <div class="copy">© 2026 Livi Jewelry — Barcha huquqlar himoyalangan.</div>
    </div>
  </footer>
</body>
</html>
"""
    safe_write_text(os.path.join("uz", "privacy.html"), privacy_html)


def generate_uz_pages():
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    active = [p for p in products if p.get("inStock", True)]
    products_uz = [translate_product_uz(p) for p in active]
    all_products_uz = [translate_product_uz(p) for p in products]

    os.makedirs("uz", exist_ok=True)
    os.makedirs(os.path.join("uz", "product"), exist_ok=True)

    # 1. Main UZ Home
    safe_write_text(os.path.join("uz", "index.html"), generate_uz_index(products_uz))

    # 2. Main UZ Shop
    safe_write_text(os.path.join("uz", "shop.html"), generate_uz_shop(products_uz))

    # 3. All 58 UZ Product Pages
    for p in all_products_uz:
        pid = p["id"]
        page_html = build_uz_product_page(p, all_products_uz)
        out_path = os.path.join("uz", "product", f"{pid}.html")
        safe_write_text(out_path, page_html)

    # 4. Service pages
    generate_uz_service_pages()

    print(f"[OK] UZ vitrina muvaffaqiyatli yaratildi: uz/index.html, uz/shop.html, 4 ta servis sahifalari va {len(all_products_uz)} ta uz/product/prod_XX.html kartochkalari.")


if __name__ == "__main__":
    generate_uz_pages()
