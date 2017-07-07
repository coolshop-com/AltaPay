#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

Klarna test script.

"""

from altapay import API, Payment

import random, sys

# These lines are only necessary because we are using utf-8 characters in the billing address:
reload(sys)
sys.setdefaultencoding('utf8')

api = API(mode='test',account='shop api', password='testpassword',  url='http://gateway.dev.earth.pensio.com/merchant/')

payment = Payment(api = api)

params = {

            'terminal': 'AltaPay Klarna DK',
            'shop_orderid': 'Example_Klarna' + str(random.randint(1, 1000)),
            'amount': 5.5,
            'currency': 'DKK',
            'type': 'payment',

            'accountNumber': '111',
            'bankCode': '222',
            'fraud_service': 'maxmind',
            'payment_source': 'eCommerce',
            'organisationNumber': '333',
            'personalIdentifyNumber': '444',
            'birthDate': '555',

            'customer_info': {
                'email': 'myuser@mymail.com',
                'username': 'myuser',
                'customer_phone': '20123456',
                'bank_name': 'My Bank',
                'bank_phone': '+45 12-34 5678',
                'billing_firstname': 'Testperson-dk',
                'billing_lastname': 'Approved',
                'billing_city':	'Varde',
                'billing_region': 'DK',
                'billing_postal': '6800',
                'billing_country': 'DK',
                'billing_address': 'Sæffleberggate 56,1 mf',
                'shipping_firstname': 'Testperson-dk',
                'shipping_lastname': 'Approved',
                'shipping_city':	'Varde',
                'shipping_region': 'DK',
                'shipping_postal': '6800',
                'shipping_country': 'DK',
                'shipping_address': 'Sæffleberggate 56,1 mf',
            },

            'orderLines': [
                {
                    'description': 'description 01',
                    'itemId': 'id 01',
                    'quantity': 1,
                    'unitPrice': 1.1
                },
                {
                    'description': 'description 02',
                    'itemId': 'id 02',
                    'quantity': 2,
                    'unitPrice': 2.2
                }
            ],

        }

payment.create(**params)

if payment.success:
    print "Success!"
    # Access the url below and use the social security number 0801363945 in the page form to complete the Klarna order
    print payment.url
else:
    print "Error code: " + str(payment.error_code)
    print "Error message: " + payment.error_message

# All the data
#print payment.__data__
