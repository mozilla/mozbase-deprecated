#!/usr/bin/env python

import doctest
import os

def run_tests():
    directory = os.path.dirname(os.path.abspath(__file__))
    tests =  [ test for test in os.listdir(directory) if test.endswith('.txt') ]
    os.chdir(directory)
    for test in tests:
        doctest.testfile(test)

if __name__ == '__main__':
    run_tests()
