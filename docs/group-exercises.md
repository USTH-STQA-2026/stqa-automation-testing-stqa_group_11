# Bài tập nhóm — Thảo luận & Nghiên cứu sâu

> 📖 **Textbook:** Paul Ammann & Jeff Offutt, *Introduction to Software Testing*, 2nd Edition.
>
> **Mục tiêu:** Hiểu các khái niệm mới: **RIPR Model**, **Model-Driven Test Design**, **Test Oracle**.

---

## Bài tập 1: Cuộc chiến của những chiếc hộp (The "Box" Debate)

> ⏱ **Thời gian:** 15–20 phút | **Chương liên quan:** Ch.2 §2.4–2.5, Ch.6

### Bối cảnh

Chúng ta thường chia kiểm thử thành **Hộp đen** (Black-box — chỉ nhìn SRS) và **Hộp trắng** (White-box — nhìn code). Nhưng tác giả cho rằng ranh giới này **lỗi thời**:

> *"Thus asking whether a coverage criterion is black-box or white-box is the wrong question. One more properly should ask from what level of abstraction is the structure drawn."*
> — Ammann & Offutt, Ch.2, p.58

### Nhiệm vụ nhóm

1. **Mở file** `docs/SRS-library-system.md` — đây là "Black-box model".

2. **Đọc đoạn trích code backend** dưới đây — đây là "White-box model" (code Dart xử lý nghiệp vụ mượn sách):

   ```dart
   // Trích từ library_service.dart — hàm borrowBook()
   ServiceResult<BorrowRecord> borrowBook({required String memberId, required String bookId}) {
     final member = getMemberById(memberId);
     if (member == null) return ServiceResult.error('Không tìm thấy thành viên.');

     // Kiểm tra trạng thái thành viên
     if (member.status == MemberStatus.expired)
       return ServiceResult.error('Thành viên đã hết hạn. Không thể mượn sách.');
     if (member.status == MemberStatus.suspended)
       return ServiceResult.error('Thành viên đang bị tạm ngưng. Không thể mượn sách.');

     final book = getBookById(bookId);
     if (book == null) return ServiceResult.error('Không tìm thấy sách.');
     if (book.status != BookStatus.available)
       return ServiceResult.error('Sách không có sẵn để mượn.');

     // Kiểm tra giới hạn mượn
     final currentBorrowCount = _records
         .where((r) => r.memberId == memberId && r.status == BorrowStatus.borrowing)
         .length;
     if (currentBorrowCount >= maxBooksPerMember)  // maxBooksPerMember = 3
       return ServiceResult.error('Đã đạt giới hạn mượn tối đa (3 sách).');

     // Tạo phiếu mượn, cập nhật trạng thái sách
     final record = BorrowRecord(
       memberId: memberId, bookId: bookId,
       borrowDate: DateTime.now(),
       dueDate: DateTime.now().add(Duration(days: 14)),  // borrowDurationDays = 14
     );
     return ServiceResult.ok(record);
   }
   ```

3. **Thiết kế 6 giá trị test cho tính năng "Mượn sách":**

   | # | Nguồn gốc | Test Value (Mô tả) | Dữ liệu cụ thể |
   |---|---|---|---|
   | 1 | Từ SRS (Black-box) | `<!-- Nhóm tự điền -->` | |
   | 2 | Từ SRS (Black-box) | | |
   | 3 | Từ SRS (Black-box) | | |
   | 4 | Từ Code (White-box) | | |
   | 5 | Từ Code (White-box) | | |
   | 6 | Từ Code (White-box) | | |

4. **Câu hỏi thảo luận:**

   a. Các giá trị test từ SRS và từ Code có **khác nhau** không? Có trùng nhau không?

   b. Tại sao hỏi *"Test này là Black-box hay White-box?"* lại là **câu hỏi sai**? Ta nên hỏi gì thay thế?

   c. **Gợi ý:** SRS là một **model** ở mức trừu tượng cao, code Dart là **model** ở mức thấp — cả hai đều là model. Câu hỏi đúng: *"Test được thiết kế từ model nào?"*

---

## Bài tập 2: Phá án cùng mô hình RIPR (The RIPR Detective)

