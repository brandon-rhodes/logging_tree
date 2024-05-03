#!/bin/bash

set -e

PYTHONDONTWRITEBYTECODE= python -m build .
rm -rf logging_tree.egg-info
echo
echo Now run: twine upload ...  for both the new files in build/
