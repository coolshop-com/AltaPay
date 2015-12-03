from __future__ import absolute_import, unicode_literals

from six.moves.urllib.parse import urljoin

import responses
from altapay.api import API
from altapay.payment import Payment

from .test_cases import TestCase


class PaymentTest(TestCase):
    def setUp(self):
        self.api = API(mode='test', auto_login=False)
        self.create_url = urljoin(self.api.url, 'API/createPaymentRequest')

    @responses.activate
    def test_create_simple_payment_request(self):
        payment = Payment(api=self.api)
        responses.add(
            responses.GET, self.create_url,
            body=self.load_xml_response('200_create_payment.xml'), status=200,
            content_type='application/xml')
        parameters = {
            'terminal': 'Test Terminal',
            'shop_orderid': 1234567,
            'amount': 9.95,
            'currency': 'EUR'
        }
        self.assertEqual(payment.create(**parameters), True)
        self.assertIn('url', payment)
        self.assertEqual(len(payment.url) > 0, True)
