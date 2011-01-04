ManifestDestiny
===============

What ManifestDestiny gives you is:
- manifests are (ordered) lists of tests
- tests may have an arbitrary number of key, value pairs
- the parser returns an ordered list of test data structures, which
  are just dicts with some keys.  For example, a test with no
  user-specified metadata looks like this::

  {'path':
   '/home/jhammel/mozmill/src/ManifestDestiny/manifestdestiny/tests/testToolbar/testBackForwardButtons.js',
   'name': 'testToolbar/testBackForwardButtons.js', 'here':
   '/home/jhammel/mozmill/src/ManifestDestiny/manifestdestiny/tests',
   'manifest': 'tests/mozmill-example.ini'}

If additional key, values were specified, they would be in this dict
as well.

Outside of 'path' (the path to the test), the remaining key, values
are up to convention to use.  There is a (currently very minimal)
generic integration layer in ManifestDestiny for use of all tests.
For instance, if the 'disabled' key is present, you can get the set of
tests without disabled (various other queries are doable as well).

Since the system is convention-based, the harnesses may do whatever
they want with the data.  They may ignore it completely, they may use
the provided integration layer, or they may provide their own
integration layer.  This should allow whatever sort of logic they
want.  For instance, if in yourtestharness you wanted to run only on
mondays for a certain class of tests::

 tests = []
 for test in manifests.tests:
     if 'runOnDay' in test:
        if calendar.day_name[calendar.weekday(*datetime.datetime.now().timetuple()[:3])].lower() == test['runOnDay'].lower():
            tests.append(test)
     else:
        tests.append(test)

To recap:
- the manifests allow you to specify test data
- the parser gives you this data
- you can use it however you want or process it further as you need

Tests are denoted by sections in an .ini file (see
http://hg.mozilla.org/automation/ManifestDestiny/file/tip/manifestdestiny/tests/mozmill-example.ini). 

Additional manifest files may be included with a [include:] directive:

[include:path-to-additional-file.manifest]

The path to included files is relative to the current manifest.

The [DEFAULT] section contains variables that all tests inherit from.

Included files will inherit the top-level variables but may override
in their own [DEFAULT] section.
