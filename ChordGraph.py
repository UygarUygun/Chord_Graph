import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.axes as axs
import matplotlib.transforms as trns
import itertools

# A convenience class to get information about nodes of the graph
class ChordNode():
	def __init__(self, id: str = None, chord: str = None, bar: int = None,
	             is_empty=False, from_tuple=False, tupleInput=None):
		if not from_tuple:
			self.id = id
			self.chord = chord
			self.bar = bar
		else:
			self.id = tupleInput[0]
			self.chord = tupleInput[1]["chord"]
			self.bar = tupleInput[1]["bar"]
		self.is_empty = is_empty
		self.in_edge_count = 0

	def as_tuple(self):
		ret: tuple = (self.id, {"chord": self.chord, "bar": self.bar})
		return ret


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

		self.lastNode = ChordNode(is_empty=True)

	def import_graph(self, input: nx.DiGraph):
		self.G = input
		self.edges = input.edges
		self.edgesWithData = input.edges(data=True)

		# print("IMPORT EDGE DATA")
		# print(self.edgesWithData)
		# print()

		self.nodes = input.nodes(data=True)

		nodesWithData = list(self.G.nodes(data=True))
		# print("NODES")
		# print(nodesWithData)
		# print()

		for i in range(len(self.nodes)):
			temp_node = ChordNode(tupleInput=nodesWithData[i], from_tuple=True)
			self.nodeObjects.append(temp_node)

		# for edge in self.edges:
		# 	self.edgeLabels[edge] = 1
		# 	print(edge)

		for edge in self.edgesWithData:
			# print('IMPORTED EDGE')
			# print(edge[2]["weight"])
			self.edgeLabels[(edge[0], edge[1])] = edge[2]["weight"]
			# TODO: see if this part funtions for size determination
			for nodeObj in self.nodeObjects:
				if edge[1] == nodeObj.id:
					nodeObj.in_edge_count += edge[2]["weight"]

		for node in self.nodeObjects:
			self.nodeLabels[node.id] = (node.chord + '\n' + str(node.in_edge_count))
			# self.nodeLabels[node.id] = node.in_edge_count

	# THIS FUNCTION SHOULD COMBINE EDGE VALUES TOO
	def combine_graphs(self, otherG : "ChordGraph"):
		outG = nx.DiGraph()
		duplicateEdges = []
		# iterate over both graphs' edges and combine duplicate edges
		# if not a duplicate edge still add the edge to the new list
		# output list should preserve all edges between nodes
		# but duplicate edges will be combined by increasing the weight

		for edge in self.edges:
			# print("EDGE CHECK")
			if edge in otherG.G.edges:
				# print(edge)
				duplicateEdges.append(edge)
				self.edgeLabels[edge] += 1

		outG.remove_edges_from(duplicateEdges)
		outG.add_edges_from(self.G.edges(data=True))
		outG.add_edges_from(otherG.G.edges(data=True))

		nx.set_edge_attributes(outG, self.edgeLabels, 'weight')

		outG.add_nodes_from(self.G.nodes(data=True))
		outG.add_nodes_from(otherG.G.nodes(data=True))

		retFormatted = ChordGraph()
		retFormatted.import_graph(outG)
		return retFormatted


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
		if self.lastNode.is_empty:
			self.nodeObjects.append(node)
			self.nodes.append(node.as_tuple())
			self.lastNode = node
			self.nodeLabels[node.id] = node.chord

			self.G.add_nodes_from(self.nodes)

		else:
			self.edges.append((self.lastNode.id, node.id))
			self.edgeLabels[(self.lastNode.id, node.id)] = 1
			wEdge = (self.lastNode.id, node.id, 1)
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


	def visualize(self, node_size=250, node_color="tab:red", y_offset=0.005, plot_title="", fig_size=(19, 7)):

		plt.figure(figsize=fig_size, frameon=False)


		nodeCountsAtIndex = [0] * len(list(self.G.nodes))
		# edgeColors = list(dict((tuple(e[0],e[1]): int(e[2]['weight']))) for e in list(self.G.edges(data=True)))
		nodes = list(self.G.nodes)
		# print(list(self.G.nodes(data=True)))
		# print(self.nodes)
		# print()
		# print('NODE ATTRIBUTES')
		# print()
		pos = {}
		nodeSizes = [node_size] * len(nodeCountsAtIndex)
		nodeColors = [0] * len(nodeSizes)

		for i in range(len(self.nodeObjects)):
			nodeSizes[i] += (self.nodeObjects[i].in_edge_count * node_size)
			nodeColors[i] += self.nodeObjects[i].in_edge_count
			# print(self.nodeObjects[i].in_edge_count)

		# print("COLORMAP")
		# print(nodeColors)

		for i in range(len(self.nodeObjects)):
			pos[self.nodeObjects[i].id] = (self.nodeObjects[i].bar,
			                               nodeCountsAtIndex[self.nodeObjects[i].bar])
			nodeCountsAtIndex[self.nodeObjects[i].bar] += y_offset

		self.p = nx.draw_networkx_nodes(
			self.G, pos, node_size=nodeSizes, nodelist=nodes,
			node_color=nodeColors, alpha=0.7
		)
		nx.draw_networkx_labels(
			self.G, pos, labels=self.nodeLabels
		)
		nx.draw_networkx_edges(
			self.G, pos, nodelist=self.nodes, alpha=0.5,
			width=1, node_size=node_size*2
		)
		# print('DEGREES')
		# print(dict(self.G.in_degree))
		# print()

		nx.draw_networkx_edge_labels(
			self.G, pos, edge_labels=self.edgeLabels, label_pos=0.6
		)

		ax = plt.gca()
		ax.margins(0)
		plt.tight_layout()
		# plt.axis("off")
		plt.suptitle(plot_title)
		plt.draw()
		# plt.show()

	def display(self, str):
		plt.show()