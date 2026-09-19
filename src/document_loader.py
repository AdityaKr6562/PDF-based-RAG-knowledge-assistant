import fitz
from pathlib import Path


def load_pdf(pdf_path):
    """
    Extract text from every page of a PDF.

    Returns a list of dictionaries containing:
    - text
    - source filename
    - page number
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        if text.strip():

            pages.append({
                "text": text.strip(),
                "source": Path(pdf_path).name,
                "page": page_number + 1
            })

    document.close()

    return pages