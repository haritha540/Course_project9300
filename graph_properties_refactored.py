import csv
import pandas as pd
import networkx as nx

class Node:
    def __init__(self, id, inN, outN):
        self.id = id
        self.in_neigh = inN
        self.out_neigh = outN
        self.reciprocals = set()        # Nodes with whom you share a reciprocal edge
        self.in_degree = None
        self.out_degree = None
        self.tc = None
        self.triadic_motif_count = None
        self.dcc = None

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
    # Check for false triangle (PG 5, https://arxiv.org/pdf/physics/0612169.pdf)
    def naive_triangle_count(self, digraph, graph):
        try:
            triangle_count = 0                          # Total number of undirected triangles node is connected to
            motif_count = 0                             # Total number of 3F & 3G triangles node is connected to
            for i in graph[self.id].out_neigh:                  
                for j in graph[i].out_neigh:          
                    for k in graph[j].out_neigh:
                        if self.id == k:              # Triangle found - node is connected to an undirected triangle
                            triangle_count += 1
                            if triadic_motif(self.id, i, j, digraph):
                                motif_count += 1
            self.tc = triangle_count / 2
            self.triadic_motif_count = motif_count / 2
        except:
            print("Could not calculate triadic motifs for node ", self.id)

    def printer(self):
        print("Node ID: ", self.id)
        print("\tIn-degree: ", self.in_degree, " | Out-degree:", self.out_degree)
        print("\tDirected Clustering Coefficient: ", self.dcc)
        #print("\tOutgoing Neighbors: ", self.out_neigh)
        #print("\tIncoming Neighbors: ", self.in_neigh)
        print("\t\tMotif 2D Count: ", self.reciprocal_edge_count())
        print("\t\tMotif 2A Count: ", self.nonreciprocal_edge_count())
        print("\t\t\tUndirected Triangle Count: ", self.tc)
        print("\t\t\tTriadic Motif Count: ", self.triadic_motif_count)
        return((self.id, self.in_degree, self.out_degree, self.reciprocal_edge_count(), self.nonreciprocal_edge_count(), self.tc, self.triadic_motif_count, self.dcc))


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


# Followees of a node are outgoing edges
# For each followee F of node N, add an edge (N,F) to graph
def followees_of_node(N):
    el = []
    if isinstance(N.friends, str):
        friends = N.friends.strip("[").strip("]")
        friends_array = friends.split(",")
        for f in friends_array:
            el.append((N.user_name,f))
    else:
        print("Invalid friends list for node ", N.user_name)
    return el

# Followers of a node are incoming edges to the node
# For each follower F of node N, add an edge (F,N)
def followers_of_node(N):
    el = []
    if isinstance(N.follwers, str):
        followers = N.follwers.strip("[").strip("]")
        followers_array = followers.split(",")
        for f in followers_array:
            el.append((f, N.user_name))
    else:
        print("Invalid followers list for node ", N.user_name)
    return el

# Provided a path to a CSV produced by data scraper
# Returns a NetworkX digraph and an undirected graph
def graph_gen_from_file(path):
    graph = nx.Graph()
    digraph = nx.DiGraph()
    df = pd.read_csv(path, index_col='user_id')
    for _, node in df.iterrows():
        try:
            friends = followees_of_node(node)
            graph.add_edges_from(friends)
            digraph.add_edges_from(friends)
        except:
            print("Could not process friends of node ", node.user_name)
        try:
            followers = followers_of_node(node)
            graph.add_edges_from(followers)
            digraph.add_edges_from(followers)
        except:
            print("Could not process followers of node ", node.user_name)
    return digraph, graph

# Maps the sentiment of a node to [-1,1] (could use tanh)
# Should only run this function on the unique set of nodes, but the df
# passed as a parameter should include the entire tweet list
def sentiment_calculator(N, df):
    df_N = df[df.user_name == N.user_name]
    aggregate = 0
    tweet_count = 0
    for n in df_N.itertuples():
        tweet_count += 1
        if n.Sentiment == 'positive':
            aggregate += 1
        elif n.Sentiment == 'negative':
            aggregate -= 1
        elif n.Sentiment == 'neutral':
            aggregate += 0
        else:
            print("Undefined sentiment!")
    numeric_sentiment = aggregate / tweet_count
    if numeric_sentiment > 0:
        class_sentiment = 'positive'
    else:
        class_sentiment = 'negative'
    user = {'id': N.Label, 'sentiment_numeric': numeric_sentiment, 'sentiment_class': class_sentiment}
    return user

# Create a datframe of users from a path to a tweet file
# Calculates the user sentiment as an aggregation of tweet sentiments
def generate_users(path):
    users = []
    tweets = tweets = pd.read_csv(filepath=path, index_col='user_id')
    unique_users = tweets.drop_duplicates(subset=['user_name'], keep='first', inplace=False)        # Label or ID?
    for n in unique_users.itertuples():
        users.append(sentiment_calculator(n, tweets))
    users_df = pd.DataFrame(data=users, columns=['user_id', 'sentiment_numeric', 'sentiment_class'])
    users_df.to_csv("user_sentiments.csv", index = False)

# Convert graphs into GAPBS-like format for triangle counting
# nodeIDs and edges must be sets of UNIQUE nodes and edges
def gapbs_converter(nodeIDs, edges):
    # Assemble a dictionary of Nodes keyed by their user ID
    graph = {}
    digraph = {}
    for n in nodeIDs:
        digraph[n] = Node(n, set(), set())
    # Iterate through edge list to populate Node neighborhoods and degrees
    for src, dest in edges:
        digraph[src].out_neigh.add(dest)
        digraph[dest].in_neigh.add(src)
    # Sort neighborhoods by node id
    for _, node in digraph.items():
        node.finalize()
    # Convert to undirected graph
    for id, node in digraph.items():
        neighbors = (set(node.out_neigh)).union(set(node.in_neigh))
        graph[id] = Node(id, neighbors, neighbors)
        graph[id].finalize()
    # Count 3D motifs
    for _, node in digraph.items():
        node.naive_triangle_count(digraph, graph)
    # Print complete node information
    #for _, node in graph.items():
    #    node.printer()
    return digraph

# (either cores or degree or something similar)
# https://arxiv.org/pdf/cs/0310049.pdf
# https://networkx.org/documentation/stable/reference/algorithms/core.html
def popularity(digraph):
    nodes = []
    nodes.append(digraph[0]) 
    nodes.append(digraph[1])
    return nodes

if __name__=="__main__":
    # Generate NetworkX format graphs
    dgX, gX = graph_gen_from_file('validusers_friendslist1.csv')
    # Generate GAPBS format digraph with 2 & 3D motif information for each node
    dgGAP = gapbs_converter(dgX.nodes, dgX.edges)
    # Find popular nodes 
    popular_nodes = ['Abbas', 'Abdul']#popularity(dgX)
    # Calculate directed clustering coefficients
    coeffs = nx.clustering(dgX, popular_nodes)
    for node, cf in coeffs.items():
        dgGAP[node].dcc = cf
    # Print node statistics to file and stdout
    fields = ['user_id', 'in-degree', 'out-degree', 
                'reciprocal_count', 'nonreciprocal_count',
                'triangle_count', 'triads', 'clustering']
    with open('metadata.csv', 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(fields)
        for p in popular_nodes:
            row = dgGAP[p].printer()
            csvwriter.writerow(row)