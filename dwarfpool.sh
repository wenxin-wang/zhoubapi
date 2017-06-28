#!/bin/bash

__FILE__=$(readlink -e ${BASH_SOURCE[0]})
__DIR__=$(dirname $__FILE__)

delay=$1
__CONFIGS__=$2
__DATA__=$3

do_curl() {
    curl -S --silent "http://dwarfpool.com/$url/api?wallet=$wallet&email=$email"
}

do_dwarfpool() {
    do_curl | $__DIR__/dwarfpool.py $username $coin
}

die() {
    kill $pid 2>/dev/null
    exit
}

query_user() {
    local conf=$1
    . $conf
    for coin in "${!coins[@]}"; do
        url="${coins[$coin]}"
        do_dwarfpool &
        pid=$!
        sleep $delay
        wait
    done
}

trap die INT TERM

cd $__CONFIGS__
for c in dwarfpool*.sh; do
    query_user $c >$__DATA__/${c%.sh}.txt
done
