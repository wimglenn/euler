"""
By replacing the 1st digit of the 2-digit number *3, it turns out that six of the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit number is the first example having seven primes among the ten generated numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993. Consequently 56003, being the first member of this family, is the smallest prime with this property.

Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit, is part of an eight prime value family.
"""
# it will never make sense to replace the last digit, because of even numbers
from itertools import combinations
from string import digits
from euler import primes


def replacements(n, positions):
    template = list(str(n))
    for position in positions:
        template[position] = '?'
    for d in digits[1 if 0 in positions else 0:]:
        yield int(''.join(template).replace('?', d))

some_primes = primes(10 ** 6)  # primes below 10 million
set_primes = set(some_primes)


def f():
    for p in some_primes:
        n = len(str(p))
        for i in range(1, n):
            for indices in combinations(range(n - 1), i):
                hits = [x for x in replacements(p, indices) if x in set_primes]
                if len(hits) == 8:
                    return sorted(hits)[0]

result = f()
