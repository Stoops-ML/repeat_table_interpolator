import numpy as np

# independent variables
l0 = [0] * 50 + [300] * 50
l1 = [10] * 10 + [20] * 10 + [30] * 10 + [40] * 10 + [50] * 10 \
     + [60] * 10 + [70] * 10 + [80] * 10 + [90] * 10 + [100] * 10
l2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] * 10

# dependent variables
l3 = np.random.rand(100)
l4 = np.random.rand(100)

# create table
out = [[]] * 100
with open('file1.csv', 'w') as f:
    for i, (a, b, c, d, e) in enumerate(zip(l0, l1, l2, l3, l4)):
        f.write(f'{a:6} {b:6} {c:6} {d:6.4f} {e:6.4f}\n')
