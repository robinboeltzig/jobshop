from Graph import Graph
from Graph import DetectCycle
from Graph import DAGLongestPath
from bidir import doBidir


import re
import copy
from random import randint
from random import seed
from collections import defaultdict


#input_table = "10 10 1 21 6 71 9 16 8 52 7 26 2 34 0 53 4 21 3 55 5 95 4 55 2 31 5 98 9 79 0 12 7 66 1 42 8 77 6 77 3 39 3 34 2 64 8 62 1 19 4 92 9 79 7 43 6 54 0 83 5 37 1 87 3 69 2 87 7 38 8 24 9 83 6 41 0 93 5 77 4 60 2 98 0 44 5 25 6 75 7 43 1 49 4 96 9 77 3 17 8 79 2 35 3 76 5 28 9 10 4 61 6  9 0 95 8 35 1  7 7 95 3 16 2 59 0 46 1 91 9 43 8 50 6 52 5 59 4 28 7 27 1 45 0 87 3 41 4 20 6 54 9 43 8 14 5  9 2 39 7 71 4 33 2 37 8 66 5 33 3 26 7  8 1 28 6 89 9 42 0 78 8 69 9 81 2 94 4 96 3 27 0 69 7 45 6 78 1 74 5 84"
input_table = "10 5 1 21 0 53 4 95 3 55 2 34 0 21 3 52 4 16 2 26 1 71 3 39 4 98 1 42 2 31 0 12 1 77 0 55 4 79 2 66 3 77 0 83 3 34 2 64 1 19 4 37 1 54 2 43 4 79 0 92 3 62 3 69 4 77 1 87 2 87 0 93 2 38 0 60 1 41 3 24 4 83 3 17 1 49 4 25 0 44 2 98 4 77 3 79 2 43 1 75 0 96"
temp = re.findall(r'\d+', input_table)
res = list(map(int, temp))
length = len(res)

best = 0

maxiter = 50 # set max iterations for hill climbing algorithm

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

print(SourceGraph.m)
print(SourceGraph.j)

SourceGraph.addNode(0,0,-1,-1,-1)  # Source
SourceGraph.addNode(1,0,-3,-3,-3)  # Sink

k = 2
for i in range(num_jobs):
    for j in range(num_machines):
        SourceGraph.addNode(k, operation[i, j][1], operation[i, j][0],i,j)
        k = k+1

print(SourceGraph.nodes)

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

print(SourceGraph.edges)

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

print(SourceGraph.edges)

TestGraph = copy.deepcopy(SourceGraph)
TestGraph.generateNextRandom()
print(TestGraph.edges)

t= 0

while t < maxiter:

    cyclic = True
    j = 0
    remainiter = SourceGraph.j

    RandomGraph = copy.deepcopy(SourceGraph)
    doBidir(RandomGraph)

    print(RandomGraph)


    NeighborGraph = copy.deepcopy(RandomGraph)

    DAG = DAGLongestPath()

    NeighborGraph.convertDAG(DAG)

    print(DAG.nodes)


    print(len(RandomGraph.edges))

    print(DAG.edges)

    print(DAG.longest_path()[1])

    currentschedule = DAG.longest_path()[0]
    currentbest = DAG.longest_path()[1]
    nextbest = DAG.longest_path()[1]

    print(currentschedule, currentbest, nextbest)


    print(RandomGraph.neighbor)
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
            print(NeighborGraph.edges)
            edgeposition = edgeposition+1
            #print(edgeposition)

        print(evallist)
        filtereval = filter(None, evallist)

        nextbest = min(filtereval)
        minpos = evallist.index(nextbest)
        print(nextbest)
        print(minpos)


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
        print(critpath)

    if currentbest < best:

        best = currentbest
        RandomGraph.convertDAG(DAG)
        critpath = DAG.longest_path()[0]
        print(critpath)

    t=t+1
    print()
    print(t)
    print()

print("shortest calculated makespan:")
print(best)
critpath.insert(0,0)
print()
print("critical path:")
print(critpath)
