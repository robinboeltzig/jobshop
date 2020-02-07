from Graph import Graph
import random

def doBidir(Graph):
    left = {0}
    right = {1}
    s = set()
    t = set()
    r = {}
    q = {}
    for n in Graph.edges:
        if n[2] == 0:
            if n[0] == 0:
               s.add(n[1])
            if n[1] == 1:
                t.add(n[0])
        if n[2] == 1:
            if n[1] == 0:
                s.add(n[0])
            if n[0] == 1:
                t.add(n[1])
    #print()
    for n in s:
        r[n] = 0
    for n in t:
        q[n] = 0

    while len(left.union(right)) != len(Graph.nodes):
        i = random.sample(s,1)[0]
        #print(i)
        k = set()
        for n in Graph.nodes:
            #print (Graph.nodes)
            #print(n)
            if not Graph.nodes[n][4] in left:
                k.add(Graph.nodes[n][4])
        for n in Graph.edges:
            if n[0] == i and n[1] in k and n[2] == 2:
                n[2] = 0
            if n[0] in k and n[1] == i and n[2] == 2:
                n[2] = 1
        s.remove(i)
        left.add(i)
        t.discard(i)
        for n in Graph.edges:
            if n[0] == i and n[2] == 0:
                for m in Graph.nodes:
                    if Graph.nodes[m][2] == Graph.nodes[i][2] and Graph.nodes[m][3] == Graph.nodes[i][3]+1:
                        succ = Graph.nodes[m][4]
                        if succ not in right:
                            s.add(succ)
            elif n[1] == i and n[2] == 1:
                for m in Graph.nodes:
                    if Graph.nodes[m][2] == Graph.nodes[i][2] and Graph.nodes[m][3] == Graph.nodes[i][3]+1:
                        succ = Graph.nodes[m][4]
                        if succ not in right:
                            s.add(succ)
        for n in r:
            x = set()
            for m in Graph.nodes:
                if Graph.nodes[m][4] in r:
                    if Graph.nodes[m][3] == 0:
                        r[n] = 0
                    else:
                        for b in Graph.nodes:
                            if Graph.nodes[b][2] == Graph.nodes[m][2] and Graph.nodes[b][3] < Graph.nodes[m][3]:
                                x.add(Graph.nodes[b][4])
            dist = 0
            for m in x:
                dist = dist + m
            r[n] = dist
        if len(left.union(right)) != len(Graph.nodes):
            i = random.sample(t,1)[0]
            j = set()
            for n in Graph.nodes:
                if not Graph.nodes[n][4] in right:
                    j.add(Graph.nodes[n][4])
            for n in Graph.edges:
                if n[0] == i and n[1] in j and n[2] == 2:
                    n[2] = 1
                if n[0] in j and n[1] == i and n[2] == 2:
                    n[2] = 0
            t.remove(i)
            right.add(i)
            s.discard(i)
            for n in Graph.edges:
                if n[0] == i and n[2] == 1:
                    for m in Graph.nodes:
                        if Graph.nodes[m][2] == Graph.nodes[i][2] and Graph.nodes[m][3] == Graph.nodes[i][3]-1:
                            pred = Graph.nodes[m][4]
                            if pred not in left:
                                t.add(pred)
                elif n[1] == i and n[2] == 0:
                    for m in Graph.nodes:
                        if Graph.nodes[m][2] == Graph.nodes[i][2] and Graph.nodes[m][3] == Graph.nodes[i][3]-1:
                            pred = Graph.nodes[m][4]
                            if pred not in left:
                                t.add(pred)
            for n in q:
                x = set()
                for m in Graph.nodes:
                    if Graph.nodes[m][4] in q:
                        if Graph.nodes[m][3] == 0:
                            q[n] = 0
                        else:
                            for b in Graph.nodes:
                                if Graph.nodes[b][2] == Graph.nodes[m][2] and Graph.nodes[b][3] > Graph.nodes[m][3]:
                                    x.add(Graph.nodes[b][4])
                dist = 0
                for m in x:
                    dist = dist + m
                q[n] = dist