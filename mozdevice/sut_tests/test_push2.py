# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from dmunit import DeviceManagerTestCase

class Push2TestCase(DeviceManagerTestCase):

  def runTest(self):
    """ This tests copying a directory structure with files to the device
    """
    testroot = self.dm.getDeviceRoot()
    testroot += '/infratest'
    self.dm.removeDir(testroot)
    self.dm.mkDir(testroot)
    path = testroot + '/push2'
    self.dm.pushDir('test-files/push2', path)

    # Let's walk the tree and make sure everything is there
    # though it's kind of cheesy, we'll use the validate file to compare
    # hashes - we use the client side hashing when testing the cat command
    # specifically, so that makes this a little less cheesy, I guess.
    self.assert_(self.dm.dirExists(testroot + '/push2/sub1'))
    self.assert_(self.dm.validateFile(testroot + '/push2/sub1/file1.txt',
                                      'test-files/push2/sub1/file1.txt'))
    self.assert_(self.dm.validateFile(testroot + '/push2/sub1/sub1.1/file2.txt',
                                      'test-files/push2/sub1/sub1.1/file2.txt'))
    self.assert_(self.dm.validateFile(testroot + '/push2/sub2/file3.txt',
                                      'test-files/push2/sub2/file3.txt'))
    self.assert_(self.dm.validateFile(testroot + '/push2/file4.bin',
                                      'test-files/push2/file4.bin'))
