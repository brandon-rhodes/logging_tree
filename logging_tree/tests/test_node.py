"""Tests for the `logging_tree.node` module."""

import logging.handlers
import unittest
from logging_tree.nodes import tree
from logging_tree.tests.case import LoggingTestCase

class AnyPlaceHolder(object):
    def __eq__(self, other):
        return isinstance(other, logging.PlaceHolder)

any_placeholder = AnyPlaceHolder()

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
        b = logging.getLogger('a.b')
        self.assertEqual(tree(), (
                '', logging.root, [
                    ('a', any_placeholder, [
                            ('a.b', b, []),
                            ]),
                    ]))

    def test_default_trim_tree(self):
        self.assertEqual(tree(trim=True), ('', logging.root, []))

    def test_one_level_trim_tree(self):
        a = logging.getLogger('a')
        b = logging.getLogger('b')
        b.setLevel(logging.INFO)
        self.assertEqual(tree(trim=True), (
                '', logging.root, [
                    ('b', b, []),
                    ]))

    def test_two_level_trim_tree(self):
        a = logging.getLogger('a')
        a.setLevel(logging.INFO)
        b = logging.getLogger('a.b')
        c = logging.getLogger('c')
        d = logging.getLogger('c.d')
        d.setLevel(logging.INFO)
        self.assertEqual(tree(trim=True), (
                '', logging.root, [
                    ('a', a, []),
                    ('c', c, [
                            ('c.d', d, []),
                            ]),
                    ]))

    def test_two_level_trim_tree_with_placeholder(self):
        b = logging.getLogger('a.b')
        d = logging.getLogger('c.d')
        d.setLevel(logging.INFO)
        self.assertEqual(tree(trim=True), (
                '', logging.root, [
                    ('c', any_placeholder, [
                            ('c.d', d, []),
                            ]),
                    ]))

    def test_two_level_trim_tree_with_placeholder_and_nullhandler(self):
        a = logging.getLogger('a')
        a.addHandler(logging.StreamHandler())
        b = logging.getLogger('b')
        b.addHandler(logging.NullHandler())
        d = logging.getLogger('c.d')
        d.addHandler(logging.StreamHandler())
        f = logging.getLogger('e.f')
        f.addHandler(logging.NullHandler())
        g = logging.getLogger('g')
        g.addHandler(logging.NullHandler())
        h = logging.getLogger('g.h')
        h.addHandler(logging.NullHandler())
        self.assertEqual(tree(trim=True), (
                '', logging.root, [
                    ('a', a, []),
                    ('c', any_placeholder, [('c.d', d, [])]),
                    ]))


if __name__ == '__main__':  # for Python <= 2.4
    unittest.main()
