import networkx as nx
import random
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math

# ---------- CONFIG ----------
filename = r"C:\Users\Ramavath kushwetha\OneDrive\Desktop\input\email.txt"
seed = 0  # For reproducible results

# ---------- Load Graph ----------
def load_graph(filename):
    G = nx.Graph()
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    u, v = map(int, parts)
                    G.add_edge(u, v, weight=1)
        print(f"✅ Loaded {len(G.nodes)} nodes and {len(G.edges)} edges.")
        return G
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        exit()

# ---------- Modularity ----------
def modularity(graph, comm):
    m2 = sum(graph[u][v]["weight"] for u, v in graph.edges()) * 2
    q = 0.0
    for c in set(comm.values()):
        nodes = [n for n, cid in comm.items() if cid == c]
        in_c = sum(graph[u][v]["weight"] for u in nodes for v in nodes if graph.has_edge(u, v))
        tot_c = sum(graph.degree(n, weight="weight") for n in nodes)
        q += (in_c / m2) - (tot_c / m2) ** 2
    return q

# ---------- Louvain Algorithm ----------
def louvain(graph, seed=0, max_iterations=500):
    random.seed(seed)
    comm = {n: i for i, n in enumerate(graph)}
    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        nodes = list(graph)
        random.shuffle(nodes)

        for n in nodes:
            current = comm[n]
            best_c, best_dq = current, 0.0
            base_q = modularity(graph, comm)
            neigh_comms = {comm[m] for m in graph[n] if comm[m] != current}

            for c in neigh_comms:
                comm[n] = c
                dq = modularity(graph, comm) - base_q
                if dq > best_dq:
                    best_c, best_dq = c, dq

            comm[n] = best_c
            if best_c != current:
                improved = True
        
        iteration += 1

    return comm

# ---------- Normalize Community IDs ----------
def normalize_communities(comm):
    cid_map = {old: new for new, old in enumerate(sorted(set(comm.values())))}
    return {node: cid_map[cid] for node, cid in comm.items()}

# ---------- Clear and Easy-to-Understand Visualization ----------
def visualize_communities(graph, communities):
    communities = normalize_communities(communities)
    community_ids = sorted(set(communities.values()))
    num_communities = len(community_ids)

    # Corrected cmap usage
    cmap = plt.colormaps.get_cmap('tab20')
    community_colors = {cid: cmap(i / max(1, num_communities - 1)) for i, cid in enumerate(community_ids)}

    # Kamada-Kawai layout (for natural separation)
    pos = nx.kamada_kawai_layout(graph)

    # Node colors based on community
    node_colors = [community_colors[communities[node]] for node in graph.nodes()]

    plt.figure(figsize=(80, 70))  # MASSIVE canvas
    nx.draw_networkx_nodes(
        graph, pos,
        node_color=node_colors,
        node_size=5000,  # Even larger nodes for better visibility
        edgecolors='black',
        linewidths=2.0,
        alpha=0.95
    )
    nx.draw_networkx_edges(
        graph, pos,
        width=1.5,
        alpha=0.4
    )
    nx.draw_networkx_labels(
        graph, pos,
        font_size=30,  # Larger font size for node labels
        font_color='black',
        font_weight='bold'
    )

    # Create a legend with larger text for community labels
    legend_patches = [
        mpatches.Patch(color=community_colors[cid], label=f"Community {i+1}")
        for i, cid in enumerate(community_ids)
    ]
    plt.legend(
        handles=legend_patches,
        title="Communities",
        loc="upper left",
        fontsize=25,  # Larger font size for the legend
        title_fontsize=28,
        frameon=True,
        fancybox=True,
        borderpad=2
    )

    plt.title("Louvain Communities Detected", fontsize=40, pad=20)
    plt.axis("off")
    plt.tight_layout(pad=5)

    # SAVE as PDF
  
    output_path = r"C:\Users\Ramavath kushwetha\OneDrive\Desktop\input\community_detection_file.pdf"
    plt.savefig(output_path, format='pdf', dpi=300)
    print(f"✅ Graph saved to {output_path}")
    plt.show()

# ---------- Main Execution ----------
if __name__ == "__main__":
    G = load_graph(filename)

    start_time = time.time()
    raw_communities = louvain(G, seed=seed, max_iterations=500)
    end_time = time.time()

    communities = normalize_communities(raw_communities)

    print(f"⏱️ Louvain execution time: {end_time - start_time:.2f} seconds.")
    print(f"🧠 Detected {len(set(communities.values()))} communities.")

    # Print communities
    for i in range(len(set(communities.values()))):
        nodes_in_community = sorted([node for node, cid in communities.items() if cid == i])
        print(f"community{i+1} - nodes: {nodes_in_community}")

    # Visualize
    visualize_communities(G, communities)
