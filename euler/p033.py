"""
The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms, find the value of the denominator.
"""
from euler import gcd

nontrivial_curious_fractions = []
for numerator in range(10, 100):
    for denominator in range(numerator + 1, 100):
        assert numerator / denominator < 1
        s = set(str(numerator)) & set(str(denominator)) - {'0'}
        if len(s) == 1:
            d = s.pop()
            try:
                numerator_, denominator_ = int(str(numerator).strip(d)), int(str(denominator).strip(d))
            except ValueError:
                # int('') called due to double digit coincidence
                continue
            if numerator * denominator_ == numerator_ * denominator:
                nontrivial_curious_fractions.append((numerator, denominator))

assert len(nontrivial_curious_fractions) == 4
prod_numerators = prod_denominators = 1

for n, d in nontrivial_curious_fractions:
    prod_numerators *= n
    prod_denominators *= d

result = prod_denominators // gcd(prod_numerators, prod_denominators)
