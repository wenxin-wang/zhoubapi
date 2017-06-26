#!/usr/bin/python

import json
import sys


def main():
    action = 'get' + sys.argv[1]
    username = sys.argv[2]
    coin = sys.argv[3]
    data = json.load(sys.stdin)[action]['data']
    if action == 'getuserstatus':
        shares = data['shares']
        print(("suprnova.status,user=%s,coin=%s "
               "hashrate=%.2f,sharerate=%.2f,valid=%.5f,invalid=%.5f") %
              (username, coin, data['hashrate'], data['sharerate'],
               shares['valid'], shares['invalid']))
    elif action == 'getuserworkers':
        for d in data:
            worker = d['username'].split('.')[1]
            print(("suprnova.workers,user=%s,coin=%s,worker=%s "
                   "count_all=%d,shares=%.5f,hashrate=%.2f,difficulty=%.2f") %
                  (username, coin, worker, d['count_all'], d['shares'],
                   d['hashrate'], d['difficulty']))
    elif action == 'getuserbalance':
        print(("suprnova.balance,user=%s,coin=%s "
               "confirmed=%.5f,unconfirmed=%.5f,orphaned=%.5f") %
              (username, coin, data['confirmed'], data['unconfirmed'],
               data['orphaned']))


if __name__ == '__main__':
    main()
