"""
It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.

 9 =  7 + 2 * 1^2
15 =  7 + 2 * 2^2
21 =  3 + 2 * 3^2
25 =  7 + 2 * 3^2
27 = 19 + 2 * 2^2
33 = 31 + 2 * 1^2

It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
"""
import numpy as np
from itertools import count
from euler import primes

bound = 10
while True:
    candidates = np.ones(bound, dtype=bool)
    # strike out the evens, and the trivial solution
    candidates[::2] = False
    candidates[1] = False
    for p in primes(bound):
        for i in count():
            try:
                candidates[p + 2 * i * i] = False
            except IndexError:
                break
    if any(candidates):
        result = int(candidates.argmax())
        break
    else:
        bound *= 2
