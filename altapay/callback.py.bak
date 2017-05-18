from __future__ import absolute_import, unicode_literals

from xml.etree import ElementTree

import altapay.transaction
from altapay import utils
from altapay.resource import Resource


class Callback(Resource):
    def transactions(self, **kwargs):
        """
        List all of the transactions returned by the callback.

        :param auth_type: the authentication type you wish to filter.
            Defaults to empty string, which means no filter will be made.

        :rtype: List of :py:class:`altapay.Transaction` objects.
        """
        def _check_value(element, **kwargs):
            for key, value in element.items():
                check_key = utils.to_pythonic_name(key)
                check_value = kwargs.pop(check_key, '')
                if check_value and element[key] != check_value:
                    return False
            return True

        data = self.__data__['transactions']['transaction']

        if not isinstance(data, list):
            data = [data]

        transaction_set = data

        transaction_set = [
            transaction for transaction in data
            if _check_value(transaction, **kwargs)
        ]

        return [
            altapay.transaction.Transaction(
                self.version, self.__header__, transaction)
            for transaction in transaction_set]

    @classmethod
    def create_invoice_reservation(cls, terminal, shop_orderid, amount,
                                   currency, api, **kwargs):
        """
        Create a new invoice without first creating a payment.

        :rtype: :py:class:`altapay.Transaction`
        """
        parameters = {
            'terminal': terminal,
            'shop_orderid': shop_orderid,
            'amount': amount,
            'currency': currency
        }

        parameters.update(kwargs)

        response = api.post(
            'API/createInvoiceReservation', data=parameters
        )['APIResponse']

        return cls(
            response['@version'], response['Header'], response['Body'])

    @classmethod
    def from_xml_callback(cls, callback):
        """
        Instantiate a :py:class:`altapay.Callback` object from an XML response.

        :rtype: :py:class:`altapay.Callback` instance.
        """
        if isinstance(callback, str):
            callback = ElementTree.XML(callback.encode('utf-8'))
            response = utils.etree_to_dict(callback)['APIResponse']
        elif isinstance(callback, ElementTree.Element):
            response = utils.etree_to_dict(callback)['APIResponse']
        else:
            response = callback

        return cls(
            response['@version'], response['Header'],
            response['Body'])
