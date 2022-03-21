##### Known User Subgraph ########

import re
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

def graph_to_el(digraph, fname):
    df = pd.DataFrame(data=digraph.edges, columns=['source','target'])
    df.drop_duplicates(subset=['source', 'target'], keep='first', inplace=True)
    df.to_csv(fname, index = False)

# Input: A text file representing all users whose sentiment is known (path) and the complete network
# Output: Edge list CSVs representing the NetworkX subgraphs of Democratic, Republican, and known users within the complete network
def decompose(path, digraph, dataset):
    # Distinguish democrats, from republicans, from users who are neither (unknown) 
    users_df = generate_users(path)    
    democrats = set([u.id for _, u in users_df.iterrows() if float(u.polarity) < 0])
    republicans = set([u.id for _, u in users_df.iterrows() if float(u.polarity) >= 0])
    known_users = democrats.union(republicans)
    unknown = set([node for node in digraph.nodes if not node in known_users])
    print("Dem count: ", len(democrats), " | Rep count: ", len(republicans), " | Unknown count: ", len(unknown))

    # Partition the subgraph into dems, reps, dems+reps, complete \ dems, complete \ reps
    # Write subgraphs to file as edge list CSVs
    dem_part = digraph.subgraph(democrats)
    graph_to_el(dem_part, dataset + "/democrat_subgraph_edgelist.csv")

    rep_part = digraph.subgraph(republicans)
    graph_to_el(rep_part, dataset + "/republican_subgraph_edgelist.csv")

    known_part = digraph.subgraph(known_users)
    graph_to_el(known_part, dataset + "/knownusers_subgraph_edgelist.csv")

    no_dems = digraph.subgraph(unknown.union(republicans))
    graph_to_el(no_dems, dataset + "/no_dems_subgraph_edgelist.csv")

    no_reps = digraph.subgraph(unknown.union(democrats))
    graph_to_el(no_reps, dataset + "/no_reps_subgraph_edgelist.csv")

if __name__=="__main__":
    datasets = ['guncontrol', 'obamacare', 'abortion']
    for d in datasets:
        complete_network = graph_gen_from_el(d + "/" + d + "_edgelist.csv")
        decompose(d + "/" + "USER_POLARITY.txt", complete_network, d)