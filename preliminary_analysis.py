##### Preliminary analysis #####

import pandas as pd
import networkx as nx
import networkx.algorithms.community as comm

# Given a path to a src/target edge list CSV
# Returns a NetworkX digraph
def graph_gen_from_el(path):
    digraph = nx.DiGraph()
    df = pd.read_csv(path, dtype={'source': str, 'target': str})
    for _, edge in df.iterrows():
        digraph.add_edge(edge.source, edge.target)
    return digraph

def read_popular_nodes(path):
    with open(path, "r") as f:
        nodes = f.readlines()

# Analyze a digraph dgX
def analyze(dgX, popular_nodes):
    # Calculate directed clustering coefficients
    coeffs = nx.clustering(dgX, popular_nodes)
    for node, cf in coeffs.items():
        print("Node: ", node, "has DCC ", cf)
    # Use NX to check reciprocity ratio
    rec = nx.reciprocity(dgX, popular_nodes)
    print("NX Reciprocity Ratio for popular nodes: ")
    print(rec)

if __name__=="__main__":
    dataset = ['guncontrol', 'obamacare', 'abortion']
    for d in dataset:
        print("######### Dataset: ", d, " #########\n")
        edge_lists = ["/democrat_subgraph", "/republican_subgraph", "/no_dems_subgraph", 
                        "/no_reps_subgraph", "/knownusers_subgraph", "/" + d]
        for e in edge_lists:
            print("Analyzing edge list ", e)
            network = graph_gen_from_el(e + "_edgelist.csv")
            popular = read_popular_nodes(e + "_pnodes.csv")
            analyze(network, popular)
