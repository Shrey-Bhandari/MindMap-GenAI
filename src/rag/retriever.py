import numpy as np
from src.embeddings.embedder import Embedder

def retrieve(query, faiss_index, top_k=5):
    embedder = Embedder()

    # Embed as batch (same model, same pipeline)
    q_vec = embedder.embed([query])   # returns (1, dim)

    q_vec = np.asarray(q_vec, dtype="float32")
    if q_vec.ndim == 1:
        q_vec = q_vec.reshape(1, -1)

    scores, idxs = faiss_index.search(q_vec, top_k)
    return idxs[0]
