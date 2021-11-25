import numpy as np
import torch
from karateclub import Graph2Vec
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from sklearn.preprocessing import StandardScaler


def getembedding(graphlist, dim=32):
    model = Graph2Vec(dimensions=dim)
    model.fit(graphlist)
    embedlist = model.get_embedding()

    return embedlist


def getsavedsample(dataset_option):
    datasetname = ""
    if dataset_option == 1:
        datasetname = "PROTEINS_graph2vec"
    if dataset_option == 2:
        datasetname = "IMDB-BINARY_graph2vec"
    if dataset_option == 3:
        datasetname = "REDDIT-BINARY_graph2vec"

    with open('data\\' + datasetname + '_classification_train1.npy', 'rb') as f:
        train1 = np.load(f, allow_pickle=True)
    with open('data\\' + datasetname + '_classification_train2.npy', 'rb') as f:
        train2 = np.load(f, allow_pickle=True)
    with open('data\\' + datasetname + '_classification_train3.npy', 'rb') as f:
        train3 = np.load(f, allow_pickle=True)
    with open('data\\' + datasetname + '_classification_test.npy', 'rb') as f:
        test = np.load(f, allow_pickle=True)

    return train1, train2, train3, test


def data_std(dataset):
    scaler = StandardScaler()

    X_data = [x for x, y, g in dataset]
    scaler_model = scaler.fit(X_data)
    X_data = scaler_model.transform(X_data)
    X_data = [[np.expand_dims(x, 0)] for x in X_data]
    X_data = torch.Tensor(X_data)

    y_data = [y for x, y, g in dataset]
    y_data = torch.Tensor(y_data)

    result = list(zip(X_data, y_data))
    return result


def train_sampler(dataset):
    pair_sample = []
    for img1, y1 in dataset:
        for img2, y2 in dataset:
            if y1 == y2:
                # label 0,1 = 1 if pairs are same
                pair_sample.append((img1, img2, torch.Tensor([0, 1])))
            if y1 != y2:
                # label 1,0 = 0 if pairs are not same
                pair_sample.append((img1, img2, torch.Tensor([1, 0])))

    pair_sample_data = [Data(
        img1=img1,
        img2=img2,
        y=y)
        for img1, img2, y in pair_sample
    ]
    train_loader = DataLoader(pair_sample_data, batch_size=1, shuffle=False)

    # validation loader is to do validation on train data with test data since train data cannot be used
    validation_list = [Data(x=x, y=y) for x, y in dataset]
    validation_loader = DataLoader(validation_list, batch_size=1, shuffle=False)

    return train_loader, validation_loader


def test_sampler(dataset):
    test_list = [Data(x=x, y=y) for x, y in dataset]
    test_loader = DataLoader(test_list, batch_size=1, shuffle=False)

    return test_loader
