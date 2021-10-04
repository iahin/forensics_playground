"""
REFERENCE: https://pytorch-geometric.readthedocs.io/en/latest/notes/colabs.html
"""
import torch
from torch_geometric.datasets import TUDataset

from server.rle.GCN import GCN, gcn
from server.rle.GNN import GNN, gnn
from server.rle.dataloader import datsetSplit
from server.rle.train_test import train, test

dataset = TUDataset(root='data/TUDataset', name='MUTAG')
train_loader, test_loader = datsetSplit(dataset)

torch.manual_seed(0)
model_path = ".\\model.pth"
model = gnn()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.CrossEntropyLoss()

for epoch in range(1, 201):
    train(model, optimizer, criterion, train_loader)
    train_acc = test(model, train_loader)
    test_acc = test(model, test_loader)
    print(f'Epoch: {epoch:03d}, Train Acc: {train_acc:.4f}, Test Acc: {test_acc:.4f}')

torch.save(model, model_path)
# model = torch.load(model_path)
