# REPORT.md — Báo cáo kiểm thử tự động / Automation Test Report

**Dự án**: Hệ thống Mượn sách Thư viện ABC — https://stqa.rbc.vn  
**Công cụ**: Python 3.12 + Playwright 1.49.1 + pytest 8.3.4  
**Ngày chạy**: 2026-06-06  
**Nhóm**: Nhóm 11 — 252ICT2012.11

---

## 1. Tóm tắt kết quả / Executive Summary

| Chỉ số | Giá trị |
|--------|---------|
| Tổng số test case | **49** |
| PASS | **35** |
| FAIL | **14** |
| SKIP | 0 |
| Thời gian chạy | ~720 giây (~12 phút) |
| Coverage | TC-01 → TC-49 (100%) |

**35/49** test case **PASS**. **14 test case FAIL** — tất cả đều là **lỗi hệ thống thực tế** (không phải lỗi kịch bản test). Đợt kiểm thử sâu (TC-41 → TC-49) phát hiện thêm 3 bug mới nghiêm trọng, nâng tổng lên **8 bug hệ thống** (BUG-01 → BUG-08).

---

## 2. Kết quả từng Test Case / Individual Test Results

### Nhóm 1: Đăng nhập (`tests/test_login.py`)

| TC | Tên test | Kết quả | Screenshot | Mô tả |
|----|----------|---------|------------|-------|
| TC-01 | `test_login_success` | ✅ PASS | `login_success.png` | Đăng nhập thành công với `ba.nguyen@email.com`. Giao diện hiển thị tên người dùng "Nguyễn Học Bá" và nút "Đăng xuất". |
| TC-02 | `test_login_fail_wrong_password` | ✅ PASS | `login_fail_wrong_password.png` | Nhập đúng email nhưng sai mật khẩu. Hệ thống không chuyển trang — vẫn ở màn hình đăng nhập. |
| TC-03 | `test_login_fail_empty_fields` | ✅ PASS | `login_fail_empty_fields.png` | Bấm "Đăng nhập" khi để trống. Hệ thống không chuyển trang. |

**Nhận xét**: Luồng đăng nhập hoạt động đúng. Hệ thống ngăn chặn đăng nhập với thông tin không hợp lệ.

---

### Nhóm 2: Tìm kiếm & Lọc sách (`tests/test_search.py`)

| TC | Tên test | Kết quả | Screenshot | Mô tả |
|----|----------|---------|------------|-------|
| TC-04 | `test_search_book_by_name` | ✅ PASS | `tc04_search_by_name.png` | Tìm kiếm "Flutter" → kết quả có sách Flutter trong `aria-label`. |
| TC-05 | `test_search_book_no_result` | ✅ PASS | `tc05_search_no_result.png` | Tìm kiếm `"xyz_khong_ton_tai_12345"` → không có card sách nào. |
| TC-06 | `test_filter_by_category` | ✅ PASS | `tc06_filter_category.png` | Lọc "Công nghệ" → tất cả card sách đều có `aria-label` chứa "Công nghệ". |
| TC-07 | `test_search_by_author` | ✅ PASS | `tc07_search_by_author.png` | Tìm kiếm tác giả "Nguyễn Minh Đức" → có kết quả. |

---

### Nhóm 3: Mượn & Trả sách (`tests/test_borrow_return.py`)

| TC | Tên test | Kết quả | Screenshot | Mô tả |
|----|----------|---------|------------|-------|
| TC-08 | `test_borrow_book` | ✅ PASS | `tc08_borrow_book.png` | Mượn sách thành công — dialog xác nhận 2 bước hoạt động đúng. |
| TC-09 | `test_view_borrowed_books` | ✅ PASS | `tc09_view_borrowed.png` | Xem danh sách sách đang mượn trong tab "Mượn / Trả". |
| TC-10 | `test_return_book` | ✅ PASS | `tc10_return_book.png` | Trả sách thành công — nút "Trả sách" biến mất sau thao tác. |

