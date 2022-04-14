##### Node Popularity Measures ######

# Rank each node in the graph induced by the provided edge list CSV according to multiple measures of popularity 

import sys
import time
import re
import csv
import pandas as pd
import networkx as nx
import multiprocessing as mp

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

# Find the core number for each node in the network
def corer(digraph, conn):
    t1 = time.time()
    cores = nx.core_number(digraph)    
    t2 = time.time()
    print("Core number took ", t2-t1, " seconds.")   
    conn.send(cores)
    conn.close()

# By default: "this is “left” eigenvector centrality which corresponds to the in-edges in the graph."
def evec(digraph, conn):
    t1 = time.time()
    eigens = nx.eigenvector_centrality(digraph)    
    t2 = time.time()
    print("Eigenvector centrality took ", t2-t1, " seconds.")  
    conn.send(eigens)
    conn.close()
    
# Find the page rank of each node
def pr(digraph, conn):
    t1 = time.time()
    pr = nx.pagerank(digraph)
    t2 = time.time()
    print("Page rank took ", t2-t1, " seconds.")  
    conn.send(pr)
    conn.close()

def popularity(digraph, out_file):
    core_parent, core_child = mp.Pipe()
    cores_proc = mp.Process(target=corer, args=(digraph,core_child,))
    cores_proc.start()

    e_parent, e_child = mp.Pipe()
    e_proc = mp.Process(target=evec, args=(digraph,e_child,))
    e_proc.start()

    pr_parent, pr_child = mp.Pipe()
    pr_proc = mp.Process(target=pr, args=(digraph,pr_child,))
    pr_proc.start()

    # In-degree of each node
    degrees = digraph.in_degree(digraph.nodes)
    cores = core_parent.recv()
    eigens = e_parent.recv()
    pranks = pr_parent.recv()
    cores_proc.join()
    e_proc.join()
    pr_proc.join()
    
    # Build nested dictionary keyed by nodeID
    pscores = {}
    for node in digraph.nodes:
        pscores[node] = {'core_number': None, 'eigenvector_centrality': None, 'in_degree': None, 'pagerank': None}
    for node, core in cores.items():
        pscores[node]['core_number'] = core
    for node, e in eigens.items():
        pscores[node]['eigenvector_centrality'] = e
    for node, pr in pranks.items():
        pscores[node]['pagerank'] = e
    for d in degrees:
        pscores[d[0]]['in_degree'] = d[1]

    # Write dictionary to CSV (unsorted)
    with open(out_file, "w") as f:
        columns = ['nodeID', 'core_number', 'eigenvector_centrality', 'in_degree', 'pagerank']
        writer = csv.DictWriter(f, columns)
        writer.writeheader()
        for key, val in pscores.items():
            row = {'nodeID': key}
            row.update(val)
            writer.writerow(row)

# Sorts nodes by core number, then tells each node's rank in the sorted degree and eigenvector lists
def ranker(pnodes, out_file):
    degree_only = pnodes[['in_degree']]
    degree_ranked = degree_only.sort_values(by='in_degree', ascending=False)
    series = [i+1 for i in range(len(degree_ranked.index))]
    degree_ranked = degree_ranked.assign(degree_rank=series)

    core_only = pnodes[['core_number']]
    core_ranked = core_only.sort_values(by='core_number', ascending=False)
    core_ranked = core_ranked.join(degree_ranked)

    eigen_only = pnodes[['eigenvector_centrality']]
    eigen_ranked = eigen_only.sort_values(by='eigenvector_centrality', ascending=False)
    series = [i+1 for i in range(len(eigen_ranked.index))]
    eigen_ranked = eigen_ranked.assign(eigen_rank=series)

    pr_only = pnodes[['pagerank']]
    pr_ranked = pr_only.sort_values(by='pagerank', ascending=False)
    series = [i+1 for i in range(len(pr_ranked.index))]
    pr_ranked = pr_ranked.assign(pr_rank=series)

    core_ranked = core_ranked.join(eigen_ranked)
    series = [i+1 for i in range(len(core_ranked.index))]
    core_ranked = core_ranked.assign(core_rank=series)#[['core_rank', 'degree_rank', 'eigen_rank']]
    core_ranked.to_csv(out_file)

if __name__=="__main__":
    el_path = sys.argv[1]
    network_name = el_path.split("_")[0]
    pop_path = "{}_popularity_measures.csv".format(network_name)
    network = graph_gen_from_el(el_path)
    popularity(network, pop_path)

    pnodes_df = pd.read_csv(pop_path, index_col='nodeID')
    ranked_df = ranker(pnodes_df, "{}_rankings.csv".format(network_name))


