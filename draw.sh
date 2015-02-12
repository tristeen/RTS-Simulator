#!/bin/sh

python -m cProfile -o profile.pstats main.py
gprof2dot -f pstats profile.pstats | dot -Tsvg -o mine.svg
