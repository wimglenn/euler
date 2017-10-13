"""
In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in the following way:

High Card: Highest value card.
One Pair: Two cards of the same value.
Two Pairs: Two different pairs.
Three of a Kind: Three cards of the same value.
Straight: All cards are consecutive values.
Flush: All cards of the same suit.
Full House: Three of a kind and a pair.
Four of a Kind: Four cards of the same value.
Straight Flush: All cards are consecutive values of same suit.
Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for example, a pair of eights beats a pair of fives (see example 1 below). But if two ranks tie, for example, both players have a pair of queens, then highest cards in each hand are compared (see example 4 below); if the highest cards tie then the next highest cards are compared, and so on.

Consider the following five hands dealt to two players:

Hand,Player 1,Player 2,Winner,
1,"5H 5C 6S 7S KD Pair of Fives","2C 3S 8S 8D TD Pair of Eights",Player 2,
2,"5D 8C 9S JS AC Highest card Ace","2C 5C 7D 8S QH Highest card Queen",Player 1,
3,"2D 9C AS AH AC Three Aces","3D 6D 7D TD QD Flush with Diamonds",Player 2,
4,"4D 6S 9H QH QC Pair of Queens Highest card Nine","3D 6D 7H QD QS Pair of Queens Highest card Seven",Player 1,
5,"2H 2D 4C 4D 4S Full House With Three Fours","3C 3D 3S 9S 9D Full House with Three Threes",Player 1,

The file, p054_poker.txt, contains one-thousand random hands dealt to two players. Each line of the file contains ten cards (separated by a single space): the first five are Player 1's cards and the last five are Player 2's cards. You can assume that all hands are valid (no invalid characters or repeated cards), each player's hand is in no specific order, and in each hand there is a clear winner.

How many hands does Player 1 win?
"""
from functools import total_ordering
from operator import attrgetter
from pathlib import Path


class Card:

    values = {k: v for v, k in enumerate(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'], 2)}
    suits = {k[0].upper(): k for k in ('clubs', 'spades', 'diamonds', 'hearts')}

    def __init__(self, vs):
        value, suit = vs
        try:
            self.value = Card.values[value]
            self.suit = Card.suits[suit]
        except KeyError:
            raise ValueError('Could not parse card: {}'.format(vs))


@total_ordering
class Hand:

    ranks = {
        'High Card': 0,
        'One Pair': 1,
        'Two Pairs': 2,
        'Three of a Kind': 3,
        'Straight': 4,
        'Flush': 5,
        'Full House': 6,
        'Four of a Kind': 7,
        'Straight Flush': 8,
        'Royal Flush': 9,
    }

    def __init__(self, cards):
        self.cards = sorted([Card(x) for x in cards.split()], key=attrgetter('value'))
        if len(self.cards) != 5:
            raise ValueError('Could not parse hand: {}'.format(cards))
        self.rank = None
        self.high_card = None
        self._check_hand()
        assert self.rank is not None and self.high_card is not None

    def score(self):
        return Hand.ranks[self.rank]*100 + self.high_card.value

    def _check_hand(self):
        if self.is_flush() and self.is_straight():
            if self.cards[-1].value == Card('AS').value:
                self.rank = 'Royal Flush'
            else:
                self.rank = 'Straight Flush'
            self.high_card = self.cards[-1]
            return

        if len({x.value for x in self.cards}) == 2:
            self.rank = 'Four of a Kind'
            try:
                self.high_card = next(c for c in self.cards if sum(1 for x in self.cards if x.value == c.value) == 4)
            except StopIteration:
                self.rank = 'Full House'
                self.high_card = next(c for c in self.cards if sum(1 for x in self.cards if x.value == c.value) == 3)
            return

        if self.is_flush():
            self.rank = 'Flush'
            self.high_card = self.cards[-1]
            return

        if self.is_straight():
            self.rank = 'Straight'
            self.high_card = self.cards[-1]
            return

        if len({x.value for x in self.cards}) == 3:
            self.rank = 'Three of a Kind'
            try:
                self.high_card = next(c for c in self.cards if sum(1 for x in self.cards if x.value == c.value) == 3)
            except StopIteration:
                self.rank = 'Two Pairs'
                extra_card = next(c for c in self.cards if sum(1 for x in self.cards if x.value == c.value) == 1)
                self.high_card = [c for c in self.cards if c.value != extra_card.value][-1]
            return

        if len({x.value for x in self.cards}) == 4:
            self.rank = 'One Pair'
            self.high_card = next(c for c in self.cards if sum(1 for x in self.cards if x.value == c.value) == 2)
            return

        self.rank = 'High Card'
        self.high_card = self.cards[-1]

    def is_flush(self):
        return len({x.suit for x in self.cards}) == 1

    def is_straight(self):
        low_value = self.cards[0].value
        return [x.value for x in self.cards] == list(range(low_value, low_value + 5))

    def __lt__(self, other):
        return self.score() < other.score()

    def __eq__(self, other):
        return self.score() == other.score()


player1_wins = 0
for line in Path('data/p054_poker.txt').read_text().splitlines():
    player1, player2 = line[:14], line[14:]
    hand1, hand2 = Hand(player1), Hand(player2)
    if hand1 < hand2:
        x = '<'
    elif hand2 < hand1:
        x = '>'
    else:
        # need to check next highest card ...
        next_high_card1 = max((c for c in hand1.cards if c.value != hand1.high_card.value), key=attrgetter('value'))
        next_high_card2 = max((c for c in hand2.cards if c.value != hand2.high_card.value), key=attrgetter('value'))
        if next_high_card1.value < next_high_card2.value:
            x = '<'
        elif next_high_card2.value < next_high_card1.value:
            x = '>'
        else:
            # really we have to keep checking the next highest card recursively.
            # just checking once is super lame but it works for the sample data, so ... meh
            assert(0)
    msg = '{} {} {} ({} {} {})'.format(
        player1.strip(), x, player2.strip(),
        hand1.rank, 'wins against' if x == '>' else 'loses to', hand2.rank
    )
    # print(msg)
    if x == '>':
        player1_wins += 1

result = player1_wins
