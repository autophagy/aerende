======
Ærende
======

.. image:: http://scieldas.autophagy.io/rtd/aerende.svg
    :target: http://aerende.readthedocs.io/en/latest
    :alt: Documentation Status

.. image:: http://scieldas.autophagy.io/travis/Autophagy/aerende.svg
    :target: https://travis-ci.org/Autophagy/aerende
    :alt: Build Status

.. image:: http://scieldas.autophagy.io/pypi/version/aerende.svg
   :target: https://pypi.python.org/pypi/aerende/
   :alt: Pypi Version

.. image:: http://scieldas.autophagy.io/pypi/pyversions/aerende.svg
   :target: https://pypi.python.org/pypi/aerende/
   :alt: Python Version

.. image:: http://scieldas.autophagy.io/licenses/MIT.svg
   :target: LICENSE
   :alt: MIT License


Ærende is a tool to facilitate the recording of reminders, similar to post-it
notes. Written in python, with a curses UI via the `urwid`_ library.
Documentation is available on `ReadTheDocs`_.

.. image:: doc/_static/screenshot.png
    :alt: aerende screenshot
    :align: center


Installation
============

Via Pip
-------

To install ærende via pip, from `pypi`_::

  python3.6 -m pip install --user aerende

Via The Repo
------------

To install via the repo, you can set up a clean environment with ``virtualenv``::

  virtualenv .venv -p python3.6
  source .venv/bin/activate

Then, install the ``aerende`` package::

  pip install -e .

You can now run ``aerende``.

Documentation
=============

To build the documentation, install the requirements via::

  pip install -r requirements.txt

In the `doc` folder, there is a Makefile to build the documentation. For example,
to build the HTML documentation::

  cd doc
  make html

The documentation is automatically built and deployed on `ReadTheDocs`_.

Tests
=====

You can run the tests via ``python -m unittest``


.. _urwid: http://urwid.org/
.. _ReadTheDocs: https://aerende.readthedocs.io/en/latest/
.. _pypi: https://pypi.python.org/pypi/aerende/
