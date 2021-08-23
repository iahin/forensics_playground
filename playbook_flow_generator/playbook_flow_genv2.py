import pandas as pd
import numpy as np
import random
from tqdm import tqdm
from pprint import pprint
from collections import Counter
from pyattck import Attck
import networkx as nx
from pyvis.network import Network
from itertools import product
import itertools
import matplotlib as plt

# Init pyatt lib
attck = Attck()


def filtermitre():
    tacticcolumns = []
    for tactic in attck.enterprise.tactics:
        templist = []
        for teachniques in tactic.techniques:
            if 'Windows' in teachniques.platforms:
                templist.append(teachniques.id)
        tacticcolumns.append((tactic.id, sorted(templist)))
    return tacticcolumns


def aptmatrix(tacticcolumns):
    # Gather and store edge pairs using n-gram(Works)
    edgelist = []

    for actor in attck.enterprise.actors:
        tempactorlist = []
        edge_i = [x.id for x in actor.techniques]

        for items in tacticcolumns:
            temptech = []
            for tech in edge_i:
                if tech in items[1]:
                    temptech.append(tech)
            if temptech:
                tempactorlist.append(temptech)
        edgelist.append(tempactorlist)
    return edgelist


def edgelist(edgelist):
    newedgelist = []
    sourcelist = []
    targetlist = []
    weightlist = []

    for x in edgelist:
        newedgelist.append(
            list(itertools.combinations(itertools.chain(*x), 2)))
    # User counter to count number of time edges appear to create weights
    newedgelist = [y for x in newedgelist for y in x]
    counter = Counter(sorted(newedgelist))

    for key, value in counter.items():
        sourcelist.append(key[0])
        targetlist.append(key[1])
        weightlist.append(value)

    # Store the nodes and weights in dataframe
    edges = pd.DataFrame(
        {
            "source": sourcelist,  # sourceId,
            "target": targetlist,  # targetlist
            "weight": weightlist
        }
    )

    # Create a graph using the dataframe
    G = nx.from_pandas_edgelist(
        edges, edge_attr=True, create_using=nx.DiGraph())
    return G


def generateFlow(G):
    dfstree = nx.dfs_tree(G, "T1030")
    return [list(x) for x in dfstree.edges()]


filteredapt = filtermitre()
aptmatrix = aptmatrix(filteredapt)
Graph = edgelist(aptmatrix)
flowlist = generateFlow(Graph)
print(flowlist)
