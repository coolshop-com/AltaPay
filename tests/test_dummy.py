from __future__ import absolute_import, unicode_literals

from .test_cases import TestCase


class VersionTest(TestCase):
    def test_module_version(self):
        version = __import__('altapay').VERSION
        self.assertGreater(len(version), 0)
