"""
The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?
"""
from euler import primes

primes4 = set(primes(10000)[len(primes(1000)):])  # 4-digit primes
for p in primes4:
    p1 = 3330 + p
    p2 = 3330 + p1
    if p1 in primes4 and p2 in primes4:
        if sorted(str(p1)) == sorted(str(p2)) == sorted(str(p)):
            if p != 1487:
                result = p2 + p1 * 10 ** 4 + p * 10 ** 8
                break
