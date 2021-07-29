import os
import random
import unittest
from datetime import date

from altapay import (API, Funding, FundingList, Invoice, Payment, Reservation,
                     Transaction)
from tests.integration import (altapay_account,
                               altapay_invoice_test_terminal_name,
                               altapay_password, altapay_test_terminal_name,
                               altapay_url)


def generate_order_id():
    return 'Test_' + str(random.randint(1000, 999999)) + '_PY'


class APITest(unittest.TestCase):

    def setUp(self):
        self.api = API(mode='test', account=altapay_account,
                       password=altapay_password,
                       url=altapay_url)

    def test_create_payment_request(self):
        print("--- PAYMENT REQUEST ---")

        payment = Payment(api=self.api)

        parameters = {
            'terminal': altapay_test_terminal_name,
            'shop_orderid': generate_order_id(),
            'amount': 1.00,
            'currency': 'EUR'
        }
        self.assertEqual(payment.create(**parameters), True)
        self.assertIn('url', payment)
        self.assertEqual(len(payment.url) > 0, True)

    def test_create_moto_reservation(self):
        reservation = Reservation(api=self.api)
        date_today = date.today()
        params = {

            'terminal': altapay_test_terminal_name,
            'shop_orderid': generate_order_id(),
            'amount': '25',
            'currency': 'DKK',
            'cardnum': '4111000011110002',
            'emonth': date_today.month,
            'eyear': date_today.year + 1,
            'cvc': '123'
        }

        print("--- RESERVATION ---")
        self.assertEqual(reservation.create(**params), True)
        self.assertEqual(reservation.success, True)

    def test_reservation_capture(self):
        print("--- CAPTURE ---")

        reservation = Reservation(api=self.api)
        date_today = date.today()
        params = {

            'terminal': altapay_test_terminal_name,
            'shop_orderid': generate_order_id(),
            'amount': '25',
            'currency': 'DKK',
            'cardnum': '4111000011110002',
            'emonth': date_today.month,
            'eyear': date_today.year + 1,
            'cvc': '123'
        }

        reservation.create(**params)

        # parse transaction from reservation response object
        transaction = list(reservation.__data__.values())[1]["transaction"]

        # find existing transaction on payment gateway by transaction id
        trans = Transaction.find(transaction['transaction_id'], api=self.api)
        # define params for advanced transaction - can be empty
        transaction_params = {
            'transaction_id': transaction["transaction_id"],
            'reconciliation_identifier': transaction["shop_order_id"],
            'invoice_number': transaction["shop_order_id"],
            'orderLines': [
                {
                    'description': 'Description of the order line',
                    'itemId': generate_order_id(),
                    'quantity': 1,
                    'unitPrice': 500,
                    'taxAmount': 1000,
                    'taxPercent': 80
                },
                {
                    'description': 'Description of the order line2',
                    'itemId': generate_order_id(),
                    'quantity': 200,
                    'unitPrice': 3,
                    'taxAmount': 10,
                    'taxPercent': 2
                }
            ]
        }

        # capture existing transaction with defined params
        self.assertEqual(trans.capture(**transaction_params).result, 'Success')

    def test_release_reservation(self):
        print("--- RELEASE ---")
        reservation = Reservation(api=self.api)
        date_today = date.today()
        params = {

            'terminal': altapay_test_terminal_name,
            'shop_orderid': generate_order_id(),
            'amount': '25',
            'currency': 'DKK',
            'cardnum': '4111000011110002',
            'emonth': date_today.month,
            'eyear': date_today.year + 1,
            'cvc': '123'
        }

        reservation.create(**params)
        # parse transaction from reservation response object
        response = list(reservation.__data__.values())
        transaction_id = response[1]["transaction"]["transaction_id"]
        transaction = Transaction.find(transaction_id, self.api)
        callback = transaction.release()

        self.assertEqual(callback.result, 'Success')
        self.assertEqual(len(callback.transactions()), 1)

    def test_refund_reservation(self):
        print("--- REFUND ---")
        reservation = Reservation(api=self.api)
        date_today = date.today()
        order_id = generate_order_id()
        params = {

            'terminal': altapay_test_terminal_name,
            'shop_orderid': order_id,
            'amount': '25',
            'currency': 'DKK',
            'cardnum': '4111000011110002',
            'emonth': date_today.month,
            'eyear': date_today.year + 1,
            'cvc': '123'
        }

        reservation.create(**params)
        # parse transaction from reservation response object
        response = list(reservation.__data__.values())
        transaction_id = response[1]["transaction"]["transaction_id"]
        transaction = Transaction.find(transaction_id, self.api)

        transaction_params = {
            'transaction_id': transaction_id,
            'reconciliation_identifier': order_id,
            'invoice_number': order_id,
            'orderLines': [
                {
                    'description': 'Description of the order line',
                    'itemId': generate_order_id(),
                    'quantity': 1,
                    'unitPrice': 500,
                    'taxAmount': 1000,
                    'taxPercent': 80
                },
                {
                    'description': 'Description of the order line2',
                    'itemId': generate_order_id(),
                    'quantity': 200,
                    'unitPrice': 3,
                    'taxAmount': 10,
                    'taxPercent': 2
                }
            ]
        }

        transaction.capture(**transaction_params)

        transaction_params = {
            'transaction_id': transaction_id,
            'reconciliation_identifier': order_id,
            'amount': '21',
            'currency': 'DKK',
            'orderLines': [
                {
                    'description': 'Description of the order line',
                    'itemId': generate_order_id(),
                    'quantity': 1,
                    'unitPrice': 500
                },
                {
                    'description': 'Description of the order line2',
                    'itemId': generate_order_id(),
                    'quantity': 200,
                    'unitPrice': 3
                }
            ]
        }

        callback = transaction.refund(**transaction_params)
        self.assertEqual(callback.result, 'Success')

    def test_charge_subscription(self):
        print("--- CHARGE SUBSCRIPTION ---")
        reservation = Reservation(api=self.api)
        date_today = date.today()
        order_id = generate_order_id()
        params = {

            'terminal': altapay_test_terminal_name,
            'shop_orderid': order_id,
            'amount': '25',
            'currency': 'DKK',
            'cardnum': '4111000011110002',
            'emonth': date_today.month,
            'eyear': date_today.year + 1,
            'cvc': '123',
            'type': 'subscription',
            'agreement_type': 'recurring'
        }

        reservation.create(**params)
        # parse transaction from reservation response object
        response = list(reservation.__data__.values())
        transaction_id = response[1]["transaction"]["transaction_id"]
        transaction = Transaction.find(transaction_id, self.api)

        transaction_params = {
            'transaction_id': transaction_id,
            'reconciliation_identifier': order_id,
            'amount': '21',
            'currency': 'DKK'
        }
        capture_result = transaction.charge_subscription(**transaction_params)
        self.assertEqual(capture_result.result, "Success")

    def test_reverse_subscription_charge(self):
        print("--- REVERSE SUBSCRIPTION CHARGE ---")
        reservation = Reservation(api=self.api)
        date_today = date.today()
        params = {

            'terminal': altapay_test_terminal_name,
            'shop_orderid': generate_order_id(),
            'amount': '25',
            'currency': 'DKK',
            'cardnum': '4111000011110002',
            'emonth': date_today.month,
            'eyear': date_today.year + 1,
            'cvc': '123',
            'type': 'subscription',
            'agreement_type': 'recurring'
        }

        reservation.create(**params)
        # parse transaction from reservation response object
        response = list(reservation.__data__.values())
        transaction_id = response[1]["transaction"]["transaction_id"]
        transaction = Transaction.find(transaction_id, self.api)

        transaction_params = {
            'transaction_id': transaction_id,
            'amount': '21',
            'currency': 'DKK'
        }

        reverse_result = transaction\
            .reserve_subscription_charge(**transaction_params)

        self.assertEqual(reverse_result.result, "Success")

    def test_funding_list(self):
        print("--- FUNDING LIST ---")
        funding_list = FundingList(api=self.api)
        self.assertIsNotNone(funding_list.fundings)
        for funding in funding_list.fundings:
            self.assertIsInstance(funding, Funding)

        while funding_list._current_page < funding_list.number_of_pages - 1:
            funding_list.next_page()
            self.assertGreater(len(funding_list.fundings), 0)
        contract_identifier = funding_list.fundings[-1].contract_identifier
        self.assertEqual(contract_identifier, 'EmbraceIT')

    def test_funding_list_download(self):
        print("--- FUNDING LIST DOWNLOAD ---")
        funding_list = FundingList(api=self.api)
        funding = funding_list.fundings[-1]
        filepath = funding.download('./')
        with open(filepath, 'rb') as fd:
            content = fd.read()
        self.assertEqual(content, funding.content())
        os.remove(filepath)

    def test_fraud_check_in_charge(self):
        print("--- FRAUD CHECK IN CHARGE ---")
        reservation = Reservation(api=self.api)
        date_today = date.today()
        params = {

            'terminal': altapay_test_terminal_name,
            'shop_orderid': generate_order_id(),
            'amount': '3.00',
            'currency': 'DKK',
            'cardnum': '4111111111111111',
            'emonth': date_today.month,
            'eyear': date_today.year + 1,
            'cvc': '123',

            'transaction_info': {
                'fraudCheckTest': 'Checkit!'
            }
        }

        reservation.create(**params)
        reservation_data = reservation.__data__
        trans = reservation_data['transactions']['transaction']
        self.assertEqual(
            trans['payment_infos']['payment_info']['@name'],
            'fraudCheckTest')
        self.assertEqual(
            trans['payment_infos']['payment_info']['#text'],
            'Checkit!')

    def test_create_simple_invoice_request(self):
        print("--- SIMPLE INVOICE ---")

        invoice = Invoice(api=self.api)

        parameters = {
            'terminal': altapay_invoice_test_terminal_name,
            'shop_orderid': generate_order_id(),
            'amount': 133.33,
            'currency': 'DKK',
            'customer_info': {
                'billing_postal': 9400,
                'billing_address': 'Address 12',
                'email': 'foo@bar.com'
            }
        }

        self.assertEqual(invoice.create(**parameters), True)

        invoice_data = invoice.__data__
        trans = invoice_data['transactions']['transaction']

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

    def test_create_complex_invoice_request(self):
        print("--- COMPLEX INVOICE ---")

        invoice = Invoice(api=self.api)

        params = {

            'terminal': altapay_invoice_test_terminal_name,
            'shop_orderid':  generate_order_id(),
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
            'birthDate': '1960-11-02',

            'orderLines': [
                {
                    'description': 'Description of the order line',
                    'itemId': generate_order_id(),
                    'quantity': 1,
                    'unitPrice': 500
                }
            ],

            'customer_info': {
                'email': 'customer@email.com',
                'username': 'testuser',
                'customer_phone': 4512345678,
                'bank_name': 'Gotham Bank',
                'bank_phone': '666 666 666',
                'billing_firstname': 'first',
                'billing_lastname': 'last',
                'billing_city': 'city',
                'billing_region': 'region',
                'billing_postal': '9400',
                'billing_country': 'US',
                'billing_address': 'street',
                'shipping_firstname': 'shipping first',
                'shipping_lastname': 'shipping last',
                'shipping_address': 'shipping address',
                'shipping_city': 'shipping city',
                'shipping_region': 'shipping region',
                'shipping_postal': '9400',
                'shipping_country': 'US',
            },

        }

        self.assertEqual(invoice.create(**params), True)

        invoice_data = invoice.__data__
        trans = invoice_data['transactions']['transaction']

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