> ⏱ **Thời gian:** 15 phút | **Chương liên quan:** Ch.2 §2.1, Ch.14

### Kịch bản giả định

Nhóm bạn đang kiểm thử tính năng "Tìm kiếm sách" (TC-05: tìm kiếm không có kết quả). Bạn nhập từ khóa `"xyz_khong_ton_tai"` vào ô tìm kiếm. Kết quả:

- **Kết quả mong đợi**: Danh sách rỗng, không hiển thị sách nào
- **Kết quả thực tế**: Giao diện vẫn **hiển thị sách từ lần tìm trước** (lỗi UI!)
- **Kết quả test**: Bạn ghi **PASS** vì "không có thông báo lỗi"

→ Bug đã tồn tại và hiển thị trên giao diện, nhưng bạn không phát hiện!

### Nhiệm vụ nhóm

1. **Vẽ sơ đồ 4 bước RIPR:**

   ```
   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │ Reachability │ → │  Infection   │ → │ Propagation  │ → │ Revealability│
   │   Chạm tới   │   │ Nhiễm trạng  │   │ Lan truyền   │   │  Bộc lộ lỗi  │
   │              │   │  thái lỗi    │   │  ra output   │   │  cho tester  │
   └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
          ✅                 ✅                 ✅                 ❌ ← GÃY!
   ```

2. **Câu hỏi thảo luận:**

   a. Bug đã **Reach** → **Infect** → **Propagate** ra UI. Vậy **bước nào** bị gãy? Tại sao?

   b. **Revealability** bị gãy vì **Test Oracle yếu**: "Kết quả mong đợi" quá chung chung. Hãy viết lại KQ mong đợi sao cho **rõ ràng, kiểm chứng được**:

   | | Trước (yếu) | Sau (mạnh) |
   |---|---|---|
   | KQ mong đợi | "Không có lỗi" | `<!-- Nhóm viết lại -->` |

   c. Nếu bạn làm **automation** (bài A2), dòng `assert` trong code tương đương với điều gì trong manual testing? (Gợi ý: "Kết quả mong đợi" = Test Oracle)

---

## Bài tập 3: Ai bảo vệ phần mềm? (Test Suite vs SRS)

> ⏱ **Thời gian:** 15 phút | **Chương liên quan:** Ch.4 §4.2

### Bối cảnh

Theo góc nhìn Agile và TDD:

> *"In agile methods, test cases are the de facto specification for the system."*
> — Ammann & Offutt, Ch.4, p.99

### Nhiệm vụ nhóm

1. **Xem xét 12 Test Case** (TC-01 → TC-12) được mô tả trong SRS:

   | Nhóm chức năng | TCs | Chức năng |
   |---|---|---|
   | Đăng nhập | TC-01, TC-02, TC-03 | Đăng nhập thành công/thất bại |
   | Tìm kiếm & Lọc | TC-04 ~ TC-07 | Tìm theo tên/tác giả, lọc thể loại |
   | Mượn & Trả | TC-08, TC-09, TC-10 | Mượn sách, xem danh sách, trả sách |
   | Chức năng chung | TC-11, TC-12 | Đăng xuất, chuyển ngôn ngữ |

2. **Câu hỏi thảo luận:**

   a. Nếu file `SRS-library-system.md` **bị xóa mất**, liệu một lập trình viên mới có thể **chỉ nhìn** vào TC-08 ~ TC-10 để code lại tính năng mượn/trả sách không? Vì sao?

   b. Liệt kê **những thông tin nghiệp vụ** mà TC-08 (Mượn sách) cho biết:

   | # | Thông tin (đọc được từ test) | Nguồn |
   |---|---|---|
   | 1 | `<!-- Nhóm tự điền -->` | |
   | 2 | | |
   | 3 | | |

   c. **Giới hạn**: Góc nhìn "Test là tài liệu" yếu ở đâu?
      - Kịch bản người dùng thao tác sai (negative) mà chưa nghĩ tới?
      - Yêu cầu phi chức năng (hiệu suất, bảo mật)?
      - Nghiệp vụ thay đổi mà test chưa cập nhật?

   d. **Kết luận nhóm:** SRS và Test Suite nên **cùng tồn tại** hay chỉ cần 1 trong 2? Giải thích.

