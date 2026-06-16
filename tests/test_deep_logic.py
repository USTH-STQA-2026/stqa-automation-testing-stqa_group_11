"""
Deep System-Logic Tests (*Kiểm thử logic nghiệp vụ chuyên sâu*)
Library Book Borrowing System — https://stqa.rbc.vn

Mục tiêu: Tập trung vào các lỗi LÀM SAI LOGIC NGHIỆP VỤ cốt lõi của hệ thống,
thử nghiệm trên TẤT CẢ các tài khoản test. Bỏ qua các lỗi phụ (vd: form thêm
thành viên, lỗi hiển thị nhỏ) và các tính năng còn THIẾU/CHƯA phát triển
(không tính là bug).

(*Focus on bugs that break core business logic, exercised across ALL test
accounts. Minor bugs and not-yet-developed features are intentionally excluded.*)

──────────────────────────────────────────────────────────────────────────────
KẾT QUẢ THỰC NGHIỆM (đã chạy trực tiếp trên hệ thống live) — 4 nhóm lỗi logic:

  BUG-A  REQ-04  Giới hạn mượn LỖI OFF-BY-ONE: một thành viên giữ được 4 sách
                 thay vì tối đa 3. (dam.tran 0→4, ba.nguyen 1→4, biet.hoang 1→4)
  BUG-B  REQ-08  Rò rỉ phiếu mượn giữa các thành viên: qua "Tra cứu phiếu mượn",
                 một thành viên xem được phiếu mượn của thành viên KHÁC.
  BUG-C  REQ-04  Sai LÝ DO từ chối: thành viên "Tạm ngưng" (cu.le) bị báo
                 "Thành viên đã hết hạn" — đúng phải là lý do "tạm ngưng".
  BUG-D  REQ-02  Danh mục sách ẩn sách "Đã mượn"/"Thất lạc": chỉ hiển thị sách
                 "Có sẵn", trái với REQ-02 (phải hiển thị mọi sách kèm trạng thái).

Các test có tiền tố `test_bug_*` kỳ vọng hành vi ĐÚNG theo SRS nên sẽ FAIL —
mỗi FAIL là một bằng chứng lỗi hệ thống. Các test `test_ok_*` là test ĐỐI CHỨNG
(control) khẳng định những phần hệ thống chạy ĐÚNG, để chứng minh bộ oracle
không "fail bừa".
──────────────────────────────────────────────────────────────────────────────
"""
import os
import re
from contextlib import contextmanager

import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter, SCREENSHOT_DIR,
)

PASSWORD = "password123"

# Trạng thái mượn ban đầu (seed) của từng thành viên — số phiếu "Đang mượn".
#   MEM002 ba.nguyen : BR001 (BOOK003, quá hạn)            -> 1
#   MEM003 dam.tran  : không có phiếu đang mượn            -> 0
#   MEM006 biet.hoang: BR003 (BOOK013)                     -> 1
SEED_ACTIVE = {
    "ba.nguyen@email.com": 1,
    "dam.tran@email.com": 0,
    "biet.hoang@email.com": 1,
}
BORROW_LIMIT = 3  # SRS REQ-04


# ─────────────────────────── helpers ───────────────────────────

@contextmanager
def _fresh_page(browser):
    """Mở context+page MỚI cho mỗi tài khoản trong cùng một test.

    Lý do: input của Flutter bị lỗi khi fill LẦN THỨ HAI vào cùng một field trong
    một session (node semantics bị tạo lại). Mỗi tài khoản dùng một context riêng
    để vừa gom nhiều tài khoản vào MỘT test (một bug = một lỗi), vừa giữ seed sạch.
    """
    context = browser.new_context()
    page = context.new_page()
    try:
        yield page
    finally:
        context.close()


