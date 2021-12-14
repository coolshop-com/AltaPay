.. image:: https://travis-ci.org/coolshop-com/AltaPay.svg
    :target: https://travis-ci.org/coolshop-com/AltaPay

.. image:: https://codecov.io/github/coolshop-com/AltaPay/coverage.svg?branch=master
    :target: https://codecov.io/github/coolshop-com/AltaPay?branch=master

.. image:: https://img.shields.io/pypi/v/altapay.svg
    :target: https://pypi.python.org/pypi/altapay

This is an unofficial Python SDK for AltaPay (formerly Valitor/Pensio), https://altapay.com/. The SDK is maintained by Coolshop.com, https://www.coolshop.com/.

Requirements
============
- Python (3.6, 3.7, 3.8, 3.9)

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

Contributing
============
Currently, this library only implements the bare minimum of the AltaPay API. It will allow you to create payment links, and do basic subscription functionality. If you need anything else, feel free to submit a full request, or if you have ideas, open an issue.

If you do decide to submit a pull request, do note that both isort and flake8 (including pep8-naming) are run for all pull requests. You are also advised to write test cases.

Running the Tests
+++++++++++++++++
First of all, install supported python versions by running below command


.. code:: python

    sudo add-apt-repository -y ppa:deadsnakes/ppa && sudo apt-get install -y python3.6 python3.7 python3.8 python3.9

For installing tox and all other dependencies run below commands


.. code:: python

    python -m pip install --upgrade pip && pip install responses requests six isort flake8 nose tox

Once you have tox installed along with all dependencies, simply run:


.. code:: python

    tox

This will run all tests, against all supported Python versions.

For running integration tests only, go to **test/integration/__init__.py** and set all required values.
Then run the below command


.. code:: python

    python3 -m unittest test_merchant_api.py

Changelog
=========

See `Changelog <CHANGELOG.rst>`_ for all the release notes.

License
=======

Distributed under the MIT License. See `LICENSE <LICENSE>`_ for more information.

Documentation
=============

For more details please see `AltaPay docs <http://altapay.readthedocs.org/en/latest/>`_
