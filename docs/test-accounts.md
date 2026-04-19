# Tài khoản kiểm thử / Test Accounts

**Hệ thống**: https://stqa.rbc.vn

> ⚠️ Dữ liệu được lưu trong bộ nhớ trình duyệt. Mỗi tab là phiên riêng biệt. Refresh trang = dữ liệu trở về trạng thái ban đầu.

---

## Tài khoản Thủ thư / Librarian Account

| Mục | Giá trị |
|-----|---------|
| Email | `librarian@library.com` |
| Mật khẩu | `admin123` |
| Vai trò | Thủ thư (Librarian) |
| Tên hiển thị | Nguyễn Thủ Thư |

**Quyền đặc biệt**: Xem tất cả phiếu mượn, thêm thành viên, kiểm tra quá hạn, khôi phục dữ liệu.

---

## Tài khoản Thành viên / Member Accounts

| Email | Mật khẩu | Tên hiển thị | ID | Trạng thái | Đặc điểm kiểm thử |
|-------|----------|-------------|-----|-----------|-------------------|
| `ba.nguyen@email.com` | `password123` | Nguyễn Học Bá | MEM002 | ✅ Hoạt động | Đang mượn 1 sách (BOOK003 — quá hạn) |
| `dam.tran@email.com` | `password123` | Trần Dựa Dẫm | MEM003 | ✅ Hoạt động | Chưa mượn sách nào — **phù hợp nhất để test mượn/trả** |
| `cu.le@email.com` | `password123` | Lê Cần Cù | MEM004 | 🔴 Tạm ngưng | Thử mượn sách → quan sát hành vi từ chối |
| `binh.pham@email.com` | `password123` | Phạm Trung Bình | MEM005 | 🔴 Hết hạn | Thử mượn sách → quan sát thông báo lỗi |
| `biet.hoang@email.com` | `password123` | Hoàng Cá Biệt | MEM006 | ✅ Hoạt động | Chưa mượn sách nào — phù hợp test giới hạn mượn |

---

## Cấu hình `.env` / Environment Configuration

Copy `.env.example` → `.env` rồi điền thông tin:

### Dùng tài khoản thành viên (khuyến nghị cho hầu hết test):

```env
BASE_URL=https://stqa.rbc.vn
TEST_EMAIL=ba.nguyen@email.com
TEST_PASSWORD=password123
TEST_DISPLAY_NAME=Nguyễn Học Bá
```

### Dùng tài khoản thủ thư (cho test quản lý thành viên):

```env
BASE_URL=https://stqa.rbc.vn
TEST_EMAIL=librarian@library.com
TEST_PASSWORD=admin123
TEST_DISPLAY_NAME=Nguyễn Thủ Thư
```

> 💡 **Mẹo**: Một số test case cần đăng nhập bằng tài khoản khác (ví dụ test mượn sách cần thành viên chưa mượn gì). Trong trường hợp đó, hãy gọi trực tiếp các helper function thay vì dùng fixture `test_config`:
>
> ```python
> flutter_fill(page, "Email", "dam.tran@email.com")
> flutter_fill(page, "Mật khẩu", "password123")
> flutter_click_button(page, "Đăng nhập")
> ```

---

## Khôi phục dữ liệu / Data Reset

Hệ thống lưu dữ liệu tạm trong bộ nhớ trình duyệt. Khi cần đưa về trạng thái gốc:

- **Trong test automation**: Mỗi fixture `page` tạo browser context mới → dữ liệu tự động sạch.
- **Khi test thủ công**: Refresh trang (F5) hoặc đăng nhập Thủ thư → nhấn nút **🔄** → xác nhận "Đặt lại".

> 💡 **Mẹo**: Nếu test trước mượn/trả sách làm thay đổi dữ liệu, test sau vẫn an toàn vì mỗi test có page context riêng.

---

## Tài khoản không hợp lệ (dùng cho test thất bại)

| Kịch bản | Email | Mật khẩu |
|----------|-------|----------|
| Email không tồn tại | `nobody@test.com` | `anything` |
| Sai mật khẩu | `ba.nguyen@email.com` | `wrongpassword` |
| Bỏ trống | *(để trống)* | *(để trống)* |
