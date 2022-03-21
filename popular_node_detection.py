##### Popular Node Detection ######

# Find the 30 most popular nodes in the graph induced by each edge list CSV, ranked by core number

import re
import csv
import pandas as pd
import networkx as nx
import networkx.algorithms.community as comm

# Read in users with known political leanings from path
def generate_users(path):
    users = []
    with open(path, "r") as f:
        lines = f.readlines()
        for l in lines:
            try:
                users.append(tuple(re.split('[\t *]', l.strip())))
            except:
                print("Failure on user ", l)
    users_df = pd.DataFrame(data=users, columns=['id','polarity'])
    return users_df

# Given a path to a src/target edge list CSV
# Returns a NetworkX digraph
def graph_gen_from_el(path):
    digraph = nx.DiGraph()
    df = pd.read_csv(path, dtype={'source': str, 'target': str})
    for _, edge in df.iterrows():
        digraph.add_edge(edge.source, edge.target)
    return digraph

def popularity(digraph):
    # Find the core number for each node in the network
    cores = nx.core_number(digraph)           
     # Find the N most popular nodes (max core number)                      
    most_popular = sorted(cores.items(), key=lambda x: x[1], reverse=True)
    return most_popular

def filter_by_userlist(democrats, republicans, el_path):
    dems = []
    reps = []
    popular_node_tuples = popularity(graph_gen_from_el(el_path))
    dem_count, rep_count = 0, 0
    for i in range(len(popular_node_tuples)):
        node_pair = popular_node_tuples[i]
        if node_pair[0] in democrats:
            if dem_count < 30:
                dems.append(node_pair)
                dem_count += 1
        if node_pair[0] in republicans:
            if rep_count < 30:
                reps.append(node_pair)
                rep_count += 1
        if dem_count >= 30 and rep_count >= 30:
            break
    with open("democratic_nodes.txt", "w") as f1:
        for d in dems:
            f1.writeline(d[0])
    with open("republican_nodes.txt", "w") as f2:
        for d in reps:
            f2.writeline(d[0])
    print("Democratic nodes: ", dems)
    print("Republican nodes: ", reps)

if __name__=="__main__":
    dataset = ['guncontrol', 'obamacare', 'abortion']
    for d in dataset:
        print("######### Popular Nodes in Dataset: ", d, " #########\n")
        edge_lists = ["/democrat_subgraph", "/republican_subgraph", "/no_dems_subgraph", "/no_reps_subgraph"]
        for e in edge_lists:
            el = e + "_edgelist.csv"
            node_path = e + "_pnodes.csv"
            network = graph_gen_from_el(el)
            popular_node_tuples = popularity(network)
            print("\t\tPopular node tuples for ", d+e, ": ", popular_node_tuples[0:30])
            with open(node_path, "w") as f:
                for p in popular_node_tuples[0:30]:
                    f.writeline(p[0])       
        users = generate_users(d + "/USER_POLARITY.txt")  
        democrats = set([u.id for _, u in users.iterrows() if float(u.polarity) < 0])
        republicans = set([u.id for _, u in users.iterrows() if float(u.polarity) >= 0])
        filter_by_userlist(democrats, republicans, "/" + d + "_edgelist.csv")
        filter_by_userlist(democrats, republicans, "/knownusers_subgraph_edgelist.csv")
