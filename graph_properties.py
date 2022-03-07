import csv
from reprlib import recursive_repr
import pandas as pd

class Node:
    def __init__(self, id, inN, outN):
        self.id = id
        self.in_degree = 0
        self.out_degree = 0
        self.in_neigh = inN
        self.out_neigh = outN
        self.reciprocals = set()        # Nodes with whom you share a reciprocal edge
        self.tc = 0
        self.triadic_motif_count = 0

    def ID(self):
        return self.id

    # Convert sets to sorted lists
    def finalize(self):
        try:
            self.reciprocals = sorted(self.in_neigh.intersection(self.out_neigh))
            self.in_neigh = sorted(self.in_neigh)
            self.out_neigh = sorted(self.out_neigh)
            self.in_degree = len(self.in_neigh)
            self.out_degree = len(self.out_neigh)
        except:
            print("Could not finalize node ", self.id)

    # Motif 2D
    def reciprocal_edge_count(self):
        return(len(self.reciprocals))

    # Motif 2A
    def nonreciprocal_edge_count(self):
        nonreciprocals = [node for node in self.in_neigh if not node in self.out_neigh]
        return(len(nonreciprocals))

    # Motifs 3F and 3G
    def naive_triangle_count(self, digraph):
        try:
            triangle_count = 0                          # Total number of undirected triangles node is connected to
            motif_count = 0                             # Total number of 3F & 3G triangles node is connected to
            graph = undirected(digraph)
            for i in graph[self.id].out_neigh:                  
                for j in graph[i].out_neigh:          
                    for k in graph[j].out_neigh:
                        if self.ID() == k:             # Triangle found - node is connected to an undirected triangle
                            triangle_count += 1
                            if triadic_motif(self.id, i, j, digraph):
                                motif_count += 1
            self.tc = triangle_count / 2
            self.triadic_motif_count = motif_count / 2
        except:
            print("Could not calculate triadic motifs for node ", self.id)

    def printer(self):
        print("Node ID: ", self.id)
        print("In-degree: ", self.in_degree, " | Out-degree:", self.out_degree)
        print("\tOutgoing Neighbors: ", self.out_neigh)
        print("\tIncoming Neighbors: ", self.in_neigh)
        print("\t\tMotif 2D Count: ", self.reciprocal_edge_count())
        print("\t\tMotif 2A Count: ", self.nonreciprocal_edge_count())
        print("\t\t\tUndirected Triangle Count: ", self.tc)
        print("\t\t\tTriadic Motif Count: ", self.triadic_motif_count)


# Given 3 nodes known to form an undirected triangle n1 -> n2 -> n3 -> n1
# Determine if their directed edges compose a 3F or 3G motif
def triadic_motif(n1, n2, n3, digraph):
    rc = 0
    if (n2 in digraph[n1].reciprocals):
        rc += 1
    if (n3 in digraph[n2].reciprocals):
        rc += 1
    if (n1 in digraph[n3].reciprocals):
        rc += 1
    if rc >= 2:
        return True
    else:
        return False

# Convert a directed graph into an undirected graph
def undirected(digraph):
    graph = {}
    for id, node in digraph.items():
        neighbors = (set(node.out_neigh)).union(set(node.in_neigh))
        graph[id] = Node(id, neighbors, neighbors)
        graph[id].finalize()
    return graph

# Convert graphs into GAPBS-like format for triangle counting
# nodeIDs and edges must be sets of UNIQUE nodes and edges
def gapbs_converter(nodeIDs, edges):
    # Assemble a dictionary of Nodes keyed by their user ID
    graph = {}
    for n in nodeIDs:
        graph[n] = Node(n, set(), set())
    # Iterate through edge list to populate Node neighborhoods and degrees
    for src, dest in edges:
        graph[src].out_neigh.add(dest)
        graph[dest].in_neigh.add(src)
    # Sort neighborhoods by node id
    for _, node in graph.items():
        node.finalize()
    # Count 3D motifs
    for _, node in graph.items():
        node.naive_triangle_count(graph)
    # Print complete node information
    for _, node in graph.items():
        node.printer()


nodes = set(pd.read_csv("nodes.csv").Label)
el1 = pd.read_csv("edges.csv")
edges= set()
for i in range(len(el1)):
    e = (el1.source[i], el1.target[i])
    edges.add(e)
gapbs_converter(nodes, edges)
