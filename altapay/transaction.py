from __future__ import absolute_import, unicode_literals

import altapay.callback
from altapay import exceptions
from altapay.resource import Resource


class Transaction(Resource):
    @classmethod
    def find(cls, transaction_id, api):
        """
        Find exactly one transaction by a transaction ID.

        :arg transaction_id: ID of the transaction in AltaPay
        :arg api: An API object which will be used for AltaPay communication.

        :rtype: :py:class:`altapay.Transaction`
        """
        response = api.post(
            'API/payments', data={'transaction_id': transaction_id}
        )['APIResponse']

        try:
            transaction = response['Body']['Transactions']['Transaction']
        except KeyError:
            raise exceptions.ResourceNotFoundError(
                'No Transaction found matching transaction ID: {}'.format(
                    transaction_id))

        if isinstance(transaction, list):
            raise exceptions.MultipleResourcesError(
                'More than one Payment was found. Total found is: {}'.format(
                    len(response['Body']['Transactions'])))

        return cls(
            response['@version'], response['Header'], transaction, api=api)

    def capture(self, **kwargs):
        """
        Capture a reservation on a transaction.

        :arg \*\*kwargs: used for optional capture parameters, see the
            AltaPay documentation for a full list.
            Note that you will need to use lists and dictionaries to map the
            URL structures from the AltaPay documentation into these kwargs.

        :rtype: :py:class:`altapay.Callback` object.
        """
        parameters = {
            'transaction_id': self.transaction_id
        }

        parameters.update(kwargs)

        response = self.api.post(
            'API/captureReservation', data=parameters)['APIResponse']

        return altapay.callback.Callback.from_xml_callback(response)

    def charge_subscription(self, **kwargs):
        """
        This will charge a subscription using a capture. Can be called many
        times on a subscription.

        If amount is not sent as an optinal parameter, the amount specified in
        the original setup of the subscription will be used.

        :arg \*\*kwargs: used for optional charge subscription parameters,
            see the AltaPay documentation for a full list.
            Note that you will need to use lists and dictionaries to map the
            URL structures from the AltaPay documentation into these kwargs.

        :rtype: :py:class:`altapay.Callback` object.
        """
        parameters = {
            'transaction_id': self.transaction_id
        }

        parameters.update(kwargs)

        response = self.api.post(
            'API/chargeSubscription', data=parameters)['APIResponse']

        return altapay.callback.Callback.from_xml_callback(response)

    def reserve_subscription_charge(self, **kwargs):
        """
        This will create a reservation on a subscription. Can be called many
        times on a subscription.

        If amount is not sent as an optinal parameter, the amount specified in
        the original setup of the subscription will be used.

        :arg \*\*kwargs: used for optional reserve subscription parameters,
            see the AltaPay documentation for a full list.
            Note that you will need to use lists and dictionaries to map the
            URL structures from the AltaPay documentation into these kwargs.

        :rtype: :py:class:`altapay.Callback` object.
        """
        parameters = {
            'transaction_id': self.transaction_id
        }

        parameters.update(kwargs)

        response = self.api.post(
            'API/reserveSubscriptionCharge',
            data=parameters)['APIResponse']

        return altapay.callback.Callback.from_xml_callback(response)

    def release(self):
        """
        This will release the reservation on the transaction. This is useful
        if you for whatever reason do not want to capture the payment.

        Refer to the AltaPay documentation for edge cases surround this method.

        :rtype: :py:class:`altapay.Callback` object.
        """
        parameters = {
            'transaction_id': self.transaction_id
        }

        response = self.api.post(
            'API/releaseReservation', data=parameters)['APIResponse']

        return altapay.callback.Callback.from_xml_callback(response)
