import numpy as np
from sklearn.datasets import make_sparse_spd_matrix
from scipy.spatial import distance

def permutation_topics(B_true, B_sampled):
    B_urn = B_sampled.copy()
    k, V = B_true.shape
    B_urn[:, k+1] = range(k)
    permutation = []
    for i in range(k):
        distances = []
        for j in range(k-i):
            distances.append(np.linalg.norm(B_true[i] - B_urn[j]))
        min_index = np.argmin(distances)
        permutation.append(B_urn[min_index, k+1])
        B_urn = np.delete(B_urn, min_index, 0)
    return permutation


def _fake_log(*args, **kwargs):
    return


def graph_loss(G_true, G_sampled, permutation, debug=False):
    log = print if debug else _fake_log  # turn log off/on
    G_perm = G_sampled.copy()
    log("BEFORE FOR")
    for i in range(G_true.shape[0]):  # Number of rows
        p = int(permutation[i])
        G_perm[i] = G_sampled[p]
        log("G_PERM")
        log(G_perm)
        G_perm[:,i] = G_sampled[:,p]
        log("G_SAMPLED")
        log(G_sampled)
        log("NEW RETURN")
        log(abs(G_true-G_perm).sum())
    return abs(G_true-G_perm).sum()

