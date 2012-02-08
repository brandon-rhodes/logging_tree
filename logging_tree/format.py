"""Routines that pretty-print a hierarchy of logging `Node` objects."""

import logging


def printout(node=None):
    """Print the tree of `Node` tuples whose root is `node`.

    If no `node` is provided, the entire tree of loggers is printed out.

    """
    if node is None:
        from logging_tree.nodes import tree
        node = tree()
    _printout(node)


def _printout(node, prefix='', is_last=True):
    logger = node.logger
    is_placeholder = isinstance(logger, logging.PlaceHolder)
    name = ('[%s]' if is_placeholder else '"%s"') % node.name
    if prefix:
        print prefix + '|'
        arrow = '<--' if (is_placeholder or logger.propagate) else '   '
        print prefix + 'o' + arrow + name
    else:
        print '    ' + name
    leader = prefix + ('    ' if is_last else '|   ')
    if not is_placeholder:
        facts = []
        if logger.level:
            facts.append('Level ' + logging.getLevelName(logger.level))
        if not logger.propagate:
            facts.append('Propagate OFF')
        for f in logger.filters:
            facts.append('Filter %s' % describe_filter(f))
        for h in logger.handlers:
            facts.append('Handler %s' % describe_handler(h))
        for fact in facts:
            print leader + fact
    if node.children:
        last_child = node.children[-1]
        for child in node.children:
            _printout(child, leader, child is last_child)


def describe_filter(f):
    """Return text describing the logging filter `f`."""
    # TODO
    return f.__class__.__name__


def describe_handler(h):
    """Return text describing the logging handler `h`."""
    if isinstance(h, logging.StreamHandler):
        return 'Stream %r' % h.stream
    # TODO: add further cases here.
    return h.__class__.__name__
