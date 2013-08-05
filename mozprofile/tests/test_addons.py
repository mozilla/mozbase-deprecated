#!/usr/bin/env python

import addon_stubs
import mozprofile
import mozfile
import tempfile
import os
import unittest
from manifestparser import ManifestParser


class TestAddonsManager(unittest.TestCase):
    """ Class to test mozprofile.addons.AddonManager """

    def setUp(self):
        self.profile = mozprofile.profile.Profile()
        self.am = mozprofile.addons.AddonManager(profile=self.profile.profile)

    def test_install_from_path(self):

        addons_to_install = []
        addons_installed = []

        # Generate installer stubs and install them
        tmpdir = tempfile.mkdtemp()
        for t in ['empty-0-1.xpi', 'another-empty-0-1.xpi']:
            temp_addon = addon_stubs.generate_addon(name=t, path=tmpdir)
            addons_to_install.append(self.am.addon_details(temp_addon)['id'])
            self.am.install_from_path(temp_addon)
        # Generate a list of addons installed in the profile
        addons_installed = [unicode(x[:-len('.xpi')]) for x in os.listdir(os.path.join(
                            self.profile.profile, 'extensions', 'staged'))]
        self.assertEqual(addons_to_install.sort(), addons_installed.sort())
        # Cleanup the temporary addon directories
        mozfile.rmtree(tmpdir)

    @unittest.skip("Feature not implemented as part of AddonManger")
    def test_install_from_path_error(self):
        """ Check install_from_path raises an error with an invalid addon"""

        temp_addon = addon_stubs.generate_invalid_addon()
        # This should raise an error here
        self.am.install_from_path(temp_addon)

    def test_install_from_manifest(self):

        temp_manifest = addon_stubs.generate_manifest()
        m = ManifestParser()
        m.read(temp_manifest)
        addons = m.get()
        # Obtain details of addons to install from the manifest
        addons_to_install = [self.am.addon_details(x['path'])['id'] for x in addons]

        self.am.install_from_manifest(temp_manifest)
        # Generate a list of addons installed in the profile
        addons_installed = [unicode(x[:-len('.xpi')]) for x in os.listdir(os.path.join(
                            self.profile.profile, 'extensions', 'staged'))]
        self.assertEqual(addons_installed.sort(), addons_to_install.sort())
        # Cleanup the temporary addon and manifest directories
        mozfile.rmtree(os.path.dirname(temp_manifest))

    @unittest.skip("Bug 900154")
    def test_clean_addons(self):

        addon_one = addon_stubs.generate_addon('empty-0-1.xpi')
        addon_two = addon_stubs.generate_addon('another-empty-0-1.xpi')

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


if __name__ == '__main__':
    unittest.main()
