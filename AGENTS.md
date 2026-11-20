# AGENTS.md — Quy tắc phát triển & Kiến trúc dự án LitePDF Annotator

## 1. Tổng quan & Ranh giới Kiến trúc (Architecture & Boundaries)
- **Ngôn ngữ & Phiên bản:** Python 3.11+
- **Thư viện chính:** PyMuPDF (fitz)
- **Cấu trúc thư mục chuẩn:**
  - `src/litepdf_annotator/`: Logic nghiệp vụ chú thích & chỉnh sửa cơ bản (Whiteout, Text Box, Highlight, Stamp). 100% headless.
  - `tests/`: Toàn bộ unit test và integration test.
- **Nguyên tắc cốt lõi:** Lớp này thực thi các thao tác ghi đè vector và annotation lên PDF. Đảm bảo hỗ trợ bảng mã tiếng Việt UTF-8 không bị lỗi font khi chèn văn bản.

---

## 2. Quy tắc phạm vi & Chống "loãng" (Anti-Drift Rules)
- **Chỉ sửa đúng phạm vi yêu cầu:** KHÔNG tự ý refactor các module không liên quan.
- **Bảo vệ giao diện lập trình nội bộ (Internal API):** Các hàm trong `src/litepdf_annotator/` phải giữ nguyên signature, nếu thay đổi phải cập nhật toàn bộ test.
- **Giới hạn kích thước tệp:** Tránh tệp quá 500 dòng.

---

## 3. Quản lý Môi trường & Thư viện (Dependencies & Cloud VM)
- **Khai báo phụ thuộc đồng bộ:** Ghi rõ thư viện vào `requirements.txt`.
- **Không đưa rác vào Git:** Không commit `venv/`, `__pycache__/`, `.pytest_cache/`, file PDF tạm.
- **Tương thích đa môi trường:** Sử dụng `pathlib.Path`, không dùng đường dẫn Windows tuyệt đối.

---

## 4. Tiêu chuẩn viết code Python
- **Type Hints & Docstrings:** Bắt buộc type hints cho tọa độ hình chữ nhật `tuple[float, float, float, float]`, màu sắc `tuple[float, float, float]`, v.v.
- **Hỗ trợ Unicode:** Chèn chữ có dấu tiếng Việt phải hoạt động trơn tru.

---

## 5. Quy trình Kiểm thử bắt buộc
- **Kiểm thử Headless:** Không dùng GUI.
- **Lệnh kiểm thử:**
  ```bash
  pytest -q
  ```

---

## 6. Chuẩn hóa Báo cáo Pull Request (PR Template)
Mô tả PR bắt buộc theo mẫu:
- **Mục tiêu nhiệm vụ:**
- **Tệp đã chỉnh sửa & tạo mới:**
- **Bằng chứng kiểm thử:**
- **Phụ thuộc mới (nếu có):**

---

## 7. Giới hạn tự sửa lỗi (Circuit Breaker)
Dừng lại và báo cáo nếu test fail quá 3 lần cho cùng 1 lỗi.
