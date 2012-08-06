# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from dmunit import DeviceManagerTestCase

class PushBinaryTestCase(DeviceManagerTestCase):

  def runTest(self):
    """This tests copying a binary file.
    """
    testroot = self.dm.getDeviceRoot()
    self.dm.removeFile(testroot + '/mybinary.zip')
    self.assert_(self.dm.pushFile('test-files/mybinary.zip', testroot + '/mybinary.zip'))
