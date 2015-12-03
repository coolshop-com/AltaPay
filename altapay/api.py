from __future__ import absolute_import, unicode_literals

import logging
import os
import platform
import ssl
from xml.etree import ElementTree

import requests
from six.moves.urllib.parse import urljoin

from . import __api_base_url__, __github_url__, __version__, exceptions, utils
from .resource import Resource

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

        # If account information is passed through the kwargs, use these
        # If not, attempt to read from the environment
        self.account = kwargs.get('account', '')
        self.password = kwargs.get('password', '')

        if not self.account or not self.password:
            self.account = os.environ.get('ALTAPAY_ACCOUNT_NAME', '')
            self.password = os.environ.get('ALTAPAY_ACCOUNT_PASSWORD', '')

        if not self.url:
            raise Exception(
                'No API URL was provided, and the selected mode could not be '
                'mapped to a default URL: ' + self.mode)  # TODO: Custom Exc?

        if auto_login:
            self.login()

    @property
    def _default_url(self):
        return __api_base_url__.get(self.mode)

    @property
    def _auth(self):
        return (self.account, self.password)

    def login(self):
        """
        Validates the account name and password against the AltaPay service.
        This method should always be called before attempting any other calls,
        and is automatically called once the `API` object is instantiated,
        unless explictly disabled.

        Raises:
            UnauthorizedAccessError: if the supplied credentials are not valid.
        """
        if self._is_authenticated:
            return

        if Resource.create_from_response(self.get('API/login')).success:
            self._is_authenticated = True
            return

        raise exceptions.UnauthorizedAccessError(
            'Credentials could not be validated against the AltaPay '
            'service.')

    def index(self):
        """
        Performs an index operation on the AltaPay service. This operation does
        not require valid API credentials, and as such can only be used to
        assert if AltaPay is responding.

        Returns:
            `True` if a valid response is returned, otherwise `False`.
        """
        return self.get('API/index')

    def _headers(self):
        return {
            'User-Agent': self.user_agent
        }

    def _request(self, url, method, params={}, headers={}):
        logger.debug('Mode: ' + self.mode)
        logger.debug('URL: ' + url)
        logger.debug('Method: ' + method)
        logger.debug('Params: ' + str(params))
        logger.debug('Headers: ' + str(headers))
        logger.debug('Is authenticated: ' + str(self._is_authenticated))

        response = requests.request(
            method, url, params=params, headers=headers, auth=self._auth)

        return self._response(response, response.content.decode('utf-8'))

    def _response(self, response, content):
        status = response.status_code

        logger.debug('Status: ' + str(status))
        logger.debug('Content: ' + content)

        if status in (200, 201):
            return utils.etree_to_dict(ElementTree.XML(content))
        elif status == 401:
            raise exceptions.UnauthorizedAccessError(
                'Credentials could not be validated against the AltaPay '
                'service.')

        raise exceptions.ResponseStatusError(
            'Response code not allowed: {status}'.format(status=status))

    def get(self, resource, parameters={}, headers={}):
        """
        Perform a GET request on the `Resource`.

        :arg resource: the resource to GET
        :arg parameters: a dictionary of GET parameters for the resource
        :arg headers: optional headers. If specified, these will override the
            default headers.

        :returns:
            A response from the AltaPay service as an `OrderedDict`.

        :raises:
            :UnauthorizedAccessError: If the supplied credentials are not
                valid.

            :ResponseStatusError: If the response code from AltaPay is not a
                subset of the allowed response codes.

        """
        return self._request(
            urljoin(self.url, resource), 'GET', params=parameters,
            headers=headers or self._headers())

    def post(self, resource, payload=None, headers={}):
        raise NotImplementedError
