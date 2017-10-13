"""
The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
"""
from itertools import count
from euler import Primes

total = 0
count_ = 0
for n in count(11, 2):
    str_n = str(n)
    len_n = len(str_n)
    if n in Primes and all(int(str_n[k:]) in Primes and int(str_n[:k]) in Primes for k in range(1, len_n)):
        count_ += 1
        total += n
        if count_ == 11:
            result = total
            break
