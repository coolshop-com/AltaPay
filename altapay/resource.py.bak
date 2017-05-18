from __future__ import absolute_import, unicode_literals

from altapay import utils


class Resource(object):
    """
    Base class that maps an AltaPay response into a Python like representation.
    """
    def __init__(self, version=None, header=None, body=None, api=None):
        self.__dict__['api'] = api

        super(Resource, self).__setattr__('version', version)
        super(Resource, self).__setattr__('__header__', header or {})
        super(Resource, self).__setattr__('__data__', {})

        self.merge(body or {})

    @classmethod
    def create_from_response(cls, response):
        """
        Instantiate a new :py:class:`altapay.Resource` object from
        a response.

        :arg response: a response of type :samp:`dict`. The response most
            conform to the AltaPay response format, which means it must carry
            four keys called :samp:`@version`, :samp:`APIResponse`,
            :samp:`Header` and :samp:`Body`.

        :rtype: a new version object of type
            :py:class:`altapay.Resource`.
        """
        try:
            api_response = response['APIResponse']
            header = utils.to_pythonic_dict(api_response['Header'])
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
                utils.to_pythonic_dict(value)
                if isinstance(value, dict) else value)

    def merge_response(self, response):
        try:
            api_response = response['APIResponse']
            super(Resource, self).__setattr__(
                'version', api_response['@version'])
            super(Resource, self).__setattr__(
                '__header__', utils.to_pythonic_dict(api_response['Header']))
            self.merge(api_response['Body'] or {})
        except KeyError:
            raise ValueError('XML document was not in the expected format')

    @property
    def error(self):
        error_code = int(self.__header__.get('error_code', 0))
        error_message = self.__header__.get('error_message', '')

        return {
            'code': error_code,
            'message': error_message
        }

    @property
    def success(self):
        return self.error['code'] == 0
