from __future__ import absolute_import, unicode_literals

from .exceptions import MultipleResourcesError
from .resource import Resource


class Transaction(Resource):
    @classmethod
    def find(cls, transaction_id, api):
        """
        Find exactly one transaction by a transaction ID.

        :param transaction_id: ID of the transaction in AltaPay
        :param api: An API object which will be used for AltaPay communication.

        :rtype: :py:class:`altapay.Transaction`
        """
        response = api.get(
            'API/payments', parameters={'transaction_id': transaction_id}
        )['APIResponse']

        if isinstance(response['Body']['Transactions']['Transaction'], list):
            raise MultipleResourcesError(
                'More than one Payment was found. Total found is: {}'.format(
                    len(response['Body']['Transactions'])))

        return cls(
            response['@version'], response['Header'],
            response['Body']['Transactions']['Transaction'], api=api)

    def capture(self, **kwargs):
        """
        Capture a reservation on a transaction.

        :param \*\*kwargs: used for optional capture parameters, see the
            AltaPay documentation for a full list.
            Note that you will need to use lists and dictionaries to map the
            URL structures from the AltaPay documentation into these kwargs.
        """
        parameters = {
            'transaction_id': self.transaction_id
        }

        parameters.update(kwargs)

        response = self.api.get(
            'API/captureReservation', parameters=parameters)['APIResponse']

        super(Transaction, self).__setattr__(
            '__data__', response['Body']['Transactions']['Transaction'])

        return Transaction(
            response['@version'], response['Header'],
            response['Body']['Transactions']['Transaction'], api=self.api)
