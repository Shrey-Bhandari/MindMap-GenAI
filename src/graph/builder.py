import networkx as nx


def build_graph(chunks: list[dict]) -> nx.Graph:
    G = nx.Graph()

    for c in chunks:
        node_id = f"{c['unit_id']}::{c['anchor']}"

        # ---------- SLIDE ID NORMALIZATION ----------
        slide_ids = None

        # Case 1: Explicit slide_ids
        if "slide_ids" in c:
            slide_ids = c["slide_ids"]

        # Case 2: Merged provenance with sources
        elif "provenance" in c and "sources" in c["provenance"]:
            slide_ids = [s["slide_id"] for s in c["provenance"]["sources"]]

        # Case 3: Single-slide fallback (Phase-2 residue)
        elif "slide_id" in c:
            slide_ids = [c["slide_id"]]

        else:
            # Corrupt or unusable record — skip
            continue

        G.add_node(
            node_id,
            anchor=c["anchor"],
            compressed_text=c["compressed_text"],
            attributes=c["attributes"],
            exam_signals=c["exam_signals"],
            confidence=c["confidence"],
            slide_ids=slide_ids,
            source_count=len(slide_ids),
        )

    # ---------- EDGE CONSTRUCTION (CO-OCCURRENCE ONLY) ----------
    nodes = list(G.nodes(data=True))

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a_id, a = nodes[i]
            b_id, b = nodes[j]

            overlap = set(a["slide_ids"]) & set(b["slide_ids"])
            if not overlap:
                continue

            weight = len(overlap) / min(len(a["slide_ids"]), len(b["slide_ids"]))

            G.add_edge(
                a_id,
                b_id,
                type="co_occurrence",
                weight=round(weight, 3),
            )

    return G
