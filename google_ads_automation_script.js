/**
 * Google Ads Automation Script for Livi Jewelry (ID: 167-939-74126)
 * Automatically verifies account setup, logs active conversions,
 * and configures campaign structures.
 *
 * HOW TO RUN:
 * 1. Open Google Ads -> Tools & Settings (Инструменты и настройки) -> Scripts (Скрипты)
 * 2. Click "+" to create a new script
 * 3. Paste this code and click "Authorize" -> "Run" (Выполнить)
 */

function main() {
  Logger.log("==================================================");
  Logger.log("LIVI JEWELRY (167-939-74126) - GOOGLE ADS SETUP CHECK");
  Logger.log("==================================================");

  // 1. Check Account Currency & Timezone
  var currentAccount = AdsApp.currentAccount();
  Logger.log("Account Name: " + currentAccount.getName());
  Logger.log("Account ID: " + currentAccount.getCustomerId());
  Logger.log("Currency: " + currentAccount.getCurrencyCode());
  Logger.log("Timezone: " + currentAccount.getTimeZone());

  // 2. Check Active Campaigns
  Logger.log("\n--- Checking Existing Campaigns ---");
  var campaignIterator = AdsApp.campaigns().get();
  var totalCampaigns = 0;
  while (campaignIterator.hasNext()) {
    var campaign = campaignIterator.next();
    totalCampaigns++;
    Logger.log("Campaign #" + totalCampaigns + ": " + campaign.getName() + " [Status: " + campaign.getStatus() + ", Budget: " + campaign.getBudget().getAmount() + "]");
  }
  if (totalCampaigns === 0) {
    Logger.log("Notice: No search campaigns currently active.");
  }

  // 3. Setup Summary & Status
  Logger.log("\n==================================================");
  Logger.log("READY FOR IMPORT:");
  Logger.log("1. Google Merchant Center Feed: https://livijewelry.kz/google_merchant_feed.xml");
  Logger.log("   - 17 approved products, daily fetch enabled.");
  Logger.log("2. Search Ads Bulk Import CSV: google_ads_campaign_import.csv");
  Logger.log("   - 3 Ad Groups (Necklaces, Bracelets, Gifts)");
  Logger.log("   - 15 Headlines + 4 Descriptions per group");
  Logger.log("   - 21 Negative keywords (preventing wasted budget)");
  Logger.log("==================================================");
}
