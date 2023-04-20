from __future__ import absolute_import, unicode_literals

import responses

from altapay import API, Callback, Transaction
from altapay.exceptions import MultipleResourcesError, ResourceNotFoundError

from .test_cases import TestCase


class PaymentTest(TestCase):
    def setUp(self):
        self.api = API(mode='test', auto_login=False)

    @responses.activate
    def test_find_transaction_failure(self):
        responses.add(
            responses.GET, self.get_api_url('API/payments'),
            body=self.load_xml_response('200_find_transaction_failure.xml'),
            status=200, content_type='application/xml')

        with self.assertRaises(ResourceNotFoundError):
            Transaction.find('TEST-TRANSACTION-ID', self.api)

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

    @responses.activate
    def test_capture_transaction_simple(self):
        responses.add(
            responses.GET, self.get_api_url('API/payments'),
            body=self.load_xml_response('200_find_transaction_single.xml'),
            status=200, content_type='application/xml')

        transaction = Transaction.find('TEST-TRANSACTION-ID', self.api)

        self.assertEqual(transaction.captured_amount, 0.0)

        responses.add(
            responses.POST, self.get_api_url('API/captureReservation'),
            body=self.load_xml_response('200_capture_response.xml'),
            status=200, content_type='application/xml')

        callback = transaction.capture()

        self.assertEqual(
            callback.transactions()[0].captured_amount, 13.29)

    @responses.activate
    def test_charge_subscription_single(self):
        responses.add(
            responses.GET, self.get_api_url('API/payments'),
            body=self.load_xml_response('200_find_transaction_single.xml'),
            status=200, content_type='application/xml')

        # Note, this transaction technically isn't a valid subscription,
        # but it will do
        transaction = Transaction.find('TEST-TRANSACTION-ID', self.api)

        responses.add(
            responses.POST, self.get_api_url('API/chargeSubscription'),
            body=self.load_xml_response('200_charge_subscription_single.xml'),
            status=200, content_type='application/xml')

        callback = transaction.charge_subscription(amount=13.95)

        self.assertIsInstance(callback, Callback)

        self.assertEqual(len(callback.transactions()), 2)
        for transaction in callback.transactions():
            self.assertIsInstance(transaction, Transaction)

    @responses.activate
    def test_reserve_subscription_single(self):
        responses.add(
            responses.GET, self.get_api_url('API/payments'),
            body=self.load_xml_response('200_find_transaction_single.xml'),
            status=200, content_type='application/xml')

        # Note, this transaction technically isn't a valid subscription,
        # but it will do
        transaction = Transaction.find('TEST-TRANSACTION-ID', self.api)

        responses.add(
            responses.POST, self.get_api_url('API/reserveSubscriptionCharge'),
            body=self.load_xml_response('200_charge_subscription_single.xml'),
            status=200, content_type='application/xml')

        callback = transaction.reserve_subscription_charge(amount=13.95)

        self.assertIsInstance(callback, Callback)

        self.assertEqual(len(callback.transactions()), 2)
        for transaction in callback.transactions():
            self.assertIsInstance(transaction, Transaction)

    @responses.activate
    def test_release_reservation(self):
        responses.add(
            responses.GET, self.get_api_url('API/payments'),
            body=self.load_xml_response('200_find_transaction_single.xml'),
            status=200, content_type='application/xml')

        transaction = Transaction.find('TEST-TRANSACTION-ID', self.api)

        responses.add(
            responses.POST, self.get_api_url('API/releaseReservation'),
            body=self.load_xml_response('200_release_reservation.xml'),
            status=200, content_type='application/xml')

        callback = transaction.release()

        self.assertEqual(callback.result, 'Success')
        self.assertEqual(len(callback.transactions()), 1)
