from __future__ import absolute_import, unicode_literals

import responses
from altapay import API, Transaction
from altapay.exceptions import MultipleResourcesError

from .test_cases import TestCase


class PaymentTest(TestCase):
    def setUp(self):
        self.api = API(mode='test', auto_login=False)

    @responses.activate
    def test_find_transaction_success(self):
        responses.add(
            responses.GET, self.get_api_url('API/payments'),
            body=self.load_xml_response('200_find_transaction_single.xml'),
            status=200, content_type='application/xml')

        transaction = Transaction.find('TEST-TRANSACTION-ID', self.api)

        # Test both for unpacking of single values and nested structures
        self.assertEqual(transaction.card_status, 'Valid')
        self.assertEqual(
            transaction.payment_nature_service['supports_refunds'], True)

    @responses.activate
    def test_find_transaction_multiple_resources_error(self):
        responses.add(
            responses.GET, self.get_api_url('API/payments'),
            body=self.load_xml_response('200_find_transaction_multiple.xml'),
            status=200, content_type='application/xml')

        with self.assertRaises(MultipleResourcesError):
            Transaction.find('TEST-TRANSACTION-ID', self.api)
