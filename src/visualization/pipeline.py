from pathlib import Path
import pickle
from src.visualization.renderer import render_graph

def main():
    with open("data/graphs/UNIT_3_graph.gpickle", "rb") as f:
        G = pickle.load(f)

    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)

    render_graph(G, out_dir / "UNIT_3_revision_map.png")
    print("✅ Phase-7 visualization created.")

if __name__ == "__main__":
    main()
