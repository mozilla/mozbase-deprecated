#!/usr/bin/env python

"""
run mozprofile tests
"""

import imp
import manifestparser
import os
import sys
import unittest

here = os.path.dirname(os.path.abspath(__file__))

def unittests(path):
    """return the unittests in a .py file"""

    unittests = []
    assert os.path.exists(path)
    modname = os.path.splitext(os.path.basename(path))[0]
    module = imp.load_source(modname, path)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(module)
    for test in suite:
        unittests.append(test)
    return unittests

def main(args=sys.argv[1:]):

    # read the manifest
    manifest = os.path.join(here, 'manifest.ini')
    assert os.path.exists(manifest), '%s not found' % manifest
    manifest = manifestparser.TestManifest(manifests=(manifest,))
    tests = manifest.active_tests()

    # gather the tests
    unittestlist = []
    for test in tests:
        unittestlist.extend(unittests(test['path']))

    # run the tests
    suite = unittest.TestSuite(unittestlist)
    runner = unittest.TextTestRunner()
    results = runner.run(suite)

    # exit according to results
    sys.exit((results.failures or results.errors) and 1 or 0)

if __name__ == '__main__':
    main()
