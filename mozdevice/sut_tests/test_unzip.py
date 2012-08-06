# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from dmunit import DeviceManagerTestCase

class UnzipTestCase(DeviceManagerTestCase):

    def runTest(self):
        """ This tests unzipping a file on the device.
        """
        testroot = self.dm.getDeviceRoot() + '/infratest'
        self.dm.removeDir(testroot)
        self.dm.mkDir(testroot)
        self.assert_(self.dm.pushFile('test-files/mybinary.zip', testroot + '/mybinary.zip'))
        self.assertNotEqual(self.dm.unpackFile(testroot + '/mybinary.zip'), None)
        # the mybinary.zip file has the zipped up contents of test-files/push2
        # so we validate it the same as test_push2.
        self.assert_(self.dm.dirExists(testroot + '/push2/sub1'))
        self.assert_(self.dm.validateFile(testroot + '/push2/sub1/file1.txt',
                                          'test-files/push2/sub1/file1.txt'))
        self.assert_(self.dm.validateFile(testroot + '/push2/sub1/sub1.1/file2.txt',
                                          'test-files/push2/sub1/sub1.1/file2.txt'))
        self.assert_(self.dm.validateFile(testroot + '/push2/sub2/file3.txt',
                                          'test-files/push2/sub2/file3.txt'))
        self.assert_(self.dm.validateFile(testroot + '/push2/file4.bin',
                                          'test-files/push2/file4.bin'))

        # test dest_dir param
        newdir = testroot + '/newDir'
        self.dm.mkDir(newdir)
        self.assertNotEqual(self.dm.unpackFile(testroot + '/mybinary.zip',
                            newdir), None)
        # check files
        self.assert_(self.dm.dirExists(newdir + '/push2/sub1'))
        self.assert_(self.dm.validateFile(newdir + '/push2/sub1/file1.txt',
                                          'test-files/push2/sub1/file1.txt'))
        self.assert_(self.dm.validateFile(newdir + '/push2/sub1/sub1.1/file2.txt',
                                          'test-files/push2/sub1/sub1.1/file2.txt'))
        self.assert_(self.dm.validateFile(newdir + '/push2/sub2/file3.txt',
                                          'test-files/push2/sub2/file3.txt'))
        self.assert_(self.dm.validateFile(newdir + '/push2/file4.bin',
                                          'test-files/push2/file4.bin'))
