"""Test fixtures cho LitePDF Annotator."""

from pathlib import Path
import pytest

try:
    import pymupdf as fitz
except ImportError:
    import fitz

from PIL import Image


@pytest.fixture
def sample_pdf_with_text(tmp_path: Path) -> Path:
    """Tạo file PDF mẫu có sẵn văn bản để test highlight và whiteout."""
    pdf_path = tmp_path / "text_sample.pdf"
    doc = fitz.open()
    page = doc.new_page(width=400, height=500)
    page.insert_text((50, 100), "Hop dong kinh te so 123", fontsize=16)
    page.insert_text((50, 140), "Gia tri hop dong: 100000000 VND", fontsize=14)
    doc.save(pdf_path)
    doc.close()
    return pdf_path


@pytest.fixture
def sample_stamp_image(tmp_path: Path) -> Path:
    """Tạo một file ảnh PNG nhỏ trong suốt giả lập con dấu."""
    img_path = tmp_path / "stamp.png"
    img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
    img.save(img_path)
    return img_path
