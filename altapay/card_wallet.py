from __future__ import absolute_import, unicode_literals

import altapay.callback
from altapay.resource import Resource


class CardWallet(Resource):
    def session(self, terminal, validation_url, domain):
        """
        This is the step to receive Apple Pay session.
        By invoking this method we will reach Apple Pay with Merchant key and certificate to retrieve a session
        which should be used to proceed with Apple Pay payment.

        Returned session object should be used in session.completeMerchantValidation(JSON.parse(merchantSession));

        :arg terminal: The title of your terminal which was configured with Apple Pay
        :arg validation_url: Validation URL which was passed from requestSession ApplePayValidateMerchantEvent.validationURL
        :arg domain: The domain from which you are initializing the request, which requires to be verified.
            Otherwise, the request will use the default domain specified in the terminal.
        """
        parameters = {
            'terminal': terminal,
            'validationURL': validation_url,
            'domain': domain
        }

        response = self.api.post(
            'API/cardWallet/session', data=parameters)['APIResponse']

        return altapay.callback.Callback.from_xml_callback(response)

    def authorize(self, provider_data, terminal, shop_orderid, amount, currency, **kwargs):
        """
        This step is required to process Apple Pay data. By invoking this method we will decrypt data
        with Processing Key and Authorize it against selected acquirer.

        Returned response is similar to callback xml.

        :arg provider_data: The string value of ApplePayPaymentAuthorizedEvent.payment.token as produced by JSON.stringify()
        :arg terminal: The title of your terminal which was configured with Apple Pay
        :arg shop_orderid: The id of the order in your webshop.
            This is what we will post back to you so you know which order a given payment is associated with.
        :arg amount: The amount of the payment in english notation (ex. 89.95)
        :arg currency: The currency of the payment in ISO-4217 format.
            Either the 3- digit numeric code, or the 3- letter character code
        :arg kwargs: used for optional parameters
            The optional parameters follow the same logic as with eCommerce/API/createPaymentRequest.
            For details on usage, see the documentation for createPaymentRequest.
            Note that you will need to use lists and dictionaries to map the
            URL structures from the AltaPay documentation into these kwargs.

        :rtype: :py:class:`altapay.Callback` object.
        """
        parameters = {
            'provider_data': provider_data,
            'terminal': terminal,
            'shop_orderid': shop_orderid,
            'amount': amount,
            'currency': currency,
        }

        parameters.update(kwargs)

        response = self.api.post(
            'API/cardWallet/authorize',
            data=parameters)['APIResponse']

        return altapay.callback.Callback.from_xml_callback(response)
