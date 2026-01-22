import json
from pathlib import Path
import numpy as np
import faiss

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
    out_dir = Path("data/embeddings/UNIT_3")
    out_dir.mkdir(parents=True, exist_ok=True)

    texts = []
    meta = []

    with units_path.open("r", encoding="utf-8") as f:
        for line in f:
            chunk = json.loads(line)
            texts.append(canonical_text(chunk))
            meta.append({
                "anchor": chunk["anchor"],
                "ppt": chunk["ppt"],
                "slide_id": chunk["slide_id"]
            })

    embedder = Embedder()
    vectors = embedder.embed(texts)

    np.save(out_dir / "vectors.npy", vectors)

    index = build_faiss_index(vectors)
    faiss.write_index(index, str(out_dir / "faiss.index"))

    with (out_dir / "meta.jsonl").open("w", encoding="utf-8") as f:
        for m in meta:
            f.write(json.dumps(m) + "\n")

    print("✅ Phase-3 embeddings & FAISS index created.")


if __name__ == "__main__":
    main()
