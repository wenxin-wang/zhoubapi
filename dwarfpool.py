#!/usr/bin/python

import json
import sys


def main():
    username = sys.argv[1]
    coin = sys.argv[2]
    data = json.load(sys.stdin)
    if data['error']:
        return
    print(("dwarfpool.status,user=%s,coin=%s "
           "total_hashrate=%.2f,total_hashrate_calculated=%.2f") %
          (username, coin, data['total_hashrate'],
           data['total_hashrate_calculated']))

    for name, d in data['workers'].items():
        print(("dwarfpool.workers,user=%s,coin=%s,worker=%s,"
               "alive=%s,hashrate_below_threshold=%s "
               "hashrate_calculated=%.2f,second_since_submit=%di") %
              (username, coin, name, d['alive'], d['hashrate_below_threshold'],
               d['hashrate_calculated'], d['second_since_submit']))


if __name__ == '__main__':
    main()
