#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

try:
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
except IOError:
    readme = ''


setup(
    name='aerende',
    author='Mika Naylor (Autophagy)',
    author_email='mail@autophagy.io',
    url='https://github.com/Autophagy/aerende',
    description='A post-it note/reminders tool',
    long_description=readme,
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
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm']
)