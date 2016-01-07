.. _guide-working-with-transactions:

Working with Transactions
=========================

When the customer completed their payment, you received a callback which contained a transaction ID. From this, you can load an :py:class:`altapay.Transaction` object, which will be used to perform further backoffice functions, such as capture money on a reservation.

The transaction itself is thought of as a separate resource from the :py:class`altapay.Payment`, and can be found using the :py:func:`altapay.Transaction.find` call:

.. code :: python

    from altapay import Transaction

    transaction = Transaction.find('TransactionID', api=api)

On the :py:class:`altapay.Transaction` object, you will find all of the information described in the AltaPay API, listed under the :samp:`API/payments` call. The usual rules for naming applies.
