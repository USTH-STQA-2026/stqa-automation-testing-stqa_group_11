# Hướng dẫn sử dụng AI — AI Usage Guidelines

> **Nguyên tắc:** Bạn là **Test Oracle**, AI là **thợ gõ**. AI có thể sinh kịch bản nhanh, nhưng **bạn chịu trách nhiệm đánh giá đúng/sai**. Theo mô hình RIPR đã học, bug chỉ bộc lộ (Revealability) khi Oracle đủ mạnh — và AI thường sinh ra Oracle rất yếu.

---

## 3 Cái bẫy khi dùng AI cho dự án này

### Bẫy 1: Weak Oracle — AI viết assert hời hợt

AI thường chỉ kiểm tra "hệ thống không crash" hoặc "trang load xong" — đó là **Null Oracle** (Ch.14). Bug thật sẽ lọt qua vì Revealability bị gãy.

**Ví dụ:**
```python
# ❌ AI thường sinh ra — Null Oracle (chỉ check không crash)
assert page.url != "about:blank"

# ✅ Bạn phải sửa lại — Strong Oracle (kiểm tra nội dung cụ thể từ SRS)
sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
assert "Mượn sách thành công" in sem_text
```

**Đối chiếu:** Mỗi `assert` phải kiểm tra **kết quả mong đợi cụ thể từ SRS**, không phải "trang vẫn sống".

### Bẫy 2: Flutter CanvasKit — AI viết selector sai 99%

Hệ thống thư viện dùng Flutter Web CanvasKit — **không có HTML DOM thông thường**. AI sẽ sinh ra `page.fill('input[type="email"]')` → **chắc chắn FAIL**.

**Bí kíp Prompting:** Khi nhờ AI viết code Playwright, **luôn kèm context này:**

> *"Hệ thống đang test là Flutter Web CanvasKit, tương tác qua Accessibility Semantics Tree (`flt-semantics`). KHÔNG dùng CSS selector thông thường. Tôi đã có sẵn helper functions trong `conftest.py`: `flutter_fill(page, label, value)`, `flutter_click_button(page, text)`, `wait_for_flutter(page, text)`, `login(page, test_config)`. Hãy sử dụng các hàm này."*

### Bẫy 3: `time.sleep()` — AI gợi ý "thuốc độc"

Khi test flaky, AI rất hay gợi ý `time.sleep(3)`. Đây là **anti-pattern** — làm chậm CI và vẫn không ổn định (xem BT9 trong bài tập nhóm).

```python
# ❌ AI gợi ý — non-deterministic, chậm, vẫn flaky
time.sleep(3)

# ✅ Đã có sẵn trong conftest.py — deterministic polling
wait_for_flutter(page, text="Đăng xuất")
```

---

## Cách dùng AI hiệu quả

| NÊN | KHÔNG NÊN |
|-----|-----------|
| Copy SRS requirement → nhờ AI gợi ý vùng dữ liệu EP/BVA | Nhờ AI bịa test data — đã có `test-accounts.md` và Seed Data |
| Dán Traceback/Error log → nhờ AI giải thích lỗi | Nhờ AI viết full test rồi copy nguyên — bạn sẽ không hiểu khi debug |
| Nhờ AI giải thích `conftest.py`, `pytest.ini` hoạt động thế nào | Dùng `time.sleep()` theo gợi ý AI — luôn dùng `wait_for_flutter()` |
| Nhờ AI review assertion → tự đánh giá Oracle mạnh hay yếu | Tin assert của AI mà không đối chiếu SRS |

---

## Khai báo (tùy chọn nhưng khuyến khích)

Nếu nhóm dùng AI, ghi 1 dòng vào phần "Khai báo sử dụng AI" trong `submissions/summary.md`:

> *"Nhóm đã dùng [tên công cụ] để [mục đích cụ thể], sau đó tự đối chiếu lại với SRS."*

Khai báo trung thực **không ảnh hưởng điểm** — đây là kỹ năng minh bạch trong nghề QA.
