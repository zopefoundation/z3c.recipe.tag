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
import optparse
import os
import subprocess
import sys

import pkg_resources

import zc.buildout.easy_install
import zc.recipe.egg


class TagsMaker:

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        # We do this early so the "extends" functionality works before we get
        # to the other options below.
        self._delegated = zc.recipe.egg.Egg(buildout, name, options)
        options['script'] = os.path.join(buildout['buildout']['bin-directory'],
                                         options.get('script', self.name),
                                         )
        if not options.get('working-directory', ''):
            options['location'] = os.path.join(
                buildout['buildout']['parts-directory'], name)

    def install(self):
        options = self.options
        generated = []
        eggs, ws = self._delegated.working_set(('z3c.recipe.tag',))

        wd = options.get('working-directory', '')
        if not wd:
            wd = options['location']
            if os.path.exists(wd):
                assert os.path.isdir(wd)
            else:
                os.mkdir(wd)
            generated.append(wd)

        initialization = initialization_template % (
            self.buildout['buildout']['directory'])

        env_section = options.get('environment', '').strip()
        if env_section:
            env = self.buildout[env_section]
            for key, value in env.items():
                initialization += env_template % (key, value)

        initialization_section = options.get('initialization', '').strip()
        if initialization_section:
            initialization += initialization_section

        arguments = options.get('defaults', '')
        if arguments:
            arguments = arguments + ' + sys.argv[1:]'

        generated.extend(zc.buildout.easy_install.scripts(
            [(options['script'], 'z3c.recipe.tag', 'build_tags')],
            ws, options['executable'],
            self.buildout['buildout']['bin-directory'],
            extra_paths=self._delegated.extra_paths,
            initialization=initialization,
        ))

        return generated

    update = install


initialization_template = """import os
sys.argv[0] = os.path.abspath(sys.argv[0])
os.chdir(%r)
"""

env_template = """os.environ['%s'] = %r
"""


def getpath(candidates):
    paths = os.environ['PATH'].split(os.pathsep)
    for c in candidates:
        for p in paths:
            full = os.path.join(p, c)
            if os.path.exists(full):
                return full
    raise RuntimeError(
        'Can\'t find executable for any of: %s' % candidates)


class Builder:
    def get_relpaths(self, paths):
        working_dir = os.getcwd()
        return [os.path.relpath(path, working_dir) for path in paths]

    def __call__(self, targets=None, languages=None, tag_relative=False):
        if not targets:
            targets = ('idutils', 'ctags_vi', 'ctags_emacs')  # legacy behavior
        self.languages = languages or ''
        self.tag_relative = tag_relative
        paths = [path for path in sys.path
                 if os.path.isdir(path)]
        if self.tag_relative:
            # ctags will ignore --tag-relative=yes for absolute paths so we
            # must pass relative paths to it.
            paths = self.get_relpaths(paths)
        self.paths = paths
        results = {}
        for target in targets:
            tool_candidates, arguments, source, destination = getattr(
                self, '_build_{}'.format(target))()
            arguments[0:0] = [getpath(tool_candidates)]
            res = subprocess.call(arguments)
            if res == 0:
                res = subprocess.call(['mv', source, destination])
            results[target] = res
        return results

    def _build_idutils(self):
        return [
            [
                'mkid'
            ], [
                '-m',
                pkg_resources.resource_filename(
                    "z3c.recipe.tag", "id-lang.map.txt"),
                '-o',
                'ID.new'
            ] + self.paths,
            'ID.new',
            'ID']

    def _build_ctags_vi(self):
        res = [['ctags-exuberant', 'ctags'],
               ['-R',
                '--python-kinds=-i',
                '-f',
                'tags.new'] + self.paths,
               'tags.new',
               'tags']
        if self.languages:
            res[1][0:0] = ['--languages=%s' % self.languages]
        if self.tag_relative:
            res[1][0:0] = ['--tag-relative=yes']
        return res

    def _build_ctags_emacs(self):
        res = self._build_ctags_vi()
        res[1][0:0] = ['-e']
        res[3] = 'TAGS'
        return res

    def _build_ctags_bbedit(self):
        res = self._build_ctags_vi()
        try:
            res[1].remove('--tag-relative=yes')
        except ValueError:
            pass
        res[1][0:0] = [
            '--excmd=number', '--tag-relative=no', '--fields=+a+m+n+S']
        return res


def append_const(option, opt_str, value, parser, const):
    # 'append_const' action added in Py 2.5, and we're in 2.4 :-(
    if getattr(parser.values, 'targets', None) is None:
        parser.values.targets = []
    parser.values.targets.append(const)


def build_tags(args=None):
    parser = optparse.OptionParser()
    parser.add_option('-l', '--languages', dest='languages',
                      default='-JavaScript',
                      help='ctags comma-separated list of languages. '
                      'defaults to ``-JavaScript``')
    parser.add_option('-e', '--ctags-emacs', action='callback',
                      callback=append_const, callback_args=('ctags_emacs',),
                      help='flag to build emacs ctags ``TAGS`` file')
    parser.add_option('-v', '--ctags-vi', action='callback',
                      callback=append_const, callback_args=('ctags_vi',),
                      help='flag to build vi ctags ``tags`` file')
    parser.add_option('-b', '--ctags-bbedit', action='callback',
                      callback=append_const, callback_args=('ctags_bbedit',),
                      help='flag to build bbedit ctags ``tags`` file')
    parser.add_option('-i', '--idutils', action='callback',
                      callback=append_const, callback_args=('idutils',),
                      help='flag to build idutils ``ID`` file')
    parser.add_option('-r', '--tag-relative', action='store_true',
                      dest='tag_relative', default=False,
                      help=('generate tags with paths relative to'
                            ' tags file instead of absolute paths'
                            ' (works with vim tags only)'))
    options, args = parser.parse_args(args)
    if args:
        parser.error('no arguments accepted')
    targets = getattr(options, 'targets', None)
    if (targets and 'ctags_bbedit' in targets and 'ctags_vi' in targets):
        parser.error('cannot build both vi and bbedit ctags files (same name)')
    builder = Builder()
    builder(targets, languages=options.languages,
            tag_relative=options.tag_relative)


try:
    import paver.easy
except ImportError:
    HAS_PAVER = False
else:  # pragma: nocover
    HAS_PAVER = True

if HAS_PAVER:  # pragma: nocover
    @paver.easy.task
    @paver.easy.consume_args
    def tags(args):
        """Build tags database file for emacs, vim, or bbedit"""
        build_tags(args)
