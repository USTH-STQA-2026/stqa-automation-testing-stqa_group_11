# Khái niệm Textbook — Liên kết Lý thuyết ↔ Thực hành

> 📖 **Textbook:** Paul Ammann & Jeff Offutt, *Introduction to Software Testing*, 2nd Edition.
>
> Tài liệu này giải thích cách các khái niệm trong textbook được **áp dụng trực tiếp** trong repo automation này.

---

## 1. RIPR Model — Mô hình phát hiện lỗi (Ch.2)

Để một bài test phát hiện được lỗi, **4 điều kiện** sau phải đồng thời thỏa mãn:

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Reachability │ → │  Infection   │ → │ Propagation  │ → │ Revealability│
│              │   │              │   │              │   │              │
│ Test chạm    │   │ Trạng thái   │   │ Lỗi lan      │   │ Assertion    │
│ đến code lỗi │   │ bị nhiễm     │   │ truyền ra    │   │ phát hiện    │
│              │   │ (infected)   │   │ output       │   │ được lỗi     │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

### Áp dụng trong repo này

Xem file `tests/test_login.py` — TC-01 đã được đánh dấu RIPR:

| Bước RIPR | Dòng code | Giải thích |
|---|---|---|
| **[R] Reachability** | `page.goto(...)` | Chạm tới trang đăng nhập |
| **[I] Infection** | `flutter_fill(..., "email")` | Nhập dữ liệu → kích hoạt logic hệ thống |
| **[P] Propagation** | `wait_for_flutter(page, text="Đăng xuất")` | Chờ kết quả lan truyền ra UI |
| **[R✓] Revealability** | `assert has_user_name or has_logout` | Test Oracle kiểm tra → phát hiện lỗi nếu có |

### Ví dụ lỗi bộc lộ

Nếu assertion quá yếu (ví dụ: chỉ kiểm tra URL mà không kiểm tra text hiển thị), **Revealability bị gãy** → bug lọt qua dù đã lan truyền ra UI. Khi viết test, hãy tự hỏi: *"Assertion của mình có đủ mạnh để bắt lỗi không?"*

---

## 2. Test Doubles — Hiểu kiến trúc hệ thống (Ch.12)

### Tại sao hệ thống KHÔNG cần server thật?

Hệ thống thư viện tại https://stqa.rbc.vn sử dụng kiến trúc **Test Double** — thay thế backend thật bằng một module mô phỏng:

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   UI Layer  │ ───→ │  Mock API Client │ ───→ │ Library Service │
│ (Flutter)   │      │  (Giả lập HTTP)  │      │ (In-memory DB)  │
└─────────────┘      └──────────────────┘      └─────────────────┘
                           ↑                          ↑
                     Mô phỏng HTTP              Xử lý nghiệp vụ
                     status codes               trong bộ nhớ
                     + network delay            (không cần DB thật)
```

### Ánh xạ với textbook (Chapter 12)

| Khái niệm textbook | Thành phần trong hệ thống | Giải thích |
|---|---|---|
| **Stub** | Library Service + Seed Data | Trả về dữ liệu cố định (20 sách, 6 thành viên) — không gọi API thật |
| **Mock** | Mock API Client | Mô phỏng HTTP response (200/400/403/409) + network delay |
| **Test Fixture** | Dữ liệu seed + nút "Khôi phục dữ liệu" | Đảm bảo test lặp lại được (repeatable) |

### Ý nghĩa cho Tester

- **Dữ liệu reset được**: Refresh trang = dữ liệu trở về ban đầu → mỗi lần test bắt đầu từ cùng trạng thái.
- **Không phụ thuộc mạng**: Hệ thống chạy hoàn toàn trong trình duyệt → test ổn định, không flaky.
- **Bug cố ý**: Hệ thống được cài sẵn 7 bug cho mục đích học tập — nhiệm vụ của bạn là tìm chúng!

> 💡 **Câu hỏi tư duy**: Nếu thay Mock API Client bằng server thật, test automation của bạn có cần thay đổi gì không? Phần nào trong code test bị ảnh hưởng?

---

## 3. Data-Driven Testing — Tách dữ liệu khỏi code (Ch.3 §3.3.2)

### Vấn đề

TC-02 (sai mật khẩu) và TC-03 (bỏ trống) có **cùng pattern**:
1. Mở trang đăng nhập
2. Nhập dữ liệu (khác nhau)
3. Click "Đăng nhập"
4. Kiểm tra vẫn ở trang đăng nhập

Viết riêng 2 hàm test → **lặp code** (violate DRY).

### Giải pháp: `@pytest.mark.parametrize`

```python
@pytest.mark.parametrize(
    "email, password, tc_id",
    [
        ("valid@email.com", "wrongpass", "TC-02"),   # Sai mật khẩu
        ("", "", "TC-03"),                            # Bỏ trống
    ],
)
def test_login_fail(page, test_config, email, password, tc_id):
    """TC-02 & TC-03: Đăng nhập thất bại — Data-Driven"""
    page.goto(test_config["base_url"], ...)
    # ... logic chung cho cả 2 TC
    assert ...  # Kiểm tra vẫn ở trang đăng nhập
