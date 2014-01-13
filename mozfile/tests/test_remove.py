#!/usr/bin/env python

import os
import stat
import shutil
import tempfile
import unittest

import mozfile
import mozinfo

import stubs


def mark_readonly(path):
    """Removes all write permissions from given file/directory.

    :param path: path of directory/file of which modes must be changed
    """
    mode = os.stat(path)[stat.ST_MODE]
    os.chmod(path, mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)


class TestRemoveTree(unittest.TestCase):
    """test our ability to remove a directory tree"""

    def setUp(self):
        # Generate a stub
        self.tempdir = stubs.create_stub()

    def tearDown(self):
        if os.path.isdir(self.tempdir):
            shutil.rmtree(self.tempdir)

    def test_remove_directory(self):
        self.assertTrue(os.path.isdir(self.tempdir))
        mozfile.remove(self.tempdir)
        self.assertFalse(os.path.exists(self.tempdir))

    def test_remove_directory_with_open_file(self):
        """ Tests handling when removing a directory tree
            which has a file in it is still open """
        # Open a file in the generated stub
        filepath = os.path.join(self.tempdir, *stubs.files[1])
        f = file(filepath, 'w')
        f.write('foo-bar')

        # keep file open and then try removing the dir-tree
        if mozinfo.isWin:
            # On the Windows family WindowsError should be raised.
            self.assertRaises(WindowsError, mozfile.remove, self.tempdir)
            self.assertTrue(os.path.exists(self.tempdir))
        else:
            # Folder should be deleted on all other platforms
            mozfile.remove(self.tempdir)
            self.assertFalse(os.path.exists(self.tempdir))

    def test_remove_directory_after_closing_file(self):
        """ Test that the call to mozfile.rmtree succeeds on
            all platforms after file is closed """

        filepath = os.path.join(self.tempdir, *stubs.files[1])
        with open(filepath, 'w') as f:
            f.write('foo-bar')

        # Delete directory tree
        mozfile.remove(self.tempdir)

        # Check deletion is successful
        self.assertFalse(os.path.exists(self.tempdir))

    def test_remove_readonly_tree(self):
        """ Test that the mozfile.remove is able to remove readonly dirs """

        dirpath = os.path.join(self.tempdir, "nested_tree")
        mark_readonly(dirpath)

        # However, mozfile should change write permissions and remove dir.
        mozfile.remove(dirpath)

        self.assertFalse(os.path.exists(dirpath))

    def test_remove_readonly_file(self):
        """ Test that the mozfile.remove can remove readonly files """
        filepath = os.path.join(self.tempdir, *stubs.files[1])
        mark_readonly(filepath)

        # However, mozfile should change write permission and then remove file.
        mozfile.remove(filepath)

        self.assertFalse(os.path.exists(filepath))