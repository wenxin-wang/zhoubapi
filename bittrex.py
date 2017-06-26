#!/usr/bin/python

import json
import sys


def main():
    market = sys.argv[1]
    data = json.load(sys.stdin)['result']
    print(("bittrex,market=%s "
           "bid=%.5f,ask=%.5f,last=%.5f") %
          (market, data['Bid'], data['Ask'], data['Last']))


if __name__ == '__main__':
    main()
