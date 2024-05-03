#!/bin/bash
#
# This merely tests that `logging_tree` works when run directly from
# source (and, of course, only tests the versions of Python you happen
# to have installed with pyenv).  For a comprehensive test of whether it
# will actually work if installed from its distribution, see `tox.ini`.

errors=0

for python in $(ls ~/.pyenv/versions/*/bin/python | sort -t. -k 2,2 -k 3n)
do
    echo
    echo ======================================================================
    echo $python
    echo ======================================================================
    for test in logging_tree/tests/test_*.py
    do
        if ! PYTHONPATH=. $python $test
        then
            let "errors=errors+1"
        fi
    done
done

echo
echo "Failure count: $errors"
