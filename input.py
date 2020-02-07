from Graph import Graph
from Graph import DetectCycle
from Graph import DAGLongestPath
from bidir import doBidir


import re
import copy
from random import randint
from random import seed
from collections import defaultdict










"""NEXT 2 LINES ARE USER INPUT
    """

input_table = "20 5 3 60 0 87 1 72 4 95 2 66 1 54 0 48 2 39 3 35 4  5 3 20 1 46 0 97 2 21 4 55 2 37 0 59 3 19 1 34 4 46 2 73 3 25 1 24 0 28 4 23 1 78 3 28 2 83 0 45 4  5 3 71 1 37 2 12 4 29 0 53 4 12 3 33 1 55 2 87 0 38 0 48 1 40 2 49 3 83 4  7 0 90 4 27 2 65 3 17 1 23 0 62 3 85 1 66 2 84 4 19 3 59 2 46 4 13 1 64 0 25 2 53 1 73 3 80 4 88 0 41 2 57 4 47 0 14 1 67 3 74 2 41 4 64 3 84 1 78 0 84 4 52 3 28 2 26 0 63 1 46 1 11 0 64 3 10 4 73 2 17 4 38 3 95 0 85 1 97 2 67 3 93 1 65 2 95 0 59 4 46 0 60 1 85 2 43 4 85 3 32"

maxiter = 20 # set max iterations for hill climbing algorithm






















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
