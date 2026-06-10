"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): TC-02 + TC-03 + TC-02b gộp bằng @pytest.mark.parametrize

This file contains 1 completed example (TC-01) and 1 data-driven test (TC-02, TC-03, TC-02b).

(*File này chứa 1 ví dụ mẫu (TC-01) đã hoàn chỉnh và 1 test data-driven gộp TC-02, TC-03, TC-02b.*)
"""
import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)

    ✅ COMPLETED — Use as a reference example.
    (*ĐÃ HOÀN THÀNH — Dùng làm ví dụ tham khảo.*)

    📖 RIPR Model (Textbook Ch.2 — Reachability → Infection → Propagation → Revealability):
        Mỗi dòng code trong test tương ứng với 1 bước trong chuỗi RIPR.
        Xem comment [R], [I], [P], [R✓] bên dưới.
    """
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập trong hệ thống
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI — nút "Đăng xuất" xuất hiện
    # (Smart Wait: thay vì time.sleep(5) — nhanh hơn và ổn định hơn)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Kiểm tra kết quả — Test Oracle phát hiện lỗi nếu có
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


# ---------------------------------------------------------------------------
# 💡 Bonus B2 — Data-Driven Testing (Ch.3 §3.3.2)
# ---------------------------------------------------------------------------
# TC-02, TC-03, TC-02b có cùng pattern (nhập → click → kiểm tra lỗi).
# Thay vì viết 3 hàm test riêng biệt (lặp code), ta gộp bằng
# @pytest.mark.parametrize — mỗi bộ dữ liệu tạo 1 test case riêng
# trong pytest output.
#
# 📖 Textbook (Ch.3 §3.3.2): Data-Driven Testing tách dữ liệu khỏi code test.
# Tương đương DataPoints trong JUnit.
#
# Trước (viết riêng):                         Sau (@parametrize):
#   3 hàm test, code gần giống nhau → DRY      1 hàm + 3 bộ dữ liệu
#   Thêm TC mới = viết thêm hàm                Thêm TC mới = thêm 1 dòng tuple
#   Khó bảo trì khi logic thay đổi             Sửa 1 chỗ = áp dụng tất cả
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "email, password, tc_id, description",
    [
        # TC-02: Sai mật khẩu — email đúng nhưng mật khẩu sai
        ("dam.tran@email.com", "wrongpassword", "TC-02", "Sai mật khẩu"),
        # TC-03: Bỏ trống cả hai trường
        ("", "", "TC-03", "Bỏ trống cả hai trường"),
        # TC-02b: Email không tồn tại trong hệ thống
        ("nobody@test.com", "anything", "TC-02b", "Email không tồn tại"),
    ],
)
def test_login_fail(page, test_config, email, password, tc_id, description):
    """TC-02/03/02b: Login fail — Data-Driven Testing
    (*Đăng nhập thất bại — Kiểm thử hướng dữ liệu*)

    💡 Bonus B2: Gộp nhiều kịch bản đăng nhập thất bại vào 1 hàm test duy nhất
    bằng @pytest.mark.parametrize. Mỗi bộ dữ liệu (email, password) tạo ra
    1 test case riêng biệt trong pytest output.

    📖 RIPR — Áp dụng cho tất cả các kịch bản trong bộ dữ liệu:
        [R] page.goto(...) → Chạm tới trang đăng nhập
        [I] flutter_fill(..., email/password) → Nhiễm trạng thái lỗi
        [P] Hệ thống xử lý login → Lỗi lan truyền ra thông báo
        [R✓] assert ... → Test Oracle kiểm tra thông báo lỗi

    Xem thêm: docs/textbook-concepts.md §3 (Data-Driven Testing)
    """
    # [R] Reachability: Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu test — mỗi bộ dữ liệu kích hoạt lỗi khác nhau
    if email:
        flutter_fill(page, "Email", email)
    if password:
        flutter_fill(page, "Mật khẩu", password)

    # Act: Click "Đăng nhập"
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ hệ thống xử lý → lỗi lan truyền ra UI
    wait_for_flutter(page)

    # Screenshot — mỗi TC có file screenshot riêng theo tc_id
    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, f"{tc_id.lower()}_login_fail.png")
    )

    # [R✓] Revealability: Kiểm tra kết quả — vẫn ở trang đăng nhập
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng nhập" in sem_text, \
        f"[{tc_id}] {description}: System unexpectedly navigated away from login page"