---

## Bài tập 4: Vòng đời cuốn sách — Đồ thị trạng thái / The Book Lifecycle FSM

> ⏱ **Thời gian:** 20 phút | **Chương liên quan:** Ch.7 §7.5.2 (p.223–234)
>
> 🌐 **Song ngữ / Bilingual:** Thuật ngữ gốc tiếng Anh được giữ nguyên trong ngoặc.

### Bối cảnh / Context

Mỗi cuốn sách trong hệ thống trải qua các trạng thái khác nhau — đây chính là một **Finite State Machine (FSM)**:

> *"A Finite State Machine is a graph whose nodes represent states... and edges represent transitions among the states."*
> — Ammann & Offutt, Ch.7 §7.5.2, p.224

### Bước 1: Trạng thái (States) và Chuyển tiếp (Transitions)

| Ký hiệu | Trạng thái | State (EN) | Ví dụ trong seed data |
|----------|-----------|------------|----------------------|
| **S1** | Có sẵn | Available | BOOK001, BOOK002 |
| **S2** | Đang mượn | Borrowed | BOOK003 |
| **S3** | Quá hạn | Overdue | Khi quá 14 ngày chưa trả |
| **S4** | Thất lạc | Lost | BOOK007 |

| Ký hiệu | Sự kiện | Trigger (EN) | Từ → Đến |
|----------|---------|-------------|-----------|
| **T1** | Mượn sách | Borrow | S1 → S2 |
| **T2** | Trả sách (đúng hạn) | Return (on time) | S2 → S1 |
| **T3** | Kiểm tra quá hạn | Check overdue | S2 → S3 |
| **T4** | Trả sách (trễ hạn) | Return (late) | S3 → S1 |
| **T5** | Đánh dấu thất lạc | Mark as lost | S3 → S4 |

### Bước 2: Vẽ sơ đồ FSM trên giấy

```
                    T1: Mượn sách                T3: Quá hạn
              ┌─────────────────┐         ┌──────────────────┐
              │                 ▼         │                  ▼
         ┌─────────┐       ┌─────────┐       ┌─────────┐       ┌─────────┐
   ●───→ │   S1    │       │   S2    │       │   S3    │       │   S4    │
         │ Có sẵn  │ ◀──── │Đang mượn│       │ Quá hạn │ ────→ │Thất lạc │
         │Available│  T2:  │Borrowed │       │ Overdue │  T5:  │  Lost   │
         └─────────┘ Trả   └─────────┘       └────┬────┘ Lost  └─────────┘
              ▲              sách                  │
              │                                    │
              └────────────────────────────────────┘
                        T4: Trả sách trễ hạn
```

### Bước 3: Test Paths cho Edge Coverage

Suy ra test paths để **mỗi transition được thực hiện ít nhất 1 lần** (Transition Coverage = Edge Coverage, Ch.7 §7.2.1):

| Test Path | Chuỗi trạng thái | Transitions bao phủ |
|-----------|------------------|---------------------|
| TP1 | S1 → S2 → S1 | `<!-- Nhóm tự điền -->` |
| TP2 | `<!-- Nhóm tự điền -->` | |
| TP3 | | |

### Bước 4: Ánh xạ với Test Case

| Test Path | TC tương ứng | Đã được cover? |
|-----------|-------------|---------------|
| TP1 (mượn → trả) | `<!-- Nhóm tự điền -->` | |
| TP2 | | |
| TP3 | | |

### Câu hỏi thảo luận

a. **Những transition nào** chưa có TC cover? Thiết kế TC mới cho chúng.

b. Hệ thống có **BUG-07** (off-by-one ở kiểm tra quá hạn) — BUG này nằm ở transition nào? Vì sao Edge Coverage **bắt buộc** phải test transition đó?

c. Nếu thêm tính năng "Tìm lại sách" (S4 → S1), FSM thay đổi thế nào?

---

## Bài tập 5: Oracle mạnh vs Oracle yếu / The Oracle Strength Challenge

