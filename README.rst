===========
Mailcap Fix
===========

| RTV provides an interface to view and interact with reddit from your terminal.
| It's compatible with *most* terminal emulators on Linux and OSX.

.. image:: http://i.imgur.com/Ek13lqM.png

`DEMO <https://asciinema.org/a/31609?speed=2&autoplay=1>`_

RTV is built in **python** using the **curses** library.

---------------

|pypi| |python| |travis-ci| |coveralls| |gitter|

---------------

* `Installation`_
* `Usage`_
* `Settings`_
* `FAQ`_
* `Changelog`_
* `License`_

============
Installation
============

https://tools.ietf.org/html/rfc1524

Location of Configuration Information

   Each user agent must clearly obtain the configuration information
   from a common location, if the same information is to be used to
   configure all user agents.  However, individual users should be able
   to override or augment a site's configuration.  The configuration
   information should therefore be obtained from a designated set of
   locations.  The overall configuration will be obtained through the
   virtual concatenation of several individual configuration files known
   as mailcap files.  The configuration information will be obtained
   from the FIRST matching entry in a mailcap file, where "matching"
   depends on both a matching content-type specification, an entry
   containing sufficient information for the purposes of the application
   doing the searching, and the success of any test in the "test="
   field, if present.