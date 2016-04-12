from __future__ import absolute_import, unicode_literals

from altapay.resource import Resource


class Payment(Resource):
    def create(self, terminal, shop_orderid, amount, currency, **kwargs):
        """
        Create a payment request.

        :arg terminal: name of the targeted AltaPay terminal
        :arg shop_orderid: your order ID to be attached to the payment resource
        :arg amount: order amount in floating point
        :arg currency: currency for the payment resource
        :arg \*\*kwargs: used for remaining, optional, payment request
            parameters, see the AltaPay documentation for a full list.
            Note that you will need to use lists and dictionaries to map the
            URL structures from the AltaPay documentation into these kwargs.

        :rtype: :samp:`True` if a payment was created, otherwise :samp:`False`.
        """
        parameters = {
            'terminal': terminal,
            'shop_orderid': shop_orderid,
            'amount': amount,
            'currency': currency,
        }

        parameters.update(kwargs)

        response = self.api.post(
            'API/createPaymentRequest', data=parameters)
        self.merge_response(response)
        return self.success
