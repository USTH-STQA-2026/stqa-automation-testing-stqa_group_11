"""
Logout & Language Tests (*Kiểm thử Đăng xuất & Chuyển ngôn ngữ*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 2 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 2 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - Logout button: 'flt-semantics[role="button"]:has-text("Đăng xuất")'
      (*Nút Đăng xuất*)
    - Language switch EN button: 'flt-semantics[role="button"]:has-text("EN")'
      (*Nút chuyển ngôn ngữ EN*)
    - After logout: page returns to login (has "Đăng nhập" button and "Email" input)
      (*Sau đăng xuất: trang quay về login*)
    - After switching to EN: text "Logout", "Borrow", "Search", "Library" may appear
      (*Sau chuyển EN: text tiếng Anh có thể xuất hiện*)
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter, SCREENSHOT_DIR,
)


def _login_as(page, base_url, email, password):
    page.goto(base_url, wait_until="domcontentloaded", timeout=60000)
    page.locator("flt-glass-pane").wait_for(state="attached", timeout=45000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)


def test_logout(page, test_config):
    """TC-11: Logout success (*Đăng xuất thành công*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → click Logout → verify page returns to login screen.
        (*Đăng nhập → click Đăng xuất → kiểm tra quay về trang đăng nhập.*)

    Suggested steps (*Gợi ý*):
        1. login(page, test_config)
        2. Find "Đăng xuất" button and click (*Tìm nút "Đăng xuất" và click*)
        3. Wait 3s, re-enable semantics (*Đợi 3s, bật lại semantics*)
        4. Assert: "Đăng nhập" button or Email input exists
           (*Assert: có nút "Đăng nhập" hoặc ô input Email*)
    """
    # biet.hoang — active, no borrowed books
    _login_as(page, test_config["base_url"], "biet.hoang@email.com", "password123")
    flutter_click_button(page, "Đăng xuất")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc11_logout.png"))
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_login_btn = "Đăng nhập" in sem_text
    has_email_input = page.locator('input[aria-label="Email"]').count() > 0
    assert has_login_btn or has_email_input, \
        "Logout failed: expected to return to login page with 'Đăng nhập' or Email input"


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → click "EN" button → verify UI switches to English.
        (*Đăng nhập → click nút "EN" → kiểm tra giao diện chuyển sang tiếng Anh.*)

    Suggested steps (*Gợi ý*):
        1. login(page, test_config)
        2. Find "EN" button and click (*Tìm nút "EN" và click*)
        3. Wait 2s, re-enable semantics (*Đợi 2s, bật lại semantics*)
        4. Get sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
        5. Assert: "Logout" or "Borrow" or "Library" in sem_text
    """
    # dam.tran — active, no borrowed books
    _login_as(page, test_config["base_url"], "dam.tran@email.com", "password123")
    flutter_click_button(page, "EN")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc12_language_en.png"))
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    english_words = ["Logout", "Borrow", "Library", "Search", "Return", "Book"]
    has_english = any(word in sem_text for word in english_words)
    assert has_english, \
        f"Language switch to EN failed: none of {english_words} found in UI"
