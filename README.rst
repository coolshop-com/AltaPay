.. image:: https://travis-ci.org/coolshop-com/AltaPay.svg
    :target: https://travis-ci.org/coolshop-com/AltaPay

.. image:: https://codecov.io/github/coolshop-com/AltaPay/coverage.svg?branch=master
    :target: https://codecov.io/github/coolshop-com/AltaPay?branch=master

.. image:: https://img.shields.io/pypi/v/altapay.svg
    :target: https://pypi.python.org/pypi/altapay

This is an unofficial Python SDK for Valitor (formerly AltaPay/Pensio), https://altapay.com/. The SDK is maintained by Coolshop.com, https://www.coolshop.com/.

Requirements
============
- Python (3.5, 3.6, 3.7, 3.8)

Other versions of Python may also be supported, but these are the only versions we test against.

Dependencies
++++++++++++
- responses
- requests
- six

Installation
============
The easiest way is using pip.

.. code:: python

    pip install altapay

Getting Started
===============
Refer to the `introduction on the documentation <http://altapay.readthedocs.org/en/latest/>`_ for some getting started use cases.

Contributing
============
Currently, this library only implements the bare minimum of the AltaPay API. It will allow you to create payment links, and do basic subscription functionality. If you need anything else, feel free to submit a full request, or if you have ideas, open an issue.

If you do decide to submit a pull request, do note that both isort and flake8 (including pep8-naming) are run for all pull requests. You are also advised to write test cases.

Running the Tests
+++++++++++++++++
First of all, have `tox <http://tox.readthedocs.org/en/latest/>`_ installed on your system. System-wide is probably the better choice. Once you have tox installed, simply run:

.. code:: python

    tox

This will run all tests, against all supported Python versions.

For running integration tests, go to test/integration/__init__.py and set all required values.
Then run the below command

`python3 -m unittest test_merchant_api.py`

Changelog
=========

See `Changelog <CHANGELOG.rst>`_ for all the release notes.

License
=======

Distributed under the MIT License. See `LICENSE <LICENSE>`_ for more information.

Documentation
=============

For more details please see `AltaPay docs <http://altapay.readthedocs.org/en/latest/>`_

Contact
=======
Feel free to contact our support team (support@altapay.com) if you need any assistance.