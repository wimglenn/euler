"""
In England the currency is made up of pound, P, and pence, p, and there are eight coins in general circulation:

1p, 2p, 5p, 10p, 20p, 50p, 1P (100p) and 2P (200p).
It is possible to make 2P in the following way:

1P + 50p + 2 x 20p + 5p + 2p + 3 x 1p
How many different ways can 2P be made using any number of coins?
"""
def ways(wallet=[], coins=(200, 100, 50, 20, 10, 5, 2, 1)):
    amount = sum(wallet)
    if amount == 200:
        return 1
    elif amount > 200:
        return 0
    else:
        smallest_coin = wallet[-1] if wallet else 200
        new_coins = coins[coins.index(smallest_coin):]
        return sum(ways(wallet + [c], new_coins) for c in new_coins)
result = ways()
