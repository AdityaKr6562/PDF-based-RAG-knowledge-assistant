from pathlib import Path

from src.document_loader import load_pdf
from src.chunker import chunk_pages
from src.embeddings import create_embeddings
from src.vector_store import VectorStore


DOCUMENT_DIR = Path("data/documents")
VECTORSTORE_DIR = "vectorstore"


# --------------------------------------------------
# 1. Find all PDFs
# --------------------------------------------------

pdf_files = list(DOCUMENT_DIR.glob("*.pdf"))

if not pdf_files:
    print("No PDF files found.")
    print("Put PDF files inside data/documents/")
    exit()


# --------------------------------------------------
# 2. Extract and chunk all documents
# --------------------------------------------------

all_chunks = []


for pdf_file in pdf_files:

    print(f"\nProcessing: {pdf_file.name}")

    pages = load_pdf(pdf_file)

    print(f"  Pages: {len(pages)}")

    chunks = chunk_pages(pages)

    print(f"  Chunks: {len(chunks)}")

    all_chunks.extend(chunks)


print("\n========================================")
print("TOTAL CHUNKS:", len(all_chunks))
print("========================================")


# --------------------------------------------------
# 3. Extract text from chunks
# --------------------------------------------------

texts = [
    chunk["text"]
    for chunk in all_chunks
]


# --------------------------------------------------
# 4. Generate embeddings
# --------------------------------------------------

print("\nGenerating embeddings...")

embeddings = create_embeddings(texts)


print("Embedding shape:", embeddings.shape)


# --------------------------------------------------
# 5. Create FAISS vector store
# --------------------------------------------------

dimension = embeddings.shape[1]

store = VectorStore(dimension)


# --------------------------------------------------
# 6. Add embeddings + document metadata
# --------------------------------------------------

store.add(
    embeddings,
    all_chunks
)


# --------------------------------------------------
# 7. Save FAISS database
# --------------------------------------------------

store.save(VECTORSTORE_DIR)


print("\n========================================")
print("FAISS KNOWLEDGE BASE CREATED")
print("========================================")

print(f"Vectors stored: {len(all_chunks)}")
print(f"Vector dimension: {dimension}")
print(f"Location: {VECTORSTORE_DIR}/")