import os
import pickle
from src.storage.jsonl_reader import read_jsonl
from src.graph.builder import build_graph
from src.graph.validator import validate_graph

def main():
    chunks = list(read_jsonl("data/processed/units_UNIT_3.jsonl"))
    G = build_graph(chunks)
    validate_graph(G)

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    os.makedirs("data/graphs", exist_ok=True)
    with open("data/graphs/UNIT_3_graph.gpickle", "wb") as f:
        pickle.dump(G, f)

    print("✅ Phase-5 graph persisted.")

if __name__ == "__main__":
    main()
