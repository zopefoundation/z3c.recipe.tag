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
import os
import optparse
import pkg_resources
import subprocess
import sys

import zc.buildout.easy_install
import z3c.recipe.scripts.scripts

class TagsMaker(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        # We do this early so the "extends" functionality works before we get
        # to the other options below.
        self._delegated = z3c.recipe.scripts.scripts.Base(
            buildout, name, options)
        options['script'] = os.path.join(buildout['buildout']['bin-directory'],
                                         options.get('script', self.name),
                                         )

    def install(self):
        options = self.options
        generated = []
        eggs, ws = self._delegated.working_set(('z3c.recipe.tag',))

        if not os.path.exists(options['parts-directory']):
            os.mkdir(options['parts-directory'])
            generated.append(options['parts-directory'])

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

        generated.extend(zc.buildout.easy_install.sitepackage_safe_scripts(
            self.buildout['buildout']['bin-directory'], ws,
            options['executable'], options['parts-directory'],
            reqs=[(options['script'], 'z3c.recipe.tag', 'build_tags')],
            extra_paths=self._delegated.extra_paths,
            include_site_packages=self._delegated.include_site_packages,
            exec_sitecustomize=self._delegated.exec_sitecustomize,
            relative_paths=self._delegated._relative_paths,
            script_initialization=initialization,
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
    def __init__(self):
        self.paths = [path for path in sys.path
                      if os.path.isdir(path)]

    def __call__(self, targets=None, languages=None):
        if not targets:
            targets = ('idutils', 'ctags_vi', 'ctags_emacs') # legacy behavior
        self.languages = languages or ''
        results = {}
        for target in targets:
            tool_candidates, arguments, source, destination = getattr(
                self, '_build_%s' % (target,))()
            arguments[0:0] = [getpath(tool_candidates)]
            res = subprocess.call(arguments)
            if res == 0:
                res = subprocess.call(['mv', source, destination])
            results[target] = res
        return results

    def _build_idutils(self):
        return [['mkid'],
                ['-m',
                 pkg_resources.resource_filename(
                    "z3c.recipe.tag", "id-lang.map"),
                 '-o',
                 'ID.new'] + self.paths,
                'ID.new',
                'ID']

    def _build_ctags_vi(self):
        res = [['ctags-exuberant', 'ctags'],
               ['-R',
                '-f',
                'tags.new'] + self.paths,
                'tags.new',
                'tags']
        if self.languages:
            res[1][0:0] = ['--languages=%s' % self.languages]
        return res

    def _build_ctags_emacs(self):
        res = self._build_ctags_vi()
        res[1][0:0] = ['-e']
        res[3] = 'TAGS'
        return res

    def _build_ctags_bbedit(self):
        res = self._build_ctags_vi()
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
    parser.add_option('-v', '--ctags-vi',  action='callback',
                      callback=append_const, callback_args=('ctags_vi',),
                      help='flag to build vi ctags ``tags`` file')
    parser.add_option('-b', '--ctags-bbedit', action='callback',
                      callback=append_const, callback_args=('ctags_bbedit',),
                      help='flag to build bbedit ctags ``tags`` file')
    parser.add_option('-i', '--idutils', action='callback',
                      callback=append_const, callback_args=('idutils',),
                      help='flag to build idutils ``ID`` file')
    options, args = parser.parse_args(args)
    if args:
        parser.error('no arguments accepted')
    targets = getattr(options, 'targets', None)
    if (targets and 'ctags_bbedit' in targets and 'ctags_vi' in targets):
        parser.error('cannot build both vi and bbedit ctags files (same name)')
    builder = Builder()
    builder(targets, options.languages)

try:
    import paver.easy
except ImportError:
    HAS_PAVER = False
else:
    HAS_PAVER = True

if HAS_PAVER:
    @paver.easy.task
    @paver.easy.consume_args
    def tags(args):
        """Build tags database file for emacs, vim, or bbedit"""
        build_tags(args)
