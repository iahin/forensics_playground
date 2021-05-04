# Karate Lib https://karateclub.readthedocs.io/en/latest/index.html

import random
import os.path as osp
import numpy as np
from networkx import to_edgelist
from karateclub import Node2Vec

import torch
from torch_geometric.data import Data
import networkx as nx

from pyattck import Attck
import networkx as nx
from collections import Counter


def networkGraph():
    attck = Attck()
    edges = []

    for actor in attck.enterprise.actors:
        edge_i = [x.id for x in actor.techniques]
        edge_j = [x.id for x in actor.techniques]
        for technique_i in edge_i:
            for technique_j in edge_j:
                if technique_j != technique_i:
                    edges.append((technique_i, technique_j))


def get_graph():
    path = osp.join(osp.dirname(osp.realpath(__file__)),
                    '.', 'data', "ia-crime-moreno.edges")

    preprocessedList = []
    with open(path, "r") as file:
        templist = file.readlines()
        templist = templist[2:]
        templist = [(int(x.split(' ')[0]) - 1, int(x.split(' ')[1]) - 1)
                    for x in templist]
        preprocessedList = templist

    edgelist = list(zip(*preprocessedList))
    col1 = list(edgelist[0])
    col2 = list(edgelist[1])

    graph = nx.Graph()
    graph.add_edges_from(preprocessedList)

    return col1, col2, graph


def extrafeats(graph, dim=128):
    model = Node2Vec(p=1, q=1, dimensions=dim)
    model.fit(graph)
    return model.get_embedding()


def get_data():
    col1, col2, graph = get_graph()

    edge_index = torch.tensor([col1, col2])
    edge_index = torch.cat(
        [edge_index, edge_index.flip(0)], 1)  # undirected graph

    edge_len = len(edge_index[0].unique())

    x = torch.tensor(extrafeats(graph))

    # train, test, val masks for each node
    train_mask = torch.tensor([True] * round(edge_len * 0.8) +
                              [False] * (edge_len - round(edge_len * 0.8)))
    test_mask = torch.tensor([False] * round(edge_len * 0.8) +
                             [True] * (round(edge_len * 0.1)) +
                             [False] * (edge_len - round(edge_len * 0.8)
                                        - round(edge_len * 0.1)))
    val_mask = torch.tensor([False] * round(edge_len * 0.8) +
                            [False] * (round(edge_len * 0.1)) +
                            [True] * (edge_len - round(edge_len * 0.8)
                                      - round(edge_len * 0.1)))

    new_data = Data(edge_index=edge_index,
                    x=x,
                    train_mask=train_mask,
                    val_mask=val_mask,
                    test_mask=test_mask)

    return new_data
