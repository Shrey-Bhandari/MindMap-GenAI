from src.storage.jsonl_reader import read_jsonl
from src.graph.builder import build_graph
from src.graph.validator import validate_graph


def main():
    chunks = list(read_jsonl("data/processed/units_UNIT_3.jsonl"))
    G = build_graph(chunks)
    validate_graph(G)

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

if __name__ == "__main__":
    main()
