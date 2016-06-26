import time
import timeit
import random
from shared import parsed_args, format_result

VALUES = (
    1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0
)


class CardPile(object):
    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)


class Shue(CardPile):
    def __init__(self, decks=8):
        super(Shue, self).__init__(range(52) * decks)
        self.shuffle()
        self.dealt = []
        self.decks = decks

    def deal(self, number):
        '''return number cards'''
        if len(self.cards) < number:
            self.dealt = []
            self.cards = range(52) * self.decks
            self.shuffle()

        cards = [self.cards.pop() for x in range(number)]
        self.dealt.extend(cards)
        return cards


class Hand(CardPile):
    def __init__(self, cards):
        self.cards = cards

    @property
    def points(self):
        return sum(VALUES[c] for c in self.cards) % 10

    @property
    def is_natural(self):
        return self.points in (8,9)

    def __eq__(self, other):
        return self.points == other.points

    def __gt__(self, other):
        return self.points > other.points

    def __lt__(self, other):
        return self.points < other.points


def play_hand(s):
    banker, punter = Hand(s.deal(2)), Hand(s.deal(2))

    if punter.is_natural or banker.is_natural:
        pass
    elif punter.points <= 5:
        punter.cards.extend(s.deal(1))

    # if player didn't draw a card banker draws on 5 or less
    if len(punter.cards) == 2:
        if banker.points <= 5:
            banker.cards.extend(s.deal(1))
    # if player did draw a card following convuluted draw rules
    else:
        if banker.points <= 2:
            banker.cards.extend(s.deal(1))
        elif banker.points == 3 and VALUES[punter.cards[2]] != 8:
            banker.cards.extend(s.deal(1))
        elif banker.points == 4 and VALUES[punter.cards[2]] not in (0,1,8,9):
            banker.cards.extend(s.deal(1))
        elif banker.points == 5 and VALUES[punter.cards[2]] in (4,5,6,7):
            banker.cards.extend(s.deal(1))
        elif banker.points == 6 and VALUES[punter.cards[2]] in (6,7):
            banker.cards.extend(s.deal(1))

    if banker > punter:
        return 'banker'
    elif banker < punter:
        return 'punter'
    else:
        return 'draw'


def play(hands=100, decks=8):
    results = dict(banker=0, punter=0, draw=0)
    s = Shue(decks)

    for hand in range(hands):
        results[play_hand(s)] += 1

    return results


if __name__ == '__main__':
    args = parsed_args()

    if args.timing == 'timediff':
        start = time.time()
        results = play(args.games)
        end = time.time()
        print 'v2,{},{}'.format(args.games,end-start)
    elif args.timing == 'time':
        results = play(args.games)
        print format_result('v2', args.games)
    elif args.timing == 'timeit':
        t = timeit.Timer("play(%s)" % args.games, "from __main__ import play")
        seconds = t.timeit()
        print 'v2,{},{}'.format(args.games,seconds)
