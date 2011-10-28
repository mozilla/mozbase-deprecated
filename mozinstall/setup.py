import os
from setuptools import setup

try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except IOError:
    description = None

version = '0.0'

deps = []

setup(name='mozInstall',
      version=version,
      description="This is a utility package for installing and uninstalling Firefox on various platforms.",
      long_description=description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla',
      author='mdas',
      author_email='mdas@mozilla.com',
      url='https://github.com/mozautomation/mozInstall',
      license='MPL',
      py_modules=['mozInstall'],
      packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
