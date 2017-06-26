#!/bin/bash

__FILE__=$(readlink -e ${BASH_SOURCE[0]})
__DIR__=$(dirname $__FILE__)

delay=$1
__CONFIGS__=$2
__DATA__=$3

do_curl() {
    curl -S --silent "https://bittrex.com/api/v1.1/public/getticker?market=$1"
}

do_bittrex() {
    do_curl $market | $__DIR__/bittrex.py $market
}

die() {
    kill $pid 2>/dev/null
    exit
}

query_markets() {
    local conf=$1
    . $conf
    for market in $markets; do
        do_bittrex $market &
        pid=$!
        sleep $delay
        wait
    done
}

trap die INT TERM

cd $__CONFIGS__
query_markets bittrex.sh >$__DATA__/bittrex.txt
