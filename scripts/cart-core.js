window.LiviCart = (() => {
  'use strict';

  function parseFirstKZT(priceStr){
    if (typeof priceStr === 'number' && isFinite(priceStr)) return priceStr;
    const str = String(priceStr || '');
    const m = str.match(/([\d\s.,]+)\s*тг/i);
    if(m) return parseInt(m[1].replace(/[^\d]/g,''),10) || 0;
    return parseInt(str.replace(/[^\d]/g,''),10) || 0;
  }
  function parseSumKZT(priceStr){
    if (typeof priceStr === 'number' && isFinite(priceStr)) return priceStr;
    const rx = /([\d\s.,]+)\s*тг/ig;
    let s = 0, m;
    const str = String(priceStr || '');
    while((m = rx.exec(str))!==null){
      s += parseInt(m[1].replace(/[^\d]/g,''),10) || 0;
    }
    return s > 0 ? s : parseFirstKZT(str);
  }
  function unitPrice(item){
    if (!item) return 0;
    if (typeof item.unit === 'number' && isFinite(item.unit) && item.unit > 0) return item.unit;
    if (Number.isFinite(item.unitPrice) && item.unitPrice > 0) return item.unitPrice;
    if (item.customBundle || item.bundleOption) {
      if (typeof item.price === 'number' && isFinite(item.price) && item.price > 0) return item.price;
      const p = parseFirstKZT(item.price);
      if (p > 0) return p;
    }
    const title = (item.title||'').toLowerCase();
    if (title.includes('комплект') && !item.customBundle && !item.bundleOption) {
      const sum = parseSumKZT(item.price);
      return sum > 0 ? sum : parseFirstKZT(item.price);
    }
    return parseFirstKZT(item.price);
  }

  function readCart(){
    try{
      const raw3 = localStorage.getItem('livi_cart_v3');
      if (raw3 !== null) {
        const items = JSON.parse(raw3);
        if (Array.isArray(items)) {
          return items.filter(it => it && typeof it === 'object' && (it.id || it.title));
        }
      }
      const raw2 = localStorage.getItem('livi_cart_v2');
      if (raw2 !== null) {
        const items = JSON.parse(raw2);
        if (Array.isArray(items)) {
          const valid = items.filter(it => it && typeof it === 'object' && (it.id || it.title));
          if (valid.length > 0) {
            localStorage.setItem('livi_cart_v3', JSON.stringify(valid));
          }
          return valid;
        }
      }
      const raw1 = localStorage.getItem('livi_cart');
      if (raw1 !== null) {
        const items = JSON.parse(raw1);
        if (Array.isArray(items)) {
          const valid = items.filter(it => it && typeof it === 'object' && (it.id || it.title));
          if (valid.length > 0) {
            localStorage.setItem('livi_cart_v3', JSON.stringify(valid));
          }
          return valid;
        }
      }
      return [];
    } catch(e){
      return [];
    }
  }
  function writeCart(v){
    try {
      const json = JSON.stringify(v);
      localStorage.setItem('livi_cart_v3', json);
      localStorage.setItem('livi_cart_v2', json);
      localStorage.removeItem('livi_cart');
    } catch(e){}
  }

  function captureAttribution(){
    try {
      const params = new URLSearchParams(window.location.search);
      const existing = JSON.parse(localStorage.getItem('livi_attribution') || '{}');
      const keys = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','gbraid','wbraid','fbclid','yclid'];
      let hasNew = false;
      keys.forEach(k => {
        const val = params.get(k);
        if(val) { existing[k] = val; hasNew = true; }
      });
      if(!existing.landing_page) existing.landing_page = window.location.pathname + window.location.search;
      if(!existing.referrer && document.referrer) existing.referrer = document.referrer;
      if(!existing.first_visit) existing.first_visit = new Date().toISOString();
      if(hasNew || !localStorage.getItem('livi_attribution')) {
        localStorage.setItem('livi_attribution', JSON.stringify(existing));
      }
    } catch(e){}
  }

  function getAttributionObject(){
    try {
      return JSON.parse(localStorage.getItem('livi_attribution') || '{}') || {};
    } catch(e){
      return {};
    }
  }

  function totalPrice(cart) {
    return cart.reduce((sum, item) => sum + unitPrice(item) * Number(item.qty || 1), 0);
  }

  function normalizedPhone(value, locale) {
    if (!/^\+?[\d\s()-]+$/.test(value.trim())) return '';
    const digits = value.replace(/\D/g, '');
    const international = value.trim().startsWith('+');
    if (/^998\d{9}$/.test(digits)) return '+' + digits;
    if (/^77\d{9}$/.test(digits) || (!international && /^87\d{9}$/.test(digits))) {
      return '+7' + digits.slice(1);
    }
    if (international) return '';
    if (locale === 'uz' && /^\d{9}$/.test(digits)) return '+998' + digits;
    if (/^7\d{9}$/.test(digits)) return '+7' + digits;
    return '';
  }

  const phoneErrors = {
    ru: 'Введите корректный номер с кодом +7 или +998.',
    kk: '+7 немесе +998 кодымен дұрыс телефон нөмірін енгізіңіз.',
    uz: '+998 yoki +7 kodi bilan to‘g‘ri telefon raqamini kiriting.',
    en: 'Enter a valid phone number with +7 or +998.'
  };

  function bindPhone(input, locale) {
    const normalize = () => normalizedPhone(input.value, locale);
    function format() {
      const number = normalize();
      if (!number) return;
      input.value = number.startsWith('+998')
        ? number.replace(/^(\+998)(\d{2})(\d{3})(\d{2})(\d{2})$/, '$1 $2 $3 $4 $5')
        : number.replace(/^(\+7)(\d{3})(\d{3})(\d{2})(\d{2})$/, '$1 ($2) $3-$4-$5');
    }
    input.addEventListener('input', () => input.setCustomValidity(''));
    input.addEventListener('blur', format);
    return () => {
      const number = normalize();
      input.setCustomValidity(number ? '' : phoneErrors[locale] || phoneErrors.ru);
      if (number) format();
      else input.reportValidity();
      return number;
    };
  }

  function escapeHtml(value) {
    const entities = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
    return String(value ?? '').replace(/[&<>"']/g, character => entities[character]);
  }

  return Object.freeze({ readCart, writeCart, unitPrice, totalPrice, captureAttribution, getAttributionObject, bindPhone, normalizedPhone, escapeHtml });
})();
