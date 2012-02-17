"""Tests for the `logging_tree.format` module."""

import logging
import logging.handlers
import unittest
import sys
from logging_tree.format import build_description, printout
from logging_tree.tests.case import LoggingTestCase
if sys.version_info >= (3,):
    from io import StringIO
else:
    from StringIO import StringIO


class FakeFile(StringIO):
    def __init__(self, filename, mode):
        self.filename = filename
        StringIO.__init__(self)

    def __repr__(self):
        return '<file %r>' % self.filename


class FormatTests(LoggingTestCase):

    def setUp(self):
        # Prevent logging file handlers from trying to open real files.
        # (The keyword delay=1, which defers any actual attempt to open
        # a file, did not appear until Python 2.6.)
        logging.open = FakeFile
        super(FormatTests, self).setUp()

    def tearDown(self):
        del logging.open
        super(FormatTests, self).tearDown()

    def test_printout(self):
        stdout, sys.stdout = sys.stdout, StringIO()
        printout()
        self.assertEqual(sys.stdout.getvalue(), '<--""\n   Level WARNING\n')
        sys.stdout = stdout

    def test_simple_tree(self):
        logging.getLogger('a')
        logging.getLogger('a.b').setLevel(logging.DEBUG)
        logging.getLogger('x.c')
        self.assertEqual(build_description(), '''\
<--""
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
        log.addHandler(logging.FileHandler('/foo/log.txt'))
        log.addHandler(MyHandler())

        self.assertEqual(build_description(), '''\
<--""
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

    def test_most_handlers(self):
        ah = logging.getLogger('').addHandler
        ah(logging.handlers.RotatingFileHandler(
                '/bar/one.txt', maxBytes=10000, backupCount=3))
        ah(logging.handlers.SocketHandler('server.example.com', 514))
        ah(logging.handlers.DatagramHandler('server.example.com', 1958))
        ah(logging.handlers.SysLogHandler())
        ah(logging.handlers.SMTPHandler(
                'mail.example.com', 'Server', 'Sysadmin', 'Logs!'))
        # ah(logging.handlers.NTEventLogHandler())
        ah(logging.handlers.HTTPHandler('api.example.com', '/logs', 'POST'))
        ah(logging.handlers.BufferingHandler(20000))
        sh = logging.StreamHandler()
        ah(logging.handlers.MemoryHandler(30000, target=sh))
        self.assertEqual(build_description(), '''\
<--""
   Level WARNING
   Handler RotatingFile '/bar/one.txt' maxBytes=10000 backupCount=3
   Handler Socket server.example.com 514
   Handler Datagram server.example.com 1958
   Handler SysLog ('localhost', 514) facility=1
   Handler SMTP via mail.example.com to ['Sysadmin']
   Handler HTTP POST to http://api.example.com//logs
   Handler Buffering capacity=20000
   Handler Memory capacity=30000 dumping to:
     Handler Stream %r
''' % (sh.stream,))
        logging.getLogger('').handlers[3].socket.close()  # or Python 3 warning

    def test_2_dot_5_handlers(self):
        if sys.version_info < (2, 5):
            return
        ah = logging.getLogger('').addHandler
        ah(logging.handlers.TimedRotatingFileHandler('/bar/two.txt'))
        self.assertEqual(build_description(), '''\
<--""
   Level WARNING
   Handler TimedRotatingFile '/bar/two.txt' when='H' interval=3600 backupCount=0
''')

    def test_2_dot_6_handlers(self):
        if sys.version_info < (2, 6):
            return
        ah = logging.getLogger('').addHandler
        ah(logging.handlers.WatchedFileHandler('/bar/three.txt'))
        self.assertEqual(build_description(), '''\
<--""
   Level WARNING
   Handler WatchedFile '/bar/three.txt'
''')

    def test_nested_handlers(self):
        h1 = logging.StreamHandler()

        h2 = logging.handlers.MemoryHandler(30000, target=h1)
        h2.addFilter(logging.Filter('worse'))

        h3 = logging.handlers.MemoryHandler(30000, target=h2)
        h3.addFilter(logging.Filter('bad'))

        logging.getLogger('').addHandler(h3)

        self.assertEqual(build_description(), '''\
<--""
   Level WARNING
   Handler Memory capacity=30000 dumping to:
     Filter name='bad'
     Handler Memory capacity=30000 dumping to:
       Filter name='worse'
       Handler Stream %r
''' % (h1.stream,))


class MyFilter(object):
    def __repr__(self):
        return '<MyFilter>'


class MyHandler(object):
    def __repr__(self):
        return '<MyHandler>'


if __name__ == '__main__':  # for Python <= 2.4
    unittest.main()