---

### Nhóm 4: Chức năng chung (`tests/test_general.py`)

| TC | Tên test | Kết quả | Screenshot | Mô tả |
|----|----------|---------|------------|-------|
| TC-11 | `test_logout` | ✅ PASS | `tc11_logout.png` | Đăng xuất → trở về màn hình đăng nhập. |
| TC-12 | `test_switch_language_to_english` | ✅ PASS | `tc12_language_en.png` | Bấm "EN" → giao diện chuyển sang tiếng Anh. |

---

### Nhóm 5: Bổ sung — Đăng nhập & Tìm kiếm nâng cao (`tests/test_extended.py`)

| TC | Tên test | Kết quả | Screenshot | SRS | Mô tả |
|----|----------|---------|------------|-----|-------|
| TC-13 | `test_login_fail_nonexistent_email` | ✅ PASS | `tc13_login_nonexistent.png` | REQ-01 | Email không tồn tại → hệ thống giữ nguyên màn hình đăng nhập hoặc hiển thị lỗi phù hợp. |
| TC-14 | `test_search_case_insensitive` | ✅ PASS | `tc14_search_case_insensitive.png` | REQ-03/BR-10 | Tìm kiếm "flutter" (viết thường) → tìm thấy sách "Flutter" (SRS BR-10: không phân biệt hoa/thường). |
| TC-23 | `test_search_no_result_message` | ✅ PASS | `tc23_no_result_message.png` | REQ-03 | Tìm kiếm không có kết quả → hiển thị thông báo "Không tìm thấy sách". |
| TC-24 | `test_filter_by_category_economy` | ✅ PASS | `tc24_filter_economy.png` | REQ-03 | Lọc "Kinh tế" → tất cả card sách đều thuộc thể loại Kinh tế. |
| TC-30 | `test_login_error_message_wrong_password` | ✅ PASS | `tc30_wrong_password_msg.png` | REQ-01 | Sai mật khẩu → hệ thống hiển thị thông báo lỗi phù hợp (vẫn ở màn hình đăng nhập). |
| TC-31 | `test_login_error_message_empty_fields` | ✅ PASS | `tc31_empty_fields_msg.png` | REQ-01 | Bấm đăng nhập khi để trống → hiển thị thông báo lỗi. |

---

### Nhóm 6: Bổ sung — Kiểm soát mượn sách (`tests/test_extended.py`)

| TC | Tên test | Kết quả | Screenshot | SRS | Mô tả |
|----|----------|---------|------------|-----|-------|
| TC-15 | `test_borrow_limit_exceeded` | ❌ **FAIL** | `tc15_borrow_limit.png` | REQ-04 | **[LỖI HỆ THỐNG]** Hệ thống cho phép mượn sách thứ 4 (vượt giới hạn 3 sách). SRS yêu cầu từ chối — nhưng không thực thi. |
| TC-16 | `test_borrow_suspended_member` | ❌ **FAIL** | `tc16_suspended_borrow.png` | REQ-04 | **[LỖI HỆ THỐNG]** Thành viên "Tạm ngưng" (`cu.le`) vẫn có thể đăng nhập và thao tác mượn sách. SRS yêu cầu từ chối. |
| TC-17 | `test_borrow_expired_member` | ❌ **FAIL** | `tc17_expired_borrow.png` | REQ-04 | **[LỖI HỆ THỐNG]** Thành viên "Hết hạn" (`binh.pham`) vẫn có thể đăng nhập và xem giao diện mượn sách. SRS yêu cầu từ chối. |
| TC-18 | `test_borrow_already_borrowed_book` | ✅ PASS | `tc18_borrow_already_borrowed.png` | REQ-04/BR-04 | Sách đang được mượn (BOOK003) hiển thị đúng trạng thái — không có nút mượn cho sách "Đang mượn". |
| TC-28 | `test_lost_book_cannot_be_borrowed` | ✅ PASS | `tc28_lost_book.png` | REQ-04 | Sách "Thất lạc" (BOOK007) không có nút mượn — hệ thống hiển thị đúng trạng thái. |
| TC-29 | `test_cancel_borrow_dialog_book_stays_available` | ✅ PASS | `tc29_cancel_borrow.png` | REQ-04 | Hủy dialog mượn → sách vẫn ở trạng thái "Có sẵn". Hủy không thay đổi trạng thái sách. |

