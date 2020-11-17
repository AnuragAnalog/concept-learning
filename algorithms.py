#!/usr/bin/python3

import numpy as np
import pandas as pd

def check_dtype(arr):
    if not isinstance(arr, np.ndarray):
        raise ValueError("Expects only numpy arrays")

    return

def candidate_elimination(features, labels, pos="yes"):
    check_dtype(features)
    check_dtype(labels)

    G_space = [[True] * features.shape[1]] * features.shape[1]
    S_space = [None] * features.shape[1]

    G = np.array([[True] * features.shape[1]] * features.shape[1])
    S = np.array([None] * features.shape[1])

    print(G_space, S_space)
    for i, (d, l) in enumerate(zip(features, labels)):
        print(S_space)
        if l == pos:
            if S_space[i] is None and i == 0:
                G_space[i] = G
                S_space[i] = d
            else:
                G_space[i] = G_space[i-1]
                S_space[i] = np.where(S_space[i-1] == d, S_space[i-1], True)
        else:
            if G_space[i] is None and i == 0:
                S_space[i] = S
                G_space[i] = G
            else:
                S_space[i] = S_space[i-1]
                for j, attr in enumerate(d):
                    if S_space[i-1][j] not in [attr, True]:
                        G_space[i][j][j] = S_space[i-1][j]

    for i, (g, s) in enumerate(zip(G_space[-1], S_space[-1])):
        if s in g:
            G[i] = g
            S[i] = s

    return G, S

def find_s(features, labels):
    pass

if __name__ == '__main__':
    data = pd.read_csv('dataset.csv')

    print(candidate_elimination(data.loc[:, data.columns != 'EnjoySport'].values, data['EnjoySport'].values, pos="Yes"))