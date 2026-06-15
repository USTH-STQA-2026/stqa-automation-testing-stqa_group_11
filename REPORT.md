# REPORT.md — Automation Test Report

**Project**: ABC Library Book-Borrowing System — https://stqa.rbc.vn
**Tools**: Python 3.12 + Playwright 1.49.1 + pytest 8.3.4 (Flutter Web / CanvasKit)
**Run date**: 2026-06-14
**Team**: Group 11 — 252ICT2012.11 — Semester 2, 2025–2026

> This report is the **Bonus B4** deliverable (results description + analysis). Every "expected
> result" is derived from the **SRS** (`docs/SRS-library-system.md`) — the single source of truth
> for deciding pass/fail (SRS, "Key principle" section). All figures below are taken directly from
> one full `pytest` run (JUnit XML), not estimated.

---

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| Total tests (executed) | **64** |
| PASS | **49** |
| FAIL | **15** |
| SKIP | 0 |
| Run time | **2202 s (~36 min 42 s)**, sequential, headless Chromium |

**How to read the 15 FAILs:** these are not 15 separate defects. Of the 15 failing tests:

- **8 tests** are **evidence for 4 genuine system bugs** (each bug confirmed by multiple tests).
- **7 tests** fail **for reasons other than a system bug**: 3 had a weak oracle (false alarm), 2 hit
  the limits of the client-side data model, 2 belong to a peripheral feature (add member) — see **§6**.

> **Update after the recorded run:** the 3 "weak-oracle" tests (TC-16, TC-17, TC-34) have been
> **fixed** to click the confirm "Mượn" (Borrow) button in the dialog (see §7.2). Re-run and verified:
> **TC-16/17/34 now PASS**, while TC-33 still FAILs but is now **valid** evidence for BUG-C (it shows
> "hết hạn" / expired for a *suspended* member). A **full** re-run would therefore yield
> **64 / 52 PASS / 12 FAIL**. The table above is kept as the recorded full run.

**All 12 mandatory test cases (TC-01 → TC-12) PASS.** The 4 confirmed system bugs (BUG-A → BUG-D)
all belong to **core business logic** and are demonstrated by `tests/test_deep_logic.py`.

---

## 2. Method & Oracle

The suite uses the **Arrange → Act → Assert** structure (ASSIGNMENT §4) and two deliberate kinds of test:

| Kind | Assertion | Meaning when it runs |
|------|-----------|----------------------|
| **Bug-finding test** (`test_bug_*`) | Asserts the **SRS-correct** behavior | **FAIL = bug evidence** (system violates the SRS). ASSIGNMENT §6.3: "A failing test still earns marks". |
| **Control test** (`test_ok_*`) | Asserts a correct behavior the system **does** get right | **PASS = oracle calibration** (proves the suite does not "fail on everything"). |

> **Key oracle lesson (see §7):** the system's borrow-rejection message only appears **after the
> confirm "Mượn" (Borrow) button is clicked in the dialog**. A test that only opens the dialog without
> confirming will **not capture** the message → false alarm. `test_deep_logic.py` always clicks the
> confirm button, so it reads the correct result.

---

## 3. Results per File

| File | Tests | PASS | FAIL |
|------|:-----:|:------:|:------:|
| `tests/test_login.py` | 4 | 4 | 0 |
| `tests/test_search.py` | 4 | 4 | 0 |
| `tests/test_borrow_return.py` | 3 | 3 | 0 |
| `tests/test_general.py` | 2 | 2 | 0 |
| `tests/test_extended.py` | 42 | 31 | 11 |
| `tests/test_deep_logic.py` | 9 | 5 | 4 |
| **Total** | **64** | **49** | **15** |

---

## 4. Mandatory Test Cases (TC-01 → TC-12)

These are the **required** part of the assignment (ASSIGNMENT §3). **All PASS.**

| TC | Test function | File | SRS | Result | Screenshot |
|----|---------------|------|-----|--------|------------|
| TC-01 | `test_login_success` | `test_login.py` | REQ-01 | PASS | `login_success.png` |
| TC-02 | `test_login_fail` (wrong password) | `test_login.py` | REQ-01 | PASS | `tc-02_login_fail.png` |
| TC-03 | `test_login_fail` (empty fields) | `test_login.py` | REQ-01 | PASS | `tc-03_login_fail.png` |
| TC-04 | `test_search_book_by_name` | `test_search.py` | REQ-03 | PASS | `tc04_search_by_name.png` |
| TC-05 | `test_search_book_no_result` | `test_search.py` | REQ-03 | PASS | `tc05_search_no_result.png` |
| TC-06 | `test_filter_by_category` | `test_search.py` | REQ-03 | PASS | `tc06_filter_category.png` |
| TC-07 | `test_search_by_author` | `test_search.py` | REQ-03 | PASS | `tc07_search_by_author.png` |
| TC-08 | `test_borrow_book` | `test_borrow_return.py` | REQ-04 | PASS | `tc08_borrow_book.png` |
| TC-09 | `test_view_borrowed_books` | `test_borrow_return.py` | REQ-08 | PASS | `tc09_view_borrowed.png` |
| TC-10 | `test_return_book` | `test_borrow_return.py` | REQ-05 | PASS | `tc10_return_book.png` |
| TC-11 | `test_logout` | `test_general.py` | — | PASS | `tc11_logout.png` |
| TC-12 | `test_switch_language_to_english` | `test_general.py` | §5 | PASS | `tc12_language_en.png` |

