from __future__ import absolute_import, unicode_literals

from altapay.resource import Resource

from .test_cases import TestCase


class ResponseTest(TestCase):
    def test_set_and_get(self):
        resource = Resource()
        resource.amount = 1.0
        self.assertEqual(resource.amount, 1.0)
        self.assertEqual(resource.__data__['amount'], 1.0)

    def test_contains(self):
        resource = Resource()
        resource.amount = 1.0
        self.assertIn('amount', resource)

    def test_merge(self):
        resource = Resource()
        resource.amount = 1.0
        body = {'currency': 'EUR'}
        resource.merge(body)
        self.assertEqual(len(resource.__data__), 2)
        self.assertEqual(resource.currency, 'EUR')

    def test_representation(self):
        resource = Resource()
        self.assertEqual(str(resource), '{}')
        resource.amount = 1.0
        self.assertEqual(str(resource), "{'amount': 1.0}")
        self.assertEqual(str(resource), repr(resource))

    def test_error(self):
        resource = Resource()
        error = {'abc': 'abc'}
        resource.__header__['error'] = error
        self.assertEqual(resource.error, error)

    def test_success(self):
        resource = Resource()
        self.assertEqual(resource.success, True)
        resource.__header__['error'] = {'abc': 'abc'}
        self.assertEqual(resource.success, False)

    def test_create_from_response(self):
        response = self.load_dict_response(
            self.load_xml_response('200_login.xml'))
        resource = Resource.create_from_response(response)
        self.assertEqual(resource.version, '20150526')
        self.assertEqual(len(resource.__header__) > 0, True)
        self.assertEqual(len(resource.__data__) > 0, True)

    def test_create_from_response_error(self):
        response = {'not': {'valid': {'altapay': {'response': None}}}}
        with self.assertRaises(ValueError):
            Resource.create_from_response(response)