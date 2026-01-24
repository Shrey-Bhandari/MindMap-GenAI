def project_nodes(G):
    nodes = []
    for node_id, data in G.nodes(data=True):
        importance = data["confidence"] * (1 + data["source_count"])
        nodes.append({
            "id": node_id,
            "label": f"{data['anchor']}\n{data['compressed_text']}",
            "importance": importance
        })
    return nodes


def project_edges(G):
    edges = []
    for u, v, data in G.edges(data=True):
        if data["weight"] >= 0.4:
            edges.append({
                "source": u,
                "target": v,
                "weight": data["weight"]
            })
    return edges
