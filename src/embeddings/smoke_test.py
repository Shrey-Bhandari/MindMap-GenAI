import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

index = faiss.read_index("data/embeddings/UNIT_3/faiss.index")
vectors = np.load("data/embeddings/UNIT_3/vectors.npy")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

query = "Fermat little theorem definition"
qvec = model.encode([query])

D, I = index.search(qvec, k=5)
print("Nearest indices:", I[0])