> ⏱ **Thời gian:** 15 phút | **Chương liên quan:** Ch.14 §14.1 (p.410–413)

### Bối cảnh

> *"Some software organizations only check to see whether the software produces a runtime exception, or crashes. This has been called the null oracle strategy. [...] only between 25% to 56% of software failures result in a crash."*
> — Ammann & Offutt, Ch.14 §14.1, p.412

### Kịch bản: TC-06 — Lọc sách theo thể loại "Công nghệ"

So sánh 3 cấp độ Oracle:

```python
# === Oracle A: Null Oracle — chỉ kiểm tra "không crash" ===
page.locator('flt-semantics[role="group"]').first.wait_for()
# Không có assert → PASS nếu không exception

# === Oracle B: Weak Oracle — kiểm tra "có kết quả" ===
results = page.locator('flt-semantics[role="group"]')
assert results.count() > 0, "Không có kết quả"

# === Oracle C: Strong Oracle — kiểm tra NỘI DUNG kết quả ===
results = page.locator('flt-semantics[role="group"]')
assert results.count() > 0, "Không có kết quả"
for i in range(results.count()):
    label = results.nth(i).get_attribute("aria-label")
    assert "Công nghệ" in label, f"Sách '{label}' không thuộc thể loại Công nghệ"
```

### Nhiệm vụ nhóm

1. **Phân loại:** Oracle nào phát hiện được BUG-06 (bộ lọc case-sensitive)?

   | Oracle | Loại | Phát hiện BUG-06? | Giải thích |
   |--------|------|-------------------|------------|
   | A | `<!-- Nhóm tự điền -->` | | |
   | B | | | |
   | C | | | |

2. Theo textbook, Oracle C có cần kiểm tra **tất cả** sách không? Hay chỉ cần output **liên quan trực tiếp** đến mục đích test?

3. Trong file `tests/test_search.py`, tìm assertion hiện tại cho TC-06. Nó thuộc cấp Oracle nào? Có thể cải thiện không?

---

## Bài tập 6: Ai cần chạy lại test? — Regression Test Selection

> ⏱ **Thời gian:** 15 phút | **Chương liên quan:** Ch.13 (p.406–409)

### Bối cảnh

> *"Regression testing constitutes the vast majority of testing effort... small changes to one part of a system often cause problems in distant parts of the system."*
> — Ammann & Offutt, Ch.13, p.406

### Kịch bản giả định

> **Thay đổi V1.1:** Số lượng sách mượn tối đa giảm từ **3 cuốn** xuống **2 cuốn**.

```dart
// V1.0 (cũ): static const int maxBooksPerMember = 3;
// V1.1 (mới): static const int maxBooksPerMember = 2;
```

### Nhiệm vụ nhóm

1. **Phân loại 12 Test Cases:**

   | TC | Mô tả | Sẽ FAIL? | Phải chạy lại? | Lý do |
   |-----|-------|---------|---------------|-------|
   | TC-01 | Đăng nhập thành công | `<!-- Nhóm tự điền -->` | | |
   | TC-02 | Đăng nhập sai mật khẩu | | | |
   | TC-03 | Đăng nhập bỏ trống | | | |
   | TC-04 | Tìm kiếm có kết quả | | | |
   | TC-05 | Tìm kiếm không kết quả | | | |
   | TC-06 | Lọc theo thể loại | | | |
   | TC-07 | Tìm theo tác giả | | | |
   | TC-08 | Mượn sách | | | |
   | TC-09 | Xem sách đang mượn | | | |
   | TC-10 | Trả sách | | | |
   | TC-11 | Đăng xuất | | | |
   | TC-12 | Chuyển ngôn ngữ | | | |

2. **Câu hỏi thảo luận:**

   a. TC nào **chắc chắn FAIL** do thay đổi?

   b. TC-08 (mượn bình thường) không FAIL — nhưng vì sao vẫn **phải chạy lại**?

   c. Nếu 12 TC được **tự động hóa** (chạy ~2–3 phút) vs **thủ công** (chạy ~2–3 giờ), chiến lược nào hợp lý hơn: Retest-All hay Selective?

---

## Bài tập 7: Tư duy đột biến — Kill the Mutant

