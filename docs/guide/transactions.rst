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
    response_transactions = transaction.charge_subscription(amount=49.00)

Note that you should always receive a list of transactions when issuing a charge on a subscription, since you will receive one representing the original :py:class:`altapay.Transaction` you charged on, and a new one for the actual capture.

As always, see the AltaPay documentation for a list of possible arguments.
