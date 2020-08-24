import numpy as np
from scipy.spatial import cKDTree
from itertools import product
from scipy import interpolate


def interpolate_table(table, coordinates, DV_columns=None):
    """interpolate table with repeated values.

    Args:
        table: table containing independent variables and dependent variables. The independent variables are expected to
        be on the stepped from left to right. For example, for three independent variables with the first (in the first
        column) having 2 entries, second (in the second column) having 10 entries and the third (in the third column)
        having 10 entries both entries in the first column must be repeated 50 times, the 10 entries in the second
        column must be repeated 10 times each, and the 10 entries in the third column must be repeated 10 times each.
        coordinates: the independent variables that you want to interpolate the dependent variables at.
        DV_columns: the column numbers of the dependent variables starting at 0. Alternatively, `DV_columns` can be set
        to the final columns of the table if it is not inputted by the user (i.e. `DV_columns=None`). The number of
        columns is the number of table columns minus the number of `coordinates` inputted.

    Returns:
        numpy array of interpolated values.

    Notes:
        The independent variables are read in from the table from left to right. For example, if `DV_columns` includes a `0`
        in the list then the first independent variable will start at the second column of the table. If `DV_columns`
        includes a `1` then the first independent variable will be the first column of the table, but if a second
        independent variable is specified it cannot be of the second column (because that is designated for the dependent
        variable); therefore, the second independent variable will jump one column to be the third column of the table.

    """
    # convert to numpy arrays
    table = np.array(table)
    coordinates = np.array(coordinates)  # values to interpolate at

    # length of variables
    num_IVs = len(coordinates)
    num_DVs = np.shape(table)[1] - num_IVs if not DV_columns else len(DV_columns)
    assert np.shape(table)[
               1] >= num_IVs + num_DVs, 'The number of independent and dependent variables must be smaller than or ' \
                                        'equal to the number of columns in the table'

    # if user hasn't chosen columns of dependent variables
    if not DV_columns:
        DV_columns = range(num_IVs, num_IVs + num_DVs)  # DV columns are the last columns of the table (that aren't the IV columns)
    elif isinstance(DV_columns, int):
        DV_columns = [DV_columns]

    # get independent and dependent variables
    columns = set(range(np.shape(table)[1]))
    IV_columns = list(columns.difference(DV_columns))[:num_IVs]  # columns of IVs
    IV, DVs = table[:, IV_columns], table[:, DV_columns]

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

        # get DV of all combinations of coordinates
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



