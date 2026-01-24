import matplotlib.pyplot as plt
import networkx as nx
import textwrap
import random


def wrap(text, width=40):
    return "\n".join(textwrap.wrap(text, width))


def render_graph(G, out_path):

    # ---------- PREP LABELS ----------
    for n, data in G.nodes(data=True):
        title = data["anchor"].replace("_", " ").title()
        desc = wrap(data["compressed_text"], 42)
        data["label"] = f"{title}\n{desc}"

    # ---------- DOMAIN ANCHORS ----------
    DOMAIN_CENTERS = {
        "number_theory": (2, 2),
        "cryptography": (2, -2),
        "general": (-2, 0),
    }

    # ---------- INITIAL POSITIONS ----------
    pos_init = {}
    for n, data in G.nodes(data=True):
        domain = data["attributes"].get("domain", "general")
        cx, cy = DOMAIN_CENTERS.get(domain, (0, 0))
        pos_init[n] = (
            cx + random.uniform(-0.6, 0.6),
            cy + random.uniform(-0.6, 0.6),
        )

    # ---------- FINAL POSITIONS (THIS WAS MISSING) ----------
    pos = nx.spring_layout(
        G,
        pos=pos_init,
        fixed=pos_init.keys(),
        iterations=200,
        weight="weight",
        seed=42,
    )

    # ---------- CANVAS ----------
    plt.figure(figsize=(22, 14))

    # ---------- EDGES FIRST ----------
    for u, v, d in G.edges(data=True):
        style = "solid" if d.get("type") == "co_occurrence" else "dashed"
        alpha = 0.55 if d.get("type") == "co_occurrence" else 0.35
        width = 2.0 + 2.5 * d.get("weight", 0.5)

        plt.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            linestyle=style,
            linewidth=width,
            color="#444444",
            alpha=alpha,
            zorder=1,
        )

    # ---------- LABEL BOXES (THE NODES) ----------
    for n, (x, y) in pos.items():
        plt.text(
            x,
            y,
            G.nodes[n]["label"],
            fontsize=11,
            ha="center",
            va="center",
            zorder=3,
            bbox=dict(
                boxstyle="round,pad=0.45",
                fc="white",
                ec="#2F5DA8",
                linewidth=1.4,
                alpha=0.98,
            ),
        )

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
