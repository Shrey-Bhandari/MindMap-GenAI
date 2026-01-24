from src.storage.jsonl_reader import read_jsonl
from src.rag.prompt import RAG_PROMPT
from src.rag.retriever import retrieve
from src.rag.context_assembler import assemble_context
  # ← your actual client
from src.llm.runner import LLMRunner
from src.llm.local_runtime import LocalLLM

import faiss
import pickle


# ---- LOAD ARTIFACTS ----
def load_faiss_index():
    return faiss.read_index("data/embeddings/UNIT_3/faiss.index")


def load_embeddings():
    with open("data/embeddings/UNIT_3/embeddings.pkl", "rb") as f:
        return pickle.load(f)


def load_chunks():
    return list(read_jsonl("data/processed/units_UNIT_3.jsonl"))


def load_graph():
    with open("data/graphs/UNIT_3_graph.gpickle", "rb") as f:
        return pickle.load(f)


# ---- MAIN ----
def main():
    faiss_index = load_faiss_index()
    embeddings = load_embeddings()
    chunks = load_chunks()
    graph = load_graph()

    llm = LLMRunner(LocalLLM())
    query = input("Query: ")

    idxs = retrieve(query, faiss_index)
    context_chunks = assemble_context(chunks, graph, idxs)

    # 🔑 RAG PROMPT AS STRING (THIS WAS THE BUG)
    prompt = RAG_PROMPT.format(
        query=query,
        context="\n".join(
            f"- {c['anchor']}: {c['compressed_text']}"
            for c in context_chunks
        )
    )

    result = llm.generate(prompt)
    print(result)


if __name__ == "__main__":
    main()
