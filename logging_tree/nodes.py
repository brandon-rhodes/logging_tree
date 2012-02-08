"""Routines that mix down the `logging` hierarchy into `Node` tuples."""

import logging
from collections import namedtuple

Node = namedtuple('Node', 'name logger children')

def tree():
    """Return a tree of `Node` tuples representing the logger layout."""
    root = Node('', logging.root, [])
    nodes = {}
    for name, logger in sorted(logging.root.manager.loggerDict.iteritems()):
        nodes[name] = node = Node(name, logger, [])
        i = name.rfind('.', 0, len(name) - 1)  # same formula used in `logging`
        parent = root if i == -1 else nodes[name[:i]]
        parent.children.append(node)
    return root
