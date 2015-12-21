from __future__ import absolute_import, unicode_literals

from xml.etree import ElementTree

from altapay import utils

from .test_cases import TestCase


class UtilsTest(TestCase):
    def test_to_pythonic_name(self):
        self.assertEqual(utils.to_pythonic_name('ABC'), 'abc')
        self.assertEqual(utils.to_pythonic_name('CamelCasing'), 'camel_casing')

    def test_etree_to_dict(self):
        xml_response = self.load_xml_response('etree_to_dict.xml')
        tree = ElementTree.XML(xml_response)
        response_as_dict = utils.etree_to_dict(tree)
        self.assertEqual(
            response_as_dict,
            {
                'APIResponse': {
                    'Header': {
                        'Date': '2015-12-12T21:35:23+01:00',
                        'ErrorCode': '0',
                        'Path': 'API/login',
                        'ErrorMessage': None
                    },
                    '@version': '20150526',
                    'Body': {
                        'Result': 'OK',
                        'TestNode': {
                            '#text': 'Test',
                            '@value': 'test'
                        }
                    }
                }
            }
        )
