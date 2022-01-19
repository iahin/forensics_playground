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

G = train_sample[4][2]
G.remove_edges_from(nx.selfloop_edges(G))

pos = nx.spring_layout(G, scale=20)
nx.draw(G, pos,
        nodelist=G.nodes(),
        node_size=200,
        width=2, alpha=0.5,
        with_labels=False)
plt.show()
