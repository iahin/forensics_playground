from inspect import FrameInfo
from re import X
import torch
from torch_geometric.datasets import TUDataset
from torch_geometric.utils import convert
import numpy as np
import networkx as nx
from sklearn.model_selection import train_test_split
from karateclub import Graph2Vec, DeepWalk, GL2Vec, FGSD, FeatherGraph
from sklearn.preprocessing import StandardScaler
import torch.nn.functional as F
import random
import scipy.sparse as sp

datalist = None

scaler = StandardScaler()


def getembedding(graphlist, dim=32):
    model = Graph2Vec(dimensions=dim)
    model.fit(graphlist)
    embedlist = model.get_embedding()

    return embedlist


def gatherdata(dataset_loader):
    graphlist = [(convert.to_networkx(x).to_directed(),
                  y) for x, y in dataset_loader]

    return graphlist


def gettrainsample(size=5, filename=''):

    collect_bag = []
    get_unique_class = np.tile(np.unique([y for x, y in datalist]), size)
    #get_unique_class = [random.randint(0, 1) for _ in range(size)]
    for unique_y in get_unique_class:
        for i, (x, y) in enumerate(datalist):
            if y == unique_y:
                collect_bag.append((x, y))
                datalist.pop(i)
                break

    X_list = getembedding([x for x, y in collect_bag])
    y_list = [y for x, y in collect_bag]
    graph_list = [x for x, y in collect_bag]

    outlist = [(x, y, graph_list)
               for x, y, graph_list in zip(X_list, y_list, graph_list)]
    with open('data\\'+filename+'.npy', 'wb') as f:
        np.save(f, outlist)
    print(len(datalist))


protein_data = TUDataset(
    r'C:\Users\16sic\Documents\GitHub\conference_draft\src\\data\\', r'PROTEINS')
protein_data = protein_data.shuffle()
protein_data = [(data, data.y.item()) for data in protein_data]

imdb_data = TUDataset(
    r'C:\Users\16sic\Documents\GitHub\conference_draft\src\\data\\', r'IMDB-BINARY')
imdb_data = imdb_data.shuffle()
imdb_data = [(data, data.y.item()) for data in imdb_data]

reddit_data = TUDataset(
    r'C:\Users\16sic\Documents\GitHub\conference_draft\src\\data\\', r'REDDIT-BINARY')
reddit_data = reddit_data.shuffle()
reddit_data = [(data, data.y.item()) for data in reddit_data]
"""
* For classification
* 4 sample from known class(balanced), 2 sample from unknown class(balanced)
* 8 additional sample divided into 4 by 4 parts for active learning
"""


# datalist = gatherdata(protein_data)
# dataname = 'PROTEINS_graph2vec'
# gettrainsample(size=4, filename=dataname+'_classification_train1')
# gettrainsample(size=6, filename=dataname+'_classification_train2')
# gettrainsample(size=8, filename=dataname+'_classification_train3')
# gettrainsample(size=5, filename=dataname+'_classification_test')

# datalist = gatherdata(imdb_data)
# dataname = 'IMDB-BINARY_graph2vec'
# gettrainsample(size=4, filename=dataname+'_classification_train1')
# gettrainsample(size=6, filename=dataname+'_classification_train2')
# gettrainsample(size=8, filename=dataname+'_classification_train3')
# gettrainsample(size=5, filename=dataname+'_classification_test')

# datalist = gatherdata(reddit_data)
# dataname = 'REDDIT-BINARY_graph2vec'
# gettrainsample(size=4, filename=dataname+'_classification_train1')
# gettrainsample(size=6, filename=dataname+'_classification_train2')
# gettrainsample(size=8, filename=dataname+'_classification_train3')
# gettrainsample(size=5, filename=dataname+'_classification_test')

"""
* For novelty detection
* 10 sample from known class, 4 sample from unknown class, without replacement
* for contimination of 0.25 - 0.3 (14/4)    
"""

# imdb_data_temp = []
# for x, y in imdb_data:
#     if y == 0:
#         imdb_data_temp.append((x, 2))
#     if y == 1:
#         imdb_data_temp.append((x, 3))

# reddit_data_temp = []
# for x, y in reddit_data:
#     if y == 0:
#         reddit_data_temp.append((x, 2))
#     if y == 1:
#         reddit_data_temp.append((x, 3))

# datalist = gatherdata(protein_data)
# gettrainsample(size=10, filename='novelty_train')
# datalist = gatherdata(reddit_data_temp)
# gettrainsample(size=5, filename='novelty_test')

"""
NEWEWEW    
"""
# TODO: create new dataset for new dataset prediction
