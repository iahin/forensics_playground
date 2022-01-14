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


def getTtpList(root_tactic):
    templist = []
    for tactic in attck.enterprise.tactics:
        if root_tactic in tactic.name:
            for teachniques in tactic.techniques:
                if 'Windows' in teachniques.platforms:
                    templist.append(teachniques.id)
    return templist


def filtermitre():
    # Filter to only have windows based TTPs
    tacticcolumns = []
    for tactic in attck.enterprise.tactics:
        templist = []
        for teachniques in tactic.techniques:
            if 'Windows' in teachniques.platforms:
                templist.append(teachniques.id)
        tacticcolumns.append((tactic.id, sorted(templist)))
    return tacticcolumns


def aptmatrix(tacticcolumns):
    # Matrix of TTPs of APT groups
    apt_list = []

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
        apt_list.append(tempactorlist)
    return apt_list


def paircounter(apt_list):
    newedgelist = []
    for x in apt_list:
        newedgelist.append(
            list(itertools.combinations(itertools.chain(*x), 2)))
    # User counter to count number of time edges appear to create weights
    newedgelist = [y for x in newedgelist for y in x]
    counter = Counter(sorted(newedgelist))

    return counter


def generate_graph(pair_counter):

    sourcelist = []
    targetlist = []
    weightlist = []

    for key, value in pair_counter.items():
        if value > 5:  # threshold to narrow down flow path
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

    edges = edges.sort_values('weight', ascending=False)

    # Create a graph using the dataframe
    G = nx.from_pandas_edgelist(
        edges, edge_attr=True, create_using=nx.DiGraph())
    return G


def generateFlow(G, node):
    visited = set()  # Set to keep track of visited nodes.
    result = []  # set()

    def dfs(visited, G, node):
        if node not in visited:
            visited.add(node)
            weightlist = [G[node][x]["weight"]
                          for x in G.neighbors(node) if x not in visited]
            maxweight = max(weightlist, default=0)
            maxweight_node = [x for x in G.neighbors(
                node) if G[node][x]["weight"] == maxweight]

            for node1 in maxweight_node:
                result.append((node, node1))
                dfs(visited, G, node1)
    dfs(visited, G, node)
    return result


filteredapt = filtermitre()
aptlist = aptmatrix(filteredapt)
counter = paircounter(aptlist)
graph = generate_graph(counter)

flowlist = generateFlow(graph, "T1020")
pprint(flowlist)
