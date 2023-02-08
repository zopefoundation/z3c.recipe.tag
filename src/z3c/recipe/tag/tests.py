import doctest
import os
import re
import unittest

import zc.buildout.testing
from zope.testing import renormalizing


def doctest_tags_recipe():
    """Test for z3c.recipe.tag

        >>> write('buildout.cfg',
        ... '''
        ... [buildout]
        ... parts = tags
        ...
        ... [tags]
        ... recipe = z3c.recipe.tag
        ... eggs =
        ...     z3c.recipe.tag
        ... ''')

        >>> print(system(join('bin', 'buildout')).rstrip())
        Installing tags.
        Generated script '/sample-buildout/bin/tags'.

        >>> cat('bin', 'tags')
        #!/usr/bin/python
        <BLANKLINE>
        import sys
        sys.path[0:0] = [
          '/z3c.recipe.tag/src',
          ]
        <BLANKLINE>
        import os
        sys.argv[0] = os.path.abspath(sys.argv[0])
        os.chdir('.../_TEST_/sample-buildout')
        <BLANKLINE>
        <BLANKLINE>
        import z3c.recipe.tag
        <BLANKLINE>
        if __name__ == '__main__':
            sys.exit(z3c.recipe.tag.build_tags())

    """


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install('zc.recipe.egg', test)
    zc.buildout.testing.install_develop('z3c.recipe.tag', test)


def tearDown(test):
    zc.buildout.testing.buildoutTearDown(test)


checker = renormalizing.RENormalizing([
    zc.buildout.testing.normalize_path,
    # zope.whatever-1.2.3-py3.7.egg -> zope.whatever-pyN.N.egg
    (re.compile(r'-[^ /]+-py\d[.]\d(-\S+)?.egg'), '-pyN.N.egg'),
    # #!/path/to/whatever/python3.2mu -> #!/usr/bin/python
    (re.compile('#![^\n]+/python[0-9.mu]*'), '#!/usr/bin/python'),
    # location of this source tree
    (re.compile("""['"][^\n"']+z3c.recipe.tag[^\n"']*['"],"""),
     "'/z3c.recipe.tag/src',"),
    # I've no idea what causes these
    #   Couldn't find index page for 'zc.recipe.egg' (maybe misspelled?)
    # error messages, let's just suppress them
    (re.compile("Couldn't find index page for '[a-zA-Z0-9.]+' "
     r"\(maybe misspelled\?\)\n"), ''),
    # I've no idea what causes these
    #   Not found: /tmp/tmpJKH0LKbuildouttests/zc.buildout/
    # error messages, let's just suppress them
    (re.compile("Not found: .*buildouttests/[a-zA-Z0-9.]+/\n"), ''),
])

if os.getenv('RUNNING_UNDER_TOX'):  # pragma: no cover
    # tox installs our test dependencies into the virtualenv,
    # and zc.buildout has no site isolation, so it finds them there,
    # so it doesn't add them to sys.path in the generated scripts
    checker += renormalizing.RENormalizing([
        (re.compile(r"\s*'/sample-buildout/eggs/zc.recipe.egg-pyN.N.egg',\n"),
         ''),
        (re.compile(r"\s*'/sample-buildout/eggs/zc.buildout-pyN.N.egg',\n"),
         ''),
        (re.compile(r"\s*'/sample-buildout/eggs/distribute-pyN.N.egg',\n"),
         ''),
        (re.compile(r"\s*'/sample-buildout/eggs/setuptools-pyN.N.egg',\n"),
         ''),
        (re.compile(r"'.*/site-packages'"), "'/z3c.recipe.tag/src'"),
        (re.compile(r"#!/.*/bin/pypy.*"), "#!/usr/bin/python"),
    ])


def test_suite():
    return unittest.TestSuite([
        doctest.DocTestSuite(
            setUp=setUp, tearDown=tearDown, checker=checker,
            optionflags=(
                doctest.NORMALIZE_WHITESPACE
                | doctest.ELLIPSIS
                | doctest.REPORT_NDIFF)),
    ])
