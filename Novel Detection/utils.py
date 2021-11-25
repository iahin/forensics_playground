from sklearn.preprocessing import StandardScaler


def data_std(train, test):
    scaler = StandardScaler()
    X_train = [x for x, y in train]
    scaler_model = scaler.fit(X_train)
    X_train = scaler_model.transform(X_train)
    Y_train = [0 for x, y in train]

    X_test = [x for x, y in test]
    X_test = scaler_model.transform(X_test)
    y_test = [1 for x, y in test]

    return result