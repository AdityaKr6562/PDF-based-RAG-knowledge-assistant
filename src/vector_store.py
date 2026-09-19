import faiss
import numpy as np
import pickle
from pathlib import Path


class VectorStore:

    def __init__(self, dimension):

        self.index = faiss.IndexFlatL2(dimension)

        self.documents = []


    def add(self, embeddings, documents):

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)

        self.documents.extend(documents)


    def search(self, query_embedding, k=5):

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index == -1:
                continue

            result = self.documents[index].copy()

            result["distance"] = float(distance)

            results.append(result)

        return results


    def save(self, path):

        path = Path(path)

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(path / "index.faiss")
        )

        with open(
            path / "documents.pkl",
            "wb"
        ) as file:

            pickle.dump(
                self.documents,
                file
            )


    @classmethod
    def load(cls, path):

        path = Path(path)

        index = faiss.read_index(
            str(path / "index.faiss")
        )

        with open(
            path / "documents.pkl",
            "rb"
        ) as file:

            documents = pickle.load(file)


        store = cls(index.d)

        store.index = index

        store.documents = documents

        return store