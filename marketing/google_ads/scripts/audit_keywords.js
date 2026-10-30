const fs = require('fs');

const content = fs.readFileSync('ads_archive/1_google_ads_keywords.csv', 'utf8');
const lines = content.trim().split('\n').slice(1);
console.log('Total keyword rows in 1_google_ads_keywords.csv:', lines.length);

const adGroups = {};
for (const l of lines) {
  const parts = l.split(',');
  if (parts.length >= 4) {
    const campaign = parts[0].trim();
    const ag = parts[1].trim();
    const kw = parts[2].trim();
    const type = parts[3].trim();
    const url = parts[4] ? parts[4].trim() : '';
    if (!adGroups[ag]) adGroups[ag] = { campaign, keywords: [] };
    adGroups[ag].keywords.push({ kw, type, url });
  }
}

console.log('Ad groups found:', Object.keys(adGroups).length);
for (const [ag, data] of Object.entries(adGroups)) {
  console.log(`\nGroup: [${ag}] (${data.keywords.length} items):`);
  const uniqueKws = [...new Set(data.keywords.map(k => k.kw))];
  console.log('  Unique phrases:', uniqueKws.length);
  console.log('  Sample phrases:', uniqueKws.slice(0, 6).join(' | '));
  const urls = [...new Set(data.keywords.map(k => k.url))];
  console.log('  Landing URLs:', urls.join(', '));
}
