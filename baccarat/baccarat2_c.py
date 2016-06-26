'''Cython version - run python setup.py build_ext --inplace first to get
   the .so
'''

import time
import timeit
from shared import parsed_args
from baccarat_ext2 import play

if __name__ == '__main__':
    args = parsed_args()

    if args.timing == 'timediff':
        start = time.time()
        results = play(args.games)
        end = time.time()
        print 'v2,{},{}'.format(args.games,end-start)
    elif args.timing == 'time':
        results = play(args.games)
        print 'v2,{}'.format(args.games)
    elif args.timing == 'timeit':
        t = timeit.Timer("play(%s)" % args.games, "from __main__ import play")
        seconds = t.timeit()
        print 'v2,{},{}'.format(args.games,seconds)
