"""Unit tests cho PDFAnnotator."""

from pathlib import Path
import pytest

try:
    import pymupdf as fitz
except ImportError:
    import fitz

from litepdf_annotator.annotator import PDFAnnotator


def test_highlight_text(sample_pdf_with_text: Path, tmp_path: Path):
    out_pdf = tmp_path / "highlighted.pdf"
    count = PDFAnnotator.highlight_text(
        input_path=sample_pdf_with_text,
        page_index=0,
        search_text="hop dong",
        output_path=out_pdf,
        color=(1.0, 1.0, 0.0)
    )
    assert count >= 1
    assert out_pdf.is_file()

    with fitz.open(out_pdf) as doc:
        page = doc[0]
        annots = list(page.annots())
        assert len(annots) >= 1
        assert annots[0].type[0] == 8  # Highlight annot type in PDF spec


def test_whiteout_box(sample_pdf_with_text: Path, tmp_path: Path):
    out_pdf = tmp_path / "whiteout.pdf"
    PDFAnnotator.whiteout_box(
        input_path=sample_pdf_with_text,
        page_index=0,
        rect=(45.0, 120.0, 300.0, 160.0),
        output_path=out_pdf
    )
    assert out_pdf.is_file()


def test_add_text_box(sample_pdf_with_text: Path, tmp_path: Path):
    out_pdf = tmp_path / "added_text.pdf"
    PDFAnnotator.add_text_box(
        input_path=sample_pdf_with_text,
        page_index=0,
        pos=(50.0, 200.0),
        text="Đã phê duyệt và nghiệm thu thành công!",
        output_path=out_pdf,
        font_size=12.0
    )
    assert out_pdf.is_file()

    with fitz.open(out_pdf) as doc:
        page = doc[0]
        text = page.get_text()
        # Chuẩn hóa khoảng trắng không ngắt (non-breaking space \xa0) nếu có
        clean_text = text.replace("\xa0", " ")
        assert "phê duyệt" in clean_text or "nghiệm thu" in clean_text


def test_insert_stamp_image(sample_pdf_with_text: Path, sample_stamp_image: Path, tmp_path: Path):
    out_pdf = tmp_path / "stamped.pdf"
    PDFAnnotator.insert_stamp_image(
        input_path=sample_pdf_with_text,
        page_index=0,
        image_path=sample_stamp_image,
        rect=(200.0, 300.0, 300.0, 400.0),
        output_path=out_pdf
    )
    assert out_pdf.is_file()

    with fitz.open(out_pdf) as doc:
        page = doc[0]
        img_list = page.get_images()
        assert len(img_list) >= 1