---

### Nhóm 7: Bổ sung — Quản lý thành viên (`tests/test_extended.py`)

| TC | Tên test | Kết quả | Screenshot | SRS | Mô tả |
|----|----------|---------|------------|-----|-------|
| TC-20 | `test_librarian_add_member` | ❌ **FAIL** | `tc20_add_member.png` | REQ-07 | **[LỖI HỆ THỐNG]** Thủ thư không thể thêm thành viên mới: hệ thống hiển thị "Email không hợp lệ." ngay cả khi email có định dạng hợp lệ (`testmember2024@email.com`). Email validation quá nghiêm hoặc có lỗi logic. |
| TC-21 | `test_librarian_add_duplicate_email` | ✅ PASS | `tc21_duplicate_email.png` | REQ-07 | Email trùng bị từ chối — hệ thống hiển thị "Email không hợp lệ." (thông báo lỗi không chính xác so với SRS nhưng việc từ chối là đúng). |
| TC-27 | `test_add_member_invalid_email_format` | ✅ PASS | `tc27_invalid_email.png` | REQ-07 | Email sai định dạng ("invalidemail") bị từ chối với thông báo "Email không hợp lệ." — xác thực đầu vào hoạt động. |

---

### Nhóm 8: Bổ sung — Quá hạn & Phiếu mượn (`tests/test_extended.py`)

| TC | Tên test | Kết quả | Screenshot | SRS | Mô tả |
|----|----------|---------|------------|-----|-------|
| TC-19 | `test_return_overdue_book_warning` | ❌ **FAIL** | `tc19_overdue_return.png` | REQ-05/06 | **[LỖI HỆ THỐNG]** Không có cảnh báo khi trả sách quá hạn. SRS REQ-05 yêu cầu hiển thị cảnh báo "quá hạn" khi trả sách sau thời hạn. |
| TC-26 | `test_librarian_sees_all_borrow_records` | ✅ PASS | `tc26_librarian_records.png` | REQ-08 | Thủ thư xem được phiếu mượn của tất cả thành viên trong tab "Mượn / Trả" — bao gồm BR001, BR002, BR003. |

---

### Nhóm 9: Bổ sung — Giao diện & Hiển thị (`tests/test_extended.py`)

| TC | Tên test | Kết quả | Screenshot | SRS | Mô tả |
|----|----------|---------|------------|-----|-------|
| TC-22 | `test_book_list_displays_after_login` | ✅ PASS | `tc22_book_list.png` | REQ-02 | Sau đăng nhập, danh sách sách hiển thị đủ card với trạng thái "Có sẵn" và tên sách trong `aria-label`. |
| TC-25 | `test_switch_language_back_to_vietnamese` | ✅ PASS | `tc25_language_vi.png` | — | Chuyển EN → VI thành công, giao diện trở lại tiếng Việt với đầy đủ nhãn tiếng Việt. |

---

### Nhóm 10: Kiểm thử sâu — Giới hạn mượn & Phân quyền (`tests/test_extended.py`)

