#!/bin/bash

__FILE__=$(readlink -e ${BASH_SOURCE[0]})
__DIR__=$(dirname $__FILE__)

__INSTANCE__=$__DIR__/instance
__CONFIGS__=${CONFIGS:-$__INSTANCE__/configs}

__PIDS__=$__INSTANCE__/pids

die() {
    local pid
    while read -r pid; do
        kill $pid 2>/dev/null
    done < <(cat $__PIDS__)
    exit
}

. $__CONFIGS__/common.sh

trap die INT TERM

while true; do
    __DATA__=$__INSTANCE__/$(date +%F)/$(date +%H-%M-%S)
    mkdir -p $__DATA__
    echo -n >$__PIDS__

    echo new round
    for site in "${!delays[@]}"; do
        $__DIR__/$site.sh "${delays[$site]}" $__CONFIGS__ $__DATA__  &
        echo $! >>$__PIDS__
    done
    sleep $interval
    wait
    echo sending data
    curl -S --silent -XPOST "$INFLUX_URL" -u "$INFLUX_AUTH" \
         --data-binary "$(cat $__DATA__/*.txt)" &
done
