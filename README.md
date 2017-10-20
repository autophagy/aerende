![aerende](doc/_static/title.png)

[![Documentation Status](https://readthedocs.org/projects/aerende/badge/?version=latest)](http://aerende.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.org/Autophagy/aerende.svg?branch=master)](https://travis-ci.org/Autophagy/aerende)

Ærende is a tool to facilitate the recording of reminders, similar to post-it
notes. Written in python, with a curses UI via the [urwid](http://urwid.org/)
library. Documentation is available on
[ReadTheDocs](https://aerende.readthedocs.io/en/latest/).

![aerende](doc/_static/screenshot.png)

## Installation

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