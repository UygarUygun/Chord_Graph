import networkx as nx
import matplotlib.pyplot as plt

class ChordGraphLegacy():
	def __init__(self):
		self.G = nx.DiGraph()
		self.pos = {}
		self.edges = []
		self.nodes = []
		self.xIndex = 0
		self.lastNode = ()
		self.edgeLabels = {}
		self.nodeLabels = {}

	# Assume that the node is a tuple that is (uniqueEdgeNo, {"chord" : "CHORDNAME", "bar" : number})
	def addSequentialNode(self, node):
		# starting case
		if len(self.lastNode) == 0:
			self.nodes.append(node)
			self.lastNode = node
			self.nodeLabels[node[0]] = node[1]["chord"]
		else:
			self.edges.append((self.lastNode[0], node[0]))
			self.edgeLabels[(self.lastNode[0], node[0])] = 1
			self.nodes.append(node)
			self.lastNode = node
			self.nodeLabels[node[0]] = node[1]["chord"]

	def addEdge(self, node1, node2):
		temp = (node1, node2)
		if node1 not in self.nodes:
			self.nodes.append(node1)
		if node2 not in self.nodes:
			self.nodes.append(node2)
		self.edges.append(temp)

	def addNodeWithPos(self, node, nodePos):
		self.pos[node] = nodePos
		self.nodes.append(node)

	def addNodeWithPos(self, node, nodePosX, nodePosY):
		self.pos[node] = (nodePosX, nodePosY)
		self.nodes.append(node)

	def visualizeWPos(self):
		G = nx.DiGraph()
		G.add_edges_from(self.edges)
		nx.draw_networkx_nodes(
			G, self.pos, node_size=300, nodelist=self.nodes,
			node_color="tab:red"
		)
		nx.draw_networkx_edges(
			G, self.pos, nodelist=self.nodes, alpha=0.3, width=6
		)
		nx.draw_networkx_labels(
			G, self.pos
		)
		ax = plt.gca()
		ax.margins(0.11)
		plt.tight_layout()
		plt.axis("off")
		plt.show()

	def visualize(self):
		# G = nx.DiGraph()
		self.G.add_edges_from(self.edges)
		self.G.add_nodes_from(self.nodes)
		nodes = list(self.G.nodes)
		print(list(self.G.nodes(data=True)))
		print(self.nodes)
		pos = {}

		for i in range(len(nodes)):
			print(self.nodes[i][1]["bar"])
			pos[nodes[i]] = (self.nodes[i][1]["bar"], 0)

		# nx.draw_networkx(G, pos, with_labels=True)
		nx.draw_networkx_nodes(
			self.G, pos, node_size=1000, nodelist=nodes,
			node_color="tab:red"
		)
		nx.draw_networkx_labels(
			self.G, pos, labels=self.nodeLabels
		)
		nx.draw_networkx_edges(
			self.G, pos, nodelist=self.nodes, alpha=0.3,
			width=6, node_size=1000, label="edge"
		)
		nx.draw_networkx_edge_labels(
			self.G, pos, edge_labels=self.edgeLabels
		)

		ax = plt.gca()
		ax.margins(0)
		plt.tight_layout()
		plt.axis("off")
		plt.show()

	def display(self):
		plt.show()

	def chord_parser(self, input: str):
		chords: list = input.split()
		for i in range(len(chords)):
			tempNode = (i, {"chord": chords[i], "bar": i})
			self.addSequentialNode(tempNode)
