# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from dmunit import DeviceManagerTestCase
import os

class Push1TestCase(DeviceManagerTestCase):

  def runTest(self):
    """ This tests copying a directory structure to the device
    """
    dvroot = self.dm.getDeviceRoot()
    dvpath = dvroot + '/infratest'
    self.dm.removeDir(dvpath)
    self.dm.mkDir(dvpath)

    # Set up local stuff
    try:
      os.rmdir('test-files/push1')
    except:
      pass

    if not os.path.exists('test-files/push1'):
      os.makedirs('test-files/push1/sub.1/sub.2')
    if not os.path.exists('test-files/push1/sub.1/sub.2/testfile'):
      file('test-files/push1/sub.1/sub.2/testfile', 'w').close()

    # push the directory
    self.dm.pushDir('test-files/push1', dvpath + '/push1')

    # verify
    self.assert_(self.dm.dirExists(dvpath + '/push1/sub.1'))
    self.assert_(self.dm.dirExists(dvpath + '/push1/sub.1/sub.2'))
