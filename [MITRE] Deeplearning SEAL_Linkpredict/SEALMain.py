# Paper: Link Prediction Based on Graph Neural Networks (NeurIPS 2018)
from SEALData import get_data
from torch_geometric.datasets import Planetoid
import os.path as osp
from SEALData import get_data
from DGCNN import DGCNN
from SEALDataloader import SEALDataset

from sklearn.metrics import roc_auc_score

import torch
from torch.nn import BCEWithLogitsLoss
from torch_geometric.data import Data, DataLoader

torch.manual_seed(0)
model_path = ".\\model\\model.pth"


def train(model):
    optimizer = torch.optim.Adam(params=model.parameters(), lr=0.0001)
    model.train()

    total_loss = 0
    for data in train_loader:
        data = data.to(device)
        optimizer.zero_grad()
        logits = model(data.x, data.edge_index, data.batch)
        loss = BCEWithLogitsLoss()(logits.view(-1), data.y.to(torch.float))
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * data.num_graphs

    torch.save(model, model_path)
    return total_loss / len(train_dataset)


@torch.no_grad()
def test(loader):
    model = torch.load(model_path)
    model.eval()

    y_pred, y_true = [], []
    for data in loader:
        data = data.to(device)
        logits = model(data.x, data.edge_index, data.batch)
        y_pred.append(logits.view(-1).cpu())
        y_true.append(data.y.view(-1).cpu().to(torch.float))

    return roc_auc_score(torch.cat(y_true), torch.cat(y_pred))


dataset = get_data()

# path = osp.join(osp.dirname(osp.realpath(__file__)), '..', 'uuhu', 'Planetoid')
# dataset = Planetoid(path, 'Cora')
# print(len(dataset[0].edge_index[0]))

train_dataset = SEALDataset(dataset, num_hops=2, split='train')
val_dataset = SEALDataset(dataset, num_hops=2, split='val')
test_dataset = SEALDataset(dataset, num_hops=2, split='test')

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32)
test_loader = DataLoader(test_dataset, batch_size=32)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
num_nodes = sorted([data.num_nodes for data in train_dataset])
dim = train_dataset.num_features
model = DGCNN(num_nodes, dim, hidden_channels=32, num_layers=3).to(device)

best_val_auc = test_auc = 0
epoc = 50

for epoch in range(1, epoc):
    loss = train(model)
    val_auc = test(val_loader)
    if val_auc > best_val_auc:
        best_val_auc = val_auc
        test_auc = test(test_loader)
    print(f'Epoch: {epoch:02d}, Loss: {loss:.4f}, Val: {val_auc:.4f}, '
          f'Test: {test_auc:.4f}')
