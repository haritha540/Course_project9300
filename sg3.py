##### Known User Subgraph ########

import re
import sys
from time import time
import pandas as pd
import networkx as nx

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

def subgraph_gen(network, users):
    sg = nx.DiGraph()
    for src, dest in network.edges:
        if (src in users or dest in users):
            sg.add_edge(src, dest)
    return sg

def graph_to_el(digraph, fname):
    df = pd.DataFrame(data=digraph.edges, columns=['source','target'])
    df.drop_duplicates(subset=['source', 'target'], keep='first', inplace=True)
    df.to_csv(fname, index = False)

# Input: A text file representing all users whose sentiment is known (path) and the complete network
# Output: Edge list CSVs representing the NetworkX subgraphs of Democratic, Republican, Known users
def decompose(userpath, digraph, dataset):
    # Distinguish democrats, from republicans, from users who are neither (unknown) 
    users_df = generate_users(userpath)    
    democrats = set([u.id for _, u in users_df.iterrows() if float(u.polarity) < 0])
    republicans = set([u.id for _, u in users_df.iterrows() if float(u.polarity) >= 0])
    known_users = democrats.union(republicans)
    unknown = set([node for node in digraph.nodes if not node in known_users])
    print("Dem count: ", len(democrats), " | Rep count: ", len(republicans), " | Unknown count: ", len(unknown))

    # Partition the graph into dems, reps and known
    # Write subgraphs to file as edge list CSVs
    t1 = time()
    dem_part = digraph.subgraph(democrats)
    graph_to_el(dem_part, dataset + "/democrat_subgraph_edgelist.csv")

    rep_part = digraph.subgraph(republicans)
    graph_to_el(rep_part, dataset + "/republican_subgraph_edgelist.csv")

    known_part = digraph.subgraph(known_users)
    graph_to_el(known_part, dataset + "/knownusers_subgraph_edgelist.csv")
    print("Took {} seconds".format(time() - t1))

#  Returns: Extended Democrat (all users who share an edge with a democrat), and
#           Extended Republican (all users who share an edge with a republican)
def subgraph_builder(complete_network, user_path, dataset):
    users_df = generate_users(user_path)
    democrats = set([u.id for _, u in users_df.iterrows() if float(u.polarity) < 0])
    d = democrats.pop()
    democrats.add(d)
    print("First dem is {}".format(d))
    republicans = set([u.id for _, u in users_df.iterrows() if float(u.polarity) >= 0])
    r = republicans.pop()
    republicans.add(r)
    print("First rep is {}".format(r))

    t1 = time()
    extended_democrat = subgraph_gen(complete_network, democrats)
    graph_to_el(extended_democrat, dataset + "/extdemocrat_subgraph_edgelist.csv")
    print("Took {} seconds".format(time() - t1))

    t2 = time()
    extended_republican = subgraph_gen(complete_network, republicans)
    graph_to_el(extended_republican, dataset + "/extrepublican_subgraph_edgelist.csv")
    print("Took {} seconds".format(time() - t2))

if __name__=="__main__":
    dataset = sys.argv[1]
    complete_network = graph_gen_from_el(dataset + "/complete_subgraph_edgelist.csv")
    #complete_network = graph_gen_from_el(dataset + "/short_edgelist.csv")
    decompose(dataset + "/" + "USER_POLARITY.txt", complete_network, dataset)
    #subgraph_builder(dataset + "/FULL_FOLLOWER_NETWORK.txt", dataset + "/FULL_FRIEND_NETWORK.txt", dataset + "/" + "USER_POLARITY.txt", dataset)
    subgraph_builder(complete_network, dataset + "/" + "USER_POLARITY.txt", dataset)