> ⏱ **Thời gian:** 15 phút | **Chương liên quan:** Ch.9 §9.1.2 (p.322), §9.2.2 (p.336)

### Bối cảnh

**ROR (Relational Operator Replacement)** — thay thế toán tử quan hệ:

> *"Replace each occurrence of one of the relational operators (<, ≤, >, ≥, ==, ≠) by each of the other operators."*
> — Ammann & Offutt, Ch.9 §9.2.2, p.336

### Tình huống 1: BUG-02 — Giới hạn mượn sách

```dart
// Code đúng (theo SRS): >= 3 → từ chối
if (currentBorrowCount >= maxBooksPerMember)

// Code thực tế (mutant ROR: >= → >): > 3 → cho mượn cuốn thứ 4!
if (currentBorrowCount > maxBooksPerMember)
```

| Số sách đang mượn | Code đúng (`>=`) | Code lỗi (`>`) | Kill mutant? |
|-------------------|-----------------|----------------|-------------|
| 2 | Cho mượn | Cho mượn | Không — cùng KQ |
| 3 | `<!-- Nhóm tự điền -->` | | |
| 4 | | | |

### Tình huống 2: BUG-07 — Kiểm tra quá hạn

```dart
// Code đúng: hôm nay >= ngày hẹn → quá hạn
if (!now.isBefore(record.dueDate))

// Code thực tế (mutant): hôm nay > ngày hẹn
if (now.isAfter(record.dueDate))
```

Sách mượn 1/9, hạn trả 15/9. Ngày nào giết mutant?

| Ngày kiểm tra | Code đúng | Code lỗi | Kill? |
|--------------|----------|---------|-------|
| 14/9 | Chưa quá hạn | Chưa quá hạn | `<!-- Nhóm tự điền -->` |
| **15/9** | | | |
| 16/9 | | | |

### Câu hỏi tổng kết

a. Giá trị test giết mutant luôn nằm ở đâu? (Gợi ý: **giá trị biên** — BVA, Ch.6)

b. Tại sao *"thiết kế test data tốt bằng BVA tự động giết được hầu hết ROR mutants"*?

c. **Liên hệ RIPR:** Giá trị biên đảm bảo **Infection** (trạng thái khác nhau giữa code đúng và code lỗi). Nếu dùng giá trị xa biên (ví dụ: 0), tại sao mutant **sống sót**?

---

## Bài tập 8: Chiếc bẫy Logic (The Logic Trap)

> ⏱ **Thời gian:** 20 phút | **Chương liên quan:** Ch.8 §8.1.1 (p.248), §8.1.2 (p.250–253)

### Bối cảnh lý thuyết

Textbook nhấn mạnh: chỉ test toàn bộ biểu thức đúng/sai (**Predicate Coverage**) là chưa đủ — vì các **mệnh đề con (clauses)** bên trong có thể ẩn chứa bug mà không bao giờ bị phát hiện:

> *"An obvious failing of this criterion is that the individual clauses are not always exercised."*
> — Ammann & Offutt, Ch.8 §8.1.1, p.248

Khái niệm **determination** (quyết định) cho phép phát hiện bug ở từng clause:

> *"The key notion is that of determination, the conditions under which a clause influences the outcome of a predicate. [...] if you flip the clause, and the predicate changes value, then the clause determines the predicate."*
> — Ammann & Offutt, Ch.8 §8.1.2, p.250

Đây là cơ sở của **Active Clause Coverage (ACC)** — còn được biết là **MC/DC (Modified Condition/Decision Coverage)**, tiêu chuẩn bắt buộc trong phần mềm hàng không (FAA DO-178C):

> *"Active Clause Coverage (ACC): For each p ∈ P and each major clause ci ∈ Cp, choose minor clauses cj, j ≠ i so that ci determines p. TR has two requirements for each ci: ci evaluates to true and ci evaluates to false."*
> — Ammann & Offutt, Ch.8, Definition 8.42, p.251

### Kịch bản: REQ-04 — Mượn sách

Điều kiện để **cho phép mượn sách thành công** là biểu thức logic gồm 3 mệnh đề (clauses):

$$P = A \wedge B \wedge C$$

