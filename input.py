from Graph import Graph
from Graph import DAGLongestPath
from bidir import doBidir


import re
import copy



"""
NEXT 2 LINES ARE USER INPUT
"""

input_table = "10 5 1 21 0 53 4 95 3 55 2 34 0 21 3 52 4 16 2 26 1 71 3 39 4 98 1 42 2 31 0 12 1 77 0 55 4 79 2 66 3 77 0 83 3 34 2 64 1 19 4 37 1 54 2 43 4 79 0 92 3 62 3 69 4 77 1 87 2 87 0 93 2 38 0 60 1 41 3 24 4 83 3 17 1 49 4 25 0 44 2 98 4 77 3 79 2 43 1 75 0 96"
maxiter = 20 #set max iterations for hill climbing algorithm


temp = re.findall(r'\d+', input_table)
res = list(map(int, temp))
length = len(res)

best = 0

num_jobs = res[0]
num_machines = res[1]
header = [num_jobs,num_machines]
nonheader = res[2:]

job = list()

for i in range(num_jobs):
    begin = 2*i*num_machines
    end = begin+2*num_machines
    job.append(nonheader[begin:end])

operation = {}

for i in range(num_jobs):
    for j in range(num_machines):
        operation[i,j] = [job[i][2*j],job[i][2*j+1]]


SourceGraph = Graph()

SourceGraph.changeJ(res[0])
SourceGraph.changeM(res[1])

SourceGraph.calcNeighbor()

# print(SourceGraph.m)
# print(SourceGraph.j)

SourceGraph.addNode(0,0,-1,-1,-1)  # Source
SourceGraph.addNode(1,0,-3,-3,-3)  # Sink

k = 2
for i in range(num_jobs):
    for j in range(num_machines):
        SourceGraph.addNode(k, operation[i, j][1], operation[i, j][0],i,j)
        k = k+1

# print(SourceGraph.nodes)

k = 0
for n in SourceGraph.nodes:
    if SourceGraph.nodes[n][3] < num_machines - 1:
        if SourceGraph.nodes[n][0] > 1:
            SourceGraph.addEdge(k,n,n+1,0, False)
            k = k+1

for i in range(num_jobs):
    SourceGraph.addEdge(k,0,2+i*num_machines,0, False)
    k=k+1

for i in range(num_jobs):
    SourceGraph.addEdge(k,1+(i+1)*num_machines,1,0, False)
    k=k+1

# print(SourceGraph.edges)

machines = {}
for i in range(num_machines):
    x = 0
    for n in SourceGraph.nodes:
        if SourceGraph.nodes[n][1] == i:
            machines[i,x] = SourceGraph.nodes[n]
            x = x+1

for m in SourceGraph.nodes:
    for n in SourceGraph.nodes:
        if SourceGraph.nodes[m][1] == SourceGraph.nodes[n][1]:
            if SourceGraph.nodes[m][4] < SourceGraph.nodes[n][4]:
                SourceGraph.addEdge(k,SourceGraph.nodes[m][4],SourceGraph.nodes[n][4],2, True)

# print(SourceGraph.edges)

TestGraph = copy.deepcopy(SourceGraph)
TestGraph.generateNextRandom()
# print(TestGraph.edges)

t= 0

while t < maxiter:

    cyclic = True
    j = 0
    remainiter = SourceGraph.j

    RandomGraph = copy.deepcopy(SourceGraph)
    doBidir(RandomGraph)

   # print(RandomGraph)


    NeighborGraph = copy.deepcopy(RandomGraph)

    DAG = DAGLongestPath()

    NeighborGraph.convertDAG(DAG)

   # print(DAG.nodes)


    # print(len(RandomGraph.edges))

    #print(DAG.edges)

   # print(DAG.longest_path()[1])

    currentschedule = DAG.longest_path()[0]
    currentbest = DAG.longest_path()[1]
    nextbest = DAG.longest_path()[1]

    # print(currentschedule, currentbest, nextbest)


   # print(RandomGraph.neighbor)
    localmin = False

    while localmin == False:

        evallist = []
        edgeposition = 0

        for n in range(NeighborGraph.neighbor):
            currentposition = 0
            NeighborGraph = copy.deepcopy(RandomGraph)
            for n in range(len(NeighborGraph.edges)):
                if NeighborGraph.edges[n][3] == True:

                    if edgeposition == currentposition:
                        if NeighborGraph.edges[n][2] == 0:
                            NeighborGraph.edges[n][2] = 1
                        else:
                            NeighborGraph.edges[n][2] = 0

                    currentposition = currentposition+1
                    #print(currentposition)
            DAG = DAGLongestPath()
            NeighborGraph.convertDAG(DAG)
            evallist.append(DAG.longest_path()[1])
            #print(NeighborGraph.edges)
            edgeposition = edgeposition+1
            #print(edgeposition)

        print("list of all neighbors:", evallist)
        filtereval = filter(None, evallist)

        nextbest = min(filtereval)
        minpos = evallist.index(nextbest)
        print("next best:", nextbest)


        if nextbest < currentbest:
            currentbest =nextbest
            c = 0
            for n in RandomGraph.edges:

                if n[3] == True:
                    if c == minpos:
                        if n[2] == 0:
                            n[2] = 1
                        else:
                            n[2] = 0
                    c= c+1

        else:
            localmin=True
    if best == 0:
        best = currentbest

        RandomGraph.convertDAG(DAG)
        critpath = DAG.longest_path()[0]
        # print(critpath)

    if currentbest < best:

        best = currentbest
        RandomGraph.convertDAG(DAG)
        critpath = DAG.longest_path()[0]
        # print(critpath)

    t=t+1
    print()
    print("current iteration:", t)
    print()

print("shortest calculated makespan:")
print(best)
critpath.insert(0,0)
print()
print("critical path:")
print(critpath)
