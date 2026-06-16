"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 4 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 4 test case trong file này.*)

Hints (*Gợi ý*):
    - After logging in, use flutter_fill() to type into the search box
      (*Sau khi đăng nhập, dùng flutter_fill() để nhập vào ô tìm kiếm*)
    - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Each book card has role="group" and aria-label containing book info
      (*Mỗi card sách có role="group" và aria-label chứa thông tin sách*)
    - Use login() helper from conftest.py to log in before testing
      (*Dùng login() helper từ conftest.py để đăng nhập trước khi test*)
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


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
        (*Đăng nhập → tìm kiếm từ khóa "Flutter" → kiểm tra có sách Flutter trong kết quả.*)

    Hints (*Gợi ý*):
        - login(page, test_config)
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
        - Verify: page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0
    """
    # biet.hoang — active, no borrowed books
    _login_as(page, test_config["base_url"], "biet.hoang@email.com", "password123")
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
    wait_for_flutter(page, text="Flutter")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc04_search_by_name.png"))
    assert page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0, \
        "No Flutter books found in search results"


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
        (*Đăng nhập → tìm kiếm từ khóa không tồn tại → kiểm tra không có sách nào hiển thị.*)

    Hints (*Gợi ý*):
        - Verify: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count() == 0
    """
    # dam.tran — active, no borrowed books
    _login_as(page, test_config["base_url"], "dam.tran@email.com", "password123")
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "xyz_khong_ton_tai_12345")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc05_search_no_result.png"))
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    assert book_cards.count() == 0, \
        f"Expected no books but found {book_cards.count()}"


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → enter "Công nghệ" in the category filter → verify all displayed books
        belong to the "Công nghệ" category.
        (*Đăng nhập → nhập "Công nghệ" vào ô lọc thể loại → kiểm tra tất cả sách
        hiển thị đều thuộc thể loại Công nghệ.*)

    Hints (*Gợi ý*):
        - flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")
        - Get book list: page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
          (*Lấy danh sách sách*)
        - Loop through each book, verify aria-label contains "Công nghệ"
          (*Lặp qua từng sách, kiểm tra aria-label chứa "Công nghệ"*)
    """
    # biet.hoang — active, no borrowed books
    _login_as(page, test_config["base_url"], "biet.hoang@email.com", "password123")
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")
    wait_for_flutter(page, text="Công nghệ")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc06_filter_category.png"))
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    count = book_cards.count()
    assert count > 0, "No books found after filtering by 'Công nghệ'"
    for i in range(count):
        label = book_cards.nth(i).get_attribute("aria-label") or ""
        assert "Công nghệ" in label, \
            f"Book {i} does not belong to 'Công nghệ' category: {label}"


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    ✅ COMPLETED (*ĐÃ HOÀN THÀNH*)

    Description (*Mô tả*):
        Log in → search author name (e.g. "Nguyễn Minh Đức") → verify results found.
        (*Đăng nhập → tìm kiếm tên tác giả → kiểm tra có kết quả.*)

    Hints (*Gợi ý*):
        - flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")
        - Verify: page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count() > 0
    """
    # dam.tran — active, no borrowed books
    _login_as(page, test_config["base_url"], "dam.tran@email.com", "password123")
    author = "Nguyễn Minh Đức"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", author)
    wait_for_flutter(page, text=author)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc07_search_by_author.png"))
    assert page.locator(f'flt-semantics[aria-label*="{author}"]').count() > 0, \
        f"No books found for author '{author}'"
