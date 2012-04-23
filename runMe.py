import networkx as nx
import matplotlib.pyplot as plt

def neighborList(G, node, props):
	neigh = G.neighbors(node)
	neigh.remove('Weight')
	for prop in props:
		neigh.remove(prop)
	return neigh

print "\n"
props = ['Actor','Director','Producer','Genre']

G = nx.Graph()

#Constructing a graph from the JSON file
fin = open("testFile.txt")
JSONarr = fin.readlines()

#creating nodes. Each movie is a node.
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

	#creating edges between nodes. Each edge is associated with a list that specifies how those two entities are related.
	for node in nodes:
		for key in props:
			#print G[JSONobj['Name']][key]
			#print G[node][key]
			#print set(G[JSONobj['Name']][key]).isdisjoint(set(G[node][key]))
			if not set(G[JSONobj['Name']][key]).isdisjoint(set(G[node][key])):
				if G.has_edge(JSONobj['Name'], node): #if the edge is being added for the first time, then initialize its value with the key, else append the key to the existing relation.
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

'''configuration'''
weightVector = [1,1,1,1] #This is the weights associated with every movie
inputSeq = ["MovieName1","MovieName2","MovieName2"] #This is the sequence in which the user has watched a movie


#normalizing the weight vector
s = float(sum(weightVector))
for i in range(len(weightVector)):
	weightVector[i] = weightVector[i] / s

#propWeight is a dictionary that has a weight associated with every property. Ex: {"Director": 0.3}
propWeight = {}
for i in range(len(props)):
	propWeight[props[i]] = weightVector[i]

for node in inputSeq: #traverse every node in the inputsequence of the reader
	neighbors = neighborList(G, node, props) #get the neighbors of the those nodes
	for neighbor in neighbors: #for each neighbor, get the information on how it is connected to this node
		#print "\n"
		#print (node, neighbor)
		Associations = G[node][neighbor]['Associations']
		for assocs in Associations:
			G[neighbor]['Weight'] += propWeight[assocs] #increase the weight of the neighbor based on its associations with the current node.

#Sort the movie names according to their Weights gained.
FinalValue = {}
for node in G.nodes():
	FinalValue[node] = G[node]['Weight']

FinalValue = FinalValue.items()
FinalValue = [(rating, name) for name,rating in FinalValue]
FinalValue.sort(reverse = True)
FinalValue = [name for rating, name in FinalValue]

print "Movies watched: " + str(inputSeq)
print "Recommendation: " + str(FinalValue)
