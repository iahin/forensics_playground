import os

import torch
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np


def chunkwise(t, size=2):
    # Pair sampling by permutation
    it = iter(t)
    newzipped = zip(*[it]*size)
    newlist = [list(x) for x in newzipped]
    return newlist


def getpredictionscore(gt, pred):
    import pandas as pd
    ACC = accuracy_score(gt, pred)
    AUC = roc_auc_score(gt, pred)
    f1_grid = precision_recall_fscore_support(gt, pred, average='macro')
    F1 = f1_grid[2]

    record_df = pd.DataFrame(data={
        'ACC': [round(ACC, 2)],
        'F1': [round(F1, 2)],
        'AUC': [round(AUC, 2)],

    })
    print(record_df.to_string(index=False))


def save(model, save_dir, save_prefix, steps):
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    save_prefix = os.path.join(save_dir, save_prefix)
    save_path = '{}_steps_{}.pt'.format(save_prefix, steps)
    torch.save(model.state_dict(), save_path)
