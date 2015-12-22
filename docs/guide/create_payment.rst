.. _guide-create-payment:

Create Payment
==============

Creating a new :py:class:`altapay.Payment` resource will result in an URL that you should redirect your customer to.

It is in creating the payment you describe what payment options the customer should have, the total order amount, and other optional parameters. The parameters you use will depend on the terminal you wish to use.

.. _guide-create-payment-basic-payment:

Basic Payment
+++++++++++++

In the most basic form, a :py:class:`altapay.Payment` object requires a terminal, order ID amount and currency. Creating such payment will look something like this:

.. code :: python

    from altapay import API, Payment

    # Create an API object using your credentials
    api = API(...)

    # Create an empty payment object using the API
    payment = Payment(api=api)

    # Create a new payment using the AltaPay service.
    payment.create('Terminal Name', 'OrderID1234', 13.95, 'EUR')

    if payment.success:
        # Assuming a function redirect() which redirects the customer
        redirect(payment.url)
    else:
        raise Exception('Payment not successful')

This payment is, of course, only very basic, and will only render the standard AltaPay payment form - but it will work. There are, of course, a lot of configuration options.

For a detailed view of these, see the AltaPay API documentation for :samp:`API/createPaymentRequest`, bearing in mind the conventions described in :ref:`guide-introduction`.

.. _guide-create-payment-complex-payment:

Complex Payment
+++++++++++++++

Using only the basic payment information will not get you very far. In reality, you are going to want to customize it to your liking, for example using a custom callback form and more detailed order and customer information. Our recommendation would be to always include as much information as possible regarding the order and the customer, since you will be covered for more of the possible terminals this way.

This following example implements a lot of the different possibilities using the AltaPay service.

.. code :: python

    from altapay import API, Payment

    api = API(...)
    payment = Payment(api=api)

    # We can pass all of the optional parameters as keyword arguments to
    # the payment creation
    params = {
        'config': {
            'callback_form': 'https://your-callback-form/form.html',
        },
        'transaction_info': [
            'ArbitraryInfo1',
            'ArbitraryInfo2'
        ],
        'customer_info': {
            'billing_postal': '9400',
            'billing_address': 'Address 12',
            'billing_firstname': 'First name',
            'billing_lastname': 'Last name',
            'email': 'foo@bar.com'
        },
        'orderLines': [
            {
                'description': 'Description of the order line',
                'itemId': '123456',
                'quantity': 1
            }
        ]
    }

    payment.create('Terminal name', 'OrderID1234', 13.95, 'EUR', **params)

    if payment.success:
        redirect(payment.url)

The above example obviously is not complete; there are many more parameters which are described in the AltaPay API documentation. Remember: more data is better, and will result in more terminals working.