---

## 5. Confirmed System Bugs (4)

All 4 bugs were verified **directly on the live system** and belong to core business logic.

### BUG-A — Borrow limit off-by-one: a member can hold 4 books instead of 3
| Field | Detail |
|-------|--------|
| **SRS** | REQ-04: "Maximum **3 books** per member at a time" |
| **Accounts** | `ba.nguyen` (holds 1), `dam.tran` (holds 0), `biet.hoang` (holds 1) |
| **Steps** | Borrow repeatedly until blocked |
| **Expected** | Blocked once holding **3** books (4th book refused) |
| **Actual** | All 3 accounts manage to hold **4** books; only blocked at the **5th**. The guard uses `>= 4` instead of `>= 3`. |
| **Evidence** | `test_bug_a_borrow_limit_off_by_one` (covers 3 accounts) + `test_borrow_limit_exceeded` (TC-15) + `test_borrow_limit_ba_nguyen` (TC-41) + `test_borrow_limit_biet_hoang` (TC-48) |
| **Screenshots** | `bug_a_limit_ba.nguyen.png`, `bug_a_limit_dam.tran.png`, `bug_a_limit_biet.hoang.png`, `tc15_borrow_limit.png`, `tc41_borrow_limit_ba_nguyen.png`, `tc48_biet_hoang_limit.png` |
| **Severity** | **Critical** — directly violates a business rule, reproducible on **every** account |

### BUG-B — Borrow-record leak between members (authorization violation)
| Field | Detail |
|-------|--------|
| **SRS** | REQ-08: "A member may only view **their own** borrow records. They **must NOT view** other members' records." |
| **Account** | `dam.tran` (MEM003) using the **"Tra cứu phiếu mượn"** (look up borrow record by member ID) feature |
| **Steps** | Borrow/Return tab → "Tra cứu phiếu mượn" → enter `MEM002` / `MEM006` → "Tra cứu" (Look up) |
| **Expected** | Other members' records are not shown |
| **Actual** | The **full** records leak: BR001 of `ba.nguyen` and BR003 of `biet.hoang` (name, book, borrow date, due date) |
| **Evidence** | `test_bug_b_member_record_isolation` |
| **Screenshots** | `bug_b_isolation_dam.tran_MEM002.png`, `bug_b_isolation_dam.tran_MEM006.png` |
| **Severity** | **Critical** — personal data exposed across members |

> **Important note:** the default "Phiếu mượn của tôi" (My borrow records) view does **not** leak
> (test `TC-32` `test_member_cannot_see_other_members_records` PASSES). The hole is **only** in the
> active "look up by member ID" feature — this is why BUG-B is a real bug even though TC-32 passes.

### BUG-C — Wrong rejection reason for a "suspended" member
| Field | Detail |
|-------|--------|
| **SRS** | REQ-04: "The error message must state the **correct reason** for rejection (suspended ≠ expired)" |
| **Account** | `cu.le` (MEM004, status **Tạm ngưng** / suspended) |
| **Steps** | Log in → borrow a book → click confirm "Mượn" |
| **Expected** | A message citing the **"suspended"** reason |
| **Actual** | The system shows **"Thành viên đã hết hạn. Không thể mượn sách."** (Member has expired. Cannot borrow.) — identical to the message for an *expired* member. There is only one shared "expired" rejection branch. |
| **Evidence** | `test_bug_c_suspended_member_wrong_reason` + `test_suspended_member_error_message_specificity` (TC-33) |
| **Screenshots** | `bug_c_suspended_reason.png`, `tc33_suspended_error_msg.png` |
| **Severity** | **High** — the system **blocks correctly** (no borrow) but **reports the wrong reason**, which misleads users |

> Control: for an **expired** member (`binh.pham`), the "expired" message is actually **correct** —
> test `test_ok_expired_member_correct_reason` PASSES (`ok_expired_reason.png`). This contrast proves
> the system wrongly assigns the "expired" reason to a "suspended" member.

