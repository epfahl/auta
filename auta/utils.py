"""Utility library.
"""

import collections


def attrize(container_name=None, **dct):
    """Given a dict, return a named tuple where the values are accessible as
    named attributes.  A collection name can be given as an optional
    parameter.

    Examples
    --------
    >>> foo = attrize(**{'a': 1, 'b': 2})
    >>> foo.a
    1
    """
    if container_name is None:
        container_name = 'coll'
    return collections.namedtuple(container_name, dct.keys())(**dct)
