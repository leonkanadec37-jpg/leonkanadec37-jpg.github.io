const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * Скрипт синхронизации карточек товаров Livi Jewelry (Node.js обертка).
 * Без технических кодов (prod_XX) в <title> и заголовках!
 * Шаблон <title>: {title} — купить по цене {price_formatted} ₸ в Астане и Алматы | Ручная работа Livi Jewelry
 */

const rootDir = path.join(__dirname, '..');
const productsPath = path.join(rootDir, 'products.json');
const products = JSON.parse(fs.readFileSync(productsPath, 'utf8'));

function formatPriceRu(price) {
  return Number(price || 0).toLocaleString('ru-RU').replace(/\u00A0/g, ' ');
}

function buildCommercialTitle(p) {
  const priceFormatted = formatPriceRu(p.price);
  return `${p.title} — купить по цене ${priceFormatted} ₸ в Астане и Алматы | Ручная работа Livi Jewelry`;
}

// Запускаем основной Python-конвейер генерации карточек, хабов, KZ-витрины, фидов и sitemap
try {
  execSync('python generate_product_pages.py', { cwd: rootDir, stdio: 'inherit' });
  if (fs.existsSync(path.join(rootDir, 'generate_seo_hubs.py'))) {
    execSync('python generate_seo_hubs.py', { cwd: rootDir, stdio: 'inherit' });
  }
  if (fs.existsSync(path.join(rootDir, 'generate_kz_pages.py'))) {
    execSync('python generate_kz_pages.py', { cwd: rootDir, stdio: 'inherit' });
  }
  if (fs.existsSync(path.join(rootDir, 'generate_feed.py'))) {
    execSync('python generate_feed.py', { cwd: rootDir, stdio: 'inherit' });
  }
  if (fs.existsSync(path.join(rootDir, 'generate_sitemap.py'))) {
    execSync('python generate_sitemap.py', { cwd: rootDir, stdio: 'inherit' });
  }
  console.log(`Updated ${products.length} products with clean commercial titles (e.g. "${buildCommercialTitle(products[0])}")`);
} catch (err) {
  console.error('Error running product generators:', err.message);
  process.exit(1);
}
