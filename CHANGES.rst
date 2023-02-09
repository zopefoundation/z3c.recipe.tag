=======
CHANGES
=======

1.0 (2023-02-09)
----------------

- Drop support for Python < 3.7.

- Add support for Python 3.7 up to 3.11.

- Require ``zc.buildout >= 3``.


0.8 (2014-10-20)
----------------

- Add --tag-relative option to support relative tag generation.


0.7 (2013-03-22)
----------------

- Support and require zc.buildout 2.0.

- Add supported Python version (3.6, 2.7, 3.2, 3.3) classifiers to
  setup.py


0.6 (2012-09-07)
----------------

- Update manifest to allow package generation fron non-VCS export. Counters the
  0.5 "brown bag" release.


0.5 (2012-09-06)
----------------

- Exclude Python import statements by default from showing up as tags.

- Add 'defaults' option to allow adding default command line options (e.g. to
  set '-v' by default)


0.4.1 (2012-01-11)
------------------

* Skip nonexistent sys.path directories to avoid ctags warnings.


0.4.0 (2010-08-29)
------------------

* Support new script features from zc.buildout 1.5 and higher.  This version
  requires zc.buildout 1.5 or higher.

* Also index Mako and HTML files with id-utils.


0.3.0 (2009-08-16)
------------------

* Add support for using this recipe as a `paver <http://www.blueskyonmars.com/projects/paver/>`_ task.

* Also index Javascript, CSS and ReStructuredText files with id-utils.

* Define a default entry point for zc.buildout, so you can simply say::

    [ctags]
    recipe = z3c.recipe.tag


0.2.0 (2008-08-28)
------------------

* Allow command-line choices for what files to build, and what languages ctags
  should parse.  (Note that the default behavior of running ``./bin/tags``
  is the same as previous releases.)

* Support the Mac OS X packaging system "macports" (exuberant ctags is
  ``ctags-exuberant`` in Ubuntu and ``ctags`` in macports).

* Support creating BBEdit-style ctags files.

* Small changes for development (use bootstrap external, set svn:ignore)

0.1.0 (2008-03-16)
------------------

- Initial release.

  * buildout recipe for generating ctags of eggs used.
