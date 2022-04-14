import re
import pandas as pd

edges = []
with open("FULL_FOLLOWER_NETWORK.txt", "r") as incoming:
#with open("follow_short.txt", "r") as incoming:
    lines = incoming.readlines()
    for l in lines:
        try:
            src_dest = re.split('[\t *]', l.strip())
            src = src_dest[0]
            dest = src_dest[1]
            edges.append((src,dest))
        except:
            print("Failed on line:\n\t{}".format(l))

with open("FULL_FRIEND_NETWORK.txt", "r") as outgoing:
#with open("friend_short.txt", "r") as outgoing:
    lines = outgoing.readlines()
    for l in lines:
        try:
            src_dest = re.split('[\t *]', l.strip())
            src = src_dest[1]
            dest = src_dest[0]
            edges.append((src,dest))
        except:
            print("Failed on line:\n\t{}".format(l))

el_df = pd.DataFrame(data=edges, columns=['source','target'])
el_df.drop_duplicates(subset=['source', 'target'], keep='first', inplace=True)
el_df.to_csv("complete_subgraph_edgelist.csv", index = False)
