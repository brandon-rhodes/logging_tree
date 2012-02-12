"""Common test class for `logging` tests."""

import logging.handlers
import unittest

class LoggingTestCase(unittest.TestCase):
    """Test case that knows the secret: how to reset the logging module."""

    def tearDown(self):
        logging.root = logging.RootLogger(logging.WARNING)
        logging.Logger.root = logging.root
        logging.Logger.manager = logging.Manager(logging.Logger.root)
