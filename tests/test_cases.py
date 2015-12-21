"""
Test cases for testing of AltaPay SDK.

Note that this module for now simply exposes the default Python unittest module
test case classes, namely TestCase and SkipTest. At some point in the future,
this module might expose different test cases with additional specific AltaPay
functionality.
"""
import os
from unittest import SkipTest, TestCase  # NOQA
from xml.etree import ElementTree

from six.moves.urllib.parse import urljoin

from altapay import utils


class TestCase(TestCase):
    def load_dict_response(self, xml_response):
        return utils.etree_to_dict(ElementTree.XML(xml_response))

    def load_xml_response(self, filename):
        path = os.path.join(os.path.dirname(__file__), 'xml', filename)
        with open(path, 'r') as f:
            return f.read()
            return utils.etree_to_dict(ElementTree.XML(f.read()))

    def get_api_url(self, resource):
        return urljoin(self.api.url, resource)
