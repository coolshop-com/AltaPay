from __future__ import absolute_import, unicode_literals

import unittest
from xml.etree import ElementTree

from altapay import utils

from .test_cases import TestCase


class UtilsTest(TestCase):
    def test_to_pythonic_name(self):
        self.assertEqual(utils.to_pythonic_name('ABC'), 'abc')
        self.assertEqual(utils.to_pythonic_name('CamelCasing'), 'camel_casing')

    @unittest.skip
    def test_etree_to_dict(self):
        xml_response = self.load_xml_response('200_login.xml')
        tree = ElementTree.XML(xml_response)
        response_as_dict = utils.etree_to_dict(tree)
        self.assertEqual(
            response_as_dict,
            {
                'APIResponse': {
                    'Header': {
                        'Date': '2015-12-18T10:23:41+01:00',
                        'ErrorCode': '0',
                        'Path': 'API/login',
                        'ErrorMessage': None
                    },
                    '@version': '20150526',
                    'Body': {
                        'Result': 'OK'
                    }
                }
            }
        )
