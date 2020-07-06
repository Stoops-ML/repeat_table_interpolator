import numpy as np
from scipy.spatial import cKDTree
from itertools import product


def interpolate_table(polar, *coords, move_columns=None):
    def push_right(table, *indices):
        """move each column in indices to the far right of the table.
        This makes the column a dependent variable"""
        a = table[:, list(*indices)]
        b = np.delete(table, indices, axis=1)
        return np.concatenate((b, a), axis=1)

    def lin_interp(y, y0, y1, x0, x1):
        """linear interpolation"""
        return (y - y0) / (y1 - y0) * (x1 - x0) + x0

    # convert to numpy arrays
    polar = np.array(polar)
    coords = np.array(coords)

    if move_columns:
        if isinstance(move_columns, int):
            move_columns = [move_columns]
        polar = push_right(polar, move_columns)

    # independent and dependent variables
    num_IVs = len(coords)
    num_DVs = polar.shape[1] - num_IVs
    IV, DVs = polar[:, :num_IVs], polar[:, -num_DVs:]

    # find upper & lower bounds of each IV column
    bounds = [[0, 0]] * num_IVs
    for i, coord in enumerate(coords):
        IV_col = np.array(list(set(IV[:, i])))
        tree = cKDTree(IV_col.reshape(-1, 1))
        _, ind = tree.query([coord], k=2)
        bounds[i] = IV_col[ind]

    output = []
    for i in range(num_DVs):
        DV = DVs[:, i]  # select column of DVs

        # get DV of all combinations of coords
        new_DV = []
        tree = cKDTree(IV)
        for bound in product(*bounds):
            _, ind = tree.query(bound, k=1)
            new_DV.append(float(DV[ind]))

        for j in reversed(range(num_IVs)):
            new_IV = []
            for k in range(len(new_DV) // 2):
                interp_value = lin_interp(coords[j],
                                          bounds[j][0], bounds[j][1],
                                          new_DV[k * 2], new_DV[k * 2 + 1])
                new_IV.append(interp_value)
            new_DV = new_IV
        output.append(*new_DV)

    return output

