"""
The prime 41, can be written as the sum of six consecutive primes:

41 = 2 + 3 + 5 + 7 + 11 + 13
This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?
"""
from itertools import count
from euler import primes

p = primes(10 ** 6)
set_p = set(p)


def f():
    # first find an upper bound on n
    n = 1
    while sum(p[:n]) < 10 ** 6:
        n += 1
    while True:
        for i in count():
            sum_p = sum(p[i:n + i])
            if sum_p < 10 ** 6:
                if sum_p in set_p:
                    return sum_p
            else:
                break
        n -= 1

result = f()
