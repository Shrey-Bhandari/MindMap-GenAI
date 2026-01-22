import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

class ChunkRetriever:
    def __init__(self, unit_dir):
        self.index = faiss.read_index(f"{unit_dir}/faiss.index")
        self.vectors = np.load(f"{unit_dir}/vectors.npy")
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def retrieve(self, text, k=5):
        qvec = self.model.encode([text])
        D, I = self.index.search(qvec, k)
        return I[0]
