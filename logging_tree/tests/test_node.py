"""Tests for the `logging_tree.node` module."""

import logging.handlers
import unittest
from logging_tree.nodes import tree
from logging_tree.tests.case import LoggingTestCase

class NodeTests(LoggingTestCase):

    def test_default_tree(self):
        self.assertEqual(tree(), ('', logging.root, []))

    def test_one_level_tree(self):
        a = logging.getLogger('a')
        b = logging.getLogger('b')
        self.assertEqual(tree(), (
                '', logging.root, [
                    ('a', a, []),
                    ('b', b, []),
                    ]))

    def test_two_level_tree(self):
        a = logging.getLogger('a')
        b = logging.getLogger('a.b')
        self.assertEqual(tree(), (
                '', logging.root, [
                    ('a', a, [
                            ('a.b', b, []),
                            ]),
                    ]))

    def test_two_level_tree_with_placeholder(self):
        # Place holders are now ignored in tree view
        b = logging.getLogger('a.b')
        self.assertEqual(tree(), (
                '', logging.root, [
                    ('a.b', b, []),
                    ]))

    def test_overridden_parent(self):
        a = logging.getLogger('a')
        b = logging.getLogger('b')
        b.parent = a

        self.assertEqual(tree(), (
                '', logging.root, [
                    ('a', a, [
                        ('b', b, []),
                        ]),
                    ]))


if __name__ == '__main__':  # for Python <= 2.4
    unittest.main()
