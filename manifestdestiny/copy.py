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
    manifest = manifests.ManifestParser(manifests=(from_manifest))

    # tests to copy
    copy_tests = []
    for test in manifest.tests:
        pass

    # destination
    if os.path.isdir(to_manifest):
        to_dir = os.path.abspath(to_manifest)
        to_manifest = os.path.join(os.path.dirname(os.path.abspath(to_manifest)),
                                   os.path.basename(from_manifest))
    else:

        # if the manifest exists, overwrite the manifest (be careful!)


def main(args=sys.argv[1:]):
    usage = '%prog [options] from_manifest.ini to_manifest.ini'
    parser = OptionParser(usage=usage, description=__doc__)
    options, args = parser.parse_args(args)

if __name__ == '__main__':
    main()
