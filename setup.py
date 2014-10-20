#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
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

# Check Python version
import sys
if sys.version_info < (2, 6):
    sys.exit("%s: need Python 2.6 or later.\nYour python is %s."
             % (sys.argv[0], sys.version))

import os
from setuptools import setup, find_packages


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

setup(
    name="z3c.recipe.tag",
    version='0.8',
    author="Ignas Mikalajūnas and the Zope Community",
    description="Generate ctags from eggs for development.",
    long_description=read('README.rst') + '\n\n' + read('CHANGES.rst'),
    license="ZPL 2.1",
    maintainer="Paul Carduner",
    maintainer_email="zope-dev@zope.org",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Framework :: Buildout",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Text Editors :: Emacs",
        "Topic :: Utilities"],
    url='https://github.com/zopefoundation/z3c.recipe.tag',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c', 'z3c.recipe'],
    extras_require=dict(
        test=[
            'zope.testing',
        ],
    ),
    install_requires=[
        'setuptools',
        'zc.buildout >= 2.0',
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
