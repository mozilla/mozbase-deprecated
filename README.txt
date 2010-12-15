ManifestDestiny
===============

Tests are denoted by sections in an .ini file (see
http://k0s.org/mozilla/hg/ManifestDestiny/file/tip/manifestdestiny/tests/mozmill-example.ini). 

Additional manifest files may be included with a [include:] directive:

[include:path-to-additional-file.manifest]

The path to included files is relative to the current manifest.

The [DEFAULT] section contains variables that all tests inherit from.

Included files will inherit the top-level variables but may override
in their own [DEFAULT] section.
