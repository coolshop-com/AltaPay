from __future__ import absolute_import, unicode_literals

import os

import responses

from altapay import API, CustomReport, Funding, FundingList, exceptions

from .test_cases import TestCase


class FundingListTest(TestCase):
    @responses.activate
    def setUp(self):
        self.api = API(mode='test', auto_login=False)
        responses.add(
            responses.GET, self.get_api_url('API/fundingList/'),
            body=self.load_xml_response('200_funding_list_page_0.xml'),
            status=200, content_type='application/xml')
        self.funding_list = FundingList(api=self.api)

    def test_fundings(self):
        self.assertEqual(len(self.funding_list.fundings), 2)
        for funding in self.funding_list.fundings:
            self.assertIsInstance(funding, Funding)

    def test_number_of_pages(self):
        self.assertEqual(self.funding_list.number_of_pages, 2)

    @responses.activate
    def test_next_page(self):
        responses.add(
            responses.GET, self.get_api_url('API/fundingList/'),
            body=self.load_xml_response('200_funding_list_page_0.xml'),
            status=200, content_type='application/xml')
        self.assertEqual(self.funding_list._current_page, 0)
        self.funding_list.next_page()
        self.assertEqual(self.funding_list._current_page, 1)
        self.assertEqual(len(self.funding_list.fundings), 2)

        # Test it's not possible to scroll past the end of the funding list
        with self.assertRaises(exceptions.ResourceNotFoundError):
            self.funding_list.next_page()


class FundingTest(TestCase):
    @responses.activate
    def setUp(self):
        self.api = API(mode='test', auto_login=False)
        responses.add(
            responses.GET, self.get_api_url('API/fundingList/'),
            body=self.load_xml_response('200_funding_list_page_0.xml'),
            status=200, content_type='application/xml')
        self.funding_list = FundingList(api=self.api)

    @responses.activate
    def test_content(self):
        responses.add(
            responses.GET, self.get_api_url('API/fundingDownload'),
            body=self.load_xml_response('200_funding.csv'),
            status=200, content_type='text/plain')
        funding = self.funding_list.fundings[0]
        content = funding.content()
        self.assertGreater(len(content), 1)

    @responses.activate
    def test_download(self):
        responses.add(
            responses.GET, self.get_api_url('API/fundingDownload'),
            body=self.load_xml_response('200_funding.csv'),
            status=200, content_type='text/plain')
        funding = self.funding_list.fundings[0]
        filepath = funding.download('./')
        self.assertEqual(filepath, './CreatedByTest.csv')
        content = None
        with open(filepath, 'rb') as fd:
            content = fd.read()
        self.assertEqual(content, funding.content())
        os.remove(filepath)


class CustomReportTest(TestCase):
    @responses.activate
    def setUp(self):
        self.api = API(mode='test', auto_login=False)
        url = '{}?id={}&from_date={}&to_date={}'.format(
            self.get_api_url('API/getCustomReport'),
            'ABCDEF',
            '2016-01-01',
            '2016-01-05')
        # Use the standard funding file response, any CSV could go here
        responses.add(
            responses.GET, url,
            body=self.load_xml_response('200_funding.csv'),
            status=200, content_type='text/plain',
            match_querystring=True)
        self.report = CustomReport(
            'ABCDEF', self.api, from_date='2016-01-01', to_date='2016-01-05')

    def test_content(self):
        self.assertGreater(len(self.report.content()), 1)

    def test_download(self):
        filename = './test.csv'
        self.report.download(filename)
        content = None
        with open(filename, 'rb') as fd:
            content = fd.read()
        self.assertEqual(content, self.report.content())
        os.remove(filename)
