#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
# 
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
# 
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# 
# The Original Code is mozilla.org code.
# 
# The Initial Developer of the Original Code is
# Mozilla.org.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
# 
# Contributor(s):
#     Jeff Hammel <jhammel@mozilla.com>     (Original author)
# 
# Alternatively, the contents of this file may be used under the terms of
# either of the GNU General Public License Version 2 or later (the "GPL"),
# or the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
# 
# ***** END LICENSE BLOCK *****

"""
Mozilla universal manifest parser
"""

__all__ = ['ManifestParser', 'TestManifest']

import os
import sys
from optparse import OptionParser

def read_ini(fp, variables=None, default='DEFAULT',
             comments=';#', separators=('=', ':'),
             strict=True):
  """
  read an .ini file and return a list of [(section, values)]
  - fp : file pointer or name to read
  - variables : default set of variables
  - default : name of the section for the default section
  - comments : characters that if they start a line denote a comment
  - separators : strings that denote key, value separation in order
  - strict : whether to be strict about parsing
  """

  if variables is None:
    variables = {}

  if isinstance(fp, basestring):
    fp = file(fp)

  sections = []
  key = value = None
  section_names = set([])

  # read the lines
  for line in fp.readlines():

    stripped = line.strip()

    # ignore blank lines
    if not stripped:
      # reset key and value to avoid continuation lines
      key = value = None
      continue

    # ignore comment lines
    if stripped[0] in comments:
      continue

    # check for a new section
    if len(stripped) > 2 and stripped[0] == '[' and stripped[-1] == ']':
      section = stripped[1:-1].strip()
      key = value = None

      # deal with DEFAULT section
      if section.lower() == default.lower():
        if strict:
          assert default not in section_names
        section_names.add(default)
        current_section = variables
        continue

      if strict:
        # make sure this section doesn't already exist
        assert section not in section_names

      section_names.add(section)

      current_section = {}
      sections.append((section, current_section))
      continue

    # if there aren't any sections yet, something bad happen
    if not section_names:
      raise Exception('No sections yet :(')

    # (key, value) pair
    for separator in separators:
      if separator in stripped:
        key, value = stripped.split(separator, 1)
        key = key.strip()
        value = value.strip()

        if strict:
          # make sure this key isn't already in the section or empty
          assert key
          if current_section is not variables:
            assert key not in current_section

        current_section[key] = value
        break
    else:
      # continuation line ?
      if line[0].isspace() and key:
        value = '%s%s%s' % (value, os.linesep, stripped)
        current_section[key] = value
      else:
        # something bad happen!
        raise Exception("Not sure what you're trying to do")

  # interpret the variables
  def interpret_variables(global_dict, local_dict):
    variables = global_dict.copy()
    variables.update(local_dict)
    return variables

  sections = [(i, interpret_variables(variables, j)) for i, j in sections]
  return sections

###

class ManifestParser(object):
    """read .ini manifests"""

    def __init__(self, manifests=(), defaults=None, strict=True):
        self._defaults = defaults or {}
        self.tests = []
        self.strict = strict
        if manifests:
            self.read(*manifests)

    def read(self, *filenames, **defaults):

        # ensure all files exist
        missing = [ filename for filename in filenames
                    if not os.path.exists(filename) ]
        if missing:
            raise IOError('Missing files: %s' % ', '.join(missing))

        # process each file
        for filename in filenames:

            # set the per file defaults
            defaults = defaults.copy() or self._defaults.copy()
            here = os.path.dirname(os.path.abspath(filename))
            defaults['here'] = here

            # read the configuration
            sections = read_ini(filename, variables=defaults)

            # get the tests
            for section, data in sections:

                # a file to include
                if section.startswith('include:'):
                    include_file = section.split('include:', 1)[-1]
                    include_file = os.path.join(here, include_file)
                    if not os.path.exists(include_file):
                      if strict:
                        raise IOError("File '%s' does not exist" % include_file)
                      else:
                        continue
                    include_defaults = data.copy()
                    self.read(include_file, **include_defaults)
                    continue

                # otherwise a test
                test = data
                test['name'] = section
                test['path'] = os.path.join(here, section)
                test['manifest'] = filename
                self.tests.append(test)

    def query(self, *checks):
        retval = []
        for test in self.tests:
            for check in checks:
                if not check(test):
                    break
            else:
                retval.append(test)
        return retval

    def get(self, _key=None, inverse=False, tags=None, **kwargs):

        # fix up tags
        if tags:
            tags = set(tags)
        else:
            tags = set()

        # make some check functions
        if inverse:
            has_tags = lambda test: tags.isdisjoint(test.keys())
            def dict_query(test):
                for key, value in kwargs.items():
                    if test.get(key) == value:
                        return False
                return True
        else:
            has_tags = lambda test: tags.issubset(test.keys())
            def dict_query(test):
                for key, value in kwargs.items():
                    if test.get(key) != value:
                        return False
                return True

        # query the tests
        tests = self.query(has_tags, dict_query)

        # if a key is given, return only a list of that key
        # useful for keys like 'name' or 'path'
        if _key:
            return [test[_key] for test in tests]

        # return the tests
        return tests

    def missing(self, tests=None):
        """return list of tests that do not exist on the filesystem"""
        if tests is None:
            tests = self.tests
        return [test for test in tests
                if not os.path.exists(test['path'])]

    def write(self, fp=sys.stdout,
              global_tags=None, global_kwargs=None,
              local_tags=None, local_kwargs=None):
        """
        TODO: write a manifest given a query
        global and local options will be munged to do the query
        globals will be written to the top of the file
        locals (if given) will be written per test
        """

class TestManifest(ManifestParser):
    """
    apply logic to manifests;  this is your integration layer :)
    specific harnesses may subclass from this if they need more logic
    """

    def active_tests(self):

        # ignore disabled tests
        tests = self.get(inverse=True, tags=['disabled'])

        # TODO: could filter out by current platform, existence, etc

        return tests

    def test_paths(self):
        return [test['path'] for test in self.active_tests()]

class ParserError(Exception):
  """error for exceptions while parsing the command line"""

def parse_args(_args):

  # return values
  _dict = {}
  tags = []
  args = []

  # parse the arguments
  key = None
  for arg in _args:
    if arg.startswith('---'):
      raise ParserError("arguments should start with '-' or '--' only")
    elif arg.startswith('--'):
      if key:
        raise ParserError("Key %s still open" % key)
      key = arg[2:]
      if '=' in key:
        key, value = key.split('=', 1)
        _dict[key] = value
        key = None
        continue
    elif arg.startswith('-'):
      if key:
        raise ParserError("Key %s still open" % key)
      tags.append(arg[1:])
      continue
    else:
      if key:
        _dict[key] = arg
        continue
      args.append(arg)

  # return values
  return (_dict, tags, args)

def main(args=sys.argv[1:]):

    # set up an option parser ...this is mostly for show
    usage = '%prog [options] manifest <manifest> <...>'
    parser = OptionParser(usage=usage)

    # actually parse the arguments in an unrelated way
    try:
        kwargs, tags, args = parse_args(args)
    except ParserError, e:
        parser.error(e.message)

    # make sure we have some manifests, otherwise it will
    # be quite boring
    if not args:
        parser.print_usage()
        parser.exit()

    # read the manifests
    manifests = ManifestParser()
    manifests.read(*args)

    # perform a query
    tests = manifests.get(*tags, **kwargs)

    # print the results
    # TODO: print these in a manner such that they are written out to
    # a new manifest!
    for test in tests:
        print test

if __name__ == '__main__':
    main()
