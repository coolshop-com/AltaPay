from __future__ import absolute_import, unicode_literals

import responses

from altapay import API, UpdateOrder

from .test_cases import TestCase


class UpdateOrderTest(TestCase):

    def setUp(self):
        self.api = API(mode='test', auto_login=False)

    @responses.activate
    def test_update_order_invalid_order_line(self):

        uo = UpdateOrder(api=self.api)

        responses.add(
            responses.POST,
            self.get_api_url('API/updateOrder'),
            body=self.load_xml_response(
                '200_update_order_success.xml'),
            status=200,
            content_type='application/xml')

        with self.assertRaisesRegexp(Exception, "order_lines must "
                                                "contain 2 elements"):
            uo.update("payment id", [])

    @responses.activate
    def test_update_order_success(self):

        uo = UpdateOrder(api=self.api)

        responses.add(
            responses.POST,
            self.get_api_url('API/updateOrder'),
            body=self.load_xml_response(
                '200_update_order_success.xml'),
            status=200,
            content_type='application/xml')

        self.assertEqual(uo.update("payment id", [{}, {}]), True)

    @responses.activate
    def test_update_order_error(self):

        uo = UpdateOrder(api=self.api)

        responses.add(
            responses.POST,
            self.get_api_url('API/updateOrder'),
            body=self.load_xml_response(
                '200_update_order_error.xml'),
            status=200,
            content_type='application/xml')

        self.assertEqual(uo.update("payment id", [{}, {}]), False)
        self.assertEqual(uo.error_code, 10000001)
        self.assertEqual(uo.error_message, "Number of original order lines "
                                           "and updated ones does not match.")