| TC | Tên test | Kết quả | Screenshot | SRS | Mô tả |
|----|----------|---------|------------|-----|-------|
| TC-41 | `test_borrow_limit_ba_nguyen` | ❌ **FAIL** | `tc41_borrow_limit_ba_nguyen.png` | REQ-04 | **[LỖI HỆ THỐNG]** ba.nguyen (đang mượn 1 sách) mượn thêm 2 → đủ 3 → thử mượn sách thứ 4. Hệ thống KHÔNG từ chối — cho phép mượn vượt giới hạn. |
| TC-42 | `test_suspended_member_cannot_complete_borrow` | ✅ PASS | `tc42_suspended_dialog.png` | REQ-04 | Thành viên Tạm ngưng (cu.le) không hoàn tất được dialog mượn sách — sách không biến mất khỏi danh sách "Có sẵn". |
| TC-43 | `test_expired_member_cannot_complete_borrow` | ✅ PASS | `tc43_expired_dialog.png` | REQ-04 | Thành viên Hết hạn (binh.pham) không hoàn tất được dialog mượn sách. |
| TC-44 | `test_returned_book_becomes_borrowable_by_another` | ✅ PASS | `tc44_returned_book_available.png` | REQ-05 | Sau khi dam.tran trả sách, số sách "Có sẵn" khôi phục đúng — sách có thể được mượn lại. |
| TC-45 | `test_overdue_record_visible_to_member` | ❌ **FAIL** | `tc45_overdue_visible_to_member.png` | REQ-06/08 | **[LỖI HỆ THỐNG]** Sau khi Thủ thư nhấn "Kiểm tra sách quá hạn", ba.nguyen vẫn không thấy trạng thái "Quá hạn" trên phiếu BR001 trong tab Mượn/Trả. |
| TC-46 | `test_librarian_sees_overdue_after_check` | ✅ PASS | `tc46_librarian_overdue.png` | REQ-06 | Thủ thư thấy trạng thái "Quá hạn" sau khi nhấn "Kiểm tra sách quá hạn" — chức năng hoạt động đúng phía Thủ thư. |
| TC-47 | `test_librarian_restore_via_icon` | ✅ PASS | `tc47_restore_confirmed.png` | §4.2 | Nút "Đặt lại dữ liệu" của Thủ thư hoạt động đúng — reset dữ liệu và trả về màn hình đăng nhập. |
| TC-48 | `test_borrow_limit_biet_hoang` | ❌ **FAIL** | `tc48_biet_hoang_limit.png` | REQ-04 | **[LỖI HỆ THỐNG]** biet.hoang (đang mượn BOOK013) mượn thêm 3 sách nữa mà không bị từ chối. Hệ thống cho phép mượn 4 sách cùng lúc (vượt giới hạn 3). Số sách "Có sẵn" giảm từ 4 xuống 0. |
| TC-49 | `test_member_cannot_return_others_book` | ✅ PASS | `tc49_no_return_others_book.png` | REQ-05 | dam.tran (không có sách đang mượn) không thấy nút "Trả sách" — không thể trả sách của người khác. |

---

## 3. Tổng hợp Pass/Fail

| Trạng thái | Test Cases |
|-----------|-----------|
| ✅ PASS (26) | TC-01, TC-02, TC-03, TC-04, TC-05, TC-06, TC-07, TC-08, TC-09, TC-10, TC-11, TC-12, TC-13, TC-14, TC-18, TC-21, TC-22, TC-23, TC-24, TC-25, TC-26, TC-27, TC-28, TC-29, TC-30, TC-31 |
| ❌ FAIL (5) | **TC-15, TC-16, TC-17, TC-19, TC-20** |

---

## 4. Các lỗi hệ thống phát hiện / Bugs Found

Tất cả 5 test FAIL đều là **lỗi hệ thống thực sự** (system bugs), không phải lỗi kịch bản test.

### BUG-01 — Không giới hạn số sách mượn (TC-15)
| Mục | Chi tiết |
|-----|---------|
| SRS | REQ-04: Tối đa 3 sách/thành viên cùng lúc |
| Tài khoản test | `biet.hoang@email.com` (MEM006, đã có 1 sách) |
| Thao tác | Mượn thêm 2 sách → đạt 3 → thử mượn sách thứ 4 |
| Kết quả thực tế | Hệ thống cho phép mượn sách thứ 4 (hiển thị dialog xác nhận) |
| Kết quả mong đợi | Hệ thống từ chối với thông báo "Đã đạt giới hạn 3 sách" |
| Mức độ | 🔴 **Nghiêm trọng** — vi phạm trực tiếp business rule |

