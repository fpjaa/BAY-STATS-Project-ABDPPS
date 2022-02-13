import numpy as np
from sklearn.datasets import make_sparse_spd_matrix
from scipy.spatial import distance

def permutation_topics(B_true, B_sampled):
    B_urn=B_sampled.copy()
    k,V=B_true.shape
    B_urn[:,k+1]=range(k)
    permutation=[]
    for i in range(k):
        distances=[]
        for j in range(k-i):
            distances.append(np.linalg.norm(B_true[i]-B_urn[j]))
        min_index = np.argmin(distances)
        permutation.append(B_urn[min_index,k+1])
        B_urn=np.delete(B_urn,min_index,0)
    return permutation
    

def graph_loss(G_true,G_sampled,permutation):
    G_perm=G_sampled.copy()
    print("BEFORE FOR")
    for i in range(int(len(G_true[0]))):
        p=int(permutation[i])
        G_perm[i]=G_sampled[p]
        print("G_PERM")
        print(type(G_perm))
        G_perm[:,i]=G_sampled[:,p]
        print("G_SAMPLED")
        print(type(G_sampled))
        print("NEW RETURN")
        print(abs(G_true-G_perm).sum())
    return abs(G_true-G_perm).sum()

