#!/bin/bash
#
# This merely tests that `logging_tree` works when run directly from
# source (and, of course, only tests the versions of Python you happen
# to have installed with pyenv).  For a comprehensive test of whether it
# will actually work if installed from its distribution, see `tox.ini`.

for python in ~/.pyenv/versions/*/bin/python
do
    echo
    echo ======================================================================
    echo $python
    echo ======================================================================
    for test in logging_tree/tests/test_*.py
    do
        PYTHONPATH=. $python $test
    done
done
