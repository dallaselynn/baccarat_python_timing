from nose.tools import ok_, eq_, raises, assert_false

from baccarat.game import InvalidCardError, InvalidHandError
from baccarat.game import Card, Deck, Shoe, BaccaratHand, PlayerHand, BankHand, BaccaratGame

def test_card_properties():
    c=Card('T','s')
    ok_(c.rank=='T')
    ok_(c.suit=='s')
    ok_(str(c) == 'T of Spades')
    ok_(c.value == 0)

    c=Card('7', 'h')
    ok_(c.rank=='7')
    ok_(c.suit=='h')
    ok_(str(c) == '7 of Hearts')
    ok_(c.value == 7)

@raises(InvalidCardError)
def test_invalid_card_rank_raises_exception():
    c=Card('G','s')

@raises(InvalidCardError)
def test_invalid_card_suit_raises_exception():
    c=Card('T','z')

def test_deck():
    d=Deck()
    ok_(len(d.cards)==52)
    ok_(len(filter(lambda(x): not isinstance(x, Card), d.cards)) == 0)

def test_shoe():
    s = Shoe()
    eq_(len(s.cards), 8 * 52)
    c = s.deal()
    ok_(isinstance(c,Card))
    s = Shoe(decks=1, shuffle=False)
    eq_(len(s.cards), 52)

@raises(TypeError)
def test_baccarat_hand():
    h = BaccaratHand()

@raises(InvalidHandError)
def test_hand_cant_have_too_many_cards():
    p = PlayerHand()
    p.add_card(Card('A','s'))
    p.add_card(Card('A','s'))
    p.add_card(Card('A','s'))
    p.add_card(Card('A','s'))

def test_hands():
    p = PlayerHand()
    b = BankHand()

    eq_(len(p.cardpile), 0)
    eq_(len(b.cardpile), 0)

    assert_false(p.is_natural)
    assert_false(b.is_natural)

    eq_(p.score, 0)
    eq_(b.score, 0)

    c1,c2,c3,c4 = Card('8','h'), Card('A','s'), Card('7','d'), Card('2', 'c')

    p.add_card(c1)
    p.add_card(c2)

    b.add_card(c3)
    b.add_card(c4)

    eq_(len(p.cardpile), 2)
    eq_(len(b.cardpile), 2)
    
    eq_(p.score, 8)
    eq_(b.score, 9)

    assert(p.is_natural)
    assert(b.is_natural)

    assert_false(p.draws_card(b))
    assert_false(b.draws_card(p))

    assert(b > p)


    b.clear()
    p.clear()

    eq_(len(p.cardpile), 0)
    eq_(len(b.cardpile), 0)
    
    c1,c2,c3,c4 = Card('8','h'), Card('8','s'), Card('4','d'), Card('K', 'c')

    p.add_card(c1)
    p.add_card(c2)
    b.add_card(c3)
    b.add_card(c4)

    assert_false(p.is_natural)
    assert_false(b.is_natural)

    eq_(p.score, 6)
    eq_(b.score, 4)

    assert_false(p.draws_card(b))
    assert(b.draws_card(p))

    assert(p > b)

    c1,c2,c3,c4 = Card('8','h'), Card('4','s'), Card('2','d'), Card('K', 'c')
    p = PlayerHand()
    b = BankHand()
    p.add_card(c1)
    p.add_card(c2)
    b.add_card(c3)
    b.add_card(c4)

    eq_(p.score, 2)
    eq_(b.score, 2)

    assert(p == b)

    assert(p.draws_card(b))
    p.add_card(Card('2','h'))
    assert(b.draws_card(p))
    b.add_card(Card('2','d'))
 
    eq_(p.score, 4)
    eq_(b.score, 4)

    assert(p == b)

def test_game():
    g = BaccaratGame()
    g.play()
    print g.winner
