import argparse

import torch
from torch import optim
from torch import nn

import dataset
from model import SCNN
from train import train, eval
from utils import getpredictionscore

parser = argparse.ArgumentParser()
parser.add_argument('-use_saved_dataset', type=bool, default=True)
parser.add_argument('-use_pretrain_model', type=bool, default=False)
parser.add_argument('-model_path', type=str, default="./data/model.pt")

args = parser.parse_args()
if args.use_saved_dataset:
    train1, train2, train3, test = dataset.getsavedsample(1)
else:
    print("TODO")

if args.use_pretrain_model:
    print("TODO")
else:
    model = SCNN(embedding_dim=32, hidden_size=16, output_size=2)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.BCELoss()

# Load train data
train_dataset = dataset.data_std(train1)
train_loader, validataion_loader = dataset.train_sampler(train_dataset)

# Load test data
test_dataset = dataset.data_std(test)
test_loader = dataset.test_sampler(test_dataset)

# Train model
train(train_loader, model, loss_fn, optimizer)

# Eval model
gt, pred = eval(test_loader, validataion_loader, model)
getpredictionscore(gt, pred)

# Predict new data(for production)
## TODO

# Retrain model
## TODO: Combine initial traindata with new labelled data
# dataiter2 = train1 + train2
# train_dataset = dataset.data_std(dataiter2)
#
# train_loader, validataion_loader = dataset.train_sampler(train_dataset)
# train(train_loader, model, loss_fn, optimizer)