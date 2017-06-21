import responses

from document import Document
from scrapers.knox_tn_agendas_scraper import KnoxCoTNAgendaScraper
from . import common
from . import utils


class TestKnoxAgendaScraper(object):
    session = None
    page_str = ""

    def test_get_docs_from_page(self):
        scraper = KnoxCoTNAgendaScraper()
        docs = scraper._get_docs_from_schedule(self.page_str)
        assert len(docs) == 4
        for doc in docs:
            # All URLs should be absolute.
            assert doc.url.startswith('https://')
        actual_titles = [doc.title for doc in docs]
        expected_titles = [
            'June 28, 2017: BZA Agenda',
            'June 26, 2017: Beer Board',
            'June 19, 2017: Work Session',
            'June 7, 2017: AGENDA COMMITTEE MEETING',
        ]
        assert expected_titles == actual_titles

    def test_full_scraper(self):
        self.session.query(Document).delete()
        count = self.session.query(Document).count()
        assert count == 0
        responses.add(
            responses.GET,
            KnoxCoTNAgendaScraper.MEETING_SCHEDULE_URL,
            body=self.page_str,
            status=200
        )
        scraper = KnoxCoTNAgendaScraper()
        scraper.scrape(self.session)
        docs = self.session.query(Document).all()
        assert len(docs) == 4
        expected_titles = {
            'June 28, 2017: BZA Agenda',
            'June 26, 2017: Beer Board',
            'June 19, 2017: Work Session',
            'June 7, 2017: AGENDA COMMITTEE MEETING',
        }
        for doc in docs:
            assert doc.title in expected_titles

    @classmethod
    def setup_class(cls):
        cls.session = common.Session()

        with open(utils.get_abs_filename('knox-co-results-page.html'), 'r') as page:
            cls.page_str = page.read()

    @classmethod
    def teardown_class(cls):
        common.Session.remove()

    def setup_method(self, test_method):
        self.session.begin_nested()

    def teardown_method(self, test_method):
        self.session.rollback()
