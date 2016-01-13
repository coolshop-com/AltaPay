AltaPay Python SDK
==================

This is an unofficial Python SDK for AltaPay (formerly Pensio), https://altapay.com/. The SDK is maintained by Coolshop.com, https://www.coolshop.com/.

The AltaPay Python SDK attempts to consume the AltaPay API in a clean and Pythonic way, without getting in your way. As a result, you will often find yourself thinking that the API is similar, but has been changed ever so slightly to make it easier for you to use.

As a simple example, once you have your API credentials and a terminal, it is very easy to create a payment in the test environment and get a redirect URL to the payment page.

.. code:: python

    >>> from altapay import API, Payment
    >>> api = API(mode='test', account='login', password='password')
    >>> payment = Payment(api=api)
    >>> payment.create('Test Terminal', 1234567, 13.95, 'EUR')
    >>> payment.success
    True
    >>> print(payment.url)
    'https://...'

Guide
+++++

.. toctree::
   :maxdepth: 2

   guide/introduction
   guide/create_payment
   guide/callback_handling
   guide/transactions


API Documentation
+++++++++++++++++

.. toctree::
   :maxdepth: 2

   api/api
   api/resource
   api/payment
   api/callback
   api/transaction
   api/exceptions
   api/utils


Indices and tables
++++++++++++++++++

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

