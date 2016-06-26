def parsed_args():
    import argparse
    timings = ('time', 'timediff', 'timeit')

    parser = argparse.ArgumentParser(description='Play Some Baccarat')
    parser.add_argument('timing', metavar='N', type=str,
                        help='one of time, timediff')
    parser.add_argument('games', metavar='N', type=int)
    args = parser.parse_args()
    if args.timing not in timings:
        raise Exception('bad timing argument')

    return args


def format_result(type_, args, results):
    return '%s,%s,%s,%s,%s,%s' % (type_, args.timing, args.games,
                                  results['bank'], results['player'],
                                  results['tie'])


def play_threads(func, hands, decks=8, threadnum=6):
    import threading
    thands = hands / threadnum
    extra = hands % threadnum

    threads = []
    for i in range(threadnum):
        threads.append(threading.Thread(target=func, args=(thands, decks)))
    threads.append(threading.Thread(target=func, args=(extra, decks)))

    for t in threads:
        t.start()
        t.join()


def play_multiprocessing(func, hands, decks=8, procnum=6):
    from multiprocessing import Process

    thands = hands / procnum
    extra = hands % procnum

    procs = []
    for i in range(procnum):
        procs.append(Process(target=func, args=(thands, decks)))
    procs.append(Process(target=func, args=(extra, decks)))

    for t in procs:
        t.start()
        t.join()