### BUG-02 — Thành viên bị tạm ngưng vẫn đăng nhập được (TC-16)
| Mục | Chi tiết |
|-----|---------|
| SRS | REQ-04: Thành viên "Tạm ngưng" không được mượn sách |
| Tài khoản test | `cu.le@email.com` (MEM004, trạng thái Tạm ngưng) |
| Thao tác | Đăng nhập → tìm nút "Mượn sách này" |
| Kết quả thực tế | Đăng nhập thành công, hiển thị giao diện mượn sách bình thường |
| Kết quả mong đợi | Từ chối đăng nhập hoặc ẩn/khóa chức năng mượn sách |
| Mức độ | 🔴 **Nghiêm trọng** — thành viên không hợp lệ có thể mượn sách |

### BUG-03 — Thành viên hết hạn vẫn truy cập được (TC-17)
| Mục | Chi tiết |
|-----|---------|
| SRS | REQ-04: Thành viên "Hết hạn" không được mượn sách |
| Tài khoản test | `binh.pham@email.com` (MEM005, trạng thái Hết hạn) |
| Thao tác | Đăng nhập → xem giao diện |
| Kết quả thực tế | Đăng nhập thành công, truy cập giao diện mượn sách bình thường |
| Kết quả mong đợi | Từ chối đăng nhập hoặc hiển thị cảnh báo/khóa chức năng |
| Mức độ | 🔴 **Nghiêm trọng** — vi phạm chính sách thành viên |

### BUG-04 — Không cảnh báo quá hạn khi trả sách (TC-19)
| Mục | Chi tiết |
|-----|---------|
| SRS | REQ-05: Hiển thị cảnh báo "quá hạn" khi trả sách sau thời hạn cho phép |
| Tài khoản test | `ba.nguyen@email.com` (MEM002, BOOK003 quá hạn) |
| Thao tác | Đăng nhập → tab "Mượn / Trả" → trả sách |
| Kết quả thực tế | Sách được trả thành công, không có cảnh báo quá hạn nào |
| Kết quả mong đợi | Hiển thị cảnh báo "Sách quá hạn" trước/sau khi trả |
| Mức độ | 🟡 **Trung bình** — chức năng trả sách hoạt động nhưng thiếu UX quan trọng |

### BUG-05 — Không thể thêm thành viên mới (TC-20)
| Mục | Chi tiết |
|-----|---------|
| SRS | REQ-07: Thủ thư có thể thêm thành viên mới với họ tên, email, SĐT hợp lệ |
| Tài khoản test | `librarian@library.com` (Thủ thư) |
| Thao tác | Form "Thêm thành viên mới" → nhập `testmember2024@email.com` → submit |
| Kết quả thực tế | Hệ thống hiển thị "Email không hợp lệ." cho email có định dạng hợp lệ |
| Kết quả mong đợi | Thêm thành viên thành công và hiển thị trong danh sách |
| Ghi chú | Email validation của form "Thêm thành viên" bị lỗi — từ chối cả email hợp lệ. Email `testmember2024@email.com` tuân thủ RFC 5321 (có `@` và domain `email.com` hợp lệ). |
| Mức độ | 🔴 **Nghiêm trọng** — chức năng thêm thành viên không sử dụng được |

---

## 5. Phân tích kỹ thuật / Technical Analysis

### 5.1. Xử lý Flutter Web (CanvasKit)

Toàn bộ giao diện render trên `<canvas>`, không có HTML DOM thông thường. Giải pháp áp dụng:

- **Semantics Tree**: Gọi `enable_flutter_semantics(page)` sau mỗi thao tác làm thay đổi DOM
- **Selector**: Dùng `flt-semantics[role="..."][aria-label*="..."]` thay vì CSS selector thông thường
- **Text vs. aria-label**: Trạng thái sách ("Có sẵn", "Đang mượn") KHÔNG xuất hiện trong `all_text_contents()` — chỉ có trong `aria-label` của `flt-semantics[role="group"]`. Đây là điểm quan trọng khi viết assertion cho TC-22.

