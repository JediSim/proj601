from scipy.sparse import *
import numpy as np


def compute_neighbors(faces):
    """
    :param faces: list of faces
    :returns: dict of list of neighbors
    """
    neighbors = {}
    for i in range(len(faces)):
        for j in range(3):
            if faces[i][j] in neighbors:
                neighbors[faces[i][j]].append(faces[i][(j+1) % 3])
                neighbors[faces[i][j]].append(faces[i][(j+2) % 3])
            else:
                neighbors[faces[i][j]] = [
                    faces[i][(j+1) % 3], faces[i][(j+2) % 3]]
    for j in range (len(neighbors)):
        neighbors[j] = list(set(neighbors[j]))
    return neighbors


def make_laplacian(vertices, faces):
    """
    :param vertices: list of vertices
    :param faces: list of faces, contains ids of vertices
    :return: laplacian matrix
    """
    n = len(vertices)

    ROWS = []
    COLS = []
    DATA = []

    neighbors = compute_neighbors(faces)
    print("neighbors : ",neighbors)

    for idVertex, idsNeighbors in neighbors.items():
        ROWS.append(idVertex)
        COLS.append(idVertex)
        DATA.append(-len(idsNeighbors))

        for idNeighbor in idsNeighbors:
            ROWS.append(idVertex)
            COLS.append(idNeighbor)
            DATA.append(1)

    # print(DATA)
    L = coo_matrix((np.array(DATA), (np.array(ROWS), np.array(COLS))), shape=(n, n))
    # print("L : ",L.tocsc())
    return L.tocsc()

def value_of_bord(i,bord):
    # index = bord.index(i)
    return (360/len(bord))*i+1

def fix_bord(L, bord,b):
    """
    :param L: laplacian matrix
    :param bord: list of vertices ids
    :return: laplacian matrix with fixed bord
    """
    n = L.shape[0]
    for i in range(n):
        if i in bord:
            L[i, i] = 1
            # on fixe les valeurs de la ligne a 0
            b[i] = value_of_bord(i,bord)
            print("bord : ",b[i])
            for j in range(n):
                # on parcours en colonne en modifiant b si il y a un coeff non null
                # if L[j, i] != 0:
                #     b[j] -= b[i]
                # On fixe la ligne et la colonne a 0 
                if j != i:
                    L[i, j] = 0
                    L[j, i] = 0
    # for i in range(len(bord)):
    #     L[bord[i], bord[i]] = 1
    #     b[bord[i]] = value_of_bord(i,bord)
    #     for j in range(n):
    #         if L[j, bord[i]] != 0:
    #             b[j] -= b[bord[i]]
    #         if j != bord[i]:
    #             L[bord[i], j] = 0
    #             L[j, bord[i]] = 0
    return L,b
    