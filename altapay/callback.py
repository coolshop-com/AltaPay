from __future__ import absolute_import, unicode_literals

from xml.etree import ElementTree

from . import utils
from .resource import Resource
from .transaction import Transaction


class Callback(Resource):
    def transactions(self, auth_type=''):
        """
        List all of the transactions returned by the callback.

        :param auth_type: the authentication type you wish to filter.
            Defaults to empty string, which means no filter will be made.

        :rtype: List of :py:class:`altapay.Transaction` objects.
        """
        data = self.__data__['transactions']['transaction']

        if not isinstance(data, list):
            data = [data]

        transaction_set = data

        if auth_type:
            transaction_set = [
                transaction for transaction in data
                if auth_type in (
                    transaction.get('AuthType', ''),
                    transaction.get('auth_type', ''))
            ]

        return [
            Transaction(self.version, self.__header__, transaction)
            for transaction in transaction_set]

    @classmethod
    def from_xml_callback(cls, callback):
        """
        Instantiate a :py:class:`altapay.Callback` object from an XML response.

        :rtype: :py:class:`altapay.Callback` instance.
        """
        if not isinstance(callback, ElementTree.Element):
            callback = ElementTree.XML(callback)

        response = utils.etree_to_dict(callback)['APIResponse']

        return cls(
            response['@version'], response['Header'],
            response['Body'])
