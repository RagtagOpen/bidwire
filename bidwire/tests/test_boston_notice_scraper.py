import os
import csv
from lxml import html
from urllib.parse import urljoin
from scrapers.boston_notice_scraper import BostonNoticeScraper
from . import common


class TestBostonNoticeScraper(object):
    session = None
    page_str = ""
    notice_strs = {}
    expected_docs = []

    def test_scrape(self):
        scraper = BostonNoticeScraper()

        def scrape_desc(href):
            try:
                return scraper.scrape_desc_page(self.notice_strs[href])
            except KeyError:
                return
        scraper.scrape_desc = scrape_desc

        assert [
            [doc.url, doc.title] for doc in
            scraper.scrape_notices_page_and_notices(self.session, html.fromstring(self.page_str))
        ] == self.expected_docs

    @classmethod
    def setup_class(cls):
        cls.session = common.Session()
        with open('bidwire/tests/boston_public_notices_expected.csv') as inf:
            cls.expected_docs = list(csv.reader(inf))
        for fn in os.listdir('bidwire/tests/boston_public_notices'):
            with open(os.path.join('bidwire/tests/boston_public_notices', fn)) as inf:
                if fn == 'index.html':
                    cls.page_str = inf.read()
                else:
                    cls.notice_strs[
                        urljoin(BostonNoticeScraper.ROOT_URL, BostonNoticeScraper.NOTICES_URL + '/' + fn)
                    ] = cls.notice_strs[fn + '.html'] = inf.read()

    @classmethod
    def teardown_class(cls):
        common.Session.remove()
