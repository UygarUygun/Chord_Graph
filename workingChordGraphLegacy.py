import networkx as nx
import matplotlib.pyplot as plt
import itertools


class ChordNode():
	def __init__(self, id: str = None, chord: str = None, bar: int = None,
	             empty=False, from_tuple=False, tupleInput=None):
		if not from_tuple:
			self.id = id
			self.chord = chord
			self.bar = bar
		else:
			self.id = tupleInput[0]
			self.chord = tupleInput[1]["chord"]
			self.bar = tupleInput[1]["bar"]
		self.empty = empty

	def as_tuple(self):
		ret: tuple = (self.id, {"chord": self.chord, "bar": self.bar})
		return ret

	def is_empty(self):
		return self.empty

	def is_duplicate(self, otherNode: "ChordNode"):
		if otherNode.id != self.id and otherNode.chord == self.chord and otherNode.bar == self.bar:
			return True
		else: return False

class ChordGraph():
	def __init__(self):
		self.G = nx.DiGraph()
		self.edges = []
		self.edgesWithData = []
		self.edgeLabels = {}

		self.nodeObjects = []
		self.nodes = []
		self.nodeLabels = {}

		self.lastNode = ChordNode(empty=True)

	def import_graph(self, input: nx.DiGraph):
		self.G = input
		self.edges = input.edges
		self.edgesWithData = input.edges(data=True)
		self.nodes = input.nodes(data=True)

		nodesWithData = list(self.G.nodes(data=True))
		print("NODES")
		print(nodesWithData)
		print()

		for i in range(len(self.nodes)):
			temp_node = ChordNode(tupleInput=nodesWithData[i], from_tuple=True)
			self.nodeObjects.append(temp_node)

		for edge in self.edges:
			self.edgeLabels[edge] = 1
			print(edge)

		for node in self.nodeObjects:
			self.nodeLabels[node.id] = node.chord

	# THIS FUNCTION SHOULD COMBINE EDGE VALUES TOO
	def combine_graphs(self, otherG : "ChordGraph"):
		outG = nx.DiGraph()
		outG.add_weighted_edges_from(self.G.edges(data=True))
		outG.add_weighted_edges_from(otherG.G.edges(data=True))
		outG.add_nodes_from(self.G.nodes(data=True))
		outG.add_nodes_from(otherG.G.nodes(data=True))

		return outG


	# this function deletes repeated nodes (nodes with the same bar and chord values)
	# while deleting the edges connected to the deleted node are connected
	# to the remaining node
	def check_duplicate_nodes(self):
		for i in range(len(self.nodes)):
			for j in range(i, len(self.nodes)):
				if self.nodeObjects[i].is_duplicate(self.nodeObjects[j]):
					# delete one node
					# reconnect edges
					print("Duplicate node found: " + str(self.nodeObjects[i].as_tuple()) + " and " + str(self.nodeObjects[j].as_tuple()))


	# Assume that the node is a tuple that is (uniqueEdgeNo, {"chord" : "CHORDNAME", "bar" : number})
	def add_sequential_node(self, node: ChordNode):
		# starting case
		if self.lastNode.is_empty():
			self.nodeObjects.append(node)
			self.nodes.append(node.as_tuple())
			self.lastNode = node
			self.nodeLabels[node.id] = node.chord

			self.G.add_nodes_from(self.nodes)

		else:
			self.edges.append((self.lastNode.id, node.id))
			self.edgeLabels[(self.lastNode.id, node.id)] = 1
			wEdge = (self.lastNode.id, node.id, {"weight": 1})
			self.edgesWithData.append(wEdge)
			self.nodeObjects.append(node)
			self.nodes.append(node.as_tuple())
			self.lastNode = node
			# print(node.id)
			self.nodeLabels[node.id] = node.chord

			self.G.add_nodes_from(self.nodes)
			# self.G.add_edges_from(self.edges)
			self.G.add_weighted_edges_from(self.edgesWithData)


	def chord_parser(self, input: str):
		chords: list = input.split()
		for i in range(len(chords)):
			tempNode = ChordNode(str(chords[i] + str(i)), chords[i], i)
			self.add_sequential_node(tempNode)


	def visualize(self, node_size=1000, node_color="tab:red", y_offset=0.005):
		# self.G.add_edges_from(self.edges)
		# self.G.add_nodes_from(self.nodes)

		nodeCountsAtIndex = [0] * len(list(self.G.nodes))
		nodes = list(self.G.nodes)
		print(list(self.G.nodes(data=True)))
		print(self.nodes)
		print()
		pos = {}

		for i in range(len(self.nodeObjects)):
			pos[self.nodeObjects[i].id] = (self.nodeObjects[i].bar,
			                               nodeCountsAtIndex[self.nodeObjects[i].bar])
			nodeCountsAtIndex[self.nodeObjects[i].bar] += y_offset

		# nx.draw_networkx(G, pos, with_labels=True)
		nx.draw_networkx_nodes(
			self.G, pos, node_size=node_size, nodelist=nodes,
			node_color=node_color
		)
		nx.draw_networkx_labels(
			self.G, pos, labels=self.nodeLabels
		)
		nx.draw_networkx_edges(
			self.G, pos, nodelist=self.nodes, alpha=0.3,
			width=6, node_size=node_size
		)
		labels = nx.get_edge_attributes(self.G, 'weight')
		nx.draw_networkx_edge_labels(
			self.G, pos, edge_labels=self.edgeLabels
		)

		ax = plt.gca()
		ax.margins(0)
		plt.tight_layout()
		plt.axis("off")
		plt.show()
