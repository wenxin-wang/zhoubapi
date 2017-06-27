#!/bin/bash

__FILE__=$(readlink -e ${BASH_SOURCE[0]})
__DIR__=$(dirname $__FILE__)

delay=$1
__CONFIGS__=$2
__DATA__=$3

python $__DIR__/nicehash.py $delay $__CONFIGS__/nicehash.txt >$__DATA__/nicehash.txt