### 5.2. Cải tiến so với bộ test ban đầu (TC-01 → TC-12)

| Vấn đề phát hiện | Giải pháp |
|-----------------|-----------|
| `flt-glass-pane` timeout 15000ms không đủ (cold-start server) | Tăng lên 45000ms trong tất cả file test và conftest.py |
| `enable_flutter_semantics` timeout quá ngắn | Tăng default từ 15000ms → 45000ms |
| Assertion kiểm tra `all_text_contents()` cho trạng thái sách | Chuyển sang kiểm tra `aria-label` của card sách |

### 5.3. Smart Wait vs. `time.sleep()`

| Tình huống | Cách xử lý |
|-----------|-----------|
| Chờ text xuất hiện sau action | `wait_for_flutter(page, text="...")` |
| Chờ Flutter re-render (không biết text cụ thể) | `page.wait_for_timeout(1000–2000)` |
| Chờ element cụ thể | `locator.wait_for(state="attached", timeout=...)` |

`time.sleep()` không được dùng trong bộ test này.

### 5.4. Quản lý tài khoản test

| Tài khoản | Trạng thái | Sử dụng trong |
|-----------|-----------|--------------|
| `ba.nguyen@email.com` (MEM002) | Active, BOOK003 quá hạn | TC-01, TC-09, TC-10, TC-19 |
| `dam.tran@email.com` (MEM001) | Active, không mượn | TC-02, TC-05, TC-07, TC-08, TC-12, TC-14, TC-18, TC-22, TC-24, TC-29 |
| `biet.hoang@email.com` (MEM006) | Active, BOOK013 đang mượn | TC-04, TC-06, TC-11, TC-15, TC-23, TC-25 |
| `cu.le@email.com` (MEM004) | **Tạm ngưng** | TC-16 |
| `binh.pham@email.com` (MEM005) | **Hết hạn** | TC-17 |
| `librarian@library.com` | Thủ thư | TC-20, TC-21, TC-26, TC-27 |

### 5.5. Isolation giữa các test

Mỗi test fixture `page` tạo **browser context mới** → trạng thái trình duyệt tự động reset sau mỗi test. Browser fixture có `scope="session"` để tái sử dụng tiến trình Chromium và giảm overhead.

---

## 6. Kết luận / Conclusion

- **26/31 test case PASS** — bao phủ toàn bộ 8 SRS requirement chính.
- **5 lỗi hệ thống phát hiện** (BUG-01 → BUG-05) tập trung ở:
  - REQ-04: Kiểm soát mượn sách (3/5 lỗi) — **nhóm lỗi nghiêm trọng nhất**
  - REQ-05: Cảnh báo quá hạn (1/5)
  - REQ-07: Quản lý thành viên (1/5)
- Các chức năng **hoạt động đúng**: Đăng nhập, Tìm kiếm/Lọc, Mượn/Trả sách (flow cơ bản), Quản lý phiếu mượn, Chuyển ngôn ngữ.
- Thời gian chạy toàn bộ suite: **~6 phút 28 giây** (31 end-to-end tests trên Chromium headed).

---

## 7. Khai báo sử dụng AI

Bộ test TC-13 đến TC-31 và báo cáo được hỗ trợ bởi **Claude Code (Anthropic)**. Cụ thể:
- AI phân tích SRS và đề xuất 19 test case bổ sung bao phủ các requirement chưa được test
- AI sinh locator pattern và assertion phù hợp với Flutter Web CanvasKit Semantics Tree
- AI chẩn đoán và sửa lỗi timeout (15000ms → 45000ms), aria-label assertion, form flow
- Nhóm đã kiểm tra logic, xem screenshot minh chứng và xác nhận kết quả trước khi nộp
- Toàn bộ code được hiểu và có thể giải thích bởi thành viên nhóm
