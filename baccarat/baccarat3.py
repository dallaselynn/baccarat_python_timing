import random
import time
import timeit
from array import array
from shared import parsed_args

VALUES = array('B', (
    1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0
))

NATURALS = (8,9)

def play(decks=8, hands=100):
    results = dict(banker=0, punter=0, draw=0)

    s = VALUES * decks
    random.shuffle(s)

    for i in range(hands):
        if len(s) < 6:
            s = VALUES * decks
            random.shuffle(s)
            
        banker, punter = [s.pop(), s.pop()], [s.pop(), s.pop()]
        banker_points, punter_points = sum(banker) % 10, sum(punter) % 10
        
        if not (banker_points in NATURALS or punter_points in NATURALS) and \
           punter_points <= 5:
            punter.append(s.pop())
            punter_points = sum(punter) % 10
            
        if len(punter) == 2:
            if banker_points <= 5:
                banker.append(s.pop())
                banker_points = sum(banker) % 10
        else:
            if banker_points <= 2:
                banker.append(s.pop())
            elif banker_points == 3 and punter[2] != 8:
                banker.append(s.pop())
            elif banker_points == 4 and punter[2] not in (0,1,8,9):
                banker.append(s.pop())
            elif banker_points == 5 and punter[2] in (4,5,6,7):
                banker.append(s.pop())
            elif banker_points == 6 and punter[2] in (6,7):
                banker.append(s.pop())

            banker_points = sum(banker) % 10

        if banker_points > punter_points:
            results['banker'] += 1
        elif punter_points > banker_points:
            results['punter'] += 1
        else:
            results['draw'] += 1
            
    return results

if __name__ == '__main__':
    args = parsed_args()
    if args.timing == 'timediff':
        start = time.time()
        results = play(args.games)
        end = time.time()
        print 'v3,{},{}'.format(args.games,end-start)
    elif args.timing == 'time':
        results = play(args.games)
        print 'v3,{}'.format(args.games)
    elif args.timing == 'timeit':
        t = timeit.Timer("play(%s)" % args.games, "from __main__ import play")
        seconds = t.timeit()
        print ','.join(('v3', args.games, seconds))
