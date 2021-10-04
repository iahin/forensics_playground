import torch
from torch.nn import Linear
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GraphConv
from torch_geometric.nn import global_mean_pool


class GNN(torch.nn.Module):
    def __init__(self, nfeat, nclass, nhid):
        super(GNN, self).__init__()
        torch.manual_seed(12345)
        self.conv1 = GraphConv(nfeat, nhid)
        self.conv2 = GraphConv(nhid, nhid)
        self.conv3 = GraphConv(nhid, nhid)
        self.lin = Linear(nhid, nclass)

    def forward(self, x, edge_index, batch):
        # 1. Obtain node embeddings
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        x = x.relu()
        x = self.conv3(x, edge_index)

        # 2. Readout layer
        x = global_mean_pool(x, batch)  # [batch_size, hidden_channels]

        # 3. Apply a final classifier
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin(x)

        return x


def gnn(nfeat=7, nclass=2, nhid=64):
    model = GNN(nfeat=nfeat, nclass=nclass, nhid=nhid)
    return model
