import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt


nparcours, netudiants = 9, 11  # rows = parcours, column = etudiants

# k = 3
parcours = {0: [5, 7],
            1: [],
            2: [9],
            3: [],
            4: [10],
            5: [0, 1, 3],
            6: [0, 1, 3],
            7: [6, 7],
            8: []}


etudiants = [f"Etu{i}" for i in range(0, netudiants, 1)]
edges = [(key, f"Etu{etud}") for key, etuds in parcours.items() for etud in etuds]
color_map = []
G = nx.Graph()

G.add_nodes_from(parcours.keys(), bipartite=0)
G.add_nodes_from(etudiants, bipartite=1)
for node in G:
    if isinstance(node, str) and "Etu" in node:
        color_map.append("#FBCEB1")
    else:
        color_map.append("#A6C7F9")


G.add_edges_from(edges)

bipartite.is_bipartite(G)

nx.draw_networkx(G, pos=nx.drawing.layout.bipartite_layout(
    G, parcours), node_color=color_map, node_size=150, width=1, linewidths=25, node_shape="s")
plt.show()
