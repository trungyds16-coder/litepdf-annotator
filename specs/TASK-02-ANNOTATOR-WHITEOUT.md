# TASK SPEC FOR GOOGLE JULES: Nâng cấp PDFAnnotator với chức năng Redaction vĩnh viễn & Chèn Watermark

## Mục tiêu
Nâng cấp `src/litepdf_annotator/annotator.py` từ vẽ đè cơ bản thành chế độ bảo mật và đóng dấu văn bản chuyên nghiệp:
1. **Chức năng Redaction thực sự (True Redaction):**
   - Hiện tại hàm `whiteout_box` chỉ vẽ đè hình chữ nhật (người dùng copy text vẫn có thể trích xuất chữ bên dưới lớp màu).
   - Hãy bổ sung phương thức `apply_permanent_redaction(input_path: str | Path, page_index: int, rect: tuple[float, float, float, float], output_path: str | Path) -> Path` sử dụng `page.add_redact_annot(rect)` và `page.apply_redactions()`. Phương thức này phải xóa triệt để text và vector bên dưới vùng bị che.
2. **Chức năng Chèn Watermark mờ chéo trang:**
   - Thêm phương thức `add_watermark(input_path: str | Path, text: str, output_path: str | Path, opacity: float = 0.3) -> Path` để chèn dòng chữ (ví dụ "BẢN NHÁP" hoặc "MẬT") nghiêng 45 độ mờ ở giữa tất cả các trang.
3. **Bổ sung Unit Tests:**
   - Viết bài test trong `tests/test_annotator.py` chứng minh rằng sau khi `apply_permanent_redaction`, lệnh `page.get_text()` không còn chứa văn bản trong vùng đó nữa.
   - Viết bài test kiểm tra hàm `add_watermark`.

## Ranh giới & Quy tắc
- Tuân thủ 100% `AGENTS.md`.
- Chạy kiểm thử:
  ```bash
  pytest -q
  ```
- Mở PR theo đúng mẫu báo cáo chuẩn trong `AGENTS.md`.
