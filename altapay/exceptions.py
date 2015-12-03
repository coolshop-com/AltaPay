from __future__ import absolute_import, unicode_literals


class AltaPayException(Exception):
    """
    Generic exception class for the AltaPay SDK. All specific exceptions raised
    from the SDK will inherit from this exceptions.
    """
    pass


class UnauthorizedAccessError(AltaPayException):
    """
    Raised on unauthorized errors against the AltaPay service.

    Corresponds to HTTP status code 401.
    """
    pass


class ResponseStatusError(AltaPayException):
    """
    The response carried out against the AltaPay service did not respond with
    the expected response status code.
    """
    pass
