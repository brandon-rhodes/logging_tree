"""Routines that pretty-print a hierarchy of logging `Node` objects."""

import logging.handlers


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
    prefix += ('    ' if is_last else '|   ')
    if not is_placeholder:
        facts = []
        if logger.level:
            facts.append('Level ' + logging.getLevelName(logger.level))
        if not logger.propagate:
            facts.append('Propagate OFF')

        # In case someone has defined a custom logger that lacks a
        # `filters` or `handlers` attribute, we call getattr() and
        # provide an empty sequence as a fallback.

        for f in getattr(logger, 'filters', ()):
            facts.append('Filter %s' % describe_filter(f))
        for h in getattr(logger, 'handlers', ()):
            facts.append('Handler %s' % describe_handler(h))
            for f in getattr(h, 'filters', ()):
                facts.append('  Filter %s' % describe_filter(f))

        for fact in facts:
            print prefix + fact

    if node.children:
        last_child = node.children[-1]
        for child in node.children:
            _printout(child, prefix, child is last_child)


# It is important that the 'if' statements in the "describe" functions
# below use `type(x) == Y` conditions instead of calling `isinstance()`,
# since a Filter or Handler subclass might implement arbitrary behaviors
# quite different from those of its superclass.


def describe_filter(f):
    """Return text describing the logging filter `f`."""
    if type(f) is logging.Filter:
        return 'name=%r' % f.name
    return repr(f)


handler_formats = {  # Someday we will switch to .format() when Py2.6 is gone.
    logging.StreamHandler: 'Stream %(stream)r',
    logging.FileHandler: 'File %(baseFilename)r',
    logging.handlers.RotatingFileHandler: 'RotatingFile %(baseFilename)r'
        ' maxBytes=%(maxBytes)r backupCount=%(backupCount)r',
    logging.handlers.TimedRotatingFileHandler:
        'TimedRotatingFile %(baseFilename)r when=%(when)r'
        ' interval=%(interval)r backupCount=%(backupCount)r',
    logging.handlers.WatchedFileHandler: 'WatchedFile %(baseFilename)r',
    logging.handlers.SocketHandler: 'Socket %(host)s %(port)r',
    logging.handlers.DatagramHandler: 'Datagram %(host)s %(port)r',
    logging.handlers.SysLogHandler: 'SysLog %(address)r facility=%(facility)r',
    logging.handlers.SMTPHandler: 'SMTP via %(mailhost)s to %(toaddrs)s',
    logging.handlers.HTTPHandler: 'HTTP %(method)s to http://%(host)s/%(url)s',
    logging.handlers.BufferingHandler: 'Buffering capacity=%(capacity)r',
    # TODO: recursively examine the next handler down
    logging.handlers.MemoryHandler: 'Memory capacity=%(capacity)r',
    }


def describe_handler(h):
    """Return text describing the logging handler `h`."""
    format = handler_formats.get(type(h))
    if format is not None:
        return format % h.__dict__
    return repr(h)
