.. image:: https://travis-ci.org/coolshop-com/AltaPay.svg
    :target: https://travis-ci.org/coolshop-com/AltaPay

.. image:: https://codecov.io/github/coolshop-com/AltaPay/coverage.svg?branch=master
    :target: https://codecov.io/github/coolshop-com/AltaPay?branch=master

.. image:: https://img.shields.io/pypi/v/altapay.svg
    :target: https://pypi.python.org/pypi/altapay

This is an unofficial Python SDK for AltaPay (formerly Pensio), https://altapay.com/. The SDK is maintained by Coolshop.com, https://www.coolshop.com/.

Documentation
=============
`Documentation is available at Read the Docs <http://altapay.readthedocs.org/en/latest/>`_.

Requirements
============
- Python (2.7, 3.3, 3.4, 3.5)

Other versions of Python may also be supported, but these are the only versions we test against.

Dependencies
++++++++++++
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
