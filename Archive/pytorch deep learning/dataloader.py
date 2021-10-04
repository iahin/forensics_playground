import torch
from torch_geometric.datasets import TUDataset
from torch_geometric.data import DataLoader


def datasetinfo(dataset):
    data = dataset[0]
    # Gather some statistics about the first graph.
    print(f'Number of nodes: {data.num_nodes}')
    print(f'Number of edges: {data.num_edges}')
    print(f'Average node degree: {data.num_edges / data.num_nodes:.2f}')
    print(f'Contains isolated nodes: {data.contains_isolated_nodes()}')
    print(f'Contains self-loops: {data.contains_self_loops()}')
    print(f'Is undirected: {data.is_undirected()}')


def datsetSplit(dataset):
    dataset = dataset.shuffle()
    train_dataset = dataset[:100]
    test_dataset = dataset[100:150]

    # print(f'Number of training graphs: {len(train_dataset)}')
    # print(f'Number of test graphs: {len(test_dataset)}')

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

    # for step, data in enumerate(train_loader):
    #     print(f'Step {step + 1}:')
    #     print('=======')
    #     print(f'Number of graphs in the current batch: {data.num_graphs}')
    #     print(data)
    #     print("Dasd", type(data.y))

    return train_loader, test_loader

# import torch
# import torchvision
# from torch.utils.data import Dataset, DataLoader
# import numpy as np
# import math
#
# class GraphDataset(Dataset):
#
#     def __init__(self):
#         xy = np.loadtxt('./data/testcsv', delimiter=",", dtype=np.float32, skiprows=1)
#         self.x = torch.from_numpy(xy[:, 1:])
#         self.y = torch.from_numpy(xy[:, [0]])
#         self.n_samples = xy.shape[0]
#
#     def __getitem__(self, index):
#         return self.x[index], self.y[index]
#
#     def __len__(self):
#         return  self.n_samples
#
#
# dataset = GraphDataset()
# dataloader = DataLoader(dataset=dataset, batch_size=4, shuffle=True, num_workers=2)
#
# dataiter = iter(dataloader)
# data = next(dataiter)
# feature, labels = data
# print(feature, labels)
