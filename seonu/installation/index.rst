Installation
============

Ærende requires python >= 3.6.

Via Pip
-------

You can install ærende via pip, from `pypi`_ : ::

    python3.6 -m pip install --user aerende


Via The Repo
-------------

To install ærende from the repo, you can clone it and set up a clean environment
with ``virtualenv``: ::

    git clone git@github.com:Autophagy/aerende.git
    cd aerende
    virtualenv .venv -p python3.6
    source .venv/bin/activate

Then, install the ``aerende`` package: ::

    pip install -e .

You can now run ``aerende``.

.. _`pypi`: https://pypi.python.org/pypi?:action=display&name=aerende
