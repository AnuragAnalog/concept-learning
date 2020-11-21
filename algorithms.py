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

    uniques = dict()
    for i, row in enumerate(features.T):
        uniques[i] = np.unique(row).tolist()

    def is_consistent(D, H):
        for (d, h) in zip(D, H):
            if d == h or h is True:
                continue
            else:
                return False

        return True

    def change_S(D, H):
        for i, (d, h) in enumerate(zip(D, H)):
            if h == None:
                H[i] = d
            else:
                if d != h:
                    H[i] = True

        return H

    def change_G(D, H):
        curr_G = list()
        for i, (h, d) in enumerate(zip(H, D)):
            tmp = [True] * features.shape[1]
            if h is True and len(uniques[i]) != 1:
                ind = uniques[i].index(d)
                tmp[i] = uniques[i][1 - ind]
            curr_G.append(tmp)

        return curr_G

    G_space = [[True] * features.shape[1]]
    S_space = [[None] * features.shape[1]]

    print_funct("Initially, G = {}".format(str(G_space[-1]).replace('True', '?')))
    print_funct("S = {}\n\n".format(str(S_space[-1]).replace('None', 'φ')))
    for i, (d, l) in enumerate(zip(features, labels)):
        G = G_space[-1]
        S = S_space[-1]

        if l == pos:
            if isinstance(G[0], list):
                for g in G:
                    if not is_consistent(d, g):
                        G.remove(g)
            else:
                if is_consistent(d, G):
                    G_space.append(G)
                else:
                    pass

            if not is_consistent(d, S):
                S = change_S(d, S)
            S_space.append(S)
        else:
            S_space.append(S)

            if is_consistent(d, G):
                tmp = change_G(d, G)
                curr_G = list()
                for t1 in tmp:
                    add_h = 0
                    for j, t2 in enumerate(features[:i+1]):
                        if (is_consistent(t2, t1) and labels[j] == pos) or (not(is_consistent(t2, t1)) and labels[j] != pos):
                            add_h = add_h + 1
                        if add_h == i+1:
                            curr_G.append(t1)
                G_space.append(curr_G)
            else:
                G_space.append(G)

        format_S = str(S_space[i]).replace('[', '<').replace(']', '>').replace('True', '?')
        format_G = str(G_space[i]).replace('[', '<').replace(']', '>').replace('True', '?')
        print_funct("For instance {}: G{} = {}\n".format(i+1, i+1, format_G))
        print_funct("\t\tS{} = {}\n".format(i+1, format_S))

    final_G = G_space[-1]
    final_S = S_space[-1]

    print_funct('\n')
    print_funct("Final G: {}".format(str(final_G).replace('[', '<').replace(']', '>').replace('True', '?')))
    print_funct("Final S: {}".format(str(final_S).replace('[', '<').replace(']', '>').replace('True', '?')))

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

    print_funct('\n')
    print_funct("Final h: {}".format(str(S_space[-1]).replace('[', '<').replace(']', '>').replace('True', '?')))

    return S_space

if __name__ == '__main__':
    data = pd.read_csv('dataset.csv')

    print(candidate_elimination(data.loc[:, data.columns != 'EnjoySport'].values, data['EnjoySport'].values))
