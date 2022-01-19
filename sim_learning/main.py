import argparse

import torch
from torch import optim
from torch import nn

import dataset
from model import SCNN
from train import predict, retrain, train, eval
from utils import getpredictionscore

import streamlit as st
import numpy as np
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('-use_saved_dataset', type=bool, default=True)
parser.add_argument('-use_pretrain_model', type=bool, default=False)
parser.add_argument('-model_path', type=str, default="./data/model.pt")

args = parser.parse_args()
if args.use_saved_dataset:
    train_sample, new_sample, test_sample = dataset.getsavedsample(1)
else:
    print("TODO")

if args.use_pretrain_model:
    model = torch.load(args.model_path)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.BCELoss()
else:
    model = SCNN(embedding_dim=32, hidden_size=16, output_size=2)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.BCELoss()

# Standardise datapoints
train_sample = dataset.data_std(train_sample)
test_sample = dataset.data_std(test_sample)
new_sample = dataset.data_std(new_sample)

# Declare train and validation loader
train_loader, validation_loader = dataset.train_sampler(train_sample)

# Train model
train(train_loader, model, loss_fn, optimizer, args.model_path)

# Eval with bast test
test_loader = dataset.test_sampler(test_sample)
gt, pred = eval(test_loader, validation_loader, model)
getpredictionscore(gt, pred)

# Predict 2 incorrect samples
print("_________________Prediction BEFORE retraining______________")
y_pred, similarity_score = predict(new_sample[9][0], validation_loader, model)
print("predicted:", y_pred, "actual:", int(new_sample[9][1]), str(
    similarity_score[1]/sum(similarity_score.values()) * 100))

y_pred, similarity_score = predict(new_sample[10][0], validation_loader, model)
print("predicted:", y_pred, "actual:", int(new_sample[10][1]), str(
    similarity_score[1]/sum(similarity_score.values()) * 100))

y_pred, similarity_score = predict(new_sample[11][0], validation_loader, model)
print("predicted:", y_pred, "actual:", int(new_sample[11][1]), str(
    similarity_score[1]/sum(similarity_score.values()) * 100))


# debug purpose
# for i, x in enumerate(new_sample):
#     y_pred, similarity_score = predict(
#         x[0], validation_loader, model)
#     print("index:", i, "predicted:", y_pred, "actual:", int(x[1]))

# relabel sample and concate to training
relabled_sample = [[new_sample[9][0], new_sample[9][1]],
                   [new_sample[10][0], new_sample[10][1]]]
combine_sample = train_sample + relabled_sample

# load again to train sample for retrain
train_loader, validation_loader = dataset.train_sampler(combine_sample)

# retrain
retrain(train_loader, model, loss_fn, optimizer, args.model_path)

# Eval with base test data dnd early predicted correction
test_loader = dataset.test_sampler(test_sample)
gt, pred = eval(test_loader, validation_loader, model)
getpredictionscore(gt, pred)

print("_________________Prediction AFTER retraining______________")
y_pred, similarity_score = predict(new_sample[9][0], validation_loader, model)
print("predicted:", y_pred, "actual:", int(new_sample[9][1]), str(
    similarity_score[1]/sum(similarity_score.values()) * 100))

y_pred, similarity_score = predict(new_sample[10][0], validation_loader, model)
print("predicted:", y_pred, "actual:", int(new_sample[10][1]), str(
    similarity_score[1]/sum(similarity_score.values()) * 100))

y_pred, similarity_score = predict(new_sample[11][0], validation_loader, model)
print("predicted:", y_pred, "actual:", int(new_sample[11][1]), str(
    similarity_score[1]/sum(similarity_score.values()) * 100))


"""
* TEST UI
"""
# st.title('SLADE Cybercrime Prediction')
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# d = st.selectbox(
#     'Select caseid',
#     ('spf1', 'spf2', 'spf3', 'spf4'))

# # Predict new data(for production)
# test_loader = next(x for i, x in enumerate(test_loader) if i ==
#                    int(''.join(i for i in d if i.isdigit())))

# st.write('Click to begin')

# if st.button('Start'):
#     y_pred, similarity_score = predict(test_loader, validation_loader, model)
#     if y_pred == 0:
#         st.write("Crime predicted: Unauthorised Access")
#         st.write("Prediction Score: " +
#                  str(similarity_score[0]/sum(similarity_score.values()) * 100))
#     if y_pred == 1:
#         st.write("Crime predicted: Data Theft")
#         st.write("Prediction Score: " +
#                  str(similarity_score[1]/sum(similarity_score.values()) * 100))
#     if y_pred == 2:
#         st.write("Crime predicted: Unknown")

# st.text("")

# st.text("Confirm Prediction?")
# if st.button('Yes'):
#     st.text("Prediction label confirmed. Added to database.")

# if st.button('No'):
#     option = st.selectbox('Please select the correct label for this case.',
#                           ('Unauthorised Access', 'Data Theft'))
