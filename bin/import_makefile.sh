#!/usr/bin/bash
path=`dirname "$0" | sed 's/\/bin$/\/makefiles/'`/$1.makefile
cp $path Makefile && echo "Succeded importing makefile" || echo "Failed importing makefile"
