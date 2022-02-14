from collections import defaultdict

import numpy as np
import torch


def train(train_loader, model, loss_fn, optimizer, savepath):
    for epoch in range(0, 100):
        model.train()
        train_losses = []
        for data in train_loader:
            img1 = data.img1
            img2 = data.img2
            y = data.y.unsqueeze(0)

            out = model(img1, img2)
            loss = loss_fn(out, y)

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            train_losses.append(loss.item())

        if epoch % 10 == 0:
            print("Epoch number {}\n Current loss {}\n".format(epoch, loss.item()))

    torch.save(model, savepath)


def eval(test_loader, validation_loader, model):
    gt = []
    pred = []
    with torch.no_grad():
        model.eval()
        for test_data in test_loader:
            similarity_score = defaultdict(list)
            for val_data in validation_loader:
                img1 = test_data.x
                img2 = val_data.x
                y_val = val_data.y.int().item()
                y_test = test_data.y.int().item()
                out = model(img1, img2)
                out = torch.argmax(out)

                similarity_score[y_val].append(out.item())
            similarity_score = {
                x: np.sum(similarity_score[x]) for x in similarity_score}
            y_pred = max(similarity_score, key=similarity_score.get)
            pred.append(y_pred)
            gt.append(y_test)

    return gt, pred


def predict(single_sample, validation_loader, model):
    with torch.no_grad():
        model.eval()
        similarity_score = defaultdict(list)
        for val_data in validation_loader:
            img1 = single_sample
            img2 = val_data.x
            y_val = val_data.y.int().item()
            out = model(img1, img2)
            out = torch.argmax(out)

            similarity_score[y_val].append(out.item())

        similarity_score = {
            x: np.sum(similarity_score[x]) for x in similarity_score}
        y_pred = max(similarity_score, key=similarity_score.get)

    return y_pred, similarity_score


def validateprediction():

    return 0


def retrain(new_train_loader, model, loss_fn, optimizer, savepath):
    for epoch in range(0, 100):
        model.train()
        train_losses = []
        for data in new_train_loader:
            img1 = data.img1
            img2 = data.img2
            y = data.y.unsqueeze(0)

            out = model(img1, img2)
            loss = loss_fn(out, y)

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            train_losses.append(loss.item())

        if epoch % 10 == 0:
            print("Epoch number {}\n Current loss {}\n".format(epoch, loss.item()))

    torch.save(model, savepath)
