"""Tests for the `logging_tree.node` module."""

import logging
from logging_tree.nodes import tree
from unittest import TestCase

class AnyPlaceHolder(object):
    def __eq__(self, other):
        return isinstance(other, logging.PlaceHolder)

any_placeholder = AnyPlaceHolder()

class NodeTests(TestCase):

    def tearDown(self):
        # Looks like `logging` gives us no other way to reset it!
        reload(logging)

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
        b = logging.getLogger('a.b')
        self.assertEqual(tree(), (
                '', logging.root, [
                    ('a', any_placeholder, [
                            ('a.b', b, []),
                            ]),
                    ]))
