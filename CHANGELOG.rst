Change Log
----------

0.1.dev2 (2015-01-XX)
+++++++++++++++++++++

**Features**

- Added ``altapay.api.Transaction`` and the ability to find a transaction by its transaction ID in the AltaPay service

**Bugfixes**

- Fixed a bug where specifying a non-existing terminal while creating an ``altapay.Payment`` object would result in ``altapay.Payment.success`` returning ``True``

0.1.dev1 (2015-01-05)
+++++++++++++++++++++

- Complex payments are now possible. This means it is now possible to send detailed payment information in a Pythonic way using just lists and dictionaries, instead of the PHP style query params syntax
- Documentation now includes a small guide for available parts of the SDK, which will make is easier to get started easily without reading the raw API documentation

0.1.dev0 (2015-12-18)
+++++++++++++++++++++

- Basic API connection class implemented in ``altapay.api.API``
- Basic Payment class implemented in ``altapay.payment.Payment`` which is currently mainly for creating a very basic payment request with the AltaPay service
