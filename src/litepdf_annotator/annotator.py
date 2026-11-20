"""Module xử lý Annotation, Highlight, Whiteout và chèn Chữ ký/Text cho PDF."""

from pathlib import Path
from typing import Optional, Tuple, Union

try:
    import pymupdf as fitz
except ImportError:
    import fitz


def _resolve_unicode_font() -> Tuple[str, Optional[str]]:
    """Tìm font TTF hỗ trợ đầy đủ ký tự Unicode (tiếng Việt) trên hệ thống."""
    font_candidates = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
        Path("/usr/share/fonts/dejavu/DejaVuSans.ttf"),
    ]
    for p in font_candidates:
        if p.is_file():
            return ("unicode_font", str(p))
    return ("helv", None)


class PDFAnnotator:
    """Xử lý chú thích, highlight, che nội dung cũ và chèn text/ảnh vào PDF (0-indexed)."""

    @staticmethod
    def highlight_text(
        input_path: Union[str, Path],
        page_index: int,
        search_text: str,
        output_path: Union[str, Path],
        color: Tuple[float, float, float] = (1.0, 1.0, 0.0)  # Vàng
    ) -> int:
        """
        Tìm kiếm tất cả các vị trí xuất hiện của search_text trên page_index và tô màu highlight.
        Trả về số lượng điểm đã được highlight.
        """
        in_p = Path(input_path)
        out_p = Path(output_path)
        if not in_p.is_file():
            raise FileNotFoundError(f"Tệp không tồn tại: {in_p}")

        highlight_count = 0
        with fitz.open(in_p) as doc:
            if not 0 <= page_index < len(doc):
                raise IndexError(f"Chỉ số trang ngoài phạm vi: {page_index}")
            
            page = doc[page_index]
            text_instances = page.search_for(search_text)
            for inst in text_instances:
                annot = page.add_highlight_annot(inst)
                annot.set_colors(stroke=color)
                annot.update()
                highlight_count += 1

            out_p.parent.mkdir(parents=True, exist_ok=True)
            doc.save(out_p)

        return highlight_count

    @staticmethod
    def whiteout_box(
        input_path: Union[str, Path],
        page_index: int,
        rect: Tuple[float, float, float, float],
        output_path: Union[str, Path],
        fill_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)  # Trắng
    ) -> Path:
        """
        Vẽ hộp che phủ đục (opaque rectangle) để che nội dung/lỗi cũ.
        rect = (x0, y0, x1, y1)
        """
        in_p = Path(input_path)
        out_p = Path(output_path)
        if not in_p.is_file():
            raise FileNotFoundError(f"Tệp không tồn tại: {in_p}")

        with fitz.open(in_p) as doc:
            if not 0 <= page_index < len(doc):
                raise IndexError(f"Chỉ số trang ngoài phạm vi: {page_index}")

            page = doc[page_index]
            r = fitz.Rect(rect)
            page.draw_rect(r, color=fill_color, fill=fill_color, overlay=True)

            out_p.parent.mkdir(parents=True, exist_ok=True)
            doc.save(out_p)

        return out_p

    @staticmethod
    def add_text_box(
        input_path: Union[str, Path],
        page_index: int,
        pos: Tuple[float, float],
        text: str,
        output_path: Union[str, Path],
        font_size: float = 12.0,
        color: Tuple[float, float, float] = (0.0, 0.0, 0.0),  # Đen
        font_file: Optional[Union[str, Path]] = None
    ) -> Path:
        """
        Chèn văn bản tại tọa độ pos = (x, y). Hỗ trợ ký tự tiếng Việt UTF-8.
        """
        in_p = Path(input_path)
        out_p = Path(output_path)
        if not in_p.is_file():
            raise FileNotFoundError(f"Tệp không tồn tại: {in_p}")

        if font_file is not None:
            font_name, font_path = "custom_font", str(font_file)
        else:
            font_name, font_path = _resolve_unicode_font()

        with fitz.open(in_p) as doc:
            if not 0 <= page_index < len(doc):
                raise IndexError(f"Chỉ số trang ngoài phạm vi: {page_index}")

            page = doc[page_index]
            point = fitz.Point(pos)
            kwargs = {
                "point": point,
                "text": text,
                "fontsize": font_size,
                "color": color,
                "overlay": True,
            }
            if font_path:
                kwargs["fontfile"] = font_path
                kwargs["fontname"] = font_name
            else:
                kwargs["fontname"] = font_name

            page.insert_text(**kwargs)

            out_p.parent.mkdir(parents=True, exist_ok=True)
            doc.save(out_p)

        return out_p

    @staticmethod
    def insert_stamp_image(
        input_path: Union[str, Path],
        page_index: int,
        image_path: Union[str, Path],
        rect: Tuple[float, float, float, float],
        output_path: Union[str, Path]
    ) -> Path:
        """
        Chèn hình ảnh con dấu / chữ ký (PNG trong suốt) vào vùng rect = (x0, y0, x1, y1).
        """
        in_p = Path(input_path)
        img_p = Path(image_path)
        out_p = Path(output_path)

        if not in_p.is_file():
            raise FileNotFoundError(f"Tệp PDF không tồn tại: {in_p}")
        if not img_p.is_file():
            raise FileNotFoundError(f"Tệp ảnh không tồn tại: {img_p}")

        with fitz.open(in_p) as doc:
            if not 0 <= page_index < len(doc):
                raise IndexError(f"Chỉ số trang ngoài phạm vi: {page_index}")

            page = doc[page_index]
            r = fitz.Rect(rect)
            page.insert_image(r, filename=str(img_p), overlay=True)

            out_p.parent.mkdir(parents=True, exist_ok=True)
            doc.save(out_p)

        return out_p
