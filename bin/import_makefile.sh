#!/usr/bin/bash
path=`dirname "$0" | sed 's/\/bin$/\/makefiles/'`/$1.makefile
cp -i $path Makefile && echo "Succeded importing makefile" || echo "Failed importing makefile"