| Clause | Ý nghĩa | Ví dụ True | Ví dụ False |
|--------|---------|-----------|------------|
| **A** | Sách có sẵn (`book.status == available`) | BOOK001 | BOOK003 (đang mượn) |
| **B** | Chưa đạt giới hạn mượn (`borrowCount < max`) | MEM002 (0 sách) | MEM001 (đã mượn 3 sách) |
| **C** | Thành viên hoạt động (`member.status == active`) | MEM001 | MEM004 (suspended) |

### Nhiệm vụ nhóm

1. **Bước 1 — Predicate Coverage (PC):** Chỉ cần 2 test cases:

   | TC | A | B | C | $P = A \wedge B \wedge C$ | Kết quả |
   |-----|---|---|---|---|---|
   | TC-α | T | T | T | **True** | Cho mượn ✅ |
   | TC-β | F | F | F | **False** | Từ chối ❌ |

   **Câu hỏi:** Với chỉ 2 TCs này, hệ thống có bug gì mà bạn **không phát hiện được**?

2. **Bước 2 — Active Clause Coverage (ACC):** Để test từng clause, phải **cô lập** nó — giữ các clause còn lại ở giá trị cho phép clause đang test **quyết định** (determine) kết quả.

   **Nhóm hãy điền bảng truth table sau:**

   | TC | A | B | C | $P$ | Major clause được test | Giải thích |
   |----|---|---|---|-----|----------------------|-----------|
   | 1 | **T** | T | T | True | A (True → P True) | Cặp với TC2 |
   | 2 | **F** | T | T | `<!-- Nhóm tự điền -->` | A (False → P ?) | Lật A, B và C giữ nguyên T: P thay đổi? |
   | 3 | T | **T** | T | True | B (True → P True) | Cặp với TC4 |
   | 4 | T | **F** | T | | B (False → P ?) | Lật B, A và C giữ nguyên T |
   | 5 | T | T | **T** | True | C (True → P True) | Cặp với TC6 |
   | 6 | T | T | **F** | | C (False → P ?) | Lật C, A và B giữ nguyên T |

   > **Lưu ý:** Nhiều TCs có thể trùng nhau. Sau khi loại bỏ trùng lặp, ACC cần tối thiểu bao nhiêu test cases cho `A AND B AND C`?

3. **Bước 3 — Phát hiện bug BUG-04:**

   Bug thực tế trong hệ thống: BUG-04 — thành viên "Tạm ngưng" nhận thông báo lỗi sai ("Thành viên đã hết hạn" thay vì "đang bị tạm ngưng"). TC nào trong bảng ACC ở trên sẽ **phát hiện** BUG-04? TC-α và TC-β của Predicate Coverage có phát hiện được không?

### Câu hỏi thảo luận

a. Với `A AND B AND C`, Predicate Coverage cần 2 TCs, ACC cần bao nhiêu? Tại sao con số tăng lên là **xứng đáng**?

b. Trong thực tế, FAA yêu cầu **MC/DC** (tương đương ACC) cho phần mềm điều khiển máy bay. Tại sao chỉ dùng Predicate Coverage cho phần mềm hàng không là **nguy hiểm**?

c. **Kết nối BT7 (Mutation):** Nếu lập trình viên viết `OR` thay vì `AND` — đây có phải là một loại **ROR mutant** không? Giá trị test nào giết mutant này?

---

## Bài tập 9: Kẻ phá hoại bất ổn — Flaky Tests

> ⏱ **Thời gian:** 10 phút (Exit Ticket) | **Chương liên quan:** Ch.4 §4.2 (p.98–100)

### Bối cảnh lý thuyết

Theo textbook, test harness đóng vai trò "người bảo vệ" — nhưng chỉ khi nó **đáng tin cậy**:

> *"Test automation is a prerequisite for test-driven development. [...] the correctness of the system at any single point in time is subject to immediate verification simply by running the test set."*
> — Ammann & Offutt, Ch.4 §4.2, p.98

> *"Not only do our tests need to be good—they also need to be fast!"*
> — Ammann & Offutt, Ch.4 §4.2.1, p.100

