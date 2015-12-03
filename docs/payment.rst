.. _payment:

Payment
=======

Create a Payment
----------------

.. code:: python

    api = API()  # Supply credentials as per the documentation
    payment = Payment(api=api)
    payment.create('Test Terminal', 1234567, 13.95, 'USD')

    # At this point, you should redirect your customer to the URL
    # from the response, e.g.:
    redirect(payment.url)

API documentation
-----------------

.. py:module:: altapay.payment

.. autoclass:: Payment
    :members:
