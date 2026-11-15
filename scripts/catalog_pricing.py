#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Единый модуль правил ценообразования каталога Livi Jewelry.
Для комплектов (товаров с реальной разбивкой в bundle_options) в каталоге
отображается цена главного (самого дорогого) отдельного предмета с пометкой «от».
"""

from typing import Optional

PLACEHOLDER_OPTION_NAMES = {
    "Основное украшение комплекта",
    "Дополнительный элемент сета",
}


def _valid_int_price(value) -> Optional[int]:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        iv = int(value)
        return iv if iv > 0 else None
    return None


def real_bundle_options(product: dict) -> list[dict]:
    """
    Возвращает исходный список bundle_options, если это настоящая разбивка комплекта:
    - bundle_options является непустым списком словарей;
    - ни один вариант не носит имя заглушки PLACEHOLDER_OPTION_NAMES;
    - есть хотя бы один вариант с is_full=False и ценой > 0.
    Иначе возвращает [].
    """
    if not isinstance(product, dict):
        return []
    opts = product.get("bundle_options")
    if not isinstance(opts, list) or not opts:
        return []

    has_non_full = False
    for opt in opts:
        if not isinstance(opt, dict):
            return []
        name = str(opt.get("name") or "").strip()
        if name in PLACEHOLDER_OPTION_NAMES:
            return []
        if not opt.get("is_full") and _valid_int_price(opt.get("price")) is not None:
            has_non_full = True

    return opts if has_non_full else []


def has_from_price(product: dict) -> bool:
    return bool(real_bundle_options(product))


def main_bundle_option(product: dict) -> Optional[tuple[int, dict]]:
    """
    Возвращает (orig_index, opt) с максимальной ценой среди is_full=False.
    При равенстве цен выбирается элемент с меньшим исходным индексом.
    """
    opts = real_bundle_options(product)
    if not opts:
        return None

    best_idx = None
    best_opt = None
    best_price = -1
    for idx, opt in enumerate(opts):
        if opt.get("is_full"):
            continue
        p = _valid_int_price(opt.get("price"))
        if p is None:
            continue
        if p > best_price:
            best_price = p
            best_idx = idx
            best_opt = opt

    if best_idx is None or best_opt is None:
        return None
    return best_idx, best_opt


def catalog_price(product: dict) -> int:
    """Цена для витрин и карточек каталога: главный предмет комплекта или полная price."""
    main = main_bundle_option(product)
    if main is not None:
        return int(main[1]["price"])
    return int((product or {}).get("price") or 0)


def ordered_bundle_options(product: dict) -> list[tuple[int, dict]]:
    """
    Возвращает [(orig_index, opt), ...]:
    сначала отдельные предметы (is_full=False) по убыванию цены (стабильно по orig_index),
    затем полный комплект (is_full=True) последним.
    """
    opts = real_bundle_options(product)
    if not opts:
        return []

    non_full = [(i, o) for i, o in enumerate(opts) if not o.get("is_full")]
    full = [(i, o) for i, o in enumerate(opts) if o.get("is_full")]
    non_full.sort(key=lambda pair: (-int(_valid_int_price(pair[1].get("price")) or 0), pair[0]))
    return non_full + full


def full_option_index(product: dict) -> Optional[int]:
    opts = real_bundle_options(product)
    for idx, opt in enumerate(opts):
        if opt.get("is_full"):
            return idx
    return None


def variant_param(orig_index: int, opt: dict) -> str:
    return "full" if opt.get("is_full") else str(orig_index)


def format_price_num(amount: int) -> str:
    return f"{int(amount):,}".replace(",", " ")


def format_from_price(amount: int, lang: str = "ru") -> str:
    amt = format_price_num(amount)
    if lang in ("kz", "kk"):
        return f"{amt} ₸ бастап"
    if lang == "uz":
        return f"{amt} ₸ dan"
    return f"от {amt} ₸"


def price_html(product: dict, lang: str = "ru") -> str:
    amt = format_price_num(catalog_price(product))
    if not has_from_price(product):
        return f"{amt} ₸"
    if lang in ("kz", "kk"):
        return f'{amt} ₸ <span class="price-from">бастап</span>'
    if lang == "uz":
        return f'{amt} ₸ <span class="price-from">dan</span>'
    return f'<span class="price-from">от</span> {amt} ₸'
