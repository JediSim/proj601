from numpy import coo_matrix


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

    for idVertex, idsNeighbors in neighbors.items():
        ROWS.append(idVertex)
        COLS.append(idVertex)
        DATA.append(-len(idsNeighbors))

        for idNeighbor in idsNeighbors:
            ROWS.append(idVertex)
            COLS.append(idNeighbor)
            DATA.append(1)

    L = coo_matrix((DATA, (ROWS, COLS)), shape=(n, n))
    return L.tocsr()
