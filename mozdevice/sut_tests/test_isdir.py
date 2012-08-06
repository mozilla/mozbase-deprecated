# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from dmunit import DeviceManagerTestCase

class IsDirTestCase(DeviceManagerTestCase):

    def runTest(self):
        """This tests the isDir() function.
        """
        testroot = self.dm.getDeviceRoot() + '/infratest'
        self.dm.removeDir(testroot)
        self.dm.mkDir(testroot)
        self.assertTrue(self.dm.isDir(testroot))
        testdir = testroot + '/testdir'
        self.assertFalse(self.dm.isDir(testdir))
        self.dm.mkDir(testdir)
        self.assertTrue(self.dm.isDir(testdir))
        origFile = open('test-files/mytext.txt', 'r').read()
        self.dm.pushFile('test-files/mytext.txt', testdir + '/mytext.txt')
        self.assertFalse(self.dm.isDir(testdir + '/mytext.txt'))
        self.dm.removeDir(testroot)
        self.assertFalse(self.dm.isDir(testroot))
        self.assertFalse(self.dm.isDir(testdir))
        self.assertFalse(self.dm.isDir(testdir + '/mytext.txt'))
        self.assertFalse(self.dm.isDir('/rootdoesnotexist/subdoesnotexist'))
