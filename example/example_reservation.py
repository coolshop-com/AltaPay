from altapay import API, Reservation

api = API(mode='test',account='shop api', password='testpassword',  url='http://gateway.dev.earth.pensio.com/merchant/')

res = Reservation(api=api)

params = {

    'terminal': 'AltaPay Soap Test Terminal',
    'shop_orderid': '444555 complex reservation',
    'amount': 666.66,
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

print res.success
print res.error_message

print res.__data__
