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

    def test_fancy_tree(self):
        logging.getLogger('').setLevel(logging.DEBUG)

        log = logging.getLogger('db')
        log.setLevel(logging.INFO)
        log.propagate = False
        log.addFilter(MyFilter())

        handler = logging.StreamHandler()
        log.addHandler(handler)
        handler.addFilter(logging.Filter('db.errors'))

        logging.getLogger('db.errors')
        logging.getLogger('db.stats')

        log = logging.getLogger('www.status')
        log.setLevel(logging.DEBUG)
        log.addHandler(logging.FileHandler('/foo/log.txt', delay=1))
        log.addHandler(MyHandler())

        printout()
        self.assertEqual(sys.stdout.getvalue(), '''\
    ""
    Level DEBUG
    |
    o   "db"
    |   Level INFO
    |   Propagate OFF
    |   Filter <MyFilter>
    |   Handler Stream %r
    |     Filter name='db.errors'
    |   |
    |   o<--"db.errors"
    |   |
    |   o<--"db.stats"
    |
    o<--[www]
        |
        o<--"www.status"
            Level DEBUG
            Handler File '/foo/log.txt'
            Handler <MyHandler>
''' % (sys.stderr,))


class MyFilter(logging.Filter):
    def __repr__(self):
        return '<MyFilter>'


class MyHandler(logging.Handler):
    def __init__(self):
        pass  # Avoid "__init__() must be called with Filterer instance" error

    def __repr__(self):
        return '<MyHandler>'
