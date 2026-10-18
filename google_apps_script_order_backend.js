/**
 * ==============================================================================
 * LIVI JEWELRY — ШЛЮЗ ПРИЁМА ЗАКАЗОВ, УЧЁТА В GOOGLE ТАБЛИЦЕ И УВЕДОМЛЕНИЙ В TELEGRAM
 * ==============================================================================
 *
 * ИНСТРУКЦИЯ ПО НАСТРОЙКЕ (занимает 3 минуты):
 * 1. Создайте новую Google Таблицу (например, "Livi Jewelry — Заказы").
 * 2. В меню таблицы выберите: Расширения (Extensions) -> Apps Script.
 * 3. Удалите весь существующий код и вставьте содержимое этого файла.
 * 4. Заполните TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID (ниже в НАСТРОЙКАХ).
 * 5. Нажмите кнопку "Развернуть" (Deploy) -> "Новое развертывание" (New deployment):
 *    - Выберите тип: "Веб-приложение" (Web app).
 *    - Описание: "Livi Orders API".
 *    - Выполнять от имени: "Меня" (Me).
 *    - У кого есть доступ: "Все" (Anyone).
 * 6. Нажмите "Развернуть", скопируйте полученный URL (заканчивается на /exec).
 * 7. Вставьте этот URL в cart.html в переменную ORDER_WEBHOOK_URL.
 * ==============================================================================
 */

// НАСТРОЙКИ:
const TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'; // Токен бота от @BotFather (например: 123456789:ABCdefGhIjkLmNoPqRsTuVwXyZ)
const TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID';     // ID чата супруги или группы (можно узнать у @userinfobot)
const SHEET_NAME = 'Заказы';

/**
 * Обработка входящего POST-запроса с сайта (cart.html)
 */
function doPost(e) {
  try {
    let order;
    if (e.postData && e.postData.contents) {
      order = JSON.parse(e.postData.contents);
    } else {
      return createJsonResponse({ error: 'No data received' }, 400);
    }

    // 1. Запись в Google Таблицу (Учёт покупок)
    recordOrderToSheet(order);

    // 2. Отправка уведомления супруге в Telegram
    sendTelegramNotification(order);

    return createJsonResponse({
      success: true,
      orderId: order.orderId,
      message: 'Заказ успешно зарегистрирован'
    });

  } catch (err) {
    return createJsonResponse({ error: err.toString() }, 500);
  }
}

/**
 * Запись заказа в Google Таблицу
 */
function recordOrderToSheet(order) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);

  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    // Заголовки таблицы
    const headers = [
      'Дата и время',
      'Номер заказа',
      'ФИО покупателя',
      'Телефон (Kaspi)',
      'Город',
      'Способ доставки',
      'Адрес СДЭК',
      'Товары',
      'Сумма (тг)',
      'Статус оплаты',
      'Трек-номер СДЭК',
      'Комментарий',
      'utm_source',
      'utm_medium',
      'utm_campaign',
      'utm_term',
      'gclid',
      'landing_page',
      'referrer'
    ];
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold').setBackground('#f3f3f3');
    sheet.setFrozenRows(1);
  }

  const itemsStr = (order.items || [])
    .map(it => {
      const customInfo = [it.customSize, it.customHardware, it.customGift].filter(Boolean).join(', ');
      return `${it.title} (${it.qty} шт. × ${it.price}${customInfo ? ' | ' + customInfo : ''})`;
    })
    .join('\n');

  const formattedDate = Utilities.formatDate(new Date(), 'Asia/Almaty', 'dd.MM.yyyy HH:mm');
  const attr = order.attribution || {};

  const row = [
    formattedDate,
    order.orderId || '',
    order.customerName || '',
    order.phone || '',
    order.city || '',
    order.deliveryTypeTitle || (order.deliveryType === 'pvz' ? 'ПВЗ СДЭК' : 'Курьер СДЭК'),
    order.address || '',
    itemsStr,
    order.totalAmount || 0,
    '⏳ Ожидает счёт Kaspi',
    '', // Трек-номер СДЭК (заполняется вручную при отправке)
    order.comment || '',
    attr.utm_source || '',
    attr.utm_medium || '',
    attr.utm_campaign || '',
    attr.utm_term || '',
    attr.gclid || '',
    attr.landing_page || '',
    attr.referrer || ''
  ];

  sheet.appendRow(row);
}

/**
 * Отправка сообщения в Telegram
 */
