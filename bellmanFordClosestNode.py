
############################################################
# Starter code for Bellman-Ford modification assignment
# November 2024
# Adam Smith, Ross Mikulskis Boston University
############################################################

import sys
import os
import heapq
import queue
import numpy as np
import simplegraphs as sg

############################################################
#
# CODE FOR ASSIGNMENT
#
############################################################

# distances_to_closest[u] should be the length of the
# lightest path of length at least 1 starting from u.
def findClosestNodes(G):
    ############################# YOUR CODE GOES HERE
    distances_to_closest = {} 
    n = G["n"]  # Number of nodes
    d = [{} for i in range(n+1)]
    for u in G["adj"]:
        d[0][u] = np.inf
    
    for i in range(1, n+1):
        difference = False
        for x in G["adj"]:
            d[i][x] = d[i-1][x]
        for u in G["adj"]:
            for v in G["adj"][u]:
                novel = min(d[i-1][v] + G["adj"][u][v], G["adj"][u][v])
                if novel < d[i][u]:
                    d[i][u] = novel
                    difference = True
        if not difference:
            distances_to_closest = d[i]
            return distances_to_closest
        
    distances_to_closest = d[n]
    

    
    return distances_to_closest

############################################################
#
# HELPFUL CODE
#
############################################################

# G is a dictionary with keys "n", "m", "adj" representing a *weighted* graph
# G["adj"][u][v] is the cost (length / weight) of edge (u,v)
#
# This algorithms finds least-costs paths to all vertices
# Will not detect negative-cost cycles
# Returns an dict of distances (path costs) and parents in the lightest-paths
# tree.
#
# This is basically the algorithm we covered in class (except it
# finds paths from a source instead of to a desitnation).
def bellmanFordSimple(G, s):
    n = G["n"]
    d = [{} for i in range(n+1)]
    for u in G["adj"]:
        d[0][u] = np.inf
    d[0][s] = 0
    parent = {s: None}
    for i in range(1,n+1):
        changed = False
        for v in G["adj"]:
            d[i][v] = d[i-1][v]
        for u in G["adj"]:
            for v in G["adj"][u]:
                newlength = d[i-1][u] + G["adj"][u][v]
                if newlength <  d[i][v]:
                    d[i][v] = newlength
                    parent[v] = u
                    changed = True
        # How can you decide whether it is ok to stop?
    if changed:
        print("Negative cycle reachable from source!")
    distance = d[n-1]
    return distance, parent

# Key: s=source node; shortestPaths, closestNodes=tasks
USAGE = "Usage: python3 bellmanFordClosestNode.py \
shortestPaths|closestNodes input_file output_file [s]"

def interpretCommandLineArgs(args = []):
    assert len(args) >= 3, USAGE
    
    task = args[0]
    graph_file_name = args[1]
    out_file_name = args[2]

    
    if task == "shortestPaths":
        assert len(args) == 4, USAGE
        s = int(args[3])
        G = sg.readGraph(graph_file_name) # read graph from disk
        distances, parent = bellmanFordSimple(G,s)
        writeBFOutput(distances, parent, out_file_name)
    elif task == "closestNodes":
        assert len(args) == 3, USAGE
        G = sg.readGraph(graph_file_name)
        distances_to_closest = findClosestNodes(G)
        writeCNDistances(distances_to_closest, out_file_name)
    else: 
        print(f"Error: Task {task} not recognized")
        print(USAGE)
    return

def writeBFOutput(distances, parent, out_file_name):
    with open(out_file_name, 'w') as f:
        for u in distances:
            f.write(f"{u}, {distances[u]}, {parent[u]}\n")
    return

def writeCNDistances(distances_to_closest, out_file_name):
    with open(out_file_name, 'w') as f:
        L = list(distances_to_closest.keys())
        L.sort()
        for u in L:
            f.write(f"{u}, {float(distances_to_closest[u])}\n")

    return

if __name__ == "__main__":
    # pass command line arg to "interpretCommandLineArgs" func
    interpretCommandLineArgs(sys.argv[1:])    
