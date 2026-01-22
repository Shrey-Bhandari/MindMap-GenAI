def validate_graph(G):
    assert G.number_of_nodes() > 0
    for _, data in G.nodes(data=True):
        assert "anchor" in data
        assert "confidence" in data
