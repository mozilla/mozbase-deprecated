"""
copy tests and manifests
"""

import manifests
import os
import sys
from optparse import OptionParser

def copy(from_manifest, to_manifest, *tags, **kwargs):

    # parse the manifests
    assert os.path.exists(from_manifest), "'%s' does not exist"
    from_dir = os.path.dirname(os.path.abspath(from_manifest))
    manifest = manifests.ManifestParser(manifests=(from_manifest,))

    # tests to copy
    copy_tests = []
    for test in manifest.tests:
        pass

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

    # copy the damn things
    


def main(args=sys.argv[1:]):
    usage = '%prog [options] from_manifest.ini to_manifest.ini'
    parser = OptionParser(usage=usage, description=__doc__)
    options, args = parser.parse_args(args)

if __name__ == '__main__':
    main()