def _login_as(page, email, password=PASSWORD):
    """Đăng nhập tươi cho mỗi test (mỗi `page` là context riêng → seed sạch)."""
    page.goto("https://stqa.rbc.vn", wait_until="domcontentloaded", timeout=60000)
    page.locator("flt-glass-pane").wait_for(state="attached", timeout=45000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")
    page.wait_for_timeout(3500)
    enable_flutter_semantics(page)
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    return "Đăng xuất" in sem


def _go_tab(page, aria):
    tab = page.locator(f'flt-semantics[role="tab"][aria-label="{aria}"]')
    if tab.count() > 0:
        tab.first.click()
        page.wait_for_timeout(1500)
        enable_flutter_semantics(page)
        return True
    return False


def _sem_text(page):
    return " ".join(page.locator("flt-semantics").all_text_contents())


def _try_borrow_once(page):
    """Thử mượn cuốn 'Có sẵn' đầu tiên (click + xác nhận dialog).

    Trả về một trong: 'SUCCESS' | 'REJECT_LIMIT' | 'REJECT_STATE' |
    'NO_BUTTON' | 'UNKNOWN'. Dựa trên snackbar tức thời (snackbar tự ẩn).
    """
    _go_tab(page, "Sách")
    btn = page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    if btn.count() == 0:
        return "NO_BUTTON"
    btn.first.click()
    page.wait_for_timeout(1200)
    enable_flutter_semantics(page)
    confirm = page.locator('flt-semantics[role="button"]').filter(has_text=re.compile(r'^Mượn$'))
    if confirm.count() > 0:
        confirm.first.click()
        page.wait_for_timeout(1800)
        enable_flutter_semantics(page)
    low = _sem_text(page).lower()
    if "thành công" in low:
        return "SUCCESS"
    if any(k in low for k in ["tối đa", "giới hạn", "3 sách"]):
        return "REJECT_LIMIT"
    if any(k in low for k in ["tạm ngưng", "hết hạn", "không thể"]):
        return "REJECT_STATE"
    return "UNKNOWN"


def _shot(page, name):
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, name))


# ════════════════════════════════════════════════════════════════════════════
# BUG-A — REQ-04: Giới hạn mượn off-by-one (giữ được 4 sách thay vì 3)
# Data-driven trên 3 tài khoản active để chứng minh lỗi ở MỌI thành viên.
# ════════════════════════════════════════════════════════════════════════════

def test_bug_a_borrow_limit_off_by_one(browser):
    """BUG-A: Hệ thống cho phép một thành viên giữ 4 sách (vượt giới hạn 3).

    SRS REQ-04: "Tối đa 3 sách / thành viên cùng lúc."
    Kiểm trên TẤT CẢ tài khoản active (dam.tran 0→4, ba.nguyen 1→4, biet.hoang 1→4):
    cuốn thứ 4 vẫn mượn được, chỉ tới cuốn thứ 5 mới bị chặn. Lý do: điều kiện chặn
    dùng `>= 4` thay vì `>= 3`. Cùng một lỗi off-by-one nên gom MỘT test → MỘT lỗi.

    Test này KỲ VỌNG hành vi đúng (≤ 3) nên sẽ FAIL → đó chính là bằng chứng lỗi.
    """
    details = []
    violations = []
    for email, start in SEED_ACTIVE.items():
        allowed_more = BORROW_LIMIT - start  # số cuốn được phép mượn thêm
        with _fresh_page(browser) as page:
            assert _login_as(page, email), f"Không đăng nhập được {email}"
            successes = 0
            outcomes = []
            # Thử mượn nhiều hơn mức cho phép 2 lần để chắc chắn chạm ngưỡng chặn.
            for _ in range(allowed_more + 2):
                r = _try_borrow_once(page)
                outcomes.append(r)
                if r == "SUCCESS":
                    successes += 1
                elif r in ("REJECT_LIMIT", "REJECT_STATE", "NO_BUTTON"):
                    break
            _shot(page, f"bug_a_limit_{email.split('@')[0]}.png")

        total_held = start + successes
        details.append(
            f"{email} (giữ sẵn {start}): mượn thêm {successes} → tổng {total_held}; {outcomes}"
        )
        if successes > allowed_more:
            violations.append(f"{email} giữ {total_held}/{BORROW_LIMIT}")

    assert not violations, (
        f"[BUG-A] REQ-04 vi phạm off-by-one — các tài khoản giữ được > {BORROW_LIMIT} sách: "
        f"{violations}. Chi tiết: {details}. Hệ thống chỉ chặn ở cuốn thứ 4 (dùng >=4 thay vì >=3)."
    )


# ════════════════════════════════════════════════════════════════════════════
# BUG-B — REQ-08: Thành viên xem được phiếu mượn của thành viên KHÁC
# (chức năng "Tra cứu phiếu mượn" không lọc theo người đang đăng nhập)
# ════════════════════════════════════════════════════════════════════════════

# dam.tran (MEM003) tra cứu phiếu của ba.nguyen (MEM002) và biet.hoang (MEM006)
B_VIEWER = "dam.tran@email.com"
B_TARGETS = [
    ("MEM002", "Nguyễn Học Bá", "BR001"),
    ("MEM006", "Hoàng Cá Biệt", "BR003"),
]


