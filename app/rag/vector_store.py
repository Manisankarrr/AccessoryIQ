import faiss
import os
import pickle
from app.rag.embeddings import embed_texts
from config.settings import settings


class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []

    def build(self, texts, metadata):
        vectors = embed_texts(texts)
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)
        self.metadata = metadata

    def save(self):
        os.makedirs(settings.VECTOR_STORE_PATH, exist_ok=True)
        faiss.write_index(
            self.index,
            os.path.join(settings.VECTOR_STORE_PATH, "index.faiss")
        )
        with open(
            os.path.join(settings.VECTOR_STORE_PATH, "meta.pkl"),
            "wb"
        ) as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(
            os.path.join(settings.VECTOR_STORE_PATH, "index.faiss")
        )
        with open(
            os.path.join(settings.VECTOR_STORE_PATH, "meta.pkl"),
            "rb"
        ) as f:
            self.metadata = pickle.load(f)

    def search(self, query, category, brand, k=5):
        vector = embed_texts([query])
        distances, indices = self.index.search(vector, k * 3)

        results = []
        for idx in indices[0]:
            meta = self.metadata[idx]
            if meta["category"] == category and meta["brand"] == brand:
                results.append(meta)
            if len(results) >= k:
                break

        return results
