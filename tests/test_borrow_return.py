"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 3 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 3 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - "Mượn / Trả" tab: role="tab", aria-label="Mượn / Trả"
    - Available books have "Có sẵn" in aria-label, borrowed books have "Đang mượn"
      (*Sách "Có sẵn" có aria-label chứa "Có sẵn", sách "Đang mượn" chứa "Đang mượn"*)
    - Borrow button: 'flt-semantics[role="button"]:has-text("Mượn sách này")'
      (*Nút mượn*)
    - After clicking "Mượn sách này", a confirmation dialog appears — click "Mượn" again
      (*Sau khi click "Mượn sách này" sẽ hiện dialog xác nhận — cần click nút "Mượn" lần nữa*)
    - Return button: 'flt-semantics[role="button"]:has-text("Trả sách")'
      (*Nút trả*)
"""
import os
import re
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, wait_for_flutter, SCREENSHOT_DIR,
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


def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → find an "Available" book → click "Mượn sách này" → confirm dialog
        → verify book status changes to "Borrowed".
        (*Đăng nhập → tìm sách "Có sẵn" → click "Mượn sách này" → xác nhận dialog
        → kiểm tra sách chuyển sang trạng thái "Đang mượn".*)

    Suggested steps (*Gợi ý các bước*):
        1. login(page, test_config)
        2. Find available book: page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]')
           (*Tìm sách Có sẵn*)
        3. Click "Mượn sách này" button inside that book card
           (*Click nút "Mượn sách này" trong sách đó*)
        4. Wait for confirmation dialog, re-enable semantics
           (*Đợi dialog xác nhận, bật lại semantics*)
        5. Click "Mượn" button (confirm button in dialog)
           (*Click nút "Mượn" — nút xác nhận trong dialog*)
        6. Assert: "Đang mượn" or "thành công" appears
           (*Assert: "Đang mượn" hoặc "thành công" xuất hiện*)
    """
    # Login with dam.tran who has no borrowed books (ideal for borrow test)
    _login_as(page, test_config["base_url"], "dam.tran@email.com", "password123")

    # Click "Mượn sách này" on the first available book
    borrow_btn = page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.first.wait_for(state="attached", timeout=10000)
    borrow_btn.first.click()

    # Wait for confirmation dialog to appear
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)

    # Click exact "Mượn" confirm button in dialog (not "Mượn sách này")
    confirm_btn = page.locator('flt-semantics[role="button"]').filter(
        has_text=re.compile(r'^Mượn$')
    )
    confirm_btn.click()

    # Wait for borrow to complete
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc08_borrow_book.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đang mượn" in sem_text or "thành công" in sem_text, \
        "Borrow operation did not succeed: expected 'Đang mượn' or 'thành công'"


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → switch to "Mượn / Trả" tab → verify borrowed books are shown.
        (*Đăng nhập → chuyển sang tab "Mượn / Trả" → kiểm tra có sách đang mượn.*)

    Hints (*Gợi ý*):
        - Click tab: page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
        - Verify: books with "Đang mượn" in aria-label, or "Trả sách" button exists
          (*Kiểm tra: có sách với aria-label chứa "Đang mượn" hoặc có nút "Trả sách"*)
    """
    # Login with ba.nguyen who already has BOOK003 borrowed
    _login_as(page, test_config["base_url"], "ba.nguyen@email.com", "password123")

    # Switch to "Mượn / Trả" tab
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc09_view_borrowed.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_borrowed_label = "Đang mượn" in sem_text
    has_return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').count() > 0
    assert has_borrowed_label or has_return_btn, \
        "No borrowed books found in 'Mượn / Trả' tab"


def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → go to "Mượn / Trả" tab → click "Trả sách" → verify book is returned.
        (*Đăng nhập → tab "Mượn / Trả" → click "Trả sách" → kiểm tra sách được trả.*)

    Hints (*Gợi ý*):
        - Switch to "Mượn / Trả" tab (*Chuyển tab "Mượn / Trả"*)
        - Find return button: page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
          (*Tìm nút "Trả sách"*)
        - Click and verify status change or success message
          (*Click và kiểm tra sách chuyển trạng thái hoặc có thông báo thành công*)
    """
    # Login with ba.nguyen who already has BOOK003 borrowed
    _login_as(page, test_config["base_url"], "ba.nguyen@email.com", "password123")

    # Switch to "Mượn / Trả" tab
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)

    # Click "Trả sách" to return the borrowed book
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
    return_btn.first.wait_for(state="attached", timeout=10000)
    return_btn.first.click()

    # Wait for the return to complete
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc10_return_book.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    no_return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').count() == 0
    assert "Có sẵn" in sem_text or "thành công" in sem_text or no_return_btn, \
        "Return operation did not succeed: expected book status change or success message"
