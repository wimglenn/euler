"""
It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.
"""
from itertools import count

for result in count(1):
    strs = [str(i * result) for i in range(1, 7)]
    if len(set([''.join(sorted(s)) for s in strs])) == 1:
        break
