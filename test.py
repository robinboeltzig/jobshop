from Graph import Graph
from bidir import doBidir

g = Graph()
g.addNode(0,0,-1,-1,-1)  # Source
g.addNode(1,0,-3,-3,-3)  # Sink
g.addNode(2,11,0,0,0)
g.addNode(3,9,2,0,1)
g.addNode(4,7,3,0,2)
g.addNode(5,4,1,1,0)
g.addNode(6,8,2,1,1)
g.addNode(7,6,0,1,2)
g.addNode(8,10,1,2,0)
g.addNode(9,5,0,2,1)
g.addNode(10,8,1,2,2)
g.addEdge(0,0,2,0,False)
g.addEdge(1,0,5,0,False)
g.addEdge(2,0,8,0,False)
g.addEdge(3,2,3,0,False)
g.addEdge(4,3,4,0,False)
g.addEdge(5,5,6,0,False)
g.addEdge(6,6,7,0,False)
g.addEdge(7,8,9,0,False)
g.addEdge(8,9,10,0,False)
g.addEdge(9,4,1,0,False)
g.addEdge(10,7,1,0,False)
g.addEdge(11,10,1,0,False)
g.addEdge(12,2,7,2,False)
g.addEdge(13,2,9,2,False)
g.addEdge(14,7,9,2,False)
g.addEdge(15,3,5,2,False)
g.addEdge(16,3,8,2,False)
g.addEdge(17,5,8,2,False)
g.addEdge(18,4,6,2,False)
g.addEdge(19,4,10,2,False)
g.addEdge(20,6,10,2,False)
doBidir(g)
print(g.edges)

print(g.edges[12][2],g.edges[13][2],g.edges[14][2])
if [g.edges[12][2],g.edges[13][2],g.edges[14][2]] == [1,0,1] or [g.edges[12][2],g.edges[13][2],g.edges[14][2]] == [0,1,0]:
    print("ERROR")
if [g.edges[15][2],g.edges[16][2],g.edges[17][2]] == [1,0,1] or [g.edges[15][2],g.edges[16][2],g.edges[17][2]] == [0,1,0]:
    print("ERROR")
if [g.edges[18][2],g.edges[19][2],g.edges[20][2]] == [1,0,1] or [g.edges[18][2],g.edges[19][2],g.edges[20][2]] == [0,1,0]:
    print("ERROR")