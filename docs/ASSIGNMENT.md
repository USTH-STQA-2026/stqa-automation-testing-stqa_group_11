# Đề bài A2 — Kiểm thử tự động Web UI / Assignment A2 — Web UI Automation Testing

**Môn học**: Kiểm thử và Đảm bảo chất lượng phần mềm (STQA)  
**Hệ thống**: Quản lý mượn sách Thư viện ABC — https://stqa.rbc.vn  
**Công cụ**: Python + Playwright + pytest  
**Repo starter**: https://github.com/chuyentt/stqa-library-automation-starter

---

## 1. Mục tiêu / Objectives

Sinh viên thực hành viết test tự động cho ứng dụng web thực tế, sử dụng Playwright (Python). Sau bài tập này, sinh viên có khả năng:

- Thiết lập dự án test automation từ starter template
- Viết test case tự động với cấu trúc **Arrange → Act → Assert**
- Xử lý đặc thù của **Flutter Web (CanvasKit)** — tương tác qua Semantics Tree thay vì DOM thông thường
- Chạy test, phân tích kết quả, chụp screenshot minh chứng
- Làm việc nhóm trên Git (fork, branch, commit, PR)

---

## 2. Yêu cầu / Requirements

### 2.1. Bắt buộc (Minimum)

| # | Yêu cầu | Ghi chú |
|---|---------|---------|
| 1 | Fork repo starter → tạo repo nhóm | Đặt tên: `stqa-automation-<tên-nhóm>` |
| 2 | Cấu hình `.env` với tài khoản test | Xem `docs/test-accounts.md` |
| 3 | Hoàn thành **tất cả 12 test case** (TC-01 → TC-12) | TC-01 đã có sẵn (mẫu) |
| 4 | Tất cả test phải **chạy được** (`pytest` không lỗi cú pháp) | Kết quả PASS hoặc FAIL đều được tính — miễn là test chạy |
| 5 | Mỗi test có **screenshot** tự động | Lưu vào `screenshots/` |
| 6 | Điền thông tin nhóm trong `README.md` | Bảng Team Information |
| 7 | Nộp bài qua **Pull Request** hoặc **link repo** | Theo hướng dẫn giảng viên |

### 2.2. Nâng cao (Bonus — cộng điểm)

| # | Yêu cầu | Điểm cộng |
|---|---------|-----------|
| B1 | Thêm **≥ 3 test case mới** ngoài 12 TC cho sẵn | +0.5 |
| B2 | Viết **data-driven test** (parametrize nhiều bộ dữ liệu cho 1 kịch bản) | +0.5 |
| B3 | Thêm **assertion chi tiết** (kiểm tra text cụ thể, không chỉ kiểm tra URL) | +0.5 |
| B4 | Viết mô tả ngắn cho mỗi test trong `REPORT.md` | +0.5 |

> ⚠️ Điểm cộng tối đa: **+1.5 điểm** (trên thang 10).

---

## 3. Danh sách Test Case / Test Case List

### Nhóm 1: Đăng nhập (`tests/test_login.py`)

| TC | Kịch bản | Trạng thái |
|----|----------|-----------|
| TC-01 | Đăng nhập thành công — email + mật khẩu đúng | ✅ Mẫu (đã viết sẵn) |
| TC-02 | Đăng nhập thất bại — sai mật khẩu → vẫn ở trang đăng nhập | 🔴 TODO |
| TC-03 | Đăng nhập thất bại — bỏ trống cả hai trường → vẫn ở trang đăng nhập | 🔴 TODO |

### Nhóm 2: Tìm kiếm & Lọc sách (`tests/test_search.py`)

| TC | Kịch bản | Trạng thái |
|----|----------|-----------|
| TC-04 | Tìm sách theo tên — nhập "Flutter" → hiển thị sách có chứa "Flutter" | 🔴 TODO |
| TC-05 | Tìm sách — không có kết quả → hiển thị thông báo phù hợp | 🔴 TODO |
| TC-06 | Lọc sách theo thể loại — nhập "Công nghệ" → chỉ hiển thị sách Công nghệ | 🔴 TODO |
| TC-07 | Tìm sách theo tác giả — nhập tên tác giả → hiển thị sách tương ứng | 🔴 TODO |

