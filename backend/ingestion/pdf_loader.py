from typing import List, Dict
import pdfplumber
from pypdf import PdfReader


def extract_text_per_page(path: str) -> List[Dict]:
    """Return list of {page_num, text} dicts.
    Uses pdfplumber for better layout; falls back to pypdf if needed.
    """
    pages = []
    try:
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append({"page": i, "text": text})
    except Exception:
        # Fallback minimal extraction
        reader = PdfReader(path)
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({"page": i, "text": text})
    return pages