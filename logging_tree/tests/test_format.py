"""Tests for the `logging_tree.format` module."""

import logging
import logging.handlers
import sys
from logging_tree.format import printout
from logging_tree.tests.case import LoggingTestCase
from StringIO import StringIO

class FormatTests(LoggingTestCase):

    def setUp(self):
        self.stdout, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        sys.stdout = self.stdout
        # Looks like `logging` gives us no other way to reset it!
        reload(logging)
        reload(logging.handlers)  # force Handler subclasses to be rebuilt

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

    def test_all_handlers(self):
        ah = logging.getLogger('').addHandler
        ah(logging.handlers.RotatingFileHandler(
                '/bar/one.txt', maxBytes=10000, backupCount=3, delay=1))
        ah(logging.handlers.TimedRotatingFileHandler(
                '/bar/two.txt', delay=1))
        ah(logging.handlers.WatchedFileHandler(
                '/bar/three.txt', delay=1))
        ah(logging.handlers.SocketHandler(
                'server.example.com', 514))
        ah(logging.handlers.DatagramHandler(
                'server.example.com', 1958))
        ah(logging.handlers.SysLogHandler())
        ah(logging.handlers.SMTPHandler(
                'mail.example.com', 'Server', 'Sysadmin', 'Logs!'))
        # ah(logging.handlers.NTEventLogHandler())
        ah(logging.handlers.HTTPHandler(
                'api.example.com', '/logs', 'POST'))
        ah(logging.handlers.BufferingHandler(20000))
        ah(logging.handlers.MemoryHandler(
                30000, target=logging.StreamHandler()))
        printout()
        self.assertEqual(sys.stdout.getvalue(), '''\
    ""
    Level WARNING
    Handler RotatingFile '/bar/one.txt' maxBytes=10000 backupCount=3
    Handler TimedRotatingFile '/bar/two.txt' when='H' interval=3600 backupCount=0
    Handler WatchedFile '/bar/three.txt'
    Handler Socket server.example.com 514
    Handler Datagram server.example.com 1958
    Handler SysLog localhost:514 facility=1
    Handler SMTP via mail.example.com to ['Sysadmin']
    Handler HTTP POST to http://api.example.com//logs
    Handler Buffering capacity=20000
    Handler Memory capacity=30000
''')


class MyFilter(object):
    def __repr__(self):
        return '<MyFilter>'


class MyHandler(object):
    def __repr__(self):
        return '<MyHandler>'
