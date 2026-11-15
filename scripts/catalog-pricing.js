window.LiviPricing = (() => {
  'use strict';

  const PLACEHOLDER_OPTION_NAMES = new Set([
    'Основное украшение комплекта',
    'Дополнительный элемент сета'
  ]);

  function validIntPrice(value) {
    if (typeof value !== 'number' || !Number.isFinite(value)) return null;
    const iv = Math.trunc(value);
    return iv > 0 ? iv : null;
  }

  function realBundleOptions(product) {
    if (!product || !Array.isArray(product.bundle_options) || product.bundle_options.length === 0) {
      return [];
    }
    let hasNonFull = false;
    for (const opt of product.bundle_options) {
      if (!opt || typeof opt !== 'object') return [];
      const name = String(opt.name || '').trim();
      if (PLACEHOLDER_OPTION_NAMES.has(name)) return [];
      if (!opt.is_full && validIntPrice(opt.price) !== null) {
        hasNonFull = true;
      }
    }
    return hasNonFull ? product.bundle_options : [];
  }

  function hasFromPrice(product) {
    return realBundleOptions(product).length > 0;
  }

  function mainBundleOption(product) {
    const opts = realBundleOptions(product);
    if (!opts.length) return null;
    let bestIdx = -1;
    let bestOpt = null;
    let bestPrice = -1;
    for (let i = 0; i < opts.length; i++) {
      const opt = opts[i];
      if (!opt || opt.is_full) continue;
      const p = validIntPrice(opt.price);
      if (p === null) continue;
      if (p > bestPrice) {
        bestPrice = p;
        bestIdx = i;
        bestOpt = opt;
      }
    }
    return bestIdx >= 0 ? { index: bestIdx, opt: bestOpt } : null;
  }

  function catalogPrice(product) {
    const main = mainBundleOption(product);
    if (main) return Number(main.opt.price) || 0;
    return Number((product && product.price) || 0);
  }

  function formatPriceNum(amount) {
    const num = Math.round(Number(amount) || 0);
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  }

  function formatFromPrice(amount, lang) {
    const amt = formatPriceNum(amount);
    if (lang === 'kz' || lang === 'kk') return `${amt} ₸ бастап`;
    if (lang === 'uz') return `${amt} ₸ dan`;
    return `от ${amt} ₸`;
  }

  function priceHtml(product, lang) {
    const amt = formatPriceNum(catalogPrice(product));
    if (!hasFromPrice(product)) return `${amt} ₸`;
    if (lang === 'kz' || lang === 'kk') return `${amt} ₸ <span class="price-from">бастап</span>`;
    if (lang === 'uz') return `${amt} ₸ <span class="price-from">dan</span>`;
    return `<span class="price-from">от</span> ${amt} ₸`;
  }

  return Object.freeze({
    PLACEHOLDER_OPTION_NAMES,
    realBundleOptions,
    hasFromPrice,
    mainBundleOption,
    catalogPrice,
    formatPriceNum,
    formatFromPrice,
    priceHtml
  });
})();
