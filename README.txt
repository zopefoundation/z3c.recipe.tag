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

On a Mac, download and install ``port`` from http://www.macports.org/ and then
install ctags and utils in this way::

  $ sudo port install ctags idutils

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

By default, this script produces three files in the directory from
which you ran the script: 

- a ctags file called ``TAGS`` for use by emacs,
- a ctags file called ``tags`` for use by vi, and
- an idutils file called ``ID`` for use by either.

You can then use these file in your editor of choice.

Optionally, you can select which files to build.  The following is the output
of ``./bin/tags --help``::

    usage: build_tags [options]
    
    options:
      -h, --help            show this help message and exit
      -l LANGUAGES, --languages=LANGUAGES
                            ctags comma-separated list of languages. defaults to
                            ``-JavaScript``
      -e, --ctags-emacs     flag to build emacs ctags ``TAGS`` file
      -v, --ctags-vi        flag to build vi ctags ``tags`` file
      -b, --ctags-bbedit    flag to build bbedit ctags ``tags`` file
      -i, --idutils         flag to build idutils ``ID`` file

(BBEdit_ is a Macintosh text editor.)

.. _BBEdit: http://barebones.com/products/bbedit/
