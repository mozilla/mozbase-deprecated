#!/usr/bin/env python
"""
convert a directory to a simple manifest
"""

import os
import sys
from optparse import OptionParser

def convert(*directories):
  retval = []
  for directory in directories:
    for dirpath, dirnames, filenames in os.walk(directory):

      # reference only the subdirectory
      dirpath = dirpath.split(directory, 1)[-1]

      retval.extend([os.path.join(dirpath, filename)
                     for filename in filenames])
  retval.sort()
  retval = ['[%s]' % filename for filename in retval]
  return '\n'.join(retval)

def main(args=sys.argv[1:]):
  usage = '%prog [options] directory'
  parser = OptionParser(usage=usage)
  options, args = parser.parse_args(args)
  if not len(args):
    parser.print_usage()
    parser.exit()
  for arg in args:
    assert os.path.exists(arg)
    assert os.path.isdir(arg)
  print convert(*args)

if __name__ == '__main__':
  main()
