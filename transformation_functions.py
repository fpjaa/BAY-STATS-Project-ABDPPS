import numpy as np
import scipy

# Transformation functions (deterministic)

def update_Theta(Theta, H, log=False):
    D = Theta.shape[0]
    for d in range(D):
        Theta[d] = scipy.special.softmax(H[d])  # Doesnt overflow
    if log:
        print('Success: Theta transformed from H')
    return Theta


def update_E(E, Z):
    k = E.shape[1]
    for topic in range(k):
        E[:, topic] = np.sum(Z == topic, axis=2).sum(axis=1)
    print('Success: E transformed from Z')
    return E


def update_C(C, Z):
    k = C.shape[0]
    for topic in range(k):
        C[topic, :] = np.sum(Z == topic, axis=2).sum(axis=0)
    print('Success: C transformed from Z')
    return C


def update_B(B, C):
    # Note this is the transformation from C
    for topic in range(0, len(B)):
        B[topic] = C[topic] / sum(C[topic])
    print('Success: B transformed from C')
    return B


def update_Sigma(K):
    Sigma = np.linalg.inv(K)
    print('Success: Sigma transformed from K')
    return Sigma


def update_G(K):  # Won't update Sigma automatically anymore
    # Generate an adjacency matrix
    G = (K != 0).astype(int)
    G[np.diag_indices_from(G)] = 0
    print('Success: G transformed from K')
    return G
