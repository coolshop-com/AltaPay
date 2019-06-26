Change Log
----------

1.4.1 (2019-06-26)
++++++++++++++++++

** Python support **

- As of version 1.4.0, Python versions below 3.5 are no longer supported.

1.4.0 (2019-06-24)
++++++++++++++++++

**Features**

- Added ``altapay.Transaction.chargebacks()`` which returns the chargeback events as custom objects.

1.3.0 (2017-10-20)
++++++++++++++++++

**Features**

- Added ``altapay.Transaction.refund()`` with functionality for refunding a transaction, both full and partial.

1.2.1 (2016-11-02)
++++++++++++++++++

**Bugfix**

- Fixed a bug where parsing the values "nan", "inf" or "-inf" would lead to a float value, when handling XML values. While this could potentially be correct, it's safer to assume that these values are in fact string values

1.2.0 (2016-04-19)
++++++++++++++++++

**Features***

- Added ``altapay.FundingList`` and ``altapay.Funding``. These two objects will interact with the funding list features of AltaPay, and will allow you to both list all of your funding files, as well as download individual files. Currently no guide section is written on the subject, but full API documentation is available
- Added ``altapay.CustomReport`` which mimics the custom reporting module of AltaPay. Using a custom report ID and additional kwargs based on the report, you can either view or download your custom reports

1.1.0 (2016-04-12)
++++++++++++++++++

- Previously, all calls would use an HTTP GET, since the AltaPay documentation in some cases suggests that this is the case. This works, however, it breaks when payments start to contain many order lines. Because of this, all calls have been changed to HTTP POST, which is the recommended way of communicating with the AltaPay API.

1.0.1 (2016-03-15)
++++++++++++++++++

**API Change**

- **Backwards incompatible** ``altapay.Transaction.capture()`` will now return an ``altapay.Callback`` object instead of a ``altapay.Transaction`` object

1.0 (2016-03-03)
++++++++++++++++

**First Production Release**

**Features**

- Addded ``altapay.Transaction.release()``

1.0.dev9 (2016-02-26)
+++++++++++++++++++++

**Improvements**

- **Backwards incompatible** Moved ``altapay.Transaction.create_invoice_reservation()`` to ``altapay.Callback.create_invoice_reservation()``. The method will now return a ``altapay.Callback`` object in order to read the result key (#41)

1.0.dev8 (2016-02-22)
+++++++++++++++++++++

**Features**

- Added ``altapay.Transaction.create_invoice_reservation()``

1.0.dev7 (2016-02-17)
+++++++++++++++++++++

**Improvements**

- **Backwards incompatible** Changed the name of ``altapay.Transaction.reserve()`` to ``altapay.Transaction.reserve_subscription_charge()``

1.0.dev6 (2016-02-17)
+++++++++++++++++++++

**Features**

- Added ``altapay.Transaction.reserve()`` which will reserve an amount on a subscription

1.0.dev5 (2016-02-11)
+++++++++++++++++++++

**Improvements**

- **Backwards incompatible** Changed the return type of ``altapay.Transaction.charge_subscription()``. It will not return a ``altapay.Callback`` object instead of a list of transactions
- **Backwards incompatible** Changed the argument of ``altapay.Callback.transactions()`` to be keyword only. Will now accept any number of filters, and these will be matched using AND logic

1.0.dev4 (2016-02-03)
+++++++++++++++++++++

**Features**

- Added ``altapay.Transaction.charge_subscription()`` which will charge a subscription on a transaction, if this transaction is setup as a subscription

**Bugfixes**

- Fixed a bug where looking up a non-existent transaction ID would result in a ``KeyError`` (#32)

0.1.dev3 (2016-01-18)
+++++++++++++++++++++

**Bugfixes**

- Added missing apostrophe's in the documentation for the callback guide (#24)
- Fixed a bug where filtering transactions on a ``altapay.Callback`` object might result in a ``KeyError`` (#25)

**Improvements**

- Made it more explicit how attributes on response objects work (#26)

0.1.dev2 (2016-01-14)
+++++++++++++++++++++

**Features**

- Added ``altapay.Transaction`` and the ability to find a transaction by its transaction ID in the AltaPay service
- Added ``altapay.Transaction.capture()`` which captures a transaction that has already been loaded. Optinally, parameters can be passed which allows for partial captures (see the AltaPay documentation for full list of possible arguments)
- Added a public facing API for converting an AltaPay XML response (as a string) to a Python dictionary (``altapay.utils.xml_to_dict``)
- Added ``altapay.Callback`` which wraps a callback response from AltaPay, and automatically wraps the coupled transactions in ``altapay.Transaction`` objects

**Bugfixes**

- Fixed a bug where specifying a non-existing terminal while creating an ``altapay.Payment`` object would result in ``altapay.Payment.success`` returning ``True``
- Fixed a bug where running in production mode was not possible. It is now possible by specifying a shop name when instantiating the API

0.1.dev1 (2016-01-05)
+++++++++++++++++++++

- Complex payments are now possible. This means it is now possible to send detailed payment information in a Pythonic way using just lists and dictionaries, instead of the PHP style query params syntax
- Documentation now includes a small guide for available parts of the SDK, which will make is easier to get started easily without reading the raw API documentation

0.1.dev0 (2015-12-18)
+++++++++++++++++++++

- Basic API connection class implemented in ``altapay.api.API``
- Basic Payment class implemented in ``altapay.payment.Payment`` which is currently mainly for creating a very basic payment request with the AltaPay service
