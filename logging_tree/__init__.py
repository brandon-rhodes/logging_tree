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
holder" that has never actually been named in a ``getLogger()`` call.
At the moment handlers and filters are not printed out in a terribly
informative manner, but this will improve as I continue to code.

I owe great thanks to `Rover Apps <http://roverapps.com/>`_ for letting
me release this.  I developed the core logic that powers this package on
their time, but they are letting me retain the copyright and distribute
it to the community!

This package is still under construction and under-documented, but even
this primitive release will hopefully help a few of you.  I welcome
contributions and ideas as this package matures!  You can find the bug
tracker at the `repository page on github <https://github.com/brandon-rhodes/logging_tree>`_.
Developers can run this package's tests with::

    $ python -m unittest discover logging_tree

On older versions of Python you will instead have to install
``unittest2`` and use its ``unit2`` command line tool to run the tests.

Changelog
---------

**Version 0.6** - 2012 February 10
    Added a display format for every ``logging.handlers`` class.

**Version 0.5** - 2012 February 8
    Initial release.

"""
__version__ = '0.6'
__all__ = ('Node', 'tree', 'printout')

from logging_tree.nodes import Node, tree
from logging_tree.format import printout
