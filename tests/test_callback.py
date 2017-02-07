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

    @responses.activate
    def test_create_invoice_reservation(self):
        responses.add(
            responses.POST, self.get_api_url('API/createInvoiceReservation'),
            body=self.load_xml_response('200_create_invoice_reservation.xml'),
            status=200, content_type='application/xml')

        parameters = {
            'terminal': 'AltaPay Test Terminal',
            'shop_orderid': 'asdf23',
            'amount': 20.0,
            'currency': 'EUR',
            'customer_info': {
                'billing_postal': '1234',
                'billing_address': 'Test Street',
                'email': 'foo@bar.com'
            },
            'personalIdentifyNumber': '123456-1234'
        }

        callback = Callback.create_invoice_reservation(
            api=self.api, **parameters)

        self.assertIsInstance(callback, Callback)
        self.assertIsInstance(callback.transactions(), list)
        self.assertIsInstance(callback.transactions()[0], Transaction)

    def test_epayment_cancelled(self):
        callback = Callback.from_xml_callback(
            self.load_xml_response('200_epayment_cancelled.xml'))

        transactions = callback.transactions()

        self.assertIsInstance(transactions, list)
        self.assertEqual(len(transactions), 1)
        self.assertIsInstance(transactions[0], Transaction)

        self.assertEqual('Cancelled', callback.result)
        self.assertEqual('epayment_cancelled',
                         transactions[0].transaction_status)
