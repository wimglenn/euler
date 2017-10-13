"""
If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?


NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.
"""
d = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six',
     7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve',
     13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
     17: 'seventeen', 18: 'eighteen', 19: 'nineteen'}
prefixes = {2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty', 6: 'sixty',
            7: 'seventy', 8: 'eighty', 9: 'ninety'}
for n in range(20, 100):
    tens = n // 10
    units = n % 10
    d[n] = prefixes[tens] + ('-{}'.format(d[units]) if units else '')
for n in range(100, 1000):
    hundreds = n // 100
    rest = n % 100
    d[n] = d[hundreds] + ' hundred' + (' and {}'.format(d[rest]) if rest else '')
d[1000] = 'one thousand'
result = sum(1 for word in d.values() for c in word if c not in '- ')
