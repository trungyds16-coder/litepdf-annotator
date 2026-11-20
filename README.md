# LitePDF Annotator — Động cơ Chú thích & Chỉnh sửa PDF cơ bản (Headless)

Module chuyên trách các thao tác ghi chú, highlight và chỉnh sửa cơ bản (Basic Edit):
- **Highlight văn bản:** Tự động dò tìm chuỗi ký tự và áp dụng màu highlight chuẩn.
- **Whiteout / Che nội dung cũ:** Vẽ khối che phủ (opaque box) trùng màu nền để che lỗi sai hoặc thông tin nhạy cảm.
- **Thêm văn bản mới (Text Overlay):** Chèn đoạn văn, số liệu mới đè lên vị trí cần sửa, hỗ trợ tiếng Việt UTF-8.
- **Chèn con dấu / Chữ ký (Stamp / Signature):** Đặt ảnh PNG (hỗ trợ nền trong suốt) vào tọa độ chỉ định.

## Cài đặt & Chạy kiểm thử
```bash
pip install -r requirements.txt
pytest -v
```