### BUG-D — Catalog hides "borrowed" / "lost" books
| Field | Detail |
|-------|--------|
| **SRS** | REQ-02: "Display **all** books... each book has a **status** (Available / Borrowed)" |
| **Account** | `dam.tran` (searching the catalog) |
| **Steps** | Search "Kiểm thử phần mềm" (BOOK003, Borrowed) and "Kinh tế vi mô" (BOOK007, Lost) |
| **Expected** | The books still appear, with their corresponding status |
| **Actual** | **0 results** for both — the catalog only shows "Available" books and hides non-available ones entirely |
| **Evidence** | `test_bug_d_catalog_hides_non_available_books` |
| **Screenshots** | `bug_d_hidden_BOOK003.png`, `bug_d_hidden_BOOK007.png` |
| **Severity** | **High** — violates the display requirement; users cannot tell a book exists but is borrowed/lost |

---

## 6. Reconciliation of All 15 Failures

| # | Failing test | Classification | Explanation |
|---|--------------|----------------|-------------|
| 1 | `test_bug_a_borrow_limit_off_by_one` | **BUG-A** | Borrow-limit evidence |
| 2 | `test_borrow_limit_exceeded` (TC-15) | **BUG-A** | 4th book not blocked |
| 3 | `test_borrow_limit_ba_nguyen` (TC-41) | **BUG-A** | ba.nguyen holds 4 books |
| 4 | `test_borrow_limit_biet_hoang` (TC-48) | **BUG-A** | biet.hoang holds 4 books |
| 5 | `test_bug_b_member_record_isolation` | **BUG-B** | Record leak via lookup |
| 6 | `test_bug_c_suspended_member_wrong_reason` | **BUG-C** | Wrong "suspended" reason |
| 7 | `test_suspended_member_error_message_specificity` (TC-33) | **BUG-C** | Oracle **strengthened** (now clicks confirm); now correctly shows "hết hạn" for a suspended member → valid BUG-C evidence. |
| 8 | `test_bug_d_catalog_hides_non_available_books` | **BUG-D** | Hides non-"Available" books |
| 9 | `test_borrow_suspended_member` (TC-16) | **Fixed → now PASS** | Previously only opened the dialog, so no response was captured. Now clicks confirm → the system blocks correctly (shows "không thể" / cannot) → **PASS**. |
| 10 | `test_borrow_expired_member` (TC-17) | **Fixed → now PASS** | Same as #9. The expired member **is correctly blocked** → **PASS**. |
| 11 | `test_expired_member_error_message_specificity` (TC-34) | **Fixed → now PASS** | Now captures the correct "hết hạn" reason → **PASS**. |
| 12 | `test_return_overdue_book_warning` (TC-19) | Model limitation — **not a bug** | Data is **client-side / per-session** (SRS §5.1): the librarian's "Kiểm tra quá hạn" (overdue check) does not propagate to the member's session. |
| 13 | `test_overdue_record_visible_to_member` (TC-45) | Model limitation — **not a bug** | Same as #12 — a member in a different session does not see the overdue marking. |
| 14 | `test_librarian_add_member` (TC-20) | Peripheral feature — **out of scope** | The "Add member" form rejects a valid email. Agreed to treat as a minor issue, not counted among the logic bugs. |
| 15 | `test_add_member_email_validation_data_driven[TC-20]` | Peripheral feature — **out of scope** | Same issue as #14 (the valid-email dataset). |

**Summary (recorded run):** 8 FAIL → 4 real bugs · 3 FAIL → weak oracle · 2 FAIL → client-side limitation · 2 FAIL → peripheral feature.
**After the oracle fix (§7.2):** the 3 tests TC-16/17/34 now **PASS** → a full re-run leaves **12 FAIL** (8 bug-evidence including the now-correct TC-33 + 2 client-side + 2 peripheral).

---

## 7. Technical Analysis

### 7.1. Handling Flutter Web (CanvasKit)
- The UI renders on `<canvas>` with no normal DOM → interaction goes through the **Accessibility Semantics Tree**.
- Call `enable_flutter_semantics(page)` after every DOM-changing action.
- **Book status** ("Có sẵn"/Available, "Đã mượn"/Borrowed) lives in the `aria-label` of
  `flt-semantics[role="group"]`, **not** in `all_text_contents()` — assertions must read `aria-label`.

### 7.2. Oracle lesson — and the fix applied
The borrow-rejection message only appears **after clicking the confirm "Mượn" button** in the dialog.
A test that only clicks "Mượn sách này" (opens the dialog) and reads immediately sees the book details,
**not yet** the rejection message → wrong conclusion. `test_deep_logic.py` uses the `_try_borrow_once()`
helper, which clicks through the dialog, so it reads correctly — this is the reliable oracle pattern.

