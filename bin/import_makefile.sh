#!/usr/bin/bash
path=`dirname "$0" | sed 's/\/bin$/\/makefiles/'`
[ -z "$1" ] && echo "Available Makefiles:" && ls $path && exit
cat $path/$1.makefile
