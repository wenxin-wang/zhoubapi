#!/bin/bash

__FILE__=$(readlink -e ${BASH_SOURCE[0]})
__DIR__=$(dirname $__FILE__)

delay=$1
__CONFIGS__=$2
__DATA__=$3

do_curl() {
    curl -S --silent "https://$domain.suprnova.cc/index.php?page=api&api_key=$key&action=$1"
}

do_suprnova() {
    do_curl get$1 | $__DIR__/suprnova.py $1 $username $coin
}

die() {
    kill $pid 2>/dev/null
    exit
}

query_user() {
    local conf=$1
    . $conf
    for coin in "${!coins[@]}"; do
        domain="${coins[$coin]}"
        do_suprnova userstatus &
        pid=$!
        sleep $delay
        wait
        do_suprnova userworkers &
        pid=$!
        sleep $delay
        wait
        do_suprnova userbalance &
        pid=$!
        sleep $delay
        wait
    done
}

trap die INT TERM

cd $__CONFIGS__
for c in suprnova*.sh; do
    query_user $c >$__DATA__/${c%.sh}.txt
done
