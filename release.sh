#!/bin/bash

set -e

PYTHONDONTWRITEBYTECODE= python -m build .
echo
echo Now run: twine upload ...  for both the new files in build/
