Tests are denoted by sections in an .ini file (see
http://k0s.org/mozilla/hg/ManifestDestiny/file/tip/manifestdestiny/tests/mozmill-example.ini). 

Additional manifest files may be included with a [include:] directive:

[include:path-to-additional-file.manifest]

The path to included files is relative to the current manifest.

The [GENERAL] section contains variables that all tests inherit from.
In addition, variables declared in [GENERAL] may be referenced as
%(variable)s within the file (see
http://docs.python.org/library/configparser.html).

Included files will inherit the [GENERAL] variables but may override
in their own [GENERAL] section.