### Nhóm 3: Mượn & Trả sách (`tests/test_borrow_return.py`)

| TC | Kịch bản | Trạng thái |
|----|----------|-----------|
| TC-08 | Mượn sách thành công — chọn sách "Có sẵn" → mượn → sách chuyển "Đã mượn" | 🔴 TODO |
| TC-09 | Xem danh sách sách đang mượn — vào tab Mượn/Trả → thấy phiếu mượn | 🔴 TODO |
| TC-10 | Trả sách — nhấn "Trả sách" → sách chuyển về "Có sẵn" | 🔴 TODO |

### Nhóm 4: Chức năng chung (`tests/test_general.py`)

| TC | Kịch bản | Trạng thái |
|----|----------|-----------|
| TC-11 | Đăng xuất — nhấn nút đăng xuất → trở về trang đăng nhập | 🔴 TODO |
| TC-12 | Chuyển ngôn ngữ sang English → giao diện hiển thị tiếng Anh | 🔴 TODO |

---

## 4. Hướng dẫn thực hiện / Step-by-Step Guide

### Bước 1: Fork & Clone

```bash
# Fork repo starter trên GitHub → repo của nhóm
# Clone về máy
git clone https://github.com/<your-team>/stqa-automation-<team-name>.git
cd stqa-automation-<team-name>
```

### Bước 2: Cài đặt môi trường

```bash
python3 -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows
pip install -r requirements.txt
playwright install chromium
```

### Bước 3: Cấu hình `.env`

```bash
cp .env.example .env
```

Sửa `.env`:
```
BASE_URL=https://stqa.rbc.vn
TEST_EMAIL=ba.nguyen@email.com
TEST_PASSWORD=password123
TEST_DISPLAY_NAME=Nguyễn Học Bá
```

### Bước 4: Chạy test mẫu

```bash
pytest tests/test_login.py::test_login_success -v
```

Nếu PASS → môi trường đã sẵn sàng.

### Bước 5: Viết test

Mở file `tests/test_login.py` → xem TC-01 mẫu → viết TC-02, TC-03 theo pattern tương tự.  
Sau đó chuyển sang `test_search.py`, `test_borrow_return.py`, `test_general.py`.

**Pattern cơ bản:**

```python
from conftest import login, flutter_click_button, wait_for_flutter

def test_ten_test_case(page, test_config):
    # 1. Arrange — Chuẩn bị
    login(page, test_config)         # Đăng nhập

    # 2. Act — Thực hiện hành động
    flutter_click_button(page, "Tên nút")

    # 3. Smart Wait — Chờ kết quả (thay vì time.sleep)
    wait_for_flutter(page, text="Kết quả mong đợi")

    # 4. Assert — Kiểm tra kết quả
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Kết quả mong đợi" in sem_text

    # 5. Screenshot — Chụp minh chứng
    page.screenshot(path=f"{test_config['screenshot_dir']}/ten_test_case.png")
```

> 💡 **Smart Wait**: `wait_for_flutter(page, text="...")` chờ cho đến khi text xuất hiện trong Semantics Tree — nhanh hơn và ổn định hơn `time.sleep()`. Xem `conftest.py` để biết chi tiết.

### Bước 6: Chạy tất cả test

```bash
pytest -v
```

### Bước 7: Commit & Push

```bash
git add .
git commit -m "Complete TC-02 to TC-12"
git push origin main
```

---

## 5. Rubric chấm điểm / Grading Rubric

