from pathlib import Path

import fitz


def first_page_to_png(pdf_path: Path, output_path: Path) -> Path:
    doc = fitz.open(pdf_path)
    if doc.page_count == 0:
        raise ValueError("PDF has no pages.")
    page = doc.load_page(0)
    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    pixmap.save(output_path)
    doc.close()
    return output_path
