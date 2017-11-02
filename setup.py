#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from aerende import version

setup(
    name='aerende',
    version=version,
    author='Mika Naylor (Autophagy)',
    author_email='mail@autophagy.io',
    url='https://github.com/Autophagy/aerende',
    description='A post-it note/reminders tool',
    long_description='''Ærende is a small, python based note taking application.
        Works offline and in the terminal via a curses interface.
        Navigation via vim-esque keys.
        Designed to slot easily into my comm workspace alongside weechat and neomutt.''',
    entry_points={
        'console_scripts': [
            'aerende = aerende.__main__:main',
        ]
    },
    packages=['aerende'],
    install_requires=[
        'PyYAML',
        'urwid'
    ],
    python_requires='>=3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
