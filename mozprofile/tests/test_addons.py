#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import mozprofile
import mozfile
import tempfile
import os
import unittest
from manifestparser import ManifestParser

from addon_stubs import generate_addon, generate_manifest

here = os.path.dirname(os.path.abspath(__file__))


class TestAddonsManager(unittest.TestCase):
    """ Class to test mozprofile.addons.AddonManager """

    def setUp(self):
        self.profile = mozprofile.profile.Profile()
        self.am = mozprofile.addons.AddonManager(profile=self.profile.profile)
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        mozfile.rmtree(self.tmpdir)

    def test_install_from_path_xpi(self):
        addons_to_install = []
        addons_installed = []

        # Generate installer stubs and install them
        for ext in ['test-addon-1@mozilla.org', 'test-addon-2@mozilla.org']:
            temp_addon = generate_addon(ext, path=self.tmpdir)
            addons_to_install.append(self.am.addon_details(temp_addon)['id'])
            self.am.install_from_path(temp_addon)

        # Generate a list of addons installed in the profile
        addons_installed = [unicode(x[:-len('.xpi')]) for x in os.listdir(os.path.join(
                            self.profile.profile, 'extensions', 'staged'))]
        self.assertEqual(addons_to_install.sort(), addons_installed.sort())

    def test_install_from_path_folder(self):
        # Generate installer stubs for all possible types of addons
        addons = []
        addons.append(generate_addon('test-addon-1@mozilla.org',
                                     path=self.tmpdir))
        addons.append(generate_addon('test-addon-2@mozilla.org',
                                     path=self.tmpdir,
                                     xpi=False))
        addons.append(generate_addon('test-addon-3@mozilla.org',
                                     path=self.tmpdir,
                                     name='addon-3'))
        addons.append(generate_addon('test-addon-4@mozilla.org',
                                     path=self.tmpdir,
                                     name='addon-4',
                                     xpi=False))

        self.am.install_from_path(self.tmpdir)

        # Bug 919368:
        # am.installed_addons cannot be used because XPI files are getting
        # copied to a temporary location first.

        # Get ids for addons installed into the profile
        addon_ids = [self.am.addon_details(x).get('id') for x in addons]
        addon_ids.sort()

        installed_addon_ids = [self.am.addon_details(x).get('id') for x in
                                   self.am._addons]
        installed_addon_ids.sort()

        self.assertEqual(addon_ids, installed_addon_ids)

    def test_install_from_path_invalid_addons(self):
        # Generate installer stubs for all possible types of addons
        addons = []
        addons.append(generate_addon('test-addon-invalid-no-manifest@mozilla.org',
                      path=self.tmpdir,
                      xpi=False))
        addons.append(generate_addon('test-addon-invalid-no-id@mozilla.org',
                      path=self.tmpdir))

        self.am.install_from_path(self.tmpdir)

        self.assertEqual(self.am.installed_addons, [])

    @unittest.skip("Feature not implemented as part of AddonManger")
    def test_install_from_path_error(self):
        """ Check install_from_path raises an error with an invalid addon"""

        temp_addon = generate_addon('test-addon-invalid-version@mozilla.org')
        # This should raise an error here
        self.am.install_from_path(temp_addon)

    def test_install_from_manifest(self):
        temp_manifest = generate_manifest(['test-addon-1@mozilla.org',
                                           'test-addon-2@mozilla.org'])
        m = ManifestParser()
        m.read(temp_manifest)
        addons = m.get()

        # Obtain details of addons to install from the manifest
        addons_to_install = [self.am.addon_details(x['path']).get('id') for x in addons]

        self.am.install_from_manifest(temp_manifest)
        # Generate a list of addons installed in the profile
        addons_installed = [unicode(x[:-len('.xpi')]) for x in os.listdir(os.path.join(
                            self.profile.profile, 'extensions', 'staged'))]
        self.assertEqual(addons_installed.sort(), addons_to_install.sort())

        # Cleanup the temporary addon and manifest directories
        mozfile.rmtree(os.path.dirname(temp_manifest))

    @unittest.skip("Bug 900154")
    def test_clean_addons(self):
        addon_one = generate_addon('test-addon-1@mozilla.org')
        addon_two = generate_addon('test-addon-2@mozilla.org')

        self.am.install_addons(addon_one)
        installed_addons = [unicode(x[:-len('.xpi')]) for x in os.listdir(os.path.join(
                            self.profile.profile, 'extensions', 'staged'))]

        # Create a new profile based on an existing profile
        # Install an extra addon in the new profile
        # Cleanup addons
        duplicate_profile = mozprofile.profile.Profile(profile=self.profile.profile,
                                                       addons=addon_two)
        duplicate_profile.addon_manager.clean_addons()

        addons_after_cleanup = [unicode(x[:-len('.xpi')]) for x in os.listdir(os.path.join(
                                duplicate_profile.profile, 'extensions', 'staged'))]
        # New addons installed should be removed by clean_addons()
        self.assertEqual(installed_addons, addons_after_cleanup)

    def test_noclean(self):
        """test `restore=True/False` functionality"""

        profile = tempfile.mkdtemp()
        tmpdir = tempfile.mkdtemp()

        try:
            # empty initially
            self.assertFalse(bool(os.listdir(profile)))

            # make an addon
            stub = generate_addon('test-addon-1@mozilla.org',
                                              path=tmpdir)

            # install it with a restore=True AddonManager
            addons  = mozprofile.addons.AddonManager(profile, restore=True)
            addons.install_from_path(stub)

            # now its there
            self.assertEqual(os.listdir(profile), ['extensions'])
            staging_folder = os.path.join(profile, 'extensions', 'staged')
            self.assertTrue(os.path.exists(staging_folder))
            self.assertEqual(os.listdir(staging_folder),
                             [os.path.basename(stub)])

            # del addons; now its gone though the directory tree exists
            del addons
            self.assertEqual(os.listdir(profile), ['extensions'])
            self.assertTrue(os.path.exists(staging_folder))
            self.assertEqual(os.listdir(staging_folder), [])

        finally:
            mozfile.rmtree(tmpdir)
            mozfile.rmtree(profile)


if __name__ == '__main__':
    unittest.main()
