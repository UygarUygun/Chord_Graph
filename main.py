# First networkx library is imported
# along with matplotlib
import networkx as nx
import matplotlib.pyplot as plt
import ChordGraph as cg

lines = []
graphObjs = []


with open('songs3.txt') as f:
	lines = f.readlines()
	print(lines)
	f.close()

name = ''
artist = ''
chordseq = ''
for line in lines:
	if line.startswith('+'):
		name = line[1:-1]
	elif line.startswith('-'):
		artist = line[1:-1]
	elif line[0].isspace():
		print('end of song ' + name + ' from ' + artist)
	else:
		chordseq = line.removesuffix('\n')
		tempChordGraph = cg.ChordGraph()
		tempChordGraph.chord_parser(chordseq)
		graphObjs.append(tempChordGraph)
		print(name + ' ' + artist)
		tempChordGraph.visualize(plot_title=(name + ' by ' + artist))


tempG = graphObjs[0]
for g in graphObjs[1:len(graphObjs)]:
	tempG = tempG.combine_graphs(g)

tempG.visualize(plot_title='all songs combined')

plt.show()

