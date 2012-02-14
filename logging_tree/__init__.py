"""Introspection for the ``logging`` logger tree in the Standard Library.

While you can write programs that call this package's ``tree()``
function and examine the hierarchy of logger objects that it finds
inside of the Standard Library ``logging`` module, the simplest use of
this package for debugging is to call ``printout()`` to print the
loggers, filters, and handlers that your application has configured::

    >>> logging.getLogger('a')
    >>> logging.getLogger('a.b').setLevel(logging.DEBUG)
    >>> logging.getLogger('x.c')
    >>> from logging_tree import printout
    >>> printout()
       ""
       Level WARNING
       |
       o<--"a"
       |   |
       |   o<--"a.b"
       |       Level DEBUG
       |
       o<--[x]
           |
           o<--"x.c"

The logger tree should always print successfully, no matter how
complicated.  A node whose ``[name]`` is in square brackets is a "place
holder" that has never actually been named in a ``getLogger()`` call,
but was created automatically to serve as the parent of loggers further
down the tree.

There are several interfaces that ``logging_tree`` supports, depending
on how much detail you need.

``logging_tree.printout(node=None)``

    Prints the current logger tree, or the tree based at the given
    `node`, to the standard output.

``logging_tree.format.build_description(node=None)``

    Builds and returns the multi-line description of the current logger
    tree, or the tree based at the given ``node``, as a single string
    with newlines inside and a newline at the end.

``logging_tree.format.describe(node)``

    A generator that yields a series of lines that describe the tree
    based at the given ``node``.  Note that the lines are returned
    without newline terminators attached.

``logging_tree.tree()``

    Fetch the current tree of loggers from the ``logging`` module.
    Returns a namedtuple of type ``logging_tree.nodes.Node`` with three
    fields:

    | ``node.name`` = the logger name (``""`` for the root logger).
    | ``node.logger`` = the ``logging.Logger`` object itself.
    | ``node.children`` = a list of zero or more child nodes.

I owe great thanks to `Rover Apps <http://roverapps.com/>`_ for letting
me release this general-purpose tool, whose core logic I developed while
working on one of their projects.  They care about the Python community!

I welcome contributions and ideas as this package matures.  You can find
the bug tracker at the `repository page on github
<https://github.com/brandon-rhodes/logging_tree>`_.  Developers can run
this package's tests with::

    $ python -m unittest discover logging_tree

On older versions of Python you will instead have to install
``unittest2`` and use its ``unit2`` command line tool to run the tests.

Changelog
---------

**Version 1.0** - 2012 February 13
    Can display the handler inside a MemoryHandler; entire public
    interface documented; 100% test coverage.

**Version 0.6** - 2012 February 10
    Added a display format for every ``logging.handlers`` class.

**Version 0.5** - 2012 February 8
    Initial release.

"""
__version__ = '1.0'
__all__ = ('Node', 'tree', 'printout')

from logging_tree.nodes import Node, tree
from logging_tree.format import printout
