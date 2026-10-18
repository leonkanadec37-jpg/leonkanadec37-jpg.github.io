#!/usr/bin/env node
/**
 * scripts/prerender_shop.js
 * Pre-renders all products from products.json into shop.html:
 * 1. Injects static HTML cards into #grid using native CSS classes (.card, .card-img-wrap, .body, .title, .card-title-link, .price)
 *    with direct <a href="/product/prod_XX.html"> links and clean alt text: "[Название] — ручная работа из [камни], Livi Jewelry"
 * 2. Ensures the error block "Ошибка загрузки каталога. Пожалуйста, обновите страницу." is hidden by default (hidden style="display:none")
 *    and only displayed in catch if the product container is empty.
 * 3. Adds/updates valid JSON-LD ItemList in <head>, where each itemListElement has "@type": "ListItem", "position": N, and "url": "https://livijewelry.kz/product/prod_XX.html".
 * 4. Keeps <link rel="canonical" href="https://livijewelry.kz/shop.html"> strictly intact, and replaces href="index.html" with href="/" in menu links.
 * 5. Ensures ?filter=, ?cat=, and ?q= URL parameters automatically filter the catalog.
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const PRODUCTS_PATH = path.join(ROOT_DIR, 'products.json');
const SHOP_PATH = path.join(ROOT_DIR, 'shop.html');

function escapeAttr(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;');
}

function formatStonesGenitive(materials) {
  if (!Array.isArray(materials) || materials.length === 0) {
    return 'натурального жемчуга и камней';
  }
  const stoneFiltered = materials.filter(m => {
    const low = m.toLowerCase();
    return !low.includes('сплав') && !low.includes('позолота') && !low.includes('фурнитура');
  });
  const list = stoneFiltered.length > 0 ? stoneFiltered : materials;

  const genitiveMap = {
    'натуральный жемчуг': 'натурального жемчуга',
    'барочный жемчуг': 'барочного жемчуга',
    'натуральный барочный жемчуг': 'натурального барочного жемчуга',
    'горный хрусталь': 'горного хрусталя',
    'жемчуг майорка': 'жемчуга Майорка',
    'керамические бусины': 'керамических бусин',
    'натуральный малахит': 'натурального малахита',
    'натуральный аметист': 'натурального аметиста',
    'натуральный авантюрин': 'натурального авантюрина',
    'натуральный агат': 'натурального агата',
    'натуральный гранат': 'натурального граната',
    'розовый кварц': 'розового кварца',
    'натуральный жадеит': 'натурального жадеита',
    'тигровый глаз': 'тигрового глаза',
    'натуральный коралл': 'натурального коралла',
    'яшма': 'яшмы',
    'натуральная бирюза': 'натуральной бирюзы',
    'натуральные камни': 'натуральных камней',
    'гематит': 'гематита',
    'натуральный флюорит': 'натурального флюорита',
    'цирконы': 'цирконов',
    'натуральный лазурит': 'натурального лазурита',
    'натуральный нефрит': 'натурального нефрита',
    'ювелирный сплав': 'ювелирного сплава',
    'позолота': 'позолоты',
    'родированная фурнитура': 'родированной фурнитуры'
  };

  const converted = list.map(m => {
    const key = m.trim().toLowerCase();
    return genitiveMap[key] || m.trim().toLowerCase();
  });

  if (converted.length === 1) return converted[0];
  if (converted.length === 2) return `${converted[0]} и ${converted[1]}`;
  return `${converted.slice(0, -1).join(', ')} и ${converted[converted.length - 1]}`;
}

function buildAlt(p) {
  const title = (p.title || '').trim();
  const stones = formatStonesGenitive(p.materials);
  return `${title} — ручная работа из ${stones}, Livi Jewelry`;
}

function formatPriceKzt(price) {
  const num = Number(price) || 0;
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₸';
}

function main() {
  const products = JSON.parse(fs.readFileSync(PRODUCTS_PATH, 'utf8'));
  const activeProducts = products.filter(p => !p.archived);

  let html = fs.readFileSync(SHOP_PATH, 'utf8');

  // 1. Ensure canonical is strictly https://livijewelry.kz/shop.html
  html = html.replace(
    /<link\s+rel="canonical"\s+href="[^"]*">/i,
    '<link rel="canonical" href="https://livijewelry.kz/shop.html">'
  );

  // 2. Replace href="index.html" with href="/" in menu/navigation links
  html = html.replace(/href="index\.html"/g, 'href="/"');

  // 3. Build JSON-LD ItemList with "@type": "ListItem", "position": N, "url": "https://livijewelry.kz/product/prod_XX.html"
  const itemListSchema = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    'itemListElement': activeProducts.map((p, idx) => {
      const pid = p.id;
      const url = `https://livijewelry.kz/product/${pid}.html`;
      const priceStr = `${Number(p.price || 0).toFixed(2)}`;
      const inStock = p.inStock !== false;
      const imgUrl = `https://livijewelry.kz/${String(p.image || '').replace(/^\/+/, '')}`;
      return {
        '@type': 'ListItem',
        'position': idx + 1,
        'url': url,
        'name': p.title,
        'image': imgUrl,
        'description': p.description || p.title,
        'sku': pid,
        'mpn': pid,
        'offers': {
          '@type': 'Offer',
          'url': url,
          'price': priceStr,
          'priceCurrency': 'KZT',
          'availability': inStock ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock'
        }
      };
    })
  };

  const jsonLdScript = `<script type="application/ld+json">\n${JSON.stringify(itemListSchema, null, 2)}\n</script>`;
  const jsonLdRegex = /<script type="application\/ld\+json">\s*\{[\s\S]*?"@type"\s*:\s*"ItemList"[\s\S]*?<\/script>/;
  if (jsonLdRegex.test(html)) {
    html = html.replace(jsonLdRegex, jsonLdScript);
  } else {
    html = html.replace('</head>', `${jsonLdScript}\n</head>`);
  }

  // 4. Generate static product cards HTML for #grid
  const cardsHtml = activeProducts.map(p => {
    const pid = p.id;
    const title = (p.title || '').trim();
    const imgSrc = String(p.image || '').replace(/^\/+/, '');
    const altText = escapeAttr(buildAlt(p));
    const priceStr = formatPriceKzt(p.price);

    return [
      `      <article class="card" data-id="${pid}">`,
      `        <div class="card-img-wrap"><img src="${imgSrc}" alt="${altText}" loading="lazy" decoding="async" width="600" height="800"></div>`,
      `        <div class="body">`,
      `          <div class="title"><a href="/product/${pid}.html" class="card-title-link">${title}</a></div>`,
      `          <div class="price">${priceStr}</div>`,
      `        </div>`,
      `      </article>`
    ].join('\n');
  }).join('\n');

  // 5. Inject static cards into #grid and include hidden catalog error block by default
  const gridWithErrorHtml = [
    `<div class="grid" id="grid">`,
    cardsHtml,
    `    </div>`,
    `    <div id="catalogError" class="empty-state" hidden style="display:none" aria-hidden="true"></div>`
  ].join('\n');

  const gridRegex = /<div class="grid" id="grid">[\s\S]*?<\/div>\s*(?:<div id="catalogError"[^>]*>[\s\S]*?<\/div>\s*)?(?=<\/main>)/;
  if (!gridRegex.test(html)) {
    throw new Error('Could not locate <div class="grid" id="grid">...</main> in shop.html');
  }
  html = html.replace(gridRegex, gridWithErrorHtml + '\n  ');

  // 6. Update client-side JS in shop.html:
  //    - Update altByCat function to produce clean alt without price spam tail
  //    - Ensure ?filter= URL param automatically filters the catalog
  //    - Update catch block so #catalogError is only unhidden if #grid has no product cards
  const altByCatRegex = /function altByCat\([^)]*\)\{[\s\S]*?\n    \}/;
  const newAltByCat = `function altByCat(cat, title, price, materials){
      const stones = Array.isArray(materials) && materials.length
        ? materials.filter(m => !/сплав|позолота|фурнитура/i.test(m)).join(', ').toLowerCase() || materials.join(', ').toLowerCase()
        : 'натурального жемчуга и камней';
      return \`\${title} — ручная работа из \${stones}, Livi Jewelry\`;
    }`;
  if (altByCatRegex.test(html)) {
    html = html.replace(altByCatRegex, newAltByCat);
  }

  html = html.replace(
    /const altText = altByCat\(p\.category,\s*p\.title,\s*p\.price(?:,\s*p\.materials)?\);/,
    'const altText = altByCat(p.category, p.title, p.price, p.materials);'
  );
  html = html.replace(
    /mImg\.alt=altByCat\(p\.category,\s*p\.title(?:,\s*p\.price,\s*p\.materials)?\);/,
    'mImg.alt=altByCat(p.category, p.title, p.price, p.materials);'
  );

  // Update URL search param block to support ?filter=, ?cat= and ?q=
  const urlParamsRegex = /\/\/ URL search param[\s\S]*?(?=\/\/ Pre-populate PRODUCTS)/;
  const newUrlParamsBlock = `// URL search param ?filter=, ?q= or ?cat=
    const urlParams = new URLSearchParams(window.location.search);
    const filterParam = urlParams.get('filter');
    const initialCat = urlParams.get('cat');
    const initialQuery = urlParams.get('q');

    const FILTER_CAT_MAP = {
      'all': 'All',
      'necklaces': 'Necklaces',
      'sets': 'Sets',
      'bracelets': 'Bracelets',
      'lariats': 'Lariats',
      'chains': 'Chains',
      'колье': 'Necklaces',
      'комплекты': 'Sets',
      'браслеты': 'Bracelets',
      'сотуары': 'Lariats',
      'цепи': 'Chains'
    };

    if(initialCat && CATS.includes(initialCat)){
      activeCat = initialCat;
      localStorage.setItem('livi_active_cat', initialCat);
    }
    if(filterParam){
      const fClean = filterParam.trim();
      const mappedCat = CATS.includes(fClean) ? fClean : FILTER_CAT_MAP[fClean.toLowerCase()];
      if(mappedCat){
        activeCat = mappedCat;
        localStorage.setItem('livi_active_cat', mappedCat);
      } else {
        activeCat = 'All';
        localStorage.setItem('livi_active_cat', 'All');
        searchQuery = fClean;
        if(searchInput) searchInput.value = fClean;
        if(searchClear) searchClear.style.display = 'block';
      }
    }
    if(initialQuery && searchInput){
      activeCat = 'All';
      localStorage.setItem('livi_active_cat', 'All');
      searchInput.value = initialQuery;
      searchQuery = initialQuery;
      if(searchClear) searchClear.style.display = 'block';
    }

    `;
  if (urlParamsRegex.test(html)) {
    html = html.replace(urlParamsRegex, newUrlParamsBlock);
  }

  // Update catch block for catalogError
  const catchRegex = /\.catch\(finalErr => \{[\s\S]*?\}\);/;
  const newCatch = `.catch(finalErr => {
        console.error('Error loading products:', finalErr);
        const hasCards = grid && grid.querySelectorAll('.card, .product-card').length > 0;
        if (!hasCards && grid && grid.children.length === 0) {
          const errEl = document.getElementById('catalogError');
          if (errEl) {
            errEl.innerHTML = '<p>Не удалось загрузить каталог. Пожалуйста, обновите страницу.</p><button onclick="location.reload()" class="btn btn-outline" style="margin-top:12px;">Обновить</button>';
            errEl.hidden = false;
            errEl.style.display = 'block';
          }
        }
      });`;
  if (catchRegex.test(html)) {
    html = html.replace(catchRegex, newCatch);
  }

  fs.writeFileSync(SHOP_PATH, html, 'utf8');
  console.log(`[OK] Pre-rendered ${activeProducts.length} products into shop.html with ?filter= support`);
}

main();
