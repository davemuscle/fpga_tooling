#!/usr/bin/bash
path=`dirname "$0" | sed 's/\/bin$/\/rtl/'`
[ -z "$1" ] && echo "Available RTL Modules:" && ls $path && exit
cat $path/$1
