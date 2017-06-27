#!/usr/bin/python

import json
import sys
import time
from subprocess import Popen, PIPE

api_url = 'https://api.nicehash.com/api?'


def get_url(method, **params):
    if params:
        ps = ['%s=%s' % (k, v) for k, v in params.items()]
        params = '&' + '&'.join(ps)
    else:
        params = ''
    return api_url + 'method=%s' % method + params


def do_curl(delay, method, **params):
    p = Popen(
        ['curl', '-S', '--silent',
         get_url(method, **params)],
        universal_newlines=True,
        stdout=PIPE)
    time.sleep(delay)
    p.wait()
    return json.load(p.stdout)['result']


def print_algos(algos):
    algo_list = ['' for _ in range(len(algos))]
    for algo in algos:
        print(("nicehash.prices,coin=%s price=%s") % (algo['name'],
                                                      algo['paying']))
        algo_list[algo['algo']] = algo['name']
    return algo_list


def print_stats(user, stats, algo_list):
    for algo in stats:
        print(("nicehash.balance,user=%s,coin=%s "
               "balance=%s,accepted_speed=%s,rejected_speed=%s") %
              (user, algo_list[algo['algo']], algo['balance'],
               algo['accepted_speed'], algo['rejected_speed']))


def do_user(delay, user, addr):
    algos = do_curl(delay, 'simplemultialgo.info')['simplemultialgo']
    algo_list = print_algos(algos)
    stats = do_curl(delay, 'stats.provider', addr=addr)['stats']
    print_stats(user, stats, algo_list)


def main():
    delay = float(sys.argv[1])
    flist = sys.argv[2]
    with open(flist) as f:
        for line in f.readlines():
            user, addr = line.rstrip().split(" ")
            do_user(delay, user, addr)


if __name__ == '__main__':
    main()
