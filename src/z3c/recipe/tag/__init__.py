##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
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
import os, sys
import pkg_resources

import zc.buildout.easy_install
import zc.recipe.egg

class TagsMaker(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        options['script'] = os.path.join(buildout['buildout']['bin-directory'],
                                         options.get('script', self.name),
                                         )

        if not options.get('working-directory', ''):
            options['location'] = os.path.join(
                buildout['buildout']['parts-directory'], name)
        self.egg = zc.recipe.egg.Egg(buildout, name, options)

    def install(self):
        options = self.options
        dest = []
        eggs, ws = self.egg.working_set(('z3c.recipe.tag',))

        wd = options.get('working-directory', '')
        if not wd:
            wd = options['location']
            if os.path.exists(wd):
                assert os.path.isdir(wd)
            else:
                os.mkdir(wd)
            dest.append(wd)

        initialization = initialization_template % self.buildout['buildout']['directory']

        env_section = options.get('environment', '').strip()
        if env_section:
            env = self.buildout[env_section]
            for key, value in env.items():
                initialization += env_template % (key, value)

        initialization_section = options.get('initialization', '').strip()
        if initialization_section:
            initialization += initialization_section

        dest.extend(zc.buildout.easy_install.scripts(
            [(options['script'], 'z3c.recipe.tag', 'build_tags')],
            ws, options['executable'],
            self.buildout['buildout']['bin-directory'],
            extra_paths=self.egg.extra_paths,
            initialization = initialization,
            ))

        return dest

    update = install


initialization_template = """import os
sys.argv[0] = os.path.abspath(sys.argv[0])
os.chdir(%r)
"""

env_template = """os.environ['%s'] = %r
"""


def build_tags():
    paths = [path for path in sys.path
             if not path.endswith('.zip')]
    paths = " ".join(paths)

    map = pkg_resources.resource_filename("z3c.recipe.tag", "id-lang.map")
    command = "mkid -m %s -o ID.new %s" % (map, paths)
    if os.system(command) == 0:
        os.system("mv ID.new ID")

    command = "ctags-exuberant -R --languages=-JavaScript -f tags.new %s" % paths
    if os.system(command) == 0:
        os.system("mv tags.new tags")

    command = "ctags-exuberant -e -R --languages=-JavaScript -f TAGS.new %s" % paths
    if os.system(command) == 0:
        os.system("mv TAGS.new TAGS")
