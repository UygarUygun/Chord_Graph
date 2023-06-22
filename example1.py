import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualization():
	def __init__(self):
		self.visual = []

	def addEdge(self, a, b):
		temp = (a, b)
		self.visual.append(temp)

	def visualize(self):
		G = nx.DiGraph()
		G.add_edges_from(self.visual)
		nx.draw_networkx(G)
		plt.show()


G = nx.DiGraph()
pos = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1), 4: (0, 2.0)}
nodes = [0, 1, 2, 3, 4]
edges = [(0,1), (1,2)]

G.add_edges_from(edges)
nx.draw_networkx_nodes(
	G, pos, node_size=3000, nodelist=[0,1,2,3], node_color="tab:red"
)
nx.draw_networkx_nodes(
	G, pos, node_size=500, nodelist=[4], node_color="tab:blue"
)
nx.draw_networkx_edges(
	G, pos, nodelist=[0,1,2,3,4], alpha=0.5, width=6
)
nx.draw_networkx_labels(
	G, pos
)
ax = plt.gca()
ax.margins(0.11)
plt.tight_layout()
plt.axis("off")
plt.show()