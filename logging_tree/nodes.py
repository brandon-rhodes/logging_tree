"""Routine that explores the `logging` hierarchy and builds a `Node` tree."""

import logging


def tree():
    """Return a tree of tuples representing the logger layout.

    Each tuple looks like ``('logger-name', <Logger>, [...])`` where the
    third element is a list of zero or more child tuples that share the
    same layout.

    """
    loggers = [
        logger for _, logger in
        sorted(logging.root.manager.loggerDict.items())
        if not isinstance(logger, logging.PlaceHolder)
    ]

    children = {}
    for logger in loggers:
        children.setdefault(logger.parent, [])
        children[logger.parent].append(logger)

    def get_tuple(logger):
        """Recursive function to get logger tuples."""
        child_tuples = [get_tuple(child) for child in children.get(logger, [])]
        logger_name = logger.name
        if logger == logging.root:
            logger_name = ''
        return (logger_name, logger, child_tuples)

    return get_tuple(logging.root)
