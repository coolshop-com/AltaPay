.. _guide-introduction:

Introduction
============

The Python SDK for AltaPay attempts to make it possible to work with the AltaPay API in the most Pythonic way possible. As such, several things are slightly different, and will not match exactly to what is described in the documentation.

Noticeable differences are;

- The Python SDK is object based, with an object per resource (e.g. an :py:class:`altapay.Payment` resource). Actions are performed on these objects in order to carry out API calls in the AltaPay API
- All values that you receive from responses are accessbile as attributes on the objects. Note that if an attributes contains a dictionary, the values of this dictionary of course needs to be accessed as it is - a dictionary. If you, for whatever reason, needs access to the underlying dictionary representation, it is available at the attribute :samp:`__data__`
- To make the naming scheme feel more Pythonic, names returned by AltaPay is mapped accordingly; e.g. ``CamelCase`` becomes ``camel_case``
- In the AltaPay API, when you send parameters to calls, and these contains nested structures in the form of either arrays or hashed values, the PHP query parameter syntax is used. In the Python SDK, this has been changed to lists and dictionaries for easier use. For a concrete use case, see the payment creation examples

The API Object
++++++++++++++

All resources that expose AltaPay functionality requires an :py:class:`altapay.API` object to be passed. The object is what authenticates you to the AltaPay API service, and is also what determines whether or not you should connect to the test service or the production service.

.. code:: python

    from altapay import API

    # Create an API object that will connect to the test service
    api = API(mode='test', account='account', password='password')

    # If you instead want to create an object for production calls, simply
    # change the mode
    api = API(
        mode='production', account='account', password='password',
        shop_name='test-shop')

Optionally, the environment variables :samp:`ALTAPAY_ACCOUNT_NAME` and :samp:`ALTAPAY_ACCOUNT_PASSWORD` can be used instead of passing the account and password directly to :py:class:`altapay.API`.

The :samp:`shop_name` parameter will be used to populate the AltaPay service URL, and is not required when running in test mode.

Making an instance of :py:class:`altapay.API` will automatically attempt to do the login service call in the AltaPay API, which will verify your account and password. This is reccomended behaviour by the AltaPay service, and will only happen when the instance is created. If this is not the desired behaviour, an optional parameter :samp:`auto_login` can be set to :samp:`False` to disable the automatic login. If you do this, you should call :py:func:`altapay.API.login()` yourself before you do any other calls.
