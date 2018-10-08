import sys

# Update this with real path and uncomment before use, please
# sys.path.append('/absolute_path_to/python-client-library')


#sdk path check
sdkPathExists = False
for path in sys.path:
    if path.endswith("/python-client-library"):
        sdkPathExists=True
if sdkPathExists is False:
    print "Path to python-client-library does not exist, update your environment variable, or put sys.path.append('/absolute_path_to/python-cliend-library') before including altapay sdk modules"
    sys.exit()



from altapay import API, Reservation, Transaction

import string
import random
import json

def id_generator(size=15, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

order_id=id_generator()
# print order_id


api = API(mode='test',account='shop api', password='testpassword',  url='https://vmedev.pensio.com/merchant/')

res = Reservation(api=api)



params = {

    'terminal': 'AltaPay Soap Test Terminal',
    'shop_orderid': order_id,
    'amount': id_generator(3),
    'currency': 'DKK',
    'cardnum': '4111000011110002',
    'emonth': 1,
    'eyear': 2017,
    'cvc': '123',

    'transaction_info':
        {
            'ArbitraryInfo1': 'ArbitraryInfo2'
        },

    'type': 'payment',
    'fraud_service': 'maxmind',
    'payment_source': 'eCommerce',


    'customer_info': {
        'email': 'customer@email.com',
        'username': 'leatheruser',
        'customer_phone': '4512345678',
        'bank_name': 'Gotham Bank',
        'bank_phone': '666 666 666',
        'billing_firstname': 'Bruce',
        'billing_lastname': 'Wayne',
        'billing_city': 'Gotham City',
        'billing_region': 'Dark Region',
        'billing_postal': '001',
        'billing_country': 'DK',
        'billing_address': '101 Night Street',
        'shipping_firstname': 'Jack',
        'shipping_lastname': 'Napier',
        'shipping_address': '42 Joker Avenue',
        'shipping_city': 'Big Smile City',
        'shipping_region': 'Umbrella Neighbourhood',
        'shipping_postal': '002',
        'shipping_country': 'DK',
    },

}

res.create(**params)


print "--- RESERVATION ---"
print res.success
print res.error_message


print "--- CAPTURE ---"
#parse transaction from reservation response object
transaction = res.__data__.values()[1]["transaction"]

#find existing transaction on payment gateway by transaciton id
trans = Transaction.find(transaction['transaction_id'],api=api)
print trans


#define params for advanced transaction - can be empty
transParams = {
    'transaction_id': transaction["transaction_id"],
    'reconciliation_identifier': transaction["shop_order_id"],
    'invoice_number': transaction["shop_order_id"],
    'orderLines': [
        {
            'description': 'Description of the order line',
            'itemId': '123456',
            'quantity': 1,
            'unitPrice': 500,
            'taxAmount': 1000,
            'taxPercent': 80
        },
        {
            'description': 'Description of the order line2',
            'itemId': '1234567',
            'quantity': 200,
            'unitPrice': 3,
            'taxAmount': 10,
            'taxPercent': 2
        }
    ]    
}


#capture existing transaciton with defined params
trans.capture(**transParams)

#capture response
print trans