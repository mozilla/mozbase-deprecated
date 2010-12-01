#!/usr/bin/env python
"""
convert a directory to a simple manifest
"""


import os
import sys
from fnmatch import fnmatch
from optparse import OptionParser

def convert(directories, pattern=None, ignore=()):
  retval = []
  for directory in directories:
    for dirpath, dirnames, filenames in os.walk(directory):

      dirnames = []

      # reference only the subdirectory
      dirpath = dirpath.split(directory, 1)[-1].strip('/')

      if dirpath.split(os.path.sep)[0] in ignore:
        continue

      # filter by glob
      if pattern:
        filenames = [filename for filename in filenames
                     if fnmatch(filename, pattern)]

      # add to the list
      retval.extend([os.path.join(dirpath, filename)
                     for filename in filenames])
  retval.sort()
  retval = ['[%s]' % filename for filename in retval]
  return '\n'.join(retval)

def main(args=sys.argv[1:]):
  usage = '%prog [options] directory <directory> <...>'
  parser = OptionParser(usage=usage)
  parser.add_option('-p', '--pattern', dest='pattern',
                    help="glob pattern for files")
  parser.add_option('-i', '--ignore', dest='ignore', action='append',
                    help='directories to ignore')
  options, args = parser.parse_args(args)
  if not len(args):
    parser.print_usage()
    parser.exit()
  for arg in args:
    assert os.path.exists(arg)
    assert os.path.isdir(arg)
  print convert(args, pattern=options.pattern, ignore=options.ignore)

if __name__ == '__main__':
  main()
