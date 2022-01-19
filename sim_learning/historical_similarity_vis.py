""" 
Based on https://stackoverflow.com/questions/61421491/similarity-measure-between-graphs-using-networkx
"""
import argparse
import networkx as nx
from matplotlib import pyplot as plt
import dataset

parser = argparse.ArgumentParser()
parser.add_argument('-use_saved_dataset', type=bool, default=True)
parser.add_argument('-use_pretrain_model', type=bool, default=False)
parser.add_argument('-model_path', type=str, default="./data/model.pt")

args = parser.parse_args()
if args.use_saved_dataset:
    train_sample, new_sample, test_sample = dataset.getsavedsample(1)
else:
    print("TODO")

G = train_sample[0][2]
H = new_sample[3][2]

GH = nx.compose(G, H)

# set edge colors
edge_colors = dict()
for edge in GH.edges():
    if G.has_edge(*edge):
        if H.has_edge(*edge):
            edge_colors[edge] = 'magenta'
            continue
        edge_colors[edge] = 'lightgreen'
    elif H.has_edge(*edge):
        edge_colors[edge] = 'lightblue'

# set node colors
G_nodes = set(G.nodes())
H_nodes = set(H.nodes())
node_colors = []
for node in GH.nodes():
    if node in G_nodes:
        if node in H_nodes:
            node_colors.append('magenta')
            continue
        node_colors.append('lightgreen')
    if node in H_nodes:
        node_colors.append('lightblue')

pos = nx.spring_layout(GH, scale=20)
nx.draw(GH, pos,
        nodelist=GH.nodes(),
        node_color=node_colors,
        edgelist=edge_colors.keys(),
        edge_color=edge_colors.values(),
        node_size=400,
        width=4, alpha=0.5,
        with_labels=True)
plt.show()
