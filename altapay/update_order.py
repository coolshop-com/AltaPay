from __future__ import absolute_import, unicode_literals

from altapay.resource import Resource


class UpdateOrder(Resource):

    def update(self, payment_id, order_lines):
        """
        Creates an update order request.

        This is used when you want to replace order lines.

        The limitations are that:

        * This feature is only available for Invoice payments
        * The unwanted order lines must be either in a captured or refunded
        state
        * Discount, TaxAmount, TaxPercent, and UnitPrice must be the same
        for the original and the replacement order line
        * Quantity must be the same in both the original (the one be
        replaced) and the replacement order line, but the original must be
        negative.
        .. note:: updateOrder is currently only supported by Klarna, and
        updating one order line at a time.

        :arg payment_id: The id of a specific payment.
        :arg order_lines: List of order lines. The original orderlines
        (the ones to be replaced) must be set with negative quantity
        :rtype: :samp:`True` in the case of a success, otherwise :samp:`False`.
        """
        parameters = {
            'payment_id': payment_id,
            'orderLines': order_lines
        }

        response = self.api.post(
            self.get_post_url(), data=parameters)

        self.merge_response(response)

        return self.success

    def get_post_url(self):
        return 'API/updateOrder'

    @property
    def success(self):
        return self.error_code == 0 and self.result == 'Success'