def test_bug_b_member_record_isolation(browser):
    """BUG-B: Một thành viên tra cứu được phiếu mượn của thành viên khác.

    SRS REQ-08: "Thành viên chỉ xem phiếu mượn của CHÍNH MÌNH. KHÔNG được xem
    phiếu mượn của thành viên khác."
    Bằng chứng live: dam.tran mở "Tra cứu phiếu mượn", nhập MEM002/MEM006 → thấy
    đầy đủ phiếu của người khác (tên, sách, ngày mượn, hạn trả). Cùng một lỗ hổng
    phân quyền nên gom MỘT test → MỘT lỗi.

    Test kỳ vọng KHÔNG rò rỉ → sẽ FAIL.
    """
    leaks = []
    for target_id, victim_name, victim_record in B_TARGETS:
        with _fresh_page(browser) as page:
            assert _login_as(page, B_VIEWER), f"Không đăng nhập được {B_VIEWER}"
            assert _go_tab(page, "Mượn / Trả"), "Không vào được tab Mượn / Trả"

            sub = page.locator('flt-semantics[role="tab"][aria-label="Tra cứu phiếu mượn"]')
            assert sub.count() > 0, "Không thấy mục 'Tra cứu phiếu mượn'"
            sub.first.click()
            page.wait_for_timeout(1200)
            enable_flutter_semantics(page)

            flutter_fill(page, "Nhập mã thành viên (VD: MEM001)", target_id)
            page.wait_for_timeout(800)
            lookup_btn = page.locator('flt-semantics[role="button"]:has-text("Tra cứu")')
            if lookup_btn.count() > 0:
                lookup_btn.first.click()
                page.wait_for_timeout(1800)
                enable_flutter_semantics(page)
            _shot(page, f"bug_b_isolation_{B_VIEWER.split('@')[0]}_{target_id}.png")

            # Gom phiếu của NGƯỜI KHÁC đang hiển thị
            leaked = []
            for g in page.locator('flt-semantics[role="group"][aria-label*="Mã phiếu"]').all():
                lbl = g.get_attribute("aria-label") or ""
                if victim_name in lbl or victim_record in lbl:
                    leaked.append(lbl.replace("\n", " | "))
            sem = _sem_text(page)
            if leaked or victim_name in sem or victim_record in sem:
                leaks.append(
                    f"{target_id}/{victim_name}: {leaked or victim_record}"
                )

    assert not leaks, (
        f"[BUG-B] REQ-08 vi phạm: {B_VIEWER} tra cứu và XEM ĐƯỢC phiếu mượn của "
        f"thành viên KHÁC. Rò rỉ: {leaks}."
    )


# ════════════════════════════════════════════════════════════════════════════
# BUG-C — REQ-04: Sai LÝ DO từ chối cho thành viên "Tạm ngưng"
# ════════════════════════════════════════════════════════════════════════════

def test_bug_c_suspended_member_wrong_reason(page):
    """BUG-C: Thành viên 'Tạm ngưng' bị từ chối với lý do SAI ('đã hết hạn').

    SRS REQ-04: "Thông báo lỗi phải mô tả ĐÚNG lý do từ chối (tạm ngưng ≠ hết hạn)."
    Bằng chứng live: cu.le (MEM004, Tạm ngưng) khi mượn nhận đúng câu
    "Thành viên đã hết hạn. Không thể mượn sách." — y hệt thông báo của thành viên
    Hết hạn (binh.pham). Hệ thống chỉ có MỘT nhánh từ chối 'hết hạn' nên gán sai
    cho người 'tạm ngưng'.

    Test kỳ vọng lý do nhắc 'tạm ngưng' → sẽ FAIL.
    """
    assert _login_as(page, "cu.le@email.com"), "Không đăng nhập được cu.le (Tạm ngưng)"
    result = _try_borrow_once(page)
    _shot(page, "bug_c_suspended_reason.png")

    low = _sem_text(page).lower()
    mentions_suspended = "tạm ngưng" in low
    mentions_expired = "hết hạn" in low

    assert result in ("REJECT_STATE", "REJECT_LIMIT", "NO_BUTTON"), \
        f"cu.le (Tạm ngưng) đáng lẽ bị từ chối mượn, nhưng kết quả = {result}"
    assert mentions_suspended and not (mentions_expired and not mentions_suspended), (
        "[BUG-C] REQ-04 vi phạm: thành viên 'Tạm ngưng' (cu.le) bị từ chối với LÝ DO SAI. "
        "Hệ thống báo 'Thành viên đã hết hạn.' thay vì lý do 'tạm ngưng'. "
        f"(mentions_suspended={mentions_suspended}, mentions_expired={mentions_expired})"
    )


# ════════════════════════════════════════════════════════════════════════════
# BUG-D — REQ-02: Danh mục ẩn sách "Đã mượn" và "Thất lạc"
# ════════════════════════════════════════════════════════════════════════════

