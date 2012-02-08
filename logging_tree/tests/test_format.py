"""Tests for the `logging_tree.format` module."""

import logging
import sys
from logging_tree.format import printout
from unittest import TestCase
from StringIO import StringIO

class FormatTests(TestCase):

    def setUp(self):
        self.stdout, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        sys.stdout = self.stdout
        # Looks like `logging` gives us no other way to reset it!
        reload(logging)

    def test_simple_tree(self):
        logging.getLogger('a')
        logging.getLogger('a.b').setLevel(logging.DEBUG)
        logging.getLogger('x.c')
        printout()
        self.assertEqual(sys.stdout.getvalue(), '''\
    ""
    Level WARNING
    |
    o<--"a"
    |   |
    |   o<--"a.b"
    |       Level DEBUG
    |
    o<--[x]
        |
        o<--"x.c"
''')
