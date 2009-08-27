==============
z3c.recipe.tag
==============

.. contents::

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
install ctags and idutils in this way::

  $ sudo port install ctags idutils

How to use this recipe
----------------------

With Buildout
.............

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

With Paver
..........

If you are using `Paver
<http://www.blueskyonmars.com/projects/paver/>`_ and already have
z3c.recipe.tag installed, then all you have to do is add this line to
your ``pavement.py`` file::

  import z3c.recipe.tag

And then run the ``z3c.recipe.tag.tags`` task from the command line::

  $ paver z3c.recipe.tag.tags

Additional Resources
--------------------

For additional information on using tags tables with different editors
see the following websites:

- **Emacs**: http://www.gnu.org/software/emacs/manual/html_node/emacs/Tags.html

  - to jump to the location of a tag, type ``M-x find-tag`` and the
    name of the tag.  Or use ``M-.`` to jump to the tag matching the token
    the cursor is currently on.  The first time you do this, you will
    be prompted for the location of the TAGS file.

- **VIM**: http://vimdoc.sourceforge.net/htmldoc/tagsrch.html

- **BBEdit**: http://pine.barebones.com/manual/BBEdit_9_User_Manual.pdf
  Chapter 14, page 324

For more information on ctags, visit http://ctags.sourceforge.net/

(BBEdit_ is a Macintosh text editor.)

.. _BBEdit: http://barebones.com/products/bbedit/
