import numpy as np
from scipy.spatial import cKDTree
from itertools import product
from scipy import interpolate


def push_right(table, *indices):
    """move each column in 'indices' to the far right of the table. This converts the column from independent variable
    to dependent variable.

    Args:
        table: table containing independent variables and dependent variables. Note that the dependent variables are
        expected to be to the right of the columns of independent variables.
        indices: column index of the table that is to be pushed to the far right of the table

    Returns:
        numpy array of updated table

    """
    a = table[:, list(*indices)]
    b = np.delete(table, indices, axis=1)
    return np.concatenate((b, a), axis=1)


def interpolate_table(table, *coordinates, move_columns=None):
    """interpolate table with repeated values.

    Args:
        table: table containing independent variables and dependent variables. Note that the dependent variables are
        expected to be to the right of the columns of independent variables.
        coordinates: the coordinates of the independent variables that the user wants to interpolate. Note that this value is
        unpacked by the method, therefore the user can specify any number of coordinates.
        move_columns: convert column(s) of the table from independent variables to dependent variables

    Returns:
        numpy array of interpolated values.

    """
    # convert to numpy arrays
    table = np.array(table)
    coordinates = np.array(coordinates)

    # converted independent variables to dependent variables
    if move_columns:
        if isinstance(move_columns, int):
            move_columns = [move_columns]
        table = push_right(table, move_columns)

    # independent and dependent variables
    num_IVs = len(coordinates)
    num_DVs = table.shape[1] - num_IVs
    IV, DVs = table[:, :num_IVs], table[:, -num_DVs:]
    if num_DVs < 1:
        raise ValueError("Number of dependent variables must be one or greater.")
    if num_IVs < 1:
        raise ValueError("Number of independent variables must be one or greater.")

    # find upper & lower bounds of each IV column
    bounds = [[0, 0]] * num_IVs
    for i, coord in enumerate(coordinates):
        IV_col = np.array(list(set(IV[:, i])))
        tree = cKDTree(IV_col.reshape(-1, 1))
        _, ind = tree.query([coord], k=2)
        bounds[i] = IV_col[ind]

    output = np.empty(0)
    for i in range(num_DVs):
        DV = DVs[:, i]  # select column of DVs

        # get DV of all combinations of coords
        new_DV = np.empty(0)
        tree = cKDTree(IV)
        for bound in product(*bounds):
            _, ind = tree.query(bound, k=1)
            new_DV = np.append(new_DV, DV[ind])

        for j in reversed(range(num_IVs)):
            new_IV = np.empty(0)
            for k in range(len(new_DV) // 2):
                lin_interp = interpolate.interp1d([bounds[j][0], bounds[j][1]],
                                                  [new_DV[k * 2], new_DV[k * 2 + 1]],
                                                  fill_value="extrapolate")
                new_IV = np.append(new_IV, lin_interp(coordinates[j]))
            new_DV = new_IV
        output = np.append(output, new_DV)

    return output

