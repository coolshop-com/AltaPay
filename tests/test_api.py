from __future__ import absolute_import, unicode_literals

import unittest

from altapay import exceptions
from altapay.api import API

from .test_cases import TestCase


class APITest(TestCase):
    def setUp(self):
        self.api = API(mode='test', auto_login=False)

    @unittest.skip
    def test_index_successful(self):
        self.assertEqual(self.api.index().success, True)

    def test_login_unauthorized(self):
        with self.assertRaises(exceptions.UnauthorizedAccessError):
            self.api.login()

    def test_headers(self):
        self.assertIsInstance(self.api._headers(), dict)
        self.assertIn('User-Agent', self.api._headers())

    def test_auto_login(self):
        with self.assertRaises(exceptions.UnauthorizedAccessError):
            API()

    def test_missing_url(self):
        with self.assertRaises(Exception):
            API(auto_login=False, mode='notworking')
