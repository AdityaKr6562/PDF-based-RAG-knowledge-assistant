from src.embeddings import create_embeddings
from src.vector_store import VectorStore


# --------------------------------------------------
# Load existing FAISS database
# --------------------------------------------------

store = VectorStore.load("vectorstore")


# --------------------------------------------------
# Ask a question
# --------------------------------------------------

question = input("\nAsk a question about the document: ")


# --------------------------------------------------
# Convert question into an embedding
# --------------------------------------------------

query_embedding = create_embeddings(
    [question]
)[0]


# --------------------------------------------------
# Search FAISS
# --------------------------------------------------

results = store.search(
    query_embedding,
    k=5
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\n========================================")
print("RETRIEVED DOCUMENT CHUNKS")
print("========================================")


for i, result in enumerate(results):

    print(f"\n--- RESULT {i + 1} ---")

    print("Source:", result["source"])

    print("Page:", result["page"])

    print("Distance:", result["distance"])

    print("\nText:")

    print(result["text"][:1000])