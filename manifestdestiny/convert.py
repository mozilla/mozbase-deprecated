#!/usr/bin/env python
"""
convert a directory to a simple manifest
"""


import os
import sys
from fnmatch import fnmatch
from optparse import OptionParser

def convert(directories, pattern=None, ignore=(), write=None):
  retval = []
  include = []
  for directory in directories:
    for dirpath, dirnames, filenames in os.walk(directory):

      # filter out directory names
      dirnames = [ i for i in dirnames if i not in ignore ]

      # reference only the subdirectory
      _dirpath = dirpath
      dirpath = dirpath.split(directory, 1)[-1].strip('/')

      if dirpath.split(os.path.sep)[0] in ignore:
        continue

      # filter by glob
      if pattern:
        filenames = [filename for filename in filenames
                     if fnmatch(filename, pattern)]

      filenames.sort()
      if write:
        manifest = file(os.path.join(_dirpath, write), 'w')
        for dirname in dirnames:
          print >> manifest, '[include:%s]' % os.path.join(dirname, write)
        for filename in filenames:
          print >> manifest, '[%s]' % filename
        manifest.close()
      
      # add to the list
      retval.extend([os.path.join(dirpath, filename)
                     for filename in filenames])

  if write:
    return
  retval.sort()
  retval = ['[%s]' % filename for filename in retval]
  return '\n'.join(retval)

def main(args=sys.argv[1:]):
  usage = '%prog [options] directory <directory> <...>'
  parser = OptionParser(usage=usage)
  parser.add_option('-p', '--pattern', dest='pattern',
                    help="glob pattern for files")
  parser.add_option('-i', '--ignore', dest='ignore',
                    default=[], action='append',
                    help='directories to ignore')
  parser.add_option('-w', '--in-place', dest='in_place',
                    help='Write .ini files in place; filename to write to')
  options, args = parser.parse_args(args)
  if not len(args):
    parser.print_usage()
    parser.exit()
  for arg in args:
    assert os.path.exists(arg)
    assert os.path.isdir(arg)
  manifest = convert(args, pattern=options.pattern, ignore=options.ignore,
                     write=options.in_place)
  if manifest:
    print manifest

if __name__ == '__main__':
  main()