D_BOOKS = [
    ("Kiểm thử phần mềm nhập môn", "BOOK003", "Đã mượn"),   # bị MEM002 mượn (seed)
    ("Kinh tế vi mô", "BOOK007", "Thất lạc"),               # thất lạc (seed)
]


def test_bug_d_catalog_hides_non_available_books(browser):
    """BUG-D: Danh mục sách chỉ hiển thị sách 'Có sẵn', ẩn 'Đã mượn'/'Thất lạc'.

    SRS REQ-02: "Hiển thị TẤT CẢ sách... mỗi sách có trạng thái (Có sẵn / Đã mượn)"
    và "trạng thái cập nhật real-time". Tức sách 'Đã mượn'/'Thất lạc' vẫn phải hiện
    (kèm trạng thái), không được biến mất.
    Bằng chứng live: tìm "Kiểm thử phần mềm" (BOOK003 Đã mượn) → 0 kết quả;
    tìm "Kinh tế vi mô" (BOOK007 Thất lạc) → 0 kết quả. Cùng một lỗi lọc danh mục
    nên gom MỘT test → MỘT lỗi.

    Test kỳ vọng sách vẫn hiển thị → sẽ FAIL.
    """
    hidden = []
    for title, code, status in D_BOOKS:
        with _fresh_page(browser) as page:
            assert _login_as(page, "dam.tran@email.com"), "Không đăng nhập được dam.tran"
            flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", title)
            page.wait_for_timeout(2000)
            enable_flutter_semantics(page)
            _shot(page, f"bug_d_hidden_{code}.png")

            cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
            labels = " ".join(
                cards.nth(i).get_attribute("aria-label") or "" for i in range(cards.count())
            )
            if not (code in labels or title in labels):
                hidden.append(f"'{title}' ({code}, trạng thái '{status}')")

    assert not hidden, (
        f"[BUG-D] REQ-02 vi phạm: các sách sau KHÔNG xuất hiện trong danh mục khi tìm kiếm "
        f"— hệ thống ẩn hoàn toàn sách không 'Có sẵn': {hidden}. "
        f"REQ-02 yêu cầu hiển thị mọi sách kèm trạng thái."
    )


# ════════════════════════════════════════════════════════════════════════════
# CONTROL (đối chứng) — các phần hệ thống chạy ĐÚNG → các test này PASS.
# Mục đích: chứng minh bộ test không "fail bừa"; oracle đã được hiệu chuẩn.
# ════════════════════════════════════════════════════════════════════════════

def test_ok_expired_member_correct_reason(page):
    """CONTROL: Thành viên 'Hết hạn' (binh.pham) bị từ chối với lý do ĐÚNG.

    Đối chứng cho BUG-C: với người HẾT HẠN, thông báo 'đã hết hạn' là CHÍNH XÁC
    → test PASS. Sự tương phản chứng minh hệ thống dùng chung 1 nhánh 'hết hạn'.
    """
    assert _login_as(page, "binh.pham@email.com"), "Không đăng nhập được binh.pham"
    result = _try_borrow_once(page)
    _shot(page, "ok_expired_reason.png")
    low = _sem_text(page).lower()
    assert result in ("REJECT_STATE", "NO_BUTTON"), \
        f"binh.pham (Hết hạn) đáng lẽ bị từ chối, kết quả = {result}"
    assert "hết hạn" in low, \
        "Đối chứng thất bại: không thấy lý do 'hết hạn' cho thành viên Hết hạn"


def test_ok_borrow_due_date_is_14_days(page):
    """CONTROL: Hạn trả = ngày mượn + 14 ngày (REQ-04). Logic ngày ĐÚNG → PASS."""
    assert _login_as(page, "dam.tran@email.com"), "Không đăng nhập được dam.tran"
    assert _try_borrow_once(page) == "SUCCESS", "Mượn cuốn đầu tiên thất bại"
    assert _go_tab(page, "Mượn / Trả"), "Không vào được tab Mượn / Trả"
    sub = page.locator('flt-semantics[role="tab"][aria-label="Phiếu mượn của tôi"]')
    if sub.count() > 0:
        sub.first.click(); page.wait_for_timeout(1200); enable_flutter_semantics(page)
    _shot(page, "ok_due_date_14d.png")

    label = ""
    for g in page.locator('flt-semantics[role="group"][aria-label*="Mã phiếu"]').all():
        lbl = g.get_attribute("aria-label") or ""
        if "Đang mượn" in lbl:
            label = lbl
            break
    m_borrow = re.search(r"Ngày mượn:\s*(\d{2})/(\d{2})/(\d{4})", label)
    m_due = re.search(r"Hạn trả:\s*(\d{2})/(\d{2})/(\d{4})", label)
    assert m_borrow and m_due, f"Không đọc được ngày từ phiếu: {label!r}"

    from datetime import date
    d_borrow = date(int(m_borrow.group(3)), int(m_borrow.group(2)), int(m_borrow.group(1)))
    d_due = date(int(m_due.group(3)), int(m_due.group(2)), int(m_due.group(1)))
    assert (d_due - d_borrow).days == 14, \
        f"Thời hạn mượn phải là 14 ngày, thực tế = {(d_due - d_borrow).days} ngày"


