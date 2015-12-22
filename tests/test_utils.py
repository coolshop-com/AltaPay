from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
from xml.etree import ElementTree

from six.moves.urllib.parse import quote

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

    def test_http_build_query_simple(self):
        payload = OrderedDict([('a', '1'), ('b', 2)])
        query_string = utils.http_build_query(payload)
        self.assertEqual(query_string, 'a=1&b=2')

    def test_http_build_query_simple_list(self):
        payload = OrderedDict([('a', ['1', '2']), ('b', [3, 4])])
        query_string = utils.http_build_query(payload)
        self.assertEqual(
            query_string, quote('a[0]=1&a[1]=2&b[0]=3&b[1]=4', safe='/=&'))

    def test_http_build_query_complex_dict(self):
        payload = OrderedDict([
            ('customer', OrderedDict([
                ('name', 'test'), ('address', 'testaddress')]
            ))
        ])
        query_string = utils.http_build_query(payload)
        self.assertEqual(
            query_string, quote(
                'customer[name]=test&customer[address]=testaddress',
                safe='/=&'))

    def test_http_build_query_list_with_complex_dict(self):
        payload = OrderedDict([
            ('orderline', [
                OrderedDict([
                    ('title', 'test'), ('qty', 1)
                ]),
                OrderedDict([
                    ('title', 'test2'), ('qty', 2)
                ])
            ])
        ])
        query_string = utils.http_build_query(payload)
        self.assertEqual(
            query_string, quote((
                'orderline[0][title]=test&orderline[0][qty]=1&'
                'orderline[1][title]=test2&orderline[1][qty]=2'),
                safe='/=&'))

    def test_http_build_query_nested_dict(self):
        payload = OrderedDict([
            ('customer', OrderedDict([
                ('address', OrderedDict([
                    ('name', 'testname'),
                    ('address', 'testaddr')
                ]))
            ]))
        ])
        query_string = utils.http_build_query(payload)
        self.assertEqual(
            query_string, quote((
                'customer[address][name]=testname&'
                'customer[address][address]=testaddr'), safe='/=&'))
