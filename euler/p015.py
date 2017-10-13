"""
Starting in the top left corner of a 2x2 grid, there are 6 routes (without backtracking) to the bottom right corner.

How many routes are there through a 20x20 grid?
"""
import numpy as np

a = np.zeros((21, 21), dtype=int)
a[0] = 1
a[:, 0] = 1
for i in range(a.shape[0]):
    for j in range(a.shape[1]):
        if a[i, j] == 0:
            a[i, j] = a[i - 1, j] + a[i, j - 1]
result = int(a[-1, -1])
