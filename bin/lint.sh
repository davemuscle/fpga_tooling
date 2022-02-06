#!/usr/bin/bash
for file in $(find . -maxdepth 1 -name "*.sv" -type f)
do
    verilator -Wall -lint-only $file
done
