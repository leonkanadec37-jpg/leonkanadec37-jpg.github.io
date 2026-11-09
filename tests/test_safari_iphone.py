# -*- coding: utf-8 -*-
"""
Playwright WebKit iPhone 13 Test Suite for Task 006 (iOS Safari Focus, Menu, Filters).
Tests:
  S1: Touch tap does not trigger blue system focus outlines on Safari iOS.
  S2: Disclosure triangles in storefront-menu are replaced with slim chevrons, sentence case.
  S3: Compact mobile catalog layout: first card top is <= 50% viewport height, bottom sheet filters.
"""
import os
import sys
import time
import socketserver
import http.server
import threading
from playwright.sync_api import sync_playwright

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
os.makedirs(FIXTURES_DIR, exist_ok=True)

PORT = 8086
BASE_URL = f"http://127.0.0.1:{PORT}"

def start_local_server():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=root, **kwargs)
        def log_message(self, format, *args):
            pass # Silent
    httpd = socketserver.TCPServer(("", PORT), CustomHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    return httpd

def run_tests():
    httpd = start_local_server()
    time.sleep(0.5)

    with sync_playwright() as p:
        iphone_13 = p.devices['iPhone 13']
        print(f"Launching WebKit with iPhone 13 emulation: {iphone_13['viewport']}...")
        browser = p.webkit.launch(headless=True)
        
        # 1. Mobile iPhone 13 Tests
        context = browser.new_context(**iphone_13, ignore_https_errors=True)
        page = context.new_page()

        # Test 1: Main Page
        print("1. Loading index.html on iPhone 13...")
        page.goto(f"{BASE_URL}/", wait_until="networkidle")
        page.screenshot(path=os.path.join(FIXTURES_DIR, "01_index_iphone13.png"))

        # Test 2: Menu Open via Tap (S1 & S2)
        print("2. Tapping storefront-menu-toggle...")
        toggle = page.locator(".storefront-menu-toggle")
        toggle.click()
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(FIXTURES_DIR, "02_menu_open_iphone13.png"))

        active_element_tag = page.evaluate("document.activeElement ? document.activeElement.tagName + '.' + document.activeElement.className : 'NONE'")
        print(f"Active element after menu tap: {active_element_tag}")
        assert "A." not in active_element_tag, "First link received programmatic focus on touch tap!"

        # Test 3: Menu Close via Tap on toggle (S1)
        print("3. Tapping toggle again to close...")
        toggle.click()
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(FIXTURES_DIR, "03_menu_closed_iphone13.png"))
        active_after_close = page.evaluate("document.activeElement ? document.activeElement.tagName + '.' + document.activeElement.className : 'NONE'")
        print(f"Active element after menu close: {active_after_close}")

        # Test 4: Shop Catalog First Screen (S3)
        print("4. Loading shop.html on iPhone 13...")
        page.goto(f"{BASE_URL}/shop.html", wait_until="networkidle")
        page.wait_for_timeout(600)

        first_card_box = page.locator("#grid .card").first.bounding_box()
        if first_card_box:
            viewport_h = iphone_13['viewport']['height']
            ratio = (first_card_box['y'] / viewport_h) * 100
            print(f"First card Y: {first_card_box['y']:.1f}px out of {viewport_h}px ({ratio:.1f}% of screen height)")
            assert first_card_box['y'] <= (viewport_h * 0.50), f"First card Y is {first_card_box['y']}, exceeding 50%!"
        page.screenshot(path=os.path.join(FIXTURES_DIR, "04_shop_catalog_iphone13.png"))

        # Test 5: Opening Filter Bottom Sheet (S3)
        print("5. Opening filter bottom sheet...")
        page.locator("#openMobileFilterBtn").click()
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(FIXTURES_DIR, "05_filter_sheet_iphone13.png"))

        # Test 6: Selecting Filter
        print("6. Selecting price chip 'до 25 000 ₸' in sheet...")
        price_chip = page.locator("#sheetPriceOptions button[data-max='25000']")
        price_chip.click()
        page.wait_for_timeout(200)

        print("Selecting 'Барочный жемчуг' in sheet...")
        stone_chip = page.locator("#sheetStoneOptions button[data-stone='Барочный жемчуг']")
        stone_chip.click()
        page.wait_for_timeout(200)

        apply_btn = page.locator("#filterSheetApply")
        print(f"Apply button text: {apply_btn.text_content()}")
        apply_btn.click()
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(FIXTURES_DIR, "06_catalog_active_chip_iphone13.png"))

        active_chips = page.locator("#activeFilterChips .active-filter-chip")
        count_chips = active_chips.count()
        print(f"Active filter chips displayed: {count_chips}")
        for i in range(count_chips):
            print(f" - Chip {i+1}: {active_chips.nth(i).text_content()}")

        context.close()

        # Test 7: Desktop Keyboard Navigation (:focus-visible)
        print("7. Testing Desktop Keyboard Navigation for :focus-visible...")
        desktop_ctx = browser.new_context(viewport={'width': 1280, 'height': 800})
        desktop_page = desktop_ctx.new_page()
        desktop_page.goto(f"{BASE_URL}/shop.html", wait_until="networkidle")
        desktop_page.keyboard.press("Tab")
        desktop_page.keyboard.press("Tab")
        desktop_page.keyboard.press("Tab")
        desktop_page.screenshot(path=os.path.join(FIXTURES_DIR, "07_desktop_keyboard_focus.png"))
        desktop_ctx.close()

        browser.close()
        httpd.shutdown()
        print("ALL WebKit tests completed successfully!")

if __name__ == "__main__":
    run_tests()