Nhưng nếu test lúc **PASS**, lúc **FAIL** (không thay đổi code) — đó là **Flaky Test**. Flaky test **phá hủy** vai trò Guardian vì lập trình viên sẽ mất niềm tin: *"Lại fail nữa rồi, chắc lại do flaky thôi"* → bỏ qua cả lỗi thật.

### Kịch bản: Flutter Web CanvasKit

Hệ thống thư viện sử dụng Flutter Web với renderer **CanvasKit** (vẽ UI trên `<canvas>`). Không giống HTML DOM thông thường, Flutter cập nhật **Semantics Tree** với độ trễ không cố định.

File `conftest.py` hiện có hàm **Smart Wait**:

```python
def wait_for_flutter(page, text=None, selector=None, timeout=10000):
    """Smart Wait: chờ Flutter Semantics Tree cập nhật."""
    if text:
        page.locator(
            f'flt-semantics:has-text("{text}"), flt-semantics[aria-label*="{text}"]'
        ).first.wait_for(state="attached", timeout=timeout)
    elif selector:
        page.locator(selector).first.wait_for(state="attached", timeout=timeout)
    else:
        page.locator("flt-semantics").first.wait_for(state="attached", timeout=timeout)
```

### Nhiệm vụ nhóm (Exit Ticket)

1. **Thí nghiệm tưởng tượng:** Nếu bạn thay `wait_for_flutter(page, text="Đăng xuất")` bằng `time.sleep(0.1)` và chạy `pytest -v` 10 lần liên tiếp, điều gì sẽ xảy ra?

   | Lần chạy | `wait_for_flutter` (Smart Wait) | `time.sleep(0.1)` (Hard Sleep) |
   |----------|-------------------------------|-------------------------------|
   | 1 | ✅ PASS | `<!-- Nhóm dự đoán -->` |
   | 2 | ✅ PASS | |
   | ... | ✅ PASS | |
   | 10 | ✅ PASS | |

2. **Giải thích kỹ thuật:** Vì sao `wait_for_flutter` **ổn định** (deterministic) còn `time.sleep(0.1)` **bất ổn** (non-deterministic)?

3. **Kết nối với Ch.4:** Tác giả nói test phải *"be good AND fast"*. Nếu bạn dùng `time.sleep(5)` (chờ dài) để tránh flaky, bạn hy sinh yếu tố nào? Nếu hệ thống CI chạy 12 TCs × 5 giây sleep mỗi bước × 10 bước = bao nhiêu phút? Có còn **"immediate verification"** không?

4. **Câu hỏi trắc nghiệm (chọn 1):** Hàm `wait_for_flutter` thuộc thành phần nào trong kiến trúc test?
   - (a) Test Oracle
   - (b) Test Driver
   - (c) Test Harness infrastructure
   - (d) Test Data

---

## Phụ lục: Ánh xạ bài tập ↔ textbook

| Bài tập | Khái niệm chính | Chương |
|---|---|---|
| BT1: Box Debate | MDTD, Level of Abstraction | Ch.2 §2.4–2.5, Ch.6 |
| BT2: RIPR Detective | RIPR Model, Test Oracle, Revealability | Ch.2 §2.1, Ch.14 |
| BT3: Test as Guardian | Test Harness, De facto Specification | Ch.4 §4.2 |
| **BT4: Book Lifecycle FSM** | **FSM, State/Transition Coverage, Test Path** | **Ch.7 §7.5.2, §7.2.1** |
| **BT5: Oracle Strength** | **Null Oracle, Oracle Precision, Revealability** | **Ch.14 §14.1** |
| **BT6: Regression Selection** | **Regression Testing, Test Selection, CI** | **Ch.13, Ch.4 §4.2** |
| **BT7: Kill the Mutant** | **Mutation Testing, ROR, BVA ↔ Mutation** | **Ch.9 §9.1.2, §9.2.2, Ch.6** |
| **BT8: The Logic Trap** | **Predicate/Clause/Active Clause Coverage, MC/DC** | **Ch.8 §8.1.1, §8.1.2** |
| **BT9: Flaky Tests** | **Test Harness, Deterministic Testing, CI Speed** | **Ch.4 §4.2, §4.2.1** |
