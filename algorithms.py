#!/usr/bin/python3

import numpy as np
import pandas as pd

def check_dtype(arr):
    if not isinstance(arr, np.ndarray):
        raise ValueError("Expects only numpy arrays")

    return

def candidate_elimination(features, labels, pos="yes", print_funct=print):
    check_dtype(features)
    check_dtype(labels)

    G_space = [[True] * features.shape[1]] * features.shape[1]
    S_space = [None] * features.shape[0]

    G = [[True] * features.shape[1]] * features.shape[1]
    S = np.array([None] * features.shape[1])

    print_funct("Initially,\tG = {}\n\t\tS = {}\n\n".format(str(G).replace('True', '?'), str(S).replace('None', 'φ')))
    for i, (d, l) in enumerate(zip(features, labels)):
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
                tmp = []
                for j, attr in enumerate(d):
                    if S_space[i-1][j] not in [attr, True]:
                        tmp.append([True] * features.shape[1])
                        tmp[-1][j] = S_space[i-1][j]
                        G_space[i][j] = tmp[-1]
                    else:
                        G_space[i][j] = [True] * features.shape[1]

        format_S = str(S_space[i]).replace('[', '<').replace(']', '>').replace('True', '?')
        format_G = [str(G_space[i]).replace('[', '<').replace(']', '>').replace('True', '?')[1:-1]]
        print_funct("For instance {}: G{} = {}\n\t\tS{} = {}\n".format(i+1, i+1, format_G, i+1, format_S))

    final_G = list()
    final_S = list()
    for i, (g, s) in enumerate(zip(G_space[-1], S_space[-1])):
        if (not isinstance(g, bool)) and (s in g) and isinstance(s, str):
            final_G.append(g)
        final_S.append(s)

    return final_G, final_S

def find_s(features, labels, pos="yes", print_funct=print):
    check_dtype(features)
    check_dtype(labels)

    S_space = [None] * features.shape[0]
    S = np.array([None] * features.shape[1])

    print_funct("Initially, H = {}".format(str(S).replace('None', 'φ')))
    for i, (d, l) in enumerate(zip(features, labels)):
        if l == pos:
            if S_space[i] is None and i == 0:
                S_space[i] = d
            else:
                S_space[i] = np.where(S_space[i-1] == d, S_space[i-1], True)
        else:
            S_space[i] = S_space[i-1]

        format_S = str(S_space[i]).replace('[', '<').replace(']', '>').replace('True', '?')
        print_funct("For instance {}: h{} = {}\n".format(i+1, i+1, format_S))

    return S_space

if __name__ == '__main__':
    data = pd.read_csv('dataset.csv')

    print(candidate_elimination(data.loc[:, data.columns != 'EnjoySport'].values, data['EnjoySport'].values))