===========
Mailcap Fix
===========

---------------

|pypi| |python| |travis-ci|

---------------

Summary
-------

The python standard library's implementation of
`mailcap <https://docs.python.org/3.5/library/mailcap.html>`_ is **broken** because
it does not respect the order in which mailcap entries are defined. Due to an
oversight in the implementation, wildcard entries are always evaluated last. 
This issue is documented on the bug tracker
`14977 <http://bugs.python.org/issue14977>`_.

*mailcap_fix* applies a minimal set of changes in order to fix this issue.

Installation
------------

.. code-block:: bash

    $ pip install mailcap_fix
    
Example
-------

Consider a mailcap file that contains the following two lines

::

    image/*; feh %s
    image/jpeg; eog %s

Because the **image/*** entry is defined first, it should take
precedence over the **image/jpeg** entry when searching for a match.

**Before**

.. code-block:: python

    >>> import mailcap
    >>> d = mailcap.getcaps()
    >>> # Incorrectly returns the second entry
    >>> mailcap.findmatch(d, 'image/jpeg', filename='test.jpg')
    ('eog test.jpg', {'view': 'eog %s'})

**After**

.. code-block:: python

    >>> import mailcap_fix as mailcap
    >>> d = mailcap.getcaps()
    >>> # Returns the correct wildcard entry
    >>> mailcap.findmatch(d, 'image/jpeg', filename='test.jpg')
    ('feh test.jpg', {'view': 'feh %s', 'lineno': 0})

Implementation
--------------

The mailcap module exposes two functions, ``findmatch()`` and ``getcaps()``.

``getcaps()`` adds a new field to each mailcap entry called ``lineno``. The
line number is persistent when loading from multiple mailcap files. For
instance, if **~/mailcap** is 10 lines long, **/etc/mailcap** will start
with line number 10.

``findmatch()`` then uses the line number to sort the entries in descending order
when searching for a match. For backwards compatibility, if the ``lineno`` is
not present entries will simply not be sorted.

RFC 1524 defines a whitelist of valid field names in mailcap, so the addition
of ``lineno`` should not conflict with any valid mailcap options.

Reference
---------

Relevant section of `RFC 1524 <https://tools.ietf.org/html/rfc1524>`_

    Location of Configuration Information

    Each user agent must clearly obtain the configuration information
    from a common location, if the same information is to be used to
    configure all user agents.  However, individual users should be able
    to override or augment a site's configuration.  The configuration
    information should therefore be obtained from a designated set of
    locations.  The overall configuration will be obtained through the
    virtual concatenation of several individual configuration files known
    as mailcap files.  **The configuration information will be obtained
    from the FIRST matching entry in a mailcap file**, where "matching"
    depends on both a matching content-type specification, an entry
    containing sufficient information for the purposes of the application
    doing the searching, and the success of any test in the "test="
    field, if present.
    
Timing
------

TODO

.. |python| image:: https://img.shields.io/badge/python-2.6%2C%202.7%2C%2032C%2pypy-blue.svg
    :target: https://pypi.python.org/pypi/mailcap_fix/
    :alt: Supported Python versions

.. |pypi| image:: https://img.shields.io/pypi/v/mailcap_fix.svg?label=version
    :target: https://pypi.python.org/pypi/mailcap_fix/
    :alt: Latest Version

.. |travis-ci| image:: https://travis-ci.org/michael-lazar/mailcap_fix.svg?branch=master
    :target: https://travis-ci.org/michael-lazar/mailcap_fix
    :alt: Build
