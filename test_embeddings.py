from src.embeddings import create_embeddings


texts = [
    "Artificial intelligence is a field of computer science.",
    "Machine learning allows computers to learn from data."
]


embeddings = create_embeddings(texts)


print("Embedding shape:")
print(embeddings.shape)

print("\nFirst embedding:")
print(embeddings[0][:10])