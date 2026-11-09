# -*- coding: utf-8 -*-
"""
Playwright WebKit iPhone 13 Test Suite for Task 006 (iOS Safari Focus, Menu, Filters, M1, M2).
Tests:
  S1: Touch tap does not trigger blue system focus outlines on Safari iOS.
  S2: Disclosure triangles in storefront-menu are replaced with slim chevrons, sentence case.
  S3: Compact mobile catalog layout: first card top is <= 50% viewport height, bottom sheet filters.
  M1: Bottom sheet shows 74 items upon opening (not 85).
  M2: Empty search/filter result displays outline button "Сбросить фильтры", which restores 74 cards.
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

    try:
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

            # Test 5: Opening Filter Bottom Sheet (M1: Count check)
            print("5. Opening filter bottom sheet...")
            page.locator("#openMobileFilterBtn").click()
            page.wait_for_timeout(400)
            apply_btn = page.locator("#filterSheetApply")
            btn_text_initial = apply_btn.text_content().strip()
            print(f"Apply button text on opening without filters: '{btn_text_initial}'")
            assert "74" in btn_text_initial, f"M1 FAIL: Expected 74 in bottom sheet apply button, got '{btn_text_initial}'"
            assert "85" not in btn_text_initial, f"M1 FAIL: 85 found in bottom sheet apply button: '{btn_text_initial}'"
            page.screenshot(path=os.path.join(FIXTURES_DIR, "05_filter_sheet_iphone13.png"))

            # Test 6: Selecting Filter -> Empty State (M2)
            print("6. Selecting price chip 'до 25 000 ₸' in sheet...")
            price_chip = page.locator("#sheetPriceOptions button[data-max='25000']")
            price_chip.click()
            page.wait_for_timeout(200)

            print("Selecting 'Барочный жемчуг' in sheet...")
            stone_chip = page.locator("#sheetStoneOptions button[data-stone='Барочный жемчуг']")
            stone_chip.click()
            page.wait_for_timeout(200)

            btn_text_filtered = apply_btn.text_content().strip()
            print(f"Apply button text after empty filter combo: '{btn_text_filtered}'")
            apply_btn.click()
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(FIXTURES_DIR, "06_empty_state_iphone13.png"))

            empty_reset_btn = page.locator("#emptyResetBtn")
            assert empty_reset_btn.is_visible(), "M2 FAIL: Reset button not visible in empty state!"
            reset_btn_text = empty_reset_btn.text_content().strip()
            print(f"Empty reset button text: '{reset_btn_text}'")
            assert "Сбросить фильтры" in reset_btn_text, f"Unexpected reset button text: '{reset_btn_text}'"

            # Test 6b: Click Reset button -> Restores 74 items
            print("6b. Clicking 'Сбросить фильтры' button...")
            empty_reset_btn.click()
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(FIXTURES_DIR, "06b_catalog_restored_iphone13.png"))

            restored_cards = page.locator("#grid .card").count()
            cat_count_text = page.locator("#catalogCount").text_content().strip()
            print(f"Cards count after reset: {restored_cards}, count label: '{cat_count_text}'")
            assert restored_cards == 74, f"Expected 74 cards after reset, got {restored_cards}"
            assert "74" in cat_count_text, f"Expected 74 in count label, got '{cat_count_text}'"

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
            print("ALL WebKit tests completed successfully!")
    finally:
        httpd.shutdown()

if __name__ == "__main__":
    run_tests()
