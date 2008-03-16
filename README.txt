z3c.recipe.tag
==============

Introduction
------------

This recipe generates a TAGS database file that can be used with a
number of different editors to quickly lookup class and function
definitions in your package's source files and egg dependencies.

Dependencies
------------

Before running a tags enabled buildout, you must install the
appropriate command line tag generation tools: exuberant-ctags and
id-utils.  In Ubuntu, you can install these with apt-get::

  $ sudo apt-get install exuberant-ctags id-utils

How to use this recipe
----------------------

Suppose you have an egg called ``MyApplication``.  To use this recipe with
buildout, you would add the following to the ``buildout.cfg`` file::

  [tags]
  recipe = z3c.recipe.tag:tags
  eggs = MyApplication

This produces a script file in the ``bin/`` directory which you can
then run like this::

  $ ./bin/tags

This script produces a file called ``TAGS`` in the directory from
which you ran the script.  You can then use this file in your editor
of choice (e.g. emacs).