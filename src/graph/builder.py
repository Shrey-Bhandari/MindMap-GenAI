import networkx as nx


def build_graph(chunks: list[dict]) -> nx.Graph:
    G = nx.Graph()

    # ---------- NODE CREATION ----------
    for c in chunks:
        node_id = f"{c['unit_id']}::{c['anchor']}"

        # ---- SLIDE ID NORMALIZATION ----
        if "slide_ids" in c:
            slide_ids = c["slide_ids"]

        elif "provenance" in c and "sources" in c["provenance"]:
            slide_ids = [s["slide_id"] for s in c["provenance"]["sources"]]

        elif "slide_id" in c:
            slide_ids = [c["slide_id"]]

        else:
            continue  # corrupt record

        G.add_node(
            node_id,
            anchor=c["anchor"],
            compressed_text=c["compressed_text"],
            attributes=c["attributes"],
            exam_signals=c["exam_signals"],
            confidence=c["confidence"],
            slide_ids=slide_ids,
            domain=c["attributes"].get("domain"),
            source_count=len(slide_ids),
        )

    # ---------- EDGE CONSTRUCTION ----------
    nodes = list(G.nodes(data=True))

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a_id, a = nodes[i]
            b_id, b = nodes[j]

            # ---- EDGE TYPE 1: CO-OCCURRENCE ----
            overlap = set(a["slide_ids"]) & set(b["slide_ids"])
            if overlap:
                weight = len(overlap) / min(len(a["slide_ids"]), len(b["slide_ids"]))
                G.add_edge(
                    a_id,
                    b_id,
                    type="co_occurrence",
                    weight=round(weight, 3),
                )
                continue  # strongest signal, don’t double-add

            # ---- EDGE TYPE 2: SEMANTIC DOMAIN ----
            if a["domain"] and a["domain"] == b["domain"]:
                G.add_edge(
                    a_id,
                    b_id,
                    type="semantic_domain",
                    weight=0.3,
                )

    return G
