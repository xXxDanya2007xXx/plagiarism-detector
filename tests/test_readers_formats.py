from pathlib import Path

from plagiarism_detector.readers import read_document


def test_read_docx(tmp_path: Path):
    # python-docx is in requirements
    import docx  # type: ignore

    p = tmp_path / "sample.docx"
    d = docx.Document()
    d.add_paragraph("Hello DOCX world")
    d.save(p)

    doc = read_document(p)
    assert "hello" in doc.text.lower()


def test_read_pdf_no_crash(tmp_path: Path):
    # pypdf is in requirements
    from pypdf import PdfWriter  # type: ignore

    p = tmp_path / "sample.pdf"
    w = PdfWriter()
    w.add_blank_page(width=72, height=72)
    with p.open("wb") as f:
        w.write(f)

    doc = read_document(p)
    assert isinstance(doc.text, str)
