from pathlib import Path

from src.document_loader import load_pdf
from src.chunker import chunk_pages


DOCUMENT_DIR = Path("data/documents")


pdf_files = list(DOCUMENT_DIR.glob("*.pdf"))


if not pdf_files:
    print("No PDF files found.")
    exit()


all_chunks = []


for pdf_file in pdf_files:

    pages = load_pdf(pdf_file)

    chunks = chunk_pages(pages)

    all_chunks.extend(chunks)


print("=" * 60)
print("DOCUMENT PROCESSING")
print("=" * 60)

print("PDF files:", len(pdf_files))
print("Total chunks:", len(all_chunks))


for i, chunk in enumerate(all_chunks[:5]):

    print("\n" + "=" * 60)
    print("CHUNK:", i + 1)
    print("Source:", chunk["source"])
    print("Page:", chunk["page"])
    print("=" * 60)

    print(chunk["text"][:500])