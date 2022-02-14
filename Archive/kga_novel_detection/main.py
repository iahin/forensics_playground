def getsavedsample():
    with open('data\\novelty_train.npy', 'rb') as f:
        train = np.load(f, allow_pickle=True)
    with open('data\\novelty_test.npy', 'rb') as f:
        test = np.load(f, allow_pickle=True)

    return train, test

train, test = getsavedsample()