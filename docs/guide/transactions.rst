.. _guide-working-with-transactions:

Working with Transactions
=========================

When the customer completed their payment, you received a callback which contained a transaction ID. From this, you can load an :py:class:`altapay.Transaction` object, which will be used to perform further backoffice functions, such as capture money on a reservation.

The transaction itself is thought of as a separate resource from the :py:class`altapay.Payment`, and can be found using the :py:func:`altapay.Transaction.find` call:

.. code :: python

    from altapay import Transaction

    transaction = Transaction.find('TransactionID', api=api)

On the :py:class:`altapay.Transaction` object, you will find all of the information described in the AltaPay API, listed under the :samp:`API/payments` call. The usual rules for naming applies.

.. _guide-working-with-transactions-capturing-transaction:

Capturing a Transaction
+++++++++++++++++++++++

Once you have an instance of :py:class:`altapay.Transaction`, it is possible to perform actions on this instance. One of the most common one, is that of capturing it. In the simplest form, it is possible to capture the full amount on the transaction:

.. code :: python

    from altapay import Transaction

    transaction = Transaction.find('TransactionID', api=api)
    response = transaction.capture()

    if response.success:
        # Capture was successful
        pass
    else:
        raise Exception('Not able to capture')

The response is a bare :py:class:`altapay.Resource` and will contain the full response returned by AltaPay.

Of course, this is often not the desired behaviour. You can provider further information to :py:func:`altapay.Transaction.capture` as described in the AltaPay API of :samp:`API/captureReservation`. For example, you can capture a partial amount in the following way, which also shows how to supply an order line.

.. code :: python

    from altapay import Transaction

    transaction = Transaction.find('TransactionID', api=api)
    respnse = transaction.capture(
        orderLines=[{
            'description': 'Blue Shirt',
            'itemId': '12345',
            'quantity': 1.0,
            'unitPrice': 19.95
        }],
        amount=19.95)

.. _guide-working-with-transactions-charge-subscription:

Charging a Subscription
+++++++++++++++++++++++

Given a :py:class:`altapay.Transaction` which is a subscription, it is possible to make a charge (effectively issuing a capture directly on the subscription):

.. code :: python

    from altapay import Transaction

    transaction = Transaction.find('TransactionID', api=api)
    callback = transaction.charge_subscription(amount=49.00)

Charging a subscription will return a Callback object that has a list of transactions; one representing the original :py:class:`altapay.Transaction` you charged on, and a new one for the actual capture.

As always, see the AltaPay documentation for a list of possible arguments.

.. _guide-working-with-transactions-reserve-subscription:

Reserving a Subscription
++++++++++++++++++++++++

Reserving a transaction works much like :ref:`guide-working-with-transactions-charge-subscription`. The only difference is of course in the name: the amount will create a reservation instead of directly charging the amount straight away.

.. code :: python

    from altapay import Transaction

    transaction = Transaction.find('TransactionID', api=api)
    callback = transaction.reserve_subscription_charge(amount=49.00)

Reserving an amount on a  will return a Callback object that has a list of transactions; one representing the original :py:class:`altapay.Transaction` you reserved on, and a new one for the actual reservation.

As always, see the AltaPay documentation for a list of possible arguments.

.. _guide-working-with-transactions-releasing-reservation:

Releasing a Reservation
+++++++++++++++++++++++

In some cases you may choose to not capture your reservation. If so, it's better to release the reservation you have. This is also a good practice in cases where you have a subscription setup on a transaction ID, but you do not have any need for it anymore (for example if your customer cancels their subscription).

Note that there are certain edge cases for calling this method, see the AltaPay documentation for ``API/releaseReservation`` for full details.

.. code :: python

    from altapay import Transaction

    transaction = Transaction.find('TransactionID', api=api)
    callback = transaction.release()

    if callback.result != 'Success':
        raise Exception('Could not release the reservation')

.. _guide-working-with-transactions-creating-invoice-reservation:

Creating an Invoice Reservation
+++++++++++++++++++++++++++++++

In some cases, you might want to create an invoice reservation without first creating a Payment object. This could be if you do not want to redirect your customer to the payment provider for validation. In the example of Klarna payments, if you provide the customer's personal identification number together with the normal payment parameters, you can complete the transaction without further confirmation.

**Note that this might require approval by the invoice company you are using**

As always, see the full list of possible arguments in the AltaPay documentation.

.. code :: python

    from altapay import Callback

    parameters = {
        'terminal': 'AltaPay Test Terminal',
        'shop_orderid': 'asdf23',
        'amount': 20.0,
        'currency': 'EUR',
        'customer_info': {
            'billing_postal': '1234',
            'billing_address': 'Test Street',
            'email': 'foo@bar.com'
        },
        'personalIdentifyNumber': '123456-1234'
    }

    transaction = Callback.create_invoice_reservation(api=api, **parameters)
