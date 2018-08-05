#!/bin/bash

set -e

python3 setup.py sdist upload || true

sed -i '1iimport setuptools' setup.py
python3 setup.py bdist_wheel upload || true
git checkout setup.py
rm -r build logging_tree.egg-info
