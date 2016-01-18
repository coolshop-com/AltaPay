.. _guide-callback-handling:

Callback Handling
=================

To make it easy to parse callbacks received from AltaPay, the special :py:class:`altapay.Callback` class can be used. Note that when you receive callbacks from AltaPay, it comes as an HTTP POST. Within this is a field called :samp:`xml`, and this is the response you should use for the :py:class:`altapay.Callback` class.

Given a callback response in the variable :samp:`xml`, this is how a callback instance can be instantiated:

.. code :: python

    from altapay import Callback

    xml = ''  # XML response here

    callback = Callback.from_xml_callback(xml)

    if callback.result == 'Success':
        for transaction in callback.transactions():
            print(transaction)
    else:
        raise Exception('Callback not successful')

:py:func:`altapay.Callback.transactions` will contain a list of :py:class:`altapay.Transaction` objects. Note that even if there is only one transaction in the callback, you will have a list of just one :py:class:`altapay.Transaction`.

Using :py:func:`altapay.Callback.transactions` it is possible to filter based on a authentication type (this will depend on what you chose for the payment type). This can be useful if you have chosen to make a subscription and reservation in the same payment; in this case you can receive a callback with two transactions, and in some cases you might want to process a specific of them ahead of the other one.

This example extends the usecase described above, and filters out the subscription portion of the payment:

.. code :: python

    from altapay import Callback

    xml = ''  # XML response here

    callback = Callback.from_xml_callback(xml)

    if callback.result == 'Success':
        transactions = callback.transactions(auth_type='subscription_payment')
        for transaction in transactions:
            # Will only show transactions of the authentication type
            # subscription_payment
            print(transaction)
    else:
        raise Exception('Callback not successful')
