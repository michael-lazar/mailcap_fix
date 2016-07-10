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
it does not respect the order of entries in mailcap files. This is due to an
oversight where wildcard entries are always evaluated last. *mailcap_fix* applies
a minimal set of changes in order to fix this issue.

Reference
---------

This issue is documented on the bug tracker in
`14977 <http://bugs.python.org/issue14977>`_.

Relevant section of `RFC 1524 <https://tools.ietf.org/html/rfc1524>`_ -

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

Example
-------

Consider a mailcap file that contains only the following two lines

::

    image/*; feh %s
    image/jpeg; eog %s

Because the **image/*** entry is defined first, it should take
precedence over the **image/jpeg** entry.

**Before**

.. code-block:: python

    >>> # Incorrectly returns the second entry
    >>> import mailcap
    >>> d = mailcap.getcaps()
    >>> mailcap.findmatch(d, 'image/jpeg', filename='test.jpg')
    ('eog test.jpg', {'view': 'eog %s'})

**After**

.. code-block:: python

    >>> import mailcap_fix as mailcap
    >>> d = mailcap.getcaps()
    >>> mailcap.findmatch(d, 'image/jpeg', filename='test.jpg')
    ('hef test.jpg', {'view': 'feh %s', 'lineno': 0})

Implementation
--------------

The mailcap module exposes two functions, ``findmatch()`` and ``getcaps()``.

``getcaps()`` adds a new field to each mailcap entry called ``lineno``. The
line number is persistent when loading from multiple mailcap files. For
instance, if ``~/mailcap`` is 10 lines long, ``/etc/mailcap`` will apply an
offset of 10 to its first ``lineno``.

``findmatch()`` then uses the field to sort the entries in descending order
when searching for a match. For backwards compatibility, if the ``lineno`` is
not present, entries will simply not be sorted.

RFC 1524 defines a whitelist of valid field names in mailcap, so the addition
of ``lineno`` should not conflict with any of the valid options.

Installation
------------

.. code-block:: bash

    $ pip install mailcap_fix

Timing
------

TODO

.. |python| image:: https://img.shields.io/badge/python-2.7%2C%203.5-blue.svg
    :target: https://pypi.python.org/pypi/mailcap_fix/
    :alt: Supported Python versions

.. |pypi| image:: https://img.shields.io/pypi/v/rtv.svg?label=version
    :target: https://pypi.python.org/pypi/mailcap_fix/
    :alt: Latest Version

.. |travis-ci| image:: https://travis-ci.org/michael-lazar/mailcap_fix.svg?branch=master
    :target: https://travis-ci.org/michael-lazar/mailcap_fix
    :alt: Build
