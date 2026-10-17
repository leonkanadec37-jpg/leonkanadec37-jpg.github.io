# Livi Jewelry (`https://livijewelry.kz/`) — Comprehensive AdTech, GMC, GA4 & GSC Audit and Fix Report

**Date:** October 17, 2026  
**Target Domain:** `https://livijewelry.kz/`  
**Backup Snapshot Branch:** `backup/pre-audit-snapshot` (pushed to `origin`)  
**Audit & Fix Branch:** `fix/adtech-architecture-audit` (merged & deployed to `main`)  
**Automated Verification Status:** **15 / 15 Checks Passed (0 Errors)** via [`verify_audit.py`](file:///d:/Livi_jewelry%20%28Antigravity%29/verify_audit.py)

---

## 1. Executive Summary & Google Identifier Map

| System / Platform | Identifier / File | Status After Fix |
| :--- | :--- | :--- |
| **Google Analytics 4 (GA4)** | `G-YFF2TR0N36` | Unified across all 40 HTML pages with cross-domain linker & Consent Mode v2 |
| **Google Ads Conversion ID** | `AW-16793974126` | Unified across all 40 HTML pages with `allow_enhanced_conversions: true` |
| **Google Ads Conversion Label** | `AW-16793974126/MuJ_CObHup8bEO7q_sc-` | Triggered on both Primary Conversion #1 (`purchase`) & Primary Conversion #2 (`generate_lead` / `contact`) |
| **Google Search Console (GSC)** | `qvEv0YmsvczSUOBETXFI8aaUjGutqAYqzEWuZ2f0Zz0` | Present on `index.html`, `shop.html`, all `/product/prod_01..28.html`, category & policy pages |
| **Google Merchant Center Feed** | [`google_merchant_feed.xml`](file:///d:/Livi_jewelry%20%28Antigravity%29/google_merchant_feed.xml) & [`feed.xml`](file:///d:/Livi_jewelry%20%28Antigravity%29/feed.xml) | 28/28 products synchronized 100% with `products.json`, `shop.html`, and `/product/prod_XX.html` |
| **XML Sitemap** | [`sitemap.xml`](file:///d:/Livi_jewelry%20%28Antigravity%29/sitemap.xml) | 36 canonical URLs (`/` + `shop.html` + 3 categories + 3 policies + 28 product pages) |
| **Crawler Directives** | [`robots.txt`](file:///d:/Livi_jewelry%20%28Antigravity%29/robots.txt) | Explicitly allows `*`, `Googlebot`, `Googlebot-Image`, `Storebot-Google`, `AdsBot-Google` |

---

## 2. Root-Cause Findings & Architectural Fixes by Phase

### Phase 1 & Phase 4: Crawler Accessibility & Internal Linking (Why Googlebot Failed to Index `/product/prod_*.html`)
* **Root Cause 1 — Empty Static DOM Containers in `shop.html` and `index.html`:**
  * Previously, `<div class="grid" id="grid"></div>` in [`shop.html`](file:///d:/Livi_jewelry%20%28Antigravity%29/shop.html) and `<div id="featGrid" class="grid" aria-live="polite"></div>` in [`index.html`](file:///d:/Livi_jewelry%20%28Antigravity%29/index.html) were empty in raw HTML and populated only after asynchronous client-side `fetch('products.json')` execution. First-wave Googlebot HTML crawlers saw **zero** `<a href="/product/prod_XX.html">` links on `index.html` and `shop.html`.
  * **Fix:** Updated [`generate_product_pages.py`](file:///d:/Livi_jewelry%20%28Antigravity%29/generate_product_pages.py) (`sync_static_catalogs()`) to pre-render all 28 `<article class="card">` elements with crawlable `<a href="/product/prod_XX.html" class="card-title-link">` links directly into the static HTML of `shop.html` and `index.html`.
* **Root Cause 2 — Stale Price/Title Drift on Category Landing Pages:**
  * [`kolye-iz-zhemchuga.html`](file:///d:/Livi_jewelry%20%28Antigravity%29/kolye-iz-zhemchuga.html), [`braslety-iz-zhemchuga.html`](file:///d:/Livi_jewelry%20%28Antigravity%29/braslety-iz-zhemchuga.html), and [`sergi-iz-zhemchuga.html`](file:///d:/Livi_jewelry%20%28Antigravity%29/sergi-iz-zhemchuga.html) had hardcoded legacy prices (`40 000 ₸` instead of `74 000 ₸` for `prod_07`, `34 000 ₸` instead of `44 000 ₸` for `prod_09`, `45 000 ₸` instead of `61 000 ₸` for `prod_11`, `36 000 ₸` instead of `52 000 ₸` for `prod_12`, `35 000 ₸` instead of `45 000 ₸` for `prod_13`, `40 000 ₸` instead of `60 000 ₸` for `prod_14`, and `40 000 ₸` instead of `56 000 ₸` for `prod_15`), causing structured data and price mismatch warnings when crawled alongside `/product/prod_XX.html`.
  * **Fix:** Synchronized all category landing pages (both HTML product cards and JSON-LD `ItemList`) directly from [`products.json`](file:///d:/Livi_jewelry%20%28Antigravity%29/products.json) via [`generate_product_pages.py`](file:///d:/Livi_jewelry%20%28Antigravity%29/generate_product_pages.py).
* **Root Cause 3 — Incomplete `sitemap.xml` & `robots.txt`:**
  * [`sitemap.xml`](file:///d:/Livi_jewelry%20%28Antigravity%29/sitemap.xml) was missing `privacy.html` and `terms.html`. [`robots.txt`](file:///d:/Livi_jewelry%20%28Antigravity%29/robots.txt) lacked explicit `Googlebot`, `Googlebot-Image`, `Storebot-Google`, and `AdsBot-Google` rules for `/product/` and `/assets/`.
  * **Fix:** Updated [`generate_sitemap.py`](file:///d:/Livi_jewelry%20%28Antigravity%29/generate_sitemap.py) and [`robots.txt`](file:///d:/Livi_jewelry%20%28Antigravity%29/robots.txt), generating all 36 canonical URLs with `2026-10-17` `<lastmod>`.

---

### Phase 2: Google Ads & GA4 Tracking Unification (`purchase` & `contact`)
* **Bug 1 — Missing Google Consent Mode v2 & Cross-Page Linker:**
  * None of the pages initialized `gtag('consent', 'default', { ad_storage, analytics_storage, ad_user_data, ad_personalization })` or `url_passthrough: true`, and `privacy.html` / `returns.html` had no `gtag.js` snippet at all, risking session/attribution loss when users navigated from a Google Shopping ad (`/product/prod_08.html?gclid=...`) to policy pages or cart checkout.
  * **Fix:** Installed unified `gtag.js` (`G-YFF2TR0N36` + `AW-16793974126`) with Google Consent Mode v2, `url_passthrough: true`, and domain linker across all 40 HTML files.
* **Bug 2 — Non-Standard Transaction IDs & Missing Direct-Order `purchase` Events on `shop.html` Modal:**
  * `cart.html` used `ORD-` and `product/prod_XX.html` used `WA-1CLICK-` instead of standardized `LIVI-<timestamp>`, and clicking "Заказать в 1 клик в WhatsApp" inside the `shop.html` product modal only fired `generate_lead` without firing `purchase`.
  * **Fix:** Standardized all purchase conversion events across [`cart.html`](file:///d:/Livi_jewelry%20%28Antigravity%29/cart.html), [`shop.html`](file:///d:/Livi_jewelry%20%28Antigravity%29/shop.html), and all 28 `/product/prod_XX.html` pages (via [`generate_product_pages.py`](file:///d:/Livi_jewelry%20%28Antigravity%29/generate_product_pages.py)) to fire:
    * `view_item` (on product page load and `shop.html` modal open)
    * `add_to_cart` (on clicking "Добавить в корзину")
    * `begin_checkout` (on opening `cart.html` with items or initiating 1-click order)
    * `purchase` with `{ transaction_id: "LIVI-<timestamp>", currency: "KZT", value: <numeric_total>, items: [...] }` + Google Ads `conversion` (`AW-16793974126/MuJ_CObHup8bEO7q_sc-`).
* **Bug 3 — Incomplete Contact (`generate_lead` / `contact`) Parameters & Aborted Beacons:**
  * Previously, Instagram links were not tracked, `contact` event was not fired alongside `generate_lead`, `page_location` and `item_id` were omitted, and same-tab links navigated away immediately before the `gtag` beacon flushed.
  * **Fix:** Added a unified global click listener across all pages that tracks every WhatsApp and Instagram link with both `generate_lead` and `contact` passing `{ currency: "KZT", value: <product_or_cart_or_default_value>, method: "WhatsApp" | "Instagram", page_location: window.location.href, item_id: "<prod_XX>" }`, with a 150ms safety callback whenever a link does not open in `target="_blank"`.

---

### Phase 3: Google Merchant Center (GMC) & `/product/prod_*.html` Synchronization
* **Bug 1 — Title Mismatch Between XML Feed and Product Landing Pages:**
  * [`generate_feed.py`](file:///d:/Livi_jewelry%20%28Antigravity%29/generate_feed.py) previously appended materials to `<g:title>` (e.g., `Колье «Лапы» — Натуральный жемчуг, Ювелирный сплав | Livi Jewelry`) while `<h1>` and JSON-LD `name` on `/product/prod_08.html` only had the base title, causing GMC title mismatch warnings.
  * **Fix:** Updated [`generate_feed.py`](file:///d:/Livi_jewelry%20%28Antigravity%29/generate_feed.py) so `<g:title>` matches `products.json` `title`, `<title>`, `<h1>`, and JSON-LD `name` 100%.
* **Bug 2 — Truncated / Generic Titles & Stub Descriptions in `products.json`:**
  * Fixed truncated/generic titles (`prod_01`, `prod_02`, `prod_04`, `prod_05`, `prod_08`, `prod_16`, `prod_22`, `prod_23`, `prod_25`, `prod_27`, `prod_28`), enriched stub descriptions (`prod_03`, `prod_06`, `prod_16`, `prod_18`, `prod_19`, `prod_20`, `prod_21`), and populated missing materials (`prod_10`–`prod_15`, `prod_17`) while strictly preserving all `AGENTS.md` set price breakdowns.
* **Bug 3 — Price Format & Category Code in XML Feed and JSON-LD:**
  * Standardized `<g:price>` in [`google_merchant_feed.xml`](file:///d:/Livi_jewelry%20%28Antigravity%29/google_merchant_feed.xml) and [`feed.xml`](file:///d:/Livi_jewelry%20%28Antigravity%29/feed.xml) to `{price:.2f} KZT` (e.g. `40000.00 KZT`), JSON-LD `offers.price` to `{price:.2f}` (`"40000.00"`) with `priceCurrency: "KZT"`, `<g:google_product_category>188</g:google_product_category>`, and `<g:identifier_exists>no</g:identifier_exists>`.
* **Bug 4 — Return Policy Contradiction (JSON-LD vs `delivery.html`):**
  * JSON-LD previously declared `https://schema.org/FreeReturn` while `delivery.html` stated buyer pays return shipping for non-defective items (`ReturnShippingFees`). Standardized JSON-LD `returnFees` to `https://schema.org/ReturnShippingFees` across all pages.
* **Bug 5 — Missing Terms of Service (`terms.html`):**
  * Created [`terms.html`](file:///d:/Livi_jewelry%20%28Antigravity%29/terms.html) (Условия использования и публичная оферта) and linked `delivery.html`, `privacy.html`, and `terms.html` in the footer of every page.

---

### Phase 5: Codebase & Garbage Cleanup + Core Web Vitals
* **Removed 47 Unreferenced Files in `assets/` and 4 Temporary Root Files:**
  * Deleted 45 orphaned legacy `.webp` files, `assets/manifest.json`, `assets/sprite.svg`, `lighthouse_report.html`, `lighthouse_report_v2.html`, `downloaded_report.csv`, and `optimize_images.py`.
* **Fixed CLS & LCP Attributes:**
  * Added explicit `width` and `height` attributes to the hero image on [`index.html`](file:///d:/Livi_jewelry%20%28Antigravity%29/index.html), the modal image on [`shop.html`](file:///d:/Livi_jewelry%20%28Antigravity%29/shop.html), all category cards, and all related product cards in [`generate_product_pages.py`](file:///d:/Livi_jewelry%20%28Antigravity%29/generate_product_pages.py).

---

## 3. Automated Verification Suite Results (`verify_audit.py`)

```text
============================================================================
LIVI JEWELRY — ADTECH, GMC, GA4 & GSC AUTOMATED VERIFICATION SUITE
============================================================================

[1/6] Validating Single Source of Truth (products.json)...
  [PASS] Loaded 28 products from products.json
  [PASS] All 28 products have unique IDs, distinct descriptive titles, valid prices, non-empty WebP images, and rich descriptions

[2/6] Validating Google Merchant Center XML Feeds...
  [PASS] google_merchant_feed.xml: valid XML with 28 items
  [PASS] feed.xml: valid XML with 28 items
  [PASS] 100% GMC XML Feed parity verified (<g:id>, <g:title>, <g:link>, <g:price>, <g:identifier_exists>no, category 188, and image existence)

[3/6] Validating 28 /product/prod_XX.html Landing Pages...
  [PASS] All 28 /product/prod_XX.html pages pass 100% HTML, JSON-LD, Canonical, CLS image dimension, and Funnel Tracking checks

[4/6] Validating shop.html, index.html, and Category Pages Parity & Crawlability...
  [PASS] shop.html #grid contains static crawlable <a href="/product/prod_XX.html"> links to all 28 products
  [PASS] shop.html JSON-LD ItemList matches all 28 products (SKU, title, price.00 KZT)
  [PASS] index.html #featGrid contains 28 static crawlable product links
  [PASS] kolye-iz-zhemchuga.html: all product cards & JSON-LD match products.json 100%
  [PASS] braslety-iz-zhemchuga.html: all product cards & JSON-LD match products.json 100%
  [PASS] sergi-iz-zhemchuga.html: all product cards & JSON-LD match products.json 100%

[5/6] Validating sitemap.xml and robots.txt...
  [PASS] robots.txt explicitly allows *, Googlebot, Googlebot-Image across /, /product/, /assets/ and declares Sitemap
  [PASS] sitemap.xml contains all 36 canonical URLs (homepage, catalog, categories, policies, and all 28 products)

[6/6] Validating Unified GA4/Ads Tracking, Consent Mode v2 & Policy Compliance Across All Pages...
  [PASS] All 40 HTML pages contain unified GA4 (G-YFF2TR0N36), Google Ads (AW-16793974126), Consent Mode v2, and non-aborting contact conversion handlers

============================================================================
ALL 15 VERIFICATION CHECKS PASSED WITH ZERO ERRORS!
============================================================================
```