def test_ok_realtime_book_leaves_catalog_after_borrow(page):
    """CONTROL: Sau khi mượn, sách rời danh mục 'Có sẵn' ngay (REQ-02 real-time).

    Mượn 'Mạng máy tính' (BOOK008) → tìm lại không còn nút mượn cho nó → PASS.
    Cũng khẳng định KHÔNG mượn trùng được 1 bản sách (single copy).
    """
    assert _login_as(page, "dam.tran@email.com"), "Không đăng nhập được dam.tran"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Mạng máy tính")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    before = page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').count()
    assert before >= 1, "Không thấy nút mượn cho BOOK008 trước khi mượn"

    page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').first.click()
    page.wait_for_timeout(1200)
    enable_flutter_semantics(page)
    confirm = page.locator('flt-semantics[role="button"]').filter(has_text=re.compile(r'^Mượn$'))
    if confirm.count() > 0:
        confirm.first.click(); page.wait_for_timeout(2000); enable_flutter_semantics(page)
    _shot(page, "ok_realtime_after_borrow.png")

    after = page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').count()
    assert after < before, (
        f"Sau khi mượn, BOOK008 vẫn còn nút mượn (before={before}, after={after}) "
        "— REQ-02 cập nhật real-time / single-copy không đúng"
    )


def test_ok_member_has_no_admin_capabilities(page):
    """CONTROL: Thành viên thường KHÔNG có tab/nút quản trị (phân quyền ĐÚNG → PASS).

    Đối chứng cho BUG-B: việc ẩn các chức năng quản trị (tab 'Thành viên',
    'Thêm thành viên', 'Đặt lại dữ liệu') hoạt động đúng — chỉ riêng dữ liệu
    'Tra cứu phiếu mượn' bị rò rỉ (BUG-B).
    """
    assert _login_as(page, "dam.tran@email.com"), "Không đăng nhập được dam.tran"
    _shot(page, "ok_member_no_admin.png")
    tab_labels = [t.get_attribute("aria-label") for t in page.locator('flt-semantics[role="tab"]').all()]
    btn_texts = " ".join((b.text_content() or "") for b in page.locator('flt-semantics[role="button"]').all())

    assert "Thành viên" not in tab_labels, \
        f"Thành viên thường KHÔNG được thấy tab quản trị 'Thành viên': {tab_labels}"
    assert "Thêm thành viên" not in btn_texts and "Đặt lại dữ liệu" not in btn_texts, \
        "Thành viên thường KHÔNG được thấy nút quản trị (Thêm thành viên / Đặt lại dữ liệu)"


def test_ok_returning_book_frees_a_slot(page):
    """CONTROL: Trả sách giải phóng đúng 1 suất mượn (bộ đếm giảm khi trả → PASS).

    Khẳng định LOGIC TRẢ là đúng: lỗi giới hạn (BUG-A) nằm ở NGƯỠNG (4 thay vì 3),
    không phải ở việc bộ đếm không giảm khi trả.
    """
    assert _login_as(page, "dam.tran@email.com"), "Không đăng nhập được dam.tran"
    # Mượn tới khi bị chặn
    for _ in range(6):
        if _try_borrow_once(page) in ("REJECT_LIMIT", "REJECT_STATE", "NO_BUTTON"):
            break
    # Trả 1 cuốn
    assert _go_tab(page, "Mượn / Trả"), "Không vào được tab Mượn / Trả"
    rb = page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
    assert rb.count() > 0, "Không có nút 'Trả sách' để trả"
    rb.first.click(); page.wait_for_timeout(2000); enable_flutter_semantics(page)
    # Mượn lại 1 cuốn — phải được phép vì vừa giải phóng 1 suất
    again = _try_borrow_once(page)
    _shot(page, "ok_return_frees_slot.png")
    assert again == "SUCCESS", (
        f"Sau khi trả 1 cuốn, mượn lại bị '{again}' — bộ đếm giới hạn không giảm khi trả"
    )
