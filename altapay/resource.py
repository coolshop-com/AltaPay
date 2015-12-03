from __future__ import absolute_import, unicode_literals

from . import utils


# TODO: Could we send a unique request ID through the header? If AltaPay
# logs this, it would mean that you could trace a specific request easily


class Resource(object):
    """
    Base class that maps an XML document from AltaPay into a Python like
    representation.
    """
    def __init__(self, version=None, header=None, body=None, api=None):
        self.__dict__['api'] = api  # TODO: Allow for global?

        super(Resource, self).__setattr__('version', version)
        super(Resource, self).__setattr__('__header__', header or {})
        super(Resource, self).__setattr__('__data__', {})

        self.merge(body or {})

    @classmethod
    def create_from_response(cls, response):
        try:
            api_response = response['APIResponse']
            header = api_response['Header']
            body = api_response['Body']
            return cls(
                version=api_response['@version'], header=header, body=body)
        except KeyError:
            raise ValueError('XML document was not in expected format')

    def __str__(self):
        return self.__data__.__str__()

    def __repr__(self):
        return self.__data__.__str__()

    def __getattr__(self, name):
        try:
            return self.__data__[name]
        except KeyError:
            return super(Resource, self).__getattribute__(name)

    def __setattr__(self, name, value):
        self.__data__[name] = value

    def __contains__(self, name):
        return name in self.__data__

    def merge(self, attributes):
        for key, value in attributes.items():
            setattr(
                self, utils.to_pythonic_name(key),
                self.merge(value) if isinstance(value, dict) else value)

    def merge_response(self, response):
        try:
            api_response = response['APIResponse']
            super(Resource, self).__setattr__(
                'version', api_response['@version'])
            super(Resource, self).__setattr__('header', api_response['Header'])
            self.merge(api_response['Body'] or {})
        except KeyError:
            raise ValueError('XML document was not in the expected format')

    @property
    def error(self):
        return self.__header__.get('error', {})

    @property
    def success(self):
        return len(self.error) == 0
