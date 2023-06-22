# First networkx library is imported
# along with matplotlib
import networkx as nx
import matplotlib.pyplot as plt
import ChordGraph as cg

chs = 'Am E Am E B G Bm A'
# chs2 = 'Am E Am E B G Bm A'
# chs3 = 'Am E Am E B G Bm A'
#
chs2 = 'Am B Am E Am G Bm C'
chs3 = 'Am D C C C G'
chs4 = 'Am C D E Am G Bm'
chs5 = 'Am A D E C G Bm C'

TESTMODE = True

# Driver code
# G = cg.ChordGraph()
# G.addSequentialNode((0, {"chord": "Am", "bar": 0}))
# G.addSequentialNode((1, {"chord": "E", "bar": 1}))
# G.addSequentialNode((2, {"chord": "Am", "bar": 2}))
# G.addSequentialNode((3, {"chord": "E", "bar": 3}))
# G.visualize()

if TESTMODE:
	testG1 = cg.ChordGraph()
	testG2 = cg.ChordGraph()
	testG3 = cg.ChordGraph()
	testG4 = cg.ChordGraph()
	testG5 = cg.ChordGraph()

	testG1.chord_parser(chs)
	testG2.chord_parser(chs2)
	testG3.chord_parser(chs3)
	testG4.chord_parser(chs4)
	testG5.chord_parser(chs5)

	# testG1.visualize(plot_title="testg1")
	# testG2.visualize(node_color="tab:gray")
	# testG3.visualize()
	# testG4.visualize()
	# testG5.visualize()

	temp1 = testG1.combine_graphs(testG2)
	temp1.visualize(plot_title="1 temp1")
	temp1 = temp1.combine_graphs(testG2)
	temp1.visualize(plot_title="2 temp1")
	temp1 = temp1.combine_graphs(testG2)
	temp1.visualize(plot_title="3 temp1")
	temp1 = temp1.combine_graphs(testG2)
	temp1.visualize(plot_title="4 temp1")

	temp2 = temp1.combine_graphs(testG3)
	temp2.visualize()
	temp3 = temp2.combine_graphs(testG4)
	temp3.visualize()
	fin = temp3.combine_graphs(testG5)

	fin.check_duplicate_nodes()
	fin.visualize()

if not TESTMODE:
	print()
	L = nx.DiGraph()
	Z = nx.DiGraph()
	L.add_edge(1,2,weight=17)
	L.add_edge(2,3,weight=8)
	Z.add_edge(1,2,weight=3)
	Z.add_edge(2,3,weight=2)
	# e1 = [('a', 'b', 17.0)]
	# L.add_weighted_edges_from(e1)
	# e2 = [('b', 'c', 8.0)]
	# L.add_weighted_edges_from(e2)
	# e3 = [('a', 'b', 3.0)]
	# Z.add_weighted_edges_from(e3)
	# e4 = [('b', 'c', 2.0)]
	# Z.add_weighted_edges_from(e4)
	print(list(L.edges(data=True)))
	print(list(Z.edges(data=True)))

	K = nx.DiGraph()
	weight=1
	# K.add_weighted_edges_from(list((5, n, weight) for n in L.nodes))
	# K.add_weighted_edges_from(list((5, n, weight) for n in Z.nodes))

	K.add_weighted_edges_from(list((n[0],n[1],n[2]['weight']) for n in list(L.edges(data=True))))
	K.add_weighted_edges_from(list((n[0],n[1],n[2]['weight']) for n in list(Z.edges(data=True))))

	K.add_nodes_from(L.nodes(data=True))
	K.add_nodes_from(Z.nodes(data=True))

	print(list(K.edges(data=True)))
	nx.draw_networkx(K, pos=nx.spring_layout(K))
	plt.show()

# nx.draw_networkx(U)
# print(list(U.nodes(data=True)))
# plt.show()

# G2 = cg.BiChordGraph()
# G2.visualize()