```

### Lợi ích

| Trước (viết riêng) | Sau (@parametrize) |
|---|---|
| 2 hàm test, code gần giống nhau | 1 hàm + 2 bộ dữ liệu |
| Thêm TC mới = viết thêm hàm | Thêm TC mới = thêm 1 dòng tuple |
| Khó bảo trì khi logic thay đổi | Sửa 1 chỗ = áp dụng cho tất cả |

> Tương đương **DataPoints** trong JUnit (textbook Ch.3 §3.3.3). Đây là requirement của Bonus B2.

---

## 4. Test Oracle — Ai phán đúng/sai? (Ch.14)

**Test Oracle** = cơ chế quyết định test PASS hay FAIL. Trong automation, đó chính là dòng `assert`.

### Oracle yếu vs Oracle mạnh

```python
# ❌ Oracle yếu — chỉ kiểm tra URL
assert page.url == "https://stqa.rbc.vn"
# → Bug có thể lan truyền ra UI nhưng URL không đổi → PASS giả!

# ✅ Oracle mạnh — kiểm tra cả URL + text hiển thị
assert page.url == "https://stqa.rbc.vn"
sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
assert "Đăng xuất" in sem_text, "Không thấy nút Đăng xuất sau đăng nhập"
```

### Nguyên tắc

- Mỗi test nên có **ít nhất 1 assertion cụ thể** kiểm tra text/trạng thái hiển thị.
- Assertion kiểm tra URL chỉ là **điều kiện cần**, không đủ.
- Tham khảo Bonus B3: "assertion chi tiết" = kiểm tra text cụ thể, không chỉ URL.

---

## Tóm tắt: Ánh xạ repo ↔ textbook

| File trong repo | Khái niệm textbook | Chương |
|---|---|---|
| `tests/test_login.py` (TC-01) | RIPR Model — [R], [I], [P], [R✓] | Ch.2 |
| `tests/test_login.py` (TC-02, TC-03) | Data-Driven Testing / @parametrize | Ch.3 §3.3.2 |
| `conftest.py` (helper functions) | Test Harness / Test Infrastructure | Ch.3 |
| Hệ thống https://stqa.rbc.vn | Test Doubles (Mock/Stub/Fixture) | Ch.12 |
| Mỗi dòng `assert` | Test Oracle — Revealability | Ch.14 |
| `docs/SRS-library-system.md` | Model / Abstraction Level (cho IDM) | Ch.6 §6.1 |
| `docs/group-exercises.md` (BT4) | FSM, State/Transition Coverage | Ch.7 §7.5.2 |
| `docs/group-exercises.md` (BT5) | Null Oracle, Oracle Precision | Ch.14 §14.1 |
| `docs/group-exercises.md` (BT6) | Regression Testing, Test Selection | Ch.13 |
| `docs/group-exercises.md` (BT7) | Mutation Testing, ROR, BVA↔Mutation | Ch.9 §9.1.2, §9.2.2, Ch.6 |
