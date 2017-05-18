from __future__ import absolute_import, unicode_literals

import os

from six.moves.urllib.parse import urljoin

from altapay import exceptions
from altapay.callback import Callback
from altapay.resource import Resource


class CustomReport(object):
    """
    Custom AltaPay report.
    """

    def __init__(self, report_id, api, **kwargs):
        """
        Access a custom AltaPay report.

        :arg report_id: ID if the AltaPay report
        :arg kwargs: additional parameters that needs to be passed to the
            report, e.g. from_date and to_date
        """
        parameters = {
            'id': report_id
        }
        parameters.update(kwargs)
        self._content = api.download(
            urljoin(api.url, 'API/getCustomReport'),
            parameters=parameters).read()

    def download(self, filename):
        """
        Download the CSV report.

        :arg filename: full filename including path where the report will be
            downloaded.
        """
        with open(filename, 'wb') as fd:
            fd.write(self.content())

    def content(self):
        """The report content as bytes."""
        return self._content


class Funding(Resource):
    """
    A funding file that can be either viewed or downloaded.
    """

    def download(self, save_to):
        """
        Download the CSV funding file.

        :arg save_to: the path to save the funding file to. The filename will
            match the name of the file at AltaPay, and will have the extension
            .csv attached.

        :rtype: a string with the complete filepath to the CSV funding file
        """
        filepath = os.path.join(save_to, self.filename) + '.csv'
        with open(filepath, 'wb') as fd:
            fd.write(self.content())
        return filepath

    def content(self):
        """The funding file content as bytes."""
        return self.api.download(self.download_link).read()


class FundingList(object):
    """
    A list of funding files to paginate through.
    """

    _fundings = []
    _current_page = 0
    _api = None
    _number_of_pages = None

    def __init__(self, api):
        """
        Retrieve the first page of the funding list.

        :arg api: An API object which will be used for AltaPay communication.
        """
        self._api = api
        self._load_page()

    def _load_page(self):
        response = self._api.post(
            'API/fundingList/', data={'page': self._current_page}
        )['APIResponse']
        callback = Callback.from_xml_callback(response)
        self._fundings = [
            Funding(
                response['@version'], response['Header'], funding,
                api=self._api)
            for funding in callback.fundings['funding']
        ]
        self._number_of_pages = callback.fundings['@number_of_pages']

    def next_page(self):
        """
        Loads the next page of funding files.

        Raises:
            :py:class:`altapay.exceptions.ResourceNotFoundError`:
            if the next page is not available, typically meaning you have
            scrolled past the available pages.
        """
        # The first current page is called 0
        if self._current_page + 1 > self._number_of_pages - 1:
            raise exceptions.ResourceNotFoundError(
                'Requested funding page does not exist.')
        self._current_page += 1
        self._load_page()

    @property
    def fundings(self):
        """
        :py:class:`altapay.Funding` objects on the current page of
        funding files.
        """
        return self._fundings

    @property
    def number_of_pages(self):
        """
        Returns the total amount of pages with fundings. Each page can hold
        100 fundings.
        """
        return self._number_of_pages
