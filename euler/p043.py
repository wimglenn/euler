"""
The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.

Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:

d2d3d4=406 is divisible by 2
d3d4d5=063 is divisible by 3
d4d5d6=635 is divisible by 5
d5d6d7=357 is divisible by 7
d6d7d8=572 is divisible by 11
d7d8d9=728 is divisible by 13
d8d9d10=289 is divisible by 17

Find the sum of all 0 to 9 pandigital numbers with this property.
"""
from euler import unique_digits

hits = {1406357289}
# d6 must be 0 or 5 in order for d4d5d6 to be divisble by 5.  but if d6 == 0,
# then d6d7d8 == d7d8 can't be divisible by 11 since this implies d7 == d8
# which is impossible for a pandigital number.  therefore d6 == 5.
d6 = 5
d678 = [x for x in range(500, 600) if x % 11 == 0 and unique_digits(x)]

for n in d678:
    d7 = (n % 100) // 10
    d8 = n % 10
    for d9 in set(range(10)) - {d6, d7, d8}:
        if (100 * d7 + 10 * d8 + d9) % 13 == 0:
            for d10 in set(range(10)) - {d6, d7, d8, d9}:
                if (100 * d8 + 10 * d9 + d10) % 17 == 0:
                    for d5 in set(range(10)) - {d6, d7, d8, d9, d10}:
                        if (100 * d5 + 10 * d6 + d7) % 7 == 0:
                            # d2d3d4 is even and hence d4 must be in '02468'
                            for d4 in set(range(0, 10, 2)) - {d5, d6, d7, d8, d9, d10}:
                                for d3 in set(range(10)) - {d4, d5, d6, d7, d8, d9, d10}:
                                    # d345, and therefore also d3 + d4 + d5, must be divisible by 3
                                    if (d3 + d4 + d5) % 3 == 0:
                                        d1, d2 = set(range(10)) - {d3, d4, d5, d6, d7, d8, d9, d10}
                                        hit = sum(10 ** i * d for i, d in enumerate([d10, d9, d8, d7, d6, d5, d4, d3, d2, d1]))
                                        hits |= {hit}
                                        d2, d1 = d1, d2
                                        hit = sum(10 ** i * d for i, d in enumerate([d10, d9, d8, d7, d6, d5, d4, d3, d2, d1]))
                                        hits |= {hit}

assert all(unique_digits(d) for d in hits)
result = sum(hits)
