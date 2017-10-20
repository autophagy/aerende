![aerende](doc/_static/title.png)

[![Documentation Status](https://readthedocs.org/projects/aerende/badge/?version=latest)](http://aerende.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/Autophagy/aerende.svg?branch=master)](https://travis-ci.org/Autophagy/aerende)
[![Pypi Version](https://img.shields.io/pypi/v/aerende.svg)](https://pypi.python.org/pypi?:action=display&name=aerende)
[![Python](https://img.shields.io/pypi/pyversions/aerende.svg)](https://pypi.python.org/pypi?:action=display&name=aerende)

Ærende is a tool to facilitate the recording of reminders, similar to post-it
notes. Written in python, with a curses UI via the [urwid](http://urwid.org/)
library. Documentation is available on
[ReadTheDocs](https://aerende.readthedocs.io/en/latest/).

![aerende](doc/_static/screenshot.png)

## Installation

### Via Pip

To install ærende via pip, from ![pypi](https://pypi.python.org/pypi?:action=display&name=aerende):
```
python3.6 -m pip install --user aerende
```

### Via The Repo

To install via the repo, you can set up a clean environment with ``virtualenv``:
```
virtualenv .venv -p python3.6
source .venv/bin/activate
```

Then, install the ``aerende`` package:
```
pip install -e .
```

You can now run ``aerende``.

## Tests

You can run the tests via ``python -m unittest``