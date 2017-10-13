"""
The first two consecutive numbers to have two distinct prime factors are:

14 = 2 x 7
15 = 3 x 5

The first three consecutive numbers to have three distinct prime factors are:

644 = 2^2 x 7 x 23
645 = 3 x 5 x 43
646 = 2 x 17 x 19.

Find the first four consecutive integers to have four distinct prime factors. What is the first of these numbers?
"""
from itertools import count
from euler import factorise

n = 4
for result in count():
    if all(len(set(factorise(result + k))) == n for k in range(n)):
        break
