from __future__ import absolute_import, unicode_literals

from altapay.payment import Payment


class Invoice(Payment):
    def create(self, terminal, shop_orderid, amount, currency, **kwargs):
        """
        Create a invoice reservation request.

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

        return super(Invoice, self).create(terminal, shop_orderid,
                                           amount, currency, **kwargs)

    def get_post_url(self):
        return 'API/createInvoiceReservation'
