"""
If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p <= 1000, is the number of solutions maximised?
"""
from collections import Counter
from euler import isqrt

squares = {n ** 2 for n in range(1, 501)}
counter = Counter()
for a in range(1, 501):
    for b in range(a, 501):
        if a ** 2 + b ** 2 in squares:
            c = isqrt(a ** 2 + b ** 2)
            p = a + b + c
            if p <= 1000:
                counter[p] += 1

result = counter.most_common(1)[0][0]
