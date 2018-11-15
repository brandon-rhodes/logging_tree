"""Routine that explores the `logging` hierarchy and builds a `Node` tree."""

import logging

def tree(trim=False):
    """Return a tree of tuples representing the logger layout.

    Each tuple looks like ``('logger-name', <Logger>, [...])`` where the
    third element is a list of zero or more child tuples that share the
    same layout.

    """
    root = ('', logging.root, [])
    nodes = {}
    items = list(logging.root.manager.loggerDict.items())  # for Python 2 and 3
    items.sort()
    for name, logger in items:
        nodes[name] = node = (name, logger, [])
        i = name.rfind('.', 0, len(name) - 1)  # same formula used in `logging`
        if i == -1:
            parent = root
        else:
            parent = nodes[name[:i]]
        parent[2].append(node)
    if trim:
        root = trim_tree(root)
    return root


def trim_tree(node=None, trim_nullhandlers=True):
    """Remove nodes that don't modify any logging configuration from tree."""
    if node is None:
        node = tree()
    name, logger, children = node
    children = list(filter(None, map(trim_tree, children)))
    handlers = getattr(logger, 'handlers', ())
    if trim_nullhandlers:
        handlers = [handler for handler in handlers
                    if not isinstance(handler, logging.NullHandler)]
    if (
        not children
        and (
            isinstance(logger, logging.PlaceHolder)
            or (
                not logger.disabled
                and logger.propagate
                and logger.level == logging.NOTSET
                and not getattr(logger, 'filters', ())
                and not handlers
            )
        )
    ):
        return None
    return name, logger, children
