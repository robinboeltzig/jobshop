from Graph import Graph
from Graph import DetectCycle
from Graph import DAGLongestPath

import re
import copy
from random import randint
from random import seed
from collections import defaultdict


# input_table = "10 10 4 88 8 68 6 94 5 99 1 67 2 89 9 77 7 99 0 86 3 92 5 72 3 50 6 69 4 75 2 94 8 66 0 92 1 82 7 94 9 63 9 83 8 61 0 83 1 65 6 64 5 85 7 78 4 85 2 55 3 77 7 94 2 68 1 61 4 99 3 54 6 75 5 66 0 76 9 63 8 67 3 69 4 88 9 82 8 95 0 99 2 67 6 95 5 68 7 67 1 86 1 99 4 81 5 64 6 66 8 80 2 80 7 69 9 62 3 79 0 88 7 50 1 86 4 97 3 96 0 95 8 97 2 66 5 99 6 52 9 71 4 98 6 73 3 82 2 51 1 71 5 94 7 85 0 62 8 95 9 79 0 94 6 71 3 81 7 85 1 66 2 90 4 76 5 58 8 93 9 97 3 50 0 59 1 82 8 67 7 56 9 96 6 58 4 81 5 59 2 96"
input_table = "4 4 2 10 3 12 1 19 0 13 3 11 0 5 1 17 2 14 2 13 3 17 0 20 1 19 0 14 3 18 1 8 2 4"
temp = re.findall(r'\d+', input_table)
res = list(map(int, temp))
length = len(res)

best = 0

maxiter = 100 # set max iterations for hill climbing algorithm

num_jobs = res[0]
num_machines = res[1]
header = [num_jobs,num_machines]
nonheader = res[2:]

job = list()

for i in range(num_machines):
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

    LastCheck = copy.deepcopy(SourceGraph)

    while remainiter > 0:

        while cyclic == True:
            RandomGraph = copy.deepcopy(LastCheck)
            RandomGraph.generateNextRandom()
            num_nodes = num_machines*num_jobs + 2
            CycleGraph = DetectCycle(num_nodes)

            RandomGraph.convertCycle(CycleGraph)

            if CycleGraph.isCyclic():
                cyclic = True
            else:
                cyclic = False
            j = j + 1
        remainiter = remainiter-1
        LastCheck = copy.deepcopy(RandomGraph)
        print(remainiter)
        j = 0
        cyclic = True


    # print("done")
    # print("Graph is acyclic!")


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
    if currentbest < best:
        best = currentbest

    t=t+1
    print()
    print(t)
    print()
print(best)
