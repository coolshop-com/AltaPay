from __future__ import absolute_import, unicode_literals

from xml.etree import ElementTree

import responses
from altapay import API, Callback, Transaction

from .test_cases import TestCase


class CallbackTest(TestCase):
    def setUp(self):
        self.api = API(mode='test', auto_login=False)
        self.response_as_str = self.load_xml_response(
            '200_callback_multiple.xml')
        self.response_as_etree = ElementTree.XML(self.response_as_str)
        self.response_single_as_str = self.load_xml_response(
            '200_callback_single.xml')

    @responses.activate
    def test_load_from_str(self):
        callback = Callback.from_xml_callback(self.response_as_str)

        self.assertEqual(callback.result, 'Success')

    def test_load_from_etree(self):
        callback = Callback.from_xml_callback(self.response_as_etree)

        self.assertEqual(callback.result, 'Success')

    def test_transaction_set(self):
        callback = Callback.from_xml_callback(self.response_as_etree)

        transactions = callback.transactions()

        self.assertEqual(len(transactions), 2)
        for transaction in transactions:
            self.assertIsInstance(transaction, Transaction)

    def test_transaction_set_filter(self):
        callback = Callback.from_xml_callback(self.response_as_etree)

        transactions = callback.transactions(auth_type='subscription_payment')

        self.assertEqual(len(transactions), 1)
        self.assertIsInstance(transactions[0], Transaction)

    def test_transaction_set_single(self):
        callback = Callback.from_xml_callback(self.response_single_as_str)

        transactions = callback.transactions(auth_type='subscription_payment')

        self.assertIsInstance(transactions, list)
        self.assertEqual(len(transactions), 1)
        self.assertIsInstance(transactions[0], Transaction)
