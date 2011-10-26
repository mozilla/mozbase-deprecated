import os
from setuptools import setup

try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except IOError:
    description = None

version = '0.1'

deps = []

setup(name='mozhttpd',
      version=version,
      description="basic python webserver, tested with talos",
      long_description=description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla',
      author='Joel Maher',
      author_email='tools@lists.mozilla.org',
      url='https://github.com/mozilla/mozbase/tree/master/mozhttpd',
      license='MPL',
      py_modules=['mozhttpd'],
      packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      mozhttpd = mozhttpd:main
      """,
      )

