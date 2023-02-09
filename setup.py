#!/usr/bin/env python
##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for z3c.recipe.tag"""

import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(
    name="z3c.recipe.tag",
    version='1.0',
    author="Ignas Mikalajūnas and the Zope Community",
    description="Generate ctags from eggs for development.",
    long_description=read('README.rst') + '\n\n' + read('CHANGES.rst'),
    license="ZPL 2.1",
    maintainer="Paul Carduner",
    maintainer_email="zope-dev@zope.dev",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Buildout",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Text Editors :: Emacs",
        "Topic :: Utilities",
    ],
    url='https://github.com/zopefoundation/z3c.recipe.tag',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c', 'z3c.recipe'],
    python_requires='>=3.7',
    extras_require=dict(
        test=[
            'zope.testing',
            'zope.testrunner',
        ],
    ),
    install_requires=[
        'setuptools',
        'zc.buildout >= 3.0',
        'zc.recipe.egg',
        # these two come from apt-get:
        #   'id-utils',
        #   'ctags-exuberant'
        # alternately, on Mac, use macports (macports.org) and
        #   ``sudo port install ctags idutils``
    ],
    entry_points={
        'zc.buildout': [
            'default = z3c.recipe.tag:TagsMaker',
            'tags = z3c.recipe.tag:TagsMaker',
        ],
        'console_scripts': [
            'build_tags = z3c.recipe.tag:build_tags',
        ],
    },
    zip_safe=False,
    include_package_data=True,
)
