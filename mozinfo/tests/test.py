#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import mock
import os
import shutil
import sys
import tempfile
import unittest

class TestMozinfo(unittest.TestCase):
    def setUp(self):
        import mozinfo
        reload(mozinfo)
        self.tempdir = os.path.abspath(tempfile.mkdtemp())

    def tearDown(self):
        del sys.modules["mozinfo"]
        shutil.rmtree(self.tempdir)

    def test_basic(self):
        """Test that mozinfo has a few attributes."""
        import mozinfo
        self.assertNotEqual(mozinfo.os, None)
        # should have isFoo == True where os == "foo"
        self.assertTrue(getattr(mozinfo, "is" + mozinfo.os[0].upper() + mozinfo.os[1:]))

    def test_update(self):
        """Test that mozinfo.update works."""
        import mozinfo
        mozinfo.update({"foo": 123})
        self.assertEqual(mozinfo.info["foo"], 123)

    def test_update_file(self):
        """Test that mozinfo.update can load a JSON file."""
        j = os.path.join(self.tempdir, "mozinfo.json")
        with open(j, "w") as f:
            f.write(json.dumps({"foo": "xyz"}))
        import mozinfo
        mozinfo.update(j)
        self.assertEqual(mozinfo.info["foo"], "xyz")

    def test_find_and_update_file(self):
        """Test that mozinfo.find_and_update_from_json can
        find mozinfo.json in a directory passed to it."""
        j = os.path.join(self.tempdir, "mozinfo.json")
        with open(j, "w") as f:
            f.write(json.dumps({"foo": "abcdefg"}))
        import mozinfo
        self.assertEqual(mozinfo.find_and_update_from_json(self.tempdir), j)
        self.assertEqual(mozinfo.info["foo"], "abcdefg")

    def test_find_and_update_file_mozbuild(self):
        """Test that mozinfo.find_and_update_from_json can
        find mozinfo.json using the mozbuild module."""
        j = os.path.join(self.tempdir, "mozinfo.json")
        with open(j, "w") as f:
            f.write(json.dumps({"foo": "123456"}))
        import mozinfo
        m = mock.MagicMock()
        # Mock the value of MozbuildObject.from_environment().topobjdir.
        m.MozbuildObject.from_environment.return_value.topobjdir = self.tempdir
        with mock.patch.dict(sys.modules, {"mozbuild": m, "mozbuild.base": m}):
            self.assertEqual(mozinfo.find_and_update_from_json(), j)
        self.assertEqual(mozinfo.info["foo"], "123456")

if __name__ == '__main__':
    unittest.main()
