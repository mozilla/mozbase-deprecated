# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import unittest

import mozprofile
import mozrunner


@unittest.skipIf(not os.environ.get('BROWSER_PATH'),
                 'No binary has been specified.')
class MozrunnerTestCase(unittest.TestCase):

    def setUp(self):
        self.profile = mozprofile.FirefoxProfile()
        self.runner = mozrunner.FirefoxRunner(self.profile)

    def tearDown(self):
        self.runner.cleanup()
