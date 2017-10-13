"""
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?
"""
from itertools import permutations
from euler import is_prime


def f():
    i = 9
    while i > 0:
        for t in permutations(''.join(str(d) for d in range(i, 0, -1)), i):
            n = int(''.join(t))
            if is_prime(n):
                return n
        else:
            i -= 1

result = f()
