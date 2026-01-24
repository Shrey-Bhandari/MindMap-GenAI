def assemble_context(chunks, graph, idxs):
    anchors = set()
    context = []

    for i in idxs:
        c = chunks[i]
        if c["anchor"] in anchors:
            continue
        anchors.add(c["anchor"])
        context.append(c)

        node_id = f"{c['unit_id']}::{c['anchor']}"
        if graph.has_node(node_id):
            for nbr in graph.neighbors(node_id):
                anchor = nbr.split("::")[1]
                for x in chunks:
                    if x["anchor"] == anchor and anchor not in anchors:
                        anchors.add(anchor)
                        context.append(x)

    return context