**Fixed:** 4 tests in `test_extended.py` (TC-16, TC-17, TC-33, TC-34) were given the extra step of
clicking the confirm "Mượn" button after opening the dialog. Re-run and verified (2m35s):
- **TC-16, TC-17, TC-34 → PASS**: the system actually **blocks** suspended/expired members (eliminating
  the 3 "displayed result differs from expectation" false alarms).
- **TC-33 → still FAIL but now for the right reason**: for a suspended member the returned message is
  "hết hạn"/expired (`says_expired_wrongly = True`) → precise evidence for **BUG-C**.

### 7.3. "One bug = one failing test"
In `test_deep_logic.py`, each bug is **one** test (BUG-A loops 3 accounts, BUG-B loops 2 IDs, BUG-D
loops 2 books) by opening a **fresh browser context per iteration** (`_fresh_page`). This avoids the
Flutter input glitch when filling the same field a second time, while keeping seed data clean.

### 7.4. Performance & recommendation
- All 64 tests run **sequentially in ~37 min**: each test logs in fresh + waits up to 45 s for
  `flt-glass-pane` (cold start) + multiple `wait_for_timeout` calls for CanvasKit re-render.
- **Recommendation:** install `pytest-xdist` and run `pytest -n auto` to parallelize across files →
  roughly **3–4× faster**. (Not applied in this run.)

### 7.5. Test isolation
Each `page` fixture creates a **new browser context** → seed data resets after every test. The
`browser` fixture is `scope="session"` to reuse the Chromium process.

---

## 8. Verified Working (PASS)

The control/passing tests prove the system behaves **correctly** in the following areas (so the FAILs
above are real signals, not a broken suite):

- **Login**: success, wrong password, empty fields, non-existent email (REQ-01).
- **Search/Filter**: by title, by author, by category, case-insensitive, and the "Không tìm thấy sách"
  (No books found) message (REQ-03).
- **Basic borrow/return**: successful borrow, view own records, return a book (REQ-04/05/08).
- **Due date = 14 days** is correct (`test_ok_borrow_due_date_is_14_days`).
- **Real-time / single-copy**: a book leaves the "Available" catalog immediately after borrowing
  (`test_ok_realtime_book_leaves_catalog_after_borrow`).
- **Tab-level authorization**: a regular member does not see admin tabs/buttons
  (`test_ok_member_has_no_admin_capabilities`, TC-40).
- **Correct "expired" reason** for an expired member (`test_ok_expired_member_correct_reason`).
- **Returning a book frees one slot** (`test_ok_returning_book_frees_a_slot`).
- **Librarian**: sees all borrow records (TC-26), "Kiểm tra quá hạn" (overdue check) works on the
  librarian side (TC-46), and data restore works (TC-47).

---

## 9. Bonus B2 — Data-Driven Testing

Uses `@pytest.mark.parametrize` (textbook Ch.3 §3.3.2) in two groups:

**Group 1 — Login failure** (`test_login.py::test_login_fail`), 3 datasets:

| Email | Password | tc_id | Result |
|-------|----------|-------|--------|
| `dam.tran@email.com` | `wrongpassword` | TC-02 | PASS |
| *(empty)* | *(empty)* | TC-03 | PASS |
| `nobody@test.com` | `anything` | TC-02b | PASS |

**Group 2 — Add-member email validation** (`test_extended.py::test_add_member_email_validation_data_driven`), 5 datasets:

| Email | tc_id | Expected | Result |
|-------|-------|----------|--------|
| `testmember2024@email.com` | TC-20 | Add succeeds | FAIL — system rejects a valid email (see §6 #15) |
| `ba.nguyen@email.com` | TC-21 | Reject (duplicate) | PASS |
| `invalidemail` | TC-27a | Reject (no @) | PASS |
| `user@domain` | TC-27b | Reject (no dot in domain) | PASS |
| *(empty)* | TC-27c | Reject | PASS |

> The TC-20 dataset FAIL correctly reflects the peripheral-feature issue in §6 (#14–15); it is not a test defect.

---

## 10. AI Usage Declaration

The extended tests, the deep-logic tests (`test_deep_logic.py`), and this report were assisted by
**Claude Code (Anthropic)**:
- Analyzed the SRS, compared it against actual behavior, and proposed test cases covering REQ-01 → REQ-08.
- Generated locators/assertions suited to Flutter Web CanvasKit (Semantics Tree, `aria-label`).
- Designed a reliable oracle (clicking through the confirm dialog) and the "one bug = one test" structure.
- Reconciled all 15 failing tests against the SRS to **remove false alarms** and keep only the 4 real logic bugs.
- The team re-ran the suite, reviewed the screenshot evidence, and verified the results before submission.
