from __future__ import absolute_import, unicode_literals

import responses
from altapay import API, Reservation

from .test_cases import TestCase


class ReservationTest(TestCase):

    def setUp(self):
        self.api = API(mode='test', auto_login=False)

    @responses.activate
    def test_read_reservation_response(self):

        reserv = Reservation(api=self.api)

        responses.add(
            responses.POST,
            self.get_api_url('API/reservation'),
            body=self.load_xml_response('200_reservation.xml'),
            status=200,
            content_type='application/xml')

        parameters = {
            'terminal': 'Some terminal',
            'shop_orderid': 123,
            'amount': 1.2,
            'currency': 'DKK',
            'customer_info': {
                'billing_postal': 456,
                'billing_address': 'Address 1',
                'email': 'foo@bar.com'
            }
        }

        self.assertEqual(reserv.create(**parameters), True)

        self.assertEqual(reserv.success, True)

        dict = reserv.__data__
        trans = dict['transactions']['transaction']

        self.assertEqual(trans['terminal'], 'AltaPay Soap Test Terminal')
        self.assertEqual(trans['shop_order_id'],
                         'ReservationTest_1500636267075')
        self.assertEqual(trans['auth_type'], 'paymentAndCapture')
        self.assertEqual(trans['captured_amount'], 1.23)
        self.assertEqual(trans['reserved_amount'], 1.23)

        self.assertEqual(trans['customer_info']['billing_address']['address'],
                         'billing address')

        self.assertEqual(
            trans['customer_info']['billing_address']['postal_code'],
            'billing postal')

        self.assertEqual(trans['customer_info']['email'], 'my@e.mail')
