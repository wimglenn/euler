"""
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 x 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.
"""
from euler import unique_digits

pandigital_products = set()
candidates = [n for n in range(2000) if '0' not in str(n) and unique_digits(n)]
for k, n in enumerate(candidates):
    for m in candidates[k:]:
        s = set(str(n)) & set(str(m))
        if not s:
            mn = str(m * n)
            if '0' not in mn and unique_digits(mn) and set('123456789') - set(str(m) + str(n)) == set(mn):
                pandigital_products |= {m * n}

result = sum(pandigital_products)
