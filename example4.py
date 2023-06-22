import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.axes as ax

# nodes = [0, 1, 2, 3, 4, 5, 6, 7]
edges = [("Am", "B"), ("B", "Em"), ("Em", "Am"), ("Am", "C")]
pos = {}

G = nx.DiGraph(edges)
nodes = list(G.nodes)

for i in range(len(nodes)):
	pos[nodes[i]] = (i, 0)

# G = nx.line_graph(H)
# pos = nx.planar_layout(G)  # Seed layout for reproducibility
nx.draw(G, pos)
plt.show()