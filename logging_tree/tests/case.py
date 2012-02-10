"""Common test class for `logging` tests."""

import logging.handlers
import unittest

class LoggingTestCase(unittest.TestCase):

    def tearDown(self):
        # Because most classes in `logging.handlers` are subclasses of
        # `logging.Handler`, we always need to reload both modules in
        # tandem or cause subsequent tests to fail with errors like:
        #
        # TypeError: unbound method __init__() must be called with
        # FileHandler instance as first argument (got
        # RotatingFileHandler instance instead)

        reload(logging)           # pragma: no cover
        reload(logging.handlers)  # pragma: no cover
