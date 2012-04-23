import networkx as nx
import matplotlib.pyplot as plt

def neighborList(G, node, props):
	neigh = G.neighbors(node)
	neigh.remove('Weight')
	for prop in props:
		neigh.remove(prop)
	return neigh

props = ['Actor','Director','Producer','Genre']

G = nx.Graph()

fin = open("testFile.txt")
JSONarr = fin.readlines()
for line in JSONarr:
	JSONobj = eval(line)
	nodes = G.nodes()
	#print nodes
	G.add_node(JSONobj['Name'])
	G[JSONobj['Name']]['Weight'] = 0
	G[JSONobj['Name']]['Director'] = JSONobj['Director'] #this is a list
	G[JSONobj['Name']]['Actor'] = JSONobj['Actor']
	G[JSONobj['Name']]['Producer'] = JSONobj['Producer']
	G[JSONobj['Name']]['Genre'] = JSONobj['Genre']
	#print G[JSONobj['Name']]

	for node in nodes:
		for key in props:
			#print G[JSONobj['Name']][key]
			#print G[node][key]
			#print set(G[JSONobj['Name']][key]).isdisjoint(set(G[node][key]))
			if not set(G[JSONobj['Name']][key]).isdisjoint(set(G[node][key])):
				if G.has_edge(JSONobj['Name'], node):
					CurrAssoc = G[JSONobj['Name']][node]['Associations']
					CurrAssoc.append(key)
					G.add_edge(JSONobj['Name'], node, Associations = CurrAssoc)
				else:
					G.add_edge(JSONobj['Name'], node, Associations = [key])
	#print G[JSONobj['Name']]
	#print "\n"

'''
for node in G.nodes():
	print "\n" + node
	print neighborList(G, node, props)
'''
#nx.draw(G)
#plt.show()

#configuration
weightVector = [1,2,1,1]
inputSeq = ["MovieName1","MovieName2","MovieName2"]
s = float(sum(weightVector))
for i in range(len(weightVector)):
	weightVector[i] = weightVector[i] / s

propWeight = {}
for i in range(len(props)):
	propWeight[props[i]] = weightVector[i]

for node in inputSeq:
	neighbors = neighborList(G, node, props)
	for neighbor in neighbors:
		print "\n"
		print (node, neighbor)
		Associations = G[node][neighbor]['Associations']
		for assocs in Associations:
			print 
			G[neighbor]['Weight'] += propWeight[assocs]

FinalValue = {}
for node in G.nodes():
	FinalValue[node] = G[node]['Weight']

FinalValue = FinalValue.items()
FinalValue = [(rating, name) for name,rating in FinalValue]
FinalValue.sort(reverse = True)
FinalValue = [name for rating, name in FinalValue]
print FinalValue
