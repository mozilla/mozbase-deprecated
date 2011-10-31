import os
from setuptools import setup

try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except IOError:
    description = None

version = '0.2'

deps = ['mozinfo']

setup(name='mozInstall',
      version=version,
      description="This is a utility package for installing Mozilla applications on various platforms.",
      long_description=description,
      classifiers=['Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                  ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla',
      author='mdas',
      author_email='mdas@mozilla.com',
      url='https://github.com/mozilla/mozbase',
      license='MPL',
      py_modules=['mozinstall'],
      packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      mozinstall = mozinstall:cli
      """,
      )