function sendTelegramNotification(order) {
  if (!TELEGRAM_BOT_TOKEN || TELEGRAM_BOT_TOKEN === 'YOUR_TELEGRAM_BOT_TOKEN') {
    return;
  }

  const itemsList = (order.items || [])
    .map(it => {
      const customInfo = [it.customSize, it.customHardware, it.customGift].filter(Boolean).join(', ');
      const customLine = customInfo ? `\n  _Параметры: ${escapeMarkdown(customInfo)}_` : '';
      return `• *${escapeMarkdown(it.title)}*\n  ${it.qty} шт. × ${it.unit ? it.unit.toLocaleString('ru-RU') : it.price} ₸${customLine}`;
    })
    .join('\n');

  const cleanPhone = (order.phone || '').replace(/[^\d]/g, '');
  const attr = order.attribution || {};

  let text = `🛍 *НОВЫЙ ЗАКАЗ НА САЙТЕ!* \`${escapeMarkdown(order.orderId)}\`\n`;
  text += `━━━━━━━━━━━━━━━━━━━━━\n`;
  text += `💎 *Состав заказа:*\n${itemsList}\n\n`;
  text += `💰 *ИТОГО К ОПЛАТЕ:* *${(order.totalAmount || 0).toLocaleString('ru-RU')} ₸*\n`;
  text += `━━━━━━━━━━━━━━━━━━━━━\n`;
  text += `👤 *Покупатель:* ${escapeMarkdown(order.customerName)}\n`;
  text += `📞 *Телефон Kaspi:* \`${escapeMarkdown(order.phone)}\`\n`;
  text += `_(нажмите на номер чтобы скопировать для Kaspi Pay)_\n\n`;
  text += `🚚 *Доставка СДЭК:*\n`;
  text += `• *Город:* ${escapeMarkdown(order.city)}\n`;
  text += `• *Тип:* ${escapeMarkdown(order.deliveryTypeTitle || order.deliveryType)}\n`;
  text += `• *Адрес:* ${escapeMarkdown(order.address)}\n`;
  if (order.comment) {
    text += `• *Комментарий:* _${escapeMarkdown(order.comment)}_\n`;
  }
  if (attr.utm_source || attr.gclid || attr.utm_term) {
    text += `📊 *Источник:* ${escapeMarkdown(attr.utm_source || (attr.gclid ? 'Google Ads' : 'Direct'))} | Запрос: ${escapeMarkdown(attr.utm_term || '—')} | GCLID: \`${escapeMarkdown((attr.gclid || '').substring(0, 12))}\`\n`;
  }
  text += `━━━━━━━━━━━━━━━━━━━━━\n`;
  text += `💳 *Действие:* Откройте Kaspi Pay ➔ Удаленная оплата ➔ Выставьте счет на *${(order.totalAmount || 0).toLocaleString('ru-RU')} ₸*`;

  const inlineKeyboard = {
    inline_keyboard: [
      [
        {
          text: '💬 Написать клиенту в WhatsApp',
          url: `https://wa.me/${cleanPhone}`
        }
      ]
    ]
  };

  const payload = {
    chat_id: TELEGRAM_CHAT_ID,
    text: text,
    parse_mode: 'Markdown',
    reply_markup: JSON.stringify(inlineKeyboard)
  };

  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
  UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });
}

function escapeMarkdown(text) {
  if (!text) return '';
  return String(text).replace(/[_*[\]()~`>#+=|{}.!-]/g, '\\$&');
}

function createJsonResponse(data, status = 200) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Тестовая функция для проверки работоспособности прямо в Apps Script
 */
function testRun() {
  const fakeOrder = {
    orderId: 'LV-TEST-001',
    customerName: 'Тестовый Покупатель',
    phone: '+7 (705) 123-45-67',
    city: 'Алматы',
    deliveryType: 'pvz',
    deliveryTypeTitle: 'ПВЗ СДЭК',
    address: 'ул. Достык, 12 (ПВЗ №1)',
    comment: 'Тестовый заказ для проверки бота и таблицы',
    totalAmount: 45000,
    items: [
      { title: 'Колье из жемчуга Майорка', qty: 1, price: '34 000 тг', unit: 34000 },
      { title: 'Браслет', qty: 1, price: '11 000 тг', unit: 11000 }
    ]
  };
  recordOrderToSheet(fakeOrder);
  sendTelegramNotification(fakeOrder);
}
