"""
copy tests and manifests
"""

import manifests
import os
import shutil
import sys
from optparse import OptionParser

def copy(from_manifest, to_manifest, *tags, **kwargs):
    """
    copy the manifests and associated tests
    - from_manifest : manifest to copy from
    - to_manifest : manifest or directory to copy to
    - tags : keywords the tests must have
    - kwargs : key, values the tests must match
    """


    # parse the manifests
    assert os.path.exists(from_manifest), "'%s' does not exist"
    from_dir = os.path.dirname(os.path.abspath(from_manifest))
    manifest = manifests.ManifestParser(manifests=(from_manifest,))

    # destination
    if os.path.isdir(to_manifest):
        to_dir = os.path.abspath(to_manifest)
        to_manifest = os.path.join(to_dir, os.path.basename(from_manifest))
    else:
        if os.path.exists(to_manifest):
            # if the manifest exists, overwrite the manifest (be careful!)
            to_dir = os.path.dirname(os.path.abspath(to_manifest))
            to_manifest = os.path.abspath(to_manifest)
        else:
            # assert that what is given is a file name
            # (not a directory)
            to_manifest = os.path.abspath(to_manifest)
            to_dir = os.path.dirname(to_manifest)
            if not os.path.exists(to_dir):
                os.path.makedirs(to_dir)
            else:
                # sanity check
                assert os.path.isdir(to_dir)

    # tests to copy
    tests = manifest.get(tags=tags, **kwargs)

    # copy the damn things
    if not tests:
        return # nothing to do!
    _manifests = [test['manifest'] for test in tests
                  if test['manifest'] != os.path.abspath(from_manifest)]
    _manifests = [os.path.relpath(_manifest, from_dir) for _manifest in _manifests]
    _manifests = set(_manifests)
    shutil.copy(from_manifest, to_manifest)
    for _manifest in _manifests:
        destination = os.path.join(to_dir, _manifest)
        dirname = os.path.dirname(destination)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        else:
            # sanity check
            assert os.path.isdir(dirname)
        shutil.copy(os.path.join(from_dir, _manifest), destination)
    for test in tests:
        if not os.path.isabs(test['name']):
            source = test['path']
            if not os.path.exists(source):
                print >> sys.stderr, "Missing test: '%s' does not exist!" % source
                continue
            destination = os.path.join(to_dir, os.path.relpath(test['path'], from_dir))
            shutil.copy(source, destination)
            # TODO: ensure that all of the tests are below the from_dir

### command line entry points
            
def copy_main(args=sys.argv[1:]):

    # set up an option parser
    usage = '%prog [options] from_manifest.ini to_manifest.ini'
    parser = OptionParser(usage=usage, description=__doc__)
    options, args = parser.parse_args(args)

    # ensure correct number of arguments passed
    if len(args) != 2:
        parser.print_usage()
        parser.exit()

    # do the thing
    copy(args[0], args[1])

if __name__ == '__main__':
    copy_main() # only get one choice
