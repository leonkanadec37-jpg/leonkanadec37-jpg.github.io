#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile Menu Safari WebKit Visual and Functional Verification Test
Runs HTTP server, tests mobile menu in Playwright WebKit (Safari engine on iPhone 13 and iPhone SE 375px),
takes screenshots, and verifies no horizontal overflow or regressions.
"""

import http.server
import os
import socketserver
import threading
import time
from playwright.sync_api import sync_playwright

PORT = 8099
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIXTURES_DIR = os.path.join(ROOT_DIR, "tests", "fixtures")
os.makedirs(FIXTURES_DIR, exist_ok=True)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
            httpd.serve_forever()
    except Exception:
        pass

def main():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    with sync_playwright() as p:
        browser = p.webkit.launch()

        # 1. RU Home - 375px (iPhone SE)
        device_375 = p.devices['iPhone SE']
        context_375 = browser.new_context(**device_375)
        page = context_375.new_page()

        print("[TEST] Testing RU index.html on Safari (375px)...")
        page.goto(f"http://127.0.0.1:{PORT}/", wait_until="networkidle")
        
        # Click burger to open menu
        burger = page.locator("#burger")
        burger.click()
        page.wait_for_timeout(400)

        # Check menu is visible
        menu = page.locator("#storefrontMobileMenu")
        assert menu.is_visible(), "Menu should be visible after clicking burger"

        # Verify body scroll lock
        body_classes = page.evaluate("() => document.body.className")
        print(f"  Body classes after open: {body_classes}")
        assert "drawer-open" in body_classes, "Body should have 'drawer-open' scroll lock class"

        # Check that no element exceeds 375px horizontally
        scroll_width = page.evaluate("() => document.documentElement.scrollWidth")
        print(f"  Document scrollWidth: {scroll_width}")
        assert scroll_width <= 375, f"Horizontal overflow detected! scrollWidth = {scroll_width}"

        # Capture RU 375px screenshot
        ru_shot = os.path.join(FIXTURES_DIR, "menu_ru_375px.png")
        page.screenshot(path=ru_shot)
        print(f"  [SAVED] {ru_shot}")

        # Scroll stones row horizontally
        stone_scroll = page.locator(".smm-pills-scroll").nth(1)
        stone_scroll.evaluate("el => el.scrollLeft = 320")
        page.wait_for_timeout(300)

        stones_scrolled_shot = os.path.join(FIXTURES_DIR, "menu_ru_stones_scrolled_375px.png")
        page.screenshot(path=stones_scrolled_shot)
        print(f"  [SAVED] {stones_scrolled_shot}")

        # Test close button
        close_btn = page.locator(".smm-close-btn")
        close_btn.click()
        page.wait_for_timeout(300)
        assert not menu.is_visible(), "Menu should be closed after clicking close button"
        body_classes_after = page.evaluate("() => document.body.className")
        print(f"  Body classes after close: {body_classes_after}")
        assert "drawer-open" not in body_classes_after, "Body scroll lock should be removed"

        # 2. RU Home - 390px (iPhone 13)
        print("[TEST] Testing RU index.html on Safari (iPhone 13 - 390px)...")
        device_390 = p.devices['iPhone 13']
        context_390 = browser.new_context(**device_390)
        page_390 = context_390.new_page()
        page_390.goto(f"http://127.0.0.1:{PORT}/", wait_until="networkidle")
        page_390.locator("#burger").click()
        page_390.wait_for_timeout(400)
        ru_390_shot = os.path.join(FIXTURES_DIR, "menu_ru_390px.png")
        page_390.screenshot(path=ru_390_shot)
        print(f"  [SAVED] {ru_390_shot}")

        # 3. KZ Home - 375px
        print("[TEST] Testing KZ kz/index.html on Safari (375px)...")
        page_kz = context_375.new_page()
        page_kz.goto(f"http://127.0.0.1:{PORT}/kz/", wait_until="networkidle")
        page_kz.locator("#burger").click()
        page_kz.wait_for_timeout(400)
        kz_shot = os.path.join(FIXTURES_DIR, "menu_kz_375px.png")
        page_kz.screenshot(path=kz_shot)
        print(f"  [SAVED] {kz_shot}")

        # Verify no russian strings in KZ menu
        kz_menu_text = page_kz.locator("#storefrontMobileMenu").inner_text()
        russian_markers = ["УКРАШЕНИЯ", "ВЕСЬ КАТАЛОГ", "ЕЩЁ КАТЕГОРИИ", "ПО КАМНЮ", "Доставка и оплата", "Магазин в Астане"]
        for marker in russian_markers:
            assert marker not in kz_menu_text, f"Russian string '{marker}' found in KZ menu!"
        print("  [PASS] KZ menu verified free of untranslated Russian strings!")

        # 4. UZ Home - 375px
        print("[TEST] Testing UZ uz/index.html on Safari (375px)...")
        page_uz = context_375.new_page()
        page_uz.goto(f"http://127.0.0.1:{PORT}/uz/", wait_until="networkidle")
        page_uz.locator("#burger").click()
        page_uz.wait_for_timeout(400)
        uz_shot = os.path.join(FIXTURES_DIR, "menu_uz_375px.png")
        page_uz.screenshot(path=uz_shot)
        print(f"  [SAVED] {uz_shot}")

        # Verify no russian strings in UZ menu
        uz_menu_text = page_uz.locator("#storefrontMobileMenu").inner_text()
        for marker in russian_markers:
            assert marker not in uz_menu_text, f"Russian string '{marker}' found in UZ menu!"
        print("  [PASS] UZ menu verified free of untranslated Russian strings!")

        # 5. Full viewport & links test (Shop, Product, Cart)
        for path_name in ["/shop.html", "/product/prod_01.html", "/cart.html"]:
            print(f"[TEST] Testing menu on {path_name}...")
            p_test = context_375.new_page()
            p_test.goto(f"http://127.0.0.1:{PORT}{path_name}", wait_until="networkidle")
            b_el = p_test.locator("#burger")
            assert b_el.count() > 0, f"Burger button not found on {path_name}"
            b_el.click()
            p_test.wait_for_timeout(300)
            m_el = p_test.locator("#storefrontMobileMenu")
            assert m_el.is_visible(), f"Mobile menu not visible on {path_name}"

        browser.close()
        print("\n========================================================")
        print("ALL SAFARI / WEBKIT MOBILE MENU TESTS PASSED (100% OK)!")
        print("========================================================")

if __name__ == "__main__":
    main()
