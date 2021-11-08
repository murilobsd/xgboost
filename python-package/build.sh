#!/bin/sh

python setup.py build_ext --inplace
python setup.py install
python test_bench.py "boavista"
