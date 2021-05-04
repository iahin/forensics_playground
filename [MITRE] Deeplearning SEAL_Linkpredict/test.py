import torch
from sklearn.metrics import roc_auc_score
from streamz.tests.test_graph import nx
from torch_geometric.data import DataLoader, Data

from SEALData import get_data, extrafeats
from SEALDataloader import SEALDataset

col1 = [0, 1, 2, 3, 4, 1, 2, 3, 4]
col2 = [0, 0, 0, 0, 0, 1, 1, 1, 1]

edge_index = torch.tensor([col1, col2])
edge_index = torch.cat([edge_index, edge_index.flip(0)], 1)  # undirected graph

edgelist = list(zip(*[col1, col2]))

graph = nx.Graph()
graph.add_edges_from(edgelist)
x = torch.tensor(extrafeats(graph))



dahhhta = Data(edge_index=edge_index, x=x)

dataloaddders = DataLoader(dahhhta, batch_size=2, shuffle=False)

@torch.no_grad()
def test(loader):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.manual_seed(0)
    model_path = ".\\model\\model.pth"
    model = torch.load(model_path)
    model.eval()

    y_pred, y_true = [], []
    for data in loader:
        data = data.to(device)
        logits = model(data.x, data.edge_index, data.batch)
        _, pred_index = torch.max(logits, 1)
        percentage = torch.nn.functional.softmax(logits, dim=1)[0] * 100
        print(data.y[pred_index[0]], percentage[pred_index[0]].item())


for data in dataloaddders:
