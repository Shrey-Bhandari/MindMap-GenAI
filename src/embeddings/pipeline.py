import json
from pathlib import Path
import numpy as np
import faiss
import pickle

from src.embeddings.embedder import Embedder
from src.embeddings.index_builder import build_faiss_index


def canonical_text(chunk):
    return "\n".join([
        chunk["anchor"],
        chunk["compressed_text"],
        chunk["attributes"]["type"],
        chunk["attributes"]["domain"]
    ])


def main():
    units_path = Path("data/processed/units_UNIT_3.jsonl")
    out_dir = Path("data/embeddings")
    out_dir.mkdir(parents=True, exist_ok=True)

    texts = []
    meta = []

    with units_path.open("r", encoding="utf-8") as f:
        for line in f:
            chunk = json.loads(line)

            texts.append(canonical_text(chunk))

            # provenance-safe metadata
            meta.append({
                "anchor": chunk["anchor"],
                "unit_id": chunk["unit_id"],
                "source_count": len(
                    chunk.get("provenance", {}).get("sources", [])
                )
            })

    embedder = Embedder()
    vectors = embedder.embed(texts)

    # save vectors
    np.save(out_dir / "vectors.npy", vectors)

    # build + save FAISS
    index = build_faiss_index(vectors)
    faiss.write_index(index, "data/embeddings/UNIT_3.index")

    # save metadata
    with (out_dir / "meta.jsonl").open("w", encoding="utf-8") as f:
        for m in meta:
            f.write(json.dumps(m) + "\n")

    # ✅ SAVE EMBEDDINGS FOR RAG
    with open("data/embeddings/UNIT_3_embeddings.pkl", "wb") as f:
        pickle.dump(vectors, f)

    print("✅ Phase-3 embeddings & FAISS index created.")



if __name__ == "__main__":
    main()
