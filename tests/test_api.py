from __future__ import absolute_import, unicode_literals

import responses
from altapay import API, exceptions

from .test_cases import TestCase

DATA = locals()


class APITest(TestCase):
    def setUp(self):
        self.api = API(mode='test', auto_login=False)

    def test_test_connection_successful(self):
        self.assertEqual(self.api.test_connection().success, True)

    @responses.activate
    def test_login_successful(self):
        "Mocks a login response to be successful to test authentication state"
        responses.add(
            responses.POST, self.get_api_url('API/login'),
            body=self.load_xml_response('200_login.xml'),
            status=200, content_type='application/xml')
        api = API(
            mode='test', account='test', password='test', auto_login=False)
        # Before login is called state should be not authenticated
        self.assertEqual(api._is_authenticated, False)
        api.login()
        # State should be authenticated after the login
        self.assertEqual(api._is_authenticated, True)

        # Use a response callback to assert whether or not login attempts
        # to log in again even if the object is already in an authenticated
        # state. This is done by setting a state in thread locals, if we ever
        # reach this point in the code. Bit of a hack.
        def http_callback(request):
            content = self.load_xml_response('200_login.xml')
            headers = {
                'content-type': 'application/xml',
            }
            DATA.callback_reached = True
            return (200, headers, content)

        responses.reset()
        responses.add_callback(
            responses.POST, self.get_api_url('API/login'),
            callback=http_callback, content_type='application/xml')
        api.login()
        self.assertEqual(getattr(DATA, 'callback_reached', None), None)

    def test_login_unauthorized(self):
        with self.assertRaises(exceptions.UnauthorizedAccessError):
            self.api.login()

    def test_headers(self):
        self.assertIsInstance(self.api._headers(), dict)
        self.assertIn('User-Agent', self.api._headers())

    def test_auto_login(self):
        with self.assertRaises(exceptions.UnauthorizedAccessError):
            API()

    def test_missing_url(self):
        with self.assertRaises(exceptions.APIError):
            API(auto_login=False, mode='notworking')

    def test_production_missing_shop_name(self):
        with self.assertRaises(exceptions.APIError):
            API(auto_login=False, mode='production')

    def test_production_shop_name(self):
        api = API(auto_login=False, mode='production', shop_name='test-shop')
        self.assertIn('test-shop', api.url)

    @responses.activate
    def test_http_response_code_not_supported(self):
        # Use a random unsupported HTTP Status Code here
        responses.add(
            responses.POST, self.get_api_url('API/notReal'),
            body='', status=402, content_type='application/xml')
        with self.assertRaises(exceptions.ResponseStatusError):
            self.api._request(
                self.get_api_url('API/notReal'), 'POST')

    @responses.activate
    def test_http_response_code_500(self):
        responses.add(
            responses.POST, self.get_api_url('API/notReal'),
            body='', status=500, content_type='application/xml')
        with self.assertRaises(exceptions.ServerError):
            self.api._request(
                self.get_api_url('API/notReal'), 'POST')
