from __future__ import absolute_import, unicode_literals

from .resource import Resource


class Payment(Resource):
    def create(self, terminal, shop_orderid, amount, currency, **kwargs):
        """
        Create a payment request.

        :arg terminal: name of the targeted AltaPay terminal
        :arg shop_orderid: your order ID to be attached to the payment resource
        :arg amount: order amount in floating point
        :arg currency: currency for the payment resource
        """

        parameters = {
            'terminal': terminal,
            'shop_orderid': shop_orderid,
            'amount': amount,
            'currency': currency,
        }

        parameters.update(kwargs)

        response = self.api.get(
            'API/createPaymentRequest', parameters=parameters)
        self.merge_response(response)
        return self.success
