from __future__ import absolute_import, unicode_literals

import responses
from altapay import API, Invoice

from .test_cases import TestCase


class InvoiceTest(TestCase):

    def setUp(self):
        self.api = API(mode='test', auto_login=False)

    @responses.activate
    def test_create_simple_invoice_request(self):

        invoice = Invoice(api=self.api)

        responses.add(
            responses.POST,
            self.get_api_url('API/createInvoiceReservation'),
            body=self.load_xml_response(
                '200_create_invoice_reservation_simple.xml'),
            status=200,
            content_type='application/xml')

        parameters = {
            'terminal': 'AltaPay Test Invoice Terminal DK',
            'shop_orderid': 111222333,
            'amount': 133.33,
            'currency': 'DKK',
            'customer_info': {
                'billing_postal': 9400,
                'billing_address': 'Address 12',
                'email': 'foo@bar.com'
            }
        }

        self.assertEqual(invoice.create(**parameters), True)

        dict = invoice.__data__
        trans = dict['transactions']['transaction']

        self.assertEqual(trans['terminal'], parameters['terminal'])
        self.assertEqual(
            trans['shop_order_id'],
            parameters['shop_orderid'])
        self.assertEqual(
            trans['customer_info']['billing_address']['address'],
            parameters['customer_info']['billing_address'])
        self.assertEqual(
            trans['customer_info']['billing_address']['postal_code'],
            parameters['customer_info']['billing_postal'])
        self.assertEqual(
            trans['customer_info']['email'],
            parameters['customer_info']['email'])

        self.assertEqual(invoice.success, True)
        # self.assert (dict['card_holder_error_message'])
        # self.assert (dict['merchant_error_message'])

    @responses.activate
    def test_create_complex_invoice_request(self):

        invoice = Invoice(api=self.api)

        responses.add(
            responses.POST,
            self.get_api_url('API/createInvoiceReservation'),
            body=self.load_xml_response(
                '200_create_invoice_reservation_complex.xml'),
            status=200,
            content_type='application/xml')

        params = {

            'terminal': 'AltaPay Test Invoice Terminal DK',
            'shop_orderid': '444555 complex invoice',
            'amount': 666.66,
            'currency': 'DKK',

            'transaction_info': {
                'ArbitraryInfo1': 'ArbitraryInfo2'
            },

            'type': 'payment',
            'accountNumber': '111',
            'bankCode': '222',
            'fraud_service': 'maxmind',
            'payment_source': 'eCommerce',
            'organisationNumber': '333',
            'personalIdentifyNumber': '444',
            'birthDate': '555',

            'orderLines': [
                {
                    'description': 'Description of the order line',
                    'itemId': '123456',
                    'quantity': 1,
                    'unitPrice': 500
                }
            ],

            'customer_info': {
                'email': 'customer@email.com',
                'username': 'leatheruser',
                'customer_phone': 4512345678,
                'bank_name': 'Gotham Bank',
                'bank_phone': '666 666 666',
                'billing_firstname': 'Bruce',
                'billing_lastname': 'Wayne',
                'billing_city':	'Gotham City',
                'billing_region': 'Dark Region',
                'billing_postal': '123',
                'billing_country': 'Bat Country',
                'billing_address': '101 Night Street',
                'shipping_firstname': 'Jack',
                'shipping_lastname': 'Napier',
                'shipping_address':	'42 Joker Avenue',
                'shipping_city': 'Big Smile City',
                'shipping_region': 'Umbrella Neighbourhood',
                'shipping_postal': '002',
                'shipping_country': 'Laughistan',
            },

        }

        self.assertEqual(invoice.create(**params), True)

        dict = invoice.__data__
        trans = dict['transactions']['transaction']

        self.assertEqual(trans['terminal'], params['terminal'])
        self.assertEqual(
            trans['shop_order_id'],
            params['shop_orderid'])

        self.assertEqual(trans['auth_type'], params['type'])

        self.assertEqual(
            trans['payment_infos']['payment_info']['@name'],
            'ArbitraryInfo1')
        self.assertEqual(
            trans['payment_infos']['payment_info']['#text'],
            'ArbitraryInfo2')

        self.assertEqual(
            trans['customer_info']['email'],
            params['customer_info']['email'])
        self.assertEqual(
            trans['customer_info']['username'],
            params['customer_info']['username'])
        self.assertEqual(
            trans['customer_info']['customer_phone'],
            params['customer_info']['customer_phone'])

        self.assertEqual(
            trans['customer_info']['billing_address']['firstname'],
            params['customer_info']['billing_firstname'])
        self.assertEqual(
            trans['customer_info']['billing_address']['lastname'],
            params['customer_info']['billing_lastname'])
        self.assertEqual(
            trans['customer_info']['billing_address']['city'],
            params['customer_info']['billing_city'])
        self.assertEqual(
            trans['customer_info']['billing_address']['region'],
            params['customer_info']['billing_region'])
        self.assertEqual(
            trans['customer_info']['billing_address']['postal_code'],
            int(params['customer_info']['billing_postal']))
        self.assertEqual(
            trans['customer_info']['billing_address']['country'],
            params['customer_info']['billing_country'])
        self.assertEqual(
            trans['customer_info']['billing_address']['address'],
            params['customer_info']['billing_address'])

        self.assertEqual(
            trans['customer_info']['shipping_address']['firstname'],
            params['customer_info']['shipping_firstname'])
        self.assertEqual(
            trans['customer_info']['shipping_address']['lastname'],
            params['customer_info']['shipping_lastname'])
        self.assertEqual(
            trans['customer_info']['shipping_address']['city'],
            params['customer_info']['shipping_city'])
        self.assertEqual(
            trans['customer_info']['shipping_address']['region'],
            params['customer_info']['shipping_region'])
        self.assertEqual(
            trans['customer_info']['shipping_address']['postal_code'],
            int(params['customer_info']['shipping_postal']))
        self.assertEqual(
            trans['customer_info']['shipping_address']['country'],
            params['customer_info']['shipping_country'])
        self.assertEqual(
            trans['customer_info']['shipping_address']['address'],
            params['customer_info']['shipping_address'])

        self.assertEqual(invoice.success, True)
