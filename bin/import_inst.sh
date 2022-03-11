#!/usr/bin/bash
path=`dirname "$0" | sed 's/\/bin$/\/inst/'`
[ -z "$1" ] && echo "Available Instantiation Templates:" && ls $path && exit
cat $path/$1
