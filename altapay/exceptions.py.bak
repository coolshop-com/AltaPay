from __future__ import absolute_import, unicode_literals


class AltaPayException(Exception):
    """
    Generic exception class for the AltaPay SDK. All specific exceptions raised
    from the SDK will inherit from this exceptions.
    """


class APIError(AltaPayException):
    """
    Raised if the API object could not be configured with the given parameters.
    """


class UnauthorizedAccessError(AltaPayException):
    """
    Raised on unauthorized errors against the AltaPay service.

    Corresponds to HTTP status code 401.
    """


class ResponseStatusError(AltaPayException):
    """
    The response carried out against the AltaPay service did not respond with
    the expected response status code.
    """


class ServerError(AltaPayException):
    """
    Raised when an error in the 500 range is returned from the AltaPay service.
    """


class MultipleResourcesError(AltaPayException):
    """
    Raised if more than one Resource was found when attempting to look up a
    single resource.
    """


class ResourceNotFoundError(AltaPayException):
    """
    Raised if a resource is not found.
    """
