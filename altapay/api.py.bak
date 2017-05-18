from __future__ import absolute_import, unicode_literals

import logging
import os
import platform
import ssl
from io import BytesIO
from xml.etree import ElementTree

import requests
from six.moves.urllib.parse import urljoin

from altapay import (__api_base_url__, __github_url__, __version__, exceptions,
                     utils)
from altapay.resource import Resource

logger = logging.getLogger(__name__)


class API(object):
    details = 'requests {requests}; python {python}; {ssl}'.format(
        requests=requests.__version__, python=platform.python_version(),
        ssl=ssl.OPENSSL_VERSION)
    user_agent = 'coolshop-com/AltaPay/{version} (+{url}; {details})'.format(
        version=__version__, url=__github_url__, details=details)
    _is_authenticated = False

    def __init__(self, **kwargs):
        """
        Instantiate an AltaPay API object.
        """
        auto_login = kwargs.get('auto_login', True)

        self.mode = kwargs.get('mode', 'test')
        self.url = kwargs.get('url', self._default_url)

        # If production mode, shop_name must be passed through kwargs, as it
        # is neede for the URL
        self.shop_name = kwargs.get('shop_name', '')
        if self.mode == 'production' and not self.shop_name:
            raise exceptions.APIError(
                'No shop_name was provided, even though production mode was '
                'specified. When running in production, a shop_name is ',
                'needed, as this is used to produce the AltaPay URL.')
        self.url = self.url.format(shop_name=self.shop_name)

        # If account information is passed through the kwargs, use these
        # If not, attempt to read from the environment
        self.account = kwargs.get('account', '')
        self.password = kwargs.get('password', '')

        if not self.account or not self.password:
            self.account = os.environ.get('ALTAPAY_ACCOUNT_NAME', '')
            self.password = os.environ.get('ALTAPAY_ACCOUNT_PASSWORD', '')

        if not self.url:
            raise exceptions.APIError(
                'No API URL was provided, and the selected mode could not be '
                'mapped to a default URL: ' + self.mode)

        if auto_login:
            self.login()

    @property
    def _default_url(self):
        return __api_base_url__.get(self.mode, '')

    @property
    def _auth(self):
        return (self.account, self.password)

    def login(self):
        """
        Validates the account name and password against the AltaPay service.
        This method should always be called before attempting any other calls,
        and is automatically called once the :py:class:`altapay.api.API`
        object is instantiated, unless explictly disabled.

        Raises:
            UnauthorizedAccessError: if the supplied credentials are not valid.
        """
        if self._is_authenticated:
            return

        if Resource.create_from_response(self.post('API/login')).success:
            self._is_authenticated = True
            return

        # Nothing at this point is intentional; if the login was not
        # successful, the HTTP response code will be 401 and result in an
        # UnauthorizedError from _response()

    def test_connection(self):
        """
        Tests the connection to the AltaPay service. This operation does
        not require valid API credentials, and as such can only be used to
        assert if AltaPay is responding.

        :rtype: :samp:`True` if a valid response is returned, otherwise
            :samp:`False`.
        """
        return Resource.create_from_response(self.post('API/testConnection'))

    def _headers(self):
        return {
            'User-Agent': self.user_agent
        }

    def _request(self, url, method, params={}, data={}, headers={}):
        logger.debug('Mode: ' + self.mode)
        logger.debug('URL: ' + url)
        logger.debug('Method: ' + method)
        logger.debug('Params: ' + str(params))
        logger.debug('Data: ' + str(data))
        logger.debug('Headers: ' + str(headers))
        logger.debug('Is authenticated: ' + str(self._is_authenticated))

        response = requests.request(
            method, url, params=params, data=data, headers=headers,
            auth=self._auth)

        return self._response(response, response.content.decode('utf-8'))

    def _response(self, response, content):
        status = response.status_code

        logger.debug('Status: ' + str(status))
        logger.debug('Content: ' + content)

        if status in (200, 201):
            return utils.etree_to_dict(
                ElementTree.XML(content.encode('utf-8')))
        elif status == 401:
            raise exceptions.UnauthorizedAccessError(
                'Credentials could not be validated against the AltaPay '
                'service.')
        elif 500 <= status <= 599:
            raise exceptions.ServerError(
                'AltaPay service server error. Response code was: {}'
                .format(status))

        raise exceptions.ResponseStatusError(
            'Response code not allowed: {status}'.format(status=status))

    def get(self, resource, parameters={}, headers={}):
        """
        Perform a GET HTTP request on a resource.

        :arg resource: the resource to GET
        :arg parameters: a dictionary of GET parameters for the resource
        :arg headers: optional headers. If specified, these will override the
            default headers.

        :returns:
            A response from the AltaPay service as a :samp:`dict`.

        :raises:
            :UnauthorizedAccessError: If the supplied credentials are not
                valid.

            :ResponseStatusError: If the response code from AltaPay is not a
                subset of the allowed response codes.

        """
        return self._request(
            urljoin(self.url, resource), 'GET',
            params=utils.http_build_query(parameters),
            headers=headers or self._headers())

    def post(self, resource, parameters={}, data={}, headers={}):
        """
        Perform a POST HTTP requeste on a resource.

        :arg resource: the resource to POST to
        :arg parameters: a dictionary of GET parameters for the resource
        :arg data: a dictionary of POST parameters for the resource
        :arg headers: optional headers. If specified, these will override the
            default headers.

        :returns:
            A response from the AltaPay service as a :samp:`dict`.

        :raises:
            :UnauthorizedAccessError: If the supplied credentials are not
                valid.

            :ResponseStatusError: If the response code from AltaPay is not a
                subset of the allowed response codes.

        """
        return self._request(
            urljoin(self.url, resource), 'POST',
            params=utils.http_build_query(parameters),
            data=utils.http_build_query_dict(data),
            headers=headers or self._headers())

    def download(self, resource, parameters={}, headers={}):
        """
        Downloads a resource. Acts as a custom HTTP GET.
        Not that it is considered the callers responsibility to actually
        flush/close the stream.
        """
        response = requests.get(
            resource, params=utils.http_build_query(parameters), stream=True,
            headers=headers or self._headers(), auth=self._auth)
        return BytesIO(response.content)