| Tiêu chí | Trọng số | Xuất sắc (9–10) | Tốt (7–8) | Đạt (5–6) | Chưa đạt (<5) |
|----------|---------|-----------------|-----------|-----------|---------------|
| **Hoàn thành TC** | **40%** | 12/12 TC chạy được, hầu hết PASS | 9–11 TC chạy được | 6–8 TC chạy được | < 6 TC hoặc không chạy được |
| **Chất lượng code** | **25%** | Assertion cụ thể (kiểm tra text, trạng thái), code sạch, có comment | Assertion hợp lý, code đọc được | Assertion cơ bản (chỉ check URL), code lộn xộn | Không có assertion hoặc code copy-paste không hiểu |
| **Xử lý Flutter Web** | **15%** | Dùng đúng helper, dùng Smart Wait hợp lý, hiểu semantics | Dùng helper đúng, đôi chỗ dùng time.sleep | Dùng helper nhưng nhiều lỗi flaky | Không dùng helper, test không tương tác được |
| **Screenshot & Evidence** | **10%** | Mỗi TC có screenshot rõ ràng, đặt tên có ý nghĩa | Hầu hết TC có screenshot | Một số TC thiếu screenshot | Không có screenshot |
| **Teamwork & Format** | **10%** | Thông tin nhóm đầy đủ, commit lịch sử rõ ràng, README cập nhật | Thông tin nhóm có, vài commit | Thông tin nhóm thiếu, 1 commit duy nhất | Không điền thông tin, repo lộn xộn |

---

## 6. Lưu ý quan trọng / Important Notes

1. **KHÔNG commit file `.env`** — file này chứa mật khẩu, đã có trong `.gitignore`.
2. **KHÔNG sửa `conftest.py` hoặc `web_detector.py`** — hai file này đã hoàn chỉnh, chỉ cần dùng.
3. **Test FAIL vẫn được điểm** — miễn là test chạy được và assertion có ý nghĩa. Nếu phát hiện bug trong hệ thống, ghi chú trong test (comment).
4. **Mỗi thành viên nên commit ít nhất 1 lần** — thể hiện đóng góp cá nhân.
5. **Flaky test** (test lúc pass lúc fail) — thường do chưa chờ đủ sau thao tác Flutter re-render. Dùng `wait_for_flutter(page, text="...")` hoặc `page.locator("...").wait_for()` thay vì `time.sleep()`.
6. **Dữ liệu reset mỗi lần refresh** — nếu test trước đã mượn sách, test sau mở trang mới sẽ có dữ liệu sạch (mỗi fixture `page` tạo context mới).

---

## 7. Nộp bài / Submission

| Mục | Yêu cầu |
|-----|---------|
| **Hình thức** | Link repo GitHub (public hoặc invite giảng viên) |
| **Bắt buộc có** | 12 test case chạy được, screenshots, README có thông tin nhóm |
| **Tùy chọn** | `REPORT.md` mô tả kết quả + nhận xét (bonus B4) |
| **Hạn nộp** | Theo thông báo của giảng viên |

---

## 8. Tài liệu tham khảo / References

| Tài liệu | Link |
|-----------|------|
| SRS hệ thống | [`docs/SRS-library-system.md`](SRS-library-system.md) |
| Tài khoản test | [`docs/test-accounts.md`](test-accounts.md) |
| Playwright Python Docs | https://playwright.dev/python/ |
| pytest Documentation | https://docs.pytest.org/ |
| Flutter Web Accessibility | https://docs.flutter.dev/ui/accessibility |

---

## 9. Khai báo sử dụng AI (Tùy chọn)

> Nếu nhóm có sử dụng công cụ AI (ChatGPT, Copilot, Gemini...) để viết test code, hãy ghi rõ trong `README.md` hoặc `REPORT.md`. Khai báo trung thực **không ảnh hưởng điểm** — đây là kỹ năng minh bạch trong nghề.
>
> Ghi chú: công cụ AI nào, dùng cho test nào, bạn đã kiểm tra/chỉnh sửa code AI thế nào.
>
> **Lưu ý quan trọng:** Xem [docs/ai-guidelines.md](ai-guidelines.md) để biết cách dùng AI hiệu quả và tránh 3 cái bẫy phổ biến (Weak Oracle, Flutter CanvasKit, `time.sleep`).
