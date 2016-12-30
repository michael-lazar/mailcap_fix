===========
Mailcap Fix
===========

|pypi| |python| |travis-ci|

| **Note**
| A fix has now been merged into `Python 3.6.0 <https://docs.python.org/3.6/whatsnew/changelog.html>`_.
| This package remains as a backport for previous versions.

Summary
-------

This package patches the python standard library's 
`mailcap <https://docs.python.org/3.5/library/mailcap.html>`_ module in order
to correctly handle windcard entries.

The bug is documented on the bug tracker here: `issue 14977 <http://bugs.python.org/issue14977>`_

Installation
------------

.. code-block:: bash

    $ pip install mailcap-fix
    
Example
-------

Consider a mailcap file that contains the following two lines

::

    image/*; feh %s
    image/jpeg; eog %s

Because the **image/*** entry is defined first, it should take
precedence over the **image/jpeg** entry when searching for a match.
This behavior is defined by `RFC 1524 <https://tools.ietf.org/html/rfc1524>`_.
However, the standard library's implementation will always evaluate
wildcard entries last.

**Before**

.. code-block:: python

    >>> import mailcap
    >>> d = mailcap.getcaps()
    >>> # Incorrectly returns the second entry
    >>> mailcap.findmatch(d, 'image/jpeg', filename='test.jpg')
    ('eog test.jpg', {'view': 'eog %s'})

**After**

.. code-block:: python

    >>> from mailcap_fix import mailcap
    >>> d = mailcap.getcaps()
    >>> # Correctly returns the wildcard entry
    >>> mailcap.findmatch(d, 'image/jpeg', filename='test.jpg')
    ('feh test.jpg', {'view': 'feh %s', 'lineno': 0})

How it works
------------

The goal of this patch is to conform to RFCC 1524,
while preserving as much backwards compatibility as possible and without adding any "magic".

*mailcap_fix* adds a new field ``lineno`` to each entry in the mailcap dict.
This line number is then used to sort entries in descending order when searching for a match.
For backwards compatability, if ``lineno`` is not present entries will simply not be sorted.
Because RFC 1524 defines a whitelist of valid mailcap fieldnames, the addition of ``lineno``
should not conflict with any other mailcap fields.

Benchmark
---------

| *Python 3.4.0*
| *Ubuntu 14.04 LTS 64bit*
| *Intel® Core™ i5-3210M CPU @ 2.50GHz × 4*
| *8 GiB RAM*
|

==================== ============ ============
        mailcap.get_caps() - per file
----------------------------------------------
..                   mailcap      mailcap_fix
==================== ============ ============
mailcap_short.txt_   0.081881 ms  0.084525 ms
mailcap_long.txt_    17.746289 ms 18.407623 ms
==================== ============ ============

==================== =========== ===========
    mailcap.lookup() - avg function call
--------------------------------------------
..                   mailcap     mailcap_fix
==================== =========== ===========
mailcap_short.txt_   0.000996 ms 0.003144 ms
mailcap_long.txt_    0.000798 ms 0.002731 ms
==================== =========== ===========

.. _mailcap_short.txt: https://github.com/michael-lazar/mailcap_fix/blob/master/tests/data/mailcap_short.txt

.. _mailcap_long.txt: https://github.com/michael-lazar/mailcap_fix/blob/master/tests/data/mailcap_long.txt

.. |python| image:: https://img.shields.io/badge/python-2.6+%2C%203.0+%2C%20pypy-blue.svg
    :target: https://pypi.python.org/pypi/mailcap_fix/
    :alt: Supported Python versions

.. |pypi| image:: https://img.shields.io/pypi/v/mailcap_fix.svg?label=version
    :target: https://pypi.python.org/pypi/mailcap_fix/
    :alt: Latest Version

.. |travis-ci| image:: https://travis-ci.org/michael-lazar/mailcap_fix.svg?branch=master
    :target: https://travis-ci.org/michael-lazar/mailcap_fix
    :alt: Build
