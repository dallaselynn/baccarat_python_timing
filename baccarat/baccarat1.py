import time
import timeit
import random
import itertools
from abc import ABCMeta, abstractmethod
from shared import parsed_args, format_result


SUIT_NAMES = {'s': 'Spades',
              'd': 'Diamonds',
              'h': 'Hearts',
              'c': 'Clubs'}
SUITS = set(['s','d','h','c'])
RANKS = set(['2','3','4','5','6','7','8','9','T','J','Q','K','A'])


class InvalidCardError(Exception): pass
class InvalidHandError(Exception): pass

class Card(object):
    def __init__(self, rank, suit):
        if rank not in RANKS:
            raise InvalidCardError("%s is not a valid card rank" % rank)
        if suit not in SUITS:
            raise InvalidCardError("%s is not a valid card suit" % suit)

        self._suit = suit
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    @property
    def value(self):
        v = 0
        try:
            v = int(self.rank)
        except ValueError:
            pass

        return v

    def __str__(self):
        return '%s of %s' % (self.rank, SUIT_NAMES[self.suit])


class Deck(object):
    def __init__(self):
        self.cards = []

        for pair in itertools.product(RANKS, SUITS):
            self.cards.append(Card(*pair))


class Shoe(object):
    '''
    Some number of cards with various values.
    '''

    def __init__(self, decks=8, shuffle=True):
        self.d = Deck()
        self.decks = decks
        self.cards = self.d.cards * self.decks
        if shuffle:
            self.shuffle()

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def refill(self, shuffle=True):
        del self.cards[:]
        self.cards = self.d.cards * self.decks

        if shuffle:
            self.shuffle()

class BaccaratHand(object):
    '''
    A Baccarat hand is 2 or 3 cards, it can be a player or banker hand.
    '''

    __metaclass__ = ABCMeta

    def __init__(self):
        super(BaccaratHand, self).__init__()
        self. cardpile = []

    def __eq__(self, other):
        if isinstance(other, BaccaratHand):
            return self.score == other.score
        elif isinstance(other, int):
            return self.score == other
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, BaccaratHand):
            return self.score > other.score
        elif isinstance(other, int):
            return self.score > other
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, BaccaratHand):
            return self.score < other.score
        elif isinstance(other, int):
            return self.score < other
        else:
            return NotImplemented

    @property
    def is_natural(self):
        if len(self.cardpile) == 2 and (self.score == 8 or self.score == 9):
            return True
        else:
            return False

    @property
    def score(self):
        '''
        all cards ace through 9 are valued according to pip count,
        TJQK are valued at 0.

        no hand may total more than 9 so any value over 10 must have
        10 subtracted from it.
        '''

        score = 0

        for card in self.cardpile:
            score += card.value

        if score >= 10:
            score -= 10

        return score

    def add_card(self, card):
        '''
        Add a Card to the hand - a 'Card' can by anything with a
        rank property.
        '''

        if len(self.cardpile) + 1 > 3:
            raise InvalidHandError("a baccarat hand never has more than 3 cards")

        self.cardpile.append(card)

    def clear(self):
        '''
        removes all cards from the hand
        '''

        del self.cardpile[:]

    @abstractmethod
    def draws_card(self, other_hand):
        '''
        Determine if the player should draw a card or not
        '''
        # raise NotImplementedError, "subclasses must implement this method"
        pass


class BankHand(BaccaratHand):
    '''
    The bank hand takes actions depending on the player hand
    '''

    def __init__(self):
        super(BankHand, self).__init__()
    
    def draws_card(self, player_hand):
        if player_hand.is_natural:
            return False

        # player hand took no card
        if len(player_hand.cardpile) == 2:
            return True if self.score < 6 else False

        # player hand took a card
        if self.score <= 2:
            return True
        elif self.score == 3 and player_hand.cardpile[2].value in [0,1,2,3,4,5,6,7,9]:
            return True
        elif self.score == 4 and player_hand.cardpile[2].value in [2,3,4,5,6,7]:
            return True
        elif self.score == 5 and player_hand.cardpile[2].value in [4,5,6,7]:
            return True
        elif self.score == 6 and player_hand.cardpile[2].value in [6,7]:
            return True
        else:
            return False 


class PlayerHand(BaccaratHand):
    def __init__(self):
        super(PlayerHand, self).__init__()

    def draws_card(self, bank_hand):
        if bank_hand.is_natural or self.score > 5:
            return False
        else:
            return True


class BaccaratGame(object):
    ''' 
    A Baccarat Game consists of some number of bettors each making 
    one of 3 possible bets: bank, player or tie, on a deal of 2 hands,
    the player hand and the bank hand.
    '''
    
    def __init__(self, decks=8):
        self.decks = decks
        self.shoe = Shoe(decks=decks)
        self.player_hand = PlayerHand()
        self.bank_hand = BankHand()
        self.winner = None

    def play(self):
        '''
        play a game of baccarat through completion
        '''

        if len(self.shoe.cards) < 6:
            self.shoe.refill()

        self.player_hand.clear()
        self.bank_hand.clear()

        self.player_hand.add_card(self.shoe.deal())
        self.bank_hand.add_card(self.shoe.deal())
        self.player_hand.add_card(self.shoe.deal())
        self.bank_hand.add_card(self.shoe.deal())

        if self.player_hand.draws_card(self.bank_hand):
            self.player_hand.add_card(self.shoe.deal())

        if self.bank_hand.draws_card(self.player_hand):
            self.bank_hand.add_card(self.shoe.deal())

        if self.player_hand > self.bank_hand:
            self.winner = self.player_hand
        elif self.player_hand < self.bank_hand:
            self.winner = self.bank_hand
        elif self.player_hand == self.bank_hand:
            self.winner = None


def play(number_of_games):
    results = {'bank': 0, 'player': 0, 'tie': 0}
    g = BaccaratGame()

    while number_of_games > 0:
        g.play()
        if isinstance(g.winner, BankHand):
            results['bank'] += 1
        elif isinstance(g.winner, PlayerHand):
            results['player'] += 1
        elif g.winner is None:
            results['tie'] += 1
        else:
            print 'wtf?!!?'
        number_of_games -= 1

    return results


if __name__ == '__main__':
    args = parsed_args()

    if args.timing == 'timediff':
        start = time.time()
        results = play(args.games)
        end = time.time()
        print 'v1,{},{}'.format(args.games, end-start)
    elif args.timing == 'time':
        results = play(args.games)
        print format_result('v1', args, results)
    elif args.timing == 'timeit':
        t = timeit.Timer("play(%s)" % args.games, "from __main__ import play")
        seconds = t.timeit()
        print ','.join(('v1', args.games, seconds))
